# Contributing to Vindicta Platform Specs

Thank you for contributing! This repository uses a spec-driven methodology. All changes must follow the workflow below.

## Creating a New Feature Spec

1. **Create a feature branch** using the helper script:

   ```powershell
   .specify/scripts/powershell/create-new-feature.ps1 "Your feature description"
   ```

2. **Fill out `spec.md`** using the template structure:
   - `# Feature Specification: NNN-feature-name` — top-level header
   - `## User Scenarios & Testing` — prioritized user stories with acceptance scenarios
   - `## Requirements` — functional requirements and key entities
   - `## Non-Functional Requirements` — performance, security, scalability constraints
   - `## Success Criteria` — measurable outcomes

3. **Complete `checklists/requirements.md`** — validates spec quality before planning.

4. **Open a Pull Request** with a conventional commit title:
   - `docs: specification for NNN-feature-name`

## PR Requirements

All PRs must pass CI checks:

- Markdown lint (see `.markdownlint.yaml`)
- Spell check (add domain terms to `cspell.json`)
- Link validation
- Conventional PR title
- Spec structure validation

## Spec Quality Standards

- **No implementation details** — specs describe *what*, not *how*
- **Independently testable user stories** — each story should be a viable MVP slice
- **Measurable success criteria** — technology-agnostic, quantifiable outcomes
- **Edge cases identified** — boundary conditions and error scenarios documented

## Adding Domain Terms

If the spell checker flags legitimate domain terminology, add the word to `cspell.json` in the `words` array.
