# Feature Specification: 046-roster-synergy

**Feature Branch**: `046-roster-synergy`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Identifying cross-unit buffs and rule interactions in a roster."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Roster Buff-Stacking Identification (Priority: P1)

As a competitive player, I want to see a "Synergy Map" showing which units in my roster can buff others (e.g., "Leader A provides +1 to hit for Unit B"), so that I don't build a list with conflicting or redundant bonuses.

**Why this priority**: High-level wargaming is won by stacking buffs. Visualizing these relationships prevents "Illegal" or "Sub-optimal" lists from reaching the table.

**Independent Test**: Load a roster with a Leader and 3 different infantry units. Verify the synergy enging identifies and draws "Connection Lines" between the Leader and exactly the units that share the required "Keyword" for its buff.

**Acceptance Scenarios**:

1. **Given** a unit with a "Reroll 1s" aura, **When** reviewing the roster dashboard, **Then** all units within the same Detachment that benefit from the aura are highlighted in a "Synergy Group."

---

### User Story 2 - Conflict and Redundancy Detection (Priority: P2)

As a tournament organizer, I want the system to flag if a player has two units providing the exact same "Non-Stacking" buff, so that I can warn them their list is inefficient or potentially illegal according to "Rule of One" constraints.

**Why this priority**: Automating the detection of "Redundant Layering" saves players from bad game experiences and TOs from tedious list-checking.

**Independent Test**: Add two Captains (both providing an identical "Aura") to the same army list. Verify the system flags this as a "Redundant Syngery" with a warning explanation.

**Acceptance Scenarios**:

1. **Given** two rules that grant the same keyword (e.g., "Feel No Pain 5+"), **When** applied to the same unit, **Then** the platform identifies the overlap and notifies the player that only the strongest/first rule applies.

### Edge Cases

- What happens with "Conditional" synergies (e.g., "Only if within 3 inches of Terrain X")? (Synergy engine MUST categorize these as "Contextual Synergies" and highlight them only during active match play, not during static list building).
- How handles keyword-obfuscation? (System MUST use the Oracle's "Keyword-Synonym" database to link "Loyalist" and "Space Marine" if they are logically identical in the ruleset).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST identify and map directional relationships (Source -> Target) for all unit-level rules and buffs.
- **FR-002**: System MUST identify "Keyword Dependencies" required for rule activation.
- **FR-003**: System MUST identify and flag redundant buff applications (Non-Stacking rules).
- **FR-004**: System MUST visualize synergy relationships as a "Network Graph" or "Interdependency List."
- **FR-005**: System MUST update synergy calculations in real-time as units are added or removed during roster construction.

### Key Entities

- **Synergy Path**: The logical connection between a Rule Provider and a Rule Recipient.
- **Rule Constraint**: The condition (Keyword, Distance, Phase) required for the synergy to exist.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Synergy graph for a standard 2000-point roster (20-30 units) calculates in < 250 milliseconds.
- **SC-002**: 100% of "Rule of One" (non-stacking) violations are identified in synthetic test rosters.
- **SC-003**: Identifying synergy paths for "Complex Keyword" chains (3+ hops) achieves 100% accuracy compared to manual rulebook cross-referencing.
