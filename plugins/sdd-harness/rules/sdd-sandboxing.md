---
trigger: always_on
description: Enforce strict role-based folder write scopes and tool execution boundaries.
---

# SDD Sandboxing Rules

You must strictly maintain the role-based boundaries defined below to ensure codebase hygiene and prevent un-reviewed modifications:

---

## 1. File Access & Write Scopes

*   **Specification & Design Phases (Parent Repo)**:
    *   **Allowed**: Writing and editing specifications under `docs/PROJECT.md` or `docs/sdd/ep-*/ft-*/*.md`.
    *   **Prohibited**: Modifying any source code files (under `src/`, `lib/`, `app/`, etc.) or project configs (like `package.json`, `requirements.txt`).
    *   **Enforcing Roles**: Only the Product Manager (`sdd-product-manager`), Engineering Manager (`sdd-engineering-manager`), and Technical Lead (`sdd-technical-lead`) profiles are authorized to operate in this phase.
*   **Implementation Phase (Sandbox Worktree)**:
    *   **Allowed**: Modifying source code files, tests, and configuration files *strictly inside the sandbox directory* (`worktrees/ep-*/ft-*/`).
    *   **Prohibited**: Modifying any specifications (under `docs/sdd/`), rules, or playbooks (under `.agents/`). Any specification issues must be raised via a `spec_change_proposal.md` artifact.
    *   **Enforcing Roles**: Only the Coder (`sdd-implementor`) profile is authorized to write files during this phase.

---

## 2. Tool Boundaries

*   **Command Execution (`run_command`)**:
    *   **PM and EM**: Strictly forbidden from calling `run_command`. They operate purely via file read/write and search tools.
    *   **Technical Lead**: Allowed to run `run_command` *only* to execute parent test runner suites during verification. Forbidden from running compilers, git commands, or code generators.
    *   **Coder**: Authorized to use `run_command` inside the sandbox to compile code, run tests, and manage the Git sandbox lifecycle (branching, worktree creation/merging).

---

## 3. Escalation Rules

*   If the Coder detects that a requirement in `SPEC.md` or a database key contract in `DESIGN.md` is physically un-implementable:
    1.  **Do not modify the spec file.**
    2.  Write a `spec_change_proposal.md` artifact detailing the conflict.
    3.  Report the issue in chat: *"Halted. Discovered specification conflict. Spec Change Proposal drafted. Please reload the Engineering Manager to adjust the design."*
    4.  Halt execution and wait for user guidance.
