---
description: Launch and manage the Spec-Driven Development (SDD) simulation test suite in both isolated and chained modes.
---

# Test Pipeline Management Workflow

You must act as the **sdd-project-manager** to execute this workflow. You will coordinate running the Python simulation scenarios and stream output logs back to the user.

## 1. Select Testing Mode
Ask the user:
*"Which simulation mode would you like to run? [isolated / chained]"*

---

## 2. Execute Isolated Scenarios
If the user selects **`isolated`**:
1.  Ask the user:
    *"Which isolated scenario would you like to execute? [bootstrap / blueprint / reconciliation / security / implementation / all]"*
2.  Map the user's choice to the target test script:
    *   `bootstrap` ➔ `python3 tests/sim_1_bootstrap.py`
    *   `blueprint` ➔ `python3 tests/sim_2_blueprint.py`
    *   `reconciliation` ➔ `python3 tests/sim_3_reconciliation.py`
    *   `security` ➔ `python3 tests/sim_4_permission_isolation.py`
    *   `implementation` ➔ `python3 tests/sim_5_implementation.py`
    *   `all` ➔ Run all of them sequentially.
3.  Propose running the command:
    *   Execute the mapped python command using your shell tool with Cwd set to the project root directory.
4.  Stream the stdout and stderr back to the user in chat.
5.  Report final pass/fail results.

---

## 3. Execute Chained E2E Pipeline Scenarios
If the user selects **`chained`**:
1.  Ask the user:
    *"Which JSON fixture file from tests/fixtures/ should we use? (Press Enter for default: generative_guestbook.json)"*
2.  If the user provides a custom name (e.g. `todo_app.json`), format the command:
    `python3 tests/sim_e2e_full.py --fixture <fixture_name>`
    Otherwise, default to:
    `python3 tests/sim_e2e_full.py`
3.  Propose running the command:
    *   Execute the `sim_e2e_full.py` python script in the background.
4.  Stream stdout log chunks to the chat to show live step progress (Phase 1 through Phase 6).
5.  Report final pass/fail results upon script completion.
