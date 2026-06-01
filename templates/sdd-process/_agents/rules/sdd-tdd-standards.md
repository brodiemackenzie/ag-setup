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
