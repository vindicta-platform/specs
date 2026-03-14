# Extended Clarifications: FEAT-044 MCTS Engine Foundation

The following 100 questions span 20 distinct categories regarding the architecture, integration, and operational constraints of the MCTS Engine within the broader `vindicta-platform-testing` ecosystem.

For each, please provide a short answer or select an option to guide the technical planning.

## 1. GameState Representation (Data Model)

1. **Encoding**: How are unit properties and locations explicitly encoded in memory (e.g., bitboards, struct arrays, entity-component)?
   - **Options**:
    - A) Bitboards (High efficiency, requires complex bitmasking logic)
    - B) Typed NumPy Arrays / Struct Arrays (Fast attribute access, easy vectorization)
    - C) Pydantic/VindictaModel classes (High abstraction, slower for high-frequency tree nodes)
   - **Recommended**: Option B - NumPy arrays offer a balance of Python-native readability and near-C performance for state snapshots.

2. **Hidden Information**: Is the board state passed to the MCTS fully observable, or are hidden secondary objectives obfuscated?
   - **Options**:
    - A) Fully Observable (Standard MCTS, simpler implementation)
    - B) Partially Observable (Information Set MCTS, handles fog-of-war/hidden cards)
    - C) Cheating AI (AI sees all, but pretends not to)
   - **Recommended**: Option A - For a foundation layer, perfect information simplifies the search; hidden info can be modeled as "expected value" branches later.

3. **Serialization**: What serialization format is used for network transfer of GameStates (e.g., JSON, Protocol Buffers, FlatBuffers)?
   - **Options**:
    - A) JSON (Human readable, high overhead)
    - B) Protocol Buffers (Compact, fast, typed)
    - C) FlatBuffers (Zero-copy, fastest but more complex schema management)
   - **Recommended**: Option B - Protobuf provides the best middle ground for the `vindicta-platform` microservice mesh.

4. **Terrain**: How is 3D terrain conceptually represented in the mathematical snapshot to calculate line-of-sight efficiently?
   - **Options**:
    - A) Voxel Grid (High precision, memory intensive)
    - B) 2D Heightmap + Obstacle Polygons (Simpler LoS math)
    - C) Abstract Keyword Tags (e.g., "Obscuring") with simplified bounding boxes
   - **Recommended**: Option C - Standardizing on "Obscuring" / "Cover" tags aligns with the core game engine logic rules.

5. **Aura Effects**: Are aura effects computed dynamically during evaluation, or are they statically attached as state flags per unit?
   - **Options**:
    - A) Dynamic (Computed on-demand, always accurate)
    - B) Static Flags (Pre-calculated at start of phase/turn, faster but risk of staleness)
    - C) Incremental (Updated only when a unit moves)
   - **Recommended**: Option B - Statically attaching flags during a "Snapshot Refresh" phase significantly speeds up playout evaluations.

## 2. Move Generation Logic

6. **Laziness**: Are child moves generated lazily (on demand per expanded node) or eagerly (all at once per state)?
   - **Options**:
    - A) Lazy (Lower memory, slower leaf expansion)
    - B) Eager (Faster search, higher memory usage per node)
   - **Recommended**: Option A - For Depth 3+, lazy expansion prevents generating thousands of unused move branches for low-probability nodes.

7. **Compound Actions**: How are compound action sequences (e.g., move, then shoot, then charge) segmented into decision nodes?
   - **Options**:
    - A) Flattened (All permutations are siblings at one depth)
    - B) Phase-Sequential (Move node -> Shoot node -> Charge node)
    - C) Action Bundling (Agents submit an "Entire Turn Plan" as one branch)
   - **Recommended**: Option B - Multi-step sequential nodes better represent the reactive nature of stratagems and dice outcomes.

8. **Measurements**: How does the generator handle continuous distances (e.g., 6" move) in a discrete search tree?
   - **Options**:
    - A) Discretized Grid (Move 1, 2, 3... inches)
    - B) Cardinal Directions (Fixed point navigation)
    - C) Cluster-Based (Only generate moves to "meaningful" objective or cover zones)
   - **Recommended**: Option C - Moving to "points of interest" reduces the branching factor from infinite to manageable.

9. **Stratagems**: Are CP usage and reactive stratagems considered standard "moves" in the tree?
   - **Options**:
    - A) Yes (Full decision tree including resource management)
    - B) No (Stratagems are handled by a separate heuristic "override" layer)
    - C) Dynamic Pruning (Only include critical CP moves like "Interrupt")
   - **Recommended**: Option C - Pruning CP usage to only high-impact actions keeps the breadth manageable.

10. **Fail States**: How are "Fail" scenarios (e.g., a failed 9" charge) mapped to branch continuations?
    - **Options**:
      - A) Stochastic Nodes (Tree branches into "Success" and "Failure" children)
      - B) Weighted Averages (Rollout uses the Entropy Buffer's mean outcome)
      - C) Outcome Sampling (Node represents only the most likely outcome)
    - **Recommended**: Option A - Real branches for success/failure are essential for risk-assessment logic in MCTS.

## 3. MCTS Node Expansion & Selection

