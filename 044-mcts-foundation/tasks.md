# Tasks: FEAT-044 MCTS Engine Foundation (PAUSED)

> [!IMPORTANT]
> This task is currently **PAUSED** per ADL directive (2026-03-07) to prioritize the organization-wide CI template rollout.

**Input**: Design documents from `/specs/044-mcts-foundation/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/engine-api.md ✅, quickstart.md ✅, checklists/ ✅
**Branch**: `044-mcts-foundation`

**Tests**: MANDATORY — per Quality Mandates (Constitution §III) and Spec Clarifications (≥90% coverage, heavy unit testing focus).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **vindicta-foundation**: `vindicta-foundation/src/vindicta_foundation/` (domain models)
- **vindicta-engine**: `vindicta-engine/src/vindicta_engine/mcts/` (engine module)
- **vindicta-engine tests**: `vindicta-engine/tests/mcts/` (test suite)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependency wiring, and skeleton module structure

- [ ] T001 Create MCTS module directory structure in `vindicta-engine/src/vindicta_engine/mcts/` with `__init__.py`, `engine.py`, `arena.py`, `heuristics.py`, `generator.py`, `config.py`, `zobrist.py`, `move_stack.py`, `tracer.py`, `exceptions.py`
- [ ] T002 Create MCTS test directory structure in `vindicta-engine/tests/mcts/` with `__init__.py`, `test_engine.py`, `test_arena.py`, `test_generator.py`, `test_heuristics.py`, `conftest.py`
- [ ] T002a [P] Initialize BDD structure in `vindicta-engine/tests/features/` with `steps/` directory and `environment.py` (Constitution §III SDD→BDD→TDD mandate)
- [ ] T003 [P] Add MCTS-specific dependencies to `vindicta-engine/pyproject.toml` (ensure `vindicta-foundation` workspace dependency, `pytest`, `pytest-cov`, `mypy` dev deps)
- [ ] T004 [P] Create `MCTSTraceLevel` enum in `vindicta-engine/src/vindicta_engine/mcts/config.py` with values: `NONE`, `BASIC`, `PV`, `FULL` (per Research §3)
- [ ] T005 [P] Create `InvalidMoveExecutionTrace` custom exception class in `vindicta-engine/src/vindicta_engine/mcts/exceptions.py` (per Research §2)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Domain models and arena allocator that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Domain Models (vindicta-foundation)

- [x] T006 [P] Implement `GameState` model in `vindicta-foundation/src/vindicta_foundation/models/mcts.py` inheriting from `VindictaModel` with fields: `turn_number` (int, 1-5), `active_player` (str), `unit_positions` (Dict[str, tuple[float, float, float]]), `unit_state_flags` (Dict[str, list[str]]), `vp_scores` (Dict[str, int]). Include `model_validate_json` support and copy-on-write semantics per Data Model spec
- [x] T007 [P] Implement `SearchNode` model in `vindicta-foundation/src/vindicta_foundation/models/mcts.py` inheriting from `VindictaModel` with fields: `id` (int), `parent_id` (int | None), `children` (list[int]), `state_hash` (str), `move_causing_state` (str | None), `visits` (int), `value_sum` (float), `is_terminal_node` (bool)
- [x] T008 [P] Implement `MCTSResult` model in `vindicta-foundation/src/vindicta_foundation/models/mcts.py` inheriting from `VindictaModel` with fields: `evaluation_score` (float), `principal_variation` (list[str]), `nodes_visited` (int), `computation_time_ms` (float), `cache_hits` (int), `trace_log` (str | None) per Contract §MCTSResult
- [x] T009 Export `GameState`, `SearchNode`, `MCTSResult` from `vindicta-foundation/src/vindicta_foundation/models/__init__.py` (Constitution §II)

### Arena Allocator (vindicta-engine)

- [ ] T010 Implement `ArenaAllocator` class in `vindicta-engine/src/vindicta_engine/mcts/arena.py` with: pre-allocated `SearchNode` pool sized by `memory_limit_mb`, `allocate() -> int` returning pool index, `get(index: int) -> SearchNode`, `release(index: int)`, `is_full() -> bool` (at 90% capacity threshold per Research §1), `reset()` to reclaim all slots. Use flat list or array-based pooling (pure Python 3.12, per Research §1)
- [ ] T011 Implement arena capacity enforcement in `vindicta-engine/src/vindicta_engine/mcts/arena.py`: when arena hits 90% capacity, stop deep expansion. At 100% capacity, raise a bounded `ArenaExhaustedError` with trace metadata

### Observability Infrastructure

- [ ] T012 [P] Implement `MCTSTracer` class in `vindicta-engine/src/vindicta_engine/mcts/tracer.py` with trace level support: `NONE` (no-op), `BASIC` (tracks `nodes_visited`, `cache_hits`, `time_elapsed`), `PV` (captures principal variation list), `FULL` (dumps arena buffer state to JSON lines). Include `start_search()`, `record_node()`, `record_pv()`, `finish_search() -> str | None` methods (per Research §3, FR-005)

### State & Undo Logic (vindicta-engine)

- [ ] T012c [US1] Implement Zobrist hashing for GameState in `vindicta_engine/mcts/zobrist.py` to enable efficient transposition table lookups.
- [ ] T012d [US1] Implement `MoveStack` and `MoveDelta` in `vindicta_engine/mcts/move_stack.py` to support efficient board state rollbacks during search.

### BDD Acceptance Scenarios (MANDATORY — SDD → BDD → TDD)

- [ ] T012a [P] Write BDD feature file `vindicta-engine/tests/features/arena_limits.feature` encoding the arena capacity, extraction, and exhaustion scenarios.
- [ ] T012b [P] Implement behave step definitions in `vindicta-engine/tests/features/steps/arena_steps.py` for the arena_limits feature.

### Foundational Tests (MANDATORY — Write FIRST, ensure they FAIL)

- [ ] T013 [P] Write unit tests for `GameState` model validation in `vindicta-engine/tests/mcts/test_models.py`: test JSON serialization/deserialization, copy-on-write semantics, `turn_number` range validation (1-5), missing field handling
- [ ] T014 [P] Write unit tests for `SearchNode` model in `vindicta-engine/tests/mcts/test_models.py`: test arena index assignments, parent-child pointer consistency, `state_hash` uniqueness
- [ ] T015 [P] Write unit tests for `ArenaAllocator` in `vindicta-engine/tests/mcts/test_arena.py`: test allocation, retrieval, release, 90% capacity threshold, 100% exhaustion error, reset behavior, memory limit enforcement
- [ ] T016 [P] Write unit tests for `MCTSTracer` in `vindicta-engine/tests/mcts/test_tracer.py`: test all four trace levels produce correct output format, `NONE` has zero overhead, `FULL` produces valid JSON lines

### Test Fixtures

- [ ] T017 Create shared test fixtures in `vindicta-engine/tests/mcts/conftest.py`: `sample_game_state` (mid-game Turn 3, 2 players, 5+ units each), `winning_game_state` (Turn 4, 20 VP lead, dominant board control per US1 independent test), `locked_in_combat_state` (unit in engagement range per US2 acceptance scenario), `empty_arena(memory_limit_mb)` factory, `malformed_game_state` (missing required fields), `oversized_game_state` (exceeds max payload size)

### GameState Input Validation (FR-008)

- [ ] T017a [P] Write unit tests for `GameState` input validation in `vindicta-engine/tests/mcts/test_models.py`: test rejection of missing required fields, test rejection of `turn_number` outside 1-5, test rejection of payloads exceeding max size limit, test acceptance of valid minimal payload (per FR-008)
- [ ] T017b [P] Implement `GameState` input validation in `vindicta-engine/src/vindicta_engine/mcts/engine.py` or as a Pydantic validator on the model: reject payloads with missing required fields, invalid `turn_number` range (outside 1-5), or payloads exceeding configurable `max_payload_size_bytes` (per FR-008)

**Checkpoint**: Foundation ready — domain models defined, arena allocator functional, tracer operational. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 — Board State Evaluation (Priority: P1) 🎯 MVP

**Goal**: Take a mathematical snapshot of a 40k board state and evaluate win probability using MCTS, returning an evaluation score and principal variation (best line of play).

**Independent Test**: Feed a known "winning" board state (Turn 4, 20 VP lead, dominant board control) and verify the engine returns a >90% win probability. Feed the board state JSON, invoke `engine.evaluate_state(root_state, max_depth=3, time_budget_ms=5000)`, assert `result.evaluation_score > 0`, `result.principal_variation` is non-empty, `result.nodes_visited > 0`, `result.computation_time_ms <= 5000`.

### Tests for User Story 1 (MANDATORY — Write FIRST, ensure they FAIL) ⚠️

- [ ] T017c [P] [US1] Write BDD feature file `vindicta-engine/tests/features/board_evaluation.feature` encoding the US1 acceptance scenario: evaluate a known winning board state to a positive expected score.
- [ ] T017d [P] [US1] Implement behave step definitions in `vindicta-engine/tests/features/steps/evaluation_steps.py` for the board_evaluation feature.
- [ ] T018 [P] [US1] Write contract test for `MCTSEngine.evaluate_state()` in `vindicta-engine/tests/mcts/test_engine.py`: verify return type is `MCTSResult`, verify all fields populated, verify `computation_time_ms <= time_budget_ms`, verify `nodes_visited >= 1`
- [ ] T019 [P] [US1] Write unit test for static evaluation heuristic in `vindicta-engine/tests/mcts/test_heuristics.py`: verify VP-dominant state scores higher than balanced state, verify material-advantage state scores higher than deficit state, verify known winning fixture returns high positive score
- [ ] T019a [P] [US1] Write contract test for Entropy Buffer stub interface in `vindicta-engine/tests/mcts/test_heuristics.py`: verify `StubEntropyBuffer` implements the expected protocol, verify `evaluate_expected_value()` returns deterministic approximation for known dice profiles (per FR-003, M3)
- [ ] T020 [P] [US1] Write integration test for end-to-end evaluation in `vindicta-engine/tests/mcts/test_engine.py`: feed `winning_game_state` fixture, assert evaluation score is significantly positive, assert principal variation contains at least one move, assert completes within 5-second budget
- [ ] T020a [P] [US1] Write acceptance test for FR-006 economy metrics in `vindicta-engine/tests/mcts/test_engine.py`: verify `MCTSResult.computation_time_ms > 0` and `MCTSResult.nodes_visited >= 1` after any successful evaluation (per FR-006, US1 Acceptance Scenario 2)

### Implementation for User Story 1

- [ ] T021 [US1] Implement static evaluation heuristic function `evaluate_board(state: GameState) -> float` in `vindicta-engine/src/vindicta_engine/mcts/heuristics.py` using weighted heuristic factors: Victory Points differential, unit material count, board position/control assessment. Return bounded float evaluation score (per FR-001, FR-003 Entropy Buffer interface)
- [ ] T022 [US1] Implement Entropy Buffer integration stub in `vindicta-engine/src/vindicta_engine/mcts/heuristics.py`: `evaluate_expected_value(action, state) -> float` that interfaces with `vindicta-foundation` Entropy Buffer to compute expected dice roll values instead of raw simulation branching (per FR-003). Initially stub with deterministic approximation
- [ ] T023 [US1] Implement UCT (Upper Confidence bounds for Trees) selection policy in `vindicta-engine/src/vindicta_engine/mcts/engine.py`: `select_child(node: SearchNode, arena: ArenaAllocator) -> int` using standard UCT1 formula: $\bar{X}_j + C \sqrt{\frac{\ln n}{n_j}}$ with configurable exploration constant C (per Research, Extended Clarifications Q11)
- [ ] T024 [US1] Implement MCTS core loop in `vindicta-engine/src/vindicta_engine/mcts/engine.py` with four phases: Selection (UCT traversal), Expansion (allocate child from arena), Simulation (static evaluation via heuristics), Backpropagation (update visit counts and value sums up the tree). Enforce `max_depth` and `time_budget_ms` constraints (per FR-002)
- [ ] T025 [US1] Implement `MCTSEngine.__init__()` in `vindicta-engine/src/vindicta_engine/mcts/engine.py`: initialize `ArenaAllocator` with `memory_limit_mb`, initialize `MCTSTracer` with `trace_level`, store configuration (per Contract §MCTSEngine)
- [ ] T026 [US1] Implement `MCTSEngine.evaluate_state()` in `vindicta-engine/src/vindicta_engine/mcts/engine.py`: create root SearchNode from `root_state`, run MCTS core loop within time budget, extract principal variation from best path, assemble and return `MCTSResult` with all fields populated including `nodes_visited`, `computation_time_ms`, `cache_hits`, `trace_log` (per Contract §evaluate_state, FR-006)
- [ ] T027 [US1] Implement transposition table (state hash cache) in `vindicta-engine/src/vindicta_engine/mcts/engine.py`: detect previously visited `GameState` hashes to avoid redundant evaluation, increment `cache_hits` counter on MCTSTracer (per Data Model §SearchNode.state_hash)
- [ ] T027a [US1] Implement loop detection via transposition table in `vindicta-engine/src/vindicta_engine/mcts/engine.py`: during tree expansion, if a newly generated `state_hash` already exists in the transposition table at the same or shallower depth, terminate that branch as a repeated state to prevent infinite cycling (per Spec §Edge Cases, M5)
- [ ] T028 [US1] Add arena exhaustion handling to MCTS loop in `vindicta-engine/src/vindicta_engine/mcts/engine.py`: when `arena.is_full()`, stop expansion and return best result found so far with partial search trace (per FR-004, Research §1)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. The engine can accept a GameState JSON, run MCTS to depth 3 within 5 seconds, and return an evaluation score with principal variation.

---

## Phase 4: User Story 2 — Move Generation Validation (Priority: P1)

**Goal**: Generate all legal moves (movement, shooting targets, charge declarations) for a given unit in a given phase, so the MCTS algorithm branches correctly on legal actions only.

**Independent Test**: Place a unit in engagement range, request move generation for the Movement phase, verify only "Fall Back" and "Remain Stationary" are returned. Place a unit in open field, verify full movement options are generated.

### Tests for User Story 2 (MANDATORY — Write FIRST, ensure they FAIL) ⚠️

- [ ] T028a [P] [US2] Write BDD feature file `vindicta-engine/tests/features/move_generation.feature` encoding the US2 acceptance scenarios (movement locked in combat, out of LoS, etc).
- [ ] T028b [P] [US2] Implement behave step definitions in `vindicta-engine/tests/features/steps/movegen_steps.py` for the move_generation feature.
- [ ] T029 [P] [US2] Write unit test for legal move generation in `vindicta-engine/tests/mcts/test_generator.py`: test unit locked in combat only returns `[FallBack, RemainStationary]` for Movement phase (per US2 acceptance scenario)
- [ ] T030 [P] [US2] Write unit test for open-field movement in `vindicta-engine/tests/mcts/test_generator.py`: test unit in open field returns full movement options (Normal Move, Advance, Remain Stationary)
- [ ] T031 [P] [US2] Write unit test for shooting phase generation in `vindicta-engine/tests/mcts/test_generator.py`: test only valid targets within range and LoS are returned
- [ ] T032 [P] [US2] Write unit test for charge phase generation in `vindicta-engine/tests/mcts/test_generator.py`: test charge declarations only target valid units within charge range
- [ ] T033 [P] [US2] Write unit test for `clamp_move()` in `vindicta-engine/tests/mcts/test_generator.py`: test movement exceeding characteristic is clamped to max (e.g., 8" command on 6" unit clamps to 6"), test invalid LoS target returns `None` (hard fail), test `InvalidMoveExecutionTrace` is raised on unresolvable moves (per Research §2)
- [ ] T034 [P] [US2] Write edge case tests in `vindicta-engine/tests/mcts/test_generator.py` covering ALL 10 defined edge cases (EC-001 through EC-010 per SC-002): EC-001 unit locked in Engagement Range, EC-002 Deep Strike 9" minimum, EC-003 zero movement unit, EC-004 already acted this phase, EC-005 shooting out of LoS, EC-006 charge beyond 12", EC-007 shooting while in Engagement Range, EC-008 Fall Back restrictions (no shoot/charge after), EC-009 Advance restrictions (no non-Assault shooting), EC-010 unit destroyed mid-phase

### Implementation for User Story 2

- [ ] T035 [US2] Implement `MoveGenerator` class in `vindicta-engine/src/vindicta_engine/mcts/generator.py` with method `generate_legal_moves(state: GameState, unit_id: str, phase: str) -> list[str]` that returns all legal actions for a unit in the given game phase (Movement, Shooting, Charge, Fight)
- [ ] T036 [US2] Implement Movement phase logic in `vindicta-engine/src/vindicta_engine/mcts/generator.py`: check `unit_state_flags` for engagement status — if `In_Engagement_Range`: return only `[FallBack, RemainStationary]`; if free: return `[NormalMove, Advance, RemainStationary]` with distance bounded by unit movement characteristic
- [ ] T037 [US2] Implement Shooting phase logic in `vindicta-engine/src/vindicta_engine/mcts/generator.py`: validate line of sight (LoS), range checks, and target eligibility. Return list of valid `(weapon, target)` action pairs
- [ ] T038 [US2] Implement Charge phase logic in `vindicta-engine/src/vindicta_engine/mcts/generator.py`: validate charge range (up to 12"), check for intervening terrain/models, return valid charge target list
- [ ] T039 [US2] Implement `clamp_move(invalid_move: str, board_state: GameState) -> str | None` in `vindicta-engine/src/vindicta_engine/mcts/generator.py`: attempt to map invalid move to closest legal equivalent (e.g., clamp displacement vector to max range). Return `None` and raise `InvalidMoveExecutionTrace` if unresolvable (per Research §2, Spec §Edge Cases)
- [ ] T040 [US2] Implement Deep Strike and special deployment edge cases in `vindicta-engine/src/vindicta_engine/mcts/generator.py`: enforce 9" minimum distance from enemy models for Deep Strike, restrict to valid deployment zones (per SC-002 edge case coverage)
- [ ] T041 [US2] Wire `MoveGenerator` into MCTS expansion step in `vindicta-engine/src/vindicta_engine/mcts/engine.py`: replace placeholder child generation with `MoveGenerator.generate_legal_moves()` calls during tree expansion, ensuring only legal branches are created

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. The engine generates only legal moves and uses them for MCTS branching. Edge cases (engagement, Deep Strike) are validated.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, observability integration, type safety, and final quality gates

- [ ] T042 [P] Create Architectural Decision Record at `docs/architecture/adr/0010-mcts-engine-foundation.md` with 7 required sections: (1) Algorithmic Overview (MCTS four-phase loop), (2) Arena Allocator Mechanics (pooling, capacity thresholds, exhaustion behavior), (3) Heuristic Evaluation Strategy (weighted factors, Entropy Buffer), (4) Move Generator Design (phase logic, clamp_move), (5) Trace Level Behaviors (NONE/BASIC/PV/FULL), (6) Performance Budget (NPS targets, time slicing), (7) Extension Points (future Cython, Root Parallelism) — per FR-007
- [ ] T043 [P] Run `mypy --strict` on `vindicta-engine/src/vindicta_engine/mcts/` and fix all type errors (Constitution §III)
- [ ] T044 [P] Run `ruff check .` and `ruff format --check .` on both `vindicta-engine/` and `vindicta-foundation/` and fix all lint/format violations (Constitution §III)
- [ ] T045 Run `pytest --cov=vindicta_engine.mcts --cov-report=term-missing` and verify ≥90% coverage on all MCTS modules. Add missing tests to close any coverage gaps (Constitution §III, Spec §Clarifications)
- [ ] T046 [P] Verify `nodes_visited` and `computation_time_ms` are accurately populated in `MCTSResult` by running targeted assertions against known-node-count fixtures. Confirm values are non-zero and plausible for upstream economy metering/auditing (per FR-006). This is a verification/validation task — implementation is in T026
- [ ] T047 [P] Write quickstart validation test in `vindicta-engine/tests/mcts/test_quickstart.py` that executes the exact code sample from `specs/044-mcts-foundation/quickstart.md` to verify it runs without error
- [ ] T048a Run SC-001 performance validation: execute `MCTSEngine.evaluate_state()` with `winning_game_state` fixture, verify depth-3 full-ply evaluation completes in < 5 seconds on standard hardware baseline (4-core CPU, 4GB RAM)
- [ ] T048b Run SC-002 edge case validation: execute all 10 edge case tests (EC-001 through EC-010), verify 100% pass rate with zero illegal state generation
- [ ] T049 [P] Update `vindicta-engine` module `__init__.py` exports to include public API: `MCTSEngine`, `MCTSTraceLevel`
- [ ] T050 Code cleanup: remove any TODO stubs, ensure all docstrings are complete, verify no dead code in MCTS module

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — **BLOCKS all user stories**
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion — can run **in parallel** with US1
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) — No dependencies on US1 (independently testable). Integration task T041 wires US2 into US1's engine but US2's generator is testable standalone
- **Cross-story integration**: T041 (wire generator into engine) bridges US1 and US2 but both stories are independently completable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models / domain logic before engine integration
- Core algorithms before optimization
- Story complete before Polish phase

### Parallel Opportunities

#### Phase 1 (Setup)

- T003, T004, T005 can all run in parallel (different files)

#### Phase 2 (Foundational)

- T006, T007, T008 can all run in parallel [P] (independent models, same file is safe since each is a separate class definition)
- T012 can run in parallel with T010, T011 (different files)
- T013, T014, T015, T016 can all run in parallel (different test files/sections)
- T017a, T017b can run in parallel with other foundational tasks (FR-008 validation)

#### Phase 3 (US1) & Phase 4 (US2) — can run in parallel

- T018, T019, T019a, T020, T020a can run in parallel (different test focus areas)
- T029, T030, T031, T032, T033, T034 can all run in parallel (all in test_generator.py but independent test cases)

#### Phase 5 (Polish)

- T042, T043, T044, T046, T047, T048b, T049 can all run in parallel

---

## Parallel Example: User Story 1

```bash

