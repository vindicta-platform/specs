# Phase 1: MCTS Engine Contract API

The MCTS Engine exposes a strictly typed Python interface within `vindicta-engine`.

## Public Interface

### `MCTSEngine`

```python
class MCTSEngine:
    def __init__(self, memory_limit_mb: int = 512, trace_level: MCTSTraceLevel = MCTSTraceLevel.BASIC):
        """
        Initializes the arena allocator and configures observability.
        """
        ...

    def evaluate_state(self, root_state: GameState, max_depth: int = 3, time_budget_ms: int = 5000) -> MCTSResult:
        """
        Executes a constrained Monte Carlo Tree Search.
        
        Args:
            root_state: The starting snapshot of the board.
            max_depth: Maximum ply depth before enforcing static evaluation.
            time_budget_ms: Hard time limit for the search in milliseconds.
            
        Returns:
            MCTSResult containing the evaluation score and Principal Variation.
        """
        ...
```

### `MCTSResult`

```python
class MCTSResult(VindictaModel):
    evaluation_score: float
    principal_variation: list[str]  # Ordered list of best moves
    nodes_visited: int
    computation_time_ms: float
    cache_hits: int
    trace_log: str | None
```