11. **UCT Formula**: What variant of the Upper Confidence Bound applied to Trees (UCT) formula will govern node selection?
    - **Options**:
      - A) Standard UCT1 (Exploration vs Exploitation balance)
      - B) PUCT (Predictor + UCB, used in AlphaZero)
      - C) RAVE (Rapid Action Value Estimation)
    - **Recommended**: Option A - Start with Standard UCT1; it is robust and easiest to tune for the foundation.

12. **Playout Strategy**: Does the engine use random heavy rollouts or a heuristic shallow evaluation function for unvisited nodes?
    - **Options**:
      - A) Traditional Rollouts (Simulate game to end - slow in 40k)
      - B) Heuristic Evaluation (Assign score at terminal depth, then backpropagate)
      - C) Hybrid (Short rollout + evaluation)
    - **Recommended**: Option B - Given the complexity of 40k, a professional heuristic score (Stockfish-style) at Depth 3 is more viable than full rollouts.

13. **Progressive Unpruning**: Will the engine implement progressive unpruning for branching factors that are initially too large?
    - **Options**:
      - A) Yes (Gradually add moves as visit count increases)
      - B) No (Evaluate all legal moves from the start)
    - **Recommended**: Option A - Essential for game states with hundreds of possible shooting/movement permutations.

14. **Transpositions**: How are transposition tables (tracking identical board states reached via different move orders) integrated?
    - **Options**:
      - A) Zobrist Hashing (Industry standard for chess/Go)
      - B) State Delta Sets (Compare unit-by-unit differences)
      - C) No Transposition (Re-evaluate identical states independently)
    - **Recommended**: Option A - Zobrist Hashing is mandatory for avoiding redundant computation in iterative deepening.

15. **Reward Discounting**: Is there a discount factor applied to rewards deeper in the tree to favor immediate certainty?
    - **Options**:
      - A) Exponential Decay (Gains far in the future are worth less)
      - B) Discrete Step Penalty (Fixed cost per turn/depth)
      - C) No Discount (Win in 5 turns is same as win in 1)
    - **Recommended**: Option A - Prevents the AI from "shuffling" or delaying a win when an immediate advantage is available.

## 4. Entropy Buffer Integration

16. **Expectation Strategy**: How are results derived from the Entropy Buffer (mean averages vs distribution sampling per rollout)?
    - **Options**:
      - A) Mean Average (Deterministic, fast, but "boring" play)
      - B) Weighted Distribution Sampling (Probabilistic, more realistic)
      - C) Percentile Pruning (Only consider 25th-75th percentile outcomes)
    - **Recommended**: Option B - Sampling from the distribution provides the "swinginess" inherent in 40k that MCTS needs to account for.

17. **Re-rolls**: Are re-rolls (e.g., Command Re-roll) resolved instantly within a buffer query or treated as separate decision branches?
    - **Options**:
      - A) Procedural (Buffer handles re-roll math internally in one call)
      - B) Branching (A re-roll is a separate move node in the tree)
      - C) Heuristic (Add a +X% boost to the initial roll success probability)
    - **Recommended**: Option A - Having the buffer handle re-roll math internally keeps the tree depth from exploding.

18. **Granularity**: What is the granularity of dice expectation requests (per single shot vs aggregate per attack sequence)?
    - **Options**:
      - A) Per Die (Highest precision, extreme latency)
      - B) Per Sequence (e.g., "10 shots at 3+ to hit")
      - C) Per Unit-Phase (Aggregate all attacks from one unit)
    - **Recommended**: Option B - "Per Sequence" is the standard for efficient 40k math engines.

19. **Mortal Wounds**: How are low-probability outlier events (e.g., rolling 6s to wound causing mortal spikes) weighted?
    - **Options**:
      - A) Ignored (Too rare to model)
      - B) Linear Weighting (Include in the average)
      - C) Importance Sampling (Give outliers higher weight during specific phases)
    - **Recommended**: Option B - Linear weighting in the distribution sampling ensures they occur at the correct frequency.

20. **Synchronization**: Does the engine pre-fetch buffer probabilities, or query the buffer synchronously during evaluation?
    - **Options**:
      - A) Synchronous (Simplest, but creates compute bottlenecks)
      - B) Pre-fetch / Cache (Store common roll results in memory)
      - C) Asynchronous (Parallelize buffer calls, process branches when results return)
    - **Recommended**: Option B - Caching the Top 500 most common dice interactions (e.g., 20 S4 shots into T4) is the best performance win.

## 5. Evaluation Heuristics (Static Evaluation)

21. **Scoring Weights**: What is the relative weight ratio between VP lead, Material advantage, and Positional control?
    - **Options**:
      - A) Material Dominant (Kill everything first)
      - B) VP Dominant (Focus strictly on objectives)
      - C) Balanced (40% VP, 30% Material, 30% Control)
    - **Recommended**: Option C - A balanced approach prevents the "passive objective holding" and "pointless bloodlust" extremes.

22. **Dynamic Overrides**: Are these heuristic weights hardcoded, or dynamically loaded via a remote config system?
    - **Options**:
      - A) Hardcoded (Fastest, requires re-build to change)
      - B) Remote Config / JSON (Flexible, easy to A/B test without deployment)
      - C) Agent-Defined (The calling agent passes the weights in the payload)
    - **Recommended**: Option B - Using a remote config (as per project guidelines for `remote_config_master.md`) allows tuning without code changes.

