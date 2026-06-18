---
name: open-feature
description: Commit specification files, provision a sandboxed branch worktree, and instruct the user to open the workspace.
---

# Open Feature Workflow

You must act as the **sdd-project-manager** (profile `agents/sdd-project-manager.json`) to execute this workflow.

## 1. Select Target Feature
*   Ask the user which Epic and Feature they want to build (e.g. `ep-guest-submissions/ft-submission-form`).
*   Verify that `SPEC.md`, `DESIGN.md`, and `TASKS.md` exist under that directory.

## 2. Commit Specifications
*   Run `git status` in the parent repository.
*   If there are uncommitted changes, explain to the user that we are going to commit all approved specifications first.
*   Run `git add .` and `git commit -m "commit specs for ep-<epic> ft-<feature>"` to ensure the parent workspace is clean.

## 3. Execute Sandbox Provisioning
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
