---
trigger: always_on
description: Enforce Spec-Driven Development (SDD) Spec-Design-Tasks pipeline and controls.
---

# SDD Core Pipeline Rules

You must strictly adhere to these core planning controls when executing design or milestone increments:

## 1. Phase 0: High-Level Project Proposal (Top-Level Vision)
* Before creating any feature branches, worktrees, specs, or writing code, you MUST compile a comprehensive Project Proposal artifact (`docs/proposals/project_proposal.md`) detailing:
  1. **Project Objective & Core Essence**: Concise, plain-English high-level vision.
  2. **Architectural Pillars & Tech Stack**: Declared technologies, frameworks, and database systems.
  3. **Epic & Feature Map Inventory**: List of Epics and their specific modular Features to implement.
* **Constraints**: Strictly no low-level database schemas, REST request mock tables, or individual user journeys in the proposal. No other files can be created until the user approves the proposal.

## 2. Phase 1: Feature Worktree Sandboxing
* Once the high-level proposal is approved, the next step is transitioning to a sandboxed worktree:
  1. Collect the target Epic and Feature to implement from the approved proposal's inventory.
  2. Execute `manage_worktree.sh prototype <epic> <feature>` to provision the sandboxed branch folder (`worktrees/<epic>/<feature>/`).
  3. Restrict all subsequent functional design and coding work exclusively inside that sandboxed folder.

## 3. The 3-Tier Feature Capsule Pipeline (Worktree Level)
Inside the active feature worktree, compilation must proceed in this exact chronological sequence:
1. **Functional Specification (`SPEC.md`)**: Plain-English objective, user journeys, requirements, and success criteria. Banish all technical code blocks or API routes.
2. **Technical Design (`DESIGN.md`)**: Schema tables, REST mock models, Mermaid charts, and a Test Verification Strategy. Production code is strictly prohibited.
3. **Actionable Task Checklist (`TASKS.md`)**: BDD Gherkin task list (`Given/When/Then`), capped at **up to 12 tasks**.

## 4. Executing Controls
* **Skill-First Discovery Hook (CRITICAL)**: Before starting *any* SDD phase (e.g., drafting a proposal in Phase 0, writing specifications in Phase 2, compiling designs in Phase 3, or executing tasks in Phase 4), you **MUST proactively scan the `.agents/skills/` folder** in your active workspace, locate the specialized playbook folder governing the phase, and read its `SKILL.md` in full before executing any actions or conversational interviews.
* **No Eager Execution**: You are strictly forbidden from relying solely on high-level rule outlines. You must verify and read the specific local `SKILL.md` first to ensure 100% compliance with the workspace's custom playbooks, and declare explicitly in your first chat response that you have loaded and are executing that skill playbook.
* **No Blind Coding**: Writing production code or test suites is strictly forbidden until both `SPEC.md` and `DESIGN.md` are completed and approved by the user.
* **Spec Reconciliation**: Coder agents are forbidden from editing specs or designs directly. Gaps must be drafted in a `spec_change_proposal.md` artifact and reviewed by the Architect.
* **Formatting Hook**: Auto-run `mdformat` after any markdown edit to maintain layout hygiene.

## 5. Strict Role-Based Orchestration Protocol
* **Top-Level Orchestrator (The Project Manager / Architect Transition)**:
  * In the root top-level directory, you MUST coordinate the initial Project Proposal.
  * You must act as the **sdd-architect** (profile `agents/sdd-architect.json`) to conduct the Vision Interview and draft the Project Proposal (`docs/proposals/project_proposal.md`).
  * Once the Proposal is approved, you must act as the **sdd-project-manager** (profile `agents/sdd-project-manager.json`) to collect the target Feature choice, run `manage_worktree.sh` branch provisioning, spawn a sandboxed subagent with the `sdd-architect` profile inside the worktree, and wait for it.
* **Sandboxed Feature Designer (The Architect)**:
  * Once spawned inside a feature worktree, you MUST act strictly as the **sdd-architect** inside that workspace sandbox.
  * You conduct the interactive spec Q&A and draft the `SPEC.md` and `DESIGN.md`. You are forbidden from writing code or executing shell scripts.
  * Once design is complete, hand the task checklist back to the PM or Implementor subagents.