23. **Objective Holding**: How is objective control evaluated if the scoring phase is not immediate?
    - **Options**:
      - A) Sticky Control (Unit is on it now = points eventually)
      - B) Projected Control (Who is likely to have OC on it at the end of the battle round?)
      - C) Distance Weighted (Reward proximity to objective centers)
    - **Recommended**: Option B - Projected control after all phase nodes resolve is the most accurate for 10th Edition.

24. **Phase Scaling**: Does the evaluation function scale its priorities based on the current game turn (e.g., late game values VP higher)?
    - **Options**:
      - A) Yes (Linear scaling of VP weight over 5 turns)
      - B) No (Static evaluation throughout)
    - **Recommended**: Option A - VP is much more valuable on Turn 5 than Turn 1, where material preservation is key.

25. **Secondary Objectives**: How are player-selected secondary objectives factored into the base heuristic score?
    - **Options**:
      - A) Global Heuristic (Add points for "Action" completions)
      - B) Explicit Trackers (Separate logic sub-modules per objective)
      - C) Ignored (AI only cares about Primary/Material)
    - **Recommended**: Option B - Since secondaries are highly specific (e.g., "Behind Enemy Lines"), they require explicit sub-logic.

## 6. Time Management & Search Constraints

26. **Budget Distribution**: How does the engine distribute the 5-second budget across iterative deepening phases?
    - **Options**:
      - A) Fixed % (e.g., 20% for Depth 1, 30% for Depth 2, 50% for Depth 3)
      - B) Adaptive (Stop when time is 90% exhausted regardless of current depth progress)
      - C) Early Exit (Return best move immediately if one line is >95% win prob)
    - **Recommended**: Option B - Adaptive time-slicing ensures we never miss the 5-second hard limit.

27. **Hard Stops**: Is there an asynchronous emergency "hard stop" signal if the evaluation exceeds strictly allowed time?
    - **Options**:
      - A) Yes (Search loop checks `time.time()` every N iterations)
      - B) No (Rely on host OS/Container to kill the process)
    - **Recommended**: Option A - Mandatory for a robust backend engine.

28. **Resumability**: Can an MCTS search tree state be paused and safely resumed across multiple network requests?
    - **Options**:
      - A) Yes (Store the tree in a shared Redis/Cache)
      - B) No (Engine is stateless; a new request starts a new search)
    - **Recommended**: Option B - Statelessness is simpler to scale horizontally.

29. **Time Pools**: Will the engine support variable time pools per player (e.g., blitz vs standard time controls)?
    - **Options**:
      - A) Yes (Engine accepts a `time_budget_ms` parameter)
      - B) No (Global 5-second limit)
    - **Recommended**: Option A - Allows the same engine to power both "Fast Preview" and "Deep Calculation" use cases.

30. **Early Termination**: What happens if the absolute depth limit of 3 is fully exhausted before the 5 seconds are up?
    - **Options**:
      - A) Return Result (Stop and save the computation cost)
      - B) Iterative Deepening (Proceed to Depth 4+ until time runs out)
    - C) Statistical Softening (Use remaining time to run more rollouts on current leaves)
    - **Recommended**: Option B - If time remains, deeper search is always better for accuracy.

## 7. Concurrency & Parallelization

31. **Threading Model**: Does the search employ Root Parallelism, Leaf Parallelism, or Tree Parallelism?
    - **Options**:
      - A) Root Parallelism (Run N independent trees, merge results at end - easiest)
      - B) Tree Parallelism (Multiple threads share one tree - requires locking)
      - C) Leaf Parallelism (Search is serial, but terminal evaluations are parallel)
    - **Recommended**: Option A - Root Parallelism is the most Python-friendly (avoiding GIL issues) and scales well in containerized environments.

32. **Mutex Locks**: If using Tree Parallelism, how are node statistic updates handle concurrency (lock-free vs mutexed)?
    - **Options**:
      - A) Lock-free (Atomic updates using specific CPU instructions - complex in Python)
      - B) Mutexed (Standard locks on node objects)
      - C) Batch Updates (Workers accumulate stats and update the tree in a single-threaded sweep)
    - **Recommended**: Option C - Batching updates minimizes lock contention and provides cleaner trace logs.

33. **Instance Scaling**: What is the maximum target thread count per container instance?
    - **Options**:
      - A) Single-threaded (1 vCPU)
      - B) 4-8 Threads (Standard high-performance container)
      - C) Elastic (Scale based on available machine cores)
    - **Recommended**: Option B - Standardizing on 4-8 threads provides predictable performance for 5-second budgets.

34. **Cache Syncing**: How are transposition tables synchronized across multiple worker threads efficiently?
    - **Options**:
      - A) Shared Memory Hash Table (requires extreme care with Python objects)
      - B) Per-Thread Cache (No sync, higher memory usage)
      - C) Sharded Cache (Divide hash range across workers)
    - **Recommended**: Option C - Sharding reduces collisions and works well with root parallelism.

