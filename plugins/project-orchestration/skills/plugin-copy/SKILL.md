---
name: plugin-copy
description: Copy a plugin from a source directory into the local .agents/plugins/ directory of the target project, supporting safe updates.
---

# Plugin Copy Skill Playbook

You are acting as the **plugin-copy** handler.
Your task is to copy a plugin from a source directory to the local plugins directory of a target project.

---

## Playbook Execution

### 1. Argument Parsing
*   Identify the target parameters from the instruction prompt:
    *   `--source` / `-s`: The location of the source plugin folder (e.g. `~/projects/ag-setup/plugins/sdd-harness`).
    *   `--target` / `-t`: The location of the target project (e.g. `~/projects/generative-guestbook-test`). Defaults to the current working directory.
    *   `--force` / `-f`: Check if the user specified the force overwrite flag.

### 2. Execute Script
*   Execute the Bash script using `run_command` in your active session:
    ```bash
    bash ~/.gemini/config/plugins/project-orchestration/scripts/copy_plugin.sh --source <source_path> --target <target_path> [--force]
    ```
*   Use absolute paths for the parameters (expand `~` variables before passing).

### 3. Report Results
*   If the script completes successfully:
    *   Display the staged files.
    *   Suggest next steps: *"Plugin staging complete. You can now load this plugin's agent profiles and rules inside the target project workspace."*
*   If the script blocks (returns exit code 2 because target exists):
    *   Display the warning: *"Staging blocked. The plugin folder already exists in the target repo. Re-run this command and add the --force flag to overwrite it."*
