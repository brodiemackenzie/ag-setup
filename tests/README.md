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
*   **[sim_6_loop_escape.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_6_loop_escape.py)**:
    *   *Focus*: TDD Loop Escape (unhappy path).
    *   *Verifies*: The Coder agent halting after 3 consecutive failures and generating `failed_test_summary.md`.
*   **[sim_7_conflict_resolution.py](file:///usr/local/google/home/brodiem/projects/ag-setup/tests/sim_7_conflict_resolution.py)**:
    *   *Focus*: Git merge conflict resolution (unhappy path).
    *   *Verifies*: The PM agent detecting merge conflicts during `/close-feature`, analyzing diff histories, surgical cleaning inline markers, and committing.

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

## ⚠️ Local IDE-Mode Limitations (Bug b/521465559)
When executing python simulation scripts inside a local IDE workspace, calls to the `agentapi` CLI tool will fail with a gRPC crash:
`failed to start cascade: rpc error: code = Internal desc = stream terminated by RST_STREAM`

This is because the local IDE-bound server does not initialize the persistent project store in IDE mode, causing the server to panic when it receives workspace configuration data from the CLI client.

## ⚠️ Sandboxing / NsJail Mount Limitations (Timeout during E2E Pipeline)
When executing the automated integration test script (`sim_sdd_process.py`), the background Jetski server might crash with a mount namespace error:
`remote error: run bash: fork/exec /usr/bin/bash: no such file or directory`
or subsequent tool calls might fail with:
`directory does not exist`

This happens due to rapid workspace directory creation and Python `.venv` setup, which can trigger file-watcher leaks or mount collisions in NsJail. When this occurs, the simulated PM agent gets stuck in a self-debugging loop, causing the client-side `agentapi` call to timeout.

### Workaround: Disable Terminal Sandboxing
To bypass this sandbox mounting error during automated E2E runs, temporarily disable terminal sandboxing in the Jetski CLI config:
1. Create a CLI settings file:
   ```bash
   mkdir -p ~/.gemini/jetski/cli
   echo '{"enableTerminalSandbox": false}' > ~/.gemini/jetski/cli/settings.json
   ```
2. Restart the Jetski Hub Server.

### Manual E2E Playback Workaround
To verify the SDD pipeline locally, you must play back the E2E lifecycle manually inside your JetSki chat conversation window using the slash commands:

1.  **Bootstrap Workspace (`/bootstrap`)**:
    *   *Prompt*: `/bootstrap`
    *   *Dialog*: Choose name `generative-guestbook` and select `no` for git binding.
    *   *Outcome*: Initializes empty git repo and copies templates to `.agents/`.
2.  **Vision Blueprint (`/blueprint`)**:
    *   *Prompt*: `/blueprint`
    *   *Dialog*: Provide project objective (`guestbook app with witty AI replies and Imagen PNGs`), tech stack (`python, html, json`), and epic/feature breakdown (`ep-guest-submissions/ft-submission-form`).
    *   *Outcome*: Creates `docs/PROJECT.md`.
3.  **Spec Discovery (`/spec-feature`)**:
    *   *Prompt*: `/spec-feature`
    *   *Dialog*: Set scope to `ep-guest-submissions/ft-submission-form` and provide functional rules (name, comment, JSON storage, homepage display).
    *   *Approval (HITL Check)*: Approve the drafted specs with `yes, write the spec files`.
    *   *Outcome*: Writes `SPEC.md`, `DESIGN.md`, and `TASKS.md` to disk.
4.  **Provision Sandbox (`/start-feature`)**:
    *   *Prompt*: `/start-feature`
    *   *Dialog*: Specify `ep-guest-submissions/ft-submission-form`.
    *   *Outcome*: PM provisions Git worktree sandbox under `~/.gemini/jetski/worktrees/` and symlinks venv dependencies.
5.  **TDD Code Loop (Sandbox implementation)**:
    *   Open a new chat thread bound to the sandbox folder directory.
    *   *Prompt*: `Please read specs and implement TASKS.md`.
    *   *Outcome*: Coder implements code/tests, runs pytest, checks off tasks sequentially, and commits.
6.  **Teardown & Merge (`/close-feature`)**:
    *   Return to your main parent workspace chat thread.
    *   *Prompt*: `/close-feature`
    *   *Dialog*: Specify `ep-guest-submissions/ft-submission-form`.
    *   *Outcome*: PM merges the feature branch into the parent branch, resolves any conflicts, and deletes the worktree folder.

---

### Clean Teardown
Each script is designed to clean up its own temporary sandbox directory under `sandbox/` and its dynamic project configurations under `~/.gemini/config/projects/` upon completion. If a test fails, it halts immediately, leaving the files intact on disk for debugging.