35. **Determinism vs Speed**: Will thread races be permitted if it increases nodes-per-second, or is strict determinism required?
    - **Options**:
      - A) Strict Determinism (Repeatable results for debugging/testing)
      - B) Asynchronous Racy Updates (Accept small inaccuracies for higher throughput)
    - **Recommended**: Option A - Determinism is a strict requirement for `vindicta-platform` to ensure audit trails and repeatable tests.

## 8. Pruning & Tree Reduction

36. **Forward Pruning**: Is Forward Pruning aggressively applied to moves with historically low immediate payouts?
    - **Options**:
      - A) Yes (Only consider Top N most promising moves)
      - B) No (Trust UCT to naturally ignore bad branches)
    - **Recommended**: Option A - aggressive pruning is necessary for 40k due to the high branching factor (e.g. dozens of targets for one unit).

37. **Alpha-Beta Hybrid**: How exactly are Alpha-Beta pruning bounds integrated within an MCTS framework?
    - **Options**:
      - A) Fixed Bounds (Prune nodes below a hard static score)
      - B) Dynamic Windowing (Use MCTS visit counts to define search "windows")
      - C) No Hybrid (Use pure MCTS)
    - **Recommended**: Option C - Stick to pure MCTS initially; alpha-beta hybrids are mathematically complex to integrate with UCT.

38. **Symmetry**: Does the engine detect and eliminate obviously symmetrical board state permutations?
    - **Options**:
      - A) Automatic (Hash units by relative position rather than absolute ID)
      - B) Manual (Rules engine flags redundant moves)
      - C) Disabled (Accept the overhead)
    - **Recommended**: Option C - Determining symmetry in a complex 3D 40k environment is often more expensive than just searching the Redundant node.

39. **Null Moves**: Are "Null Move" heuristics allowed to test for immediate localized threat detection?
    - **Options**:
      - A) Yes (Test if not moving still results in unit death)
      - B) No (Every unit must declare an action)
    - **Recommended**: Option A - "What if I do nothing?" is a powerful baseline for evaluating threat levels.

40. **Dice Pruning**: How aggressive is the pruning on highly improbable dice combinations (e.g., failing five 2+ armor saves)?
    - **Options**:
      - A) Aggressive (Ignore roll outcomes with <1% probability)
      - B) Balanced (Ignore <0.1% probability)
      - C) Full (Include every possible discrete die combination)
    - **Recommended**: Option A - Pruning extreme outliers keeps the tree representation sane and focused on realistic outcomes.

## 9. Observability, Tracing, and Logging

41. **Trace Format**: What industry-standard format is used for exported traces (OpenTelemetry, JSON logs)?
    - **Options**:
      - A) OpenTelemetry (OTLP) (Native support for Jaeger/Grafana)
      - B) Structured JSON Logs (Easy to pipe to ELK/CloudWatch)
      - C) Custom Binary (Fastest export, requires custom viewer)
    - **Recommended**: Option A - Standardizing on OTel is mandatory for the `vindicta-foundation` observability goals.

42. **PV Export**: Is the Final Principal Variation exported automatically to standard out or dedicated metrics stores?
    - **Options**:
      - A) Stdout (Simple for local dev)
      - B) Metric Store (Prometheus/InfluxDB)
      - C) API Payload (Returned in the search result object)
    - **Recommended**: Option C - The PV is functional data; it belongs in the response payload.

43. **NPS Tracking**: How are nodes-per-second (NPS) and cache-hit metrics aggregated and visualized?
    - **Options**:
      - A) Prometheus Counters (Real-time monitoring)
      - B) Trace Attributes (Per-request granularity)
      - C) Console Logs (Debugging only)
    - **Recommended**: Option B - Attaching NPS to the request trace identifies slow scenarios/board states.

44. **Reproducibility**: Can developers trace and extract the exact random seed used for a specific outlier rollout?
    - **Options**:
      - A) Yes (Random seed is logged per request)
      - B) No (Seeds are transient)
    - **Recommended**: Option A - Essential for fixing "hallucination" bugs where the AI makes a bizarre move.

45. **Artifact Retention**: How long are full memory tree dumps (if Level 4 Trace is enabled) retained on disk?
    - **Options**:
      - A) 1 Hour (Local buffer)
      - B) 7 Days (Standard debug window)
      - C) Not Retained (Live stream only)
    - **Recommended**: Option B - Seven days allows for retroactive post-mortem analysis of failed game sessions.

## 10. Hardware & Resource Limits

46. **Hardware Acceleration**: Are neural network evaluations (if added later) explicitly targeted for CPU or GPU hardware?
    - **Options**:
      - A) CPU Only (Focus on vectorized AVX/SIMD instructions)
      - B) GPU Accelerated (Requires CUDA/ROCm dependencies)
      - C) NPU/Dedicated (Targeting edge AI hardware)
    - **Recommended**: Option A - CPU-only simplifies the container deployment and is sufficient for the foundation's mathematical complexity.

47. **Memory Limits**: What is the default hard RAM limit for the Engine container (e.g., 1GB, 4GB)?
    - **Options**:
      - A) 1GB (Lightweight, high density)
      - B) 4GB (Balanced for large MCTS trees)
      - C) 16GB+ (For professional tournament-grade depth)
    - **Recommended**: Option B - 4GB provides enough space for a massive transposition table and arena allocator.

