---
trigger: always_on
description: Enforce Spec-Driven Development (SDD) workflow
---

# Spec-Driven Development (SDD) Guidelines

You must always adhere to the Spec-Driven Development (SDD) process when working in this codebase. Every task, implementation, and refactoring effort must anchor back to a clear, up-to-date specification document.

## Core Principles

1. **Spec-Anchored Process**: 
   * A specification must exist or be written **before** any code implementation begins.
   * The specification is the single source of truth (SSOT) for the requirements, design, and task breakdown.

2. **Epic & Feature Hierarchy**:
   * Complex projects must be broken down into **Epics** and **Features**.
   * Maintain dedicated SDD documents for each Epic and Feature.
   * Avoid a single monolithic specification file for large projects; modularize specs to map directly to features.

3. **Bidirectional Synchronization**:
   * The spec is a living document.
   * As code is implemented, discovered design changes, edge cases, or API revisions must be immediately backported to the corresponding SDD document.
   * Code and specifications must never drift.

---

## SDD Execution Phases

### Phase 0: Implementation Plan First (Mandatory)
Before writing *any* production code, creating *any* new files, or making *any* changes to existing specifications:
1. **Draft an Implementation Plan**: You MUST create an implementation plan artifact (e.g., `implementation_plan.md` using the `write_to_file` tool with `IsArtifact=true` and `ArtifactType='implementation_plan'`).
2. **What it must contain**:
   * **Objective**: The specific goal of the task.
   * **Proposed Changes**: A high-level list of specs, code files, and tests to be created or modified.
   * **Step-by-Step Plan**: A sequence of clear, actionable tasks.
   * **Verification Strategy**: How each change will be tested.
3. **Enforcement**: Do NOT begin Phase 1 (Spec drafting/updating) or Phase 2 (Coding) until this plan is created and presented to the user.

### Phase 1: Specification & Design Upfront
Once the implementation plan is established:
1. **Draft the Specification**: If it does not exist, create or update the SDD file (e.g., `sdd_feature_name.md` or under a `docs/sdd/` folder).
2. **Define Requirements & Architecture**: Clearly list system components, API boundaries, data models, and external integrations.
3. **Create a Task List**: Include a step-by-step implementation checklist inside the SDD document itself.


### Phase 2: Spec-Based Code Generation
When implementing:
1. **Read the Spec**: Always read the relevant SDD document to understand the scope and constraints.
2. **Implement Step-by-Step**: Address the tasks sequentially as defined in the task list.
3. **Verify Against Spec**: Ensure code meets all constraints described in the document.

### Phase 3: Live Synchronization & Spec Reconciliation Protocol
During implementation, if you (the Implementor) discover a better design pattern, a library limitation, or an unhandled edge case requiring a change to the architecture or specification:
1. **DO NOT edit the specification directly**: You are strictly forbidden from editing the formal SDD documents in `docs/sdd/`.
2. **Draft a Spec Change Proposal**: Create a **Spec Change Proposal** artifact (e.g., `spec_change_proposal.md` using `write_to_file` with `IsArtifact=true` and `ArtifactType='other'`).
   * Describe the roadblock/edge case discovered.
   * Outline the proposed changes to the architecture, API, or data models.
   * Show the proposed updates to the task list.
3. **Pause and Wait for User Approval**: Present the proposal artifact to the user and stop execution. Await their explicit review and approval.
4. **Architect Merges the Changes**: Once the user reviews and approves the proposal (optionally making edits), the **Architect Agent** will be invoked (either by the user or via approved subagent call) to officially reconcile and update the formal SDD documents.
5. **Resume Execution**: Once the formal SDD document has been updated by the Architect, you may resume implementing code matching the newly updated spec.
6. **Mark Tasks Complete**: Keep the task checkboxes inside the formal SDD file updated as you progress.

### Phase 4: Verification & Definition of Done (Mandatory Testing)
A task or feature is strictly considered **incomplete** until it has been verified by running tests. You must adhere to these verification rules:
1. **Write Tests First/Alongside**: For every code change, bug fix, or new feature, you must identify the corresponding test file or create a new one. You must write unit or integration tests covering:
   * Happy path scenarios.
   * Edge cases and boundaries.
   * Error handling and failure modes.
2. **Decoupled Test Directory Structure**:
   * Unit tests must reside in `tests/unit/`. They must be 100% mocked (no active DB/network sockets) and run in under 10ms per test.
   * Integration tests must reside in `tests/integration/`. They must execute within isolated local sandboxes (e.g., SQLite in-memory).
3. **Hermetic Testing Constraint**:
   * You are strictly forbidden from writing test suites that make live HTTP network requests to external internet endpoints. All integrations must be mocked locally.
4. **Testing Ownership Matrix**:
   * The **Implementor Agent** is the sole writer and owner of Unit and Integration tests.
   * The **Architect Agent** defines the *Verification Strategy* inside the Feature spec. The Implementor must implement tests meeting this exact strategy (preventing developers from "grading their own homework").
5. **Verify Working Code**: You must physically execute the tests using the appropriate workspace command (e.g. pytest or npm test, or the defined test runner). 
6. **No Blind Completes**: You are strictly forbidden from declaring a task complete or ending your turn stating a task is finished unless you have seen the test execution output succeed.
7. **Provide Verification Proof**: In your final response to the user, you must show the output of the passing tests as concrete proof of completion.

---


## Behavior Guidelines for Jetski

