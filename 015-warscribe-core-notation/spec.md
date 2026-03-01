# Feature Specification: 015-warscribe-core-notation

**Feature Branch**: `015-warscribe-core-notation`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "The definitive grammar syntax for writing tabletop battle reports."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Standardized Match Recording (Priority: P1)

As a competitive player or tournament organizer, I want a standardized, human-readable shorthand notation for recording match events so that anyone on the platform can understand exactly what happened during a game.

**Why this priority**: WARScribe requires a universal "language" to function. This definition is the foundation for all subsequent parsing, validation, and replay systems.

**Independent Test**: Provide 5 players with the notation guide and ask them to transcribe a brief combat sequence. Determine if the resulting strings accurately define the event without subjective variations.

**Acceptance Scenarios**:

1. **Given** a player wants to record a unit moving, **When** they use the notation, **Then** the shorthand (`A:Move[UnitX, 6in]`) is unambiguous and consistently applied.

---

### User Story 2 - Automated Transcription Conversion (Priority: P2)

As a developer building the ingestion pipeline, I need a strictly defined grammar mapping so that I can confidently build parsers that convert human shorthand into structured platform data objects.

**Why this priority**: Parsers cannot interpret ambiguity. The rules of the notation must be mathematically precise.

**Independent Test**: Develop a parser adhering perfectly to the grammar spec. Run thousands of generated valid notations through it and verify 100% structured data equivalence.

**Acceptance Scenarios**:

1. **Given** a parsed notation sequence representing a full turn, **When** processed by the downstream engine, **Then** the sequence perfectly reconstructs the described logical game state.

### Edge Cases

- What happens if a player misspells a unit name in the notation? (The standard defines "fuzzy matching" bounds or requires strict roster-imported GUIDs rather than raw strings).
- How does the grammar handle deeply nested simultaneous actions (e.g., three separate units resolving combat at the same physical time)? (Notation must include explicit sequential or simultaneous block delimiters).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define a complete, documented grammar capable of describing all standard tabletop wargaming actions (Movement, Shooting, Melee, Scoring, Morale).
- **FR-002**: System MUST structure the syntax specifically for minimizing keystrokes while maintaining human legibility.
- **FR-003**: System MUST provide structural definition for metadata blocks mapping generic token names to strictly defined active roster entities.
- **FR-004**: System MUST supply an exhaustive reference document detailing expected grammatical behavior.

### Key Entities

- **WARScribe Syntax Grammar**: The formal, mathematically defined ruleset dictating valid notation structure.
- **Lexicon Dictionary**: The reference manual mapping specific platform actions to shorthand tokens.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The notation successfully and unambiguously represents 100% of actions available in standard competitive matches for supported game systems.
- **SC-002**: An average user can manually transcribe a standard 2000-point physical match using the syntax strictly within a 15-minute post-game window.
- **SC-003**: The defined grammar proves robust enough to parse cleanly into an Abstract Syntax Tree without unresolvable ambiguities.
