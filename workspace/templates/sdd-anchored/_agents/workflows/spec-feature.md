---
description: Conduct requirements discovery and compile SPEC.md, DESIGN.md, and TASKS.md for a specific feature.
---

# Feature Specification Workflow

You must act as the **sdd-architect** to compile specifications, designs, and task checklists.

## 1. Scope Selection
*   Ask the user which Epic and Feature they want to spec (e.g. `ep-guest-submissions/ft-submission-form`). The feature directory must already exist on disk (scaffolded during `/blueprint`).

## 2. Playbook Initialization (Proactive Skill Loading)
*   You **MUST** read the following playbooks before starting the conversational interview:
    *   `.agents/skills/sdd-spec-writer/SKILL.md` (for functional specs rules)
    *   `.agents/skills/sdd-design-architect/SKILL.md` (for data structures, diagrams, and verification checks)
    *   `.agents/skills/sdd-task-generator/SKILL.md` (for Gherkin BDD checklist parameters)

## 3. Conversational Discovery Interview
Collect the required parameters **one at a time**:
1.  **Functional Requirements**: Ask the user to describe the user journeys, inputs, validation rules, and success metrics.
2.  **API / Schema Shapes**: Ask the user to clarify database storage shapes and integration contracts (endpoints, payloads).
3.  **Verification Bounds**: Confirm if they have specific integration test desires (e.g., SQLite, mocking parameters).

*   *Note*: To avoid user fatigue, if the user provides these requirements in a single comprehensive payload, you may bypass individual interview questions.

## 4. Draft Specifications & HITL Audit Checklist
*   Formulate drafts of the three core specification files:
    1.  `SPEC.md`: Plain-English requirements (`req-<name>`) and journeys. No code blocks.
    2.  `DESIGN.md`: Data schemas, REST/RPC API contracts, Mermaid sequence diagrams, and test Verification Strategy.
    3.  `TASKS.md`: Actionable BDD task checklist (`tsk-<name>`) capped at **up to 12 tasks**. If greenfield, `tsk-0-scaffold` must be the first task.
*   Present the drafted specifications to the user in chat.
*   **Mandatory HITL Audit Checkpoint**: You must explicitly ask the user to verify and approve the draft by answering these three audit points:
    1.  **User Journeys Check**: Do the plain-English journeys in `SPEC.md` match your business objective?
    2.  **Contracts Check**: Do the REST/RPC endpoints and database schemas in `DESIGN.md` align with your system architecture?
    3.  **BDD Tasks Check**: Do the Gherkin scenario checklists in `TASKS.md` represent a complete, chronological path to build the code, and are they under the 12-task limit?
*   Ask the user: *"Please review the specs against the three audit points. Do you approve writing these files to disk?"*

## 5. File Execution
Once the user confirms approval (e.g., "yes, write the spec files"):
1.  Write the compiled content to their respective files inside the feature capsule directory:
    *   `docs/sdd/ep-<epic>/ft-<feature>/SPEC.md`
    *   `docs/sdd/ep-<epic>/ft-<feature>/DESIGN.md`
    *   `docs/sdd/ep-<epic>/ft-<feature>/TASKS.md`
2.  Report success: *"Specification, Design, and Tasks have been compiled successfully. You are ready to open a sandbox using /start-feature."*
