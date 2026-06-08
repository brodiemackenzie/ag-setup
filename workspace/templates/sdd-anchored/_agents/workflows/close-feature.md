---
description: Dismantle the sandboxed worktree folder, prune local Git branches, and clean up workspace configurations.
---

# Close Feature Workflow

You must act as the **sdd-project-manager** (profile `agents/sdd-project-manager.json`) to execute this workflow.

## 1. Select Target Feature
*   Ask the user which Epic and Feature sandbox they want to close (e.g. `ep-guest-submissions/ft-submission-form`).

## 2. Verify Sandbox Cleanliness
*   Run `git status --porcelain` inside the sandbox directory `~/.gemini/jetski/worktrees/<project>/ep-<epic>-ft-<feature>/`.
*   If the command outputs any uncommitted or untracked changes:
    *   Alert the user in chat: *"There are uncommitted changes in the feature sandbox. Shall I commit them on your behalf before closing, or would you like to review them first?"*
    *   If the user approves automatic commit, run `git add -A && git commit -m "stage remaining changes before sandbox closure"` inside the sandbox directory. *(Note: This commit is fully authorized under the global commit ban exception, as it is explicitly dictated by this structured workflow).*
    *   If the user prefers manual review, halt the workflow and await instructions.

## 3. Execute Teardown Command
*   Run the worktree manager shell script to dismantle the sandbox:
    ```bash
    ./.agents/skills/worktree-manager/scripts/manage_worktree.sh close-feature ep-<epic> ft-<feature>
    ```
*   **Merge Conflict Check**: If the merge command fails with conflicts, immediately load `.agents/skills/git-reconciliation/SKILL.md` and execute its conflict reconciliation rules to resolve markers and finish the merge.
*   Verify that the sandbox folder under `~/.gemini/jetski/worktrees/<project>/ep-<epic>-ft-<feature>/` has been deleted from disk.

## 4. Report Cleanup Status
*   Confirm branch pruning.
*   Notify the user that the workspace is clean: *"Sandbox dismantled, branch cleaned up, and workspace returned to a clean parent state."*
