# Worktree Manager Skill

This skill outlines the local Git worktree lifecycle management and environment configurations that isolate active feature development capsules.

---

## Overview

In standard Spec-Driven Development, every feature is developed in complete isolation. This isolation is achieved physically by checking out feature branches into separate workspace directories using Git worktrees, ensuring no parallel feature branches pollute the main working tree.

---

## Playbook

### 1. Provisioning a Feature Workspace (`prototype`)
To begin developing a new feature, the Project Manager agent or user runs the `prototype` command to create a sandboxed feature capsule:
```bash
.agents/plugins/sdd-harness/skills/worktree-manager/scripts/manage_worktree.sh prototype <epic_slug> <feature_slug>
```
**Actions Performed**:
* Creates a new Git branch: `feature/<epic_slug>/<feature_slug>`.
* Provisions a Git worktree at `worktrees/<epic_slug>/<feature_slug>/`.
* Automatically scaffolds empty template documents inside the worktree:
  * `docs/sdd/<epic_slug>/<feature_slug>/SPEC.md`
  * `docs/sdd/<epic_slug>/<feature_slug>/DESIGN.md`
  * `docs/sdd/<epic_slug>/<feature_slug>/TASKS.md`



### 3. Merging & Deleting a Feature Capsule (`close-feature`)
Once verification tests are passing, safely close and dismantle the worktree:
```bash
.agents/plugins/sdd-harness/skills/worktree-manager/scripts/manage_worktree.sh close-feature <epic_slug> <feature_slug>
```
**Actions Performed**:
* Standardizes git status checks inside the worktree.
* Prompts the user to commit all active changes.
* Performs a Git merge from the worktree branch back into the active base branch.
* Gracefully prunes and deletes the Git worktree folder from the file system:
  ```bash
  git worktree remove "worktrees/<epic_slug>/<feature_slug>"
  ```
