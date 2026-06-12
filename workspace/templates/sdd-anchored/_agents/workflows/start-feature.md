---
description: Commit specification files, provision a sandboxed branch worktree, link runtime environments, and launch the coder IDE.
---

# Start Feature Workflow

You must act as the **sdd-project-manager** (profile `agents/sdd-project-manager.json`) to execute this workflow.

## 1. Select Target Feature
*   Ask the user which Epic and Feature they want to build (e.g. `ep-guest-submissions/ft-submission-form`).
*   Verify that `SPEC.md`, `DESIGN.md`, and `TASKS.md` exist under that directory.

## 2. Commit Specifications
*   Run `git status` in the parent repository.
*   If there are uncommitted changes, explain to the user that we are going to commit all approved specifications first.
*   Run `git add .` and `git commit -m "commit specs for ep-<epic> ft-<feature>"` to ensure the parent workspace is clean.

## 3. Dependency Scanning & Linking Approval
*   Open and read `docs/sdd/ep-<epic>/ft-<feature>/DESIGN.md`.
*   Scan the tech stack and database sections for dependencies (e.g. `python`, `node`, `rust`).
*   Prompt the user in chat for linking approval:
    *   *Example*: *"I detected python dependencies in the technical design. I will link the python virtualenv. Do you approve? [Yes/No]"*

## 4. Execute Sandbox Provisioning & Start Implementation
Once the user approves or adjusts the parameters:
1.  Run the worktree manager shell script to provision the sandbox branch and register the workspace in the parent project:
    ```bash
    ./.agents/skills/worktree-manager/scripts/manage_worktree.sh prototype ep-<epic> ft-<feature>
    ```
2.  Run the link-env subcommand with the approved environments list:
    ```bash
    ./.agents/skills/worktree-manager/scripts/manage_worktree.sh link-env ep-<epic> ft-<feature> [approved_envs...]
    ```
    *(e.g., `./manage_worktree.sh link-env ep-guest-submissions ft-submission-form python`)*
3.  Start the implementation conversation in the new worktree sandbox. Run the `agentapi` command with the working directory (`Cwd`) set to the absolute path of the worktree (`~/.gemini/jetski/worktrees/<project_name>/ep-<epic>-ft-<feature>`):
    ```bash
    agentapi new-conversation "Phase 4 - Sandboxed Implementation: Please read the specifications at docs/sdd/ep-<epic>/ft-<feature>/ and implement the tasks checklist in TASKS.md using TDD loops."
    ```
4.  Capture the `conversationId` from the command output.
5.  Direct the user:
    *   *"The sandbox has been successfully provisioned and registered as a workspace under your parent project in Jetski Hub!"*
    *   *"Started implementation conversation: **<conversationId>**."*
    *   *"You can now open Jetski Hub, select the parent project **<project_name>**, switch to the **ep-<epic>-ft-<feature>** workspace in the sidebar, and monitor the implementation progress live."*
6.  **Immediately halt execution** and stop calling tools.
