---
name: retrospective-compiler
description: Parse implementation logs, identify architectural deviations or testing bottlenecks, and update the LESSONS_LEARNED.md registry.
---

# Retrospective Compiler Playbook

This playbook can be executed by either the **sdd-product-manager** or the **sdd-engineering-manager** (profiles `agents/sdd-product-manager.json` or `agents/sdd-engineering-manager.json`) at the end of a feature lifecycle.

---

## Playbook Execution

### 1. Context Gathering
*   Read `docs/sdd/ep-*/ft-*/VERIFICATION_REPORT.md` (must be `VERIFIED`).
*   Read the Coder's session checkpoint file (if any exists under `.agents/plugins/sdd-harness/history/checkpoint.md`).
*   Scan the Git history logs (`git log -n 10 --oneline`) and diff files to identify implementation struggles or design deviations.
*   Parse if the `--auto` flag is present in instructions.

### 2. Extract Learning Signals
Analyze the feature logs to identify:
1.  **Specification Gaps**: Were there user stories or requirements missing that had to be added midway?
2.  **Architectural Deviations**: Did the coder have to bypass a contract in `DESIGN.md` because of a library limitation?
3.  **Testing Bottlenecks**: Did the TDD loop hit the 3-retry escape hatch on any task card? Why did it fail?
4.  **Process Gaps**: Were there helper tools or configs missing?

### 3. Compile Lessons
*   Formulate a new entry for `docs/LESSONS_LEARNED.md` following the template layout.

#### Guided Mode (Default)
*   Present the drafted retro entry in chat.
*   Ask: *"I have drafted the retrospective entry. Shall I append these lessons to the global LESSONS_LEARNED.md registry?"*
*   **Wait for user confirmation before writing.**

#### Auto Mode (`--auto`)
If `--auto` is enabled:
*   Autonomously compile the retro entry.
*   Append the entry directly to `docs/LESSONS_LEARNED.md` without waiting for confirmation.

---

## Retrospective Registry Layout (`docs/LESSONS_LEARNED.md`)
The lessons learned registry is a single, continuous document appended in reverse chronological order:

```markdown
# Retrospective Registry & Lessons Learned

## [Feature Slug] - [Current Date]
*   **Component**: [e.g. Auth Subsystem / Database]
*   **Learnings / Findings**:
    *   [Explain what went wrong, e.g. SQL Alchemy event loop blocked when using sqlite in-memory in pytest].
*   **Preventative Recommendation**:
    *   [Actionable advice for future agents, e.g. Always set 'check_same_thread=False' on SQLite database connection pools in integration tests].
```

---

## 4. Completion
*   Append the compiled entry to `docs/LESSONS_LEARNED.md`.
*   Report completion: *"Lessons learned registry updated. The Spec-Driven Development cycle for this feature is now officially complete!"*
