# Feature Specification: FEAT-047 Statistical Upset Detector & Meta Alerts

**Feature Branch**: `047-upset-detector`  
**Created**: 2026-02-28  
**Status**: Draft  
**Input**: User description: "Advance meta analysis capabilities."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Match Probability vs Actual Outcome (Priority: P1)
As the platform's Arbiter agent, I want to compare the pre-game estimated win probability with the actual result, flagging the match as an "Upset" if a <15% probability list wins.
**Why this priority**: Identifies sleeper lists and meta-breakers immediately.
**Independent Test**: Can be tested by feeding a match log where a mathematically inferior list wins by a wide margin, verifying the match is flagged.

**Acceptance Scenarios**:
1. **Given** a completed tournament match result, **When** the winner had an Elo or List Grade significantly lower than the loser, **Then** the match is flagged as "High Upset".

### User Story 2 - Emerging Meta Trend Alerts (Priority: P2)
As a meta analyst, I want to receive an automated weekly report highlighting units or archetypes that have spiked in win-rate by more than 5% over a 14-day trailing window, so I can discuss them in content.
**Why this priority**: Creates sticky, recurring engagement with the platform's data.
**Independent Test**: Can be tested by modifying historical match data to artificially boost a specific unit's win rate and verifying the alert triggers during the weekly cron job.

**Acceptance Scenarios**:
1. **Given** historical data, **When** the anomaly detection cron runs, **Then** any unit exhibiting a >5% delta in win-rate over 14 days triggers an "Emerging Trend" event.

### Edge Cases
- What if an upset is caused by player drops/concessions? (Filter out matches that end in Turn 1 or 2, or where the score is a 0-100 forfeit).

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST record pre-match predictive probabilities alongside final outcomes in the dataset.
- **FR-002**: System MUST implement a statistical process control algorithm (e.g., Bollinger Bands on win rates) to detect anomalies.
- **FR-003**: System MUST publish identified trends to an event bus for consumption by UI and email systems.

### Key Entities
- **MatchAnomaly**: A record detailing why a specific match outcome defied mathematical expectations.
- **TrendAlert**: A time-series anomaly detected across multiple matches.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Anomaly detection logic filters out statistically insignificant sample sizes (e.g., requires >50 matches to trigger).
- **SC-002**: Platform generates valid Meta Alerts automatically on a weekly schedule.
