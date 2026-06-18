---
name: start-feature
description: Initialize the implementation phase inside the sandboxed workspace, load TDD playbooks, and identify the first task.
---

# Start Feature Workflow (Implementation)

You must act strictly as the **sdd-implementor** (profile `agents/sdd-implementor.json`) in this sandboxed workspace.

## 1. Environment Verification
*   Verify that the current working directory is inside a Git worktree sandbox (path contains `worktrees/`).
*   If you are running in the parent repository root (path does not contain `worktrees/`):
    *   Halt execution immediately.
    *   Instruct the user: *"I cannot execute the start-feature workflow from the parent workspace. Please run **/open-feature** first to provision the sandbox, select that Project in the Jetski Hub sidebar, and run **/start-feature** in that project session."*
*   Verify that `docs/sdd/ep-<epic>/ft-<feature>/SPEC.md`, `DESIGN.md`, and `TASKS.md` exist in the workspace.

## 2. Playbook Initialization
*   Proactively load the TDD playbook:
    *   Read `.agents/plugins/sdd-harness/skills/tdd-flow/SKILL.md` to align with TDD controls and retry limits.

## 3. Task Identification
1.  Open `docs/sdd/ep-<epic>/ft-<feature>/TASKS.md`.
2.  Scan the checklist to locate the **first unchecked task** (e.g., `- [ ] tsk-0-scaffold` or `- [ ] tsk-1-model`).
3.  Announce the target task to the user in chat:
    *   *"Starting implementation of task: **tsk-<name>** ([Ref: Subsystem])"*
    *   *Show the Given/When/Then scenarios for this task.*
4.  Begin the TDD loop for this task:
    *   Navigate to tests and write the failing test (RED phase).
