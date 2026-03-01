# Feature Specification: 045-positional-heuristics

**Feature Branch**: `045-positional-heuristics`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Core logic for calculating geometric positioning advantages."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Flanking maneuvers Identification (Priority: P1)

As a tactical analyst, I want the system to identify when a unit is "Flanked" or "Pincered" by two enemy units so that the AI or analytical engine can evaluate the severity of the threat correctly.

**Why this priority**: Positional context (where a unit is relative to others) is what differentiates a "Game Engine" from a "Calculated Result Engine."

**Independent Test**: Place a target model at (0,0). Place two enemies at (1,0) and (-1,0). Verify the heuristic engine identifies this as a "Pincer" state with a high structural vulnerability weighting.

**Acceptance Scenarios**:

1. **Given** a unit's position and the orientation of all nearby enemies, **When** the heuristic calculator runs, **Then** it identifies and tags specific geometric states like "Encircled," "Screened," or "Flanked."

---

### User Story 2 - Objective Coverage Analysis (Priority: P2)

As a player reviewing a replay, I want to see a value overlay showing which parts of the table were "Secure" vs "Contested" based on the threat ranges of my units, so I can see where my screen failed.

**Why this priority**: Helps players visualize "Invisible Walls" created by high-threat units (e.g., massive ranged guns).

**Independent Test**: Load a board state with a long-range artillery unit. Verify the heuristic renders a "High-Threat Radius" where any moving unit would be statistically likely to be deleted.

**Acceptance Scenarios**:

1. **Given** an active match board, **When** the overlay is toggled, **Then** the engine renders semi-transparent zones of "Influence" where units have > 75% probability of successful engagement.

### Edge Cases

- What happens if a unit is in an "Impossible" position (e.g., inside solid terrain)? (Heuristic engine must flag a "Geometry Violation" rather than trying to calculate strategic value for an invalid state).
- How handles "Hidden" or "Reserved" units? (Heuristics only consider "On-Board" entities; however, a "Reserved Threat" weight can be applied to deployment zones to reflect potential late-game arrivals).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST calculate geometric relationships (Distances, Angles) between all on-board game entities.
- **FR-002**: System MUST identify and classify specific tactical archetypes (Pincer, Flank, Screen, Conga-line).
- **FR-003**: System MUST assign a "Threat Weight" to table regions based on unit engagement ranges.
- **FR-004**: System MUST provide a standardized API for raw positional data to be ingested by the MCTS foundation.
- **FR-005**: System MUST identify "Critical Failure Points" in screening (holes large enough for an enemy base to fit through).

### Key Entities

- **Geometric Context**: The relative spatial relationship of a unit to its allies, enemies, and terrain.
- **Threat Radius**: The calculated 2D or 3D area where a unit can effectively apply its primary power.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Heuristic evaluation of a 50-unit board state completes in < 50 milliseconds.
- **SC-002**: Identification of "Pincer" and "Flank" states matches human-expert designations in 95% of test scenarios.
- **SC-003**: Screening-hole detection identifies gaps as small as the smallest possible base size (e.g., 25mm) with 100% accuracy.
