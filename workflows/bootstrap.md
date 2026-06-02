---
description: Initialize a new Spec-Driven Development project workspace cleanly sandboxed and bound to GitHub.
---

Instructions:
1. **Gather parameters**: Conversationally ask the user for any missing parameters (`project_name`, `github_url`, and `scaffold` (boilerplate choice: 'python', 'nextjs', or 'none')) one at a time in chat.
2. **Execute bootstrap**: Run the local bootstrap script on behalf of the user inside a shell terminal:
   ```bash
   /usr/local/google/home/brodiem/projects/ag-setup/skills/project-bootstrap/scripts/bootstrap.sh "{{project_name}}" "{{github_url}}" --scaffold "{{scaffold}}"
   ```
