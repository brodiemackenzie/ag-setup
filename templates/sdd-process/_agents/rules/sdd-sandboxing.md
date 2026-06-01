---
trigger: always_on
description: Enforce strict Git worktree sandboxing and active workspace relative locks.
---

# SDD Workspace Sandboxing Rules

You must strictly operate within your allocated workspace directories to prevent security and Git history pollution:

## 1. Active Worktree Sandboxing
* **Architect and Implementor Restrictions**: The Architect (`sdd-architect`) and Implementor (`sdd-implementor`) agents are strictly prohibited from executing commands inside or writing files directly to the top-level repository directory. 
* **Worktree Confines**: They must operate exclusively within their assigned Git worktree subdirectory (`worktrees/<epic-slug>/<feature-slug>/`).
* **Relative path Locks**: Write paths inside agent configurations are resolved relative to their CWD workspace root (e.g., `./src/*`, `./docs/*`). 
* **Top-Level Protection**: Any file creation, modification, or execution targeting files outside the active worktree directory (e.g., attempting to write via relative path traversal like `../../src/*` or to the top-level folder directories) is strictly forbidden and will be blocked immediately as a permission violation.

## 2. Project Manager Exceptions
* **The PM Boundary**: The Project Manager (`sdd-project-manager`) is the only agent permitted to operate in the top-level repository workspace.
* **Scope**: The PM's operations are strictly limited to repository layout coordination, running branch automation (creating/cleaning worktrees via `manage_worktree.sh`), and formatting document styles via linters.
