---
trigger: always_on
description: Enforce the 8-step Spec-Driven Development (SDD) software factory pipeline.
---

# SDD Workflow Rules

You must strictly adhere to the 8-step software factory workflow when planning, designing, or implementing features:

---

## 1. The 8-Step Pipeline

1.  **Step 1: Feature Specification (`/spec-feature`)**
    *   **Role**: Product Manager (`sdd-product-manager`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/SPEC.md`
2.  **Step 2: Codebase Grounding (`/analyze-code`)**
    *   **Role**: Engineering Manager (`sdd-engineering-manager`)
    *   **Asset**: `docs/sdd/CODE_ANALYSIS.md`
3.  **Step 3: Technical Design (`/design-feature`)**
    *   **Role**: Engineering Manager (`sdd-engineering-manager`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/DESIGN.md`
4.  **Step 4: Execution Planning (`/generate-tasks`)**
    *   **Role**: Technical Lead (`sdd-technical-lead`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/TASKS.md`
5.  **Step 5: Specification Audit (`/audit-tasks`)**
    *   **Role**: Engineering Manager (`sdd-engineering-manager`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/TASKS.md` (Audit approval header)
6.  **Step 6: Sandboxed Execution (`/start-feature`)**
    *   **Role**: Implementor (`sdd-implementor`)
    *   **Asset**: Local code, tests, and Git worktree sandbox
7.  **Step 7: Code Verification (`/verify-feature`)**
    *   **Role**: Technical Lead (`sdd-technical-lead`)
    *   **Asset**: `docs/sdd/ep-*/ft-*/VERIFICATION_REPORT.md`
8.  **Step 8: Retrospective (`/retrospective`)**
    *   **Role**: Product Manager & Engineering Manager
    *   **Asset**: `docs/LESSONS_LEARNED.md`

---

## 2. Command-Persona Ownership Enforcement

Before executing any slash command, you **MUST** verify that your active system profile matches the owner persona declared in the mapping table below:

| Command (Skill Name) | Required Owner Agent Profile Persona |
| :--- | :--- |
| `/blueprint-project` | `sdd-product-manager` |
| `/spec-feature` | `sdd-product-manager` |
| `/analyze-code` | `sdd-engineering-manager` |
| `/design-feature` | `sdd-engineering-manager` |
| `/generate-tasks` | `sdd-technical-lead` |
| `/audit-tasks` | `sdd-engineering-manager` |
| `/open-feature` | `sdd-implementor` |
| `/close-feature` | `sdd-implementor` |
| `/verify-feature` | `sdd-technical-lead` |
| `/retrospective` | `sdd-engineering-manager` OR `sdd-product-manager` |
| `/compile-docs` | `sdd-engineering-manager` OR `sdd-product-manager` |

*   **Enforcement Rule**: If you parse one of these commands from the user (or are about to execute it autonomously) and your active system prompt persona does **not** match the required profile name:
    *   **Halt execution immediately.** Do not call any further tools.
    *   Output the following warning banner:
        > [!CAUTION]
        > **Execution Blocked**: You are running this command under the wrong agent profile. Please select the **[Required Agent Persona]** profile in your chat panel settings and retry.

---

## 3. Dynamic State Discovery & Startup

*   **Startup Verification Rule**: Upon starting a new conversation (on the very first turn), you **MUST** immediately run the programmatic status script using `run_command`:
    ```bash
    bash .agents/plugins/sdd-harness/scripts/status_report.sh
    ```
*   Display the output table at the top of your response.
*   **Next Steps Recommendation**: Below the Status Report table, recommend the next action based on the discovered file states:
    1.  If `docs/PROJECT.md` is missing ➔ Recommend `/blueprint-project` (using `blueprint-project`).
    2.  If `SPEC.md` is missing/draft ➔ Recommend `/spec-feature` (using `spec-feature`).
    3.  If `CODE_ANALYSIS.md` is missing ➔ Recommend `/analyze-code` (using `analyze-code`).
    4.  If `DESIGN.md` is missing/draft ➔ Recommend `/design-feature` (using `design-feature`).
    5.  If `TASKS.md` is missing/draft ➔ Recommend `/generate-tasks` (using `generate-tasks`).
    6.  If `TASKS.md` has no EM approval signature ➔ Recommend `/audit-tasks` (using `audit-tasks`).
    7.  If audit is complete and you are in the parent repo ➔ Instruct the user to run `/open-feature` to provision the sandbox.
    8.  If you are in a sandbox worktree and tasks remain unchecked ➔ Recommend `/start-feature` (using `start-feature` & `tdd-flow`).
    9.  If all tasks are checked, but you are inside the worktree ➔ Instruct the user to return to the parent repo and run `/close-feature` to merge.
    10. If sandbox is closed, but `VERIFICATION_REPORT.md` is missing ➔ Recommend `/verify-feature` (using `verify-feature`).
    11. If verified, but lessons are not updated ➔ Recommend `/retrospective` (using `retrospective`).

---

## 4. Plan-First Gate

*   **Plan-First Hook**: Before modifying any files or executing write operations, you MUST compile a clear Plan Asset (e.g., Implementation Plan or Task checklist artifact) and explicitly state to the user in chat what changes are going to happen. You **MUST set `RequestFeedback: true`** in the plan's metadata, **stop calling tools immediately**, and **wait for the user's explicit approval or 'Proceed' button confirmation** before executing any changes. File modifications without stating what is going to happen and waiting for approval are strictly forbidden, for all chats, without exception, **UNLESS** you are operating in one of these contexts:
    1.  **Test/Simulation Projects**: The active project name contains `test` or `sim` (all simulation phases run eagerly to prevent E2E hangs).
    2.  **Active TDD Task Execution**: You are inside a feature worktree (path contains `worktrees/`) and are **actively executing the structured TDD loop** (writing/running unit or integration tests to satisfy a specific `tsk-<id>` task from the checklist in `TASKS.md`). Any ad-hoc requests, free-form chats, or design alterations that bypass the structured TDD checklist are **NOT exempt** and strictly require a Plan Asset and user approval.
*   **Proactive Skill Discovery**: Before starting *any* SDD phase, you **MUST read the specific playbook (`skills/<persona>/SKILL.md`)** governing that phase, and declare explicitly in your first response that you have loaded and are executing that skill playbook.
*   **Spec Reconciliation**: Implementor agents are forbidden from editing specs or designs directly. Gaps must be drafted in a `spec_change_proposal.md` artifact and reviewed by the EM.
