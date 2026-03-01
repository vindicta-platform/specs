# Feature Specification: FEAT-038 List Archetype Identification

**Feature Branch**: `038-archetype-id`  
**Created**: 2026-02-28  
**Status**: Draft  
**Input**: User description: "Advance meta analysis capabilities."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Roster Tagging (Priority: P1)
As a meta analyst, I want uploaded rosters to be automatically tagged with their strategic archetype (e.g., "Horde", "Vehicle Skew", "MSU", "Deathstar"), so that I can filter win-rates by playstyle rather than just faction.
**Why this priority**: Faction win-rates are too broad. Archetypes define the true meta.
**Independent Test**: Can be tested by uploading 10 known "Vehicle Skew" lists and verifying the classifier tags at least 9 of them correctly.

**Acceptance Scenarios**:
1. **Given** a parsed roster containing 80% points invested in Vehicles/Monsters, **When** ingested by the Oracle, **Then** it is tagged with "Vehicle Skew".

### User Story 2 - Archetype Matchup Matrix (Priority: P2)
As a competitive player, I want to see a matrix showing how my archetype performs against other archetypes, so I know my bad matchups before a tournament.
**Why this priority**: High-value insight for subscription users.
**Independent Test**: Can be tested by querying the aggregated statistics and verifying the UI plots the cross-archetype win percentages.

**Acceptance Scenarios**:
1. **Given** sufficient match data, **When** viewing the Meta Dashboard, **Then** a heat-matrix displays Win Rates of (Row Archetype) vs (Col Archetype).

### Edge Cases
- What if a list fits multiple archetypes? (Support primary and secondary archetype tags).
- How are new meta-shifts handled? (Unsupervised clustering periodically runs to identify emerging untagged archetypes).

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The Meta-Oracle MUST analyze incoming parsed rosters and apply one or more semantic tags.
- **FR-002**: The classification logic MUST use configurable rules (e.g., `if count(units with MODEL_COUNT > 20) >= 3 -> "Horde"`).
- **FR-003**: The system MUST expose an API endpoint to query win-rates filtered by these tags.

### Key Entities
- **ArchetypeDefinition**: The rule-based or ML-based criteria defining a strategy.
- **RosterTag**: The mapping of an archetype to a specific submitted list.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: 95% of parsed lists are successfully assigned at least one archetype tag.
- **SC-002**: The Archetype Classification executes synchronously during list upload (< 200ms).
