# Feature Specification: 025-ar-table-overlay

**Feature Branch**: `025-ar-table-overlay`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Augmented reality visual aids for measurement and line-of-sight."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Augmented Line-of-Sight (Priority: P1)

As a player in a complex urban terrain environment, I want to use my AR-enabled device to see exactly what my model "sees" from its eyes so that debates about line-of-sight are settled instantly and objectively.

**Why this priority**: LOS arguments are the single most frequent cause of judge calls and player friction in physical wargaming. Digital measurement removes subjectivity.

**Independent Test**: Place two models in a terrain setup where LoS is "borderline." View through the AR overlay. Verify the system draws a "Green" or "Red" line based on strict calculated geometry.

**Acceptance Scenarios**:

1. **Given** a clear visual path between two recognized models, **When** viewed through the AR lens, **Then** the platform renders a "Valid Shot" indicator.
2. **Given** a model partially obscured by terrain, **When** viewed, **Then** the AR overlay correctly identifies the percentage of the model visible and calculates if it meets the "Cover" rule threshold.

---

### User Story 2 - Aura and Thread visualization (Priority: P2)

As a player with complex buff ranges (auras), I want to see a ghostly circle around my leader unit indicating exactly how far their influence extends so I can position units perfectly.

**Why this priority**: Managing "6-inch auras" manually requires constant measuring and guesswork. Visualizing them in 3D space improves tactical precision.

**Independent Test**: Activate an aura effect on a unit. Move the unit physically. Verify the AR overlay "ghost circle" moves in real-time with the physical model.

**Acceptance Scenarios**:

1. **Given** a Captain unit with a 6-inch reroll aura, **When** viewed in AR, **Then** a semi-transparent sphere or circle of exactly 6-inch radius is projected around the model's base.

### Edge Cases

- What happens when a model is accidentally nudged slightly? (The AR system must support "snap back" or "re-calibration" of the digital twin to the physical model's new location).
- How handles multiple players walking around the table with different AR perspectives? (The table state must be a "Single Source of Truth" cloud anchor so all viewers see the same digital objects at the same physical locations).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support high-precision tracking of physical game objects (Model Bases, Terrain) in 3D space.
- **FR-002**: System MUST calculate and render line-of-sight vectors between any two designated game entities.
- **FR-003**: System MUST project 3D visual manifestations (spheres, rings) representing logical game distances.
- **FR-004**: System MUST allow users to measure distances arbitrarily between two physical points in the AR view.
- **FR-005**: System MUST synchronize the shared table state across all active viewers at a single match.

### Key Entities

- **Table Anchor**: The physical origin point (usually a QR code or mat corner) binding the digital coordinate system to reality.
- **Digital Twin**: The virtual representation of a physical model used for geometric calculation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Measurement accuracy error is < 2.0 millimeters compared to a physical tape measure in optimal lighting.
- **SC-002**: AR overlays maintain "stickiness" at < 50ms of jitter when moving the camera around the physical table.
- **SC-003**: Shared table state propagates to second and third viewers in < 500 milliseconds.
