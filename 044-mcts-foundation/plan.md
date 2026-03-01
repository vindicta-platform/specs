# Implementation Plan: FEAT-044 MCTS Engine Foundation

**Branch**: `044-mcts-foundation` | **Date**: 2026-02-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/044-mcts-foundation/spec.md`

## Summary

Implement a Monte Carlo Tree Search (MCTS) Engine to evaluate Warhammer 40k board states. The engine will manage a deterministic game tree within a pre-allocated fixed memory buffer (512MB default, ~1.75M nodes), feature configurable OpenTelemetry-based observability traces, and handle invalid move constraints by clamping (weighted proximity metric) or hard failing with structured trace output.

## Technical Context

**Language/Version**: Python 3.12+ (uv workspace)
**Primary Dependencies**: `vindicta-foundation` (Entropy Buffer, base models), `vindicta-engine` (core game logic)
**Storage**: Transient In-Memory (Pre-allocated Arena Allocator, 512MB default, bound by 4GB container limit)
**Testing**: `pytest` (minimum 90% coverage, heavy unit testing) + `behave` (BDD acceptance scenarios per Constitution §III SDD→BDD→TDD mandate)
**Target Platform**: Linux Container (4-core x86_64 or ARM64, ≥2.5 GHz, 4GB RAM)
**Project Type**: Core backend library / module
**Performance Goals**: ≥2,000 NPS; evaluate mid-game state to a depth of 3 full-ply within 5 seconds (4,750ms effective + 250ms safety buffer)
**Constraints**: Hard boundary on memory (arena buffer), 100% test coverage on 15 defined move generator edge cases (EC-001 through EC-015)
**Scale/Scope**: Manage thousands of MCTS nodes per request efficiently in Python using NumPy structured arrays

### Key Definitions

| Term | Definition |
|------|-----------|
| **Depth 3** | 3 full-ply: each ply = one complete phase-sequential action set for one player |
| **Principal Variation** | The ordered sequence of best moves (phase-actions) from root to the deepest evaluated leaf, analogous to chess PV but representing 40k phase sequences |
| **Standard Hardware** | 4-core CPU (x86_64 or ARM64), ≥2.5 GHz, 4GB RAM container, no GPU |
| **Evaluation Score** | Unbounded float where positive = advantage for active player, negative = disadvantage. Range typically [-10.0, +10.0] in practice |
| **NPS** | Nodes Per Second — target ≥2,000 for foundation, ≥5,000 with NumPy vectorization |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Foundation Law (Zero-Order Axioms)**: Does this feature violate established physical/logical boundaries? (No, mathematical validation only).
- [x] **Structural Integrity**: Will domain models correctly inherit from `VindictaModel`? (Yes, `GameState`, `SearchNode`, `MCTSResult`, and `HeuristicConfig` will be `VindictaModel`s).
- [x] **Quality Mandates**: Is 90% test coverage and strict type checking accounted for? (Yes, enforced via `pytest` and `mypy`).
- [x] **Architecture Documentation**: Are container boundaries changing, requiring a C4 Model/ADR update?
- [x] **Meso-Repo Consolidation**: Will this feature follow ADR 0006 if porting code? (N/A, new feature).
- [x] **Gate VI (Economy)**: Does the Engine return cost metrics? (Yes, `MCTSResult.nodes_visited` + `computation_time_ms` for upstream economy metering).
- [x] **Gate VII (Observability)**: Is OTel integration planned? (Yes, `MCTSTracer` wraps OTLP exporter with 4 configurable levels).

## Project Structure

### Documentation (this feature)

```text
specs/044-mcts-foundation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── engine-api.md
├── checklists/
│   ├── requirements.md
│   ├── quality-assurance.md
│   ├── comprehensive.md
│   └── technical-design.md
└── tasks.md
```

### Source Code (repository root)

```text
vindicta-engine/
├── src/
│   └── vindicta_engine/
│       ├── mcts/
│       │   ├── __init__.py
│       │   ├── engine.py
│       │   ├── arena.py
│       │   ├── heuristics.py
│       │   ├── generator.py
│       │   ├── config.py        # MCTSTraceLevel enum
│       │   ├── tracer.py        # MCTSTracer observability
│       │   ├── zobrist.py       # Zobrist hash constants & functions
│       │   ├── move_stack.py    # MoveStack, MoveDelta (undo logic)
│       │   └── exceptions.py    # InvalidMoveExecutionTrace, ArenaExhaustedError
└── tests/
    ├── mcts/
    │   ├── test_engine.py
    │   ├── test_arena.py
    │   ├── test_generator.py
    │   ├── test_heuristics.py
    │   ├── test_zobrist.py
    │   ├── test_tracer.py
    │   └── test_move_stack.py
    ├── features/                  # BDD (behave) acceptance scenarios
    │   ├── board_evaluation.feature
    │   ├── move_generation.feature
    │   ├── arena_limits.feature
    │   └── steps/
    │       ├── evaluation_steps.py
    │       ├── movegen_steps.py
    │       └── arena_steps.py
    └── fixtures/
        └── entropy/
            ├── charge_9inch.json
            ├── bolter_volley_t4.json
            ├── melta_t8.json
            └── manifest.json

