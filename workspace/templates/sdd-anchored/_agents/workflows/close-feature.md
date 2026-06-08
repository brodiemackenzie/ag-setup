---
description: Dismantle the sandboxed worktree folder, prune local Git branches, and clean up workspace configurations.
---

# Close Feature Workflow

You must act as the **sdd-project-manager** (profile `agents/sdd-project-manager.json`) to execute this workflow.

## 1. Select Target Feature
*   Ask the user which Epic and Feature sandbox they want to close (e.g. `ep-guest-submissions/ft-submission-form`).

## 2. Execute Teardown Command
*   Run the worktree manager shell script to dismantle the sandbox:
    ```bash
    ./.agents/skills/worktree-manager/scripts/manage_worktree.sh close-feature ep-<epic> ft-<feature>
    ```
*   **Merge Conflict Check**: If the merge command fails with conflicts, immediately load `.agents/skills/git-reconciliation/SKILL.md` and execute its conflict reconciliation rules to resolve markers and finish the merge.
*   Verify that the sandbox folder under `~/.gemini/jetski/worktrees/<project>/ep-<epic>-ft-<feature>/` has been deleted from disk.

## 3. Report Cleanup Status
*   Confirm branch pruning.
*   Notify the user that the workspace is clean: *"Sandbox dismantled, branch cleaned up, and workspace returned to a clean parent state."*
