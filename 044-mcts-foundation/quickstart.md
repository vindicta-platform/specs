# Quickstart: MCTS Engine

Integrating the FEAT-044 MCTS Engine into your domain logic.

## Initialization

```python
from vindicta_engine.mcts.engine import MCTSEngine
from vindicta_engine.mcts.config import MCTSTraceLevel
from vindicta_foundation.models.mcts import GameState

# 1. Initialize the engine with a strict arena buffer and BASIC tracing
engine = MCTSEngine(
    memory_limit_mb=512, 
    trace_level=MCTSTraceLevel.BASIC
)

# 2. Reconstruct the GameState from incoming payload
board_state = GameState.model_validate_json(incoming_json_payload)

# 3. Request evaluation (5 seconds, Depth 3)
try:
    result = engine.evaluate_state(
        root_state=board_state,
        max_depth=3,
        time_budget_ms=5000
    )
    print(f"Engine Evaluation: {result.evaluation_score}")
    print(f"Best Line of Play: {result.principal_variation}")

except Exception as e:
    # Captures invalid moves or OOM boundaries from the arena layer
    print(f"Search Failed: {e}")
```
