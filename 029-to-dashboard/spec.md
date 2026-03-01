# Feature Specification: 029-to-dashboard

**Feature Branch**: `029-to-dashboard`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Centralized control panel for Tournament Organizers."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Real-Time Tournament Oversight (Priority: P1)

As a Tournament Organizer, I want to see a live view of all active tables in my event so that I can identify which games are running behind and deploy judges to keep the event on schedule.

**Why this priority**: "Time Parity" is the hardest part of running a Large Scale Tournament. Real-time visibility into game progress (turn count, time remaining) is a logistics game-changer.

**Independent Test**: Load the dashboard for an event with 50 active matches. Verify that every table's turn count and remaining clock time update every 60 seconds without page refresh.

**Acceptance Scenarios**:

1. **Given** an event with 10 tables, **When** the round starts, **Then** the TO dashboard visually identifies which tables have NOT yet started their clocks.
2. **Given** a table with only 5 minutes remaining on a match clock, **When** reaching that threshold, **Then** the dashboard highlights that table in "Critical" red to alert the TO.

---

### User Story 2 - Mass Roster Verification (Priority: P2)

As a TO before the event starts, I want to see a list of all submitted rosters and their validation status so that I can contact players who submitted illegal or incomplete lists.

**Why this priority**: Manual roster checks for a 100-person event take hours. Automating the oversight of the validation process saves immense pre-event labor.

**Independent Test**: Submit 3 valid and 2 invalid rosters via the player portal. Verify the TO dashboard correctly counts and identifies the 2 failures for review.

**Acceptance Scenarios**:

1. **Given** 100 players registered, **When** rosters are submitted, **Then** the dashboard provides a "Percent Validated" progress bar and one-click access to the specific rule violations for every failing list.

### Edge Cases

- What happens if the TO's internet goes down while trying to push pairings? (The dashboard must support a local "Master State" that can be printed or exported to PDF for manual distribution in a networking emergency).
- How handles "Secret" mission scoring? (TO must see the "True" score in the dashboard for judging purposes, even if that information is hidden from the opponent's view on the table).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a high-density, real-time grid view of all active matches in an event.
- **FR-002**: System MUST aggregate and display critical match telemetry (Turn count, Clock time, Score).
- **FR-003**: System MUST provide mass-management tools for rosters, pairings, and results.
- **FR-004**: System MUST allow TOs to manually override any score or clock state in any active match.
- **FR-005**: System MUST provide a "Printable Backup" export of the current tournament state and upcoming pairings.

### Key Entities

- **Event Master View**: The centralized, real-time control plane for a tournament.
- **Table Monitor**: The individual data unit tracking a specific physical table's digital progress.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dashboard sustains real-time updates for 1,000 simultaneous matches without significant UI lag.
- **SC-002**: Critical alerts (Time warnings, Score disputes) appear on the TO dashboard in < 5.0 seconds of detection.
- **SC-003**: The TO "Master State" PDF export generates and is available for download in under 10.0 seconds.
