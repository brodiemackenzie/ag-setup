---
description: Initialize a new Spec-Driven Development project workspace cleanly sandboxed and optionally bound to GitHub.
---

Instructions:

1. **Pre-flight Check (Strict Halt)**: 
   * Verify if the active editor workspace is already bootstrapped. If the active workspace contains an `.agents/` folder or is already initialized with Spec-Driven Development rules, **immediately halt execution**.
   * Politely explain to the user that the current project is already bootstrapped and that `/bootstrap` is strictly a greenfield installer designed for initializing fresh repositories.

2. **Parameter Parsing & Interactive Interview**:
   * The user may run `/bootstrap` with optional arguments, e.g., `/bootstrap [project_name] [--git-remote <url>] [--process <process_slug>]`.
   * Parse any arguments provided by the user.
   * If any required parameters are missing, collect them **one at a time** in chat (do not dump multiple questions at once to avoid user fatigue):
     * **Step A**: If not provided, ask the user for the **Project Name** (e.g., *"Great! Let's initialize a new workspace. What would you like to name the project folder?"*).
     * **Step B**: If not provided, ask the user for the **Target GitHub SSH URL** (e.g., *"Got it. What is the target GitHub remote repository SSH URL to bind to this project? (Reply 'none' or press Enter to skip)"*).
     * **Step C**: If not provided, ask the user for the **Process Template Choice** (e.g., *"Which agent interaction process template should we configure? Please reply with 'sdd-anchored' (Recommended), 'sdd-first', 'sdd-source', or 'vibe'."*). Default to `sdd-anchored` if not specified.

3. **Execute the Installer**:
   * Once all parameters are collected, formulate the CLI command and run it:
     ```bash
     /usr/local/google/home/brodiem/projects/ag-setup/global/skills/project-bootstrap/scripts/bootstrap.sh <project_name> <github_url> --process <process_slug>
     ```
     *(Replace `<project_name>`, `<github_url>` (use 'none' if skipped), and `<process_slug>` with the corresponding values).*

4. **Present Success & Transition Workspace**:
   * Show the successful shell output logs to the user.
   * Confirm that the script has automatically opened a new JetSki window matching the project folder using the JetSki CLI launcher.
   * Direct the user to:
     1. Switch to the newly opened IDE window.
     2. Open a new chat session (which will automatically be named after the project workspace).
     3. Ask the new agent to start the discovery process (e.g., "Help me draft the project proposal") to begin the Spec-Driven Development functional journey.

Constraints:
* Only use the instructions in this file when bootstrapping a new project.
* Do not refer to other files that may have conflicting project initialization instructions.
* Do not begin coding or creating specifications until the bootstrapper has completed successfully.
