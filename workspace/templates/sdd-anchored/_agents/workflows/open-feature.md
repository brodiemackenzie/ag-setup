---
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
1.  Run the worktree manager shell script to provision the sandbox branch and register the workspace in the parent project:
    ```bash
    ./.agents/skills/worktree-manager/scripts/manage_worktree.sh prototype ep-<epic> ft-<feature>
    ```
2.  Direct the user:
    *   *"The sandbox has been successfully provisioned and registered as a workspace under your parent project in Jetski Hub!"*
    *   *"To start implementation:"*
    *   *"1. Open Jetski Hub and select the parent project **<project_name>**."*
    *   *"2. Switch to the **ep-<epic>-ft-<feature>** workspace in the sidebar."*
    *   *"3. Open a new chat session and run **/start-feature** to begin the implementation phase."*
3.  **Immediately halt execution** and stop calling tools.
