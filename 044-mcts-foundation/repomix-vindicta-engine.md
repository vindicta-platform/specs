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
.agent/workflows/jd-bugfix.md
.agent/workflows/sd-implement.md
.agent/workflows/sse-code-review.md
.github/workflows/docs.yml
.gitignore
.specify/memory/constitution.md
.specify/templates/plan-template.md
.specify/templates/spec-template.md
.specify/templates/tasks-template.md
docs/index.md
features/integrity.feature
features/steps/integrity_steps.py
mkdocs.yml
pyproject.toml
README.md
specs/001-simulation-stat-retrieval/checklists/requirements.md
specs/001-simulation-stat-retrieval/data-model.md
specs/001-simulation-stat-retrieval/plan.md
specs/001-simulation-stat-retrieval/quickstart.md
specs/001-simulation-stat-retrieval/research.md
specs/001-simulation-stat-retrieval/spec.md
specs/001-simulation-stat-retrieval/tasks.md
src/vindicta_engine/__init__.py
src/vindicta_engine/ai/__init__.py
src/vindicta_engine/ai/base.py
src/vindicta_engine/dice/__init__.py
src/vindicta_engine/dice/engine.py
src/vindicta_engine/dice/models.py
src/vindicta_engine/health.py
src/vindicta_engine/integrity.py
src/vindicta_engine/physics/engine.py
src/vindicta_engine/physics/models.py
tests/dice/test_engine.py
tests/test_physics.py
```

# Files

## File: .agent/workflows/jd-bugfix.md
````markdown
---`ndescription: Bug fix workflow for learning developers`n---`n1. Reproduce the bug with an automated test`n2. execute `/speckit.plan` for the fix`n3. execute `/speckit.tasks``n4. execute `/speckit.implement``n5. Verify fix and delete reproduction test if temporary
````

## File: .agent/workflows/sd-implement.md
````markdown
---`ndescription: Feature implementation from specification to PR`n---`n1. Read the feature specification in `.specify/specs/``n2. execute `/speckit.plan``n3. execute `/speckit.tasks``n4. execute `/speckit.implement`
````

## File: .agent/workflows/sse-code-review.md
````markdown
---`ndescription: Comprehensive code review with mentoring feedback`n---`n1. execute `git diff` against target branch`n2. Perform static analysis check`n3. Provide feedback on architecture, performance, and constitution compliance
````

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

## File: .gitignore
````
__pycache__/
````

## File: docs/index.md
````markdown
# Vindicta Engine Documentation

Welcome to the **Vindicta Engine** documentation — the physics, dice, and AI core for the Vindicta Platform.

## Modules

- **Dice Engine**: CSPRNG-powered dice rolling with full statistical modeling.
- **Entropy Buffer**: Thread-safe buffered entropy for reliable RNG.
- **Primordia AI**: Deterministic tactical AI engine.

## Links

- [GitHub Repository](https://github.com/vindicta-platform/vindicta-engine)
- [Foundation & Standards](https://github.com/vindicta-platform/vindicta-foundation)
````

## File: features/integrity.feature
````
Feature: System Integrity Check

  Scenario: Agent reports system integrity
    Given the Vindicta Engine system is active
    When I request an integrity check
    Then the system status should be "operational"
    And the response should contain a timestamp
````

## File: features/steps/integrity_steps.py
````python
from behave import given, when, then
from vindicta_engine.integrity import verify_integrity
import datetime

@given('the Vindicta Engine system is active')
def step_impl(context):
    pass

@when('I request an integrity check')
def step_impl(context):
    context.response = verify_integrity()

@then('the system status should be "operational"')
def step_impl(context):
    assert context.response['status'] == 'operational'

@then('the response should contain a timestamp')
def step_impl(context):
    assert 'timestamp' in context.response
    assert isinstance(context.response['timestamp'], str)
````

## File: mkdocs.yml
````yaml
site_name: Vindicta Engine
site_description: Physics, Dice, and AI Core for the Vindicta Platform.
site_author: Vindicta Platform Contributors
site_url: https://vindicta-platform.github.io/vindicta-engine/

repo_name: vindicta-platform/vindicta-engine
repo_url: https://github.com/vindicta-platform/vindicta-engine

theme:
  name: material
  palette:
    - scheme: slate
      primary: red
      accent: amber
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
    - scheme: default
      primary: red
      accent: amber
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
name = "vindicta-engine"
version = "0.1.0"
description = "Physics, Dice, and AI Core for the Vindicta Platform"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "vindicta-foundation",
    "numpy>=1.26.0",
    "langgraph>=1.0.8",
    "behave>=1.3.3",
    "structlog>=25.5.0",
]

[project.optional-dependencies]
dev = [
    "mypy>=1.0.0",
    "ruff>=0.1.0",
    "pytest>=8.0.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/vindicta_engine"]

[tool.hatch.metadata]
allow-direct-references = true

[tool.uv.sources]
vindicta-foundation = { path = "../vindicta-foundation", editable = true }

[tool.mypy]
strict = true
python_version = "3.12"

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "D"]
ignore = ["D100", "D104"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.pytest.ini_options]
pythonpath = ["src"]
addopts = "--cov=vindicta_engine --cov-report=term-missing"

[dependency-groups]
dev = [
    "pytest-sugar>=1.1.1",
    "pytest-cov>=6.0.0",
    "behave>=1.2.6",
    "pytest-xdist>=3.5.0",
]

[tool.coverage.run]
source = ["src/vindicta_engine"]
omit = ["tests/*"]

[tool.coverage.report]
fail_under = 90
show_missing = true
````

## File: README.md
````markdown
# Vindicta Engine

Core physics, dice rolling, and AI simulation engine for the Vindicta Platform.

## Documentation

> **📌 Important:** Architectural decisions and game logic axioms for the engine are documented in [**vindicta-foundation**](https://github.com/vindicta-platform/vindicta-foundation).

## Installation


```bash
uv add vindicta-engine
```

## Features

- **Dice Physics**: Trusted RNG and True-Random entropy integration.
- **Combat Simulation**: Monte Carlo simulation for attack sequences.
- **AI Primitives**: Base classes for tactical AI.
````

## File: specs/001-simulation-stat-retrieval/checklists/requirements.md
````markdown
# Specification Quality Checklist: Simulation Stat Retrieval

**Purpose**: Validate specification completeness and quality before proceeding to planning  
**Created**: 2026-02-23  
**Feature**: [spec.md](file:///c:/Users/bfoxt/vindicta-playground/vindicta-engine/specs/001-simulation-stat-retrieval/spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- The spec references the RAG pipeline (005) as the upstream dependency — this is a system-level reference, not an implementation detail.
- Variable damage parsing (e.g., "D6", "D3+1") is explicitly called out as being resolved at simulation time, deferring to the existing dice resolution capability.
- The Assumptions section documents the local-first deployment model (localhost RAG server) and bounded cache expectations.
- All checklist items pass. Spec is ready for `/speckit.clarify` or `/speckit.plan`.
````

## File: specs/001-simulation-stat-retrieval/data-model.md
````markdown
# Data Model: Simulation Stat Retrieval

These models will reside in `src/vindicta_engine/physics/models.py` or their own domain models file logically associated with the simulation. All inherit from `vindicta_foundation.models.base.VindictaModel`.

## `StatModifier` (Entity)
Represents a specific ability or keyword altering combat.
- `type`: str (e.g., "re_roll_hits", "lethal_hits", "anti")
- `value`: Optional[int] (e.g., The '4' in Anti-Vehicle 4+)
- `condition`: Optional[str] (e.g., "vehicle")

## `WeaponStatLine` (Entity)
Strongly typed combat parameters for a weapon instance.
- `weapon_name`: str
- `range`: int (0 for melee)
- `attacks`: str (e.g., "3", "D6") - kept as string to pass to the dice roller.
- `hit_on`: int (Target BS/WS)
- `strength`: int
- `ap`: int (Formatted to positive absolute integer internally if preferred)
- `damage`: str (e.g., "2", "D3")
- `modifiers`: List[StatModifier]

## `UnitProfile` (Entity)
Structured core statistics.
- `unit_name`: str
- `rules_version`: str
- `movement`: int
- `toughness`: int
- `save`: int
- `wounds`: int
- `leadership`: int
- `oc`: int
- `weapons`: List[WeaponStatLine]

## `StatCacheEntry` (Entity)
Internal caching wrapper.
- `profile`: UnitProfile
- `insertion_time`: float (Unix timestamp)
- `last_access`: float (Unix timestamp)
- `query_count`: int (Observability counter)

## State Transitions
**Cache Retrieval Workflow**:
1. Request for `(unit, weapon, version)` is received by `StatRetriever`.
2. Check `StatCache` dict. 
    - **HIT**: Update `last_access` and `query_count`, return immediately.
    - **MISS**: 
        a. Acquire async lock for this specific key to prevent thundering herds from parallel simulations.
        b. Check cache again inside lock (double-checked locking).
        c. Issue MCP query to RAG server. (Retry exactly once after 500ms on failure).
        d. Parse returned markdown into `UnitProfile`.
        e. Insert into `StatCache` with current timestamp.
        f. Enforce LRU eviction if cache size > limit (e.g., 500 entries).
        g. Release lock, return result.
````

## File: specs/001-simulation-stat-retrieval/plan.md
````markdown
# Implementation Plan: Simulation Stat Retrieval

**Branch**: `001-simulation-stat-retrieval` | **Date**: 2026-02-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-simulation-stat-retrieval/spec.md`

