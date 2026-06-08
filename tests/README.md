# SDD E2E Simulation & Testing Framework

This directory contains the automated evaluation suite for the Spec-Driven Development (SDD) process. It provides end-to-end simulations of agent interactions, validating changes to rules, playbooks, and utility scripts without requiring manual execution.

---

## 📂 Test Scenarios

### 1. Isolated Mode Tests (Fast & Targeted)
These scripts test a single phase of the SDD process in isolation. They seed approved upstream mock inputs directly onto the disk and only invoke the relevant agent profile. This is ideal for validating changes to rules/prompts in a specific phase.

*   **[sim_1_bootstrap.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_1_bootstrap.py)**:
    *   *Focus*: Greenfield Project Bootstrapping.
    *   *Verifies*: Interactive conversational questions, copy of rules/playbooks, and git initialization.
*   **[sim_2_blueprint.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_2_blueprint.py)**:
    *   *Focus*: Vision Interview & Blueprint Generation.
    *   *Verifies*: The Architect Vision interview prompts, the creation of `docs/PROJECT.md`, and the scaffolding of folder capsule directory structures.
*   **[sim_3_reconciliation.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_3_reconciliation.py)**:
    *   *Focus*: Spec change proposal merging.
    *   *Verifies*: The Architect merging a `spec_change_proposal.md` into `SPEC.md` and committing it.
*   **[sim_4_permission_isolation.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_4_permission_isolation.py)**:
    *   *Focus*: Sandbox Security verification.
    *   *Verifies*: That path-based write permission block rules prevent the agent from writing files outside its sandbox folder.
*   **[sim_5_implementation.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_5_implementation.py)**:
    *   *Focus*: Implementor TDD coding loop.
    *   *Verifies*: The Coder agent reading specs, writing a Flask app, creating a pytest suite, and successfully passing all tests.

---

### 2. Chained Integration Mode (The E2E Pipeline)
This script simulates the entire developer lifecycle sequentially in one master integration run. Each phase operates on the *actual filesystem outputs* produced by the previous phase, matching the real-world user journey.

*   **[sim_e2e_full.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_e2e_full.py)**:
    *   *Flow*:
        1.  **Bootstrap**: Initializes empty workspace.
        2.  **Blueprint**: Runs the Vision interview to write `docs/PROJECT.md`.
        3.  **Discovery**: Conducts the functional spec discovery interview, generating `SPEC.md`, `DESIGN.md`, and `TASKS.md` for a Flask Guestbook app.
        4.  **Start-feature**: Commits specs and provisions the Git worktree branch sandbox and python environment.
        5.  **Implementation**: Spawns the Implementor agent inside the sandbox, which implements the routes and UI code.
        6.  **Verification**: Executes the generated test suite inside the sandbox, verifying it passes.
        7.  **Teardown**: Runs close-feature to dismantle the worktree.

---

## 🚀 How to Execute Tests

Ensure you are inside the `ag-setup` parent workspace repository, and run any test script directly:

```bash
# Run isolated implementor test
./tests/sim_5_implementation.py

# Run full chained E2E pipeline integration test
./tests/sim_e2e_full.py
```

### Clean Teardown
Each script is designed to clean up its own temporary sandbox directory under `sandbox/` and its dynamic project configurations under `~/.gemini/config/projects/` upon completion. If a test fails, it halts immediately, leaving the files intact on disk for debugging.
