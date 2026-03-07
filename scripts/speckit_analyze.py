"""Speckit Analyze - Automated cross-artifact consistency analysis.

Runs the speckit-analyze workflow against spec.md, plan.md, and tasks.md files,
uses Ollama (local model) to identify inconsistencies, duplications, ambiguities,
and underspecified items. Creates issues for findings and blocks PRs on CRITICAL.

Designed to run in GitHub Actions on PRs that touch spec artifacts.
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

MODEL = os.environ.get("SPECKIT_MODEL", "gemma2:2b")
MAX_FINDINGS = 50


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
                return result
        except json.JSONDecodeError:
            pass

    # Strategy 2: Any code fence
    if "```" in raw:
        parts = raw.split("```")
        for i in range(1, len(parts), 2):
            try:
                result = json.loads(parts[i].strip())
                if isinstance(result, list):
                    return result
            except json.JSONDecodeError:
                continue

    # Strategy 3: Find the outermost [ ... ] bracket pair
    bracket_match = re.search(r"\[.*\]", raw, re.DOTALL)
    if bracket_match:
        try:
            result = json.loads(bracket_match.group())
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass

    return None


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------


def analyze_artifacts(
    feature_dir: Path, max_retries: int = 2
) -> list[dict[str, str]]:
    """Run cross-artifact consistency analysis using Ollama."""

    spec_path = feature_dir / "spec.md"
    plan_path = feature_dir / "plan.md"
    tasks_path = feature_dir / "tasks.md"

    spec_content = spec_path.read_text(encoding="utf-8") if spec_path.exists() else ""
    plan_content = plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""
    tasks_content = tasks_path.read_text(encoding="utf-8") if tasks_path.exists() else ""

    # Load constitution
    repo_root = feature_dir.parent
    constitution = ""
    for const_path in [
        repo_root / ".specify" / "memory" / "constitution.md",
        repo_root / "docs" / "constitution.md",
    ]:
        if const_path.exists():
            content = const_path.read_text(encoding="utf-8")
            constitution = content[:4000] if len(content) > 4000 else content
            break

    available = []
    if spec_content:
        available.append("spec.md")
    if plan_content:
        available.append("plan.md")
    if tasks_content:
        available.append("tasks.md")

    if not available:
        log.warning("No artifacts found in %s", feature_dir)
        return []

    # Truncate large artifacts for context window
    def truncate(content: str, limit: int = 6000) -> str:
        if len(content) > limit:
            return content[:limit] + "\n... (truncated)"
        return content

    prompt = dedent(f"""\
        You are a specification quality analyst. Perform a cross-artifact consistency
        and quality analysis across the following development artifacts.

        Your task:
        1. Detect DUPLICATIONS — near-duplicate requirements across artifacts
        2. Detect AMBIGUITIES — vague terms lacking measurable criteria
        3. Detect UNDERSPECIFICATION — requirements missing acceptance criteria or tasks
        4. Detect INCONSISTENCIES — conflicting statements across artifacts
        5. Detect CONSTITUTION VIOLATIONS — requirements conflicting with project principles
        6. Detect COVERAGE GAPS — requirements with no associated tasks, or orphan tasks

        === PROJECT CONSTITUTION ===
        {truncate(constitution, 3000)}

        === spec.md ===
        {truncate(spec_content)}

        === plan.md ===
        {truncate(plan_content)}

        === tasks.md ===
        {truncate(tasks_content)}

        CRITICAL: Return ONLY a valid JSON array. No prose before or after.
        Each object MUST have exactly these fields:
        - "id": string (e.g., "D1", "A2", "U3", "I4", "C5", "G6")
        - "category": string ("Duplication", "Ambiguity", "Underspecification", "Inconsistency", "Constitution", "Coverage Gap")
        - "severity": string ("CRITICAL", "HIGH", "MEDIUM", "LOW")
        - "location": string (which file(s) and approximate section)
        - "summary": string (concise description of the finding)
        - "recommendation": string (how to fix it)

        Severity rules:
        - CRITICAL: Constitution violations, missing core artifacts, requirements blocking baseline
        - HIGH: Conflicting requirements, ambiguous security/performance, untestable criteria
        - MEDIUM: Terminology drift, missing NFR coverage, underspecified edge cases
        - LOW: Style improvements, minor redundancy

        If no meaningful issues exist, return: []
        Limit to {MAX_FINDINGS} findings maximum.
    """)

    for attempt in range(1, max_retries + 1):
        log.info("Analysis attempt %d/%d...", attempt, max_retries)
        raw = ask_ollama(prompt)
        if not raw:
            log.warning("Empty response from Ollama on attempt %d", attempt)
            continue

        findings = _extract_json_array(raw)
        if findings is not None:
            valid = []
            for f in findings:
                if isinstance(f, dict) and "summary" in f and "severity" in f:
                    valid.append(f)
            if valid:
                return valid[:MAX_FINDINGS]
            log.info("Parsed JSON but no valid finding objects")
            return []

        log.warning(
            "Failed to parse JSON on attempt %d. Raw (first 500): %s",
            attempt, raw[:500],
        )

    log.error("All %d analysis attempts failed", max_retries)
    return []


def format_report(findings: list[dict[str, str]], feature_dir: str) -> str:
    """Format findings into a markdown report."""
    if not findings:
        return f"## \u2705 Spec Analysis: `{feature_dir}`\n\nNo issues detected."

    criticals = [f for f in findings if f.get("severity") == "CRITICAL"]
    highs = [f for f in findings if f.get("severity") == "HIGH"]
    mediums = [f for f in findings if f.get("severity") == "MEDIUM"]
    lows = [f for f in findings if f.get("severity") == "LOW"]

    report = f"## \U0001f50d Specification Analysis Report: `{feature_dir}`\n\n"
    report += f"**Total Findings:** {len(findings)} "
    report += f"(\U0001f534 {len(criticals)} Critical, \U0001f7e0 {len(highs)} High, "
    report += f"\U0001f7e1 {len(mediums)} Medium, \U0001f7e2 {len(lows)} Low)\n\n"

    report += "| ID | Category | Severity | Location | Summary | Recommendation |\n"
    report += "|:---|:---------|:---------|:---------|:--------|:---------------|\n"

    for f in findings:
        fid = f.get("id", "?")
        cat = f.get("category", "?")
        sev = f.get("severity", "?")
        loc = f.get("location", "?")
        summary = f.get("summary", "?")
        rec = f.get("recommendation", "?")
        emoji = {"CRITICAL": "\U0001f534", "HIGH": "\U0001f7e0", "MEDIUM": "\U0001f7e1", "LOW": "\U0001f7e2"}.get(sev, "\u26aa")
        report += f"| {fid} | {cat} | {emoji} {sev} | {loc} | {summary} | {rec} |\n"

    if criticals:
        report += "\n> \u26d4 **CRITICAL issues detected.** These MUST be resolved before implementation.\n"

    report += f"\n---\n_Generated by speckit-analyze using Ollama ({MODEL})_\n"
    return report


def create_issues(
    gh: Github, repo_name: str, feature_dir: str, findings: list[dict[str, str]]
) -> list[str]:
    """Create GitHub issues for HIGH and CRITICAL findings."""
    repo = gh.get_repo(repo_name)
    created = []

    for f in findings:
        severity = f.get("severity", "")
        if severity not in ("CRITICAL", "HIGH"):
            continue

        title = f"[{feature_dir}] {f.get('category', '?')}: {f.get('summary', '?')[:80]}"

        # Check for duplicates
        existing = repo.get_issues(state="open")
        found = False
        for issue in existing:
            if issue.title == title:
                found = True
                break
        if found:
            log.info("Issue already exists: %s", title)
            continue

        body = dedent(f"""\
            ## {f.get('category', 'Finding')}

            **Severity:** {severity}
            **Location:** {f.get('location', 'Unknown')}
            **Feature:** `{feature_dir}`

            ### Summary
            {f.get('summary', 'No summary')}

            ### Recommendation
            {f.get('recommendation', 'No recommendation')}

            ---
            _Auto-generated by the speckit-analyze workflow._
        """)

        try:
            labels = ["speckit", "automated"]
            if severity == "CRITICAL":
                labels.append("priority:critical")
            elif severity == "HIGH":
                labels.append("priority:high")

            issue = repo.create_issue(title=title, body=body, labels=labels)
            created.append(issue.html_url)
            log.info("Created issue #%d: %s", issue.number, title)
        except Exception:
            log.exception("Failed to create issue for: %s", title)

    return created


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point for the speckit analyze automation."""
    token = os.environ.get("GITHUB_TOKEN")
    changed_dirs = os.environ.get("CHANGED_FEATURE_DIRS", "")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "")
    pr_number = os.environ.get("PR_NUMBER", "")
    block_on_critical = os.environ.get("BLOCK_ON_CRITICAL", "true").lower() == "true"

    if not token:
        log.error("GITHUB_TOKEN not set")
        sys.exit(1)

    if not changed_dirs:
        log.info("No feature directories to analyze. Exiting.")
        sys.exit(0)

    if not repo_name:
        log.error("GITHUB_REPOSITORY not set")
        sys.exit(1)

    gh = Github(auth=Auth.Token(token))
    feature_dirs = [d.strip() for d in changed_dirs.split(",") if d.strip()]

    log.info("Analyzing %d feature dir(s): %s", len(feature_dirs), feature_dirs)

    all_findings: list[dict[str, str]] = []
    all_reports: list[str] = []
    all_issues: list[str] = []
    has_critical = False

    for dir_path in feature_dirs:
        path = Path(dir_path)
        if not path.exists():
            log.warning("Feature dir not found: %s", dir_path)
            continue

        feature_name = path.name
        log.info("=== Analyzing: %s ===", feature_name)

        findings = analyze_artifacts(path)
        all_findings.extend(findings)

        report = format_report(findings, feature_name)
        all_reports.append(report)
        log.info("Report generated: %d findings", len(findings))

        # Create issues for CRITICAL/HIGH findings
        if findings:
            issues = create_issues(gh, repo_name, feature_name, findings)
            all_issues.extend(issues)

            if any(f.get("severity") == "CRITICAL" for f in findings):
                has_critical = True

    # Post combined report as PR comment
    if pr_number and all_reports:
        try:
            repo = gh.get_repo(repo_name)
            pr = repo.get_pull(int(pr_number))

            combined = "\n\n---\n\n".join(all_reports)
            if all_issues:
                combined += "\n\n### Created Issues\n\n"
                for url in all_issues:
                    combined += f"- {url}\n"

            # Deduplicate comments
            for comment in pr.get_issue_comments():
                if (
                    comment.user.login == "github-actions[bot]"
                    and "Specification Analysis Report" in comment.body
                ):
                    comment.edit(body=combined)
                    log.info("Updated existing analysis comment on PR #%s", pr_number)
                    break
            else:
                pr.create_issue_comment(body=combined)
                log.info("Posted analysis comment on PR #%s", pr_number)
        except Exception:
            log.exception("Failed to post PR comment")

    # Summary
    criticals = sum(1 for f in all_findings if f.get("severity") == "CRITICAL")
    highs = sum(1 for f in all_findings if f.get("severity") == "HIGH")
    log.info(
        "=== Analysis Complete: %d findings (%d critical, %d high), %d issues created ===",
        len(all_findings), criticals, highs, len(all_issues),
    )

    # Exit with failure if critical issues found and blocking is enabled
    if has_critical and block_on_critical:
        log.error("CRITICAL issues detected — blocking PR")
        sys.exit(1)


if __name__ == "__main__":
    main()
