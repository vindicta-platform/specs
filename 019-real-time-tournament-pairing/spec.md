# Feature Specification: 019-real-time-tournament-pairing

**Feature Branch**: `019-real-time-tournament-pairing`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Automated bracket generation based on live match transcription state."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Instant Next-Round Pairings (Priority: P1)

As a Tournament Organizer, I want the system to calculate the next round's matchups the moment the final table submits its score so that players aren't waiting around for manual calculation.

**Why this priority**: Eliminating downtime between rounds is a primary driver for adopting digital tournament software over pen-and-paper brackets.

**Independent Test**: Simulate an active round with 100 players. Submit the final match score for that round. Verify the system immediately generates completely legal pairings for the next round (no players facing previous opponents, correctly grouped by win-loss record) without manual intervention.

**Acceptance Scenarios**:

1. **Given** all matches in Round 1 are finalized, **When** the state locks, **Then** the platform instantly generates Round 2 brackets mapping winners to winners.
2. **Given** a 5-round Swiss format tournament, **When** generating late-round pairings, **Then** the logic strictly ensures two players never face each other twice in the same event.

---

### User Story 2 - Live Scenario Avoidance (Priority: P2)

As a player competing in a tournament, I want the system to ensure I don't repeatedly play against the exact same opposing Faction (e.g., Space Marines) three rounds in a row so that my event experience is varied.

**Why this priority**: Diversity of play improves competitor satisfaction, even when win-loss records identical.

**Independent Test**: Run a simulated pairing algorithm across 3 rounds. Assert that the pairing logic applies a negative weight (penalty) to matchups where a player is facing a faction they have already confronted in a previous round.

**Acceptance Scenarios**:

1. **Given** a pool of eligible opponents with identical win-loss records, **When** pairings calculate, **Then** the algorithm prioritizes opponents playing factions the user has not yet faced.

### Edge Cases

- What happens if a player drops out mid-tournament? (System must gracefully grant a formal "Bye" to the odd player out in subsequent rounds, scoring it explicitly as a win).
- What happens if a score is entered incorrectly and needs to be altered after the next round has been drawn? (System must allow a manual TO override to break the active round, recalculate the true standings, and redraw the entire affected pairing pool).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support standard competitive pairing algorithms (Swiss System, Round Robin, Single Elimination).
- **FR-002**: System MUST automatically trigger round pairing calculation the moment the final match of the preceding round completes.
- **FR-003**: System MUST provide table assignment logic to ensure players know exactly where they are physically sitting.
- **FR-004**: System MUST enforce a "Never Play Twice" absolute constraint within a single event.
- **FR-005**: System MUST weigh secondary constraints (Faction Diversity, Club Mates) during identical record pairing.

### Key Entities

- **Tournament Round**: The container governing all simultaneous active matches within a specific phase of the event.
- **Pairing Matrix**: The calculated list of Player A vs Player B match definitions for an active round.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Automatic pairing generation for a 500-player event (250 distinct matches) completes in under 2.0 seconds.
- **SC-002**: 100% adherence to absolute constraints (Never Play Twice) across all generated tournament simulated data.
- **SC-003**: Manual score corrections post-round generate a correctly updated replacement bracket within 1.0 second of TO approval.
