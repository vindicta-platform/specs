# Feature Specification: 007-battle-transcript-engine

**Feature Branch**: `007-battle-transcript-engine`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Real-time streaming of table events."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Real-Time Match Streaming (Priority: P1)

As a spectator or remote judge, I want to watch a match's logical state update in real-time as events occur at the physical table, so I can follow the action without lag.

**Why this priority**: Streaming match data live to dashboards and viewers is the primary engagement mechanism for remote competitive wargaming.

**Independent Test**: Can be tested by pushing synthetic match events into the engine and verifying that a listening client receives the exact sequence in the correct chronological order within the latency limit.

**Acceptance Scenarios**:

1. **Given** an active match generating score and movement events, **When** those events are captured, **Then** they are immediately broadcast to all subscribed viewing dashboards.
2. **Given** a viewer joining an in-progress match, **When** they connect, **Then** they receive the current full logical state to synchronize before receiving the live event stream.

---

### User Story 2 - Full Match Replay Capability (Priority: P2)

As a player analyzing my games, I want to replay a completed match from turn 1 step-by-step, so I can review tactical decisions and dice variance.

**Why this priority**: Post-match analysis is a critical feature for competitive players looking to improve via data.

**Independent Test**: Run a recorded transcript from start to finish and verify the final computed game state matches the official end-of-game scorecard perfectly.

**Acceptance Scenarios**:

1. **Given** a completely recorded match transcript, **When** loaded into the replay engine, **Then** the user can step forward and backward through every tracked action and die roll.

### Edge Cases

- What happens if the local ingestion device temporarily loses internet connection? (System must buffer events locally and transmit them chronologically upon reconnection without breaking sequence).
- What happens if a player physically rewinds an action (e.g., taking back a move with opponent permission)? (Engine must support explicit "Undo" events that logically reverse the previous state without mutating the historical audit trail).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST record all submitted game actions into a chronologically sorted, immutable log stream.
- **FR-002**: System MUST broadcast new events in real-time to subscribed clients.
- **FR-003**: System MUST support calculating "Delta-State updates" so clients only receive what changed, minimizing bandwidth.
- **FR-004**: System MUST construct a complete point-in-time point representation of the game board/score based on the transcript history.

### Key Entities

- **Match Transcript**: The chronological ledger containing every distinct state change and action applied to a game.
- **State Snapshot**: A reconstructed point-in-time representation of the entire game's board and score standings.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Event propagation delay from ingestion receipt to spectator broadcast is consistently < 500 milliseconds.
- **SC-002**: Replaying a recorded transcript guarantees 100% state fidelity compared against the original live stream.
- **SC-003**: System gracefully handles connection volatility, correctly sequencing bursts of offline-buffered events up to 5 minutes long.