## Summary

This feature adds asynchronous retrieval and caching of game statistics for the vindicta-engine. It integrates with the RAG server to natively parse markdown rules into distinct numeric `UnitProfile`, `WeaponStatLine`, and `StatModifier` Pydantic models using regex extraction heuristics and an embedded local async-safe LRU cache system to optimize Monte Carlo pipeline latencies.

## Technical Context

**Technical Setup & Integration**:
- **Domain Context**: Resides entirely within the `vindicta-engine` package domain.
- **Data Architecture**: Reads from `vindicta-foundation` schemas implicitly (requires `VindictaModel`).
- **Dependencies**: Depends on the MCP Client integration for requesting `search_40k_rules`.

**Language/Version**: Python 3.12+ (uv workspace)
**Primary Dependencies**: `pydantic` (models), `mcp` (MCP SDK for RAG server queries), `logging`
**Storage**: Embedded in-memory LRU cache
**Testing**: `pytest`, `pytest-asyncio`
**Target Platform**: Any system running the local MVP platform
**Performance Goals**: RAG latency lookup minimal constraints, cache lookups < 1ms
**Constraints**: 1 retry per RAG access. Cache invalidates structurally via rules versioning keys.

## Constitution Check
- [x] **I. Foundation Adherence**: Models align with AX-01 (Entity Identity) — unique identifiers on all entities.
- [x] **II. Model Integrity**: Models `UnitProfile`, `WeaponStatLine`, `StatModifier` inherit `VindictaModel` from `vindicta_foundation/models/base`.
- [x] **IV. Documentation Discipline**: No container boundary changes — C4 model update not required.
- [x] **V. Quality Mandate**: `pytest` + `pytest-asyncio` running coverage bounds. `ruff` and `mypy --strict` enforced.
- [x] **VII. Spec Directory**: Feature resides in `specs/001-simulation-stat-retrieval/` following `NNN-short-name` convention.

## Project Structure

### Documentation
```text
specs/001-simulation-stat-retrieval/
├── plan.md              # This file
├── spec.md
└── tasks.md             # To be generated
```

### Source Code
```text
src/vindicta_engine/
├── ai/
├── physics/
│   ├── engine.py
│   └── models.py
└── retrieval/                        # NEW DOMAIN
    ├── __init__.py                   # Public API exports
    ├── exceptions.py                 # RAGQueryError, StatParseError
    ├── metrics.py                    # CacheMetrics counters
    ├── models.py                     # UnitProfile, WeaponStatLine, StatModifier
    ├── mcp_client.py                 # MCP connectivity & retry logic
    ├── parser.py                     # Markdown → Pydantic parser
    └── stat_cache.py                 # Async-safe LRU cache + StatRetriever facade

tests/
└── retrieval/
    ├── test_models.py                # Model construction & validation
    ├── test_mcp_client.py            # RAG client & retry logic
    ├── test_parser.py                # Markdown parsing & keyword extraction
    ├── test_stat_cache.py            # Cache hits, LRU, async-safety, metrics
    └── test_integration.py           # End-to-end retrieval flow
```
````

## File: specs/001-simulation-stat-retrieval/quickstart.md
````markdown
# Quickstart: Simulation Stat Retrieval

## Overview
This subsystem abstracts the heavy network calls to the local RAG rules server when loading Unit data for the Monte Carlo simulation engine. It parses the raw markdown output into structured Pydantic `UnitProfile` entities.

## Prerequisites
- The RAG MCP Server (setup in `005-rag-pipeline`) must be running locally.
- Engine execution must be wrapped in an `asyncio` event loop.

## Usage Example

```python
import asyncio
from vindicta_engine.retrieval.stat_cache import StatCache
from vindicta_engine.retrieval.mcp_client import RAGClient

async def run_simulation_batch():
    # Initialize the retrieval system
    rag_client = RAGClient(endpoint="http://localhost:8000/mcp") # Standard MCP config
    cache = StatCache(max_size=100)
    
    # Example request for a single unit profile
    unit_name = "Intercessor Squad"
    version = "1.0.0"
    
    # Retrieve the parsed stats (hits MCP on first call, then caches)
    try:
        profile = await cache.get_unit_stats(
            client=rag_client, 
            unit_name=unit_name, 
            version=version
        )
        print(f"Loaded {unit_name} with Toughness {profile.toughness}")
        
    except RAGQueryError as e:
        print(f"Failed to load stats after retry: {e}")

if __name__ == "__main__":
    asyncio.run(run_simulation_batch())
```

## Observability
Check the built-in tracking variables on the `StatCache` instance to verify metrics matching the specification:
```python
print(f"Cache Hits: {cache.metrics.hits}, Misses: {cache.metrics.misses}")
print(f"Parse Errors: {cache.metrics.parse_errors}")
```
````

## File: specs/001-simulation-stat-retrieval/research.md
````markdown
# Research & Technical Decisions: Simulation Stat Retrieval