48. **Eviction Strategy**: How is cache eviction managed when memory constraints are reached (LRU vs Depth-based)?
    - **Options**:
      - A) LRU (Least Recently Used - standard)
      - B) Depth-based (Protect nodes closer to the root)
      - C) Visit-based (Keep nodes with the most statistical weight)
    - **Recommended**: Option C - In MCTS, the nodes with the most visits are the most valuable to retain.

49. **Vectorization**: Does the engine rely on strict SIMD/Vectorization instruction sets for bit computations?
    - **Options**:
      - A) Explicit (Use NumPy/PyTorch internals for vector math)
      - B) Auto-vectorized (Trust Python interpreter/compiler)
      - C) None (Pure Python objects)
    - **Recommended**: Option A - Mandatory for meeting the 5-second depth 3 goal in Python.

50. **CPU Arch**: Will the infrastructure predominantly deploy on ARM64 (AWS Graviton/M-series) or standard x86_64?
    - **Options**:
      - A) ARM64 (Cost effective, modern)
      - B) x86_64 (Broad compatibility)
      - C) Multi-arch (Support both)
    - **Recommended**: Option C - The codebase should be multi-arch, but ARM64 is the preferred production target for cost.

## 11. Integration with `vindicta-engine` (Core Logic)

51. **Logic Duplication**: Does MCTS duplicate `vindicta-engine`'s rules internally for speed, or call the module directly?
    - **Options**:
      - A) Call Directly (Maintainable, slower)
      - B) Compiled Subset (Duplicate critical path logic in Cython/Numba for speed)
      - C) Logic Mapping (MCTS uses a simplified proxy of the full engine)
    - **Recommended**: Option B - Re-implementing the core "Move/Hit/Wound" loop in a high-performance subset is essential for Stockfish-level speed.

52. **State Mutability**: Is `vindicta-engine` structurally stateless enough to support concurrent node expansion without cloning entire domains?
    - **Options**:
      - A) Full Clone (Copy entire GameState object - slow)
      - B) Copy-on-Write (Only clone modified units)
      - C) Delta-based (Apply moves and then "Undo" them to return to parent state)
    - **Recommended**: Option C - "Undo" logic (Rollback) is the preferred industry standard for high-performance search engines.

53. **Rules Erratas**: How are mid-season rule erratas dynamically injected into the active search heuristics?
    - **Options**:
      - A) Factory Pattern (Inject new logic classes)
      - B) Parameterized Constants (Change math weights via config)
      - C) Code Deployment (Hard update the module)
    - **Recommended**: Option B - Most erratas (e.g., points changes, AP caps) can be handled as weights in the evaluation function.

54. **Panic Handling**: What happens to a tree branch if `vindicta-engine` unexpectedly panics or throws an exception during rollout?
    - **Options**:
      - A) Prune & Log (Discard the branch, mark moves as invalid)
      - B) Hard Fail (Kill the search session)
      - C) Retry (Re-initialize state and try same move again)
    - **Recommended**: Option A - Robust systems should prune the segment and continue searching healthy branches.

55. **Versioning Cycle**: How tightly coupled is the MCTS release cycle to `vindicta-engine` version updates?
    - **Options**:
      - A) Locked (Must match major.minor version)
      - B) Decoupled (MCTS implements a standard interface)
    - **Recommended**: Option A - MCTS logic is inextricably tied to the exact rules version and point values.

## 12. Integration with `vindicta-oracle` (RAG / Rules)

56. **Live Queries**: Can the MCTS proactively query the Oracle during evaluation for unknown edge case rulings?
    - **Options**:
      - A) Yes (Synchronous RAG during search - extremely slow)
      - B) No (Oracle is used only for pre-processing or post-search logging)
      - C) Pre-cached (Oracle pre-generates common ruling summaries into the engine)
    - **Recommended**: Option C - Oracle should bake "Rule Interpretations" into the Engine's move generator at startup.

57. **Pre-Validation**: Does the Oracle pre-validate the root node board state before an expensive search is initialized?
    - **Options**:
      - A) Yes (Ensure the starting position is legal)
      - B) No (Search anyway; illegal states will naturally have low win % or errors)
    - **Recommended**: Option A - Prevents "Garbage In, Garbage Out" scenarios.

58. **Illegality Penalties**: If the Oracle flags a strategy sequence as "illegal", is the branch pruned or heavily mathematically penalized?
    - **Options**:
      - A) Pruned (Immediate removal)
      - B) Penalized (Give it a -10,000 score, but keep it in the tree for trace visibility)
    - **Recommended**: Option B - Keeping the branch with a massive penalty allows developers to see *why* the AI "wanted" to cheat.

59. **Caching**: Are Oracle queries cached globally per engine instance or flushed after every search?
    - **Options**:
      - A) Persistent (Global cache across all matches)
      - B) Session-scoped (Flushed after turn ends)
      - C) None
    - **Recommended**: Option A - Rules donor change; keep them cached for the life of the container.

