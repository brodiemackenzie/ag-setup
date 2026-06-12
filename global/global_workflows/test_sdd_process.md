---
description: Launch and manage the Spec-Driven Development (SDD) simulation test suite in both isolated and chained modes.
---

# Test Pipeline Management Workflow

You must act as the **sdd-project-manager** to execute this workflow. You will coordinate running the Python simulation scenarios and stream output logs back to the user.

## Simulation Actions Guide
Before running, explain the difference between the testing actions to the user if they ask or if it's the first execution:

*   **Chained Mode (End-to-End)**:
    *   Runs the entire SDD lifecycle sequentially in a single flow (Blueprint ➔ Spec ➔ Code ➔ Teardown).
    *   *Usage*: Select `chained`.
    *   *Command Line Example*: `./test_sdd_process.sh` or `./test_sdd_process.sh --fixture generative_guestbook.json`
*   **Isolated Mode (Phase-Specific)**:
    *   Runs a targeted simulation of a *single* phase in isolation. It uses static mock files to simulate previous steps, allowing you to test specific agent behaviors quickly without running the full E2E flow.
    *   *Usage*: Select `isolated` and pick a phase.
    *   *Command Line Example*: `./test_sdd_process.sh --phase blueprint`
*   **Clean Mode (Tear Down)**:
    *   Deregisters a test project from Jetski Hub and deletes the target folder from disk.
    *   *Usage*: Select `clean` and specify the project name/path.
    *   *Command Line Example*: `./test_sdd_process.sh --clean sandbox/my-test-project`

---

## 1. Select Action
Ask the user:
*"Which action would you like to perform? [isolated / chained / clean]"*

---

## 2. Execute Isolated Scenarios
If the user selects **`isolated`**:
1.  Ask the user:
    *"Which isolated scenario would you like to execute? [bootstrap / blueprint / reconciliation / security / implementation]"*
2.  Map the user's choice to the unified runner command:
    *   `bootstrap` ➔ `./test_sdd_process.sh --phase bootstrap`
    *   `blueprint` ➔ `./test_sdd_process.sh --phase blueprint`
    *   `reconciliation` ➔ `./test_sdd_process.sh --phase reconciliation`
    *   `security` ➔ `./test_sdd_process.sh --phase security`
    *   `implementation` ➔ `./test_sdd_process.sh --phase implementation`
3.  Propose running the command:
    *   Execute the mapped command using your shell tool with Cwd set to the project root directory.
4.  Stream the stdout and stderr back to the user in chat.
5.  Report final pass/fail results.

---

## 3. Execute Chained E2E Pipeline Scenarios
If the user selects **`chained`**:
1.  Ask the user:
    *"Which JSON fixture file from tests/fixtures/ should we use? (Press Enter for default: generative_guestbook.json)"*
2.  If the user provides a custom name (e.g. `todo_app.json`), format the command:
    `./test_sdd_process.sh --fixture <fixture_name>`
    Otherwise, default to:
    `./test_sdd_process.sh`
3.  Propose running the command:
    *   Execute the mapped script command in the background.
4.  Stream stdout log chunks to the chat to show live step progress (Phase 2 through Phase 6).
5.  Report final pass/fail results upon script completion.

---

## 4. Clean Up Test Project
If the user selects **`clean`**:
1.  Ask the user:
    *"Which project name or directory path should we clean up?"*
2.  Propose running the command:
    `./test_sdd_process.sh --clean <project_name_or_path>`
3.  Stream the stdout and stderr back to the user in chat.
4.  Confirm when the project is successfully deregistered and deleted.
