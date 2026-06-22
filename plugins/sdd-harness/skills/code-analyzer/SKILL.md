---
name: code-analyzer
description: Scan the codebase to extract patterns, interfaces, and dependencies before technical design.
---

# Code Analyzer Skill Playbook

You must act as the **sdd-engineering-manager** (profile `agents/sdd-engineering-manager.json`) to execute this playbook.

---

## Playbook Execution

### 1. Scope Target
*   Identify the target Epic and Feature to analyze.
*   Verify `docs/sdd/ep-*/ft-*/SPEC.md` exists and is `APPROVED`.
*   Parse if the `--auto` flag is present in instructions.

### 2. Mode Execution

#### Guided Mode (Default)
1.  Ask the user what specific subdirectories, modules, or database configurations are most relevant.
2.  Perform programmatic code searches (`code_search`) to locate existing classes, functions, and imports related to the feature.
3.  Propose a draft `CODE_ANALYSIS.md` outlining the discoveries, dependencies, and reusable patterns.
4.  Present the proposal in chat and ask the user to verify.
5.  **Wait for user confirmation before writing.**

#### Auto Mode (`--auto`)
If `--auto` is enabled:
*   Bypass conversational discovery.
*   Autonomously perform codebase searches (`code_search`) to locate imports, databases, and libraries.
*   Identify existing conventions, gotchas, and patterns.
*   Write `docs/sdd/CODE_ANALYSIS.md` directly.

---

## Codebase Analysis Template (`CODE_ANALYSIS.md`)
The generated document must strictly conform to this structure:

```markdown
---
Type: Codebase Grounding Report
Status: COMPILED
Author: sdd-engineering-manager
Date: [Current Date]
---

# Codebase Analysis: [Feature Name]

## 1. Relevant Modules & Files
*   `path/to/file.py`: Implements the existing [Module Name] class.

## 2. Reusable Code & Conventions
*   **Database Access**: Queries should use the [ORM Name] connection pool patterns defined in `db.py`.
*   **Logging**: Use the logger class configured in `utils/logging.py`.

## 3. Discovered Technical Gotchas
*   Avoid importing [Library Name] directly as it blocks event loops; use the async wrapper in `async_utils.py` instead.
```

---

## 3. Completion
*   Write the report to `docs/sdd/CODE_ANALYSIS.md` (if one doesn't exist, create it. If it exists, append a new section for this feature).
*   Report completion: *"Codebase grounding complete. Suggest proceeding to technical design using the design-architect skill."*
