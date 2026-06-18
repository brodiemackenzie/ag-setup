---
name: blueprint
description: Conduct the Vision Interview and compile the high-level Project Blueprint (docs/PROJECT.md) for a new project.
---

# Project Blueprint Workflow

You must act as the **sdd-architect** to compile the Project Blueprint (`docs/PROJECT.md`).

## 1. Conversational interview
Guide the user through the Vision Interview by collecting the following details **one at a time** (do not dump multiple questions in one turn to avoid user fatigue):
1.  **Core Objective**: Ask the user to describe the main purpose, goal, and core features of the application.
2.  **Technical Stack**: Ask the user to specify the target languages, frameworks, and database backend they intend to use.
3.  **Epics and Features Breakdown**: Ask the user to map out the application's boundaries into a structured list of Epics and Feature components (e.g. `ep-billing/ft-stripe-checkout`).

## 2. Compile Blueprint
Once all details are collected:
*   Formulate a draft of `docs/PROJECT.md` containing:
    *   **Project Title**
    *   **Core Objective**
    *   **Tech Stack**
    *   **Epic / Feature Breakdown** (using standard epic/feature slugs)
*   Present the draft to the user in chat.
*   Explicitly ask: *"Shall I write this blueprint to docs/PROJECT.md and scaffold the feature folders?"*

## 3. Scaffolding Execution
Once the user confirms (e.g., "yes"):
1.  Write the compiled content to `docs/PROJECT.md`.
2.  For each feature listed in the breakdown (e.g., `ep-guest-submissions/ft-submission-form`), scaffold the capsule directories:
    *   `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/`
3.  Create blank specification files inside each scaffolded feature folder to prepare for specification discovery:
    *   Create `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/SPEC.md`
    *   Create `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/DESIGN.md`
    *   Create `docs/sdd/ep-<epic-slug>/ft-<feature-slug>/TASKS.md`
4.  Report success and state the next steps: *"Blueprint written and feature folder capsules scaffolded. You can now spec individual features using /spec-feature."*