60. **Blame Attribution**: How does MCTS attribute a win/loss specifically to a complex Oracle rules interpretation in its logs?
    - **Options**:
      - A) Specific Trace Tags (e.g. `ruling_id: 1234`)
      - B) Custom Log Level (Oracle Impact Level)
      - C) Narrative summary
    - **Recommended**: Option A - Allows automated analysis of which "Rules Interpretations" lead to the highest win rates.

## 13. Integration with `Vindicta-Agents`

61. **Personality Bias**: Do Agents pass "personality" parameter weights into the MCTS to bias certain playstyles (aggressive vs defensive)?
    - **Options**:
      - A) Yes (Heuristic weights are passed in the request header)
      - B) No (MCTS is always "Optimal"; Agents decide which optimal move to take)
      - C) Mixed (Base weights are fixed, but agents can suggest "Focus Units")
    - **Recommended**: Option A - Different agent personalities (e.g. World Eaters vs Tau) require fundamentally different exploration biases to feel "correct".

62. **Polling Frequency**: How often are Agents expected or allowed to poll the Engine for move suggestions?
    - **Options**:
      - A) Once per turn (Full plan generation)
      - B) Once per phase (Movement, Shooting, etc.)
      - C) Reactive (Whenever the GameState changes)
    - **Recommended**: Option B - Phase-level polling allows for adjustments based on actual dice results without overwhelming the engine.

63. **Partial Trees**: Can Agents request partial tree subsets (e.g., "what if I only move unit X") rather than the global best move?
    - **Options**:
      - A) Yes (Request scoped to specific unit IDs)
      - B) No (Search is always holistic)
    - **Recommended**: Option A - Unit-scoped search is much faster for "Quick Look" scenarios.

64. **Payload Syntax**: Do Agents send raw text via `warscribe-system` to the engine, or parsed JSON structures directly?
    - **Options**:
      - A) Raw Text (Engine handles parsing - high error risk)
      - B) Parsed JSON (Agents must use `warscribe-parser` first)
    - **Recommended**: Option B - MCTS should only receive clean, mathematical JSON state.

65. **Interrupts**: How are real-time Agent interruptions (e.g., an opponent suddenly plays a stratagem) injected to halt the search?
    - **Options**:
      - A) Signal-based (SIGINT to the process)
      - B) Polling (Engine checks a "Halt" flag in a shared cache)
      - C) Connection Drop (Closing the socket kills the search)
    - **Recommended**: Option C - Standard socket-level interruption is the cleanest for microservice architectures.

## 14. Integration with `vindicta-economy`

66. **Compute Bounding**: Is the total MCTS search depth bounded dynamically by a user's Gas Tank / token balance?
    - **Options**:
      - A) Yes (Depth is capped based on prepaid tokens)
      - B) No (Search completes, and user is billed after)
    - **Recommended**: Option A - Preventing "Bill Shock" by capping compute at the request level is safer for the platform.

67. **Cost Metric**: How are compute costs calculated and billed (seconds of CPU time vs total nodes searched)?
    - **Options**:
      - A) CPU Time (Ms used)
      - B) Node Count (Total unique states visited)
      - C) Tiered (Fixed price for Depth 2, Depth 3, etc.)
    - **Recommended**: Option B - Node count is the most hardware-agnostic metric for fair billing.

68. **Depth Premiums**: Does requesting a deeper search (e.g., Depth 5) automatically deduct more economy tokens?
    - **Options**:
      - A) Linear (Price = Depth * X)
      - B) Exponential (Price = BranchingFactor ^ Depth)
      - C) Fixed
    - **Recommended**: Option B - Computational cost for MCTS is exponential; the price should reflect that reality.

69. **Mid-Search Exhaustion**: What is the behavior if an account runs out of tokens while a search is actively processing at Depth 2?
    - **Options**:
      - A) Immediate Kill (Discard all results)
      - B) Graceful Return (Return the best found results so far, bill the partial amount)
    - **Recommended**: Option B - Users should still get what they paid for up to the point of exhaustion.

70. **Free Tiers**: Are cached Principal Variations or shallow Depth 1 estimations provided at zero token cost?
    - **Options**:
      - A) Yes (Encourage use for basic validation)
      - B) No (All compute is metered)
    - **Recommended**: Option A - Providing shallow "Sanity Checks" for free improves the ecosystem's developer experience.

## 15. Integration with `warscribe-system`

71. **Output Notation**: Is the resulting Principal Variation (best line of play) automatically translated back into standard Warscribe notation?
    - **Options**:
      - A) Yes (Engine includes a `notation` field in response)
      - B) No (A separate `warscribe-encoder` service handles translation)
    - **Recommended**: Option B - Keep the Engine purely mathematical; offload NLP/Notation logic to specialized services.

72. **Input Parsing**: Are incoming GameStates natively parsed from Warscribe text logs before initializing the root node?
    - **Options**:
      - A) Yes (Support text-to-search)
      - B) No (Require pre-parsed state)
    - **Recommended**: Option B - Explicit separation of concerns.