# Launch all tests for User Story 1 together:

Task T018: "Contract test for MCTSEngine.evaluate_state() in tests/mcts/test_engine.py"
Task T019: "Unit test for static evaluation heuristic in tests/mcts/test_heuristics.py"
Task T020: "Integration test for end-to-end evaluation in tests/mcts/test_engine.py"

# Launch core implementation (after tests fail):

Task T021: "Static evaluation heuristic in src/vindicta_engine/mcts/heuristics.py"
Task T022: "Entropy Buffer integration stub in src/vindicta_engine/mcts/heuristics.py"

# Then sequential:

Task T023 → T024 → T025 → T026 → T027 → T028 (engine core loop, depends on heuristics)
```

## Parallel Example: User Story 2

```bash

# Launch ALL tests for User Story 2 together:

Task T029-T034: "All move generator tests in tests/mcts/test_generator.py"

# Launch implementation (after tests fail):

Task T035: "MoveGenerator class skeleton"
Task T036-T040: "Phase-specific logic (can be partially parallel within generator.py)"
Task T041: "Wire into engine (sequential, depends on T035 + US1 engine)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T005)
2. Complete Phase 2: Foundational (T006–T017)
3. Complete Phase 3: User Story 1 (T018–T028)
4. **STOP and VALIDATE**: Test User Story 1 independently — feed winning board state, verify evaluation score
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → The engine evaluates board states (MVP!)
3. Add User Story 2 → Test independently → The engine generates legal moves and branches correctly
4. Polish → Documentation, type safety, coverage gates
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers/agents:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Agent A**: User Story 1 (Board State Evaluation)
   - **Agent B**: User Story 2 (Move Generation)
3. Stories complete and integrate independently
4. T041 bridges the two at the end

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD-first per Quality Mandates)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Both US1 and US2 are P1 priority — US1 is sequenced first because US2 (move generation) provides branches for US1's search tree, but US1 can use placeholder branching initially
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
