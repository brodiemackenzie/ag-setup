---
trigger: always_on
description: Enforce Spec-Driven Development (SDD) Spec-Design-Tasks pipeline and controls.
---

# SDD Core Pipeline Rules

You must strictly adhere to these core planning controls when executing design or milestone increments:

## 1. Phase 0: High-Level Project Blueprint (docs/PROJECT.md)
* Before creating any feature branches, worktrees, specs, or writing code, you MUST compile a comprehensive Project Blueprint artifact (`docs/PROJECT.md`) in the project's documentation folder detailing:
  1. **Core Objective**: Clear explanation of system purpose and factory models.
  2. **Target Audience & Success Criteria**: Target users and concrete, measurable success metrics.
  3. **Core Features**: Enumerate high-level user-facing and backend capabilities.
  4. **Out of Scope**: Explicitly declare boundaries and deferred features.
  5. **High-Level Tech Stack**: Declared languages, frameworks, libraries, and dev tools.
  6. **Epic / Feature Component Breakdown**: List of Epics and their specific modular Features.
  7. **Open Questions**: Open functional or technical decisions needing resolution.
* **Constraints**: Strictly no low-level database schemas, REST request mock tables, or individual user journeys in the blueprint. No other files can be created until the user approves the blueprint.

## 2. Phase 1: Feature Specification & Design (Parent Repository)
* Once the high-level project blueprint is approved, you MUST author functional specifications and designs directly in the parent repository under the documentation directory:
  1. **Functional Specification (`docs/sdd/ep-<epic_name>/ft-<feature_name>/SPEC.md`)**: Conduct the spec discovery interview, outline user journeys, requirements (`req-<requirement_name>`), and success criteria. Banish all technical code blocks.
  2. **Technical Design (`docs/sdd/ep-<epic_name>/ft-<feature_name>/DESIGN.md`)**: Define data models, schemas, and a test Verification Strategy. Production code is strictly prohibited.
  3. **Actionable Task Checklist (`docs/sdd/ep-<epic_name>/ft-<feature_name>/TASKS.md`)**: Compile a BDD Gherkin task list (`tsk-<task_name>`), capped at **up to 12 tasks**.

## 3. Phase 2: Feature Worktree Sandboxing (Code Implementation ONLY)
* Once the specification and design are approved, the next step is transitioning to code execution:
  1. The Project Manager MUST commit all approved specifications (`SPEC.md`, `DESIGN.md`, `TASKS.md`), the project blueprint (`docs/PROJECT.md`), and any customized `.agents/` rules in the parent repository first.
  2. The Project Manager will then execute `manage_worktree.sh prototype ep-<epic_name> ft-<feature_name>` to provision the sandboxed worktree folder under `~/.gemini/jetski/worktrees/<project>/ep-<epic_name>-ft-<feature_name>/`. This will automatically check out the entire repository state via Git. The PM will then trigger the JetSki launcher to open the worktree in a fresh IDE window.
  3. The Project Manager MUST halt execution immediately after launching the window. All subsequent coding and implementation will occur in the new workspace window's chat.

## 4. Executing Controls
* **Plan-First Execution Hook (CRITICAL)**: Before modifying any files or executing write operations, you MUST compile a clear Plan Asset (e.g., Implementation Plan or Task checklist artifact) and explicitly state to the user in chat what changes are going to happen. File modifications without stating what is going to happen are strictly forbidden, for all chats, without exception.
* **Skill-First Discovery Hook (CRITICAL)**: Before starting *any* SDD phase (e.g., drafting a proposal in Phase 0, writing specifications in Phase 2, compiling designs in Phase 3, or executing tasks in Phase 4), you **MUST proactively scan the `.agents/skills/` folder** in your active workspace, locate the specialized playbook folder governing the phase, and read its `SKILL.md` in full before executing any actions or conversational interviews.
* **No Eager Execution**: You are strictly forbidden from relying solely on high-level rule outlines. You must verify and read the specific local `SKILL.md` first to ensure 100% compliance with the workspace's custom playbooks, and declare explicitly in your first chat response that you have loaded and are executing that skill playbook.
* **No Blind Coding**: Writing production code or test suites is strictly forbidden until both `SPEC.md` and `DESIGN.md` are completed and approved by the user.
* **Spec Reconciliation**: Coder agents are forbidden from editing specs or designs directly. Gaps must be drafted in a `spec_change_proposal.md` artifact and reviewed by the Architect.

## 5. Strict Role-Based Orchestration Protocol
* **Top-Level Orchestrator (The Project Manager / Architect Transition)**:
  * In the root top-level directory, you MUST coordinate the initial Project Blueprint, specifications, and designs.
  * You must act as the **sdd-architect** (profile `agents/sdd-architect.json`) to conduct the Vision/Spec interviews and draft `PROJECT.md`, `SPEC.md`, and `DESIGN.md` in the parent repository context.
  * Once the Design and Tasks are approved, you must act as the **sdd-project-manager** (profile `agents/sdd-project-manager.json`) to commit all approved specs and blueprints, run `manage_worktree.sh` branch provisioning, launch the new JetSki workspace window, and **immediately halt execution**. Do not spawn subagents.
* **Sandboxed Implementor (The Coder)**:
  * In the newly opened JetSki workspace, the user will start a new conversation. You must act strictly as the **sdd-implementor** (profile `agents/sdd-implementor.json`) in this sandboxed workspace.
  * You implement code and test cases, execute verification suites locally, and capture passing console logs directly in the conversation history. You are forbidden from editing specifications or designs.
