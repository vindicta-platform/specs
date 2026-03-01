# Technical Design Quality Checklist: MCTS Engine Foundation (FEAT-044)

**Purpose**: Validation of technical architecture decisions and implementation readiness for the MCTS "Stockfish" Core.
**Created**: 2026-02-28
**Audience**: Lead Architect & Implementation Swarm
**Scope**: Technical Design & Architectural Consistency (Spec, Plan, Extended Clarifications)

## Decision Consistency & Alignment

- [x] CHK001 - Does the selection of **NumPy Arrays** (Q1) align with the Python 3.12 `uv` workspace performance requirements in the Plan? [Consistency, Clarification §1.1] → **Resolved**: Plan confirms NumPy structured arrays; Research §1 defines dtype schema (~292 bytes/node).
- [x] CHK002 - Does **Root Parallelism** (Q31) with 4-8 threads (Q33) fit within the **4GB RAM limit** (Q47) when multiplying the arena allocator's size by thread count? [Consistency, Gap] → **Resolved**: Research §1 specifies 512MB/4 threads = 128MB/thread; Plan confirms 4GB container limit with headroom.
- [x] CHK003 - Is **Phase-Sequential** action segmentation (Q7) consistent with the **Depth 3 search limit**? [Consistency, Clarification §2.7] → **Resolved**: Plan defines Depth 3 as "3 full-ply" where each ply = one complete phase-sequential action set, not one sub-phase.
- [x] CHK004 - Does the **JSON** serialization choice (Q3) align with the `GameState` Pydantic models defined in the Data Model? [Consistency, Clarification §1.3] → **Resolved**: Pydantic models use standard JSON serialization; removing Protobuf to adhere to YAGNI.
- [x] CHK005 - Is the **Standard UCT1** (Q11) decision consistent with the "Aggressive Pruning" requirement for 40k's high branching factor? [Consistency, Clarification §3.11] → **Resolved**: Research §8 confirms UCT1 + Progressive Unpruning + Forward Pruning as complementary (not conflicting) strategies.
- [x] CHK006 - Do the **Static Aura Flags** (Q5) account for dynamic state changes within the 5-second search window? [Consistency, Clarification §1.5] → **Resolved**: Research §6 Undo/Rollback logic handles state transitions; aura flags are part of the snapshot and don't change during internal search.

## Implementation Completeness (Task Readiness)

- [x] CHK007 - Is the **NumPy struct array schema** (fields, dtypes) explicitly defined for `GameState` transfer? [Gap, Clarification §1.1] → **Resolved**: Research §1 defines `SEARCH_NODE_DTYPE` with exact field dtypes (int32, float32, uint64, bool).
- [x] CHK008 - Are the **Zobrist Hash constants** or generation strategy defined for the 40k board state? [Gap, Clarification §3.14] → **Resolved**: Research §4 defines full Zobrist strategy with PCG64-seeded constants for unit_type, position, status, turn, and player.
- [x] CHK009 - Is the **JSON schema definition** for the Engine API response (MCTSResult) specified? [Gap, Clarification §1.3] → **Resolved**: JSON schema derived automatically from Pydantic models; removing Protobuf to adhere to YAGNI.
- [x] CHK010 - Are the **Static Evaluation Heuristic weights** (VP, Material, Control) quantified with initial default values? [Gap, Clarification §5.21] → **Resolved**: Research §5 defines VP=0.40, Material=0.30, Control=0.30 with turn scaling formula.
- [x] CHK011 - Does the `MCTSTracer` class (Research.md) have a defined interface for the **OpenTelemetry (OTLP)** export requested in Q41? [Gap, Research §3] → **Resolved**: Research §3 defines full `MCTSTracer` interface with `start_search_span`, `record_node_expansion`, `record_pv`, `finalize` methods.
- [x] CHK012 - Is the **"Undo" (Rollback) logic** interface defined for the `GameState` transitions to support backpropagation? [Gap, Clarification §11.52] → **Resolved**: Research §6 defines `MoveStack` + `MoveDelta` dataclass with push/pop_and_undo interface.

## Hard Metrics & Performance Requirements

- [x] CHK013 - Is there a specific **Nodes-Per-Second (NPS) target** required to reliably hit Depth 3 in 5 seconds across 40k's branching factor? [Measurability, Spec §SC-001] → **Resolved**: Research §8 defines ≥2,000 NPS minimum, ≥5,000 target, with branching factor analysis (25^3 worst case).
- [x] CHK014 - Is "Fast attribute access" for NumPy quantified with a **micro-latency threshold** (e.g., <100ns per lookup)? [Clarity, Clarification §1.1] → **Resolved**: Implicit in NPS target; 5,000 NPS with ~292 bytes/node implies <200μs per node including all field access.
- [x] CHK015 - Is the **Adaptive time-slice** (Q26) defined with specific safety buffers (e.g., 500ms overhead)? [Clarity, Clarification §6.26] → **Resolved**: Research §8 specifies 250ms safety buffer, check every 100 nodes, stop at 90% budget consumption.
- [x] CHK016 - Is the **cache hit ratio target** specified for the transposition tables to ensure depth goals are met? [Measurability, Gap] → **Resolved**: Research §4 defines ≥15% hit ratio target, <10% triggers diagnostic warning.
- [x] CHK017 - Are **max payload size limits** for GameState JSON quantified for sanitization? [Security, Clarification §19.91] → **Resolved**: Research §11 specifies 2MB JSON, max 10 nesting levels, max 200 units.

## Architectural Integrity (Constitution)

- [x] CHK018 - Does the **Root Parallelism** implementation guarantee **100% Determinism** (Q35/Q86) mandated by the Constitution? [Consistency, Clarification §7.35] → **Resolved**: Research §9 defines fixed arena slices + deterministic seed per worker (base_seed + worker_id) + visit-count merge.
- [x] CHK019 - Are the **Rule Erratas** weights (Q53) structured to inherit from `VindictaModel` for remote config compatibility? [Consistency, Clarification §11.53] → **Resolved**: Research §5 defines `HeuristicConfig(VindictaModel)` with remote-configurable fields.
- [x] CHK020 - Does the **Node Count billing** (Q67) have a defined "Price Per Node" schema in the economy requirements? [Gap, Clarification §14.67] → **Deferred**: Engine only *returns* `nodes_visited`; pricing schema is `vindicta-economy`'s responsibility (Plan §Dependencies).

## Swarm Readiness (Task Extraction)

- [x] CHK021 - Are implementation tasks for **Cython/Numba Compiled subsets** (Q51) included in the planning for the core logic loop? [Gap, Clarification §11.51] → **Resolved**: Plan explicitly defers Cython to "Phase 2" in Dependencies table. Foundation uses direct Python calls.
- [x] CHK022 - Is the **Mocking Strategy** for the Entropy Buffer (Q87) detailed enough for a sub-agent to generate test data snapshots? [Clarity, Clarification §18.87] → **Resolved**: Research §7 defines `MockEntropyBuffer` class, fixture directory structure, JSON schema, and seeded sampling.
- [x] CHK023 - Are the **7-day retention** requirements (Q45) for tree dumps translated into a specific cleanup task? [Completeness, Clarification §9.45] → **Resolved**: Research §3 specifies 7-day retention + 50MB cap per request + cron/TTL cleanup policy.
