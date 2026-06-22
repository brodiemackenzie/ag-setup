---
name: project-interviewer
description: Conduct the Vision Interview and compile the high-level Project Blueprint (docs/PROJECT.md) for a new project.
---

# Project Interviewer Skill Playbook

You must act as the **sdd-product-manager** (profile `agents/sdd-product-manager.json`) to execute this playbook.

---

## Playbook Execution

### 1. Parse Arguments & Mode Selection
*   Extract the Project Name and check if the `--auto` flag is present in your instructions.

### 2. Mode Execution

#### Guided Mode (Default)
Guide the user through the Vision Interview by collecting the following details **one at a time** (do not dump multiple questions in one turn to avoid user fatigue):
1.  **Core Objective**: Ask the user to describe the main purpose, goal, and core features of the application.
2.  **Technical Stack**: Ask the user to specify the target languages, frameworks, and database backend they intend to use.
3.  **Epics and Features Breakdown**: Ask the user to map out the application's boundaries into a structured list of Epics and Feature components (e.g. `ep-billing/ft-stripe-checkout`).

Once all details are collected:
*   Formulate a draft of `docs/PROJECT.md` following the template below.
*   Present the draft to the user in chat.
*   Explicitly ask: *"Shall I write this blueprint to docs/PROJECT.md and scaffold the feature folders?"*
*   **Wait for user confirmation before writing.**

#### Auto Mode (`--auto`)
If `--auto` is enabled:
*   Bypass the conversational interview.
*   Scan the local workspace to infer the project name and any existing readme metadata.
*   Use your best technical judgment to compile the `docs/PROJECT.md` file directly.
*   Write the file immediately without waiting for confirmation.

---

## Project Blueprint Template (`docs/PROJECT.md`)
The generated document must strictly conform to this structure:

```markdown
# Project Blueprint: [Project Title]

## 1. Core Objective
[Concise description of the system's purpose and success metrics]

## 2. Technical Stack
*   **Languages**: [e.g. Python 3.11]
*   **Frameworks**: [e.g. Flask 3.0]
*   **Database**: [e.g. SQLite]

## 3. Epic / Feature Component Breakdown
*   **Epic: [Epic Slug 1]** - [Epic Description]
    *   `ep-slug/ft-feature-slug-1`: [Feature Description]
    *   `ep-slug/ft-feature-slug-2`: [Feature Description]
```

---

## 3. Scaffolding Execution
Once approved (or completed autonomously in `--auto`):
1.  Write the compiled content to `docs/PROJECT.md`.
2.  For each feature listed in the breakdown (e.g., `ep-billing/ft-stripe-checkout`), scaffold the capsule directories:
    *   `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/`
3.  Create blank specification files inside each scaffolded feature folder to prepare for design discovery:
    *   Create `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/SPEC.md`
    *   Create `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/DESIGN.md`
    *   Create `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/TASKS.md`
4.  Report success: *"Blueprint written and feature folder capsules scaffolded. The PM can now spec individual features using /spec-feature."*
