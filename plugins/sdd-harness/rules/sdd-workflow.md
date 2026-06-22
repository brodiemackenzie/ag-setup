---
trigger: always_on
description: Enforce the 8-step Spec-Driven Development (SDD) software factory pipeline.
---

# SDD Workflow Rules

You must strictly adhere to the 8-step software factory workflow when planning, designing, or implementing features:

---

## 1. The 8-Step Pipeline

1.  **Step 1: Feature Specification (`skills/spec-writer`)**
    *   **Role**: Product Manager (`sdd-product-manager`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/SPEC.md`
2.  **Step 2: Codebase Grounding (`skills/code-analyzer`)**
    *   **Role**: Engineering Manager (`sdd-engineering-manager`)
    *   **Asset**: `docs/sdd/CODE_ANALYSIS.md`
3.  **Step 3: Technical Design (`skills/design-architect`)**
    *   **Role**: Engineering Manager (`sdd-engineering-manager`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/DESIGN.md`
4.  **Step 4: Execution Planning (`skills/task-generator`)**
    *   **Role**: Technical Lead (`sdd-technical-lead`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/TASKS.md`
5.  **Step 5: Specification Audit (`skills/design-auditor`)**
    *   **Role**: Engineering Manager (`sdd-engineering-manager`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/TASKS.md` (Audit approval header)
6.  **Step 6: Sandboxed Execution (`skills/tdd-flow` & `skills/start-feature`)**
    *   **Role**: Implementor (`sdd-implementor`)
    *   **Asset**: Local code, tests, and Git worktree sandbox
7.  **Step 7: Code Verification (`skills/feature-verifier`)**
    *   **Role**: Technical Lead (`sdd-technical-lead`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/VERIFICATION_REPORT.md`
8.  **Step 8: Retrospective (`skills/retrospective-compiler`)**
    *   **Role**: Product Manager & Engineering Manager
    *   **Asset**: `docs/LESSONS_LEARNED.md`

---

## 2. Dynamic State Discovery & Startup

*   **Startup Verification Rule**: Upon starting a new conversation (on the very first turn), you **MUST** immediately run the programmatic status script using `run_command`:
    ```bash
    bash .agents/plugins/sdd-harness/scripts/status_report.sh
    ```
*   Display the output table at the top of your response.
*   **Next Steps Recommendation**: Below the Status Report table, recommend the next action based on the discovered file states:
    1.  If `docs/PROJECT.md` is missing ➔ Recommend `/blueprint` (using `project-interviewer`).
    2.  If `SPEC.md` is missing/draft ➔ Recommend `/spec-feature` (using `spec-writer`).
    3.  If `CODE_ANALYSIS.md` is missing ➔ Recommend `/code-analysis` (using `code-analyzer`).
    4.  If `DESIGN.md` is missing/draft ➔ Recommend `/design-feature` (using `design-architect`).
    5.  If `TASKS.md` is missing/draft ➔ Recommend `/taskify` (using `task-generator`).
    6.  If `TASKS.md` has no EM approval signature ➔ Recommend `/audit-tasks` (using `design-auditor`).
    7.  If audit is complete and you are in the parent repo ➔ Instruct the user to run `/open-feature` to provision the sandbox.
    8.  If you are in a sandbox worktree and tasks remain unchecked ➔ Recommend `/start-feature` (using `start-feature` & `tdd-flow`).
    9.  If all tasks are checked, but you are inside the worktree ➔ Instruct the user to return to the parent repo and run `/close-feature` to merge.
    10. If sandbox is closed, but `VERIFICATION_REPORT.md` is missing ➔ Recommend `/verify-feature` (using `feature-verifier`).
    11. If verified, but lessons are not updated ➔ Recommend `/retrospective` (using `retrospective-compiler`).

---

## 3. Plan-First Gate

*   **Plan-First Hook**: Before modifying any files or executing write operations, you MUST compile a clear Plan Asset (e.g., Implementation Plan or Task checklist artifact) and explicitly state to the user in chat what changes are going to happen. You **MUST set `RequestFeedback: true`** in the plan's metadata, **stop calling tools immediately**, and **wait for the user's explicit approval or 'Proceed' button confirmation** before executing any changes. File modifications without stating what is going to happen and waiting for approval are strictly forbidden, for all chats, without exception, **UNLESS** you are operating in one of these contexts:
    1.  **Test/Simulation Projects**: The active project name contains `test` or `sim` (all simulation phases run eagerly to prevent E2E hangs).
    2.  **Active TDD Task Execution**: You are inside a feature worktree (path contains `worktrees/`) and are **actively executing the structured TDD loop** (writing/running unit or integration tests to satisfy a specific `tsk-<id>` task from the checklist in `TASKS.md`). Any ad-hoc requests, free-form chats, or design alterations that bypass the structured TDD checklist are **NOT exempt** and strictly require a Plan Asset and user approval.
*   **Proactive Skill Discovery**: Before starting *any* SDD phase, you **MUST read the specific playbook (`skills/<persona>/SKILL.md`)** governing that phase, and declare explicitly in your first response that you have loaded and are executing that skill playbook.
*   **Spec Reconciliation**: Implementor agents are forbidden from editing specs or designs directly. Gaps must be drafted in a `spec_change_proposal.md` artifact and reviewed by the EM.
