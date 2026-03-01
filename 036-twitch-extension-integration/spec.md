# Feature Specification: 036-twitch-extension-integration

**Feature Branch**: `036-twitch-extension-integration`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Interactive Twitch overlays allowing viewers to hover over units for rules."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Roster Overlay (Priority: P1)

As a Twitch viewer, I want to hover my mouse over a unit on the stream and see its active stats and special rules so that I can understand the match without being an expert in that specific army.

**Why this priority**: Lowering the barrier to entry for spectators is the only way to grow wargaming as a viewing sport.

**Independent Test**: Open a test stream with the extension active. Move the mouse cursor over a unit's screen coordinates (provided by the AR-sync layer). Verify a tooltip appears with the correct name and "Ranged Weapon" stats.

**Acceptance Scenarios**:

1. **Given** a streamer has synchronized their table layout, **When** a viewer interacts with the video player, **Then** the platform serves unit-specific rules text from the Oracle database based on the unit's physical location.

---

### User Story 2 - Real-Time Crowd Voting (Priority: P2)

As a streamer, I want to run a "Who will win?" or "MVP" poll that uses real-time match data (e.g., current score) to inform the audience, so that they feel personally involved in the match.

**Why this priority**: Enhances viewer retention and social engagement during long tournament streams.

**Independent Test**: Trigger an "MVP Vote" via the TO dashboard. Verify the Twitch extension displays the choice of all active units on the table with their current kill-counts attached as context.

**Acceptance Scenarios**:

1. **Given** an active match reaching Turn 5, **When** the streamer triggers the "MVP Poll," **Then** the top 3 most impactful units (by points scored/dealt) are automatically suggested as the voting options.

### Edge Cases

- What happens if the stream delay is excessive (e.g., 30 seconds)? (The extension must provide a "Delay Offset" setting so the digital overlays match the visual video feed exactly).
- How handles mobile-phone Twitch app viewers? (System MUST fall back to a "Mobile Panel" layout rather than an overlay, permitting the same rules-lookup functionality without obstructing the smaller video feed).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a transparent interactive overlay layer accessible via the Twitch Extension API.
- **FR-002**: System MUST synchronization visual element positions with real-time AR table telemetry.
- **FR-003**: System MUST provide on-demand rules text and stat-cards for any unit identified in the active match.
- **FR-004**: System MUST support localized stream delay buffers to ensure audio-visual synchronization of data.
- **FR-005**: System MUST allow viewers to interact with match-level metrics (Score, Turn, Clock) independently of the streamer's view.

### Key Entities

- **Extension State**: The local configuration on the viewer's browser governing their interaction with the stream data.
- **Sync Pulse**: The periodic coordinate update sent from the platform to the extension to keep graphics aligned with the video.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Interaction latency (Hover-to-Tooltip) is < 250 milliseconds for cached rules data.
- **SC-002**: Overlay alignment remains accurate to within 10 pixels of the intended physical unit location on a standard 1080p stream.
- **SC-003**: Extension handles 100,000 concurrent viewers on a single stream without API rate-limiting or crash.
