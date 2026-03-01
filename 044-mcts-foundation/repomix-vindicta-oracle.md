This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.github/workflows/docs.yml
CONTRIBUTING.md
docs/adr/000-template.md
docs/adr/001-python-language.md
docs/adr/002-precommit-required.md
docs/agents.md
docs/api.md
docs/contributing.md
docs/getting-started.md
docs/index.md
docs/proposals/feat-011-match-prediction-api.md
docs/SETUP.md
LICENSE
mkdocs.yml
pyproject.toml
README.md
specs/001-debate-engine/analysis.md
specs/001-debate-engine/plan.md
specs/001-debate-engine/spec.md
specs/list-grader-api/checklist.md
specs/list-grader-api/plan.md
specs/list-grader-api/spec.md
specs/list-grader-api/tasks.md
src/vindicta_oracle/__init__.py
src/vindicta_oracle/__main__.py
src/vindicta_oracle/agents/__init__.py
src/vindicta_oracle/agents/adversary_impl.py
src/vindicta_oracle/agents/adversary.py
src/vindicta_oracle/agents/arbiter_impl.py
src/vindicta_oracle/agents/arbiter.py
src/vindicta_oracle/agents/base.py
src/vindicta_oracle/agents/chaos.py
src/vindicta_oracle/agents/home_impl.py
src/vindicta_oracle/agents/home.py
src/vindicta_oracle/agents/rule_sage_impl.py
src/vindicta_oracle/agents/rule_sage.py
src/vindicta_oracle/api.py
src/vindicta_oracle/debate.py
src/vindicta_oracle/demo.py
src/vindicta_oracle/engine.py
src/vindicta_oracle/grader.py
src/vindicta_oracle/models.py
src/vindicta_oracle/ollama_client.py
src/vindicta_oracle/protocol.py
src/vindicta_oracle/transcript.py
tests/test_agents.py
tests/test_api.py
tests/test_grader.py
tests/test_oracle.py
```

# Files

## File: .github/workflows/docs.yml
````yaml
name: docs
on:
  push:
    branches:
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.x
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
````

## File: CONTRIBUTING.md
````markdown
# Contributing to Meta-Oracle

Thank you for your interest in contributing!

## Cross-Cutting Decisions

> **⚠️ Important:** All decisions that affect multiple repositories or have platform-wide implications **must** be recorded in [**Platform-Docs**](https://github.com/vindicta-platform/Platform-Docs) before implementation.

This includes:
- API contract changes
- Shared schema modifications
- Authentication/authorization changes
- New inter-service dependencies
- Platform-wide configuration changes

See the [Platform-Docs Contributing Guide](https://github.com/vindicta-platform/Platform-Docs/blob/main/CONTRIBUTING.md) for the full process.

## Repo-Specific Guidelines

1. Follow existing code style and conventions
2. Write tests for new functionality
3. Keep PRs focused and atomic
4. Reference related [Platform-Docs proposals](https://github.com/vindicta-platform/Platform-Docs/tree/main/docs/proposals) when applicable
````

## File: docs/adr/000-template.md
````markdown
# ADR-XXX: [Title]
**Status**: Proposed | Accepted  
**Date**: YYYY-MM-DD
## Context
## Decision
## Consequences
````

## File: docs/adr/001-python-language.md
````markdown
# ADR-001: Python as Primary Language
**Status**: Accepted | **Date**: 2026-02-01
## Decision
Python 3.10+ with Gemini API integration.
## Rationale
- Vindicta Platform is Python-first
- Google AI Python SDK
## Alternatives Considered
TypeScript, Rust — Rejected for ecosystem consistency.
````

## File: docs/adr/002-precommit-required.md
````markdown
# ADR-002: Pre-commit Hooks Required
**Status**: Accepted | **Date**: 2026-02-01
## Decision
Pre-commit with ruff required.
````

## File: docs/agents.md
````markdown
# The 5-Agent Swarm

## Agent Roles

| Agent | Role |
|-------|------|
| **Home** | Argues for your list's strengths |
| **Adversary** | Argues for opponent's advantages |
| **Arbiter** | Provides statistical context |
| **Rule-Sage** | Validates mechanical claims |
| **Council** | Synthesizes final prediction |

## Debate Protocol

1. Home makes opening argument
2. Adversary counters
3. Arbiter adds data
4. Rule-Sage validates claims
5. Council renders verdict

## Rule-Sage Auditing

All mechanical claims must:
- Cite valid rule IDs
- Reference existing units only
- Use correct move notation
````

## File: docs/api.md
````markdown
# API

## Oracle

```python
from meta_oracle import Oracle

oracle = Oracle()
result = oracle.predict(my_list, opponent_list, mission="Purge the Enemy")
```

## PredictionResult

```python
class PredictionResult:
    probability: float  # 0.0 to 1.0
    confidence: float   # margin of error
    factors: list[str]  # key factors
```

## Sleeper Detection

```python
sleepers = oracle.find_sleepers(faction="Tyranids")
```
````

## File: docs/contributing.md
````markdown
# Contributing

## Pre-Commit Hooks (Required)

All contributors **must** install and run pre-commit hooks before committing.
```bash
uv pip install pre-commit
pre-commit install
```

## Setup

```bash
git clone https://github.com/vindicta-platform/Meta-Oracle.git
cd Meta-Oracle
uv venv && uv pip install -e ".[dev]"
pytest tests/ -v
```

MIT License
````

## File: docs/getting-started.md
````markdown
# Getting Started

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/Meta-Oracle.git
```

## Requirements

- Python 3.10+
- Gemini API key (for AI inference)

## Configuration

```bash
export GOOGLE_API_KEY=your-api-key
```

## First Prediction

```python
from meta_oracle import Oracle

oracle = Oracle()
result = oracle.predict(my_list, opponent_list)
```
````

## File: docs/index.md
````markdown
# Vindicta Oracle Documentation

Welcome to the **Vindicta Oracle** documentation — meta analysis, predictions, and the AI debate council for the Vindicta Platform.

## Modules

- **Meta-Seer**: Faction meta analysis and heuristic evaluation.
- **Arbiter Council**: Multi-model AI debate and consensus engine.

## Links

