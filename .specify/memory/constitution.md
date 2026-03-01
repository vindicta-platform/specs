<!--
Sync Impact Report:
- Version change: 3.0.0 → 3.1.0 (MINOR)
- List of modified sections:
  - Modular Ecosystem Registry: Updated with exact repository list from `vindicta-platform` organization analysis via GitHub MCP.
  - Behavioral Standards for Agents: Integrated Principle VI (GitHub Operations Priority) to mandate MCP server usage.
- Added sections:
  - Principle VI: GitHub Operations Priority (Previously added in this session).
- Templates requiring updates (✅ updated / ⚠ pending):
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
  - .specify/templates/constitution-template.md (⚠ pending - external core sync)
- Follow-up TODOs: Ensure Principle VI is propagated to the `vindicta-foundation` reference constitution.
-->

# Vindicta Platform Constitution

## Core Principles

### I. The Economic Prime Directive
Core operations MUST run on GCP Free Tier. Agents MUST ONLY operate within the `vindicta-warhammer` project. Cost efficiency is a primary architectural constraint; variable-cost features MUST be isolated behind cost-estimation gates and Gemini-standard inference.

### II. Spec-Driven Methodology (BDD-First Mandate)
No code without a Spec. All development MUST follow the **BDD → TDD → Implementation** flow. Behavioral expectations MUST be defined and confirmed failing FIRST. The `.specify` folder is the single source of truth for feature intent and requirement alignment.

### III. Tooling Adherence & Environment
Strictly Windows environment (PowerShell/Batch). Mandatory use of `uv` for dependency management. Utilize project-defined CLI tools (`specify`, `just`) for all orchestration and setup. All repositories must maintain ecosystem synchronization with the Core.

### IV. Agentic Rights & Mechanical Fidelity
Brevity is the enemy of nuance; chains of thought are primary deliverables. Mechanical resolutions (RNG) MUST use casino-grade CSPRNG and produce `EntropyProof`. Strict adherence to the established Source of Truth rule-sets (Engine, Economy, Oracle) is non-negotiable.

### V. Automated Quality & Stability
Working models must not leave the repository in a broken state. Full unit suite must run in <60s; individual tests <1s. Mandatory `async/await` for all I/O. WIP features must be tagged with `@wip` and remain black-box oriented.

## Modular Ecosystem Registry

The Vindicta Platform (org: `vindicta-platform`) is a distributed ecosystem of specialized repositories, each governing a specific domain. All components MUST align with the unified architecture and governance defined here.

### Specialized Repositories
- **`vindicta-platform`**: The Orchestrator and mono-entry point for the platform.
- **`vindicta-foundation`**: Core base models, underlying architecture, and constitutional framework.
- **`vindicta-engine`**: Mechanical domain context, including Physics, Dice, and AI Core.
- **`vindicta-economy`**: Economic domain context, governing the Ledger, Quotas, and Gas Tank.
- **`vindicta-oracle`**: Oracle domain context for meta-analysis, predictions, and the AI debate council.
- **`warscribe-system`**: Scribe domain context for Notation, Parsing, and Transcripts.
- **`specs`**: The central repository for all feature specifications and BDD/TDD definitions (this repo).
- **`Vindicta-Agents`**: Dedicated logic and implementations for the platform's agentic workforce.
- **`features`**: Centralized repository for multi-repo feature testing and integration validation.
- **`.github`**: Organization-wide configuration, project templates, and strategic roadmaps.
- **`vindicta-platform.github.io`**: The public-facing root for platform documentation via GitHub Pages.

## Behavioral Standards for Agents

Prioritize precision and technical accuracy over conversational exhaustiveness. The Human User is the **Supreme Architect**. Constitutional requirements are non-negotiable. Mandatory use of directory-based memory. Standalone FAQ docs are prohibited; fix UX or documentation instead.

### VI. GitHub Operations Priority
Agents MUST prioritize `github-mcp-server` for all GitHub interactions (Issues, PRs, metadata). Fallback to `gh` CLI ONLY if MCP is unavailable or lacks specific functionality. Local `git` commands remain valid for direct filesystem workspace synchronization.

## Governance

The Constitution is the supreme governing document and supersedes all other practices. All PRs and reviews MUST verify compliance with these principles. Amendments require documentation and version bumps following semantic versioning. 

**Version**: 3.1.0 | **Ratified**: 2026-03-01 | **Last Amended**: 2026-03-01
