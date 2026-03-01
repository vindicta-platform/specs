# Phase 0: Research & Architecture Decisions (FEAT-044)

## 1. MCTS Arena Allocator in Python

**Context**: Python's garbage collector can cause non-deterministic pauses, and creating thousands of `SearchNode` objects dynamically per 5-second search introduces severe performance and memory fragmentation overhead. We must comply with the "Pre-allocated fixed memory buffer" clarification constraint.

**Decision**: Implement a pseudo-arena allocator using pre-allocated NumPy structured arrays. Each `SearchNode` is stored as a row in a contiguous NumPy array with dtype:

```python
SEARCH_NODE_DTYPE = np.dtype([
    ('id', np.int32),
    ('parent_id', np.int32),       # -1 = root
    ('children', np.int32, (64,)), # max 64 children per node
    ('child_count', np.int8),
    ('state_hash', np.uint64),     # Zobrist hash
    ('visits', np.int32),
    ('value_sum', np.float32),
    ('is_terminal', np.bool_),
    ('depth', np.int8),
])
# ~292 bytes per node
```

**Arena Sizing**: Default 512MB buffer → ~1,750,000 nodes capacity. At 90% fill (1,575,000 nodes) the engine stops expanding and applies visit-based eviction (nodes with fewest visits are reclaimed first). At 100% capacity, the engine returns the best result found so far and sets `MCTSResult.arena_exhausted = True`.

**Root Parallelism Memory**: With Root Parallelism (4 threads), each thread receives its own arena slice: `512MB / 4 = 128MB per thread` (~437,000 nodes each). This fits within the 4GB container limit with headroom for GameState copies and Python overhead.

**Rationale**: Ensures deterministic memory consumption and avoids out-of-memory (OOM) crashes by strictly bounding node count to the arena's length.

**Note on COW vs Pool Coexistence**: Copy-on-write (COW) immutability (from data-model.md) applies to `GameState` objects — each tree expansion creates a new, immutable snapshot of the board. Arena pooling applies to `SearchNode` structural metadata (visit counts, child pointers, hashes). These are separate concerns: `GameState` is never mutated in-place, while `SearchNode` slots are reused from the pre-allocated pool. `SearchNode` fields like `visits` and `value_sum` are updated in-place during backpropagation since they are pool-managed structural counters, not domain state.

**Alternatives considered**:
- Native Python GC instantiation: Rejected due to OOM risk and GC jitter.
- C++ Extension bindings: High maintenance overhead; deferred unless Python pooling fails performance targets.

## 2. Invalid Move Handling & `clamp_move` Proximity Metric

**Context**: Clarification Q3 states: "First attempt to map/clamp to the closest legal equivalent to preserve memory/token context. If unresolvable, issue a hard failure trace."

**Decision**: The generator will include a `clamp_move(invalid_move, legal_moves, board_state) -> valid_move | None` function.

**Proximity definition**: "Closest legal equivalent" is defined as the legal move that minimizes a weighted distance function. The weights are configured via a fail-fast Pydantic model (`ProximityScoreConfig`) that guarantees they always sum to 1.0 at construction time:

```python
from pydantic import ConfigDict, Field, model_validator
import math

class ProximityScoreConfig(VindictaModel):
    # Lock this down! No monkey-patching fields later.
    model_config = ConfigDict(
        frozen=True,      # Makes it immutable (like a real data structure)
        extra='forbid',   # Rejects random keys in your config files
        strict=True       # Forces floats to be floats (no "1" instead of "1.0")
    )

    spatial_weight: float = Field(default=0.5, ge=0.0, le=1.0)
    phase_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    action_type_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    hard_fail_threshold: float = Field(default=0.8, gt=0.0, le=1.0)

    @model_validator(mode="after")
    def _validate_integrity(self) -> "ProximityScoreConfig":
        # Python's floating point math is a mess, so we still need this...
        total = self.spatial_weight + self.phase_weight + self.action_type_weight
        if not math.isclose(total, 1.0, abs_tol=1e-9):
            raise ValueError(f"Weights must sum to 1.0 (got {total:f})")
        return self

def proximity_score(invalid_move, candidate_legal_move, cfg: ProximityScoreConfig) -> float:
    """Lower is closer. 0.0 = exact match."""
    return (
        cfg.spatial_weight * spatial_distance(invalid_move.target, candidate_legal_move.target) +
        cfg.phase_weight * phase_match_penalty(invalid_move.phase, candidate_legal_move.phase) +
        cfg.action_type_weight * action_type_penalty(invalid_move.type, candidate_legal_move.type)
    )
```

**Implementation**: See `vindicta_engine/ai/mcts_config.py` for the full model with type annotations.


