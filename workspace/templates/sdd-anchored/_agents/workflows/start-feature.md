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

## 4. Execute Sandbox Provisioning
Once the user approves or adjusts the parameters:
1.  Run the worktree manager shell script to provision the sandbox branch:
    ```bash
    ./.agents/skills/worktree-manager/scripts/manage_worktree.sh prototype ep-<epic> ft-<feature>
    ```
2.  Run the link-env subcommand with the approved environments list:
    ```bash
    ./.agents/skills/worktree-manager/scripts/manage_worktree.sh link-env ep-<epic> ft-<feature> [approved_envs...]
    ```
    *(e.g., `./manage_worktree.sh link-env ep-guest-submissions ft-submission-form python`)*
3.  Confirm that the script has successfully opened a new JetSki window for the sandbox folder.
4.  Direct the user:
    *   *"The sandbox has been successfully provisioned! Please switch to the newly opened JetSki window, open a new chat, and instruct the Coder: 'Please implement the feature outlined in the specifications'."*
5.  **Immediately halt execution** and stop calling tools.