vindicta-foundation/
├── src/
│   └── vindicta_foundation/
│       └── models/
│           ├── mcts.py           # GameState, SearchNode, MCTSResult, HeuristicConfig
│           └── entropy.py        # EntropyBufferProtocol, AttackProfile, StubEntropyBuffer

docs/
└── architecture/
    └── mcts_engine.md            # FR-007 deliverable (7 required sections)
```

**Structure Decision**: The MCTS Engine will live as a submodule within `vindicta-engine` (`src/vindicta_engine/mcts/`), as it heavily relies on the domain logic. Domain models representing the state (`GameState`, `SearchNode`, `MCTSResult`, `HeuristicConfig`) will be defined in `vindicta-foundation/models/` to preserve cross-package transportability.

## Dependencies & Cross-Repo Build

| Dependency | Repo | Status | Strategy |
|-----------|------|--------|----------|
| `VindictaModel` base class | `vindicta-foundation` | ✅ Available | Import directly |
| Entropy Buffer API | `vindicta-foundation` | ⚠️ Future | Use `StubEntropyBuffer` with JSON fixtures |
| Core game rules | `vindicta-engine` | ✅ Available | Call directly; Cython subset deferred to Phase 2 |
| Oracle rule cache | `vindicta-oracle` | ⚠️ Future | Not in scope for foundation |
| Economy metering | `vindicta-economy` | ⚠️ Future | Engine only *returns* metrics; billing handled upstream |

**Build dependency**: `vindicta-engine` depends on `vindicta-foundation` via `uv` workspace. Tests require both packages installed. CI must install foundation before engine.

## Complexity & Risk Tracker

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| NumPy arena slower than needed | Medium | High | Benchmark at 1,000-node test; fallback to Cython |
| Branching factor exceeds estimates | Medium | High | Progressive unpruning + aggressive forward pruning |
| Entropy Buffer unavailable | High | Medium | StubEntropyBuffer with static JSON fixtures |
| Determinism broken by Root Parallelism | Low | Critical | Fixed arena slices + deterministic RNG per worker |
| Heuristic weights produce degenerate play | Medium | Medium | Remote config allows rapid tuning without redeploy |

## Acceptance Scenario Traceability

| Requirement | Traced To |
|-------------|-----------|
| FR-001 | US1 Acceptance Scenario, SC-001 |
| FR-002 | US1 Acceptance Scenario (depth/time params), SC-001 |
| FR-003 | Research §12 (Entropy Buffer Interface) |
| FR-004 | Research §1 (Arena Allocator), SC-001 (within time budget) |
| FR-005 | Research §3 (Observability & Tracing) |
| FR-006 | Contract API (`MCTSResult.nodes_visited`, `computation_time_ms`) |
| FR-007 | Research §13 (Documentation Architecture, 7 sections) |
