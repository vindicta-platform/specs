"""Speckit Clarify - Automated spec clarification on merge.

Runs the speckit-clarify workflow taxonomy scan against changed spec.md files,
uses Ollama (local model, default: mistral) to identify ambiguities, auto-accepts
recommended clarifications, updates the spec, and creates a PR with changes.

Designed to run in GitHub Actions after a spec.md is merged into main.
Zero paid LLM tokens — uses only local Ollama models.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import ollama  # type: ignore[import-untyped]
from github import Auth, Github  # type: ignore[import-untyped]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = os.environ.get("SPECKIT_MODEL", "mistral")
MAX_QUESTIONS = 5

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def ask_ollama(prompt: str) -> str:
    """Send a prompt to Ollama and return the response text."""
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"].strip()  # type: ignore[no-any-return]
    except Exception:
        log.exception("Ollama request failed")
        return ""


def _extract_json_array(raw: str) -> list[dict[str, str]] | None:
    """Try multiple strategies to extract a JSON array from LLM output."""
    import re

    # Strategy 1: Markdown code fence
    if "```json" in raw:
        json_str = raw.split("```json")[1].split("```")[0].strip()
        try:
            result = json.loads(json_str)
            if isinstance(result, list):
                return result  # type: ignore[no-any-return]
        except json.JSONDecodeError:
            pass

    # Strategy 2: Any code fence
    if "```" in raw:
        parts = raw.split("```")
        for i in range(1, len(parts), 2):  # odd indices are inside fences
            try:
                result = json.loads(parts[i].strip())
                if isinstance(result, list):
                    return result  # type: ignore[no-any-return]
            except json.JSONDecodeError:
                continue

    # Strategy 3: Find the outermost [ ... ] bracket pair
    bracket_match = re.search(r"\[.*\]", raw, re.DOTALL)
    if bracket_match:
        try:
            result = json.loads(bracket_match.group())
            if isinstance(result, list):
                return result  # type: ignore[no-any-return]
        except json.JSONDecodeError:
            pass

    # Strategy 4: Line-by-line search for arrays
    for line in raw.split("\n"):
        line = line.strip()
        if line.startswith("["):
            try:
                result = json.loads(line)
                if isinstance(result, list):
                    return result  # type: ignore[no-any-return]
            except json.JSONDecodeError:
                continue

    return None


def scan_spec(
    spec_path: Path, spec_content: str, max_retries: int = 2
) -> list[dict[str, str]]:
    """Scan a spec for ambiguities using the `.specify` workflow files and sibling context."""

    # 1. Load root context (.specify)
    repo_root = spec_path.parent.parent
    specify_dir = repo_root / ".specify"

    constitution = ""
    constitution_path = specify_dir / "memory" / "constitution.md"
    if constitution_path.exists():
        constitution = constitution_path.read_text(encoding="utf-8")

    template_str = ""
    template_path = specify_dir / "templates" / "spec-template.md"
    if template_path.exists():
        template_str = template_path.read_text(encoding="utf-8")

    # 2. Load sibling feature files (Exclude downstream artifacts)
    sibling_context = ""
    for sibling in spec_path.parent.glob("*.md"):
        if sibling.name not in ("spec.md", "plan.md", "tasks.md"):
            try:
                content = sibling.read_text(encoding="utf-8")
                # Truncate to avoid overloading the context window
                if len(content) > 2000:
                    content = content[:2000] + "\n... (truncated)"
                sibling_context += f"--- {sibling.name} ---\n{content}\n\n"
            except Exception:
                pass

    prompt = dedent(f"""\
        You are a specification analyst. Analyze the following feature specification
        for ambiguities, missing information, underspecified areas, or contradictions.
        
        Rely on the following project context and workflow files to evaluate the spec:
        
        === PROJECT CONSTITUTION ===
        {constitution}
        
        === SPECIFICATION TEMPLATE ===
        {template_str}
        
        === ADDITIONAL FEATURE CONTEXT ===
        {sibling_context}
        
        Based on these workflow boundaries, evaluate if the spec is ambiguous or requires clarification.
        Generate up to {MAX_QUESTIONS} clarification questions. Each question MUST:
        1. Be answerable with a short answer (<=5 words) or a choice from 2-5 options.
        2. Materially impact architecture, data modeling, or test design.
        3. Include your RECOMMENDED answer based on best practices.
        4. MUST NOT contradict any existing assumptions, examples, or requirements in the spec itself. Pay critical attention to existing metrics, scoring scales, or values in Acceptance Criteria, and assure your recommendations align perfectly with them.

        
        CRITICAL: Return ONLY a valid JSON array. No prose before or after.
        Each object must have exactly these fields:
        - "category": string (e.g., "Data Model", "Scoring Logic", "Edge Case")
        - "status": string ("Partial" or "Missing")
        - "question": string (the clarification question)
        - "recommended_answer": string (your recommendation)
        - "reasoning": string (1-2 sentences explaining why the clarity matters)

        If no meaningful ambiguities exist, return: []

        --- SPEC START ---
        {spec_content}
        --- SPEC END ---
    """)

    for attempt in range(1, max_retries + 1):
        log.info("Scan attempt %d/%d...", attempt, max_retries)
        raw = ask_ollama(prompt)
        if not raw:
            log.warning("Empty response from Ollama on attempt %d", attempt)
            continue

        questions = _extract_json_array(raw)
        if questions is not None:
            # Validate structure
            valid = []
            for q in questions:
                if isinstance(q, dict) and "question" in q:
                    valid.append(q)
            if valid:
                return valid[:MAX_QUESTIONS]
            log.info("Parsed JSON but no valid question objects found")
            return []

        log.warning(
            "Failed to parse JSON on attempt %d. Raw response (first 500 chars): %s",
            attempt,
            raw[:500],
        )

    log.error("All %d scan attempts failed to produce valid JSON", max_retries)
    return []


def apply_clarifications(
    spec_content: str,
    questions: list[dict[str, str]],
    today: str,
) -> str:
    """Apply auto-accepted clarifications to the spec content.

    Uses deterministic, append-only logic — no LLM-based rewriting.
    Inserts a `## Clarifications` section with structured Q&A bullets
    and a per-category detail block with reasoning.
    """
    if not questions:
        return spec_content

    # Build the Q&A bullets
    qa_bullets = []
    for q in questions:
        question = q.get("question", "Unknown")
        answer = q.get("recommended_answer", "See recommendation")
        qa_bullets.append(f"- Q: {question} → A: {answer}")

    # Build the detailed category breakdown
    detail_lines = []
    for q in questions:
        category = q.get("category", "Unknown")
        status = q.get("status", "Unknown")
        question = q.get("question", "Unknown")
        answer = q.get("recommended_answer", "See recommendation")
        reasoning = q.get("reasoning", "")
        detail_lines.append(
            f"- **{category}** ({status}): {question}\n"
            f"  - **Answer**: {answer}\n"
            f"  - **Rationale**: {reasoning}"
        )

    session_block = (
        f"\n### Session {today} (Automated)\n\n"
        + "\n".join(qa_bullets)
        + "\n\n#### Detail\n\n"
        + "\n".join(detail_lines)
        + "\n"
    )

    # Insert or append to Clarifications section
    if "## Clarifications" in spec_content:
        # Append new session under existing Clarifications section
        parts = spec_content.split("## Clarifications", 1)
        remaining = parts[1]
        # Find the next ## section (not ###)
        next_h2_idx = remaining.find("\n## ", 1)
        if next_h2_idx == -1:
            # No subsequent H2 — append at end of Clarifications
            return parts[0] + "## Clarifications" + remaining + session_block
        else:
            return (
                parts[0]
                + "## Clarifications"
                + remaining[:next_h2_idx]
                + session_block
                + remaining[next_h2_idx:]
            )

    # No existing Clarifications section — insert before the last ## section
    # (keeps it near the end of the spec, before Edge Cases / Revisions)
    lines = spec_content.split("\n")
    last_h2_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("## "):
            last_h2_idx = i
            break

    clarifications_block = "\n## Clarifications\n" + session_block

    if last_h2_idx > 0:
        before = "\n".join(lines[:last_h2_idx])
        after = "\n".join(lines[last_h2_idx:])
        return before + clarifications_block + "\n" + after
    else:
        # No H2 sections at all — append to end
        return spec_content + clarifications_block


def create_branch_and_pr(
    gh: Github,
    repo_name: str,
    spec_path: str,
    updated_content: str,
    feature_dir: str,
    commit_sha: str,
    num_questions: int,
) -> str | None:
    """Create a branch with the updated spec and open a PR."""
    repo = gh.get_repo(repo_name)
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    branch_name = f"speckit/clarify-{feature_dir}-{today}"

    # Get the main branch SHA
    main_branch = repo.get_branch("main")
    main_sha = main_branch.commit.sha

    # Create the branch
    try:
        repo.create_git_ref(f"refs/heads/{branch_name}", main_sha)
        log.info("Created branch: %s", branch_name)
    except Exception:
        # Branch may already exist, try updating it
        log.warning("Branch %s may already exist, attempting update", branch_name)
        try:
            ref = repo.get_git_ref(f"heads/{branch_name}")
            ref.edit(main_sha, force=True)
        except Exception:
            log.exception("Failed to create or update branch")
            return None

    # Update the spec file on the new branch
    try:
        file = repo.get_contents(spec_path, ref=branch_name)
        sha = file.sha if not isinstance(file, list) else file[0].sha
        repo.update_file(
            spec_path,
            f"chore(specs): auto-clarify {feature_dir} spec ({num_questions} clarifications)",
            updated_content,
            sha,
            branch=branch_name,
        )
    except Exception:
        log.exception("Failed to update spec file on branch")
        return None

    # Create the PR
    pr_body = dedent(f"""\
        ## Automated Spec Clarification

        This PR was automatically generated by the **speckit-clarify** workflow
        after `{spec_path}` was merged into `main` (commit: {commit_sha[:8]}).

        ### What happened

        - Scanned the spec against project workflows, constitution, and cross-repo context
        - Identified **{num_questions}** areas needing clarification
        - Auto-accepted best-practice recommendations from local Ollama model
        - Applied clarifications to the spec

        ### Changes

        - Added a `## Clarifications` session with Q&A pairs
        - Integrated clarifications into relevant spec sections

        ### Review guidance

        Please review the auto-applied clarifications and:
        1. ✅ Approve if the recommendations are appropriate
        2. 📝 Edit if adjustments are needed
        3. ❌ Close if the clarifications are not useful

        > **Note:** This was generated using local models (Ollama {MODEL}) — zero external LLM tokens consumed.
    """)

    try:
        pr = repo.create_pull(
            title=f"chore(specs): auto-clarify {feature_dir}",
            body=pr_body,
            head=branch_name,
            base="main",
        )
        log.info("Created PR #%d: %s", pr.number, pr.html_url)
        return pr.html_url
    except Exception:
        log.exception("Failed to create PR")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point for the speckit clarify automation."""
    token = os.environ.get("GITHUB_TOKEN")
    changed_specs = os.environ.get("CHANGED_SPECS", "")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "")
    commit_sha = os.environ.get("GITHUB_SHA", "")

    if not token:
        log.error("GITHUB_TOKEN not set")
        sys.exit(1)

    if not changed_specs:
        log.info("No spec files to process. Exiting.")
        sys.exit(0)

    if not repo_name:
        log.error("GITHUB_REPOSITORY not set")
        sys.exit(1)

    gh = Github(auth=Auth.Token(token))
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    spec_paths = [s.strip() for s in changed_specs.split(",") if s.strip()]

    log.info("Processing %d spec file(s): %s", len(spec_paths), spec_paths)

    results: list[dict[str, str | int]] = []

    for spec_path in spec_paths:
        path = Path(spec_path)
        if not path.exists():
            log.warning("Spec file not found: %s", spec_path)
            continue

        feature_dir = path.parent.name
        log.info("=== Processing: %s (%s) ===", feature_dir, spec_path)

        spec_content = path.read_text(encoding="utf-8")

        # Step 1: Scan for ambiguities
        log.info("Scanning spec for ambiguities...")
        questions = scan_spec(path, spec_content)

        if not questions:
            log.info("No critical ambiguities detected in %s. Skipping.", feature_dir)
            results.append({"feature": feature_dir, "questions": 0, "status": "clean"})
            continue

        log.info("Found %d clarification(s) for %s", len(questions), feature_dir)
        for i, q in enumerate(questions, 1):
            log.info(
                "  Q%d [%s]: %s → %s",
                i,
                q.get("category", "?"),
                q.get("question", "?"),
                q.get("recommended_answer", "?"),
            )

        # Step 2: Apply clarifications (auto-accept recommendations)
        log.info("Applying auto-accepted clarifications...")
        updated_content = apply_clarifications(spec_content, questions, today)

        if updated_content == spec_content:
            log.warning("No changes produced for %s. Skipping PR.", feature_dir)
            results.append(
                {
                    "feature": feature_dir,
                    "questions": len(questions),
                    "status": "no_diff",
                }
            )
            continue

        # Step 3: Create branch and PR
        log.info("Creating PR with clarified spec...")
        pr_url = create_branch_and_pr(
            gh=gh,
            repo_name=repo_name,
            spec_path=spec_path,
            updated_content=updated_content,
            feature_dir=feature_dir,
            commit_sha=commit_sha,
            num_questions=len(questions),
        )

        results.append(
            {
                "feature": feature_dir,
                "questions": len(questions),
                "status": "pr_created" if pr_url else "pr_failed",
                "pr_url": pr_url or "",
            }
        )

    # Summary
    log.info("=== Clarification Summary ===")
    for r in results:
        log.info(
            "  %s: %s (%d question(s)) %s",
            r["feature"],
            r["status"],
            r["questions"],
            r.get("pr_url", ""),
        )

    # Create a summary comment on the commit if any PRs were created
    pr_results = [r for r in results if r.get("pr_url")]
    if pr_results:
        repo = gh.get_repo(repo_name)
        comment_body = "## 🔍 Speckit Auto-Clarify Results\n\n"
        comment_body += "The following specs were automatically analyzed and clarification PRs created:\n\n"
        for r in pr_results:
            comment_body += f"- **{r['feature']}**: {r['questions']} clarification(s) → {r['pr_url']}\n"
        comment_body += (
            "\n> Generated by speckit-clarify workflow using local Ollama models."
        )

        try:
            commit = repo.get_commit(commit_sha)
            commit.create_comment(comment_body)
            log.info("Posted summary comment on commit %s", commit_sha[:8])
        except Exception:
            log.warning("Failed to post commit comment, creating issue instead")
            try:
                repo.create_issue(
                    title=f"Speckit Clarify Results — {today}",
                    body=comment_body,
                    labels=["speckit", "automated"],
                )
            except Exception:
                log.exception("Failed to create issue")


if __name__ == "__main__":
    main()
