---
name: worktree
description: Create, sync, diff, merge, close, or list isolated Git worktrees and register them in Jetski Hub
---
You are acting as the worktree-manage handler.
Your task is to manage the lifecycle of Git worktrees and their registration.

1. **Parse the action and branch name** from the user's request: "{{.Message}}".
   - Actions map as follows:
     - `create` / `new` / `init` ➔ `create`
     - `sync` / `update` / `pull` ➔ `sync`
     - `diff` / `changes` / `status` ➔ `diff`
     - `merge` / `integrate` ➔ `merge`
     - `close` / `cleanup` / `delete` ➔ `close`
     - `finish` / `complete` ➔ `finish`
     - `list` / `show` ➔ `list`
     - `help` / `?` ➔ `help`
   - Identify the branch name (e.g. "my-feature", "feature/login") for all actions except `list` and `help`.
   - Identify if the user passed `--force` or `-f` flags.
   - Identify any optional custom worktree path if provided.
   - If action or branch name is missing (and not doing `list` or `help`), ask the user for clarification.
2. **Execute the worktree script**:
   - Run the script located at `~/.gemini/config/plugins/project-orchestration/scripts/manage_worktree.sh`.
   - Arguments mapping: `bash ~/.gemini/config/plugins/project-orchestration/scripts/manage_worktree.sh <action> [<branch_name>] [<custom_path>] [--force]`
   - Pass `--force` to the script if the user requested it.
3. **Report results**:
   - Report the output of the script to the user.
   - If the action is `diff` or `finish` (during the preview step), output the diff results in a clean markdown code block.
   - If the action is `list`, format the list of active worktrees as a clean bulleted list or table.
   - If the script fails (e.g., merge conflicts during sync or merge), explain which step failed, instruct the user how to open the worktree workspace to resolve conflicts, and stop.