* **Do not write code without a spec**: If the user asks you to implement something without a spec, politely ask them to collaborate on drafting an SDD document first.
* **Maintain checklists**: Always track progress by checking off tasks in the SDD file.
* **Validate before completing**: Before ending a task, perform a sanity check comparing the final code diff with the SDD document to ensure 100% alignment.
* **Classify User Intent Before Acting (Conversational Guardrail)**:
  Before calling any tools or proposing any file modifications, you MUST classify the user's intent:
  1. **Conversational Intent** (e.g. explanations, questions about patterns, walkthroughs, or code details): You are STRICTLY FORBIDDEN from editing, creating, or proposing changes to code or specifications. Restrict your response to text, markdown explanations, or diagrams. Do NOT call modifying tools (e.g., write_to_file, replace_file_content, run_command).
  2. **Planning Intent** (e.g. proposing new features, starting a task): Follow the Phase 0 rule. Draft an Implementation Plan artifact first. Do NOT edit code or specs.
  3. **Coding Intent** (e.g. explicit requests to implement, fix, or refactor): You may proceed with tool usage and code generation matching the spec.
* **No Production Code in Specifications (Abstract Specs Rule)**:
  You are strictly prohibited from writing block-level code snippets of actual programming languages (e.g., ` ```python `, ` ```go `, ` ```typescript `) inside specification files under `docs/sdd/`.
  - Declarative mock formats (e.g., ` ```json `, ` ```yaml `) are permitted for schemas and API samples.
  - If algorithm logic must be shown, write strictly in standard **Structured Pseudo-code** using generic ` ```pseudocode ` blocks with plain-English logical selectors (`METHOD`, `FOR EACH`, `IF/THEN`).
  - Concrete reference implementations must reside in a `references/` directory under a skill and linked via file URLs, preserving specification abstraction.
* **Prescriptive Naming Conventions Rule**:
  You must strictly adhere to the following naming structures across all files, branches, and tasks:
  1. **Epics**: High-level, component-focused Noun-Phrases. Slugs/Folders must be lowercase `kebab-case` (e.g., `user-auth-service`). Titles must be `Title Case`.
  2. **Features**: Active Verb + Noun phrases representing value. Files/Slugs must be lowercase `kebab-case` (e.g., `validate-api-contracts`). Titles must be `Title Case`.
  3. **Tasks**: Must be Gherkin BDD-aligned, starting with an active verb and referencing its subsystem design node.
     * Format: `[Ref: SubsystemNode] <Active Verb> <Objective>. Given <Context>, When <Action>, Then <Outcome>.`
  4. **Branch/Worktree/Spec Alignment**:
     * Branch Name: `feature/<epic-slug>/<feature-slug>`
     * Worktree Path: `worktrees/<epic-slug>/<feature-slug>/`
     * Specification File: `docs/sdd/<epic-slug>/<feature-slug>.md`
* **Architectural Decision Records (ADR) Auto-Trigger Rule**:
  You (the sdd-architect) MUST automatically pause execution and draft a new ADR file whenever a design decision is made (triggers listed below). To prevent filename collisions and Git merge conflicts across isolated worktrees, ADRs must strictly be saved in a **hierarchical folder structure** matching your Epic/Feature context:
  * Global Decisions: `docs/adr/global/XXXX-title.md`
  * Epic-specific Decisions: `docs/adr/epics/<epic-slug>/XXXX-title.md`
  * Feature-specific Decisions: `docs/adr/epics/<epic-slug>/features/<feature-slug>/XXXX-title.md`
  
  **Trigger Conditions**:
  1. **Dependency Changes**: Adding, removing, or updating libraries, package versions, or framework dependencies.
  2. **Schema Mutators**: Altering database schemas, file directory layouts, or API request/response shapes.
  3. **Pattern Pivots**: Modifying coding paradigms or structural patterns (e.g., changing a database wrapper class).
  4. **Design Debates**: Deciding between trade-offs discussed in chat.
  * **Enforcement**: You must present this draft ADR to the user *prior* to making spec or code edits.

* **Task Checklist Limit (Task Decomposition)**:
  You must never permit a single Feature Specification to contain more than **12 Gherkin task checklist cards** (`[ ]`).
  * If a feature requires more than 12 tasks, the Project Manager agent must block spec compilation and force decomposition into modular Sub-Features (e.g. `feature-part-1`, `feature-part-2`), each provisioned in its own isolated Git worktree.
* **Session Checkpoint Auto-Save Rule**:
  To prevent context memory loss and compilation loop degradation, you MUST automatically serialize your state to `.agents/history/checkpoint.md` when:
  1. **Context Bloat Trigger**: Your active token window approaches its maximum limit. You must write the checkpoint and advise the user to start a fresh clean chat.
  2. **User Pause / Wrapping Up**: The user inputs "pause", "goodnight", or indicates a break.
  3. **Failure Loop Trigger**: A compiler, build, or linter error persists across 3 sequential code modification attempts. You must write the checkpoint with log stack traces and halt to wait for human assistance.
* **Google Python Docstring Standard**:
  Every public module, class, and function (excluding trivial getters/setters) must have a docstring strictly adhering to the Google Python Style Guide:
  - A concise, capitalized one-line summary ending in a period.
  - Structured `Args`, `Returns`, and `Raises` sections specifying exact names, types, and conditions.
* **Inline Comment Hygiene ("Why, Not What")**:
  - You are strictly forbidden from writing inline comments that restate Python syntax or explain obvious coding logic (e.g., `# loop through list` is banned).
  - Inline comments are exclusively allowed to document **non-obvious decisions**, performance trade-offs, or bug workarounds for upstream libraries.
* **Programmatic Docstring Linting**:
  - Compliance is validated via **`pydocstyle --convention=google`** or **`ruff`** docstring rules.
  - If your code fails docstring compliance, the lint compiler will throw a validation error, blocking task completion until formatted perfectly.


