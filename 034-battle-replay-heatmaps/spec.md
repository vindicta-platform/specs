# Feature Specification: 034-battle-replay-heatmaps

**Feature Branch**: `034-battle-replay-heatmaps`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Visualized area-of-effect and movement density analysis for replays."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visualizing Lethality Zones (Priority: P1)

As a coach or competitive player, I want to see a heatmap overlay on a match replay showing where the most damage was dealt so that I can understand which parts of the table were "Kill Zones."

**Why this priority**: Spatial analysis is the keys difference between basic score-tracking and high-level tactical coaching.

**Independent Test**: Load a completed match replay. Toggle the "Damage Heatmap." Verify that sectors where unit deletions occurred are highlighted in "Hot" colors (Red/Orange).

**Acceptance Scenarios**:

1. **Given** a 5-turn match transcript, **When** heatmaps are generated, **Then** the map visually differentiates between "High Combat Density" (center objective) and "Safe Zones" (corners/deployment).

---

### User Story 2 - Movement Patterns Over Time (Priority: P2)

As a player, I want to see a "Pathing Heatmap" showing the most common routes my units took across multiple games so that I can identify if my deployment is too predictable.

**Why this priority**: Identifying behavioral patterns in model movement is essential for breaking sub-optimal habits.

**Independent Test**: Aggregate 5 games of the same player. Request the "Movement Density" heatmap. Verify the map correctly highlights the overlapping paths taken by the player's core units.

**Acceptance Scenarios**:

1. **Given** a collection of match transcripts, **When** aggregated, **Then** the heatmap provides a "Glow" effect indicating the most frequently occupied coordinates on the 6x4 table.

### Edge Cases

- What happens if the terrain layout changed between the 5 games being aggregated? (The system must allow a "Ghost Terrain" view or strictly aggregate only games with identical tournament map IDs).
- How handles very large datasets? (Generating heatmaps for 100+ matches simultaneously must be processed as a background task, notifying the user when the visualization is ready).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST translate transcript-based coordinates into a weighted visual density map (Heatmap).
- **FR-002**: System MUST differentiate between different event types (Movement, Damage Dealt, Objectives Scored) via distinct color scales.
- **FR-003**: System MUST support temporal filtering (e.g., "Show me the heatmap for only Turn 1").
- **FR-004**: System MUST support aggregation of multiple matches into a single unified analysis view.

### Key Entities

- **Spatial Matrix**: The underlying grid coordinate system storing event weights.
- **Heatmap Layer**: The visual SVG or Canvas overlay rendered atop the match board representation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Heatmap generation from a standard 5-turn transcript completes in < 1.0 second.
- **SC-002**: Aggregated analysis of 10 matches completes and renders in under 5.0 seconds.
- **SC-003**: Visual representations accurately map to transcript coordinates with < 0.5 inch (table scale) of error.
