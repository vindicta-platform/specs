# Phase 1: Data Model (FEAT-044)

The MCTS Engine defines two primary entities: `GameState` and `SearchNode`. These will be represented using `pydantic` classes inheriting from `VindictaModel` to ensure serialization to JSON and integration compatibility across the Vindicta ecosystem.

## GameState
A mathematical translation of the current 40k board.

**Fields**:
- `turn_number` (int): Current game turn (1-5).
- `active_player` (str): Identifier for the player whose turn it is.
- `unit_positions` (Dict[str, tuple[float, float, float]]): Mapping of unit IDs to their 3D coordinates.
- `unit_state_flags` (Dict[str, list[str]]): Mapping of unit IDs to current statuses (e.g., `["Fell_Back", "In_Engagement_Range"]`).
- `vp_scores` (Dict[str, int]): Current Victory Points per player.

**State Transitions**:
Modified immutably (copy-on-write) during tree expansion to ensure deterministic search.

## SearchNode
A node representing a branch in the MCTS tree.

**Fields**:
- `id` (int): Internal index in the arena buffer.
- `parent_id` (int | None): Pointer to parent node.
- `children` (List[int]): Pointers to child nodes.
- `state_hash` (str): Unique hash of the `GameState` at this node (for transposition tables).
- `move_causing_state` (str | None): The serialized move that resulted in this state.
- `visits` (int): MCTS visitation count ($n_i$).
- `value_sum` (float): Total reward sum ($w_i$).
- `is_terminal_node` (bool): Whether the game ends here or depth limit reached.
