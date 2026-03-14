# Quality Assurance Checklist: MCTS Engine Foundation (FEAT-044)

**Purpose**: Validate the strictness, clarity, and completeness of the MCTS Engine requirements and contracts before and during implementation.
**Audience**: Implementation Author & Peer/QA Reviewers
**Focus**: Internal Engine Core + Ecosystem Integration (Strict Non-Functional Gates)

## 1. Engine Core & Data Model [Completeness & Clarity]

- [x] CHK001 - Is the serialization format and boundary constraint for `GameState` perfectly unambiguous? [Clarity, Spec §FR-001] → **Resolved**: Plan defines Protobuf for wire, Pydantic internally; Research §11 defines payload limits.
- [x] CHK002 - Are the copy-on-write immutability constraints for state transitions documented? [Completeness, Data Model] → **Resolved**: Research §6 clarifies: external immutability preserved, internal delta-based undo for performance.
- [x] CHK003 - Is the exact mathematical hashing algorithm for transpose tables (`state_hash`) specified? [Ambiguity, Data Model] → **Resolved**: Research §4 defines Zobrist Hashing with PCG64-seeded 64-bit constants, collision handling, and hit ratio targets.
- [x] CHK004 - Are the exact heuristics weighting ratios (VP vs Material vs Positioning) defined? [Gap, Ext. Clarifications Q21] → **Resolved**: Research §5 defines VP=0.40, Material=0.30, Control=0.30 via `HeuristicConfig(VindictaModel)`.

## 2. Memory & Performance constraints [Measurability & Coverage]

- [x] CHK005 - Is the maximum allowed size of the pre-allocated fixed memory buffer explicitly quantified? [Measurability, Spec §FR-004] → **Resolved**: 512MB default, ~1.75M nodes, configurable via `MCTSEngine(memory_limit_mb=512)`.
- [x] CHK006 - Is the behavior defining what happens *when the arena fills up* strictly specified? [Completeness, Plan Phase 0] → **Resolved**: Research §1: 90% = stop expanding + visit-based eviction; 100% = return best + `arena_exhausted` flag.
- [x] CHK007 - Is the 5-second depth 3 evaluation constraint bound to a specific hardware baseline? [Ambiguity, Spec §SC-001] → **Resolved**: Plan defines "Standard Hardware" = 4-core ≥2.5GHz, 4GB RAM, no GPU.
- [x] CHK008 - Are rollback or safe-failure recovery requirements defined if the execution loop panics? [Coverage, Exception Flow] → **Resolved**: Research §6 MoveStack provides undo; Research §10 references Prune & Log strategy for engine panics.

## 3. Move Generation & Edge Cases [Coverage & Consistency]

- [x] CHK009 - Are all scenarios concerning the engine's reaction to "Fail States" addressed? [Coverage, Ext. Clarifications Q10] → **Resolved**: Research §10 EC table covers charge failures, Deep Strike blocks, capacity limits, etc.
- [x] CHK010 - Is the mapping of "invalid moves" to "closest equivalent" clearly defined? [Ambiguity, Spec §Edge Cases] → **Resolved**: Research §2 defines weighted proximity function with spatial/phase/action_type components and 0.8 hard threshold.
- [x] CHK011 - Are the requirements for infinite looping board state detection explicitly defined? [Completeness, Spec §Edge Cases] → **Resolved**: Research §4 Zobrist hashing detects repeated states via transposition tables; Research §8 adaptive time budget prevents infinite loops.
- [x] CHK012 - Do the move generator success criteria explicitly define how many edge cases make up "100%"? [Measurability, Spec §SC-002] → **Resolved**: Research §10 enumerates 15 edge cases (EC-001 through EC-015). 100% = all 15 passing.

## 4. Integration & Extensibility [Completeness & Consistency]

- [ ] CHK013 - Are the data contracts between `MCTSEngine` and `vindicta-oracle` documented for rule query fallbacks? [Gap, Ext. Clarifications Q56] → **Deferred**: Oracle integration is out of scope for MCTS foundation (Plan §Dependencies).
- [x] CHK014 - Is the synchronization and integration mechanism with the `Entropy Buffer` defined with exact timing expectations? [Clarity, Spec §FR-003] → **Resolved**: Research §12 defines `EntropyBufferProtocol` (synchronous calls); Research §7 defines mock strategy with pre-cached fixtures.
- [ ] CHK015 - Does the specification detail how the `MCTSResult` translates back into standard Warscribe notation? [Gap, Ext. Clarifications Q71] → **Deferred**: Warscribe encoding is handled by a separate service (per extended clarification Q71 Option B).
- [x] CHK016 - Are the metric reporting formats (for OpenTelemetry) explicitly defined for the "Configurable trace levels"? [Completeness, Spec §FR-005] → **Resolved**: Research §3 defines `MCTSTracer` interface with OTel span attributes for NPS and cache_hit_ratio.

## 5. Security & Isolation [Non-Functional Requirements]

- [x] CHK017 - Are payload sanitization limits specified to prevent infinite JSON parsing loops? [Coverage, Ext. Clarifications Q91] → **Resolved**: Research §11 defines 2MB JSON / 512KB Protobuf, max 10 nesting levels, pydantic strict validators.
- [x] CHK018 - Are query rate limiting constraints outlined to prevent brute-forcing? [Gap, Ext. Clarifications Q95] → **Resolved**: Research §11 specifies rate limiting tied to `vindicta-economy` Gas Tank balance (no balance = 429).
