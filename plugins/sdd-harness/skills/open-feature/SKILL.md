---
name: open-feature
description: Commit approved specification files, provision a sandboxed branch worktree, and instruct the user to open the workspace.
---

# Open Feature Playbook

You must act as the **sdd-implementor** (profile `agents/sdd-implementor.json`) to execute this playbook.

---

## Playbook Execution

### 1. Pre-Execution Checks
*   Identify the target Epic and Feature to build (e.g. `ep-billing/ft-stripe-checkout`).
*   Verify that `SPEC.md`, `DESIGN.md`, and `TASKS.md` exist under that feature directory.
*   **Audit Check**: Verify that `TASKS.md` has the `EM_AUDIT: APPROVED` header block. If missing, halt execution and instruct the user to run the EM design auditor first.

### 2. Commit Specifications
*   Run `git status` in the parent repository.
*   If there are uncommitted changes, explain to the user that we are going to commit all approved specifications first.
*   Run `git add .` and `git commit -m "commit specs for ep-<epic> ft-<feature>"` to ensure the parent workspace is clean.

### 3. Provision Sandbox
1.  Run the `/worktree create` slash command to provision the sandbox branch and register it as a new Project in Jetski Hub:
    ```
    /worktree create ep-<epic>-ft-<feature>
    ```
2.  Direct the user:
    *   *"The sandbox has been successfully provisioned and registered as a new Project in Jetski Hub!"*
    *   *"To start implementation:"*
    *   *"1. Open Jetski Hub."*
    *   *"2. Select the new Project **<project_name> (ep-<epic>-ft-<feature>)** from the sidebar."*
    *   *"3. Open a new chat session and run **/start-feature** to begin the implementation phase."*
3.  **Immediately halt execution** and stop calling tools.
