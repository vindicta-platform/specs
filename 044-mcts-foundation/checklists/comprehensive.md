# Comprehensive Requirements Quality Checklist: MCTS Engine Foundation (FEAT-044)

**Purpose**: Cross-artifact validation of all requirement quality dimensions after second clarification pass.
**Created**: 2026-02-28
**Audience**: Implementation Author & Peer Reviewers
**Scope**: Full feature directory (spec, plan, research, data-model, contracts)

## Requirement Completeness

- [ ] CHK001 - Are success criteria defined for User Story 2 (Move Generation)? Only US1 has an acceptance scenario with measurable output. [Gap, Spec §US2] → **Open**: Spec needs a measurable SC for move gen (e.g., "generates legal moves for all 15 edge cases in <50ms per unit").
- [x] CHK002 - Are requirements for the `clamp_move` function's proximity metric (what defines "closest legal equivalent") specified? [Gap, Spec §Edge Cases] → **Resolved**: Research §2 defines weighted proximity function (spatial 0.5, phase 0.3, action type 0.2) with 0.8 threshold.
- [x] CHK003 - Is the Entropy Buffer interface contract (expected input/output shapes) documented or referenced? [Gap, Spec §FR-003] → **Resolved**: Research §12 defines `EntropyBufferProtocol` with `expected_value` and `sample_outcome` methods plus `AttackProfile` dataclass.
- [x] CHK004 - Are requirements for `GameState` validation on ingestion (malformed JSON, missing fields) specified? [Gap, Spec §FR-001] → **Resolved**: Research §11 defines max payload 2MB, max depth 10, max 200 units, turn range 1-5.
- [x] CHK005 - Is the documentation deliverable (`docs/architecture/mcts_engine.md`) scoped with required sections or table of contents? [Gap, Spec §FR-007] → **Resolved**: Research §13 defines 7 required sections with pass/fail criteria.
- [x] CHK006 - Are requirements for arena allocator behavior at exactly 100% capacity specified (vs the 90% threshold in research.md)? [Gap, Plan §Research] → **Resolved**: Research §1 now specifies: 90% = stop expanding + eviction; 100% = return best result + set `arena_exhausted` flag.
- [x] CHK007 - Are requirements for `SearchNode.state_hash` collision handling documented? [Gap, Data Model §SearchNode] → **Resolved**: Research §4 defines collision handling: treat as new node, track `collision_count`, warn if >0.01%.
- [ ] CHK008 - Are acceptance scenarios defined for the economy auditing metrics (FR-006)? No user story covers this requirement. [Gap, Spec §FR-006] → **Open**: Spec needs economy-facing acceptance scenario. Plan traces FR-006 to Contract API fields.

## Requirement Clarity

- [x] CHK009 - Is "standard hardware" in SC-001 quantified with specific CPU/RAM/container specs? [Ambiguity, Spec §SC-001] → **Resolved**: Plan defines "Standard Hardware" as 4-core x86_64/ARM64, ≥2.5 GHz, 4GB RAM, no GPU.
- [x] CHK010 - Is "100% of defined edge cases" in SC-002 scoped? The exhaustive list of edge cases is not enumerated. [Ambiguity, Spec §SC-002] → **Resolved**: Research §10 enumerates 15 specific edge cases (EC-001 through EC-015) with expected behaviors.
- [x] CHK011 - Is "depth of 3" consistently defined as 3 full-ply or 3 half-ply across all artifacts? [Ambiguity, Spec §SC-001, Contract §evaluate_state] → **Resolved**: Plan Key Definitions table defines "Depth 3 = 3 full-ply."
- [x] CHK012 - Is `evaluation_score` in the contract defined with a bounded range or is it unbounded? [Ambiguity, Contract §MCTSResult] → **Resolved**: Plan defines "Unbounded float, typically [-10.0, +10.0]. Positive = active player advantage."
- [x] CHK013 - Is "pre-allocated fixed memory buffer" quantified with a default size? [Ambiguity, Spec §FR-004 vs Contract] → **Resolved**: Plan and Research §1 align on 512MB default.
- [x] CHK014 - Is the term "principal variation" formally defined for the 40k simulation domain? [Ambiguity, Spec §FR-001, Contract §MCTSResult] → **Resolved**: Plan defines PV as "ordered sequence of best phase-actions from root to deepest evaluated leaf."

## Requirement Consistency

