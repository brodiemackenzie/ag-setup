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
   * Confirm that the script has automatically opened a new JetSki window matching the project folder using the JetSki CLI launcher.
   * Advise the user that a new conversation session has been automatically pre-populated in their **Agent Manager** window and is immediately ready to resume.
   * Direct the user to:
     1. Switch to the newly opened IDE window, OR open their **Agent Manager** window.
     2. Locate and resume the pre-populated conversation session.
     3. Ask the new agent to trigger the discovery process (e.g., "Let's begin the SDD proposal interview!") to start the functional journey.

Constraints:
* Only use the instructions in this file when bootstrapping a new project.
* Do not refer to other files that may have conflicting project initialization instructions.
* Do not begin coding or creating specifications until the bootstrapper has completed successfully.