- Spatial: Euclidean distance between target coordinates, normalized to board diagonal.
- Phase: 0 if same phase, 1.0 if different.
- Action Type: 0 if same (move→move), 0.5 if related (shoot→overwatch), 1.0 unrelated.

If all candidates score > 0.8 threshold, return `None` (hard fail). Upon hard fail, an exception `InvalidMoveExecutionTrace` is raised, triggering the observability layer.

**Rationale**: Directly satisfies user requirement with a deterministic, testable proximity metric.

## 3. Observability & Tracing (OpenTelemetry)

**Context**: Clarification Q2 requested configurable trace levels (None, Basic Stats, PV, Full Tree).

**Decision**: Use a `MCTSTracer` class that wraps OpenTelemetry's OTLP exporter for structured spans.

**Interface**:

```python
class MCTSTraceLevel(str, Enum):
    NONE = "none"
    BASIC = "basic"       # nodes_visited, cache_hits, time_elapsed
    PV = "pv"             # + principal variation list
    FULL = "full"         # + complete arena buffer dump as JSON lines

class MCTSTracer:
    def __init__(self, level: MCTSTraceLevel, otel_endpoint: str | None = None):
        """Initialize tracer. If otel_endpoint is None, uses structured JSON logs."""
        ...

    def start_search_span(self, root_state_hash: str) -> Span: ...
    def record_node_expansion(self, node_id: int, depth: int) -> None: ...
    def record_pv(self, pv: list[str]) -> None: ...
    def finalize(self, result: MCTSResult) -> None: ...
```

**FULL trace retention**: Tree dumps at FULL level are written to ephemeral storage and retained for **7 days** before automatic cleanup via a scheduled `cron` task (or container TTL policy). Max dump size capped at **50MB** per request to prevent disk exhaustion.

**Metric Attachment**: NPS and cache_hit_ratio are attached as span attributes (OTLP), enabling per-request performance analysis in Grafana/Jaeger.

**Rationale**: Provides flexible debugging paths without burdening the standard fast-path execution. OTel standardization aligns with `vindicta-foundation` observability strategy.

## 4. Zobrist Hashing for Transposition Tables

**Context**: Transposition tables require a fast, collision-resistant hashing scheme for identifying duplicate board states reached via different move orders.

**Decision**: Use Zobrist Hashing with pre-generated 64-bit random constants.

**Generation Strategy**:
```python
# Generated once at module load, seeded deterministically for reproducibility
ZOBRIST_SEED = 0xDEADBEEF_44000000  # Feature-specific seed
rng = np.random.Generator(np.random.PCG64(ZOBRIST_SEED))

# Constants for: unit_type × position_bucket × status_flag
ZOBRIST_UNIT_TYPE = rng.integers(0, 2**64, size=(MAX_UNIT_TYPES,), dtype=np.uint64)
ZOBRIST_POSITION = rng.integers(0, 2**64, size=(POSITION_BUCKETS,), dtype=np.uint64)
ZOBRIST_STATUS = rng.integers(0, 2**64, size=(MAX_STATUS_FLAGS,), dtype=np.uint64)
ZOBRIST_TURN = rng.integers(0, 2**64, size=(6,), dtype=np.uint64)  # turns 0-5
ZOBRIST_PLAYER = rng.integers(0, 2**64, size=(2,), dtype=np.uint64)
```

**Collision Handling**: On hash collision (same `state_hash`, different actual state), the node is treated as a new unique node. A `collision_count` metric is tracked per search and logged at BASIC trace level. If collision rate exceeds 0.01%, a warning is emitted.

