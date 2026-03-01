# Feature Specification: 028-coaching-marketplace

**Feature Branch**: `028-coaching-marketplace`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Connecting top-tier players with students for tutoring sessions."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Tutoring Session Booking (Priority: P1)

As a player struggling with a specific faction, I want to find and book a coaching session with a verified pro player so that I can receive personalized feedback on my playstyle.

**Why this priority**: Monetizing expert knowledge creates a sustainable professional ecosystem for top players and provides a path for improvement for students.

**Independent Test**: Use a student account to search for "Space Marine Experts," find a coach, and book a 1-hour slot. Verify the appointment appears in both users' calendars.

**Acceptance Scenarios**:

1. **Given** a list of available coaches, **When** I filter by "Faction Proficiency," **Then** only coaches with a verified history of high-level performance with that faction are displayed.

---

### User Story 2 - Automated Session Payout (Priority: P2)

As a coach, I want to be paid automatically in platform Credits once a tutoring session is completed, so I don't have to chase students for payment.

**Why this priority**: Built-in trust via automated escrow is the primary reason to use the platform over informal external arrangements.

**Independent Test**: Complete a simulated session. Verify the "Credits" are deducted from the student and awarded to the coach (minus platform fee) automatically upon "Session Concluded" signal.

**Acceptance Scenarios**:

1. **Given** a booked session, **When** both users signal session completion, **Then** the economy engine executes the credit transfer atomically.

### Edge Cases

- What happens if one party fails to show up for a booked session? (System must implement a "dispute resolution" phase and "no-show" penalty fees stored in the economy layer).
- How are "Professional" coaches verified? (System must tie coach status to verifiable platform tournament results and a manual review of credentials).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a searchable directory of verified coaching professionals.
- **FR-002**: System MUST integrate with the Economy Engine for secure session booking and payout escrow.
- **FR-003**: System MUST provide an availability calendar management interface for coaches.
- **FR-004**: System MUST allow students to rate and review coaches post-session.
- **FR-005**: System MUST verify coach proficiency by linking their profile to their public tournament result certificates.

### Key Entities

- **Coaching Session**: The time-bound contract between a Coach and a Student.
- **Coach Profile**: The collection of credentials, availability, and reviews for a professional user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Booking a session and confirming escrow completes in < 3.0 seconds of user interaction.
- **SC-002**: Zero platform-side payment failure occurs across 10,000 simulated coaching transactions.
- **SC-003**: Profile search filters resolve in < 500 milliseconds across a database of 1,000 coaches.
