---
name: generate-tasks
description: Decompose specifications and designs into a sequential BDD Gherkin task checklist (TASKS.md) capped at 12 cards.
---

# Task Generator Skill Playbook

You must act as the **sdd-technical-lead** (profile `agents/sdd-technical-lead.json`) to execute this playbook.

---

## Playbook Execution

### 1. Context Collection
*   Read `docs/sdd/ep-*/ft-*/SPEC.md` and `docs/sdd/ep-*/ft-*/DESIGN.md` in full.
*   Verify both are `APPROVED`.
*   Parse if the `--auto` flag is present in instructions.

### 2. Mode Execution

#### Guided Mode (Default)
1.  Ask the user if they have any task breakdown preferences (e.g. step-by-step model setup first, or routing setup first).
2.  Propose a draft `TASKS.md` following the template below:
    *   Ensure the checklist is capped at **up to 12 task cards** to enforce feature encapsulation.
    *   **Enforce Traceability**: Each task card MUST list the specific requirement ID (`req-N`) and design contract section it satisfies.
    *   **BDD Gherkin**: Every task card must define explicit `Given / When / Then` scenarios to guide the Coder's test suites.
3.  Present the proposal in chat and ask the user: *"I have compiled the task list draft. Please inspect the TASKS.md artifact. Click 'Proceed' to approve, or request changes."*
4.  **Wait for user approval before writing to disk.**

#### Auto Mode (`--auto`)
If `--auto` is enabled:
*   Bypass conversational planning.
*   Directly decompose requirements and designs into a sequential list of up to 12 task cards.
*   Write `docs/sdd/ep-*/ft-*/TASKS.md` directly.

---

## Task Checklist Template (`TASKS.md`)
The generated document must strictly conform to this structure:

```markdown
---
Type: Task Checklist
Status: DRAFT
Author: sdd-technical-lead
Date: [Current Date]
---

# Task Checklist: [Feature Name]

- [ ] `tsk-0-scaffold`: Initialize project code layout [Ref: DESIGN.md Sec 3]
  * **Given**: An empty workspace branch
  * **When**: Project packages are bootstrapped
  * **Then**: The test suite can run and verify zero-state success
- [ ] `tsk-1-model`: Implement user models [Ref: `req-1-valid-input`, DESIGN.md Sec 1]
  * **Given**: An empty database schema
  * **When**: A new signup query is executed
  * **Then**: The user record is created successfully
```

---

## 3. Completion
Once approved (or completed autonomously in `--auto`):
1.  Write the compiled content to `docs/sdd/ep-<epic>/ft-<feature>/TASKS.md`.
2.  Report completion: *"Task Checklist saved. Before sandbox creation, the EM must review and approve the task list using the design-auditor skill."*
