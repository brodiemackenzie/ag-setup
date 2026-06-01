---
name: worktree-manager
description: Automates the lifecycle of Git worktrees, linking environments dynamically based on open source stacks (Python, Node.js, Rust, Go), and aligning them with the Spec-Driven Development (SDD) Epic/Feature hierarchy.
---

# Worktree Manager Skill

This skill equips the Project Manager Agent with the capability to provision, sync, link, and tear down isolated workspaces (Git worktrees) that correspond directly to Epics and Features designed in the Spec-Driven Development (SDD) lifecycle.

## When to Use This Skill

* **Task Initialization**: Use when starting a new feature implementation (either from scratch or from an existing specification doc).
* **Dependency Linking**: Use to retroactively link runtime environments (node_modules, python venv, rust cargo target cache) to an active worktree.
* **Code Synchronization**: Use to pull main repository updates and cleanly rebase active feature branches.
* **Feature Finalization**: Use to merge a completed feature branch back into main, reconcile dependencies, and clean up directories.

## Capabilities & Commands

The skill relies on the helper script `scripts/manage_worktree.sh` to perform the following actions:

1. **`draft-spec <epic> <feature>`**
   * Creates a new, blank SDD specification file at `docs/sdd/<epic>/<feature>.md` in the main workspace. No branches or worktrees are created. Used for pure design phases.

2. **`prototype <epic> <feature> [--link]`**
   * Starts a new prototyping feature from scratch. provisions a Git branch `feature/<epic>/<feature>`, sets up a worktree directory, and creates a blank specification file. Optionally links dependencies if `--link` is passed.

3. **`provision-from-spec <spec_path> [--link]`**
   * Provisions a worktree based on an *already existing* specification file (e.g. `docs/sdd/malloy/trends.md`). Extracts the epic/feature names, spins up the branch, provisions the worktree, and copies the spec context over.

4. **`link-env <epic> <feature>`**
   * Retroactively auto-detects open-source stacks in the main repository and creates fast, robust symlinks/inherited environments for the worktree (e.g., symlinking `node_modules`, creating inherited Python virtual environments, sharing Cargo target caches).

5. **`sync-worktree <epic> <feature>`**
   * Fetches updates from the origin main branch and rebases the worktree branch to keep it synchronized.

6. **`close-feature <epic> <feature>`**
   * Runs lints/tests, merges the branch back to main, reconciles dependency changes back to the main environment, and safely deletes the worktree directory.

## Usage Guidelines for Agents

* **Hygiene**: When creating a new worktree, the skill will automatically append `worktrees/` to the main repository's `.gitignore` file to ensure local worktrees are never tracked.
* **Decoupling**: Prefer using `draft-spec` for design sessions with the sdd-architect, and `provision-from-spec` once the design is finalized. Use `prototype` only when explicitly requested.
