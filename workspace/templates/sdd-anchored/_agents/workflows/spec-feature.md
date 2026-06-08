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

## 3. Phase A: Functional Specification (SPEC.md)
1.  **Interview**: Conduct a targeted conversational interview strictly focused on the functional scope, user personas, input validations, and user journey paths.
2.  **Draft Artifact**: Compile the requirements into a new Antigravity Artifact named **`sdd_spec_draft`** (set `IsArtifact` to true, and use type `other`). Ensure requirements use `req-` prefixes and contain no code blocks.
3.  **HITL Review**: Instruct the user: *"I have generated the Functional Specification draft. Please review the 'sdd_spec_draft' artifact tab. You can leave comments directly on the artifact for any changes needed. Once satisfied, reply: 'SPEC is approved'."*
4.  **Iteration**: If the user leaves comments or requests edits, surgically edit the `sdd_spec_draft` artifact. Do not proceed until you receive SPEC approval.

## 4. Phase B: Technical Design (DESIGN.md)
1.  **Interview**: Conduct a targeted conversational interview focused on the technical design: database schemas, API payload structures (endpoints, parameters), Sequence diagrams, and mock test constraints.
2.  **Draft Artifact**: Compile the design into a new Antigravity Artifact named **`sdd_design_draft`** (set `IsArtifact` to true). Include database entity shapes and endpoint contracts.
3.  **HITL Review**: Instruct the user: *"I have generated the Technical Design draft. Please review the 'sdd_design_draft' artifact tab. Once satisfied, reply: 'DESIGN is approved'."*
4.  **Iteration**: Surgically edit `sdd_design_draft` based on comments. Do not proceed until you receive DESIGN approval.

## 5. Phase C: Actionable Tasks Checklist (TASKS.md)
1.  **Draft Check**: Map the approved specifications and design contracts into a sequential, actionable BDD task checklist.
2.  **Draft Artifact**: Compile the tasks list into a new Antigravity Artifact named **`sdd_tasks_draft`** (set `IsArtifact` to true).
    *   Ensure tasks are capped at **up to 12 tasks**.
    *   Ensure each task defines explicit Gherkin `Given/When/Then` scenarios.
3.  **HITL Review**: Instruct the user: *"I have generated the Task Checklist draft. Please review the 'sdd_tasks_draft' artifact tab. Once satisfied, reply: 'TASKS is approved'."*
4.  **Iteration**: Edit `sdd_tasks_draft` based on comments. Do not proceed until you receive TASKS approval.

## 6. Phase D: Commit and Write to Workspace
Once all three drafts are approved:
1.  Copy the finalized contents from the three artifacts and write them to their permanent workspace files inside the feature capsule:
    *   `docs/sdd/ep-<epic>/ft-<feature>/SPEC.md`
    *   `docs/sdd/ep-<epic>/ft-<feature>/DESIGN.md`
    *   `docs/sdd/ep-<epic>/ft-<feature>/TASKS.md`
2.  Clean up the temporary draft artifacts.
3.  Report completion: *"Specification, Design, and Tasks have been compiled and saved to disk. You are now ready to open a sandbox using /start-feature."*