73. **Ambiguity Handling**: How are ambiguous Warscribe commands (e.g., "move forward") deterministically mapped to specific MCTS coordinates?
    - **Options**:
      - A) Closest Legal (Engine guesses based on rules)
      - B) Error Out (Require exact coordinates)
      - C) Multi-branch (MCTS searches all possible interpretations of the ambiguity)
    - **Recommended**: Option C - If a command is vague, the MCTS should search the top 3-5 interpretations and see which is strongest.

74. **Narrative Export**: Does the MCTS output support including generated narrative explanations attached to the Warscribe output?
    - **Options**:
      - A) Yes (e.g. "AI chose this to block the charge lane")
      - B) No (Mathematical scores only)
    - **Recommended**: Option B - MCTS handles "Why mathematically"; a separate LLM layer should handle "Why narratively".

75. **Nested Sequences**: How are complex nested sequences (like a prolonged fight phase) represented in Warscribe coming from flattened MCTS branches?
    - **Options**:
      - A) Sequence IDs (Group nodes by Battle Round/Phase/Interaction)
    - **Recommended**: Option A - Structured sequence IDs are necessary for multi-phase verification.

## 16. Integration with `vindicta-platform` (Backend API)

76. **Microservice Topology**: Does the Engine run as an isolated pod communicating via gRPC, or an embedded library?
    - **Options**:
      - A) Isolated Pod (gRPC/Protobuf)
      - B) Embedded Library (Imported directly into the Gateway)
      - C) Sidecar (Runs alongside the Game Manager)
    - **Recommended**: Option A - Isolation allows scaling the compute-heavy Engine independently from the I/O-heavy Gateway.

77. **Autoscaling Policy**: How are Engine instances autoscaled in Kubernetes (by message queue length, CPU utilization, or concurrent matches)?
    - **Options**:
      - A) Queue Length (NATS/RabbitMQ depth)
      - B) CPU Utilization (Standard HPA)
      - C) Custom (HPA based on "Active Search" count)
    - **Recommended**: Option C - Since MCTS is a continuous "5-second burst", scaling based on the number of concurrently active searches prevents overloading nodes.

78. **Session Pinning**: Are long-running game sessions pinned to specific Engine pods to maximize transposition table cache hits?
    - **Options**:
      - A) Yes (Sticky sessions via Ingress)
      - B) No (Any Engine can handle any request; cache is shared/external)
    - **Recommended**: Option A - Transposition tables are too large to share efficiently; pinning dramatically increases performance.

79. **Client Disconnects**: How are network partitions or sudden client disconnects managed while an evaluation is running?
    - **Options**:
      - A) Terminate Search (Save compute)
      - B) Complete & Cache (Complete the search and store the result for 1 min)
    - **Recommended**: Option B - If the client reconnects quickly, the result is immediately available.

80. **Transport Protocol**: Is the main MCTS query API strictly synchronous REST, or asynchronously managed via WebHooks/WebSockets?
    - **Options**:
      - A) Synchronous (Request/Response)
      - B) Asynchronous (Submit Task -> Receive Callback/Webhook)
      - C) Streaming (WebSockets)
    - **Recommended**: Option B - Mandatory for any task that takes >1 second to prevent gateway timeouts.

## 17. Simulation & Self-Play Infrastructure

81. **Heuristic Tuning**: Does the ecosystem support the Engine playing against itself internally to automatically tune heuristics?
    - **Options**:
      - A) Yes (Continuous self-play loop)
      - B) No (Heuristics are tuned manually by rules experts)
    - **Recommended**: Option A - Data-driven tuning is the only way to achieve "Stockfish" level accuracy.

82. **Record Storage**: Where and how are self-play game records continuously archived for offline analysis?
    - **Options**:
      - A) Object Storage (S3/GCS as Parquet/Avro files)
      - B) SQL Database (Metadata only)
      - C) Search Tree Dumps
    - **Recommended**: Option A - Parquet is ideal for training future neural network models.

83. **Elo Rating**: Is there a continuous integration step that gates deployment if the new Engine's Elo rating fails to beat the prior version?
    - **Options**:
      - A) Yes (CI runs N self-play matches before Merge)
      - B) No (Functional tests only)
    - **Recommended**: Option A - Regression testing in game AI MUST include "Strength Verification".

84. **Opening Books**: How are early-game "opening book" libraries generated and indexed from these self-play iterations?
    - **Options**:
      - A) Hash Map (Lookup by Board Hash)
      - B) SQL Index (Common turn 1 deployments)
    - **Recommended**: Option A - Fast O(1) lookup for common turn 1 layouts.

85. **Opponent Generation**: Does the Engine use specific adversarial matchmaking algorithms during self-play training?
    - **Options**:
      - A) Self (Newest vs Newest)
      - B) Ancestral (Newest vs Random prior versions)
      - C) Diversified (Aggressive Heuristic vs Defensive Heuristic)
    - **Recommended**: Option B - Standard practice to prevent "strategy collapse" or overfitting.

## 18. Testing Strategy & Determinism

86. **Strict Determinism**: Must the MCTS engine guarantee 100% deterministic output trees given a fixed integer seed?
    - **Options**:
      - A) Yes (Mandatory for regression testing)
      - B) No (Accept stochastic noise)
    - **Recommended**: Option A - Non-deterministic AI is impossible to debug at scale.

