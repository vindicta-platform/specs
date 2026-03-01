# Feature Specification: 039-faq-scraper

**Feature Branch**: `039-faq-scraper`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Ingesting official and community FAQs for rules resolution."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Rule Corrections (Priority: P1)

As a player, I want the platform's rules database (Oracle) to automatically update when an official publisher releases a new FAQ document, so that I'm never checking out-of-date rules during a match.

**Why this priority**: Competitive integrity relies on playing the "latest" version of the rules. Manual updates are slow and prone to human error.

**Independent Test**: Provide an official PDF or URL of a new rules errata. Verify the "Scraper" identifies the changed text, parses the specific unit affected, and updates the platform's active rule state within the defined time limit.

**Acceptance Scenarios**:

1. **Given** a new FAQ document stating "Unit X's Move is now 6 inches (was 5)," **When** scraped, **Then** all subsequent rosters generated correctly reflect the 6-inch movement stat.

---

### User Story 2 - Source Attribution & Verification (Priority: P2)

As a judge, I want to see exactly which FAQ document or community ruling a specific rule change came from so that I can verify its legality for a specific tournament.

**Why this priority**: Not all FAQs are "official." Different tournaments use different community FAQ sets. Clarity on source is essential for judge dispute resolution.

**Independent Test**: Hover over a modified rule in the Oracle view. Verify the system displays a clear link or reference ID to the source document ingested by the scraper.

**Acceptance Scenarios**:

1. **Given** a rule ingested from a "Community FAQ," **When** viewed in the platform, **Then** it is visually tagged as "Non-Official" with a timestamp and source link.

### Edge Cases

- What happens if a new FAQ contradicts an older one? (Scraper must implement "Date-Based Precedence," where the most recently published document overwrites older conflicting entries).
- How handles complex diagram-based FAQs? (Scraper MUST flag "Image-Based Rulings" for manual human review rather than attempting to guess geometric intent).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST identify and ingest text-based rule changes from specified external sources (PDF, Web).
- **FR-002**: System MUST parse natural language "Q&A" formats into structured rule modifications (Overrides).
- **FR-003**: System MUST maintain a versioned history of every rule change with its associated source attribution.
- **FR-004**: System MUST allow TOs to "Toggle" specific FAQ sources on or off for their specific events.
- **FR-005**: System MUST identify "High-Conflict" ingestion entries and flag them for manual administrator verification.

### Key Entities

- **FAQ Source**: The digital location or document being monitored for updates.
- **Rule Override**: The discrete data object modifying a base rule in the Oracle database.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System detects a new document publication on a monitored source within 4 hours.
- **SC-002**: Conversion from "FAQ Document" to "Oracle Rule Revision" (for clear text) is > 95% accurate without human intervention.
- **SC-003**: 100% of ingested rules are assigned a permanent, non-deletable Source URI.
