# SDD Retrospective Playbook

This playbook guides the `sdd-project-manager` agent through the retrospective analysis that harvests spec gaps, engineering bugs, and design lessons upon feature completion.

---

## Objective
Analyze Git commit and diff history after a feature branch is merged, extract design/architectural insights, and record them inside a local lessons learned registry to prevent future development pitfalls.

---

## The Retrospective Harvesting Protocol

Immediately after a feature worktree is closed and merged back into the main branch, execute the following harvesting steps:

1. **Parse Git History**: Run git log to extract the list of commits for the feature branch:
   ```bash
   git log -n 10
   ```
2. **Evaluate Spec Change Proposals**: Read any `spec_change_proposal.md` created in the worktree. Identify the root cause (e.g., *Why did the specification drift from the implementation? Was it a library limitation or an unhandled edge case?*).
3. **Formulate Actionable Lessons**:
   * Keep lessons concise, active, and architectural.
   * Avoid vague summaries (e.g. "wrote code"). Focus on concrete warnings (e.g., *Warning: Swagger client version X requires explicit header Y; mock this by...*).

---

## Local Lessons Learned Registry

All harvested lessons must be written and appended strictly to a local file in the target workspace:
* **File Location**: `docs/lessons_learned.md` (relative to the top-level repository).

### Registry Format
```markdown
# SDD Lessons Learned Registry

This document tracks architectural and implementation lessons compiled during project retrospectives. Agents must review this registry prior to drafting new specifications.

---

## Epic: [Epic Slug] | Feature: [Feature Slug]
* **Date**: [YYYY-MM-DD]
* **Specification Gap Discovered**: Describe the edge case or gap that required a spec change proposal.
* **Bugs & Gotchas**: List any third-party library limitations, API integration anomalies, or styling caveats.
* **Architectural Recommendations**: Actionable instructions for future features (e.g., *When interfacing with component A, always initialize schema B first.*).

---
```

### Consumption Rule
The `sdd-spec-writer` and `sdd-design-architect` agents must read `docs/lessons_learned.md` at the start of every new feature spec discovery phase, ensuring that past mistakes are never repeated.