87. **Mocking**: How do we mock the Entropy Buffer robustly for unit testing tree depth generation?
    - **Options**:
      - A) Fixed Returns (Roll 3 always returns 3)
      - B) Static Distributions (JSON files representing the curve)
      - C) Mathematical Proxy (Simple Gaussian function)
    - **Recommended**: Option B - Using real data snapshots for mocks ensures the math logic handles "swingy" edge cases correctly.

88. **Regression Baselines**: Are there standardized regression scenario suites to ensure evaluation logic doesn't mathematically drift over time?
    - **Options**:
      - A) Yes (Suite of 100 "Puzzle" board states with expected scores)
      - B) No (Focus on unit test coverage)
    - **Recommended**: Option A - "Chess Puzzles" for 40k are essential for verifying heuristic changes.

89. **Memory Profiling**: Which tools are mandated for testing memory leaks and fragmentation in the custom arena allocator?
    - **Options**:
      - A) Valgrind / Memcheck (Requires C-extensions)
      - B) `tracemalloc` / `objgraph` (Python-native)
      - C) Prometheus Memory Metrics
    - **Recommended**: Option B - Standard for uv/Python 3.12 workspaces.

90. **Coverage Gates**: What minimum percentage of BDD scenario coverage is expected strictly for MCTS extreme edge cases?
    - **Options**:
      - A) 90% (Project Standard)
      - B) 100% (Intent-to-Execution Mandate)
    - **Recommended**: Option B - Essential for the core math modules as per `TDD_SKILL.md`.

## 19. Security, Cheating, and Sandboxing

91. **Payload Sanitization**: Could a maliciously crafted JSON GameState payload force the engine into an infinite parsing loop?
    - **Options**:
      - A) Yes (If recursive parser is used without depth limits)
      - B) No (JSON schemas and standard library parsers enforce strict limits)
    - **Recommended**: Option B - Standardizing on `orjson` or `pydantic` with strict recursive depth guards is sufficient.

92. **Timeout Enforcement**: Are client connection timeouts and search time limits enforced strictly by the orchestrator or internally by the engine?
    - **Options**:
      - A) Internal (Engine monitors its own clock)
      - B) External (API Gateway kills the socket)
      - C) Dual (Both)
    - **Recommended**: Option C - Redundant enforcement is required for high-availability systems.

93. **Hidden Objective Fishing**: Can malicious clients extract hidden opponent objectives by repeatedly probing the MCTS with targeted queries?
    - **Options**:
      - A) Yes (By observing score spikes for specific moves)
      - B) No (Search tree is scrubbed of all hidden state data before return)
    - **Recommended**: Option B - "What the UI doesn't need, it shouldn't see."

94. **Response Scrubbing**: Is the returned search tree sanitized to remove opponent-hidden states before dispatch to the client?
    - **Options**:
      - A) Yes (Sanitize `GameNode` metadata)
      - B) No (Metadata is already abstracted enough)
    - **Recommended**: Option A - Mandatory for competitive integrity.

95. **Rate Limiting**: At what gateway layer is MCTS evaluation request rate-limiting applied per user account?
    - **Options**:
      - A) NGINX / Network Ingress
      - B) Internal Engine Quota
      - C) Economy Layer (Gas Tank)
    - **Recommended**: Option C - Tying compute strictly to the `Gas Tank` economy naturally limits abuse.

## 20. Frontend & `vindicta-platform.github.io`

96. **Visual Overlays**: Does the single-page web frontend render MCTS evaluations visually (e.g., win probability bar graphs)?
    - **Options**:
      - A) Yes (Live-updating charts)
      - B) No (Text logs only)
    - **Recommended**: Option A - Visualizing the "Swing" of a turn is a key feature of the platform.

97. **Map Projections**: Are Principal Variations projected as movement arrows and pathing indicators on a 2D map in the browser?
    - **Options**:
      - A) Yes (SVG pathing overlays)
      - B) No (Coordinate lists only)
    - **Recommended**: Option A - Visualizing "The AI's Intent" makes the platform significantly more usable for players.

98. **Fast What-Ifs**: Can the frontend request asynchronous "what-if" fast evaluations without committing to a turn?
    - **Options**:
      - A) Yes (Low-depth Depth 1 searches)
      - B) No (Only full turn evaluations allowed)
    - **Recommended**: Option A - Allows players to "Check their Math" on move ideas.

99. **Loading States**: Flow-wise, how does the frontend UI gracefully handle the mandatory 5-second asynchronous loading states?
    - **Options**:
      - A) Skeleton Screens (Representing the board)
      - B) Progress Bar (Showing search depth progress)
      - C) Narrative Stream (Live log of what the AI is "thinking")
    - **Recommended**: Option C - Streaming "Thinking..." logs is the most engaging way to handle high-latency AI tasks.

100. **Client-Side Engine**: Are lightweight WASM (WebAssembly) versions of the MCTS engine planned for offloading compute to the browser?
    - **Options**:
       - A) Yes (Future Roadmap)
       - B) No (Keep compute behind the API for Prop/IP protection)
    - **Recommended**: Option B - Competitive game logic should stay on the server to prevent cheating and reverse-engineering of the evaluation weights.