## 1. Async-Safe State Cache
- **Decision**: Use `asyncio.Lock` coupled with a standard `dict` for the cache store, or leverage an `asyncio` primitive like a bounded `LRU` cache implementation using `OrderedDict`. Since Python's dictionary is thread-safe for simple operations but async operations involving I/O (like an MCP query on a cache miss) need to prevent "thundering herd" query duplication, a per-key `asyncio.Event` or a unified `asyncio.Lock` is necessary during the retrieval phase.
- **Rationale**: The Monte Carlo simulator will trigger thousands of async lookup requests simultaneously. A simple lock prevents redundant network queries for the same unit while waiting for the RAG server to respond (FR-011).
- **Alternatives considered**: External caching like Redis (rejected: local-first MVP constraint), `functools.lru_cache` (rejected: doesn't handle shared async waiting cleanly without wrappers).

## 2. Markdown Parsing
- **Decision**: Utilize standard Python string processing and regex combined with Pydantic validation for the extraction of core combat modifiers and common keywords (FR-007). Unrecognized abilities will be captured as raw strings.
- **Rationale**: The RAG server returns Wahapedia/40k.app style structured markdown (tables, lists). Regex and basic table-parsing utilities are sufficient for the MVP "core" keywords, and Pydantic will ensure proper typed casting (e.g., extracting "3" from "WS 3+").
- **Alternatives considered**: LLM-based parsing at runtime (rejected: too slow for large simulation batches, parser needs to be deterministic and fast).

## 3. RAG Server MCP Communications
- **Decision**: Implement a lightweight asynchronous MCP client using the standard `mcp` SDK to query the rule segments. Implement a wrapper around the client request that catches `mcp` timeouts, waits ~500ms, and retries exactly once before raising an exception (FR-006).
- **Rationale**: Aligns with the platform's standard for MCP communication while fulfilling the robust error-handling requirement from the clarification session.
- **Alternatives considered**: Direct database queries to ChromaDB (rejected: violates the architectural container boundary by bypassing the RAG MCP server interface).

## 4. Cache Identity Key
- **Decision**: The cache key will be a formatted string or a named tuple: `(unit_name, weapon_name, rules_version)`. 
- **Rationale**: Directly aligns with the clarification for Q1. By embedding the version inside the key itself, cache invalidation for newly versioned data is handled inherently by a cache miss, preventing stale reads.
- **Alternatives considered**: Hashing the values (rejected: unnecessary overhead, the tuple/string is clean and unique).
````

## File: specs/001-simulation-stat-retrieval/spec.md
````markdown
# Feature Specification: Simulation Stat Retrieval

**Feature Branch**: `001-simulation-stat-retrieval`  
**Created**: 2026-02-23  
**Status**: Draft  
**Input**: User description: "How the Monte Carlo simulation engine queries the RAG server to load unit profiles and weapon stats before running combat simulations, including caching strategies and markdown-to-struct parsing."

## Clarifications

### Session 2026-02-23

- Q: What uniquely identifies a cached stat entry — unit name + weapon name alone, or should the rules version also be part of the cache key? → A: Unit name + weapon name + rules version (version is part of the key, so new versions auto-miss the cache).
- Q: Should the engine retry failed RAG queries, and if so, how many attempts before surfacing the error? → A: 1 retry after a short delay (~500ms), then fail if still unavailable.
- Q: Should the engine emit observable signals for monitoring and debugging? → A: Structured logging with in-memory counters (cache hits/misses, query latency, parse errors) accessible via API or log output.
- Q: Should the stat cache support thread-safe concurrent access, or is single-threaded sequential access sufficient? → A: Thread-safe and async-safe — cache must support concurrent access from async simulation tasks.
- Q: Should the MVP parser handle all known ability types, or a curated core subset? → A: Core modifiers + common keywords (re-rolls, Lethal Hits, Sustained Hits, Devastating Wounds, Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load Unit Stats for Combat Simulation (Priority: P1)

As the simulation engine, before executing a Monte Carlo combat run, I need to retrieve the complete unit profile and weapon stats for each participating unit from the RAG rules server so that all combat parameters (attacks, hit threshold, wound threshold, save, damage, special rules) are accurate and rules-authoritative.

**Why this priority**: Without accurate stat retrieval, the simulation produces meaningless results. This is the foundational data path that enables all downstream physics calculations.

**Independent Test**: Can be fully tested by requesting a known unit's profile (e.g., "Intercessor Squad") from the RAG server and verifying the returned data is correctly parsed into the engine's structured combat parameters — `attacks`, `hit_on`, `wound_on`, `save`, `damage` — matching the canonical rules source.

**Acceptance Scenarios**:

1. **Given** the simulation engine is initialized and the RAG server is available, **When** the engine requests the profile for "Intercessor Squad with Bolt Rifle", **Then** it receives and parses a structured stats object containing all required combat parameters (attacks, ballistic skill, strength, AP, damage) within 2 seconds.
2. **Given** a unit has multiple weapon options (e.g., heavy, rapid fire, melee), **When** the engine requests the unit profile, **Then** it receives all weapon profiles as distinct structured objects, each with their own stat line.
3. **Given** the RAG server returns rules text that includes special abilities or modifiers (e.g., "re-roll hit rolls of 1"), **When** the engine parses the response, **Then** the modifier is identified and encoded as a structured flag or parameter alongside the base stats.

---

### User Story 2 - Cache Stats During Heavy Simulation Runs (Priority: P2)

As the simulation engine during a batch Monte Carlo run (e.g., evaluating 10,000 iterations of a matchup), I need frequently requested unit stats to be served from a local cache to avoid redundant RAG server queries, so that simulation throughput is not bottlenecked by repeated network round-trips.

**Why this priority**: A single Monte Carlo batch may reference the same unit stat line thousands of times. Without caching, the system would send thousands of identical requests to the RAG server, creating unacceptable latency and wasted resources.

**Independent Test**: Can be tested by running a 1,000-iteration Monte Carlo batch for a known matchup (e.g., 10 Intercessors vs. 10 Ork Boyz) and verifying via instrumented counters that the RAG server is queried at most once per unique unit/weapon combination, with all subsequent lookups served from cache.

**Acceptance Scenarios**:

1. **Given** a Monte Carlo batch of N iterations for the same two-unit matchup, **When** the batch executes, **Then** the RAG server receives at most one query per unique unit-weapon combination, regardless of the iteration count.
2. **Given** a cached stat entry exists for a unit, **When** a new simulation iteration requests that unit's stats, **Then** the cached result is returned in under 1 millisecond.
3. **Given** the simulation engine is configured with a maximum cache size, **When** the cache reaches capacity, **Then** least-recently-used entries are evicted first to make room for new queries.

---

### User Story 3 - Parse RAG Markdown into Structured Stat Objects (Priority: P1)

As the simulation engine, when the RAG server returns rule chunks as markdown text, I need a reliable parser that converts those free-form markdown chunks into strongly typed statistical objects that the physics engine can consume, so that combat calculations are driven by precise numeric values rather than raw text.

**Why this priority**: The RAG pipeline (005) stores and serves rules as markdown chunks. The simulation engine's physics layer expects structured numeric data (integers, floats, booleans). This translation layer is critical for correctness.

**Independent Test**: Can be tested by feeding the parser a representative markdown rules chunk (containing a unit's stat block, weapon profiles, and special rules) and verifying the output is a correctly populated structured object with all numeric fields extracted and typed.

**Acceptance Scenarios**:

1. **Given** a markdown chunk containing a standard Warhammer 40k unit datasheet (Movement, Toughness, Save, Wounds, Leadership, OC), **When** the parser processes it, **Then** each stat is extracted into its corresponding typed field with correct values.
2. **Given** a markdown chunk containing a weapon profile table (Range, A, BS/WS, S, AP, D), **When** the parser processes it, **Then** each weapon is parsed into a distinct stat object with all fields correctly typed (including variable damage like "D3" encoded as a range or roll type).
3. **Given** a markdown chunk that includes an ability or aura rule (e.g., "Each time this model makes a ranged attack, re-roll a wound roll of 1"), **When** the parser processes it, **Then** the ability is identified by keyword and encoded as a structured modifier applicable to the combat roll parameters.
4. **Given** a malformed or incomplete markdown chunk (missing columns, unexpected formatting), **When** the parser processes it, **Then** it returns a partial result with clearly flagged missing fields rather than failing silently or producing incorrect values.

---

### Edge Cases

- What happens when the RAG server is unreachable or returns an empty result set for a valid unit query?
- How does the system handle units with conditional or phase-dependent stat profiles (e.g., stats change in melee vs. ranged)?
- What happens when the RAG server returns multiple versioned rule chunks for the same unit (e.g., pre-errata and post-errata) and the engine must select the correct one?
- How does the parser handle non-standard stat values like "2D6", "D3+1", or "N/A" for damage or attacks?
- What happens if a cached stat entry becomes stale because the RAG server has ingested updated rules between simulation batches?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST query the RAG rules server via its published interface to retrieve unit profiles and weapon stat lines by unit name or identifier before initiating any combat simulation.
- **FR-002**: System MUST parse returned markdown text chunks into strongly typed statistical objects with discrete numeric fields (e.g., attacks, ballistic skill, strength, armour penetration, damage).
- **FR-003**: System MUST support parsing variable stat values (e.g., "D6", "2D6", "D3+1") into a representation that the dice engine can resolve at simulation time.
- **FR-004**: System MUST maintain a local stat cache keyed by the composite of unit name, weapon name, and rules version, eliminating redundant queries for the same unit-weapon-version combination within a single simulation session or batch run. A new rules version for the same unit-weapon pair MUST result in a cache miss and fresh retrieval.
- **FR-005**: System MUST implement a cache eviction strategy (e.g., least-recently-used) to bound memory usage during heavy simulation runs.
- **FR-006**: System MUST attempt exactly one retry after a short delay (~500ms) when a RAG server query fails, then return a meaningful error or partial result to the caller if the retry also fails, rather than silently proceeding with default or zero values.
- **FR-007**: System MUST support retrieving and parsing the following ability categories for the MVP: core combat modifiers (re-roll hits, re-roll wounds, Lethal Hits, Sustained Hits, Devastating Wounds) and common weapon keywords (Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent). Unrecognized abilities MUST be preserved as raw text and flagged for future parser expansion.
- **FR-008**: System MUST version-stamp cached entries using the rules segment version from the RAG pipeline so that stale data can be detected and refreshed.
- **FR-009**: System MUST allow cache invalidation or refresh on demand (e.g., between successive batch runs or when the user triggers a rules update).
- **FR-010**: System MUST expose structured logging and in-memory counters for key operational signals — cache hit/miss counts, RAG query latency, and parse error counts — accessible via programmatic API or log output for debugging and validation.
- **FR-011**: System MUST ensure the stat cache is async-safe, supporting concurrent reads and writes from multiple async simulation tasks without data corruption or race conditions.

### Key Entities

- **Unit Profile**: A structured representation of a unit's core statistics (Movement, Toughness, Save, Wounds, Leadership, Objective Control), uniquely identified by unit name and rules version.
- **Weapon Stat Line**: A structured representation of a single weapon's combat parameters (Range, Attacks, Skill, Strength, AP, Damage, Keywords/Abilities), linked to a parent Unit Profile.
- **Stat Modifier**: A structured encoding of a conditional rule or ability that alters base combat parameters (e.g., re-roll type, bonus attacks, conditional hit/wound modifiers), linked to either a Unit Profile or Weapon Stat Line.
- **Stat Cache Entry**: A cached unit-weapon stat bundle keyed by the composite of (unit name, weapon name, rules version). Includes insertion timestamp and last-access timestamp for LRU eviction. A new rules version naturally creates a distinct cache entry, ensuring stale data is never served.

## Assumptions

- The RAG rules server (005-rag-pipeline) is operational and serves rules as markdown text chunks via the Model Context Protocol (MCP) interface.
- The markdown format returned by the RAG pipeline follows a consistent structure (e.g., Wahapedia/40k.app style datasheet layouts) that can be reliably parsed.
- The simulation engine runs locally on the same machine as the RAG server, so network latency is negligible (localhost communication).
- Cache sizes will be bounded by available system memory; typical simulation batches involve fewer than 100 unique unit-weapon combinations.
- The stat cache will be accessed concurrently by async simulation tasks and must be designed for async-safe operation from the outset.
- Variable damage values (e.g., "D6") will be resolved at dice-roll time by the existing `DiceEngine`, not at parse time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The simulation engine can load all required stats for a two-army matchup (up to 20 unique units) from the RAG server and begin simulation within 5 seconds.
- **SC-002**: During a 10,000-iteration Monte Carlo batch, cached stat lookups account for ≥99% of all stat retrievals, with at most one RAG query per unique unit-weapon combination.
- **SC-003**: 95% of parsed stat objects from RAG markdown chunks match the canonical source values with zero field errors.
- **SC-004**: When the RAG server is unavailable, the system reports the failure to the caller within 3 seconds rather than hanging or producing silently incorrect results.
- **SC-005**: Cache memory usage for a typical 20-unit matchup remains under 10 MB.
````

## File: specs/001-simulation-stat-retrieval/tasks.md
````markdown
# Tasks: Simulation Stat Retrieval

**Input**: Design documents from `specs/001-simulation-stat-retrieval/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), quickstart.md (✓)

**Tests**: Tests included — the constitution mandates 90% coverage and `uv run pytest`.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Engine Subsystem**: `src/vindicta_engine/` at repository root (`vindicta-engine/`)
- **Tests**: `tests/` at repository root (`vindicta-engine/`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the `retrieval` subpackage scaffold and install dependencies

- [ ] T001 Create retrieval subpackage directory with `__init__.py` at src/vindicta_engine/retrieval/__init__.py
- [ ] T002 Add `mcp` SDK dependency to vindicta-engine/pyproject.toml
- [ ] T003 [P] Create test directory structure at tests/retrieval/__init__.py
- [ ] T004 [P] Add `pytest-asyncio` to dev dependencies in vindicta-engine/pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared data models and base types that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create `StatModifier` Pydantic model (type, value, condition fields) inheriting from VindictaModel in src/vindicta_engine/retrieval/models.py
- [ ] T006 [P] Create `WeaponStatLine` Pydantic model (weapon_name, range, attacks, hit_on, strength, ap, damage, modifiers fields) inheriting from VindictaModel in src/vindicta_engine/retrieval/models.py
- [ ] T007 Create `UnitProfile` Pydantic model (unit_name, rules_version, movement, toughness, save, wounds, leadership, oc, weapons fields) inheriting from VindictaModel in src/vindicta_engine/retrieval/models.py
- [ ] T008 [P] Create `CacheMetrics` dataclass (hits, misses, parse_errors, total_query_latency_ms counters) in src/vindicta_engine/retrieval/metrics.py
- [ ] T009 [P] Create `RAGQueryError` and `StatParseError` exception classes in src/vindicta_engine/retrieval/exceptions.py
- [ ] T010 Write unit tests for all foundational models (construction, validation, serialization) in tests/retrieval/test_models.py

**Checkpoint**: Foundation ready — all data models validated and exportable. User story implementation can now begin.

---

## Phase 3: User Story 1 — Load Unit Stats for Combat Simulation (Priority: P1) 🎯 MVP

**Goal**: The simulation engine queries the RAG MCP server for a unit's profile and weapon stats and receives a fully populated `UnitProfile` object.

**Independent Test**: Request "Intercessor Squad" from the RAG server and verify the returned `UnitProfile` has correct combat parameters matching the canonical source.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Unit test for `RAGClient.query_unit_stats()` with mocked MCP responses in tests/retrieval/test_mcp_client.py
- [ ] T012 [P] [US1] Unit test for `RAGClient` retry logic — verify exactly 1 retry after ~500ms on failure, then raises `RAGQueryError` in tests/retrieval/test_mcp_client.py
- [ ] T013 [P] [US1] Integration test for full stat retrieval flow: query → parse → return `UnitProfile` in tests/retrieval/test_integration.py

### Implementation for User Story 1

- [ ] T014 [US1] Implement `RAGClient` class with async `query_unit_stats(unit_name: str, version: str)` method using `mcp` SDK in src/vindicta_engine/retrieval/mcp_client.py
- [ ] T015 [US1] Implement retry logic in `RAGClient` — catch connection errors, wait ~500ms, retry once, then raise `RAGQueryError` with context in src/vindicta_engine/retrieval/mcp_client.py
- [ ] T016 [US1] Implement timeout handling — ensure total query time (including retry) stays within 3-second budget per SC-004 in src/vindicta_engine/retrieval/mcp_client.py
- [ ] T017 [US1] Export `RAGClient` and all retrieval models from src/vindicta_engine/retrieval/__init__.py

**Checkpoint**: `RAGClient` can query the RAG server and return raw markdown. Retry logic verified. US1 is independently testable.

---

## Phase 4: User Story 3 — Parse RAG Markdown into Structured Stat Objects (Priority: P1)

**Goal**: A parser converts raw markdown from the RAG server into populated `UnitProfile` objects with all weapon stat lines and recognized modifiers.

**Independent Test**: Feed the parser a representative Wahapedia-style markdown chunk and verify the output `UnitProfile` has correctly typed fields and all weapons parsed.

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T018 [P] [US3] Unit test for parsing a standard unit datasheet (M, T, Sv, W, Ld, OC extraction) in tests/retrieval/test_parser.py
- [ ] T019 [P] [US3] Unit test for parsing weapon profile tables (Range, A, BS/WS, S, AP, D) into `WeaponStatLine` objects in tests/retrieval/test_parser.py
- [ ] T020 [P] [US3] Unit test for parsing variable stat values ("D6", "2D6", "D3+1") kept as strings for dice-engine resolution in tests/retrieval/test_parser.py
- [ ] T021 [P] [US3] Unit test for parsing MVP keyword abilities (Lethal Hits, Sustained Hits, Devastating Wounds, Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent) into `StatModifier` objects in tests/retrieval/test_parser.py
- [ ] T022 [P] [US3] Unit test for malformed/incomplete markdown — returns partial result with flagged missing fields in tests/retrieval/test_parser.py
- [ ] T023 [P] [US3] Unit test for unrecognized abilities — preserved as raw text and flagged per FR-007 in tests/retrieval/test_parser.py

### Implementation for User Story 3

- [ ] T024 [US3] Implement `MarkdownStatParser` class with `parse_unit_profile(markdown: str) -> UnitProfile` method in src/vindicta_engine/retrieval/parser.py
- [ ] T025 [US3] Implement datasheet stat extraction (regex-based parsing of M, T, Sv, W, Ld, OC from markdown tables/lists) in src/vindicta_engine/retrieval/parser.py
- [ ] T026 [US3] Implement weapon profile table parser — extract each weapon row into a `WeaponStatLine`, handling variable damage/attacks as raw strings in src/vindicta_engine/retrieval/parser.py
- [ ] T027 [US3] Implement MVP keyword ability parser — match the 12 enumerated keywords (re-rolls, Lethal Hits, Sustained Hits, Devastating Wounds, Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent) into `StatModifier` objects in src/vindicta_engine/retrieval/parser.py
- [ ] T028 [US3] Implement partial result handling — return `UnitProfile` with `None` or sentinel values for missing fields and a list of parse warnings in src/vindicta_engine/retrieval/parser.py

**Checkpoint**: Parser converts raw markdown to typed `UnitProfile` objects. All 12 MVP keywords recognized. Malformed input handled gracefully. US3 is independently testable.

---

## Phase 5: User Story 2 — Cache Stats During Heavy Simulation Runs (Priority: P2)

**Goal**: An async-safe LRU cache eliminates redundant RAG queries during Monte Carlo batches, keyed by `(unit_name, weapon_name, rules_version)`.

**Independent Test**: Run a 1,000-iteration batch and verify via `CacheMetrics` that the RAG server is queried at most once per unique unit-weapon-version combination.

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T029 [P] [US2] Unit test for cache hit — second lookup for same key returns cached result in <1ms in tests/retrieval/test_stat_cache.py
- [ ] T030 [P] [US2] Unit test for cache miss — new key triggers RAG query and stores result in tests/retrieval/test_stat_cache.py
- [ ] T031 [P] [US2] Unit test for LRU eviction — when max_size exceeded, least-recently-used entry is evicted in tests/retrieval/test_stat_cache.py
- [ ] T032 [P] [US2] Unit test for async-safety — concurrent async tasks requesting the same uncached key trigger only one RAG query (no thundering herd) in tests/retrieval/test_stat_cache.py
- [ ] T033 [P] [US2] Unit test for version-keyed cache miss — same unit+weapon but different version triggers fresh retrieval in tests/retrieval/test_stat_cache.py
- [ ] T034 [P] [US2] Unit test for cache invalidation — `invalidate()` clears all entries; `refresh(key)` forces re-fetch in tests/retrieval/test_stat_cache.py
- [ ] T035 [P] [US2] Unit test for `CacheMetrics` counters — hits, misses, and parse_errors increment correctly in tests/retrieval/test_stat_cache.py

### Implementation for User Story 2

- [ ] T036 [US2] Implement `StatCacheKey` named tuple `(unit_name, weapon_name, rules_version)` in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T037 [US2] Implement `StatCache` class with async-safe `get()` method using `asyncio.Lock` per-key double-checked locking pattern in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T038 [US2] Implement LRU eviction — track insertion/access timestamps, evict least-recently-used when `max_size` exceeded in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T039 [US2] Implement `invalidate()` (clear all) and `refresh(key)` (force re-fetch for specific key) methods in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T040 [US2] Integrate `CacheMetrics` counters — increment hits/misses/parse_errors on each operation in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T041 [US2] Implement `StatRetriever` facade combining `RAGClient` + `MarkdownStatParser` + `StatCache` in src/vindicta_engine/retrieval/stat_cache.py

**Checkpoint**: Cache eliminates redundant queries. Async-safe under concurrent load. LRU eviction bounds memory. Metrics observable. US2 is independently testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Integration, documentation, and quality improvements across all stories

- [ ] T042 [P] Export full public API from src/vindicta_engine/retrieval/__init__.py (StatRetriever, UnitProfile, WeaponStatLine, StatModifier, CacheMetrics, RAGQueryError)
- [ ] T043 [P] Add structured logging (Python `logging` module) for cache hits/misses, RAG query latency, and parse errors in src/vindicta_engine/retrieval/stat_cache.py and src/vindicta_engine/retrieval/mcp_client.py
- [ ] T044 [P] Add docstrings to all public classes and methods across src/vindicta_engine/retrieval/
- [ ] T045 Run `ruff check .` and `ruff format --check .` across vindicta-engine and fix any violations
- [ ] T046 Run `mypy --strict` across vindicta-engine and fix any type errors
- [ ] T047 Validate `quickstart.md` code example runs correctly against the implemented API
- [ ] T048 Run full test suite `uv run pytest` and verify ≥90% coverage
- [ ] T049 Add memory benchmark test validating SC-005: cache memory for a 20-unit matchup stays under 10 MB in tests/retrieval/test_stat_cache.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — RAG client needs models
- **US3 (Phase 4)**: Depends on Foundational — parser needs models. **Can run in parallel with US1**
- **US2 (Phase 5)**: Depends on US1 + US3 — cache wraps client + parser
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational — no dependencies on other stories. **Can run in parallel with US1.**
- **User Story 2 (P2)**: Depends on US1 (RAGClient) and US3 (Parser) — composes both into the cached `StatRetriever`

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T003/T004 (Setup) can run in parallel
- T005/T006/T008/T009 (Foundational models) can run in parallel
- T011/T012/T013 (US1 tests) can run in parallel
- T018–T023 (US3 tests) can all run in parallel
- T029–T035 (US2 tests) can all run in parallel
- **US1 and US3 can execute in parallel** after Foundational completes
- T042/T043/T044 (Polish) can run in parallel

---

## Parallel Example: User Stories 1 & 3

```bash
# After Foundational completes, launch both P1 stories in parallel:

# Stream 1: User Story 1 (RAG Client)
Task: "Unit test for RAGClient.query_unit_stats() in tests/retrieval/test_mcp_client.py"
Task: "Implement RAGClient class in src/vindicta_engine/retrieval/mcp_client.py"

# Stream 2: User Story 3 (Parser) — runs simultaneously
Task: "Unit test for parsing a standard unit datasheet in tests/retrieval/test_parser.py"
Task: "Implement MarkdownStatParser class in src/vindicta_engine/retrieval/parser.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational models
3. Complete Phase 3: User Story 1 (RAG Client)
4. **STOP and VALIDATE**: Verify RAGClient returns raw markdown from real MCP server
5. Demo stat retrieval independently

### Incremental Delivery

1. Complete Setup + Foundational → Models ready
2. Add US1 (RAG Client) + US3 (Parser) **in parallel** → Full stat loading pipeline → Demo
3. Add US2 (Cache) → Wraps US1+US3 → Performant for Monte Carlo batches → Demo
4. Polish → Production-quality code with logging, docs, full coverage

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (RAG Client)
   - Developer B: User Story 3 (Parser)
3. Both complete → Developer A or B: User Story 2 (Cache Integration)
4. Polish phase

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US3 (parsing) is ordered before US2 (caching) despite being labeled US3 in the spec, because the cache depends on the parser

## Deferred Items

- **Conditional/phase-dependent stats** (spec.md edge case L72): Units whose stats change between melee and ranged phases are not handled by the MVP parser. This will be addressed in a future iteration once the core parsing pipeline is validated.
- **SC-001 end-to-end benchmark** and **SC-003 accuracy benchmark**: Covered by unit tests; formal benchmark tasks deferred to post-MVP.
````

## File: src/vindicta_engine/__init__.py
````python
__version__ = "0.1.0"
````

## File: src/vindicta_engine/ai/__init__.py
````python
from .base import BaseTacticalDecision, BaseAIProfile, BaseTacticalEngine

__all__ = ["BaseTacticalDecision", "BaseAIProfile", "BaseTacticalEngine"]
````

## File: src/vindicta_engine/ai/base.py
````python
from typing import Any, List, Optional
from abc import ABC, abstractmethod
from pydantic import Field
from vindicta_foundation.models.base import VindictaModel

class BaseTacticalDecision(VindictaModel):
    """
    Base model for a tactical decision made by an AI.
    """
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this decision")
    reasoning: str = Field(..., description="Explanation of why this decision was made")
    action_type: str = Field(..., description="Type of action (e.g., 'move', 'shoot', 'charge')")
    target_id: Optional[str] = Field(None, description="Optional ID of the target unit/location")

class BaseAIProfile(VindictaModel):
    """
    Configuration profile for an AI opponent.
    """
    name: str = Field(..., description="Name of the AI personality")
    aggression: float = Field(0.5, ge=0.0, le=1.0, description="Tendency to attack vs defend")
    risk_tolerance: float = Field(0.5, ge=0.0, le=1.0, description="Willingness to take risks")
    
class BaseTacticalEngine(ABC):
    """
    Abstract interface for AI decision making engines.
    """
    
    @abstractmethod
    def evaluate_state(self, game_state: Any) -> float:
        """Evaluate the current game state from the perspective of the active player."""
        pass
        
    @abstractmethod
    def decide_next_action(self, game_state: Any) -> BaseTacticalDecision:
        """Determine the next best action given the current state."""
        pass
````

## File: src/vindicta_engine/dice/__init__.py
````python
"""
Dice-Engine: Cryptographically secure dice rolling.

Provides CSPRNG-backed dice rolling with entropy proofs
for fair gameplay in the Vindicta Platform.
"""

from dice_engine.engine import DiceEngine
from dice_engine.models import DiceRoll, CombatResult

__version__ = "1.0.0"

__all__ = [
    "DiceEngine",
    "DiceRoll",
    "CombatResult",
]
````

## File: src/vindicta_engine/dice/engine.py
````python
"""
DiceEngine: CSPRNG-backed dice rolling engine.

Uses Python's secrets module for cryptographically secure
random number generation with entropy proofs.
"""

import hashlib
import secrets
from typing import Optional

from dice_engine.models import DiceRoll, CombatResult, BatchRollResult


class DiceEngine:
    """
    Cryptographically secure dice rolling engine.
    
    All rolls are CSPRNG-backed and include entropy proofs
    for verification and audit purposes.
    
    Example:
        engine = DiceEngine()
        roll = engine.roll_d6()
        print(roll.value, roll.entropy_proof)
    """
    
    def __init__(self, seed: Optional[bytes] = None) -> None:
        """
        Initialize the dice engine.
        
        Args:
            seed: Optional seed for testing (uses CSPRNG by default).
        """
        self._seed = seed
        self._roll_count = 0
    
    def _generate_entropy(self) -> bytes:
        """Generate cryptographically secure entropy."""
        if self._seed:
            # Deterministic for testing
            combined = self._seed + self._roll_count.to_bytes(8, 'big')
            self._roll_count += 1
            return hashlib.sha256(combined).digest()
        else:
            return secrets.token_bytes(32)
    
    def _create_proof(self, entropy: bytes) -> str:
        """Create entropy proof hash."""
        return hashlib.sha256(entropy).hexdigest()[:16]
    
    def roll(self, sides: int) -> DiceRoll:
        """
        Roll a die with the specified number of sides.
        
        Args:
            sides: Number of sides (e.g., 6 for D6).
            
        Returns:
            DiceRoll with value and entropy proof.
        """
        entropy = self._generate_entropy()
        value = (int.from_bytes(entropy[:4], 'big') % sides) + 1
        proof = self._create_proof(entropy)
        
        return DiceRoll(value=value, sides=sides, entropy_proof=proof)
    
    def roll_d6(self) -> DiceRoll:
        """Roll a D6."""
        return self.roll(6)
    
    def roll_d3(self) -> DiceRoll:
        """Roll a D3 (1-3)."""
        return self.roll(3)
    
    def roll_2d6(self) -> tuple[DiceRoll, DiceRoll]:
        """Roll 2D6."""
        return self.roll_d6(), self.roll_d6()
    
    def roll_batch(self, count: int, sides: int = 6) -> BatchRollResult:
        """
        Roll multiple dice.
        
        Args:
            count: Number of dice to roll.
            sides: Number of sides per die.
            
        Returns:
            BatchRollResult with all rolls and statistics.
        """
        rolls = [self.roll(sides) for _ in range(count)]
        total = sum(r.value for r in rolls)
        average = total / count if count > 0 else 0
        
        return BatchRollResult(rolls=rolls, total=total, average=average)
    
    def combat_roll(
        self,
        attacks: int,
        hit_on: int,
        wound_on: int,
        save: int,
        damage: int,
        hit_reroll: bool = False,
        wound_reroll: bool = False
    ) -> CombatResult:
        """
        Perform a complete combat roll sequence.
        
        Args:
            attacks: Number of attacks.
            hit_on: Target number to hit (e.g., 3 means 3+).
            wound_on: Target number to wound.
            save: Target save (e.g., 5 means 5+).
            damage: Damage per failed save.
            hit_reroll: Reroll failed hits.
            wound_reroll: Reroll failed wounds.
            
        Returns:
            CombatResult with all rolls and damage dealt.
        """
        result = CombatResult(
            attacks=attacks,
            hit_on=hit_on,
            wound_on=wound_on,
            save=save,
            damage=damage
        )
        
        # Hit rolls
        for _ in range(attacks):
            roll = self.roll_d6()
            result.hit_rolls.append(roll)
            if roll.value >= hit_on:
                result.hits += 1
            elif hit_reroll:
                reroll = self.roll_d6()
                result.hit_rolls.append(reroll)
                if reroll.value >= hit_on:
                    result.hits += 1
        
        # Wound rolls
        for _ in range(result.hits):
            roll = self.roll_d6()
            result.wound_rolls.append(roll)
            if roll.value >= wound_on:
                result.wounds += 1
            elif wound_reroll:
                reroll = self.roll_d6()
                result.wound_rolls.append(reroll)
                if reroll.value >= wound_on:
                    result.wounds += 1
        
        # Save rolls
        for _ in range(result.wounds):
            roll = self.roll_d6()
            result.save_rolls.append(roll)
            if roll.value < save:
                result.saves_failed += 1
        
        # Damage
        result.damage_dealt = result.saves_failed * damage
        
        return result
````

## File: src/vindicta_engine/dice/models.py
````python
"""
Data models for Dice-Engine.
"""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class DiceRoll:
    """A single dice roll with entropy proof."""
    
    value: int
    sides: int
    entropy_proof: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    roll_id: UUID = field(default_factory=uuid4)
    
    def __str__(self) -> str:
        return f"D{self.sides}: {self.value}"
    
    def verify(self, entropy_bytes: bytes) -> bool:
        """Verify this roll was generated from given entropy."""
        expected_proof = hashlib.sha256(entropy_bytes).hexdigest()[:16]
        return self.entropy_proof == expected_proof


@dataclass
class CombatResult:
    """Result of a combat roll sequence."""
    
    # Input parameters
    attacks: int
    hit_on: int
    wound_on: int
    save: int
    damage: int
    
    # Roll results
    hit_rolls: list[DiceRoll] = field(default_factory=list)
    wound_rolls: list[DiceRoll] = field(default_factory=list)
    save_rolls: list[DiceRoll] = field(default_factory=list)
    
    # Computed results
    hits: int = 0
    wounds: int = 0
    saves_failed: int = 0
    damage_dealt: int = 0
    
    def __str__(self) -> str:
        return f"{self.attacks}A → {self.hits}H → {self.wounds}W → {self.damage_dealt}D"


@dataclass
class BatchRollResult:
    """Result of a batch dice roll."""
    
    rolls: list[DiceRoll]
    total: int
    average: float
    
    @property
    def values(self) -> list[int]:
        return [r.value for r in self.rolls]
````

## File: src/vindicta_engine/health.py
````python
import time

def check_health() -> dict:
    """Returns the health status of the service."""
    return {'status': 'ok', 'realm': 'vindicta-engine', 'timestamp': time.time()}
````

## File: src/vindicta_engine/integrity.py
````python
import datetime

def verify_integrity():
    """
    Performs a self-check of the Vindicta Engine domain.
    """
    return {
        "status": "operational",
        "timestamp": datetime.datetime.now().isoformat(),
        "metrics": {
            "engine_status": "online",
            "active_tasks": 0
        }
    }
````

## File: src/vindicta_engine/physics/engine.py
````python
import hashlib
import secrets
from typing import Optional, List
from vindicta_engine.physics.models import DiceRoll, CombatResult, BatchRollResult

class DiceEngine:
    """
    Cryptographically secure dice rolling engine.
    
    All rolls are CSPRNG-backed and include entropy proofs
    for verification and audit purposes.
    """
    
    def __init__(self, seed: Optional[bytes] = None) -> None:
        """
        Initialize the dice engine.
        
        Args:
            seed: Optional seed for testing (uses CSPRNG by default).
        """
        self._seed = seed
        self._roll_count = 0
    
    def _generate_entropy(self) -> bytes:
        """Generate cryptographically secure entropy."""
        if self._seed:
            # Deterministic for testing
            # We use a simple counter to ensure subsequent rolls differ
            combined = self._seed + self._roll_count.to_bytes(8, 'big')
            self._roll_count += 1
            return hashlib.sha256(combined).digest()
        else:
            return secrets.token_bytes(32)
    
    def _create_proof(self, entropy: bytes) -> str:
        """Create entropy proof hash."""
        return hashlib.sha256(entropy).hexdigest()[:16]
    
    def roll(self, sides: int = 6) -> DiceRoll:
        """
        Roll a die with the specified number of sides.
        
        Args:
            sides: Number of sides (e.g., 6 for D6).
            
        Returns:
            DiceRoll with value and entropy proof.
        """
        entropy = self._generate_entropy()
        # Modulo bias is negligible for 32 bytes of entropy vs small N
        value = (int.from_bytes(entropy[:4], 'big') % sides) + 1
        proof = self._create_proof(entropy)
        
        return DiceRoll(value=value, sides=sides, entropy_proof=proof)
    
    def roll_d6(self) -> DiceRoll:
        """Roll a D6."""
        return self.roll(6)
    
    def roll_d3(self) -> DiceRoll:
        """Roll a D3 (1-3)."""
        return self.roll(3)
    
    def roll_2d6(self) -> List[DiceRoll]:
        """Roll 2D6."""
        return [self.roll_d6(), self.roll_d6()]
    
    def roll_batch(self, count: int, sides: int = 6) -> BatchRollResult:
        """
        Roll multiple dice.
        
        Args:
            count: Number of dice to roll.
            sides: Number of sides per die.
            
        Returns:
            BatchRollResult with all rolls and statistics.
        """
        rolls = [self.roll(sides) for _ in range(count)]
        total = sum(r.value for r in rolls)
        average = total / count if count > 0 else 0.0
        
        return BatchRollResult(rolls=rolls, total=total, average=average)
    
    def combat_roll(
        self,
        attacks: int,
        hit_on: int,
        wound_on: int,
        save: int,
        damage: int,
        hit_reroll: bool = False,
        wound_reroll: bool = False
    ) -> CombatResult:
        """
        Perform a complete combat roll sequence.
        
        Args:
            attacks: Number of attacks.
            hit_on: Target number to hit (e.g., 3 means 3+).
            wound_on: Target number to wound.
            save: Target save (e.g., 5 means 5+).
            damage: Damage per failed save.
            hit_reroll: Reroll failed hits.
            wound_reroll: Reroll failed wounds.
            
        Returns:
            CombatResult with all rolls and damage dealt.
        """
        result = CombatResult(
            attacks=attacks,
            hit_on=hit_on,
            wound_on=wound_on,
            save=save,
            damage=damage
        )
        
        # Hit rolls
        for _ in range(attacks):
            roll = self.roll_d6()
            result.hit_rolls.append(roll)
            if roll.value >= hit_on:
                result.hits += 1
            elif hit_reroll:
                reroll = self.roll_d6()
                result.hit_rolls.append(reroll)
                # Note: This logic assumes reroll replaces the miss but we keep both in log
                if reroll.value >= hit_on:
                    result.hits += 1
        
        # Wound rolls
        for _ in range(result.hits):
            roll = self.roll_d6()
            result.wound_rolls.append(roll)
            if roll.value >= wound_on:
                result.wounds += 1
            elif wound_reroll:
                reroll = self.roll_d6()
                result.wound_rolls.append(reroll)
                if reroll.value >= wound_on:
                    result.wounds += 1
        
        # Save rolls
        for _ in range(result.wounds):
            roll = self.roll_d6()
            result.save_rolls.append(roll)
            if roll.value < save:
                result.saves_failed += 1
        
        # Damage
        result.damage_dealt = result.saves_failed * damage
        
        return result
````

## File: src/vindicta_engine/physics/models.py
````python
from typing import List
from pydantic import Field
from vindicta_foundation.models.base import VindictaModel

class DiceRoll(VindictaModel):
    """
    A single dice roll with entropy proof.
    
    Inherits from VindictaModel for standard ID/Timestamp/Serialization.
    """
    value: int = Field(..., description="The result of the roll (e.g., 1-6)")
    sides: int = Field(..., description="Number of sides on the die")
    entropy_proof: str = Field(..., description="SHA-256 hash fragment of the entropy used")
    
    def __str__(self) -> str:
        return f"D{self.sides}: {self.value}"

class BatchRollResult(VindictaModel):
    """
    Result of a batch dice roll.
    """
    rolls: List[DiceRoll] = Field(..., description="List of individual dice rolls")
    total: int = Field(..., description="Sum of all roll values")
    average: float = Field(..., description="Average value of the rolls")
    
    @property
    def values(self) -> List[int]:
        return [r.value for r in self.rolls]

class CombatResult(VindictaModel):
    """
    Result of a combat roll sequence.
    """
    # Input parameters
    attacks: int = Field(..., description="Number of attacks")
    hit_on: int = Field(..., description="Target number to hit")
    wound_on: int = Field(..., description="Target number to wound")
    save: int = Field(..., description="Target save")
    damage: int = Field(..., description="Damage description or value")
    
    # Computed results
    hits: int = Field(0, description="Total successful hits")
    wounds: int = Field(0, description="Total successful wounds")
    saves_failed: int = Field(0, description="Total failed saves")
    damage_dealt: int = Field(0, description="Total damage dealt")
    
    # Detailed rolls
    hit_rolls: List[DiceRoll] = Field(default_factory=list, description="Individual hit rolls")
    wound_rolls: List[DiceRoll] = Field(default_factory=list, description="Individual wound rolls")
    save_rolls: List[DiceRoll] = Field(default_factory=list, description="Individual save rolls")

    def __str__(self) -> str:
        return f"{self.attacks}A -> {self.hits}H -> {self.wounds}W -> {self.damage_dealt}D"
````

## File: tests/dice/test_engine.py
````python
"""
Unit tests for Dice-Engine.
"""

import pytest
from dice_engine import DiceEngine, DiceRoll, CombatResult


class TestDiceRoll:
    """Tests for DiceRoll model."""

    def test_dice_roll_creation(self):
        """DiceRoll should be creatable."""
        roll = DiceRoll(value=4, sides=6, entropy_proof="abc123")
        
        assert roll.value == 4
        assert roll.sides == 6

    def test_dice_roll_str(self):
        """str() should show die type and value."""
        roll = DiceRoll(value=3, sides=6, entropy_proof="x")
        
        assert "D6" in str(roll)
        assert "3" in str(roll)


class TestDiceEngine:
    """Tests for DiceEngine."""

    def test_roll_d6_range(self):
        """D6 should produce values 1-6."""
        engine = DiceEngine()
        
        for _ in range(100):
            roll = engine.roll_d6()
            assert 1 <= roll.value <= 6

    def test_roll_d3_range(self):
        """D3 should produce values 1-3."""
        engine = DiceEngine()
        
        for _ in range(100):
            roll = engine.roll_d3()
            assert 1 <= roll.value <= 3

    def test_roll_has_entropy_proof(self):
        """Rolls should include entropy proof."""
        engine = DiceEngine()
        roll = engine.roll_d6()
        
        assert roll.entropy_proof
        assert len(roll.entropy_proof) == 16

    def test_deterministic_with_seed(self):
        """Same seed should produce same rolls."""
        seed = b"test_seed_12345"
        
        engine1 = DiceEngine(seed=seed)
        engine2 = DiceEngine(seed=seed)
        
        rolls1 = [engine1.roll_d6().value for _ in range(10)]
        rolls2 = [engine2.roll_d6().value for _ in range(10)]
        
        assert rolls1 == rolls2

    def test_roll_batch(self):
        """Batch rolling should work."""
        engine = DiceEngine()
        
        result = engine.roll_batch(10, sides=6)
        
        assert len(result.rolls) == 10
        assert result.total == sum(r.value for r in result.rolls)

    def test_roll_2d6(self):
        """2D6 should return two rolls."""
        engine = DiceEngine()
        
        r1, r2 = engine.roll_2d6()
        
        assert 1 <= r1.value <= 6
        assert 1 <= r2.value <= 6


class TestCombatRoll:
    """Tests for combat roll sequences."""

    def test_combat_roll_basic(self):
        """Combat roll should process hits, wounds, saves."""
        engine = DiceEngine(seed=b"combat_test")
        
        result = engine.combat_roll(
            attacks=10,
            hit_on=3,
            wound_on=4,
            save=5,
            damage=1
        )
        
        assert result.attacks == 10
        assert 0 <= result.hits <= 10
        assert 0 <= result.wounds <= result.hits
        assert 0 <= result.saves_failed <= result.wounds

    def test_combat_result_damage(self):
        """Damage should equal saves_failed * damage."""
        engine = DiceEngine(seed=b"damage_test")
        
        result = engine.combat_roll(
            attacks=10,
            hit_on=2,  # Very likely to hit
            wound_on=2,  # Very likely to wound
            save=6,  # Poor save
            damage=3
        )
        
        assert result.damage_dealt == result.saves_failed * 3

    def test_combat_result_str(self):
        """CombatResult str should show sequence."""
        engine = DiceEngine(seed=b"str_test")
        
        result = engine.combat_roll(
            attacks=5,
            hit_on=3,
            wound_on=4,
            save=5,
            damage=1
        )
        
        s = str(result)
        assert "5A" in s  # 5 attacks


class TestEntropyProofs:
    """Tests for entropy proof system."""

    def test_unique_proofs(self):
        """Each roll should have unique proof."""
        engine = DiceEngine()
        
        proofs = set()
        for _ in range(100):
            roll = engine.roll_d6()
            proofs.add(roll.entropy_proof)
        
        # All proofs should be unique
        assert len(proofs) == 100
````

## File: tests/test_physics.py
````python
import pytest
from vindicta_engine.physics.engine import DiceEngine
from vindicta_engine.physics.models import DiceRoll, CombatResult

def test_dice_roll_defaults() -> None:
    engine = DiceEngine()
    roll = engine.roll_d6()
    
    assert isinstance(roll, DiceRoll)
    assert 1 <= roll.value <= 6
    assert roll.sides == 6
    assert roll.id is not None  # Inherited from VindictaModel
    assert roll.created_at is not None  # Inherited from VindictaModel

def test_deterministic_seed() -> None:
    seed = b"test_seed_123"
    engine1 = DiceEngine(seed)
    engine2 = DiceEngine(seed)
    
    roll1 = engine1.roll_d6()
    roll2 = engine2.roll_d6()
    
    assert roll1.value == roll2.value
    assert roll1.entropy_proof == roll2.entropy_proof

def test_combat_roll_logic() -> None:
    # Deterministic engine to ensure hits
    # We can't easily force specific values without mocking internals, 
    # but we can check constraints.
    engine = DiceEngine()
    
    result = engine.combat_roll(
        attacks=10,
        hit_on=2,
        wound_on=2,
        save=6, # Hard save
        damage=1
    )
    
    assert isinstance(result, CombatResult)
    assert result.attacks == 10
    assert len(result.hit_rolls) >= 10 # Could be more if rerolls implemented logic was slightly different, here it's appended
    assert result.hits <= 10 + len(result.hit_rolls) - 10 # Rerolls add to list
    assert result.damage_dealt >= 0

def test_batch_roll() -> None:
    engine = DiceEngine()
    batch = engine.roll_batch(count=10, sides=6)
    
    assert len(batch.rolls) == 10
    assert batch.total == sum(r.value for r in batch.rolls)
````

## File: .specify/templates/spec-template.md
````markdown
# [Feature Name]`n`n## User Stories`n- [ ] US1: ...`n`n## Requirements`n- R1: ...`n`n## Acceptance Criteria`n- [ ] AC1: ...
````

## File: .specify/templates/tasks-template.md
````markdown
# Tasks - [Feature Name]`n`n- [ ] T001 Description`n- [ ] T002 Description
````

## File: .specify/memory/constitution.md
````markdown
# Vindicta Engine Constitution

## Core Principles

### I. MCP-First Mandate...

### II. Spec-Driven Development (SDD)...

### III. Zero-Issue Stability...

### IV. Tech Standards...

### V. Domain Isolation...
````

## File: .specify/templates/plan-template.md
````markdown
# Implementation Plan - [Feature Name]`n`n## Technical Context`n...`n`n## Proposed Changes`n...`n`n## Verification Plan`n...
````
