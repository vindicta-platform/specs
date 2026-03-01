# Feature Specification: 038-archetype-id

**Feature Branch**: `038-archetype-id`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: Established reference spec for archetype identification.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cross-System Archetype Recognition (Priority: P1)

As a multi-game player, I want the platform to recognize that "Aggro Melee" in Game A and "Swarm Combat" in Game B share a similar structural archetype so that my player profile reflects my consistent playstyle regardless of the specific ruleset.

**Why this priority**: Core to providing meaningful "Player Archetype" analytics and cross-game coaching.

**Independent Test**: Load two disparate rosters from different game systems. Verify that the Archetype Engine assigns correctly identified "Class Tags" (e.g., #Horde, #Elite, #GlassCannon) based on unit-level attribute distributions.

**Acceptance Scenarios**:

1. **Given** a roster consisting of 80% low-cost, high-velocity units, **When** processed by the engine, **Then** it is assigned the "Swarm" archetype ID global tag.

---

### User Story 2 - Roster Comparison & Meta Analysis (Priority: P2)

As a tournament analyst, I want to see which archetypes are currently dominating the competitive meta, rather than just which factions, so that I can provide deeper strategic commentary.

**Why this priority**: Faction names (e.g., "Space Marines") obscure the actual *way* the army plays. Archetype IDs reveal the underlying mechanical trends.

**Independent Test**: Aggregate 100 tournament rosters. Verify that the dashboard can group them by Archetype ID (e.g., 20% "Castle", 40% "Alpha Strike") with 100% accuracy based on the defined heuristic thresholds.

**Acceptance Scenarios**:

1. **Given** a collection of top-performing rosters, **When** grouped by Archetype, **Then** the system identifies which archetype ID has the highest win rate across all factions.

### Edge Cases

- What happens if a roster fits two archetypes equally (e.g., Hybrid)? (System must allow "Multi-Tagging" or identify a "Primary" and "Secondary" archetype ID).
- How handles new unit types that haven't been categorized? (System defaults to a "Generalist" archetype until enough sample data exists to trigger a heuristic classification).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a global registry of standardized Archetype IDs (e.g., Swarm, Elite, Gunline).
- **FR-002**: System MUST analyze roster data-models to identify underlying mechanical signatures.
- **FR-003**: System MUST provide deterministic mapping between unit-level attributes and archetype categories.
- **FR-004**: System MUST expose archetype metadata to other platform services (Analytics, Anti-Cheat, Matchmaking).

### Key Entities

- **Archetype ID**: The unique platform identifier for a specific playstyle signature.
- **Heuristic Signature**: The mathematical definition of unit distributions that trigger an archetype identification.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Archetype classification of a 2000-point roster completes in < 100 milliseconds.
- **SC-002**: Recursive metadata identification achieves > 90% correlation with human-expert "Playstyle" labels in test datasets.
- **SC-003**: 100% of rosters in the platform database are assigned at least one Primary Archetype ID.
