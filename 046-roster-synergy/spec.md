# Feature Specification: FEAT-046 Roster Synergy Scoring System

**Feature Branch**: `046-roster-synergy`  
**Created**: 2026-02-28  
**Status**: Draft  
**Input**: User description: "Advance meta analysis capabilities."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Synergy Detection (Priority: P1)
As a list builder, I want the system to highlight units in my roster that have overlapping buffs (e.g., Core units near Aura leaders), so I can see if my army is mathematically efficient.
**Why this priority**: Teaches players how to build better lists using platform intelligence.
**Independent Test**: Can be tested by submitting a list with a Character that buffs "CORE" units, alongside 3 "CORE" units, and asserting the Synergy Score is high.

**Acceptance Scenarios**:
1. **Given** a parsed list, **When** the Oracle evaluates it, **Then** it identifies pairings between Leader abilities and eligible targets, generating a synergy count.

### User Story 2 - Anti-Synergy Warnings (Priority: P2)
As a list builder, I want to be warned if I include a character whose buffs have no valid targets in my army, so I don't waste points.
**Why this priority**: Immediate, tangible value to the user during the list-building phase.
**Independent Test**: Can be tested by adding a Character buffing "VEHICLE" to a list with 0 Vehicles, verifying a warning is generated.

**Acceptance Scenarios**:
1. **Given** a list with orphaned buff capabilities, **When** evaluated, **Then** the UI flags an "Anti-Synergy" warning indicating wasted points.

### Edge Cases
- How does the system handle conditional synergies (e.g., buffs that only apply in melee)? (Calculate theoretical maximum output and display it as an "activation dependent" synergy).

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST query the RAG rules database to identify Aura and Buff abilities for units in the list.
- **FR-002**: The system MUST calculate the intersection of buff targets and army keywords.
- **FR-003**: The system MUST output a cohesive Synergy Index (0-100) based on points efficiency of buffs.

### Key Entities
- **SynergyGraph**: A relational mapping of which units in a list benefit from which rules.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: The platform correctly identifies 100% of explicit keyword-based synergies in a test batch of 50 lists.
- **SC-002**: Synergy evaluation APIs return results in under 1 second.
