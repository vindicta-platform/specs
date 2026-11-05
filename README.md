# Vindicta Platform — Specification Registry

> **Status:** complete as a design: 47 feature specifications written BDD-first for the Vindicta Platform, February-March 2026. Specs 002-008 carry the correctness argument; 019-043 are unbuilt product ideas. Single maintainer.

The single source of truth for all platform feature specifications. Each feature is defined using a BDD-first, spec-driven methodology before any implementation begins.

## Repository Structure

```text
.agent/              # Agent workflows and rules
.specify/            # Spec framework: templates, scripts, constitution
.github/workflows/   # CI checks (markdownlint, cspell, link-check, spec-validator)
NNN-feature-name/    # Feature specification directories (001–047)
  spec.md            # Feature specification
  checklists/
    requirements.md  # Quality checklist
```

## Feature Numbering

Features are numbered sequentially with a three-digit prefix (`001`–`047`). Each directory contains:

| File | Purpose |
|------|---------|
| `spec.md` | Behavioral specification with user stories, requirements, and success criteria |
| `checklists/requirements.md` | Quality gate checklist validated before planning |

## Methodology

All development follows the **BDD → TDD → Implementation** flow:

1. **Specify** — Define behavioral expectations in `spec.md`
2. **Plan** — Generate implementation design artifacts
3. **Task** — Break the plan into dependency-ordered tasks
4. **Implement** — Write code against failing tests

See [`.specify/memory/constitution.md`](.specify/memory/constitution.md) for governance principles.

## Quick Start

```powershell
# Create a new feature specification
.specify/scripts/powershell/create-new-feature.ps1 "Your feature description"
```

## CI Checks

Every pull request runs:

- **Markdown Lint** — Structure and formatting
- **Spell Check** — Domain-aware via `cspell.json`
- **Link Checker** — Validates all URLs
- **PR Title Lint** — Enforces conventional commits
- **Spec Validator** — Ensures `spec.md` and `checklists/requirements.md` exist with required headers

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on creating and reviewing specifications.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## Independence

This is a personal project by Brandon Fox, built on my own time and equipment. It is not affiliated with, endorsed by, or derived from the work of any employer, current or former, and does not represent their views, products or practices. Licensed under the MIT License; principles at [First-ADE/PRINCIPLES.md](https://github.com/First-ADE/.github/blob/main/PRINCIPLES.md).
