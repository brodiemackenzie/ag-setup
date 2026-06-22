---
name: close-feature
description: Dismantle the sandboxed worktree folder, prune local Git branches, and clean up workspace configurations.
---

# Close Feature Playbook

You must act as the **sdd-implementor** (profile `agents/sdd-implementor.json`) to execute this playbook.

---

## Playbook Execution

### 1. Environment Verification
*   Verify that the current working directory is the **parent repository root** (path does NOT contain `worktrees/`).
*   If you are running inside a sandbox worktree (path contains `worktrees/`):
    *   Halt execution immediately.
    *   Instruct the user: *"I cannot execute the close-feature workflow from within the sandbox workspace. Please switch back to the parent project in Jetski Hub and run **/close-feature** from there to merge and clean up."*

### 2. Select Target Feature
*   Identify the Epic and Feature sandbox to close.

### 3. Verify Sandbox Cleanliness
*   Run `git status --porcelain` inside the sandbox directory `~/.gemini/jetski/worktrees/<project>/ep-<epic>-ft-<feature>/`.
*   If the command outputs any uncommitted or untracked changes:
    *   Alert the user in chat: *"There are uncommitted changes in the feature sandbox. Shall I commit them on your behalf before closing, or would you like to review them first?"*
    *   If the user approves automatic commit, run `git add -A && git commit -m "stage remaining changes before sandbox closure"` inside the sandbox directory.
    *   If the user prefers manual review, halt the workflow and await instructions.

### 4. Execute Teardown Command
*   Run the `/worktree finish` slash command to execute the unified sync, diff, merge, and closure pipeline:
    ```
    /worktree finish ep-<epic>-ft-<feature>
    ```
*   **Merge Conflict Check**: If the merge command fails with conflicts, immediately load `.agents/plugins/sdd-harness/skills/git-reconciliation/SKILL.md` and execute its conflict reconciliation rules to resolve markers and finish the merge.
*   Verify that the sandbox folder under `~/.gemini/jetski/worktrees/<project>/ep-<epic>-ft-<feature>/` has been deleted from disk.
*   Verify that the worktree project config file under `~/.gemini/config/projects/` has been deleted from disk.

### 5. Report Cleanup Status & Git Summary
*   Confirm branch pruning.
*   Collect the final repository status by executing:
    *   `git status` (to verify the clean parent branch)
    *   `git worktree list` (to verify the sandbox worktree was deleted)
    *   `git branch` (to verify the local feature branch was pruned)
    *   `git log -n 3 --oneline` (to show recent merge history)
*   Notify the user that the workspace is clean: *"Sandbox dismantled, branch merged and cleaned up. Suggest loading the Technical Lead to run feature verification using the feature-verifier skill."*
