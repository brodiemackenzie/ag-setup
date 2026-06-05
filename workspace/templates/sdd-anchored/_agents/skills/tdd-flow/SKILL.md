# Test-Driven Development (TDD) Playbook

This playbook outlines the rigorous **Test-Driven Development (TDD)** engineering loops that the `sdd-implementor` agent must strictly execute for every task checkbox.

---

## Objective
Translate Technical Design verification strategies into hermetic, fully-automated unit and integration test suites, enforcing that code is only written to satisfy failing test cases.

---

## The Red-Green-Refactor TDD Loop

For every single task card in `TASKS.md`, you must execute this three-phase loop:

```
   [Identify Task in TASKS.md]
               │
               ▼
   1. RED: Write Failing Test
               │
               ▼
     [Run Test Suite ➔ FAIL]
               │
               ▼
   2. GREEN: Write Minimal Code
               │
               ▼
     [Run Test Suite ➔ PASS]
               │
               ▼
   3. REFACTOR: Clean Up Code
               │
               ▼
     [Run Test Suite ➔ PASS]
               │
               ▼
    [Check off Task in TASKS.md]
```

### Phase 1: RED (Write Failing Test First)
* Locate the test file or create a new one inside `tests/unit/` or `tests/integration/`.
* Implement a test case covering the specific Happy Path or Boundary condition defined in the task.
* Run the local test suite using `run_command` and verify that the test fails cleanly (RED). **You are strictly forbidden from writing production code before seeing a failing test.**

### Phase 2: GREEN (Write Minimal Code to Pass)
* Go to `src/` or the active codebase directory.
* Write the *absolute minimum* production code necessary to satisfy the failing test. Do not build speculative features.
* Run the test suite again. Verify that the test passes successfully (GREEN).

### Phase 3: REFACTOR (Clean and Standardize)
* Clean up any code structures: remove duplicate variables, modularize logic, and optimize loops.
* Run the test suite once more to ensure the refactoring did not break any assertions (stays GREEN).
* Standardize comments and docstrings according to the Google Python Style Guide.

---

## Testing Constraints

To maintain stable, high-speed, and decoupled test suites, you must enforce the following boundaries:

### 1. Decoupled Folders
* **Unit Tests (`tests/unit/`)**: Must be 100% mocked. Unit tests are strictly prohibited from making external HTTP calls, reading local files, or opening SQLite/PostgreSQL databases. Must run in under 10ms.
* **Integration Tests (`tests/integration/`)**: Must execute within isolated sandboxes, such as an in-memory SQLite instance or mock network handlers.

### 2. Hermetic Constraint
* **No Active Network Sockets**: You are strictly forbidden from writing tests that make live API requests to external internet servers. If a third-party integration is required, you must fully mock the interface locally.

### 3. No "Blind Completes"
* **Physical Proof**: You are strictly forbidden from checking off a task `[x]` or ending your turn stating a task is finished without capturing and displaying the successful test runner output log directly in your text response.
