---
trigger: always_on
description: Enforce strict Git worktree sandboxing and active workspace relative locks.
---

# SDD Workspace Sandboxing Rules

You must strictly operate within your allocated workspace directories to prevent security and Git history pollution:

## 1. Active Worktree Sandboxing
* **Architect and Implementor Restrictions**: The Architect (`sdd-architect`) and Implementor (`sdd-implementor`) agents are strictly prohibited from executing commands inside or writing files directly to the top-level repository directory, with a single strict exception:
  * **Phase 0 Exception**: The Architect is permitted to create and edit the `docs/PROJECT.md` file in the documentation folder context exclusively when compiling the High-Level Project Blueprint.
* **Worktree Confines**: Aside from the Phase 0 exception, they must operate exclusively within their assigned Git worktree directory under `~/.gemini/jetski/worktrees/<project-name>/ep-<epic-name>-ft-<feature-name>/`.
* **Relative path Locks**: Write paths inside agent configurations are resolved relative to their CWD workspace root (e.g., `./src/*`, `./docs/*`). 
* **Top-Level Protection**: Any file creation, modification, or execution targeting files outside the active worktree directory (excluding the `docs/PROJECT.md` exception) is strictly forbidden and will be blocked immediately as a permission violation.

## 2. Project Manager Exceptions
* **The PM Boundary**: The Project Manager (`sdd-project-manager`) is the only agent permitted to operate in the top-level repository workspace for repository management and branch automation.
* **Scope**: The PM's operations are strictly limited to repository layout coordination, running branch automation (creating/cleaning worktrees via `manage_worktree.sh`), and formatting document styles via linters.
