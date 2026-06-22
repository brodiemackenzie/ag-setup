---
name: design-feature
description: Compile cross-cutting technical design (DESIGN.md) mapping spec requirements to code interfaces.
---

# Design Architect Skill Playbook

You must act as the **sdd-engineering-manager** (profile `agents/sdd-engineering-manager.json`) to execute this playbook.

---

## Playbook Execution

### 1. Scope Verification
*   Verify that `docs/sdd/ep-*/ft-*/SPEC.md` exists and is `APPROVED`.
*   Read `docs/sdd/CODE_ANALYSIS.md` if present to align design with conventions.
*   Parse if the `--auto` flag is present in instructions.

### 2. Mode Execution

#### Guided Mode (Default)
Conduct a technical design interview. Ask questions **one at a time**:
1.  **Architecture**: What is the structural approach (endpoints, classes, database tables)?
2.  **API Contracts**: Detail request payloads, parameters, response codes, and schemas.
3.  **Data Models**: Propose the schema columns and relationships.
4.  **Verification Strategy**: How will we test this (what to mock, what integration tests are required)?

Once details are collected:
*   Compile a draft of the `DESIGN.md` document following the template below.
*   **Enforce Traceability**: Ensure every model, table, and endpoint block explicitly references the corresponding `req-N` ID it satisfies.
*   Present the draft in chat and ask the user: *"I have generated the Technical Design draft. Please inspect the DESIGN.md artifact tab. Click 'Proceed' to approve, or request edits."*
*   **Wait for user approval before writing to disk.**

#### Auto Mode (`--auto`)
If `--auto` is enabled:
*   Bypass conversational design discovery.
*   Scan functional requirements and code analysis.
*   Make best technical design choices (schemas, models, endpoints) autonomously.
*   Write `docs/sdd/ep-*/ft-*/DESIGN.md` directly.

---

## Design Template (`DESIGN.md`)
The generated document must strictly conform to this structure:

```markdown
---
Type: Technical Design
Status: DRAFT
Author: sdd-engineering-manager
Date: [Current Date]
---

# Technical Design: [Feature Name]

## 1. Database Schemas
*   **Table `users`** [Ref: `req-1-valid-input`]
    *   `id`: INTEGER PRIMARY KEY
    *   `email`: VARCHAR UNIQUE

## 2. API & Class Interface Contracts
*   **POST `/api/v1/auth/signup`** [Ref: `req-2-processing`]
    *   **Request Payload**:
        ```json
        { "email": "user@example.com" }
        ```
    *   **Response**: `201 Created`

## 3. Mock & Verification Strategy
*   **Unit Tests**: Mock [Service Name] class returns using fixture mocks.
*   **Integration Tests**: Execute in-memory SQLite database runs.
```

---

## 3. Completion
Once approved (or completed autonomously in `--auto`):
1.  Write the compiled content to `docs/sdd/ep-<epic>/ft-<feature>/DESIGN.md`.
2.  Set `Status` to `APPROVED` and record the user's approval.
3.  Report completion: *"Technical Design approved and saved. Suggest loading the Technical Lead to plan tasks using the task-generator skill."*
