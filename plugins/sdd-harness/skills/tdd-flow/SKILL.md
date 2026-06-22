---
name: tdd-flow
description: Enforce strict Test-Driven Development (TDD) Red-Green-Refactor cycles and loop-escape escalation safety.
---

# TDD Flow Playbook

You must act strictly as the **sdd-implementor** (profile `agents/sdd-implementor.json`) in this sandboxed workspace.

---

## Playbook Execution

### 1. Loop Initialization
*   Locate the active task card in `docs/sdd/ep-*/ft-*/TASKS.md`.
*   Maintain a local retry counter (starts at 0).

### 2. Execution Phases

#### Phase A: RED (Write Failing Test)
1.  Navigate to the tests folder (e.g. `tests/unit/` or `tests/integration/`).
2.  Write a minimal test case representing the BDD `Given/When/Then` scenarios defined for the active task.
3.  **Execute the test runner** (e.g. `pytest` or `npm test`) using `run_command`.
4.  Verify that the test fails with the expected failure signature.
5.  **Do not proceed to production code until you have a failing test.**

#### Phase B: GREEN (Write Minimal Production Code)
1.  Implement the minimal code necessary to make the failing test pass.
2.  **Execute the test runner**.
3.  If the test suite passes, proceed to Refactoring.
4.  If the test suite fails:
    *   Increment the retry counter.
    *   If the retry counter is less than 3:
        *   Surgically adjust the production code or mock details.
        *   Re-run the test suite.
    *   If the retry counter reaches 3:
        *   **Halt execution immediately.**
        *   Write a summary file `docs/sdd/ep-<epic>/ft-<feature>/failed_test_summary.md` detailing:
            *   The failing test signature and traceback.
            *   The code adjustments made in the 3 failed attempts.
            *   Your hypothesis on the root cause.
        *   Notify the user: *"Reached max retry limit of 3 for <task>. I have compiled failed_test_summary.md. Halting execution for guidance."*
        *   Stop calling tools and wait for user instruction.

#### Phase C: REFACTOR (Code Cleanup)
1.  Clean up code layout, variable scopes, and confirm all methods contain strict Google style docstrings.
2.  Re-run the test suite to confirm it remains GREEN.
3.  **Physical Proof**: Display the successful passing test runner output log directly in your text response to the user.
4.  Update `TASKS.md` to check off the active task card: `- [x] tsk-<name>`.
5.  Proceed to the next task card.
