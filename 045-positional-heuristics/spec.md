# Feature Specification: FEAT-045 Advanced Positional Evaluation Heuristics

**Feature Branch**: `045-positional-heuristics`  
**Created**: 2026-02-28  
**Status**: Draft  
**Input**: User description: "Advance the logical stockfish setup and accuracy."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Threat Range Heatmaps (Priority: P1)
As the AI evaluation engine, I want to calculate the overlapping threat ranges (movement + weapon range) of all units on the board, so that I can penalize my own pieces for standing in deadly areas.
**Why this priority**: Raw "material" counts don't work in 40k; positioning is everything.
**Independent Test**: Can be tested by placing a fragile unit in the open vs behind ruins and verifying the engine evaluation significantly prefers the hidden position.

**Acceptance Scenarios**:
1. **Given** an enemy unit with a 36" weapon, **When** the heuristic calculates board control, **Then** all tiles within 36" of that unit without obscuring terrain receive a negative control score.

### User Story 2 - Objective Control Weighting (Priority: P2)
As the evaluation engine, I need to weigh the presence of "Objective Secured" (OC) models near objective markers higher than models in empty space, so that the engine understands how to win the game.
**Why this priority**: AI must prioritize scoring over merely killing.
**Independent Test**: Can be tested by giving the engine a choice between killing a non-scoring unit or moving onto an objective. It must choose the objective if it changes the VP math.

**Acceptance Scenarios**:
1. **Given** a choice to score 5 VP or destroy 100 points of enemy models, **When** evaluating the paths, **Then** the engine prefers the 5 VP if the ultimate game win probability is higher.

### Edge Cases
- How are complex terrain traits (e.g., Ruins, Craters) digested by the heuristic? (Grid-based raycasting for Line of Sight checks).

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Heuristic function MUST calculate total OC per objective marker.
- **FR-002**: Heuristic function MUST calculate expected damage output (Lethality) between all pairs of units with Line of Sight.
- **FR-003**: Heuristic function MUST run in under 50ms to be viable within the MCTS inner loop.

### Key Entities
- **HeuristicWeights**: Configurable parameters dictating the relative value of Material vs Board Control vs VP.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Heuristic accurately predicts the winner of historical matches from turn 3 onwards in 85% of test cases.
- **SC-002**: Function execution time averages < 50ms.
