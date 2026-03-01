# Vindicta Platform — Specification Registry

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
