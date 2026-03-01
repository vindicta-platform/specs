# Feature Specification: 006-rules-validation-parser

**Feature Branch**: `006-rules-validation-parser`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Validate transcript actions against rules RAG."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate Transcribed Actions Against Rules (Priority: P1)

As a tournament organizer or player, I want the system to automatically flag illegal moves or actions within a game transcript so that rule-breaking can be identified even if unnoticed during physical play.

**Why this priority**: Ensuring absolute rule compliance without constant manual refereeing is a primary value proposition of the automated platform.

**Independent Test**: Provide the validation parser with a synthetic sequence of game actions where one action clearly violates a known rule (e.g., moving further than a unit's Movement allowance).

**Acceptance Scenarios**:

1. **Given** a transcribed move action for a unit, **When** evaluated against the active ruleset, **Then** the parser successfully identifies if the distance moved exceeds the legal parameter.
2. **Given** an action attempting to shoot a weapon in an illegal phase (e.g., Melee phase), **When** evaluated, **Then** the parser flags the action as a rules violation with a specific citation.

---

### User Story 2 - Augment Game State with Rules Text (Priority: P2)

As a judge reviewing a flagged action, I want the system to provide the exact text of the rules involved so that I can quickly verify the context before making a ruling.

**Why this priority**: Judges need rapid access to the "why" behind an automated flag to make binding human decisions during dispute resolution.

**Independent Test**: Assert that generated validation flag objects contain attached contextual text fetched from the active rules dictionary.

**Acceptance Scenarios**:

1. **Given** an automatically flagged rules violation, **When** presented to a judge, **Then** the flag includes the verbatim text describing the broken rule.

### Edge Cases

- What happens if the transcript is ambiguous about standard measurement states (e.g., "moved exactly 6 inches" vs "moved about 6 inches")? (System flags ambiguity for manual review, rather than strictly violating).
- What happens if the rules database lacks data on a newly released faction? (System must fail gracefully, alerting the user that the faction is unverified).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST process sequenced game actions and query the active rules database for compliance parameters.
- **FR-002**: System MUST detect impossible state transitions, such as acting out of turn phase order.
- **FR-003**: System MUST identify physical violations based on unit statistics (Movement values, Weapon ranges).
- **FR-004**: System MUST attach specific source rule citations to any generated violation flag.
- **FR-005**: System MUST differentiate between "Hard Violations" (mathematically impossible moves) and "Soft Inconsistencies" (ambiguous declarations).

### Key Entities

- **Action Sequence**: A chronological list of game actions submitted for review.
- **Validation Flag**: An alert raised against a specific action containing the violation type and rules citation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System successfully detects 100% of priority 1 violations (distance, phase order, line of sight assumptions) in synthetic benchmark tests.
- **SC-002**: Verification processing latency is less than 1.0 seconds per standard logical action block.
- **SC-003**: System generates zero "Hard Violation" false positives on a known verified dataset of legal competitive matches.
