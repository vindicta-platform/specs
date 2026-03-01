# Feature Specification: 023-mobile-companion-app

**Feature Branch**: `023-mobile-companion-app`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Portable match tracker and roster viewer."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pocket Roster Access (Priority: P1)

As a player at a physical game table, I want to quickly pull up my unit's statistics and rules on my phone so that I don't have to carry heavy paper rulebooks to the table.

**Why this priority**: Mobile access is the primary way users will interact with the platform in the "real world." It is the foundation for match ingestion.

**Independent Test**: Load a standard 2000-point roster into the mobile view. Verify that switching between units takes < 1 second and all relevant special rules are legible on a standard 6-inch screen.

**Acceptance Scenarios**:

1. **Given** a pre-loaded army roster, **When** a user clicks a unit name, **Then** a clean, mobile-optimized card appears containing every relevant stat (M, WS, BS, etc.) and active weapon profile.

---

### User Story 2 - Real-Time Scoring & Turn Management (Priority: P1)

As a player during a match, I want to tap buttons to record VPs, command points, and end-of-turn events so that I can maintain an accurate score without a physical calculator.

**Why this priority**: The companion app is the "remote control" for the overarching tournament platform.

**Independent Test**: Start a live match in the companion app. Execute a sequence of 5 scoring actions. Verify that the central platform dashboard reflects these changes instantly.

**Acceptance Scenarios**:

1. **Given** the current score is 10-10, **When** I tap "+5 Primary Points" on my mobile device, **Then** the local and remote scores immediately synchronize to 15-10.

### Edge Cases

- What happens if the phone battery dies or the app crashes during a final turn? (All match state MUST be persistently saved locally per-action so that a simply battery-swap and restart resumes at the exact second of failure).
- How handles "Offline" play when cellular signal in a convention basement is zero? (App must fully support local match tracking and "sync when back online" without losing data).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a responsive, high-contrast interface optimized for one-handed mobile use.
- **FR-002**: System MUST allow pre-loading and offline caching of rules and custom army rosters.
- **FR-003**: System MUST provide intuitive manual input for all common match metrics (VP, CP, HP).
- **FR-004**: System MUST synchronize local match state with the central platform whenever a network connection is available.
- **FR-005**: System MUST support persistent state saving to prevent data loss during app interruptions.

### Key Entities

- **Mobile Workspace**: The isolated local data container on the phone managing the active match session.
- **Roster Snapshot**: The mobile-optimized representation of a player's army list and rules.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Core app bundle and baseline ruleset load in under 3.0 seconds even on mid-range 4G data connections.
- **SC-002**: Zero match data loss occurs across 100 simulated app crashes and immediate restarts during active turn sequences.
- **SC-003**: Interface meets 44x44 pixel minimum touch target sizes for 100% of critical scoring buttons.
