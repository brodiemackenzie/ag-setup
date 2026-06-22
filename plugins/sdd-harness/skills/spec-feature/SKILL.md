---
name: spec-feature
description: Conduct functional requirements discovery and compile SPEC.md for a feature.
---

# Spec Writer Skill Playbook

You must act as the **sdd-product-manager** (profile `agents/sdd-product-manager.json`) to execute this playbook.

---

## Playbook Execution

### 1. Scope Selection & Verification
*   Identify the target Epic and Feature folder (e.g. `docs/sdd/ep-billing/ft-stripe-checkout/`).
*   Confirm that `docs/PROJECT.md` exists and contains this feature.
*   Parse if the `--auto` flag is present in instructions.

### 2. Mode Execution

#### Guided Mode (Default)
Conduct a targeted conversational interview strictly focused on the functional scope. Ask questions **one at a time**:
1.  **Objective**: What is the immediate goal of this feature?
2.  **User Journeys**: Walk through the step-by-step user path (who triggers it, what input they provide, what they expect to see).
3.  **Requirements**: Enumerate functional requirements (`req-N`), validations, and explicit error conditions.
4.  **Acceptance Criteria**: What must hold true to declare the feature functionally complete?

Once details are collected:
*   Compile a draft of the `SPEC.md` document following the template below.
*   Present the draft in chat.
*   Ask the user: *"I have generated the Functional Specification draft. Please review the SPEC.md artifact. Click 'Proceed' to approve, or request edits."*
*   **Wait for user approval before writing to disk.**

#### Auto Mode (`--auto`)
If `--auto` is enabled:
*   Bypass the conversational interview.
*   Scan the codebase and existing blueprint to gather domain context.
*   Use your best judgment to draft functional specifications and user journeys.
*   Write `docs/sdd/ep-*/ft-*/SPEC.md` directly.

---

## Specification Template (`SPEC.md`)
The generated document must strictly conform to this structure:

```markdown
---
Type: Functional Specification
Status: DRAFT
Author: sdd-product-manager
Date: [Current Date]
---

# Functional Specification: [Feature Name]

## 1. Purpose & User Persona
[Description of who this is for and why they need it]

## 2. User Journeys
*   **Journey 1**: Given [Initial State], When [User Action], Then [Expected Outcome]

## 3. Functional Requirements
*   `req-1-valid-input`: The system must validate that [Fields] are not empty.
*   `req-2-processing`: The system must execute [Logic].

## 4. Acceptance Criteria
*   When [Condition], the system returns [Result].
```

---

## 3. Completion
Once approved (or completed autonomously in `--auto`):
1.  Write the compiled content to `docs/sdd/ep-<epic>/ft-<feature>/SPEC.md`.
2.  Set `Status` to `APPROVED` and record the user's approval.
3.  Report completion: *"Functional Specification compiled and saved. Suggest loading the Engineering Manager to design the feature using the design-architect skill."*
