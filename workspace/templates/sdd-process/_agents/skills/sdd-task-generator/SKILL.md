# SDD Task Generator Playbook

This playbook guides the `sdd-architect` or `sdd-project-manager` through compiling actionable **Gherkin-style BDD Task checklists (TASKS.md)** inside an active Git worktree feature capsule.

---

## Objective
Translate the architecture contracts and Verification Strategy from `DESIGN.md` into a clear, chronological execution checklist of actionable developer steps.

---

## Checklist Document Structure

The resulting file must be saved at `docs/sdd/<epic-slug>/<feature-slug>/TASKS.md` inside the active worktree capsule, conforming strictly to this structure:

```markdown
# Actionable Tasks: [Feature Title in Title Case]

This document tracks the TDD implementation steps. Tasks must be checked off sequentially by the implementor.

---

## Epic: [Epic Title]
## Feature: [Feature Title]

---

## Gherkin BDD Checklist

- [ ] **Task 1: [Ref: SubsystemNode] Description of Deliverable**
  * **Given** [Initial system state or mock configurations]
  * **When** [Action performed by user or test trigger]
  * **Then** [Expected outcome and assertions]
  
- [ ] **Task 2: [Ref: SubsystemNode] Description**
  * **Given** ...
  * **When** ...
  * **Then** ...
```

---

## Naming & Gherkin Alignments

* **Reference Target**: Every task must specify its subsystem mapping reference (e.g. `[Ref: Table Schema]`, `[Ref: Router Controller]`, `[Ref: Test Suite]`).
* **BDD Alignment**: Tasks must have clear `Given`, `When`, and `Then` descriptors.
* **TDD Focus**: The task must implicitly or explicitly guide the implementor to write a failing RED test before writing production code.

---

## The 12-Task Checklist Limit

To prevent scope bloat and enforce micro-feature isolation, a single `TASKS.md` checklist **MUST NOT contain more than 12 tasks (`[ ]`)**.

### Splitting Protocol for Over-Scoped Features
If compilation results in **more than 12 tasks**:
1. **Halt Execution**: Block the spec/task compilation immediately.
2. **Draft Sub-Feature Plan**: The Project Manager agent must generate a modular sub-feature splitting plan (e.g., `part-1`, `part-2`).
3. **Allocate Isolated Worktrees**: Present the plan to the user and advise creating isolated Git worktrees for each split feature capsule.
