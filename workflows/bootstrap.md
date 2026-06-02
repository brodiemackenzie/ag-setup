---
description: Initialize a new Spec-Driven Development project workspace cleanly sandboxed and bound to GitHub.
---

Instructions:
1. **Gather parameters**: Ask the user for the new project name, the GitHub Remote SSH URL, and their framework scaffolding choice ('python', 'nextjs', or 'none') one at a time in the chat conversation.
2. **Execute bootstrap**: Run the global bootstrap script using your terminal command tool to initialize the workspace:
   ```bash
   /usr/local/google/home/brodiem/projects/ag-setup/skills/project-bootstrap/scripts/bootstrap.sh <project_name> <github_url> --scaffold <scaffold>
   ```
   *(Replace `<project_name>`, `<github_url>`, and `<scaffold>` with the values provided by the user).*

Constraints:
Only use the instructions in this file when bootstrapping a new project.
Do not begin coding or creating specifications until the bootstrapper has completed successfully.
