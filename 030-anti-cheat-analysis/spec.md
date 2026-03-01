# Feature Specification: 030-anti-cheat-analysis

**Feature Branch**: `030-anti-cheat-analysis`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "ML-driven detection of anomalous dice results and state discrepancies."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Statistical Anomaly Detection (Priority: P1)

As a tournament organizer, I want the system to flag players whose physical dice rolls (captured via hardware or manual entry) deviate significantly from normal probability distributions, so that I can investigate potential "loaded dice" or input fraud.

**Why this priority**: Integrity is everything in high-stakes competition. Hard data on "impossible" runs of luck provides an objective basis for judge intervention.

**Independent Test**: Inject a series of 100 rolls where the result is "6" 60% of the time. Verify the system flags this as a "Critical Probability Anomaly" with a confidence score.

**Acceptance Scenarios**:

1. **Given** a match transcript, **When** a player's cumulative dice results deviate by > 3 standard deviations from the mean, **Then** an alert is sent to the TO dashboard for manual review.

---

### User Story 2 - State Discrepancy Flagging (Priority: P2)

As an auditor, I want the system to identify if the final submitted score "impossible" given the sequence of actions and unit capabilities recorded in the transcript.

**Why this priority**: Detects "score padding" where players agree to a higher result than what actually happened at the table.

**Independent Test**: Create a transcript where a player scores 100 points, but their army's registered objectives only allow for a maximum of 45. Verify the system flags the outcome as a "State Paradox."

**Acceptance Scenarios**:

1. **Given** a match conclusion, **When** the final score is submitted, **Then** the engine performs a "Backward-Trace" verification to ensure every point has a corresponding justifying action in the transcript.

### Edge Cases

- What happens if a player has legitimate "hot dice" (pure luck)? (The system must never automatically ban/disqualify; it only raises "Flags for Review," maintaining the human-in-the-loop requirement).
- How handles "Fudged" measurements in AR/manual entries? (System flags sequences of moves that are consistently 0.5 inches longer than the recorded unit's maximum capability).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST perform real-time probability analysis on all captured match dice rolls.
- **FR-002**: System MUST compare physical action sequences (moves, shots) against unit capability profiles for legitimacy.
- **FR-003**: System MUST identify and flag discrepancies between the logical transcript and the final submitted score.
- **FR-004**: System MUST provide a "Suspected Integrity Violation" report containing the specific mathematical evidence.
- **FR-005**: System MUST aggregate player "Karma" scores over time, identifying repeat offenders across multiple events.

### Key Entities

- **Integrity Score**: A numerical value representing the likelihood a match followed all rules and probability norms.
- **Probability Deviation**: The mathematical distance between recorded outcomes and the expected bell curve.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Statistical analysis engine identifies 100% of "Impossible Streaks" (> 4 Std Dev) in synthetic test data.
- **SC-002**: Backward-trace verification of a full 2000-point match transcript completes in under 2 seconds.
- **SC-003**: Zero false-positive "Bans" produced (as the system is designed strictly for flagging, not automated sentencing).
