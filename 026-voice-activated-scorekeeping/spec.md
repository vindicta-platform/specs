# Feature Specification: 026-voice-activated-scorekeeping

**Feature Branch**: `026-voice-activated-scorekeeping`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Voice commands for managing match scores and phase transitions."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Voice-Driven Scoring (Priority: P1)

As a player in the heat of a match, I want to say "Score 5 points for Primary" and have the system automatically update the scorecard so that I don't break my focus on the strategy.

**Why this priority**: Complementary to battle logging, voice scoring is the most frequent interaction during a game. Low friction here improves the user experience significantly.

**Independent Test**: Speak 5 different scoring intents into the system. Verify that the score updates correctly on the companion app and main dashboard.

**Acceptance Scenarios**:

1. **Given** a player is in Round 3, **When** they say "I scored my secondary objective for 4 points," **Then** the platform identifies the objective from the player's active roster and increments the score.

---

### User Story 2 - Phase and Turn Navigation (Priority: P2)

As a player, I want to say "End my movement phase" or "Next turn" to move the logical state of the game forward hands-free.

**Why this priority**: Required for keeping the digital clock and transcript in sync with the physical reality of the game.

**Independent Test**: Say "End Deployment." Verify the digital state transitions to "Turn 1, Movement Phase."

**Acceptance Scenarios**:

1. **Given** it is the Player A shooting phase, **When** the player says "Done shooting," **Then** the system transitions the active turn to the Charge or Melee phase automatically.

### Edge Cases

- What if the player says "Add 5 points" without specifying which objective? (System must ask "To which objective?" or default to the most likely primary score).
- How handles conflicting commands from the opponent? (System only accepts scoring or phase commands from the device/user officially logged in as that player for that match).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST resolve auditory numbers and map them to logical score increments.
- **FR-002**: System MUST identify and execute phase transition intents.
- **FR-003**: System MUST identify the specific objective indicated in a voice command based on the active match setup.
- **FR-004**: System MUST differentiate between "Intent to Score" and "Incidental Table Talk."
- **FR-005**: System MUST provide clear, non-intrusive auditory confirmation of the action taken (e.g., a subtle "Plus five registered" chime).

### Key Entities

- **Scoring Intent**: The specific auditory request to modify a numeric match value.
- **Phase Intent**: The request to transition the game's logical state to a different turn part.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System accurately differentiates score commands from table talk with > 98% filtering accuracy.
- **SC-002**: Resulting score updates propagate to all match views in < 1.0 second.
- **SC-003**: Average time to resolve and commit a scoring intent is < 500 milliseconds.
