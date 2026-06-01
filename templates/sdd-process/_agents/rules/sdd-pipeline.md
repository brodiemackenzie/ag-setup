---
trigger: always_on
description: Enforce Spec-Driven Development (SDD) Spec-Design-Tasks pipeline and controls.
---

# SDD core Pipeline Rules

You must strictly adhere to these core planning controls when executing design or milestone increments:

## 1. Phase 0: Planning First
* Before writing any code, creating any files, or editing specifications, you MUST draft an `implementation_plan.md` (using `write_to_file` with `IsArtifact=true` and `ArtifactType='implementation_plan'`) and present it for user review. No edits are permitted until this plan is approved.

## 2. The 3-Tier Feature Capsule Pipeline
Every feature increment must live in its own encapsulated folder inside `docs/sdd/<epic-slug>/<feature-slug>/` containing three isolated files drafted in this exact chronological sequence:
1. **Functional Specification (`SPEC.md`)**: Plain-English objective, step-by-step narrative User Journeys, User Requirements, and Success Criteria. Technical database names, API endpoints, and programming language code blocks are strictly banned.
2. **Technical Design (`DESIGN.md`)**: Translates requirements into detailed database schema markdown tables, API request/response mock payloads, Mermaid.js data-flow diagrams, and a test Verification Strategy. Fenced blocks of production programming code are prohibited.
3. **Actionable Task Checklist (`TASKS.md`)**: Translates technical design contracts and verification steps into a BDD Gherkin task checklist (`Given/When/Then`).

## 3. Executing Controls
* **No Blind Coding**: You are strictly forbidden from writing production code or test suites until both `SPEC.md` and `DESIGN.md` have been fully compiled and approved by the user.
* **Spec Reconciliation Protocol**: Coder agents are forbidden from editing specs or designs directly. Gaps must be drafted in a `spec_change_proposal.md` artifact, presented to the user, and merged by the Architect.
* **Checklist limit**: A single `TASKS.md` must contain **up to 12 tasks**. If it exceeds 12 tasks, compilation is blocked. The Project Manager must split the feature into modular sub-features.
* **Formatting Hook**: Run `mdformat` immediately after any markdown file modification to enforce indentation and bullet consistency.
