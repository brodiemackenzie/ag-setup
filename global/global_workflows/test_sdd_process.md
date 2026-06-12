---
description: Launch and manage the Spec-Driven Development (SDD) simulation test suite step-by-step.
---

# Test Pipeline Management Workflow

You must act as the **sdd-project-manager** to execute this workflow. You will coordinate running the Python simulation scenarios step-by-step and report progress to the user.

## Simulation Stages Guide
This workflow executes the SDD process step-by-step. The process is completely **stateless**; each stage reads from the repository's physical files. 

Because of container jail isolation boundaries, you must run the stages in their respective workspaces:

### 1. In the Parent Repository Chat:
*   `/test_sdd_process --stage=bootstrap` ➔ Sets up the git sandbox environment.
*   `/test_sdd_process --stage=blueprint` ➔ Generates `docs/PROJECT.md` inside the container.
*   `/test_sdd_process --stage=specs` ➔ Drafts `SPEC.md`, `DESIGN.md`, and `TASKS.md` inside the container and commits them.
*   `/test_sdd_process --stage=worktree` ➔ PM provisions the Git worktree branch on the host and copies simulation files.

> [!IMPORTANT]
> Once the `worktree` stage completes, you **must switch your active workspace in the Jetski UI** to the newly created feature worktree workspace.

### 2. In the Feature Worktree Workspace Chat:
*   Have the Coder agent implement the code and verify the test suite.
*   `/test_sdd_process --stage=implement` ➔ Runs local E2E simulation assertions (verifies files exist and executes the pytest suite).

> [!IMPORTANT]
> Once the `implement` stage passes, you **must switch your active workspace in the Jetski UI back to the parent repository**.

### 3. In the Parent Repository Chat:
*   `/test_sdd_process --stage=close` ➔ PM agent merges the feature and dismantles the worktree.

---

## Execution Guide

1.  **Parse Stage Argument**:
    *   Read the user's prompt. Find the `--stage` flag (e.g. `--stage=bootstrap` or `--stage specs`).
    *   If no stage flag is provided, halt and reply: *"Please specify a stage to execute, e.g. `/test_sdd_process --stage=bootstrap`"*
2.  **Verify Active Workspace Context**:
    *   If executing stage `implement`, verify that the current working directory path contains `worktrees/`. If not, warn the user to switch to the Coder workspace first.
    *   If executing any other stage, verify that the current working directory is the parent repository (does NOT contain `worktrees/`). If not, warn the user to switch back to the parent workspace first.
3.  **Execute Command**:
    *   Map the stage to: `python3 tests/sim_sdd_process.py --stage <stage_name>`
    *   Run the command in the workspace directory.
4.  **Report Progress**:
    *   Stream the output logs and report pass/fail.
    *   If the stage completed was `worktree`, show a prominent alert warning:
        > [!IMPORTANT]
        > The Git worktree has been provisioned. Please **switch to the new feature worktree workspace in the UI sidebar** and open a new chat to run `/test_sdd_process --stage=implement`.
    *   If the stage completed was `implement`, show a prominent alert warning:
        > [!IMPORTANT]
        > Implementation verification complete. Please **switch back to the parent workspace in the UI sidebar** and run `/test_sdd_process --stage=close` to finalize.
