# Feature Specification: 044-mcts-foundation

**Feature Branch**: `044-mcts-foundation`
**Created**: 2026-02-28
**Status**: Draft
**Input**: User description: "Advance the logical stockfish setup and accuracy."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Board State Evaluation (Priority: P1)

As an AI developer, I want the system to take a mathematical snapshot of the current 40k board state and evaluate the win probability using Monte Carlo Tree Search (MCTS) so that we can objectively rate a player's position.

**Why this priority**: Core algorithmic foundation for the entire intelligence suite.

**Independent Test**: Can be tested by feeding a known "winning" board state (e.g., Turn 4, 20 VP lead, dominant board control) and verifying the engine returns a >90% win probability.

**Acceptance Scenarios**:

1. **Given** a structured JSON representation of the board state, **When** the MCTS engine is invoked with a depth of 3, **Then** it returns an evaluation score (e.g., +4.5) and the principal variation (best line of play).

---

### User Story 2 - Move Generation Validation (Priority: P1)

As the engine, I need to generate all legal moves (movement, shooting targets, charge declarations) for a given unit in a given phase, so the MCTS algorithm can branch correctly.

**Why this priority**: Without legal move generation, the tree search is useless or invalid.

**Independent Test**: Can be tested via unit tests that place a unit in a constrained scenario (e.g., in engagement range) and verify it only generates "Fall Back" or "Remain Stationary" and melee attack moves.

**Acceptance Scenarios**:

1. **Given** a unit locked in combat, **When** move generation is requested for the Movement phase, **Then** only legal actions (Fall Back, Remain Stationary) are returned.

### Edge Cases

- How does the engine handle infinitely looping board states or mathematically intractable numbers of permutations? (Implement aggressive alpha-beta pruning and hard time limits per search node).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Engine MUST accept a standardized GameState and output an EvaluationScore.
- **FR-002**: The Engine MUST implement Monte Carlo Tree Search with configurable depth and time constraints.
- **FR-003**: The Engine MUST interface with the Entropy Buffer to evaluate expected values of dice rolls, rather than simulating every possible raw die outcome branching.
- **FR-004**: The Engine MUST utilize a pre-allocated Arena Allocator for memory management.
- **FR-005**: The Engine MUST provide structured observability traces (NONE/BASIC/PV/FULL).
- **FR-006**: The Engine MUST return computation metrics (time, nodes) for upstream economy metering.
- **FR-007**: Architecture MUST be documented via an ADR in the platform's central decision record.
- **FR-008**: The Engine MUST validate GameState input for Turn Range (1-5) and payload size limit.

### Key Entities

- **GameState**: The mathematical representation of the board, units, and scores.
- **SearchNode**: A node in the MCTS tree representing a potential future state.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Engine can evaluate a mid-game state to a depth of 3 within 5 seconds on standard hardware.
- **SC-002**: Engine move generator unit tests pass with 100% coverage against edge cases like Deep Strike and Engagement contours.
