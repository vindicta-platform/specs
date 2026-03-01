# Feature Specification: 040-reputation-system

**Feature Branch**: `040-reputation-system`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Tracking player and TO reliability scores."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fair Play Verification (Priority: P1)

As a tournament organizer, I want to see a player's "Karma" or reputation score before accepting their registration so that I can identify and potentially bar players with a consistent history of cheating, poor sportsmanship, or "no-showing" events.

**Why this priority**: Essential for maintaining the social health of the competitive scene. High reputation acts as a "Trust Signal" for community safety.

**Independent Test**: Register a series of validated sportsmanship reviews for a player. Verify the player's Reputation Score updates accordingly and is visible to TOs of events they join.

**Acceptance Scenarios**:

1. **Given** a player with multiple negative sportsmanship reports, **When** they apply for a major GT, **Then** the TO receives a "High Friction Risk" alert in their dashboard.

---

### User Story 2 - TO Reliability Tracking (Priority: P2)

As a player traveling cross-country for an event, I want to see the reputation of the Hosting Venue/TO so I can be confident the event will be well-run, scored correctly, and safe.

**Why this priority**: Prevents players from wasting time/money on poorly managed or predatory events.

**Independent Test**: Assign a "Verified Event Partner" badge to a TO. Verify that players searching the global event locator can filter specifically for "High Rep" organizers.

**Acceptance Scenarios**:

1. **Given** a tournament concludes, **When** players submit their "Event Feedback," **Then** the TO's reputation score is recalculated based on metrics like "Scoring Accuracy," "Schedule Adherence," and "Venue Quality."

### Edge Cases

- What happens if a player is "Brigaded" (targeted with false negative reviews)? (System must identify "Coordinate Rating Bursts" and flag them for manual moderation, potentially ignoring them in the final score calculation).
- How handles "Reputation Decay"? (Reputation should not be permanent; poor behavior 10 years ago should weigh less than positive behavior last month).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST maintain a persistent, multi-dimensional Reputation Score for every user identity.
- **FR-002**: System MUST aggregate data from multiple sources (Judge Calls, Player Reviews, TO Feedback, Matching Timing).
- **FR-003**: System MUST identify and flag anomalous rating patterns (Brigading detection).
- **FR-004**: System MUST apply a temporal decay function to ancient reputation data points.
- **FR-005**: System MUST expose reputation metadata to registration and matchmaking services for policy enforcement.

### Key Entities

- **Reputation Profile**: The unified record of trust-based data points for a specific user.
- **Trust Event**: A single interaction (Review, Report, Completion) that modifies a reputation score.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Reputation scores recalculate and propagate globally within 15 minutes of an event's conclusion.
- **SC-002**: Detecting a coordinate rating attack (Brigading) happens with > 90% accuracy in synthetic tests.
- **SC-003**: 100% of reputation-modifying events are tied to a verifiable Match ID or Event ID to prevent anonymous spam.