- [x] CHK015 - Do the `MCTSResult` fields in the contract (`nodes_visited`, `computation_time_ms`) explicitly satisfy FR-006's economy auditing requirement? [Consistency, Spec §FR-006 vs Contract] → **Resolved**: Plan Traceability table maps FR-006 → Contract API fields.
- [x] CHK016 - Does the plan's testing line (`pytest` + `behave`) align with the clarification answer selecting "Heavy Unit Testing" AND the Constitution §III SDD→BDD→TDD mandate? [Consistency, Plan §Technical Context vs Constitution §III] → **Resolved**: Both are required. `pytest` for heavy unit testing (clarification), `behave` for BDD acceptance scenarios (Constitution mandate). Not conflicting — complementary.
- [x] CHK017 - Is `GameState.turn_number` range (1-5) in the data model consistent with 40k game rules? [Consistency, Data Model vs Spec] → **Resolved**: Research §11 enforces turn range 1-5; Research §10 EC-014 handles Turn 5 end-state.
- [x] CHK018 - Does the copy-on-write immutability constraint in the data model align with the arena allocator's pooling strategy? [Consistency, Data Model vs Research §1] → **Resolved**: Research §6 explicitly addresses this: external API preserves immutability, internal search uses delta-based undo.
- [x] CHK019 - Are the four trace levels in research.md consistent with the list in Spec §FR-005? [Consistency, Spec §FR-005 vs Research §3] → **Resolved**: Research §3 defines matching enum: NONE, BASIC, PV, FULL.

## Acceptance Criteria Quality

- [ ] CHK020 - Can the ">90% win probability" in US1's independent test be objectively verified without a reference implementation? [Measurability, Spec §US1] → **Open**: Requires a "Puzzle Suite" (Research §7 mock fixtures provide the data, but acceptance threshold needs a reference board state + expected score).
- [ ] CHK021 - Is "evaluation score (e.g., +4.5)" a concrete acceptance threshold or just an illustrative example? [Measurability, Spec §US1 Acceptance] → **Open**: Currently illustrative. Needs task to define regression puzzle suite with expected score ranges.
- [x] CHK022 - Are pass/fail criteria defined for FR-007's documentation requirement? [Measurability, Spec §FR-007] → **Resolved**: Research §13 defines 7 required sections, each needing ≥3 sentences + 1 code example/diagram.

## Scenario Coverage

- [x] CHK023 - Are requirements defined for concurrent evaluation requests? [Coverage, Gap] → **Resolved**: Research §9 specifies: each instance is NOT thread-safe; concurrency via worker pool of separate instances.
- [x] CHK024 - Are requirements specified for partial search results (engine times out before target depth)? [Coverage, Exception Flow] → **Resolved**: Research §8 specifies: return best result at current depth when 90% budget consumed.
- [x] CHK025 - Are requirements defined for empty board states or games that are already over? [Coverage, Edge Case] → **Resolved**: Research §10 EC-014 (Turn 5 end) and EC-015 (empty board) defined as terminal nodes.
- [x] CHK026 - Are recovery requirements specified if the arena allocator encounters a corrupted node pointer? [Coverage, Exception Flow, Gap] → **Resolved**: Research §1 arena uses NumPy array indices (not pointers); out-of-bounds raises `IndexError`, caught and logged as `arena_corruption` trace event.

## Non-Functional Requirements

- [x] CHK027 - Are latency requirements for individual node expansion steps defined? [Gap, Spec §SC-001] → **Resolved**: Implied by NPS target: ≥2,000 NPS = ≤500μs per node expansion (Research §8).
- [x] CHK028 - Are thread-safety or async-safety requirements for the engine documented? [Gap] → **Resolved**: Research §9 defines engine as NOT thread-safe; concurrency at service layer.
- [x] CHK029 - Are log volume/rotation requirements specified for the FULL trace level? [Gap, Spec §FR-005] → **Resolved**: Research §3 specifies 50MB cap per request, 7-day retention, cron cleanup.
- [x] CHK030 - Are security requirements for GameState input sanitization specified? [Gap] → **Resolved**: Research §11 defines payload limits, nesting depth, unit count, dual timeout enforcement.

## Dependencies & Assumptions

- [x] CHK031 - Is the assumption that `vindicta-foundation` VindictaModel supports arena-style pre-allocation validated? [Assumption, Data Model] → **Resolved**: Research §1 clarifies: VindictaModel is for API contracts only; arena uses raw NumPy arrays internally.
- [x] CHK032 - Is the dependency on the Entropy Buffer API currently available, or future? [Dependency, Spec §FR-003] → **Resolved**: Research §12 + Plan Dependencies table: StubEntropyBuffer for foundation; full buffer is future.
- [x] CHK033 - Are cross-repository build/test dependencies documented? [Dependency, Plan §Structure] → **Resolved**: Plan Dependencies table + build dependency note (uv workspace, foundation before engine).

## Cross-Artifact Traceability

- [x] CHK034 - Does every functional requirement (FR-001 through FR-007) have at least one acceptance scenario or success criterion tracing to it? [Traceability] → **Resolved**: Plan Acceptance Scenario Traceability table maps all 7 FRs.
- [x] CHK035 - Are all data model fields traceable to a specific functional requirement or user story? [Traceability, Data Model] → **Resolved**: All fields serve FR-001 (GameState) or FR-002/FR-004 (SearchNode arena).
