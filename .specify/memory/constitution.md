<!--
Sync Impact Report:
- Version change: [UNDEFINED] → 3.0.0
- List of modified principles:
  - Unified General Core, Portal, and Agent principles.
  - Principle I: Economic Prime Directive (GCP Free Tier).
  - Principle II: Spec-Driven Methodology (BDD/TDD First).
  - Principle III: Tooling Adherence (uv, specific environment).
  - Principle IV: Agentic Rights & mechanical fidelity (EntropyProof).
  - Principle V: Quality & Stability (Async-First, wip tagging).
- Added sections:
  - Modular Ecosystem Registry
  - Behavioral Standards for Agents
- Templates requiring updates (✅ updated / ⚠ pending):
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
- Follow-up TODOs: None.
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

The system consists of a main orchestrator (`platform-core`) and specialized satellite repositories (e.g., `WARScribe-CLI`, `Meta-Oracle`, `Dice-Engine`, `Economy-Engine`, `Logi-Slate-UI`). All components must align with the unified architecture and governance of the Vindicta Platform.

## Behavioral Standards for Agents

Prioritize precision and technical accuracy over conversational exhaustiveness. The Human User is the **Supreme Architect**. Constitutional requirements are non-negotiable. Mandatory use of directory-based memory. Standalone FAQ docs are prohibited; fix UX or documentation instead.

## Governance

The Constitution is the supreme governing document and supersedes all other practices. All PRs and reviews MUST verify compliance with these principles. Amendments require documentation and version bumps following semantic versioning. 

**Version**: 3.0.0 | **Ratified**: 2026-03-01 | **Last Amended**: 2026-03-01
