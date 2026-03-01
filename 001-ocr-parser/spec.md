# Feature Specification: 001-ocr-parser

**Feature Branch**: `001-ocr-parser`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Automated ingestion of Warscribe screenshots."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Process Digital Scorecards (Priority: P1)

Users need to supply a screenshot of a completed match from official scoring apps and receive structured, machine-readable data containing all scores, objectives, and metadata.

**Why this priority**: Enables automated ingestion of scorecards into the overarching platform, bypassing manual data entry.

**Independent Test**: Can be fully tested by providing a standard scorecard screenshot, running the parser, and asserting the output data perfectly matches the visual information.

**Acceptance Scenarios**:

1. **Given** a clear screenshot of a 2-player match scorecard, **When** the image is processed by the parser, **Then** it produces a document with the correct date, players, final scores, and winner.
2. **Given** a scorecard containing specific secondary objective names and per-round scores, **When** processed, **Then** the result contains those exact objectives, matched to the correct player, with the correct round-by-round sequences.

---

### User Story 2 - Process Physical Scorecards (Priority: P2)

Users need to scan or photograph standard paper score sheets provided at tournaments and extract the same level of structured data.

**Why this priority**: Many large tournaments still rely on physical paper traces for primary record keeping.

**Independent Test**: Can be tested by providing high-resolution photographs of filled-out standard score sheets and verifying extraction accuracy.

**Acceptance Scenarios**:

1. **Given** a well-framed photograph of a standard paper scorecard, **When** processed, **Then** the platform successfully extracts the handwritten or marked objective scores.

### Edge Cases

- What happens when an image is blurry or has low resolution? (System should reject or provide partial data with low confidence warnings).
- How does the system handle non-standard scorecard layouts? (Explicit failure/error if canonical structure isn't detected).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept standard image files.
- **FR-002**: System MUST output structured data containing all match metrics.
- **FR-003**: System MUST accurately extract the overarching match metadata (Date, Ruleset, Match Type, Final Scores, Winner).
- **FR-004**: System MUST accurately partition data by Player, extracting Faction.
- **FR-005**: System MUST extract both the Primary and Secondary objectives, capturing point values per round.
- **FR-006**: System MUST run locally on user devices without depending on external cloud vision services.

### Key Entities

- **Match Record**: The root document containing match metadata and player results.
- **Player Record**: Contains player-specific context and a collection of scored objectives.
- **Objective Score**: A specific scored mechanic, tracked across game rounds, with a final total.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The parser achieves 100% data extraction accuracy on high-quality, uncropped baseline screenshots of official scoring apps.
- **SC-002**: Image processing and data generation completes in under 5.0 seconds per image on standard consumer hardware.
- **SC-003**: The resulting data schema maps 1:1 with the expected data structures required by downstream platform services.