**Cache Hit Ratio Target**: ≥15% transposition hits per search session at Depth 3 (based on chess engine benchmarks, adjusted for 40k's lower repetition rate). Below 10% triggers a diagnostic warning.

## 5. Static Evaluation Heuristic Weights

**Context**: The engine needs a deterministic evaluation function when it reaches a leaf node (Depth 3 or time-limited cutoff).

**Decision**: Balanced heuristic with initial defaults, loaded via remote config (`VindictaModel`-based `HeuristicConfig`):

```python
class HeuristicConfig(VindictaModel):
    """Remote-configurable heuristic weights. Inherits VindictaModel for serialization."""
    vp_weight: float = 0.40          # Victory Point differential
    material_weight: float = 0.30    # Remaining wounds / points value
    control_weight: float = 0.30     # Objective marker proximity + OC
    turn_scaling: bool = True        # VP weight increases linearly per turn
    discount_factor: float = 0.95    # Exponential decay per ply depth
```

**Turn Scaling**: When enabled, VP weight at Turn T is: `vp_weight * (1 + 0.1 * T)`, capped at 0.60. Material weight adjusts proportionally downward.

**Rationale**: Balanced approach prevents "passive objective holding" and "pointless bloodlust" extremes. Remote config allows A/B testing without code changes.

## 6. Undo/Rollback Logic for State Transitions

**Context**: The extended clarification (Q52) recommends Delta-based "Undo" logic for performance rather than full GameState cloning.

**Decision**: Implement a `MoveStack` that records deltas:

```python
@dataclass
class MoveDelta:
    """Reversible state change produced by applying a single move."""
    unit_id: str
    field: str                      # e.g., "position", "state_flags", "vp_scores"
    old_value: Any
    new_value: Any

class MoveStack:
    def __init__(self, max_depth: int = 10):
        self._stack: list[list[MoveDelta]] = []

    def push(self, deltas: list[MoveDelta]) -> None: ...
    def pop_and_undo(self, game_state: GameState) -> None: ...
    def depth(self) -> int: ...
```

**Compatibility with Arena**: The arena allocator manages `SearchNode` storage. `GameState` mutation uses the `MoveStack` for in-place apply/undo. This avoids copy-on-write overhead while maintaining determinism (undo is mandatory before backpropagation).

**Note**: The `data-model.md` states "Modified immutably (copy-on-write)." This is updated: the *external API* preserves immutability guarantees (callers never see mutated states), but *internally* the search uses delta-based undo for performance. The `MoveStack` restores state before any node result is returned.

## 7. Entropy Buffer Mock Strategy

**Context**: Heavy unit testing requires deterministic mocking of the Entropy Buffer for reproducible tree expansion tests.

**Decision**: Use **Static Distribution JSON fixtures**:

```text
tests/fixtures/entropy/
├── charge_9inch.json     # { "success_prob": 0.2778, "distribution": [0, 0, 0, 0.028, 0.056, ...] }
├── bolter_volley_t4.json # 10 S4 AP0 shots into T4 Sv3+
├── melta_t8.json         # 2 S9 AP-4 D6 shots into T8 Sv2+
└── manifest.json         # Index of all fixtures with metadata
```

Each fixture contains a full probability distribution captured from the real Entropy Buffer. In tests, `MockEntropyBuffer` loads these fixtures and returns deterministic values based on a seeded index:

```python
class MockEntropyBuffer:
    def __init__(self, fixture_dir: Path, seed: int = 42):
        self._fixtures = load_fixtures(fixture_dir)
        self._rng = np.random.Generator(np.random.PCG64(seed))

    def query(self, attack_profile: AttackProfile) -> float:
        fixture = self._fixtures[attack_profile.key]
        return self._rng.choice(fixture["distribution"], p=fixture["weights"])
```

**Rationale**: Real data snapshots ensure the math logic handles "swingy" edge cases (e.g., mortal wound spikes) correctly, unlike simplified Gaussian mocks.

## 8. Performance Targets & NPS Budget

**Context**: SC-001 requires Depth 3 in 5 seconds. We need to quantify the Nodes-Per-Second (NPS) target.

**Branching Factor Analysis** (40k with cluster-based movement + pruning):
- Movement: ~8 meaningful positions per unit
- Shooting: ~4 target priority options per unit
- Charge: ~3 options (charge, don't, overwatch)
- With progressive unpruning, effective branching factor: **~15-25 moves per node**

**NPS Target**:
- Worst case Depth 3 tree: 25^3 = 15,625 nodes
- With pruning + transpositions: ~5,000-8,000 unique nodes
- Required NPS: **≥2,000 nodes/second** (gives 10,000 nodes in 5s with safety margin)
- Target NPS with NumPy vectorization: **5,000+ nodes/second**

**Adaptive Time Budget**:
- Reserve 250ms safety buffer (4,750ms effective search time)
- Check `time.monotonic()` every 100 node expansions
- If 90% of budget consumed: stop deepening, return best result at current depth

**Hardware Baseline** ("standard hardware"):
- **CPU**: 4-core x86_64 or ARM64, ≥2.5 GHz (e.g., AWS t3.medium / Graviton3 equivalent)
- **RAM**: 4GB container limit
- **No GPU**: CPU-only evaluation

## 9. Concurrent Evaluation & Thread Safety

**Context**: Multiple `evaluate_state` calls may arrive simultaneously. Root Parallelism requires clear thread-safety boundaries.

**Decision**:
- Each `MCTSEngine` instance owns **one arena buffer** and is **NOT thread-safe** internally.
- Concurrency is handled at the **service layer**: each incoming request gets its own `MCTSEngine` instance (or is queued to a worker pool of pre-initialized engines).
- Root Parallelism (4 threads) operates **within** a single `evaluate_state` call using `multiprocessing.Pool` (avoids GIL). Each worker gets a slice of the arena.

**Determinism Guarantee**: Root Parallelism produces deterministic results by:
1. Splitting the arena into N fixed slices (not random).
2. Merging results by selecting the child with the highest visit count across all workers.
3. Using the same RNG seed per worker (worker_seed = base_seed + worker_id).

## 10. Edge Case Enumeration

**Context**: SC-002 requires "100% of defined edge cases" validated. The exhaustive list must be enumerated.

**Defined Edge Cases for Move Generator** (SC-002 scope):

| ID | Edge Case | Expected Behavior |
|----|-----------|-------------------|
| EC-001 | Unit in Engagement Range | Only generates: Fall Back, Remain Stationary, Fight |
| EC-002 | Deep Strike arrival (Turn 1) | Blocked: no Deep Strike on Turn 1 |
| EC-003 | Deep Strike placement (<9" from enemy) | Rejected: minimum distance violation |
| EC-004 | Unit with 0 wounds remaining | No moves generated (destroyed) |
| EC-005 | Aircraft movement (minimum move) | Must move minimum distance or leave board |
| EC-006 | Transport embarkation (capacity) | Rejected if transport at max capacity |
| EC-007 | Heroic Intervention declaration | Only valid during opponent's Charge phase |
| EC-008 | Falling Back through enemy models | Requires Fly keyword or specific ability |
| EC-009 | Shooting into Engagement Range | Only models with Pistol keyword may shoot |
| EC-010 | Battle-shock effects on OC | Unit OC reduced to 0, affects objective control |
| EC-011 | CP usage exceeds pool | Stratagem rejected |
| EC-012 | Target out of weapon range | Shooting action rejected |
| EC-013 | Charge through Engagement Range | Charge path blocked by intervening enemy |
| EC-014 | Turn 5 end-state (game over) | Terminal node, no further moves generated |
| EC-015 | Empty board (all units destroyed) | Terminal node with auto-loss evaluation |

**Total**: 15 defined edge cases. SC-002 "100%" = all 15 passing.

## 11. GameState Input Validation & Security

**Context**: Maliciously crafted payloads must not crash or hang the engine.

**Decision**:
- **Max payload size**: 2MB for JSON (reject with HTTP 413 at gateway)
- **Max nested depth**: 10 levels (enforced by `pydantic` model validators)
- **Max units per state**: 200 (reject states with more)
- **Max turns**: 1-5 (reject values outside range)
- **Timeout enforcement**: Dual (engine internal `time.monotonic()` + external gateway 6-second hard kill)
- **Rate limiting**: Tied to `vindicta-economy` Gas Tank balance (no balance = 429 Too Many Requests)

## 12. Entropy Buffer Interface Contract

**Context**: FR-003 requires interfacing with the Entropy Buffer, but the contract is not yet defined.

**Decision**: The Entropy Buffer provides a **stub interface** for this foundation release:

```python
class EntropyBufferProtocol(Protocol):
    def expected_value(self, attack: AttackProfile) -> float:
        """Returns the expected wounds dealt for the given attack profile."""
        ...

    def sample_outcome(self, attack: AttackProfile, seed: int) -> float:
        """Returns a sampled outcome from the statistical distribution."""
        ...

@dataclass
class AttackProfile:
    num_attacks: int
    skill: int          # e.g., 3 for BS/WS 3+
    strength: int
    toughness: int
    ap: int
    damage: str         # e.g., "D6", "2", "D3+1"
    save: int
    invuln: int | None
    feel_no_pain: int | None
    reroll_hits: bool
    reroll_wounds: bool
```

**Availability**: For this foundation milestone, a `StubEntropyBuffer` implementation will be provided that uses pre-computed lookup tables. The full `vindicta-foundation` Entropy Buffer is a future dependency.

## 13. Documentation Architecture (FR-007)

**Context**: FR-007 requires architecture documentation in `docs/architecture/mcts_engine.md`.

**Required Sections**:
1. **Overview** — Purpose, position in the Vindicta ecosystem
2. **Architecture Diagram** — C4 Component-level showing Engine ↔ Foundation ↔ Oracle
3. **Arena Allocator Internals** — Memory layout, sizing, eviction strategy
4. **Heuristic Tuning Guide** — Weight descriptions, config format, A/B testing instructions
5. **Observability** — Trace levels, OTel setup, retention policy
6. **Performance Benchmarks** — NPS baselines, hardware requirements
7. **Edge Case Reference** — Link to EC-001 through EC-015 table

**Pass/Fail Criteria**: Documentation is "complete" when all 7 sections contain ≥3 sentences of substantive content and at least one code example or diagram each.
