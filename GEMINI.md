# specs Development Guidelines

Auto-generated from feature specifications. Last updated: 2026-03-01

## Core Rules & Governance

### G-001: GitHub MCP Priority

Agents MUST prioritize `github-mcp-server` for all GitHub interactions (Issues, PRs, metadata). Fallback to `gh` CLI ONLY if MCP is unavailable or lacks specific functionality. Local `git` commands remain valid for direct filesystem workspace synchronization.

### G-002: Spec-Driven Methodology (BDD-First)

No code without a Spec. All development MUST follow the **BDD → TDD → Implementation** flow. Behavioral expectations MUST be defined and confirmed failing FIRST. The `.specify` folder is the single source of truth.

## Project Structure

```text
.agent/             # Agent-specific workflows and rules
.specify/           # Business Logic Specifications (BDD)
  memory/           # Long-term agent memory (Constitution)
  templates/        # Templates for plans, tasks, and specs
[feature-dir]/      # Specific feature implementation tracking
```

## Active Technologies

- **MCP**: github-mcp-server (Primary for GitHub Ops)
- **Environment**: Windows (PowerShell/Batch)
- **Dependency Management**: uv
- **Methodology**: BDD-First Spec-Driven Development

## Commands

- `specify`: Feature orchestration and status
- `just`: Ecosystem automation and setup

## Code Style

- **Brevity**: Avoided in favor of technical nuance and thorough Chains of Thought.
- **Async-First**: Mandatory `async/await` for I/O operations.
- **EntropyProof**: Deterministic mechanical resolutions via CSPRNG.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
