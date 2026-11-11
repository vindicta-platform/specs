# Feature Specification: 002-dice-core

**Feature Branch**: `002-dice-core`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Secure, non-manipulable RNG for competitive tabletop gaming with cryptographic proofs."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Randomness Generation (Priority: P1)

As a competitive player or tournament organizer, I need dice rolls to be truly random and securely generated so that neither side can predict or manipulate the outcomes.

**Why this priority**: Cryptographically secure randomness is the foundational requirement for competitive integrity in the platform.

**Independent Test**: Can be tested by generating a large statistical sample of rolls and verifying uniform distribution.

**Acceptance Scenarios**:

1. **Given** a request for a random integer within a range, **When** the core engine processes it, **Then** it produces the result in a completely unpredictable manner.
2. **Given** multiple sequential roll requests, **When** they are generated, **Then** the sequence represents a statistically uniform distribution without repeating patterns.

---

### User Story 2 - Verifiable Entropy Proofs (Priority: P1)

As an auditor or skeptical player, I want to mathematically verify that a specific dice roll was generated fairly using the stated seed, so I can trust the platform's integrity.

**Why this priority**: In online competitive wargaming, "trust but verify" is essential. Providing verifiable proofs proves the platform is not altering rolls.

**Independent Test**: Can be tested by taking the output proof and verifying it independently using standard cryptographic algorithms.

**Acceptance Scenarios**:

1. **Given** a generated diceroll, **When** the result is returned, **Then** it includes a mathematical proof based on its initial entropy state.
2. **Given** a roll result and its proof, **When** an external auditor evaluates them, **Then** the auditor can mathematically confirm the outcome was derived fairly.

### Edge Cases

- What happens if the system requests an excessively large range of numbers (e.g., 1 to 1 billion)? (System should handle large boundaries securely).
- How handles identical entropy submissions from malicious clients? (System must ensure non-reproducibility of identical states without authorization).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST utilize cryptographically safe algorithms for all randomization operations.
- **FR-002**: System MUST generate and return a verifiable proof of generation alongside every roll result.
- **FR-003**: System MUST NOT rely on potentially predictable sources such as raw system time.
- **FR-004**: System MUST allow deterministic states purely for automated testing environments, but strictly prevent it in production contexts.

### Key Entities

- **Roll Entropy**: Represents the mathematical state and proof data associated with a generated random value.
- **Random Result**: Contains the generated outcome along with the `Roll Entropy` ensuring its validity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Randomness passes standard statistical security suites with >99% confidence intervals.
- **SC-002**: 100% of generated rolls contain a verification payload that can be independently audited.
- **SC-003**: Generation of a single random value with its associated verification proof takes less than 1 millisecond.

## Clarifications *(proposed 2026-11-11, awaiting approval)*

These resolve ambiguities found when the two existing implementations were read against this spec
(https://github.com/vindicta-platform/vindicta-foundation/issues/52, https://github.com/vindicta-platform/vindicta-engine/issues/21, https://github.com/vindicta-platform/vindicta-engine/issues/22). Status stays Draft until they are approved.

- **C-001 (User Story 2, FR-002): the proof binds the result.** A proof is valid only if every returned value can be recomputed from the committed seed, the context and the value's position. Showing that a seed matches a commitment is not enough.
- **C-002 (FR-002): the commitment comes first.** The commitment is given to the other party before any external input that could influence the outcome is fixed. The seed is chosen before its commitment is generated, kept secret, and revealed afterwards.
- **C-003 (User Story 1, SC-001): the mapping to a range is exactly uniform.** Reducing random bits with a remainder is not acceptable unless the bit range is an exact multiple of the die range. Uniformity of the mapping is shown by an exhaustive check at reduced width, not by sampling alone.
- **C-004 (Edge Case 1): range limits.** The lower bound is at least 1, the upper bound is above the lower bound, the count is at least 1, and the inclusive range contains at most 2^32 values (`upper - lower + 1 <= 2^32`). Anything else is refused with a validation error.
- **C-005 (FR-004): the deterministic mode is unreachable in production.** It requires an explicit testing mode. Supplying a seed in production mode is an error, and no production code path constructs the deterministic generator.
- **C-006 (SC-001): what the statistical check is.** A fixed-seed distribution test with a stated sample size and threshold, repeatable run to run. It supports the uniformity claim; C-003 carries it.
- **C-007 (SC-003): the 1 ms budget is reported, not gated,** until a baseline measurement exists on the reference CI runner.
- **C-008: one implementation.** The dice core has a single implementation, in vindicta-foundation. Other packages import it.

## Acceptance Scenarios in Gherkin *(proposed)*

```gherkin
Feature: Dice core (spec 002)

  Scenario: Values are in range
    Given a request for a count of values between a lower and an upper bound
    When the roll is produced
    Then exactly that count of values is returned
    And every value is between the bounds inclusive

  Scenario: The proof binds the roll (C-001)
    Given a roll result with its proof and its revealed seed
    When an auditor recomputes each value from the seed, the context and its position
    Then verification succeeds only when the proof and commitment validate and the recomputed values equal the returned values

  Scenario: An altered value fails verification (C-001)
    Given a valid roll result
    When any single value is changed
    Then verification fails

  Scenario Outline: An altered seed, commitment or context fails verification
    Given a valid roll result
    When the <field> is changed
    Then verification fails
    Examples:
      | field      |
      | seed       |
      | commitment |
      | context    |

  Scenario: The commitment comes first (C-002)
    Given the context and other outcome-influencing inputs have not been fixed
    When the commitment is given to the other party before those inputs are fixed, the roll is produced, and the seed is revealed
    Then the commitment recomputed from the revealed seed equals the one given

  Scenario: The mapping is exactly uniform (C-003)
    Given the function that maps random bits to a range
    When it is evaluated over every input at a reduced bit width for each die size under test
    Then at least one input is accepted and every face is produced the same positive number of times
    And rejected inputs are counted separately

  Scenario: Production refuses a seed (C-005)
    Given production mode
    When an engine is requested with a seed
    Then a security error is raised
    And no engine is returned

  Scenario: Testing mode is repeatable (FR-004)
    Given testing mode and a fixed seed
    When the same sequence of rolls is requested twice
    Then both sequences are identical

  Scenario: An out-of-range request is refused (C-004)
    Given a lower bound below 1, an upper bound not above the lower bound, a count below 1, or a range wider than 2^32
    When a roll is requested
    Then a validation error is raised
```
