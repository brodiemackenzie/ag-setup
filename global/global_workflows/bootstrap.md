---
description: Initialize a new Spec-Driven Development project workspace cleanly sandboxed and bound to GitHub.
---

Instructions:

1. **Pre-flight Check (Strict Halt)**: 
   * Verify if the active editor workspace is already bootstrapped. If the active workspace contains an `.agents/` folder or is already initialized with Spec-Driven Development rules, **immediately halt execution**.
   * Politely explain to the user that the current project is already bootstrapped and that `/bootstrap` is strictly a greenfield installer designed for initializing fresh repositories.

2. **Interactive Conversational Interview**:
   * If the workspace is greenfield, take the lead and collect the required parameters **one at a time** in chat (do not dump multiple questions at once to avoid user fatigue):
     * **Step A**: Ask the user for the **Project Name** (e.g., *"Great! Let's initialize a new workspace. What would you like to name the project folder?"*).
     * **Step B**: Ask the user for the **Target GitHub SSH URL** (e.g., *"Got it. What is the target GitHub remote repository SSH URL to bind to this project?"*).
     * **Step C**: Ask the user for the **Scaffolding Choice** (e.g., *"Should we scaffold a basic Python structure, a Next.js app, or start with a blank slate? Please reply with 'python', 'nextjs', or 'none'."*).

3. **Execute the Installer**:
   * Once all parameters are collected, formulate the CLI command exactly as specified below and run it on behalf of the user using your terminal command tool:
     ```bash
     /usr/local/google/home/brodiem/projects/ag-setup/global/skills/project-bootstrap/scripts/bootstrap.sh <project_name> <github_url> --scaffold <scaffold>
     ```
     *(Replace `<project_name>`, `<github_url>`, and `<scaffold>` with the exact answers provided by the user).*

4. **Present Success & Transition Workspace**:
   * Show the successful shell output logs to the user.
   * Confirm that the script has automatically opened a new Jetski window matching the project folder using the `code -n` CLI utility.
   * Direct the user to:
     1. Switch to the newly opened IDE window.
     2. Open a new chat session (which will automatically be named after the project workspace).
     3. Ask their new agent to start the discovery process (e.g., "Help me draft the project proposal") to begin the Spec-Driven Development functional journey.

Constraints:
* Only use the instructions in this file when bootstrapping a new project.
* Do not refer to other files that may have conflicting project initialization instructions.
* Do not begin coding or creating specifications until the bootstrapper has completed successfully.
