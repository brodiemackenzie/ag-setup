---
name: audit-tasks
description: Audit the Technical Lead's TASKS.md against DESIGN.md to check for completeness and verification alignment.
---

# Design Auditor Skill Playbook

You must act as the **sdd-engineering-manager** (profile `agents/sdd-engineering-manager.json`) to execute this playbook.

---

## Playbook Execution

### 1. Scope Verification
*   Read `docs/sdd/ep-*/ft-*/DESIGN.md` (APPROVED) and `docs/sdd/ep-*/ft-*/TASKS.md` (DRAFT) in full.
*   Parse if the `--auto` flag is present in instructions.

### 2. Audit Verification Checks
Perform a strict mapping audit of `TASKS.md`:
1.  **Contract Coverage**: Does the task list cover all database tables, models, and API endpoints defined in the technical design?
2.  **BDD Testability**: Does every task have BDD Gherkin scenarios (`Given/When/Then`) that can be translated directly into failing unit or integration tests?
3.  **Encapsulation Check**: Is the task count capped at 12?
4.  **Traceability Check**: Does every task reference the corresponding `req-N` functional spec requirement?

### 3. Mode Execution

#### Guided Mode (Default)
*   If gaps are found:
    *   State the gaps clearly in chat.
    *   Propose specific additions or Gherkin modifications to the TL.
    *   Ask: *"Shall I write these audit recommendations back to the TL?"*
    *   If user approves, edit `TASKS.md` to append the fixes.
*   If the audit is clean:
    *   Explain to the user that the audit is complete and clean.
    *   Ask: *"Shall I sign off on the TASKS.md spec and authorize feature sandbox provisioning?"*
    *   Upon confirmation, append the audit signature metadata block to `TASKS.md`:
        ```markdown
        ---
        EM_AUDIT: APPROVED
        EM_AUDIT_BY: [User LDAP]
        EM_AUDIT_DATE: [Current Date]
        ---
        ```

#### Auto Mode (`--auto`)
If `--auto` is enabled:
*   Autonomously verify all audit mapping checks.
*   If missing gaps are detected:
    *   Edit `TASKS.md` directly to insert the missing task definitions or test setups.
*   Sign off the audit autonomously by writing the approval header block to `TASKS.md` directly.

---

## 4. Completion
*   Save the signed `TASKS.md` to disk.
*   Report completion: *"Task Checklist audit complete. The Coder is now authorized to open the workspace using the /open-feature slash command."*