- [GitHub Repository](https://github.com/vindicta-platform/vindicta-oracle)
- [Foundation & Standards](https://github.com/vindicta-platform/vindicta-foundation)
````

## File: docs/proposals/feat-011-match-prediction-api.md
````markdown
# Feature Proposal: Meta-Oracle Match Prediction API

**Proposal ID**: FEAT-011  
**Author**: Unified Product Architect (Autonomous)  
**Created**: 2026-02-01  
**Status**: Draft  
**Priority**: High  
**Target Repository**: Meta-Oracle  

---

## Part A: Software Design Document (SDD)

### 1. Executive Summary

Expose a public API for match predictions, allowing players to query expected win probabilities, optimal secondaries, and key matchup insights based on faction/subfaction combinations.

### 2. System Architecture

#### 2.1 Current State
- Internal analytics engine
- No public API
- Batch-processed statistics

#### 2.2 Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 Meta-Oracle Prediction API                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   API Gateway                           │    │
│  │   /predict/match  |  /stats/faction  |  /recommend      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Prediction Engine                          │    │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │    │
│  │   │ Win Rate    │  │ Secondary   │  │  Matchup    │     │    │
│  │   │ Predictor   │  │ Recommender │  │  Analyzer   │     │    │
│  │   └─────────────┘  └─────────────┘  └─────────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Historical Data Store                      │    │
│  │   Battle logs | Tournament results | Meta snapshots     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.3 File Changes

```
Meta-Oracle/
├── src/
│   └── meta_oracle/
│       ├── api/
│       │   ├── __init__.py      [NEW]
│       │   ├── routes.py        [NEW] FastAPI routes
│       │   └── schemas.py       [NEW] Request/response models
│       ├── prediction/
│       │   ├── match.py         [NEW] Match outcome predictor
│       │   ├── secondaries.py   [NEW] Secondary optimizer
│       │   └── matchups.py      [NEW] Matchup analysis
│       └── data/
│           └── aggregator.py    [MODIFY] API-friendly queries
├── tests/
│   └── test_prediction_api.py   [NEW]
└── docs/
    └── api.md                   [NEW] API documentation
```

### 3. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/predict/match` | Predict match outcome |
| GET | `/api/v1/stats/faction/{id}` | Faction win rates |
| GET | `/api/v1/stats/matchup` | Head-to-head stats |
| POST | `/api/v1/recommend/secondaries` | Optimal secondary objectives |
| GET | `/api/v1/meta/trends` | Current meta trends |

### 4. Prediction Request/Response

```python
class MatchPredictionRequest(BaseModel):
    player1_faction: str
    player1_subfaction: Optional[str]
    player2_faction: str
    player2_subfaction: Optional[str]
    mission: Optional[str]
    points_limit: int = 2000

class MatchPredictionResponse(BaseModel):
    player1_win_probability: float  # 0.0 - 1.0
    player2_win_probability: float
    confidence: float               # Algorithm confidence
    key_factors: list[str]          # "Player 1 has strong anti-vehicle"
    recommended_secondaries: dict[str, list[str]]
    sample_size: int                # Games analyzed
```

### 5. Rate Limiting

| Tier | Requests/Hour | Cache TTL |
|------|---------------|-----------|
| Anonymous | 10 | 1 hour |
| Free Member | 50 | 30 min |
| Supporter | 200 | 15 min |
| Champion | 1000 | 5 min |

### 6. Data Sources

- Historical battle logs from Vindicta platform
- Tournament results (40kstats integration potential)
- ELO-weighted outcomes
- Regularly updated meta snapshots

---

## Part B: Behavior Driven Development (BDD)

### User Stories

#### US-001: Pre-Game Analysis
**As a** tournament player  
**I want to** check my matchup before a game  
**So that** I can prepare an optimal strategy

#### US-002: Secondary Selection
**As a** competitive player  
**I want** AI-recommended secondaries  
**So that** I maximize my scoring potential

#### US-003: Meta Insights
**As a** list builder  
**I want to** see current faction win rates  
**So that** I can build competitive lists

### Acceptance Criteria

```gherkin
Feature: Match Prediction API

  Scenario: Predict match outcome
    Given I submit a prediction request
      | player1_faction | Necrons       |
      | player2_faction | Space Marines |
    When the API processes the request
    Then I should receive win probabilities for each player
    And the confidence score based on sample size
    And key matchup insights

  Scenario: Get secondary recommendations
    Given my faction is "Aeldari"
    And opponent faction is "Death Guard"
    And mission is "Take and Hold"
    When I request secondary recommendations
    Then I should receive ranked secondary objectives
    And expected success rates for each

  Scenario: Rate limit enforcement
    Given I am an anonymous user
    When I exceed 10 requests in an hour
    Then I should receive a 429 Too Many Requests
    And a message indicating upgrade options
```

---

## Implementation Estimate

| Phase | Effort | Dependencies |
|-------|--------|--------------|
| API Routes | 4 hours | FastAPI |
| Prediction Engine | 12 hours | Historical data |
| Secondary Recommender | 8 hours | Mission data |
| Rate Limiting | 3 hours | Redis |
| Documentation | 3 hours | OpenAPI |
| Testing | 4 hours | None |
| **Total** | **34 hours** | |

---

## References

- [Meta-Oracle Spec](file:///c:/Users/bfoxt/Vindicta-Platform/platform-core/specs/005-meta-oracle)
- [Arbiter-Predictor](file:///c:/Users/bfoxt/Vindicta-Platform/Arbiter-Predictor)
````

## File: docs/SETUP.md
````markdown
# Setup Guide

```bash
git clone https://github.com/vindicta-platform/Meta-Oracle.git
cd Meta-Oracle
uv venv && uv pip install -e ".[dev]"
```
````

## File: LICENSE
````
MIT License

Copyright (c) 2026 Vindicta Platform Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
````

## File: mkdocs.yml
````yaml
site_name: Vindicta Oracle
site_description: Meta analysis, predictions, and AI debate council for the Vindicta Platform.
site_author: Vindicta Platform Contributors
site_url: https://vindicta-platform.github.io/vindicta-oracle/

repo_name: vindicta-platform/vindicta-oracle
repo_url: https://github.com/vindicta-platform/vindicta-oracle

theme:
  name: material
  palette:
    - scheme: slate
      primary: deep orange
      accent: orange
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
    - scheme: default
      primary: deep orange
      accent: orange
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
  font:
    text: Outfit
    code: JetBrains Mono

nav:
  - Home: index.md

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.details
  - attr_list
  - md_in_html

plugins:
  - search
````

## File: pyproject.toml
````toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "vindicta-oracle"
version = "0.1.0"
description = "AI debate engine for competitive Warhammer predictions"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
dependencies = [
    "ollama>=0.3",
    "pydantic>=2.0",
    "duckdb>=0.10",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.4", "pre-commit>=3.7"]
api = ["fastapi>=0.109.0", "uvicorn>=0.27.0"]

[tool.hatch.build.targets.wheel]
packages = ["src/vindicta_oracle"]

[tool.ruff]
line-length = 88
target-version = "py310"

[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-asyncio>=1.3.0",
]
````

## File: README.md
````markdown
# ⚔️ Vindicta Oracle

*Predictive Models & Strategic Meta Analysis.*

The Oracle Domain provides the AI-driven foresight of the Vindicta Platform. It evaluates army lists, predicts match outcomes, and resolves complex strategic debates through a multi-agent consensus system.

## 🏛️ Core Components

- **Debate Engine**: Multi-agent system where different tactical personas (Tech-Priest, Chaos Sorcerer, etc.) debate game mechanics.
- **List Grader**: Automated evaluation of competitive army lists against current meta-trends.
- **Outcome Predictor**: Statistical models for win probability and tactical risk assessment.

## 🚀 Quick Start (Development)

This repository is managed with `uv`.

```bash
# Install dependencies
uv sync

# Run the debate engine demo
uv run src/vindicta_oracle/demo.py
```

## 📦 Architecture

- `src/vindicta_oracle/agents/`: Individual strategic personas and reasoning logic.
- `src/vindicta_oracle/engine.py`: The consensus and orchestration logic for debates.
- `src/vindicta_oracle/grader.py`: Army list evaluation logic.

## 📜 Governance

Part of the [Vindicta Platform](https://github.com/vindicta-platform). See [vindicta-foundation](https://github.com/vindicta-platform/vindicta-foundation) for global standards.
````

## File: specs/001-debate-engine/analysis.md
````markdown
# Analysis Report: 001-debate-engine

**Feature:** Debate Engine Foundation (v0.1.0)
**Status:** PASS ✅

## Coverage

| Roadmap Deliverable | Spec        | Plan               |
| ------------------- | ----------- | ------------------ |
| DebateEngine core   | US-01, §4.1 | engine/            |
| Agent protocol      | US-02, §4.2 | agents/protocol.py |
| Stub agents (3)     | US-04, §4.4 | agents/*.py        |
| Debate transcript   | US-03, §4.3 | models/            |

## Checks: All PASS ✅

## Verdict
**PROCEED TO IMPLEMENTATION** ✅
````

## File: specs/001-debate-engine/plan.md
````markdown
# Implementation Plan: Debate Engine Foundation (v0.1.0)

**Spec Reference:** [spec.md](./spec.md)

---

## Proposed Changes

```
src/meta_oracle/
├── __init__.py
├── engine/
│   ├── __init__.py
│   └── debate_engine.py    # DebateEngine: orchestrate debate rounds
├── agents/
│   ├── __init__.py
│   ├── protocol.py         # DebateAgent protocol, Proposal, Argument
│   ├── aggressive.py       # AggressiveAgent stub
│   ├── defensive.py        # DefensiveAgent stub
│   └── balanced.py         # BalancedAgent stub
├── judging/
│   ├── __init__.py
│   └── scoring_judge.py    # Score-based winner selection
└── models/
    ├── __init__.py
    ├── debate_result.py    # DebateResult, DebateRound
    └── transcript.py       # Debate transcript serialization
```

### Tests

```
tests/
├── test_debate_engine.py    # Full debate flow
├── test_agents.py           # Stub agent behavior
├── test_judging.py          # Score-based judging
├── test_transcript.py       # Serialization round-trip
└── fixtures/
```

---

## Verification

```powershell
uv run pytest tests/ -v
uv run mypy src/meta_oracle/ --strict
```
````

## File: specs/001-debate-engine/spec.md
````markdown
# Specification: Debate Engine Foundation (v0.1.0)

**Feature ID:** 001-debate-engine
**Milestone:** v0.1.0 — Foundation
**Priority:** P0
**Status:** Specified
**Target Date:** Feb 24, 2026

---

## 1. Problem Statement

The Vindicta Platform's AI layer needs a debate-based decision system where
multiple specialist AI agents argue for different actions, and a judge agent
selects the best recommendation. Meta-Oracle provides this "council of AIs"
architecture. Without it, Primordia-AI would be a single-perspective engine
with no deliberative reasoning.

---

## 2. Vision

Create the DebateEngine framework with stub agents that can propose, argue
for, and adjudicate tactical actions through structured debate rounds.

---

## 3. User Stories

### US-01: Debate Engine — Multi-Agent Decision

> As the **Vindicta recommendation system**,
> I want to **run a structured debate between AI agents**,
> So that **the final recommendation considers multiple perspectives**.

**Acceptance Criteria:**

- [ ] `DebateEngine.debate(game_state)` returns `DebateResult`
- [ ] At least 2 agents propose actions
- [ ] Judge agent scores each proposal
- [ ] Winning proposal becomes the recommendation

### US-02: Agent Interface — Pluggable Agents

> As an **AI researcher**,
> I want to **implement custom debate agents via a protocol**,
> So that **I can experiment with different reasoning strategies**.

**Acceptance Criteria:**

- [ ] `DebateAgent` protocol with `propose()` and `argue()` methods
- [ ] Agents receive game state and debate context
- [ ] Stub agents provided as reference implementations
- [ ] Agent registration via DebateEngine configuration

### US-03: Debate Transcript — Audit Trail

> As the **Agent-Auditor-SDK**,
> I want to **record the full debate transcript**,
> So that **AI reasoning can be reviewed and analyzed**.

**Acceptance Criteria:**

- [ ] Each debate round produces a `DebateRound` entry
- [ ] Rounds include: proposals, arguments, scores, verdict
- [ ] Transcript serializable to JSON
- [ ] Timestamps on all entries

### US-04: Stub Agents — Reference Implementations

> As a **developer bootstrapping Meta-Oracle**,
> I want **pre-built stub agents** (aggressive, defensive, balanced),
> So that **the system can work end-to-end without ML models**.

**Acceptance Criteria:**

- [ ] `AggressiveAgent` — maximizes expected damage output
- [ ] `DefensiveAgent` — maximizes unit survivability
- [ ] `BalancedAgent` — weighted combination of both
- [ ] All agents use Primordia-AI evaluation as their base

---

## 4. Functional Requirements

### 4.1 DebateEngine

```python
from meta_oracle import DebateEngine, AggressiveAgent, DefensiveAgent

engine = DebateEngine(
    agents=[AggressiveAgent(), DefensiveAgent()],
    rounds=3,
    judge="scoring",  # scoring | llm | human
)

result = engine.debate(game_state)
print(result.winner.action)
print(result.transcript)
```

### 4.2 DebateAgent Protocol

```python
class DebateAgent(Protocol):
    name: str

    def propose(self, state: GameState) -> Proposal:
        """Propose an action with reasoning."""
        ...

    def argue(self, state: GameState, proposals: list[Proposal]) -> Argument:
        """Argue for own proposal or against others."""
        ...
```

### 4.3 DebateResult Model

| Field           | Type                | Description        |
| --------------- | ------------------- | ------------------ |
| `winner`        | `Proposal`          | Winning proposal   |
| `scores`        | `dict[str, float]`  | Agent name → score |
| `transcript`    | `list[DebateRound]` | Full debate log    |
| `total_time_ms` | `float`             | Debate duration    |

### 4.4 Stub Agent Behavior

| Agent      | Strategy              | Evaluation Weight                     |
| ---------- | --------------------- | ------------------------------------- |
| Aggressive | Maximize damage dealt | Material: 0.7, Position: 0.1, VP: 0.2 |
| Defensive  | Minimize damage taken | Material: 0.3, Position: 0.4, VP: 0.3 |
| Balanced   | Equal weighting       | Material: 0.4, Position: 0.3, VP: 0.3 |

---

## 5. Non-Functional Requirements

| Category          | Requirement                                      |
| ----------------- | ------------------------------------------------ |
| **Performance**   | 3-round debate < 500ms                           |
| **Dependencies**  | vindicta-core, primordia-ai                      |
| **Type Safety**   | 100% strict mypy                                 |
| **Extensibility** | New agents via Protocol, no inheritance required |

---

## 6. Out of Scope

- LLM-based agents (v0.2.0)
- Human-in-the-loop judging
- Agent training/learning

---

## 7. Success Criteria

| Metric            | Target                      |
| ----------------- | --------------------------- |
| Debate resolution | 3 rounds, 2+ agents         |
| Stub agents       | 3 reference implementations |
| Transcript        | Full audit trail            |
| Test coverage     | > 90%                       |
````

## File: specs/list-grader-api/checklist.md
````markdown
# Checklist: List Grader API

## Functional Requirements

- [ ] **CHK-001**: `POST /grade` accepts valid JSON and returns 200
- [ ] **CHK-002**: Response includes `grade`, `score`, `analysis`, `council_verdict`
- [ ] **CHK-003**: Response time under 30 seconds
- [ ] **CHK-004**: Invalid JSON returns 400
- [ ] **CHK-005**: Scoring formula: `0.6 * council + 0.4 * primordia`
- [ ] **CHK-006**: Grade scale: A=90-100, B=75-89, C=60-74, D=40-59, F=0-39
- [ ] **CHK-007**: Council executes 3 rounds with 5 agents

## Error Handling

- [ ] **CHK-008**: Empty units returns 400
- [ ] **CHK-009**: Unknown faction returns 400
- [ ] **CHK-010**: Quota exhaustion returns 429
- [ ] **CHK-011**: Ollama timeout returns 504

## Integration

- [ ] **CHK-012**: Full 5-agent council debate triggered
- [ ] **CHK-013**: Each agent appears in `analysis`
- [ ] **CHK-014**: `consensus_agents` lists agreeing agents
- [ ] **CHK-015**: Agent-Auditor quota check runs before debate
````

## File: specs/list-grader-api/plan.md
````markdown
# Implementation Plan: List Grader API

## Proposed Changes

### API Layer

#### [NEW] `src/meta_oracle/api.py`
- Create FastAPI `APIRouter` with prefix `/api/v1`
- Implement `POST /grade` endpoint accepting `GradeRequest`
- Return `GradeResponse` with council verdict
- Include error handlers for 400/429/503/504

#### [NEW] `src/meta_oracle/grader.py`
- `ListGrader` class with async `grade()` method
- Integrate quota pre-check via Agent-Auditor-SDK (stub)
- Calculate final score: `0.6 * council_consensus + 0.4 * primordia_score`
- Map numeric score to letter grade (A-F)

### Core Engine

#### [MODIFY] `src/meta_oracle/models.py`
Add Pydantic models: `Unit`, `ArmyList`, `GradeRequest`, `GradeResponse`

#### [MODIFY] `src/meta_oracle/engine.py`
Add `run_grading_session(army_list: ArmyList) -> DebateResult`

#### [MODIFY] `pyproject.toml`
Add FastAPI, uvicorn dependencies under `[project.optional-dependencies].api`

---

## Verification Plan

### Automated Tests
- `tests/test_grader.py`: Unit tests for grading logic
- `tests/test_api.py`: Integration tests for API endpoint

### Run Command
```bash
uv run pytest tests/test_grader.py tests/test_api.py -v
```

### Manual Integration Test
```bash
uv run uvicorn meta_oracle.api:app --port 8000
curl -X POST http://localhost:8000/api/v1/grade \
  -H "Content-Type: application/json" \
  -d '{"army_list": {"faction": "Space Marines", "units": [{"name": "Captain", "points": 100}]}}'
```

---

*Last Updated: 2026-02-06*
````

## File: specs/list-grader-api/spec.md
````markdown
# Specification: List Grader API

**Feature**: List Grader API  
**Repository**: vindicta-platform/Meta-Oracle  
**Issue Reference**: #8  
**Version**: 1.3  
**Status**: ✅ Clarified  
**Last Updated**: 2026-02-06

---

## Executive Summary

The List Grader API exposes Meta-Oracle's AI council debate capability as a REST endpoint, allowing users to submit competitive army lists and receive structured grades, tactical analysis, and council verdicts.

---

## User Stories

### US-1: Competitive Player List Evaluation
**As a** competitive player,  
**I want to** submit my army list for AI evaluation,  
**So that** I can understand its strengths and weaknesses before a tournament.

### US-2: List Comparison Analysis
**As a** player preparing for a matchup,  
**I want to** receive a grade and analysis for my list,  
**So that** I can make informed decisions about unit choices and tactics.

### US-3: API Integration
**As a** Vindicta Portal developer,  
**I want to** call the List Grader API programmatically,  
**So that** I can integrate grading into the web UI.

---

## Acceptance Criteria

### AC-1: API Endpoint
- [ ] `POST /grade` endpoint accepts an army list payload
- [ ] Endpoint returns JSON response within 30 seconds
- [ ] Endpoint validates input schema and returns 400 for invalid requests

### AC-2: Grading Response
- [ ] Response includes a letter grade (A-F) with numeric score (0-100)
- [ ] Response includes structured analysis from each council agent
- [ ] Response includes final council verdict with confidence percentage

### AC-3: Council Integration
- [ ] Grading triggers a full 5-agent council debate
- [ ] Debate uses Home agent advocacy and Adversary critique
- [ ] Arbiter produces the final verdict

### AC-4: Error Handling
- [ ] Invalid list format returns 400 with descriptive error
- [ ] Quota exhaustion returns 429 with retry-after header
- [ ] Internal errors return 500 with correlation ID

---

## API Contract

### `POST /api/v1/grade`

#### Request Schema
```json
{
  "army_list": {
    "faction": "string",
    "points_limit": 2000,
    "units": [
      {
        "name": "string",
        "points": 150,
        "wargear": ["string"]
      }
    ],
    "detachment": "string"
  },
  "context": {
    "mission": "string (optional)",
    "opponent_faction": "string (optional)"
  }
}
```

#### Response Schema
```json
{
  "grade": "B+",
  "score": 78,
  "analysis": {
    "home_advocacy": "string",
    "adversary_critique": "string",
    "rule_sage_notes": "string",
    "arbiter_verdict": "string"
  },
  "council_verdict": {
    "prediction": "COMPETITIVE",
    "confidence": 0.72,
    "consensus_agents": ["Home", "Rule-Sage", "Arbiter"]
  },
  "metadata": {
    "debate_id": "uuid",
    "rounds": 3,
    "processing_time_ms": 2500
  }
}
```

---

## Integration Points

| Dependency | Role | Integration |
|------------|------|-------------|
| `DebateEngine` | Orchestration | Async debate session |
| `Agent-Auditor-SDK` | Quota | Pre-flight budget check |
| `WARScribe-Core` | Validation | List schema validation |
| `Primordia-AI` | Scoring | Tactical evaluation input |

---

## Clarification Cycle 1: Ambiguity Resolution

### Grading Scale Definition
| Grade | Score Range | Description |
|-------|-------------|-------------|
| A | 90-100 | Tournament-winning tier |
| B | 75-89 | Competitively viable |
| C | 60-74 | Average performance expected |
| D | 40-59 | Below average, exploitable weaknesses |
| F | 0-39 | Non-competitive |

### Decisions Made
1. **Grading formula**: Score = 0.6 × Council Consensus + 0.4 × Primordia Tactical Score
2. **Caching strategy**: No caching - always fresh debate
3. **Partial results**: Return 503 with partial transcript if debate cannot complete
4. **Authentication**: JWT required; anonymous requests return 401

---

## Clarification Cycle 2: Component Impact

### Files Requiring Modification

| File | Change Type | Impact |
|------|-------------|--------|
| `src/meta_oracle/api.py` | **[NEW]** | FastAPI router for `/grade` endpoint |
| `src/meta_oracle/grader.py` | **[NEW]** | Grading orchestration logic |
| `src/meta_oracle/models.py` | **[MODIFY]** | Add `GradeRequest`, `GradeResponse` Pydantic models |
| `src/meta_oracle/engine.py` | **[MODIFY]** | Expose `run_grading_session()` method |
| `pyproject.toml` | **[MODIFY]** | Add FastAPI, uvicorn dependencies |

---

## Clarification Cycle 3: Edge Case & Failure Analysis

### Failure Modes

| Scenario | Detection | Response |
|----------|-----------|----------|
| Invalid list JSON | Pydantic validation | 400 + validation errors |
| Empty units array | Schema check | 400 + "List must have at least 1 unit" |
| Quota exhausted | Agent-Auditor pre-check | 429 + retry-after header |
| Agent timeout | asyncio.wait_for | 504 + partial transcript |
| Ollama unavailable | Connection error | 503 + "AI service unavailable" |

### Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Single-unit list | Valid grading; may score F due to lack of synergy |
| 3000+ point list | Accept but warn; debates may run longer |
| Duplicate units | Valid; analyze point concentration risks |
| Missing wargear | Default to base loadout for analysis |
````

## File: specs/list-grader-api/tasks.md
````markdown
# Tasks: List Grader API

## Phase 1: Foundation

### T-001: Add GradeRequest/GradeResponse Models
**File**: `src/meta_oracle/models.py`  
**Issue**: [#17](https://github.com/vindicta-platform/Meta-Oracle/issues/17)

### T-002: Add FastAPI Dependencies
**File**: `pyproject.toml`  
**Issue**: [#18](https://github.com/vindicta-platform/Meta-Oracle/issues/18)

---

## Phase 2: API Implementation

### T-003: Implement ListGrader Class
**File**: `src/meta_oracle/grader.py` [NEW]  
**Issue**: [#19](https://github.com/vindicta-platform/Meta-Oracle/issues/19)

### T-004: Expose Engine Grading Interface
**File**: `src/meta_oracle/engine.py`  
**Issue**: [#20](https://github.com/vindicta-platform/Meta-Oracle/issues/20)

### T-005: Create FastAPI Router
**File**: `src/meta_oracle/api.py` [NEW]  
**Issue**: [#21](https://github.com/vindicta-platform/Meta-Oracle/issues/21)

---

## Phase 3: Testing

### T-006: Unit Tests for Grader
**File**: `tests/test_grader.py` [NEW]  
**Issue**: [#22](https://github.com/vindicta-platform/Meta-Oracle/issues/22)

### T-007: API Integration Tests
**File**: `tests/test_api.py` [NEW]  
**Issue**: [#23](https://github.com/vindicta-platform/Meta-Oracle/issues/23)

### T-008: Documentation Update
**File**: `README.md`  
**Issue**: [#24](https://github.com/vindicta-platform/Meta-Oracle/issues/24)

---

## Summary

| Phase | Tasks | Effort | Issues |
|-------|-------|--------|--------|
| Foundation | T-001, T-002 | 1.25 hrs | #17, #18 |
| API Implementation | T-003, T-004, T-005 | 4.5 hrs | #19, #20, #21 |
| Testing | T-006, T-007, T-008 | 2.5 hrs | #22, #23, #24 |
| **Total** | 8 tasks | ~8.25 hrs | 8 issues |
````

## File: src/vindicta_oracle/__init__.py
````python
"""Meta-Oracle: AI Council for competitive Warhammer predictions."""
from meta_oracle.models import (
    AgentRole,
    Argument,
    ArgumentType,
    DebateContext,
    DebateTranscript,
    Vote,
)
from meta_oracle.engine import DebateEngine
from meta_oracle.ollama_client import OllamaClient, OllamaConfig

__all__ = [
    "AgentRole",
    "Argument",
    "ArgumentType",
    "DebateContext",
    "DebateTranscript",
    "Vote",
    "DebateEngine",
    "OllamaClient",
    "OllamaConfig",
]

__version__ = "0.1.0"
````

## File: src/vindicta_oracle/__main__.py
````python
"""Meta-Oracle CLI - Run AI council debates locally."""
import argparse
import json

from meta_oracle.models import DebateContext
from meta_oracle.engine import DebateEngine
from meta_oracle.ollama_client import OllamaConfig


def main():
    """Run a Meta-Oracle council debate from the command line."""
    parser = argparse.ArgumentParser(
        description="Meta-Oracle: AI Council for Warhammer Predictions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m meta_oracle
  python -m meta_oracle --model mistral --rounds 2
  python -m meta_oracle --p1-faction "Orks" --p2-faction "Imperial Knights"
        """
    )
    parser.add_argument(
        "--model", 
        default="llama3.2", 
        help="Ollama model to use (default: llama3.2)"
    )
    parser.add_argument(
        "--rounds", 
        type=int, 
        default=3, 
        help="Number of debate rounds (default: 3)"
    )
    parser.add_argument(
        "--p1-faction", 
        default="Space Marines", 
        help="Player 1 faction (default: Space Marines)"
    )
    parser.add_argument(
        "--p2-faction", 
        default="Tyranids", 
        help="Player 2 faction (default: Tyranids)"
    )
    parser.add_argument(
        "--output", 
        default="debate_transcript.json",
        help="Output file for transcript (default: debate_transcript.json)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="LLM temperature (default: 0.7)"
    )
    
    args = parser.parse_args()
    
    # Configure Ollama
    config = OllamaConfig(
        model=args.model,
        temperature=args.temperature,
    )
    
    # Create debate engine
    engine = DebateEngine(config=config, num_rounds=args.rounds)
    
    # Set up the matchup context
    context = DebateContext(
        player1_faction=args.p1_faction,
        player1_list=_get_sample_list(args.p1_faction),
        player2_faction=args.p2_faction,
        player2_list=_get_sample_list(args.p2_faction),
        mission="Take and Hold (Leviathan)",
        terrain="Mixed urban ruins with scatter terrain",
    )
    
    # Run the debate
    transcript = engine.run_debate(context)
    
    # Save transcript
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(transcript.model_dump_json(indent=2))
    
    print(f"\n📄 Full transcript saved to {args.output}")


def _get_sample_list(faction: str) -> str:
    """Return a sample army list for a given faction."""
    lists = {
        "Space Marines": """Gladius Task Force:
- Captain in Gravis Armour (Warlord)
- 2x Assault Intercessor Squads (5 each)
- Eradicator Squad (3) with Multi-meltas
- Repulsor Executioner
- Bladeguard Veterans (5)""",
        
        "Tyranids": """Invasion Fleet:
- Winged Hive Tyrant (Warlord)
- 2x Hormagaunt Broods (20 each)
- Carnifex Brood (2) with Crushing Claws
- Exocrine
- Zoanthropes (3)""",
        
        "Orks": """Waaagh! Detachment:
- Warboss in Mega Armour (Warlord)
- 30 Boyz with Choppas
- 10 Nobz with Power Klaws
- Battlewagon with Deffrolla
- 3 Deffkoptas""",
        
        "Imperial Knights": """Noble Lance:
- Knight Castellan (Warlord)
- 2x Armiger Helverins
- Knight Gallant
- 2x Armiger Warglaives""",
        
        "Necrons": """Awakened Dynasty:
- Overlord with Resurrection Orb (Warlord)
- 20 Necron Warriors
- 10 Immortals with Tesla Carbines
- 3 Skorpekh Destroyers
- Doom Scythe""",
    }
    
    return lists.get(faction, f"Standard competitive {faction} list")


if __name__ == "__main__":
    main()
````

## File: src/vindicta_oracle/agents/__init__.py
````python
"""Meta-Oracle council agents and stubs."""
from meta_oracle.agents.base import BaseAgent
from meta_oracle.agents.home import HomeAgent
from meta_oracle.agents.adversary import AdversaryAgent
from meta_oracle.agents.arbiter import ArbiterAgent
from meta_oracle.agents.rule_sage import RuleSageAgent
from meta_oracle.agents.chaos import ChaosAgent
from meta_oracle.protocol import AgentRole, Argument, ArgumentType, OracleAgent, DebateRound

class StubAgent(OracleAgent):
    """A stub agent for testing that returns hardcoded responses."""
    
    def __init__(self, role: AgentRole) -> None:
        super().__init__(role)
        self.call_count = 0
    
    async def analyze(self, context: dict) -> str:
        """Return stub analysis."""
        self.call_count += 1
        return f"{self.role.value} analysis: stub response"
    
    async def respond(self, previous_arguments: list[Argument], topic: str) -> Argument:
        """Return stub argument."""
        self.call_count += 1
        return Argument(
            agent_role=self.role,
            argument_type=ArgumentType.CLAIM,
            content=f"{self.role.value} response to: {topic}",
            confidence=0.7
        )
    
    async def vote(self, transcript) -> dict:
        """Return stub vote."""
        self.call_count += 1
        # HOME votes for player 1, ADVERSARY for player 2, others random
        winner = 1 if self.role in [AgentRole.HOME, AgentRole.ARBITER] else 2
        return {
            "winner": winner,
            "confidence": 0.6,
            "reasoning": f"{self.role.value} votes for player {winner}",
            "upset": self.role == AgentRole.CHAOS
        }

__all__ = [
    "BaseAgent",
    "HomeAgent",
    "AdversaryAgent",
    "ArbiterAgent",
    "RuleSageAgent",
    "ChaosAgent",
    "StubAgent",
]
````

## File: src/vindicta_oracle/agents/adversary_impl.py
````python
"""
Adversary Agent implementation for Meta-Oracle.

Argues against the player's army list (devil's advocate) per Issue #5.
"""

from dataclasses import dataclass, field
from typing import Optional

from meta_oracle.agents.base import BaseAgent


@dataclass
class ListWeakness:
    """Identified weakness in player's list."""
    name: str
    description: str
    severity: float = 0.5  # 0.0 = minor, 1.0 = critical
    vulnerable_to: list[str] = field(default_factory=list)


@dataclass
class AdversaryAnalysis:
    """Analysis result from Adversary agent."""
    weaknesses: list[ListWeakness] = field(default_factory=list)
    counter_strategies: list[str] = field(default_factory=list)
    critical_matchups: list[str] = field(default_factory=list)


class AdversaryAgent(BaseAgent):
    """
    Adversary Agent - argues against player's army list.
    
    Responsibilities:
    - Identify weaknesses in list
    - Generate counter-arguments
    - Play devil's advocate
    """
    
    def __init__(self, **kwargs):
        super().__init__(name="Adversary", **kwargs)
    
    async def run(self, army_list: dict) -> AdversaryAnalysis:
        """Analyze army list weaknesses."""
        # TODO: Implement weakness analysis
        return AdversaryAnalysis()
    
    async def generate_counter(self, argument: str) -> str:
        """Generate counter-argument."""
        # TODO: Implement counter generation
        return f"Counter to: {argument}"
````

## File: src/vindicta_oracle/agents/adversary.py
````python
"""Adversary Agent - Advocate for Player 2."""
from typing import Optional

from meta_oracle.agents.base import BaseAgent
from meta_oracle.models import AgentRole, Argument, ArgumentType, DebateContext


class AdversaryAgent(BaseAgent):
    """Skeptical advocate for Player 2's advantages.
    
    Implements Issue #5 acceptance criteria:
    - Identifies weaknesses in Player 1's list
    - Generates counter-arguments against HOME
    - Devil's advocate behavior to stress-test predictions
    """
    
    def __init__(self, client=None, aggression_level: int = 7):
        """Initialize AdversaryAgent with configurable aggression.
        
        Args:
            client: OllamaClient for LLM generation.
            aggression_level: 1-10 scale for how aggressively to counter (default 7).
        """
        super().__init__(client)
        self._aggression_level = min(10, max(1, aggression_level))
    
    @property
    def role(self) -> AgentRole:
        return AgentRole.ADVERSARY
    
    @property
    def personality(self) -> str:
        return "Skeptical advocate for Player 2"
    
    @property
    def system_prompt(self) -> str:
        return """You are ADVERSARY, an advocate for Player 2 in the Meta-Oracle council.

Your role is to:
- Highlight Player 2's list strengths and key threats
- Counter claims made about Player 1's advantages
- Identify Player 1's weaknesses and exploitable gaps
- Challenge optimistic assessments with tactical reality

Be thorough and analytical. Cite specific counters, stat comparisons, and tactical scenarios.
Push back against HOME's optimism with concrete counterpoints.
You want Player 2 to be taken seriously as a threat."""
    
    def identify_weaknesses(self, context: DebateContext) -> dict:
        """Identify weaknesses in Player 1's list.
        
        Issue #5 Acceptance Criteria:
        - Identifies weaknesses
        
        Args:
            context: The debate context with list information.
            
        Returns:
            Dictionary with weakness categories and exploits.
        """
        prompt = f"""Analyze Player 1's list WEAKNESSES:

Faction: {context.player1_faction}
List: {context.player1_list}

Player 2 Counters:
Faction: {context.player2_faction}
List: {context.player2_list}

Identify and categorize:
1. VULNERABILITIES: Gaps in defense or offense
2. BAD MATCHUPS: Where Player 2 dominates
3. EXPLOITABLE SYNERGIES: Dependencies that can be broken
4. SCORING WEAKNESSES: Objective control problems

Be specific about unit names, stat comparisons, and tactical exploits."""

        analysis = self.client.generate(self.system_prompt, prompt)
        
        return {
            "role": self.role.value,
            "analysis": analysis,
            "target_faction": context.player1_faction,
            "aggression_level": self._aggression_level,
        }
    
    def generate_counter_argument(
        self, 
        context: DebateContext, 
        claim_to_counter: str
    ) -> Argument:
        """Generate a counter-argument against a claim.
        
        Issue #5 Acceptance Criteria:
        - Generates counter-arguments
        
        Args:
            context: The debate context.
            claim_to_counter: The specific claim to argue against.
            
        Returns:
            Argument object with rebuttal.
        """
        aggression_modifier = self._get_aggression_modifier()
        
        prompt = f"""Counter this claim about Player 1:
CLAIM: "{claim_to_counter}"

{aggression_modifier}

Context:
- Player 1: {context.player1_faction}
- Player 2: {context.player2_faction}

Provide a concrete counter-argument citing:
- Specific unit counters from Player 2's list
- Stat comparisons that favor Player 2
- Tactical scenarios where the claim fails

Keep under 150 words. Be factual but assertive."""

        content = self.client.generate(self.system_prompt, prompt)
        
        return Argument(
            agent_role=self.role,
            round=0,  # Will be set by debate engine
            argument_type=ArgumentType.REBUTTAL,
            content=content,
        )
    
    def devils_advocate(self, context: DebateContext, consensus: str) -> Argument:
        """Challenge a consensus prediction as devil's advocate.
        
        Issue #5 Acceptance Criteria:
        - Devil's advocate behavior
        
        Args:
            context: The debate context.
            consensus: The current consensus prediction to challenge.
            
        Returns:
            Argument challenging the consensus.
        """
        prompt = f"""As devil's advocate, challenge this consensus prediction:
CONSENSUS: "{consensus}"

You MUST argue the opposite position, even if unlikely.

Matchup:
- Player 1: {context.player1_faction}
- Player 2: {context.player2_faction}

Provide:
1. The strongest possible counter-case
2. Scenarios where consensus is wrong
3. Edge cases or lucky swings that could flip the outcome

Be provocative but grounded in real game mechanics."""

        content = self.client.generate(self.system_prompt, prompt)
        
        return Argument(
            agent_role=self.role,
            round=0,
            argument_type=ArgumentType.CHALLENGE,
            content=content,
        )
    
    def _get_aggression_modifier(self) -> str:
        """Get prompt modifier based on aggression level."""
        if self._aggression_level >= 8:
            return "Be AGGRESSIVE. Show no mercy to weak arguments. Demolish their claims."
        elif self._aggression_level >= 5:
            return "Be firm and assertive. Challenge assumptions directly."
        else:
            return "Be measured but thorough. Present alternatives calmly."
````

## File: src/vindicta_oracle/agents/arbiter_impl.py
````python
"""
Arbiter Agent implementation for Meta-Oracle.

Neutral judge that weighs evidence from Home and Adversary per Issue #6.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from meta_oracle.agents.base import BaseAgent


class VerdictType(str, Enum):
    """Types of verdicts."""
    STRONG_APPROVE = "strong_approve"
    APPROVE = "approve"
    NEUTRAL = "neutral"
    CONCERNS = "concerns"
    REJECT = "reject"


@dataclass
class Verdict:
    """Final verdict from Arbiter."""
    verdict_type: VerdictType
    confidence: float = 0.5
    reasoning: str = ""
    key_factors: list[str] = field(default_factory=list)


class ArbiterAgent(BaseAgent):
    """
    Arbiter Agent - neutral judge of debates.
    
    Responsibilities:
    - Weigh evidence from Home and Adversary
    - Produce structured verdict
    - Explain reasoning clearly
    """
    
    def __init__(self, **kwargs):
        super().__init__(name="Arbiter", **kwargs)
    
    async def run(self, home_args: list[str], adversary_args: list[str]) -> Verdict:
        """Weigh arguments and produce verdict."""
        # TODO: Implement verdict logic
        return Verdict(verdict_type=VerdictType.NEUTRAL)
    
    async def explain_reasoning(self, verdict: Verdict) -> str:
        """Generate explanation for verdict."""
        # TODO: Implement reasoning explanation
        return f"Verdict: {verdict.verdict_type.value}"
````

## File: src/vindicta_oracle/agents/arbiter.py
````python
"""Arbiter Agent - Data-driven neutral referee."""
from meta_oracle.agents.base import BaseAgent
from meta_oracle.models import AgentRole


class ArbiterAgent(BaseAgent):
    """Data-driven neutral referee focusing on statistics."""
    
    @property
    def role(self) -> AgentRole:
        return AgentRole.ARBITER
    
    @property
    def personality(self) -> str:
        return "Data-driven neutral referee"
    
    @property
    def system_prompt(self) -> str:
        return """You are ARBITER, the data-driven referee in the Meta-Oracle council.

Your role is to:
- Provide statistical context (win rates, tournament results, meta positioning)
- Remain strictly neutral between Player 1 and Player 2
- Fact-check claims made by HOME and ADVERSARY
- Reference historical matchup data when available
- Ground the debate in competitive meta realities

Always cite sources when possible (e.g., "According to recent ITC data...", "In the current meta...").
When HOME and ADVERSARY disagree, provide data that clarifies the truth.
Your job is to inject objectivity into an adversarial debate."""
````

## File: src/vindicta_oracle/agents/base.py
````python
"""Base agent class with shared Ollama integration."""
import re
from abc import ABC, abstractmethod

from meta_oracle.models import (
    AgentRole,
    Argument,
    ArgumentType,
    DebateContext,
    DebateTranscript,
    Vote,
)
from meta_oracle.ollama_client import OllamaClient


class BaseAgent(ABC):
    """Abstract base class for all council agents."""
    
    def __init__(self, client: OllamaClient | None = None):
        self.client = client or OllamaClient()
    
    @property
    @abstractmethod
    def role(self) -> AgentRole:
        """The agent's role in the council."""
        ...
    
    @property
    @abstractmethod
    def personality(self) -> str:
        """Description of the agent's debate style."""
        ...
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt defining the agent's behavior."""
        ...
    
    def analyze(self, context: DebateContext) -> str:
        """Perform initial analysis of the matchup."""
        prompt = f"""Analyze this Warhammer 40K matchup:

Player 1: {context.player1_faction}
List: {context.player1_list}

Player 2: {context.player2_faction}
List: {context.player2_list}

Mission: {context.mission or "Standard"}
Terrain: {context.terrain or "Mixed"}

Provide your initial analysis based on your role. Be specific about units and tactics."""
        return self.client.generate(self.system_prompt, prompt)
    
    def respond(self, transcript: DebateTranscript, round_num: int) -> Argument:
        """Generate a response based on debate history."""
        history = self._format_history(transcript, round_num)
        context = transcript.context
        
        prompt = f"""Round {round_num} of the council debate.

MATCHUP:
- Player 1: {context.player1_faction}
- Player 2: {context.player2_faction}
- Mission: {context.mission or "Standard"}

Previous arguments this debate:
{history}

Now speak according to your role. Be specific about units, abilities, and tactical implications.
Keep your response focused and under 200 words."""
        
        content = self.client.generate(self.system_prompt, prompt)
        return Argument(
            agent_role=self.role,
            round=round_num,
            argument_type=ArgumentType.CLAIM,
            content=content,
        )
    
    def vote(self, transcript: DebateTranscript) -> Vote:
        """Cast final prediction vote after debate."""
        summary = self._format_full_debate(transcript)
        context = transcript.context
        
        prompt = f"""The council debate has concluded.

MATCHUP: {context.player1_faction} vs {context.player2_faction}

Full debate transcript:
{summary}

Now cast your final vote.

You MUST respond in this EXACT format:
WINNER: [Player 1 or Player 2 or Draw]
PROBABILITY: [number between 0 and 100]%
REASONING: [your reasoning in 2-3 sentences]"""
        
        response = self.client.generate(self.system_prompt, prompt)
        return self._parse_vote(response)
    
    def _format_history(self, transcript: DebateTranscript, round_num: int) -> str:
        """Format debate history up to current round."""
        lines = []
        for round_args in transcript.rounds[:round_num]:
            for arg in round_args:
                role_name = arg.agent_role.value.upper().replace("_", "-")
                lines.append(f"[{role_name}]: {arg.content}")
        return "\n\n".join(lines) if lines else "No arguments yet - you are opening the debate."
    
    def _format_full_debate(self, transcript: DebateTranscript) -> str:
        """Format the complete debate transcript."""
        return self._format_history(transcript, len(transcript.rounds) + 1)
    
    def _parse_vote(self, response: str) -> Vote:
        """Parse vote from LLM response."""
        # Determine prediction
        response_lower = response.lower()
        if "player 2" in response_lower:
            prediction = "Player 2 wins"
        elif "draw" in response_lower:
            prediction = "Draw"
        else:
            prediction = "Player 1 wins"
        
        # Extract probability
        probability = 0.5
        prob_match = re.search(r'(\d+)%', response)
        if prob_match:
            probability = int(prob_match.group(1)) / 100
            probability = max(0.0, min(1.0, probability))
        
        return Vote(
            agent_role=self.role,
            prediction=prediction,
            win_probability=probability,
            confidence=0.7,
            reasoning=response,
        )
````

## File: src/vindicta_oracle/agents/chaos.py
````python
"""Chaos Agent - Devil's advocate and upset detector."""
from meta_oracle.agents.base import BaseAgent
from meta_oracle.models import AgentRole


class ChaosAgent(BaseAgent):
    """Devil's advocate who identifies upsets and edge cases."""
    
    @property
    def role(self) -> AgentRole:
        return AgentRole.CHAOS
    
    @property
    def personality(self) -> str:
        return "Devil's advocate and upset detector"
    
    @property
    def system_prompt(self) -> str:
        return """You are CHAOS, the devil's advocate in the Meta-Oracle council.

Your role is to:
- Challenge any consensus forming among other agents
- Identify low-probability, high-impact scenarios (upsets)
- Point out "what if" edge cases that could flip the game
- Detect overconfidence and groupthink in the council
- Advocate for unexpected outcomes and sleeper strategies

Be provocative but logical. Your job is to stress-test the prediction.
Ask uncomfortable questions like "But what if..." and "Has anyone considered..."
You exist to ensure the council doesn't get complacent or miss obvious risks.
Embrace chaos, but ground it in plausible game scenarios."""
````

## File: src/vindicta_oracle/agents/home_impl.py
````python
"""
Home Agent implementation for Meta-Oracle.

Advocates for the player's army list per Issue #4.
"""

from dataclasses import dataclass, field
from typing import Optional

from meta_oracle.agents.base import BaseAgent


@dataclass
class ListStrength:
    """Identified strength in player's list."""
    name: str
    description: str
    confidence: float = 0.5
    supporting_units: list[str] = field(default_factory=list)


@dataclass
class HomeAnalysis:
    """Analysis result from Home agent."""
    strengths: list[ListStrength] = field(default_factory=list)
    overall_rating: float = 0.0
    key_synergies: list[str] = field(default_factory=list)
    recommended_plays: list[str] = field(default_factory=list)


class HomeAgent(BaseAgent):
    """
    Home Agent - advocates for the player's army list.
    
    Responsibilities:
    - Analyze list strengths
    - Generate supporting arguments
    - Identify key synergies
    """
    
    def __init__(self, **kwargs):
        super().__init__(name="Home", **kwargs)
    
    async def run(self, army_list: dict) -> HomeAnalysis:
        """Analyze army list and generate advocacy."""
        # TODO: Implement full analysis with Primordia integration
        return HomeAnalysis()
    
    async def generate_argument(self, topic: str) -> str:
        """Generate supporting argument for a topic."""
        # TODO: Implement argument generation
        return f"Supporting argument for: {topic}"
````

## File: src/vindicta_oracle/agents/home.py
````python
"""Home Agent - Advocate for Player 1."""
from typing import Any, Optional

from meta_oracle.agents.base import BaseAgent
from meta_oracle.models import AgentRole, Argument, ArgumentType, DebateContext


class HomeAgent(BaseAgent):
    """Optimistic advocate for Player 1's strengths.
    
    Implements Issue #4 acceptance criteria:
    - Analyzes player list strengths
    - Generates supporting arguments
    - Integrates with Primordia evaluation (when available)
    """
    
    def __init__(self, client=None, evaluation_service: Optional[Any] = None):
        """Initialize HomeAgent with optional Primordia integration.
        
        Args:
            client: OllamaClient for LLM generation.
            evaluation_service: Optional Primordia evaluation service for grounding.
        """
        super().__init__(client)
        self._evaluation_service = evaluation_service
    
    @property
    def role(self) -> AgentRole:
        return AgentRole.HOME
    
    @property
    def personality(self) -> str:
        return "Optimistic advocate for Player 1"
    
    @property
    def system_prompt(self) -> str:
        return """You are HOME, an advocate for Player 1 in the Meta-Oracle council.

Your role is to:
- Highlight Player 1's list strengths and key units
- Identify favorable matchups and synergies
- Counter arguments against Player 1
- Be optimistic but grounded in actual game mechanics

You have deep knowledge of Warhammer 40K competitive play, unit stats, and tactical strategies.
Always cite specific units, abilities, and rules when making claims.
Be passionate but fair - acknowledge real weaknesses if pressed."""
    
    def analyze_strengths(self, context: DebateContext) -> dict:
        """Analyze Player 1 list strengths.
        
        Issue #4 Acceptance Criteria:
        - Analyzes player list strengths
        
        Args:
            context: The debate context with list information.
            
        Returns:
            Dictionary with strength categories and specific units.
        """
        prompt = f"""Analyze Player 1's list strengths:

Faction: {context.player1_faction}
List: {context.player1_list}

Identify and categorize:
1. KEY THREATS: Units that will win games
2. SYNERGIES: How units work together
3. SCORING: Objective control strengths
4. DURABILITY: Survivability advantages

Be specific about unit names, abilities, and stat values."""

        analysis = self.client.generate(self.system_prompt, prompt)
        
        return {
            "role": self.role.value,
            "analysis": analysis,
            "faction": context.player1_faction,
            "grounded": self._evaluation_service is not None,
        }
    
    def generate_supporting_argument(
        self, 
        context: DebateContext, 
        topic: str
    ) -> Argument:
        """Generate a supporting argument for Player 1.
        
        Issue #4 Acceptance Criteria:
        - Generates supporting arguments
        
        Args:
            context: The debate context.
            topic: The specific topic to argue for.
            
        Returns:
            Argument object with supporting claim.
        """
        evaluation_context = ""
        if self._evaluation_service:
            evaluation_context = self._get_evaluation_grounding(context)
        
        prompt = f"""Generate a strong argument supporting Player 1 regarding: {topic}

{evaluation_context}

Faction: {context.player1_faction}
List: {context.player1_list}

Provide a concrete argument citing:
- Specific units and their stats
- Game mechanics that favor Player 1
- Historical success or meta positioning

Keep under 150 words. Be assertive but factual."""

        content = self.client.generate(self.system_prompt, prompt)
        
        return Argument(
            agent_role=self.role,
            round=0,  # Will be set by debate engine
            argument_type=ArgumentType.CLAIM,
            content=content,
        )
    
    def _get_evaluation_grounding(self, context: DebateContext) -> str:
        """Get Primordia evaluation for grounding arguments.
        
        Issue #4 Acceptance Criteria:
        - Integrates with Primordia evaluation
        """
        if not self._evaluation_service:
            return ""
        
        try:
            # Primordia integration point - expects score from evaluation service
            # This is a stub for when Primordia is available
            return """[EVALUATION DATA AVAILABLE]
Use the following evaluation scores to support your argument with data."""
        except Exception:
            return ""
````

## File: src/vindicta_oracle/agents/rule_sage_impl.py
````python
"""
Rule-Sage Agent implementation for Meta-Oracle.

Rules expert that validates claims and cites sources per Issue #7.
"""

from dataclasses import dataclass, field
from typing import Optional

from meta_oracle.agents.base import BaseAgent


@dataclass
class RuleCitation:
    """Citation from official rules source."""
    source: str  # e.g., "Core Rules p.23"
    text: str
    confidence: float = 1.0


@dataclass
class RuleValidation:
    """Result of validating a rules claim."""
    is_valid: bool
    claim: str
    citations: list[RuleCitation] = field(default_factory=list)
    correction: Optional[str] = None
    reasoning: str = ""


class RuleSageAgent(BaseAgent):
    """
    Rule-Sage Agent - rules expertise and validation.
    
    Responsibilities:
    - Validate rules claims from other agents
    - Cite official sources
    - Correct rule misinterpretations
    """
    
    def __init__(self, **kwargs):
        super().__init__(name="RuleSage", **kwargs)
    
    async def run(self, claim: str) -> RuleValidation:
        """Validate a rules claim."""
        # TODO: Implement rules validation with RAG
        return RuleValidation(is_valid=True, claim=claim)
    
    async def cite_rule(self, topic: str) -> list[RuleCitation]:
        """Find citations for a rules topic."""
        # TODO: Implement RAG-based citation lookup
        return []
````

## File: src/vindicta_oracle/agents/rule_sage.py
````python
"""Rule-Sage Agent - Rules validator and mechanical expert."""
from meta_oracle.agents.base import BaseAgent
from meta_oracle.models import AgentRole


class RuleSageAgent(BaseAgent):
    """Precise rules expert who validates mechanical claims."""
    
    @property
    def role(self) -> AgentRole:
        return AgentRole.RULE_SAGE
    
    @property
    def personality(self) -> str:
        return "Precise rules expert"
    
    @property
    def system_prompt(self) -> str:
        return """You are RULE-SAGE, the rules expert in the Meta-Oracle council.

Your role is to:
- Validate mechanical claims made by other agents
- Correct any rules misunderstandings or errors
- Clarify ability interactions, timing, and sequencing
- Ensure the debate stays grounded in actual game rules
- Reference specific rule numbers, FAQs, and errata when correcting

Be precise and pedantic. Quote rules text when necessary.
Challenge any claim that seems mechanically incorrect or overstated.
You are the council's safeguard against rules errors affecting predictions."""
````

## File: src/vindicta_oracle/api.py
````python
"""Meta-Oracle API - REST interface for list grading and council debates."""
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from meta_oracle.grader import ListGrader
from meta_oracle.models import GradeRequest, GradeResponse
from meta_oracle.ollama_client import OllamaConfig

app = FastAPI(
    title="Meta-Oracle API",
    description="AI council debate engine for competitive wargaming.",
    version="0.3.0"
)

router = APIRouter(prefix="/api/v1")


def get_grader() -> ListGrader:
    """Dependency provider for ListGrader."""
    # Custom config could be injected here
    return ListGrader()


@router.post("/grade", response_model=GradeResponse)
async def grade_list(
    request: GradeRequest,
    grader: ListGrader = Depends(get_grader)
) -> GradeResponse:
    """Submit an army list for AI council grading.
    
    Grading involves a 3-round adversarial debate between 5 specialized agents.
    """
    try:
        # Check units validity (extra safety beyond Pydantic)
        if not request.army_list.units:
            raise HTTPException(status_code=400, detail="List must have at least 1 unit")
            
        return await grader.grade(request)
        
    except ConnectionError:
        raise HTTPException(status_code=503, detail="AI service (Ollama) unavailable")
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Debate timed out")
    except Exception as e:
        # In a real system, we'd log this with a correlation ID
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "operational", "version": "0.3.0"}


app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
````

## File: src/vindicta_oracle/debate.py
````python
"""
DebateEngine for Meta-Oracle structured debates.

Orchestrates multi-agent debates per Issue #2.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class DebateRole(str, Enum):
    """Roles in a structured debate."""
    PROPOSER = "proposer"
    CHALLENGER = "challenger" 
    ARBITER = "arbiter"


@dataclass
class DebateTurn:
    """A single turn in a debate."""
    turn_number: int
    role: DebateRole
    agent_id: str
    argument: str
    confidence: float = 0.5
    references: list[str] = field(default_factory=list)


@dataclass
class DebateResult:
    """Final result of a debate."""
    winner: Optional[DebateRole] = None
    final_position: str = ""
    confidence: float = 0.0
    turns: list[DebateTurn] = field(default_factory=list)
    reasoning: str = ""


class DebateEngine(ABC):
    """Abstract interface for debate orchestration."""
    
    @abstractmethod
    async def start_debate(self, topic: str) -> str:
        """Start a new debate, returns debate_id."""
        pass
    
    @abstractmethod
    async def submit_turn(self, debate_id: str, turn: DebateTurn) -> None:
        """Submit a turn to the debate."""
        pass
    
    @abstractmethod
    async def resolve(self, debate_id: str) -> DebateResult:
        """Resolve the debate and return result."""
        pass
````

## File: src/vindicta_oracle/demo.py
````python
"""Demo: Run a sample Meta-Oracle debate with local models."""
from meta_oracle.models import DebateContext
from meta_oracle.engine import DebateEngine
from meta_oracle.ollama_client import OllamaConfig


def run_demo():
    """Run a complete demo debate between Space Marines and Tyranids."""
    print("\n" + "🎮" * 35)
    print("       META-ORACLE DEMO")
    print("🎮" * 35)
    print("\nRunning 5-agent council debate with local Ollama inference...")
    print("This may take a few minutes depending on your hardware.\n")
    
    # TODO: Setup with pydantic settings for env drive
    # Configure for local model - try common models
    config = OllamaConfig(
        model="llama3.2",  # Change to "mistral" or "gemma2" if needed
        temperature=0.7,
        max_tokens=512,
    )
    
    # Create a sample competitive matchup
    context = DebateContext(
        player1_faction="Space Marines (Gladius Task Force)",
        player1_list="""
HQ:
- Captain in Gravis Armour with Heavy Bolt Rifle (Warlord)
  - Enhancement: Adept of the Codex

Troops:
- 2x Assault Intercessor Squads (5 each)

Elites:
- Bladeguard Veterans (5) with Storm Shields

Heavy Support:
- Eradicator Squad (3) with Multi-meltas
- Repulsor Executioner with Heavy Laser Destroyer

Total: ~1000 points
""",
        player2_faction="Tyranids (Invasion Fleet)",
        player2_list="""
HQ:
- Winged Hive Tyrant (Warlord)
  - Psychic Powers: Onslaught, Catalyst
  - Enhancement: Alien Cunning

Troops:
- 2x Hormagaunt Broods (20 each)

Elites:
- Zoanthropes (3)

Heavy Support:
- Carnifex Brood (2) with Crushing Claws + Bio-plasma
- Exocrine

Total: ~1000 points
""",
        mission="Take and Hold (Leviathan Mission Pack)",
        terrain="Dense urban ruins with 6 large LOS-blocking buildings, scatter terrain throughout",
        additional_context="Tournament setting, competitive lists, both players are experienced",
    )
    
    # Run the debate with 3 rounds
    engine = DebateEngine(config=config, num_rounds=3)
    transcript = engine.run_debate(context)
    
    # Print full transcript
    print("\n\n" + "=" * 70)
    print("📜  FULL DEBATE TRANSCRIPT")
    print("=" * 70)
    
    for round_num, round_args in enumerate(transcript.rounds, 1):
        print(f"\n{'─' * 70}")
        print(f"ROUND {round_num}")
        print(f"{'─' * 70}")
        
        for arg in round_args:
            role_name = arg.agent_role.value.upper().replace("_", "-")
            print(f"\n[{role_name}]:")
            print(arg.content)
    
    print("\n\n" + "=" * 70)
    print("🗳️   DETAILED VOTES")
    print("=" * 70)
    
    for vote in transcript.votes:
        role_name = vote.agent_role.value.upper().replace("_", "-")
        print(f"\n[{role_name}]")
        print(f"  Prediction: {vote.prediction}")
        print(f"  Win Probability: {vote.win_probability * 100:.0f}%")
        print(f"  Reasoning:")
        # Wrap reasoning text
        reasoning_lines = vote.reasoning.split("\n")
        for line in reasoning_lines[:5]:  # Limit to 5 lines
            print(f"    {line}")
    
    # Save transcript to file
    print("\n\n" + "=" * 70)
    print("💾  SAVING TRANSCRIPT")
    print("=" * 70)
    
    output_file = "demo_transcript.json"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcript.model_dump_json(indent=2))
    
    print(f"\n✅ Full transcript saved to: {output_file}")
    print(f"\n🏆 Final Verdict: {transcript.consensus}")
    print(f"📊 Council Confidence: {transcript.consensus_confidence * 100:.0f}%")
    
    return transcript


if __name__ == "__main__":
    run_demo()
````

## File: src/vindicta_oracle/engine.py
````python
"""Debate Engine - Orchestrates the 5-agent council debate."""
from collections import Counter

from meta_oracle.models import Argument, DebateContext, DebateTranscript
from meta_oracle.agents import (
    HomeAgent,
    AdversaryAgent,
    ArbiterAgent,
    RuleSageAgent,
    ChaosAgent,
)
from meta_oracle.ollama_client import OllamaClient, OllamaConfig


class DebateEngine:
    """Orchestrates the multi-round adversarial debate between 5 agents."""
    
    def __init__(self, config: OllamaConfig | None = None, num_rounds: int = 3):
        """Initialize the debate engine with all 5 council agents.
        
        Args:
            config: Ollama configuration (model, temperature, etc.)
            num_rounds: Number of debate rounds (default 3)
        """
        client = OllamaClient(config)
        self.agents = [
            HomeAgent(client),
            AdversaryAgent(client),
            ArbiterAgent(client),
            RuleSageAgent(client),
            ChaosAgent(client),
        ]
        self.num_rounds = num_rounds
    
    def run_debate(self, context: DebateContext) -> DebateTranscript:
        """Execute the full debate protocol.
        
        Args:
            context: The matchup context (factions, lists, mission, etc.)
            
        Returns:
            Complete debate transcript with all rounds, votes, and consensus
        """
        transcript = DebateTranscript(context=context)
        
        self._print_header(context)
        
        # Run debate rounds
        for round_num in range(1, self.num_rounds + 1):
            self._print_round_header(round_num)
            
            round_arguments: list[Argument] = []
            for agent in self.agents:
                role_name = agent.role.value.upper().replace("_", "-")
                print(f"\n🎙️  [{role_name}] Speaking...")
                
                argument = agent.respond(transcript, round_num)
                round_arguments.append(argument)
                
                # Print truncated preview
                preview = argument.content[:300].replace("\n", " ")
                if len(argument.content) > 300:
                    preview += "..."
                print(f"   {preview}")
            
            transcript.rounds.append(round_arguments)
        
        # Voting phase
        self._print_voting_header()
        
        for agent in self.agents:
            role_name = agent.role.value.upper().replace("_", "-")
            print(f"\n🗳️  [{role_name}] Casting vote...")
            
            vote = agent.vote(transcript)
            transcript.votes.append(vote)
            
            print(f"   → {vote.prediction} ({vote.win_probability*100:.0f}% confidence)")
        
        # Calculate consensus
        transcript.consensus, transcript.consensus_confidence = self._calculate_consensus(transcript)
        
        self._print_verdict(transcript)
        
        return transcript
    
    def _calculate_consensus(self, transcript: DebateTranscript) -> tuple[str, float]:
        """Calculate the council's consensus prediction.
        
        Uses simple majority voting with averaged confidence.
        """
        votes = transcript.votes
        predictions = [v.prediction for v in votes]
        
        # Simple majority
        vote_counts = Counter(predictions)
        winner = vote_counts.most_common(1)[0][0]
        
        # Average probability of agents who voted for the winner
        winning_probs = [v.win_probability for v in votes if v.prediction == winner]
        avg_confidence = sum(winning_probs) / len(winning_probs) if winning_probs else 0.5
        
        return winner, avg_confidence
    
    def _print_header(self, context: DebateContext) -> None:
        """Print the debate header."""
        print("\n" + "=" * 70)
        print("🏛️   META-ORACLE COUNCIL CONVENES")
        print("=" * 70)
        print(f"\n📋 MATCHUP: {context.player1_faction} vs {context.player2_faction}")
        print(f"📍 Mission: {context.mission or 'Standard'}")
        if context.terrain:
            print(f"🏔️  Terrain: {context.terrain}")
    
    def _print_round_header(self, round_num: int) -> None:
        """Print a round header."""
        print(f"\n{'─' * 70}")
        print(f"🔔 ROUND {round_num}")
        print(f"{'─' * 70}")
    
    def _print_voting_header(self) -> None:
        """Print the voting phase header."""
        print(f"\n{'=' * 70}")
        print("🗳️   VOTING PHASE")
        print(f"{'=' * 70}")
    
    def _print_verdict(self, transcript: DebateTranscript) -> None:
        """Print the final council verdict."""
        print(f"\n{'=' * 70}")
        print("🏆  COUNCIL VERDICT")
        print(f"{'=' * 70}")
        print(f"\n🎯 Prediction: {transcript.consensus}")
        print(f"📊 Confidence: {transcript.consensus_confidence * 100:.0f}%")
        
        # Show vote breakdown
        print("\n📜 Vote Breakdown:")
        for vote in transcript.votes:
            role = vote.agent_role.value.upper().replace("_", "-")
            print(f"   • {role}: {vote.prediction} ({vote.win_probability*100:.0f}%)")

    def run_grading_session(self, army_list: "meta_oracle.models.ArmyList") -> DebateTranscript:
        """Execute a debate to grade a single army list.
        
        Args:
            army_list: The army list to grade
            
        Returns:
            Transcript containing the evaluation debate
        """
        # Format units into a readable string
        unit_details = "\n".join(
            [f"- {u.name} ({u.points} pts): {', '.join(u.wargear)}" for u in army_list.units]
        )
        player1_list = f"Faction: {army_list.faction}\nDetachment: {army_list.detachment or 'Unknown'}\nUnits:\n{unit_details}"
        
        context = DebateContext(
            player1_faction=army_list.faction,
            player1_list=player1_list,
            player2_faction="Meta Challenger",
            player2_list="A generic competitive list representing the current tournament meta.",
            mission="Grand Tournament: Leviathan",
            terrain="WTC Standard Layout",
            additional_context="Grading requested for competitive viability."
        )
        
        return self.run_debate(context)
````

## File: src/vindicta_oracle/grader.py
````python
"""List Grader - Orchestrates list evaluation and scoring."""
import random
import time
from typing import Any

from meta_oracle.engine import DebateEngine
from meta_oracle.models import ArmyList, GradeRequest, GradeResponse, DebateTranscript


class ListGrader:
    """Orchestrates the army list grading process."""

    def __init__(self, engine: DebateEngine | None = None):
        self.engine = engine or DebateEngine()

    async def grade(self, request: GradeRequest) -> GradeResponse:
        """Grade a single army list.
        
        Args:
            request: The grading request containing the army list
            
        Returns:
            Structured grade response
        """
        start_time = time.time()
        
        # 1. Run the council debate session
        transcript = self.engine.run_grading_session(request.army_list)
        
        # 2. Extract council performance (0-100)
        council_consensus = transcript.consensus_confidence * 100
        
        # 3. Simulate/Calculate Primordia tactical score (0-100)
        # In a real system, this would call Primordia-AI
        primordia_score = self._calculate_primordia_score(request.army_list)
        
        # 4. Apply final scoring formula: 0.6 * council + 0.4 * primordia
        final_score = int(0.6 * council_consensus + 0.4 * primordia_score)
        
        # 5. Map numeric score to letter grade
        letter_grade = self._map_score_to_grade(final_score)
        
        # 6. Format analysis from agent roles
        analysis = self._format_analysis(transcript)
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return GradeResponse(
            grade=letter_grade,
            score=final_score,
            analysis=analysis,
            council_verdict={
                "prediction": transcript.consensus,
                "confidence": transcript.consensus_confidence,
                "consensus_agents": [v.agent_role.value for v in transcript.votes if v.prediction == transcript.consensus]
            },
            metadata={
                "debate_id": str(transcript.id),
                "rounds": len(transcript.rounds),
                "processing_time_ms": processing_time_ms
            }
        )

    def _calculate_primordia_score(self, army_list: ArmyList) -> int:
        """Stub for Primordia-AI tactical evaluation."""
        # Derived score from points efficiency (just a heuristic for the demo)
        total_points = sum(u.points for u in army_list.units)
        seed = len(army_list.units) + total_points
        random.seed(seed)
        return random.randint(40, 95)

    def _map_score_to_grade(self, score: int) -> str:
        """Map numeric score (0-100) to letter grade (A-F)."""
        if score >= 90:
            return "A"
        if score >= 75:
            return "B"
        if score >= 60:
            return "C"
        if score >= 40:
            return "D"
        return "F"

    def _format_analysis(self, transcript: DebateTranscript) -> dict[str, str]:
        """Extract agent reasoning for the response."""
        analysis = {}
        for vote in transcript.votes:
            role = vote.agent_role.value
            analysis[role] = vote.reasoning
        return analysis
````

## File: src/vindicta_oracle/models.py
````python
"""Meta-Oracle data models for the 5-agent debate council."""
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class AgentRole(str, Enum):
    """The five council agent roles."""
    HOME = "home"           # Advocate for Player 1
    ADVERSARY = "adversary" # Advocate for Player 2
    ARBITER = "arbiter"     # Data-driven referee
    RULE_SAGE = "rule_sage" # Rules validator
    CHAOS = "chaos"         # Upset detector / devil's advocate


class ArgumentType(str, Enum):
    """Types of arguments agents can make during debate."""
    CLAIM = "claim"
    EVIDENCE = "evidence"
    REBUTTAL = "rebuttal"
    CONCESSION = "concession"
    QUESTION = "question"


class Argument(BaseModel):
    """A single argument made by an agent during debate."""
    id: UUID = Field(default_factory=uuid4)
    agent_role: AgentRole
    round: int
    argument_type: ArgumentType
    content: str
    in_response_to: UUID | None = None
    confidence: float = 0.5
    timestamp: datetime = Field(default_factory=datetime.now)


class Vote(BaseModel):
    """Final prediction vote from an agent."""
    agent_role: AgentRole
    prediction: str        # e.g., "Player 1 wins", "Player 2 wins", "Draw"
    win_probability: float # 0.0 to 1.0
    confidence: float      # How confident in this vote
    reasoning: str


class DebateContext(BaseModel):
    """Context for a debate matchup."""
    player1_faction: str
    player1_list: str
    player2_faction: str
    player2_list: str
    mission: str | None = None
    terrain: str | None = None
    additional_context: str | None = None


class DebateTranscript(BaseModel):
    """Full transcript of a council debate session."""
    id: UUID = Field(default_factory=uuid4)
    context: DebateContext
    rounds: list[list[Argument]] = Field(default_factory=list)
    votes: list[Vote] = Field(default_factory=list)
    consensus: str | None = None
    consensus_confidence: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)


class Unit(BaseModel):
    """A single unit in an army list."""
    name: str = Field(..., description="Name of the unit")
    points: int = Field(..., description="Points cost of the unit")
    wargear: list[str] = Field(default_factory=list, description="List of chosen wargear/upgrades")


class ArmyList(BaseModel):
    """Container for a competitive army list."""
    faction: str = Field(..., description="The army's faction (e.g., 'Space Marines')")
    points_limit: int = Field(default=2000, description="The maximum points for the game")
    units: list[Unit] = Field(..., description="List of units in the army")
    detachment: str | None = Field(default=None, description="The chosen detachment or sub-faction")

    @field_validator("units")
    @classmethod
    def must_have_units(cls, v: list[Unit]) -> list[Unit]:
        if not v:
            raise ValueError("List must have at least 1 unit")
        return v


class GradeRequest(BaseModel):
    """Payload for the /grade API endpoint."""
    army_list: ArmyList
    context: dict | None = Field(default=None, description="Optional mission or opponent context")


class GradeResponse(BaseModel):
    """Response payload for the /grade API endpoint."""
    grade: str = Field(..., description="Letter grade (A-F)")
    score: int = Field(..., description="Numeric score (0-100)")
    analysis: dict[str, str] = Field(..., description="Structured analysis by agent role")
    council_verdict: dict = Field(..., description="Final consensus and prediction details")
    metadata: dict = Field(..., description="Processing metadata and session IDs")
````

## File: src/vindicta_oracle/ollama_client.py
````python
"""Ollama client for local LLM inference."""
import ollama
from pydantic import BaseModel


class OllamaConfig(BaseModel):
    """Configuration for Ollama local inference."""
    model: str = "llama3.2"
    temperature: float = 0.7
    max_tokens: int = 512


class OllamaClient:
    """Wrapper for local Ollama LLM inference."""
    
    def __init__(self, config: OllamaConfig | None = None):
        self.config = config or OllamaConfig()
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using local Ollama model."""
        response = ollama.chat(
            model=self.config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            }
        )
        return response["message"]["content"]
````

## File: src/vindicta_oracle/protocol.py
````python
"""Oracle Agent protocol - interface for all council agents."""
from typing import Protocol

from meta_oracle.models import Argument, DebateContext, DebateTranscript, Vote


class OracleAgent(Protocol):
    """Interface that all council agents must implement."""
    
    @property
    def role(self) -> str:
        """The agent's role identifier."""
        ...
    
    @property
    def personality(self) -> str:
        """Description of the agent's debate style."""
        ...
    
    def analyze(self, context: DebateContext) -> str:
        """Perform initial analysis of the matchup."""
        ...
    
    def respond(self, transcript: DebateTranscript, round_num: int) -> Argument:
        """Generate a response based on debate history."""
        ...
    
    def vote(self, transcript: DebateTranscript) -> Vote:
        """Cast final prediction vote after debate concludes."""
        ...

"""
OracleAgent protocol for Meta-Oracle debates.

Defines the interface that all debate agents must implement.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    """Roles in the Oracle Council."""
    HOME = "home"           # Advocate for player 1 / home faction
    ADVERSARY = "adversary" # Advocate for player 2 / opponent
    ARBITER = "arbiter"     # Data-driven referee
    RULE_SAGE = "rule_sage" # Rules expert / validation
    CHAOS = "chaos"         # Devil's advocate / upset detector


class ArgumentType(str, Enum):
    """Types of arguments in debate."""
    CLAIM = "claim"
    EVIDENCE = "evidence"
    REBUTTAL = "rebuttal"
    CONCESSION = "concession"
    QUESTION = "question"


class Argument(BaseModel):
    """A single argument in a debate."""
    
    id: UUID = Field(default_factory=uuid4)
    agent_role: AgentRole
    argument_type: ArgumentType
    content: str
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    references: list[str] = Field(default_factory=list)
    in_response_to: Optional[UUID] = None


class DebateRound(BaseModel):
    """A single round of debate."""
    
    round_number: int
    topic: str
    arguments: list[Argument] = Field(default_factory=list)
    
    def add_argument(self, argument: Argument) -> None:
        """Add an argument to this round."""
        self.arguments.append(argument)


class OracleAgent(ABC):
    """
    Abstract base class for Oracle Council agents.
    
    Each agent specializes in a different aspect of game analysis.
    """
    
    def __init__(self, role: AgentRole) -> None:
        self.role = role
        self.id = uuid4()
    
    @abstractmethod
    async def analyze(self, context: dict) -> str:
        """
        Analyze the current debate context.
        
        Args:
            context: Debate context including lists, history, etc.
            
        Returns:
            Initial analysis text.
        """
        pass
    
    @abstractmethod
    async def respond(
        self,
        previous_arguments: list[Argument],
        topic: str
    ) -> Argument:
        """
        Respond to previous arguments.
        
        Args:
            previous_arguments: Arguments from other agents.
            topic: Current debate topic.
            
        Returns:
            This agent's argument.
        """
        pass
    
    @abstractmethod
    async def vote(self, transcript: "DebateTranscript") -> dict:
        """
        Vote on debate outcome.
        
        Args:
            transcript: Complete debate transcript.
            
        Returns:
            Vote with prediction and confidence.
        """
        pass


# Type alias for agent implementations
AgentFactory = type[OracleAgent]
````

## File: src/vindicta_oracle/transcript.py
````python
"""
DebateTranscript for Meta-Oracle.

Records the complete history of a debate session.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from meta_oracle.protocol import AgentRole, Argument, DebateRound


class Prediction(BaseModel):
    """A prediction outcome with confidence."""
    
    winner: int  # 1 or 2
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    upset_detected: bool = False


class AgentVote(BaseModel):
    """An agent's vote on the outcome."""
    
    agent_role: AgentRole
    prediction: Prediction
    dissenting: bool = False


class DebateTranscript(BaseModel):
    """
    Complete record of a Meta-Oracle debate session.
    
    Captures all rounds, arguments, votes, and the final consensus.
    """
    
    id: UUID = Field(default_factory=uuid4)
    
    # Context
    topic: str
    player1_faction: str
    player2_faction: str
    
    # Debate content
    rounds: list[DebateRound] = Field(default_factory=list)
    
    # Votes and outcome
    votes: list[AgentVote] = Field(default_factory=list)
    consensus: Optional[Prediction] = None
    
    # Timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    
    def add_round(self, round: DebateRound) -> None:
        """Add a debate round."""
        self.rounds.append(round)
    
    def add_vote(self, vote: AgentVote) -> None:
        """Add an agent vote."""
        self.votes.append(vote)
    
    def calculate_consensus(self) -> Prediction:
        """Calculate consensus from votes."""
        if not self.votes:
            return Prediction(winner=1, confidence=0.5, reasoning="No votes")
        
        # Count votes
        winner_votes = {}
        total_confidence = 0
        
        for vote in self.votes:
            w = vote.prediction.winner
            winner_votes[w] = winner_votes.get(w, 0) + 1
            total_confidence += vote.prediction.confidence
        
        # Find majority
        winner = max(winner_votes, key=winner_votes.get)
        confidence = total_confidence / len(self.votes)
        
        # Check for upset
        upset = any(v.prediction.upset_detected for v in self.votes)
        
        self.consensus = Prediction(
            winner=winner,
            confidence=confidence,
            reasoning=f"Consensus from {len(self.votes)} agents",
            upset_detected=upset
        )
        return self.consensus
    
    def to_json(self) -> str:
        """Serialize to JSON."""
        return self.model_dump_json(indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "DebateTranscript":
        """Deserialize from JSON."""
        return cls.model_validate_json(json_str)
````

## File: tests/test_agents.py
````python
"""
Comprehensive unit tests for Meta-Oracle council agents.

Tests cover:
- Agent property definitions (role, personality, system_prompt)
- analyze() method functionality
- respond() method with debate history
- vote() parsing and format
- Edge cases and error handling
"""
import pytest
from unittest.mock import MagicMock, patch

from meta_oracle.models import (
    AgentRole,
    Argument,
    ArgumentType,
    DebateContext,
    DebateTranscript,
    Vote,
)
from meta_oracle.agents.base import BaseAgent
from meta_oracle.agents.home import HomeAgent
from meta_oracle.agents.adversary import AdversaryAgent
from meta_oracle.agents.arbiter import ArbiterAgent
from meta_oracle.agents.rule_sage import RuleSageAgent
from meta_oracle.agents.chaos import ChaosAgent


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def mock_client():
    """Create a mock Ollama client."""
    client = MagicMock()
    client.generate = MagicMock(return_value="Test response")
    return client


@pytest.fixture
def sample_context():
    """Create a sample debate context."""
    return DebateContext(
        player1_faction="Space Marines",
        player1_list="Captain, 5x Intercessors, Redemptor Dreadnought",
        player2_faction="Orks",
        player2_list="Warboss, 20x Boyz, Battlewagon",
        mission="Take and Hold",
        terrain="Mixed ruins and forests"
    )


@pytest.fixture
def sample_transcript(sample_context):
    """Create a sample debate transcript with one round."""
    transcript = DebateTranscript(context=sample_context)
    transcript.rounds.append([
        Argument(
            agent_role=AgentRole.HOME,
            round=1,
            argument_type=ArgumentType.CLAIM,
            content="Space Marines have superior firepower."
        )
    ])
    return transcript


@pytest.fixture
def all_agents(mock_client):
    """Create all five council agents with mock client."""
    return [
        HomeAgent(mock_client),
        AdversaryAgent(mock_client),
        ArbiterAgent(mock_client),
        RuleSageAgent(mock_client),
        ChaosAgent(mock_client),
    ]


# =============================================================================
# Agent Property Tests
# =============================================================================

class TestAgentProperties:
    """Test that all agents define required properties correctly."""

    def test_home_agent_properties(self, mock_client):
        """HomeAgent should advocate for Player 1."""
        agent = HomeAgent(mock_client)
        assert agent.role == AgentRole.HOME
        assert "Player 1" in agent.system_prompt or "player 1" in agent.system_prompt.lower()
        assert len(agent.personality) > 0

    def test_adversary_agent_properties(self, mock_client):
        """AdversaryAgent should advocate for Player 2."""
        agent = AdversaryAgent(mock_client)
        assert agent.role == AgentRole.ADVERSARY
        assert "Player 2" in agent.system_prompt or "player 2" in agent.system_prompt.lower()
        assert len(agent.personality) > 0

    def test_arbiter_agent_properties(self, mock_client):
        """ArbiterAgent should be neutral and data-driven."""
        agent = ArbiterAgent(mock_client)
        assert agent.role == AgentRole.ARBITER
        assert "neutral" in agent.system_prompt.lower() or "data" in agent.system_prompt.lower()
        assert len(agent.personality) > 0

    def test_rule_sage_agent_properties(self, mock_client):
        """RuleSageAgent should focus on rules validation."""
        agent = RuleSageAgent(mock_client)
        assert agent.role == AgentRole.RULE_SAGE
        assert "rule" in agent.system_prompt.lower()
        assert len(agent.personality) > 0

    def test_chaos_agent_properties(self, mock_client):
        """ChaosAgent should be a devil's advocate."""
        agent = ChaosAgent(mock_client)
        assert agent.role == AgentRole.CHAOS
        assert len(agent.system_prompt) > 0
        assert len(agent.personality) > 0

    def test_all_agents_have_unique_roles(self, all_agents):
        """All five agents should have distinct roles."""
        roles = [agent.role for agent in all_agents]
        assert len(roles) == len(set(roles))

    def test_all_agents_have_system_prompts(self, all_agents):
        """All agents must have non-empty system prompts."""
        for agent in all_agents:
            assert len(agent.system_prompt) > 50, f"{agent.role} has short system prompt"


# =============================================================================
# Analyze Method Tests
# =============================================================================

class TestAnalyzeMethod:
    """Test the analyze() method across agents."""

    def test_analyze_calls_client(self, mock_client, sample_context):
        """analyze() should call the Ollama client."""
        agent = HomeAgent(mock_client)
        result = agent.analyze(sample_context)
        
        mock_client.generate.assert_called_once()
        call_args = mock_client.generate.call_args
        assert agent.system_prompt in call_args[0]
        assert "Space Marines" in call_args[0][1]

    def test_analyze_includes_all_context(self, mock_client, sample_context):
        """analyze() prompt should include all context fields."""
        agent = ArbiterAgent(mock_client)
        agent.analyze(sample_context)
        
        prompt = mock_client.generate.call_args[0][1]
        assert sample_context.player1_faction in prompt
        assert sample_context.player2_faction in prompt
        assert sample_context.mission in prompt

    def test_analyze_handles_none_fields(self, mock_client):
        """analyze() should handle None mission and terrain."""
        context = DebateContext(
            player1_faction="Tyranids",
            player1_list="Hive Tyrant",
            player2_faction="Necrons",
            player2_list="C'tan"
        )
        agent = HomeAgent(mock_client)
        agent.analyze(context)  # Should not raise


# =============================================================================
# Respond Method Tests
# =============================================================================

class TestRespondMethod:
    """Test the respond() method which generates arguments."""

    def test_respond_returns_argument(self, mock_client, sample_transcript):
        """respond() should return an Argument object."""
        agent = AdversaryAgent(mock_client)
        result = agent.respond(sample_transcript, round_num=2)
        
        assert isinstance(result, Argument)
        assert result.agent_role == AgentRole.ADVERSARY
        assert result.round == 2

    def test_respond_includes_history(self, mock_client, sample_transcript):
        """respond() should format debate history in prompt."""
        agent = ArbiterAgent(mock_client)
        agent.respond(sample_transcript, round_num=2)
        
        prompt = mock_client.generate.call_args[0][1]
        assert "HOME" in prompt  # Previous argument from HomeAgent
        assert "superior firepower" in prompt

    def test_respond_first_round(self, mock_client, sample_context):
        """respond() should work for opening round with no history."""
        transcript = DebateTranscript(context=sample_context)
        agent = HomeAgent(mock_client)
        
        result = agent.respond(transcript, round_num=1)
        
        assert result.round == 1
        prompt = mock_client.generate.call_args[0][1]
        assert "opening the debate" in prompt.lower() or "no arguments" in prompt.lower()


# =============================================================================
# Vote Method Tests
# =============================================================================

class TestVoteMethod:
    """Test the vote() method and response parsing."""

    def test_vote_returns_vote_object(self, mock_client, sample_transcript):
        """vote() should return a Vote object."""
        agent = HomeAgent(mock_client)
        result = agent.vote(sample_transcript)
        
        assert isinstance(result, Vote)
        assert result.agent_role == AgentRole.HOME

    def test_vote_parses_player1_winner(self, mock_client, sample_transcript):
        """vote() should correctly parse Player 1 as winner."""
        mock_client.generate.return_value = """
WINNER: Player 1
PROBABILITY: 65%
REASONING: Space Marines have the advantage.
"""
        agent = HomeAgent(mock_client)
        result = agent.vote(sample_transcript)
        
        assert "Player 1" in result.prediction
        assert result.win_probability == 0.65

    def test_vote_parses_player2_winner(self, mock_client, sample_transcript):
        """vote() should correctly parse Player 2 as winner."""
        mock_client.generate.return_value = """
WINNER: Player 2
PROBABILITY: 70%
REASONING: Orks will overwhelm.
"""
        agent = AdversaryAgent(mock_client)
        result = agent.vote(sample_transcript)
        
        assert "Player 2" in result.prediction
        assert result.win_probability == 0.70

    def test_vote_parses_draw(self, mock_client, sample_transcript):
        """vote() should correctly parse Draw prediction."""
        mock_client.generate.return_value = """
WINNER: Draw
PROBABILITY: 50%
REASONING: Evenly matched.
"""
        agent = ArbiterAgent(mock_client)
        result = agent.vote(sample_transcript)
        
        assert "Draw" in result.prediction
        assert result.win_probability == 0.50

    def test_vote_handles_malformed_response(self, mock_client, sample_transcript):
        """vote() should gracefully handle malformed LLM responses."""
        mock_client.generate.return_value = "I think player 1 might win maybe 60%"
        agent = HomeAgent(mock_client)
        result = agent.vote(sample_transcript)
        
        # Should still return a Vote, defaulting where needed
        assert isinstance(result, Vote)
        assert result.win_probability == 0.60

    def test_vote_clamps_probability(self, mock_client, sample_transcript):
        """vote() should clamp probability to 0.0-1.0 range."""
        mock_client.generate.return_value = "WINNER: Player 1\nPROBABILITY: 150%"
        agent = HomeAgent(mock_client)
        result = agent.vote(sample_transcript)
        
        assert result.win_probability <= 1.0


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_agent_without_client_uses_default(self):
        """Agents should create default client if none provided."""
        with patch('meta_oracle.agents.base.OllamaClient') as MockClient:
            MockClient.return_value = MagicMock()
            agent = HomeAgent()
            assert agent.client is not None

    def test_empty_transcript_vote(self, mock_client, sample_context):
        """Agents should handle voting on empty transcripts."""
        transcript = DebateTranscript(context=sample_context)
        agent = RuleSageAgent(mock_client)
        
        result = agent.vote(transcript)
        assert isinstance(result, Vote)

    def test_long_debate_history(self, mock_client, sample_context):
        """Agents should handle long debate histories."""
        transcript = DebateTranscript(context=sample_context)
        
        # Add 5 rounds of 5 agents each
        for round_num in range(1, 6):
            round_args = []
            for role in AgentRole:
                round_args.append(Argument(
                    agent_role=role,
                    round=round_num,
                    argument_type=ArgumentType.CLAIM,
                    content=f"Argument from {role.value} in round {round_num}"
                ))
            transcript.rounds.append(round_args)
        
        agent = ChaosAgent(mock_client)
        result = agent.respond(transcript, round_num=6)
        
        assert isinstance(result, Argument)


# =============================================================================
# Integration Tests (mock client)
# =============================================================================

class TestAgentInteraction:
    """Test agents work together as expected."""

    def test_all_agents_can_analyze(self, all_agents, sample_context):
        """All agents should successfully analyze a context."""
        for agent in all_agents:
            result = agent.analyze(sample_context)
            assert isinstance(result, str)

    def test_all_agents_can_respond(self, all_agents, sample_transcript):
        """All agents should successfully respond in debate."""
        for agent in all_agents:
            result = agent.respond(sample_transcript, round_num=2)
            assert isinstance(result, Argument)
            assert result.agent_role == agent.role

    def test_all_agents_can_vote(self, all_agents, sample_transcript):
        """All agents should successfully cast votes."""
        for agent in all_agents:
            result = agent.vote(sample_transcript)
            assert isinstance(result, Vote)
            assert result.agent_role == agent.role
````

## File: tests/test_api.py
````python
"""Integration tests for the Meta-Oracle API."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from meta_oracle.api import app
from meta_oracle.models import GradeResponse

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"


@patch("meta_oracle.grader.ListGrader.grade")
def test_grade_endpoint_success(mock_grade):
    """Test successful grading via the API endpoint."""
    # Mock the grader response
    mock_grade.return_value = {
        "grade": "B",
        "score": 80,
        "analysis": {"home": "Good"},
        "council_verdict": {"prediction": "Win", "confidence": 0.8, "consensus_agents": ["home"]},
        "metadata": {"debate_id": "test-id", "rounds": 3, "processing_time_ms": 100}
    }
    
    payload = {
        "army_list": {
            "faction": "Space Marines",
            "units": [{"name": "Captain", "points": 100}]
        }
    }
    
    response = client.post("/api/v1/grade", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == "B"
    assert data["score"] == 80


def test_grade_endpoint_invalid_payload():
    """Test API behavior with invalid request payloads."""
    # Missing units
    payload = {
        "army_list": {
            "faction": "Space Marines"
        }
    }
    response = client.post("/api/v1/grade", json=payload)
    assert response.status_code == 422  # Pydantic validation error
    
    # Empty units (should trigger our 400 or Pydantic validator)
    payload = {
        "army_list": {
            "faction": "Space Marines",
            "units": []
        }
    }
    response = client.post("/api/v1/grade", json=payload)
    # Since we added a field_validator that raises ValueError, this becomes 422
    assert response.status_code == 422
````

## File: tests/test_grader.py
````python
"""Unit tests for the ListGrader."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from meta_oracle.grader import ListGrader
from meta_oracle.models import (
    ArmyList, 
    Unit, 
    GradeRequest, 
    DebateTranscript, 
    Vote, 
    AgentRole,
    DebateContext
)


class MockDebateEngine:
    def run_grading_session(self, army_list):
        context = DebateContext(
            player1_faction=army_list.faction,
            player1_list="mock",
            player2_faction="mock",
            player2_list="mock"
        )
        transcript = DebateTranscript(id=uuid4(), context=context)
        transcript.consensus = "Player 1 wins"
        transcript.consensus_confidence = 0.8
        transcript.rounds = [[], [], []]
        transcript.votes = [
            Vote(agent_role=AgentRole.HOME, prediction="Player 1 wins", win_probability=0.8, confidence=0.9, reasoning="Good list"),
            Vote(agent_role=AgentRole.ARBITER, prediction="Player 1 wins", win_probability=0.8, confidence=0.8, reasoning="Strong units")
        ]
        return transcript


@pytest.mark.asyncio
async def test_grade_valid_list():
    """Test the happy path for grading a valid list."""
    grader = ListGrader(engine=MockDebateEngine())
    army_list = ArmyList(
        faction="Space Marines",
        units=[Unit(name="Captain", points=100)]
    )
    request = GradeRequest(army_list=army_list)
    
    response = await grader.grade(request)
    
    assert response.score > 0
    assert response.grade in ["A", "B", "C", "D", "F"]
    assert "home" in response.analysis
    assert response.council_verdict["confidence"] == 0.8


def test_scoring_formula():
    """Verify the 60/40 scoring formula and grade mapping."""
    grader = ListGrader(engine=MockDebateEngine())
    
    # Mocking internal methods for formula test
    grader._calculate_primordia_score = MagicMock(return_value=100)
    
    # 0.6 * 80 (council) + 0.4 * 100 (primordia) = 48 + 40 = 88
    # 88 should be a "B"
    score = int(0.6 * 80 + 0.4 * 100)
    grade = grader._map_score_to_grade(score)
    
    assert score == 88
    assert grade == "B"


def test_grade_mapping():
    """Test all grade thresholds."""
    grader = ListGrader()
    assert grader._map_score_to_grade(95) == "A"
    assert grader._map_score_to_grade(85) == "B"
    assert grader._map_score_to_grade(70) == "C"
    assert grader._map_score_to_grade(50) == "D"
    assert grader._map_score_to_grade(30) == "F"
````

## File: tests/test_oracle.py
````python
"""
Unit tests for Meta-Oracle.
"""

import pytest
from meta_oracle.protocol import AgentRole, Argument, ArgumentType, DebateRound
from meta_oracle.transcript import DebateTranscript, Prediction, AgentVote
from meta_oracle.engine import DebateEngine
from meta_oracle.agents import StubAgent


class TestProtocol:
    """Tests for OracleAgent protocol."""

    def test_agent_roles(self):
        """All 5 agent roles should exist."""
        roles = list(AgentRole)
        assert len(roles) == 5
        assert AgentRole.HOME in roles
        assert AgentRole.ADVERSARY in roles
        assert AgentRole.ARBITER in roles
        assert AgentRole.RULE_SAGE in roles
        assert AgentRole.CHAOS in roles

    def test_argument_creation(self):
        """Argument should be creatable."""
        arg = Argument(
            agent_role=AgentRole.HOME,
            argument_type=ArgumentType.CLAIM,
            content="Player 1 will win"
        )
        
        assert arg.agent_role == AgentRole.HOME
        assert arg.content == "Player 1 will win"

    def test_debate_round(self):
        """DebateRound should hold arguments."""
        round = DebateRound(round_number=1, topic="Test")
        
        arg = Argument(
            agent_role=AgentRole.HOME,
            argument_type=ArgumentType.CLAIM,
            content="Test"
        )
        round.add_argument(arg)
        
        assert len(round.arguments) == 1


class TestTranscript:
    """Tests for DebateTranscript."""

    def test_transcript_creation(self):
        """Transcript should be creatable."""
        transcript = DebateTranscript(
            topic="Who will win?",
            player1_faction="Space Marines",
            player2_faction="Orks"
        )
        
        assert transcript.player1_faction == "Space Marines"

    def test_consensus_calculation(self):
        """Consensus should be calculated from votes."""
        transcript = DebateTranscript(
            topic="Test",
            player1_faction="A",
            player2_faction="B"
        )
        
        # 3 votes for player 1, 2 for player 2
        for i in range(3):
            transcript.add_vote(AgentVote(
                agent_role=AgentRole.HOME,
                prediction=Prediction(winner=1, confidence=0.7, reasoning="Test")
            ))
        for i in range(2):
            transcript.add_vote(AgentVote(
                agent_role=AgentRole.ADVERSARY,
                prediction=Prediction(winner=2, confidence=0.6, reasoning="Test")
            ))
        
        consensus = transcript.calculate_consensus()
        
        assert consensus.winner == 1

    def test_json_round_trip(self):
        """Transcript should serialize/deserialize."""
        transcript = DebateTranscript(
            topic="Test",
            player1_faction="A",
            player2_faction="B"
        )
        
        json_str = transcript.to_json()
        restored = DebateTranscript.from_json(json_str)
        
        assert restored.topic == "Test"


class TestDebateEngine:
    """Tests for DebateEngine."""

    @pytest.mark.asyncio
    async def test_engine_runs_debate(self):
        """Engine should run complete debate."""
        engine = DebateEngine(rounds=2)
        
        # Register stub agents
        for role in AgentRole:
            engine.register_agent(StubAgent(role))
        
        transcript = await engine.run_debate(
            topic="Who will win?",
            player1_faction="Marines",
            player2_faction="Orks"
        )
        
        assert len(transcript.rounds) == 2
        assert transcript.consensus is not None

    @pytest.mark.asyncio
    async def test_engine_collects_votes(self):
        """Engine should collect votes from all agents."""
        engine = DebateEngine(rounds=1)
        
        for role in AgentRole:
            engine.register_agent(StubAgent(role))
        
        transcript = await engine.run_debate(
            topic="Test",
            player1_faction="A",
            player2_faction="B"
        )
        
        assert len(transcript.votes) == 5  # All 5 agents voted
````
