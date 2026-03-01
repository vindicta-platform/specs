# Feature Specification: 042-i18n-support

**Feature Branch**: `042-i18n-support`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Architecture for multi-language rulesets and interface support."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Language Rules Lookup (Priority: P1)

As a non-English speaking player (e.g., Spanish speaking), I want to see all unit stats and special rules in my native language so that I can play accurately without mental translation overhead.

**Why this priority**: Wargaming is a global hobby. Localization is the single largest barrier to entry outside the US/UK markets.

**Independent Test**: Switch the platform language to "German." Load a standard roster. Verify that unit names, ability descriptions, and weapon profiles are displayed in grammatically correct German.

**Acceptance Scenarios**:

1. **Given** a rules database containing multiple localized strings, **When** a user's profile is set to "French," **Then** all Oracle rule lookups return the French variant of the rule text by default.

---

### User Story 2 - Right-to-Left (RTL) Layout Support (Priority: P2)

As a player using an RTL language (e.g., Arabic), I want the entire platform interface (text alignment, sliders, button positions) to flip correctly so that the app feels natural to use.

**Why this priority**: True internationalization requires structural layout flexibility, not just text translation.

**Independent Test**: Toggle the UI to an RTL language. Verify that the "Profile" side-menu moves to the right and text flow starts from the right margin without visual clipping.

**Acceptance Scenarios**:

1. **Given** an active match dashboard, **When** switched to an RTL locale, **Then** all logical "Forward" and "Back" UI directions are mirrored to match linguistic expectations.

### Edge Cases

- What happens if a specific rule hasn't been translated yet? (System MUST fall back to the "Source" language [usually English] while visually flagging the entry as "Pending Translation").
- How handles mixed-language matches (e.g., Player A is in Spanish, Player B is in English)? (The system must allow both players to view the same match state in their respective preferred languages simultaneously).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support storage and retrieval of localized rule strings for all core game entities.
- **FR-002**: System MUST detect and apply user-specific locale preferences across all interface layers.
- **FR-003**: System MUST provide automatic structural mirroring for Right-to-Left (RTL) language locales.
- **FR-004**: System MUST implement a "Deterministic Fallback" chain for missing translations (Asset -> Locale -> Language Group -> Source).
- **FR-005**: System MUST allow community-contributed translation "Packs" for minor languages not officially supported by publishers.

### Key Entities

- **Localization Token**: A unique pointer to a piece of content that resolves to different text based on the active locale.
- **Locale Context**: The unified settings object (Language, Region, Directionality) for a user session.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Language switching completes and re-renders the active UI in < 1.0 second.
- **SC-002**: 100% of "Critical Path" UI elements (Join Match, Score, Profile) have verified translations for Tier-1 languages.
- **SC-003**: Rules lookup latency for localized text is identical to source-language lookup (no performance penalty for "Foreign" keys).
