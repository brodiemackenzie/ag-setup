---
trigger: always_on
description: Enforce strict TDD Red-Green-Refactor execution loops, test decoupling, and Google docstring hygiene.
---

# SDD TDD & Code Documentation Rules

You must maintain absolute engineering rigor and code documentation standards:

## 1. Strict TDD Red-Green-Refactor Loops
Coder agents must strictly follow the Test-Driven Development (TDD) execution cycle:
1. **RED**: Write a minimal failing test first (under `tests/unit/` or `tests/integration/`). Execute the test suite using the test runner and verify the RED failure output.
2. **GREEN**: Implement the minimal production code necessary to get the test to pass. Verify success.
3. **REFACTOR**: Clean up code layout and variable scopes, confirming that all tests remain green.
* **No Blind Completes**: You are strictly forbidden from marking task checkboxes complete or ending your turn declaring a task finished without physically running the tests and showing the successful passing logs directly in your conversation transcript.

## 2. Hermetic Test Isolation
All test suites must be fully hermetic:
* **No Network Sockets**: You are strictly forbidden from writing tests that open active network sockets or make live HTTP calls to external internet endpoints. All external APIs and services must be fully mocked.
* **Unit Tests (`tests/unit/`)**: Must run in under 10ms, rely 100% on mock interfaces, and perform zero local file or database operations.
* **Integration Tests (`tests/integration/`)**: Must execute within isolated sandboxes (e.g., SQLite in-memory databases).

## 3. Google docstring compliance
* **Mandatory Documentation**: Every public module, class, and method (excluding trivial getters/setters) must contain a strict Google Style docstring detailing a concise capitalized summary, explicit `Args`, `Returns`, and `Raises` exception conditions.
* **Inline comment Hygiene**: You are strictly forbidden from writing inline comments that restate syntax or explain obvious logical flows (e.g. `# loop over list`). Inline comments are allowed exclusively to document *non-obvious decisions* or upstream library workarounds.

## 4. TDD Loop Escape & Process Boundaries
To prevent infinite token burn and maintain specification alignment, you must adhere to these loop escape limits:
*   **Max TDD Retries**: You are allowed a maximum of **3 consecutive retries** to fix code for a single task after a test failure.
*   **Strict Process Boundaries (No Cheating)**: The TDD execution loop and retry limits apply strictly to editing **project application code** and **local test suites** to satisfy specs. You are **strictly prohibited** from altering specifications (`SPEC.md` / `DESIGN.md` / `TASKS.md`), rules (`.agents/rules/`), or playbooks (`.agents/skills/`) to force tests to pass. Any specification discrepancies must trigger immediate escalation to the user.
*   **Halt & Escalate**: If the test suite fails on the 3rd attempt:
    1.  Halt the TDD loop immediately.
    2.  Write a summary file `docs/sdd/ep-<epic>/ft-<feature>/failed_test_summary.md` detailing:
        *   The task slug under work.
        *   The exact failing test traceback.
        *   A summary of changes made in the 3 failed attempts.
        *   Your hypothesis on why the test is failing (e.g. library credential needs, mock returns mismatches).
    3.  Report the failure to the user in chat: *"I have reached the max retry limit of 3 for <task_slug>. I have compiled a failed test summary. Please inspect the code or provide guidance on how to resolve the test failure."*
    4.  Stop calling tools and await user instructions.

