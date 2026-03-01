# Feature Specification: 020-live-stream-overlay-widget

**Feature Branch**: `020-live-stream-overlay-widget`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "OBS-compatible overlays for tournament streaming."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Live Score Broadcast (Priority: P1)

As a tournament broadcaster, I want a transparent, web-based widget displaying the live score of the feature match so that I can overlay it onto my video feed without manually typing updates as they happen.

**Why this priority**: High-quality streaming is essential for wargaming community engagement. Providing native broadcast tools embeds the platform firmly in the content creation ecosystem.

**Independent Test**: Load the overlay widget into a standard broadcasting software environment. Submit score changes to the active match via the platform. Verify the overlay updates automatically within the broadcast feed.

**Acceptance Scenarios**:

1. **Given** an active streamed match, **When** a player scores a secondary objective, **Then** the overlay automatically animates to reflect the updated point totals and the specific objective completed.

---

### User Story 2 - Player Information Display (Priority: P2)

As a stream viewer, I want to see the names, current factions, and overall tournament standings of the players on screen so that I have context for the match I am watching.

**Why this priority**: Contextualizing the players in a 500-person tournament creates stronger narrative engagement for the audience.

**Independent Test**: Connect the widget to a specific tournament match ID. Verify it correctly pulls the current W-L bracket record for exactly those two players alongside their names.

**Acceptance Scenarios**:

1. **Given** a match in round 4, **When** the overlay initializes, **Then** it correctly displays both players' current 3-0 records alongside their faction icons.

### Edge Cases

- What happens if the stream overlays disconnect from the central server? (The overlay must maintain the last known good state rather than displaying an error message or disappearing from the live broadcast, retrying silently in the background).
- How are very long player names or club affiliations handled? (Overlay UI must implement graceful text clipping or scrolling to avoid pushing visual elements out of their defined transparent bounding boxes).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a discrete, transparent-background visual interface designed specifically for video composition.
- **FR-002**: System MUST subscribe to real-time telemetry from the specific match being broadcast.
- **FR-003**: System MUST provide customizable visual themes (e.g., standard layout, compact layout) selectable via query parameter.
- **FR-004**: System MUST display real-time points, command resource pools, and active turn timers.

### Key Entities

- **Broadcast Widget**: The actual visual interface loaded into the streaming software.
- **Match Telemetry Stream**: The continuous data feed providing live state updates from the engine.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Broadcast widget updates visually within 1.0 second of a score change occurring on the platform.
- **SC-002**: The widget draws fewer than 5% of CPU resources on a standard consumer rendering machine to avoid interfering with video encoding.
- **SC-003**: Graphic animations for score changes trigger correctly 100% of the time during simulated stream bursts without visual tearing.
