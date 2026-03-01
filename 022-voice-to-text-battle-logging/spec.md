# Feature Specification: 022-voice-to-text-battle-logging

**Feature Branch**: `022-voice-to-text-battle-logging`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Hands-free match transcription using voice commands."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hands-Free Action Logging (Priority: P1)

As a player in a dense physical match, I want to speak my actions aloud (e.g., "Unit A moves 5 inches") and have them automatically converted into WARScribe notation so that I don't have to touch a device during play.

**Why this priority**: Wargaming involves handling models and dice; requiring a player to type into a phone is a massive barrier to transcript adoption. Voice is the "killer app" for data ingestion.

**Independent Test**: Provide a headset and speak a sequence of 10 standard WARScribe commands. Verify the system converts them into the exact required shorthand string with > 90% accuracy.

**Acceptance Scenarios**:

1. **Given** a noisy tournament hall environment, **When** a player speaks a command clearly into a microphone, **Then** the system filters background noise and correctly identifies the intentional command.
2. **Given** a command involving a complex unit name (e.g., "Roboute Guilliman"), **When** spoken, **Then** the system uses the active match roster's context to correctly map the phonetic sound to the intended entity ID.

---

### User Story 2 - Real-Time Command Confirmation (Priority: P2)

As a player using voice, I want to hear/see a non-intrusive confirmation that my command was understood correctly, so that I can fix errors immediately rather than at the end of the match.

**Why this priority**: Voice recognition error rates are real. Low-friction feedback loops prevent corrupted match history.

**Independent Test**: Speak an intentional command and verify a visual or auditory "success" signal triggers within the defined latency limit.

**Acceptance Scenarios**:

1. **Given** a misunderstood command, **When** the system fails to map it to a valid WARScribe grammar, **Then** it provides an immediate "Did you mean X?" or "Unrecognized command" alert.

### Edge Cases

- What happens if the local device loses internet connectivity during the voice transaction? (Speech-to-intent MUST happen locally on the ingestion device specifically to avoid tournament-hall Wi-Fi failures).
- How handles multiple voices (e.g., the opponent talking over the player)? (System must allow "Speaker Enrollment" or high-gain focus on the primary user's microphone).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST capture auditory input and convert it into text strings.
- **FR-002**: System MUST identify and map specific phonetic patterns to the WARScribe Grammar tokens.
- **FR-003**: System MUST utilize active match roster data to resolve entity name ambiguities (Fuzzy Name Matching).
- **FR-004**: System MUST process all voice-to-intent operations locally on the client device without mandatory cloud hop.
- **FR-005**: System MUST provide immediate feedback loops for successful or failed command recognition.

### Key Entities

- **Voice Command Intent**: The psychological action the user is trying to perform, represented by auditory data.
- **Logical Transcript Event**: The resulting WARScribe command generated from the successfully resolved intent.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System achieves > 95% word-error-rate accuracy on standard tabletop gaming command sets in controlled quiet environments.
- **SC-002**: "Speech-to-WARScribe" latency (from end-of-utterance to command generated) is < 750 milliseconds.
- **SC-003**: System correctly resolves 100% of unit names that exist on the active match's pre-loaded rosters.
