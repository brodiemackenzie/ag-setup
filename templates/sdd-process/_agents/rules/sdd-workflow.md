---
trigger: always_on
description: Enforce strict Spec-Driven Development (SDD) 3-Tier Feature Capsule pipeline.
---

# Core Spec-Driven Development (SDD) Rules of Engagement

You must strictly adhere to these rules when working in this workspace. Every single functional increase, technical design choice, or coding iteration must map directly to the three-tier Feature Capsule pipeline.

---

## 🏛️ The 3-Tier Feature Capsule Pipeline

Every feature increment must live in its own encapsulated folder inside `docs/sdd/<epic-slug>/<feature-slug>/` containing three isolated files. Development must follow this exact sequential order:

```
Interactive Q&A Discovery
          │
          ▼
   1. SPEC.md (What & Why)
          │
          ▼
   2. DESIGN.md (How)
          │
          ▼
   3. TASKS.md (Execution)
          │
          ▼
   4. Coding & TDD
```

### 1. Functional Specification (`SPEC.md`)
* **Objective**: Defines the functional user experience, requirements, and success boundaries in plain English.
* **Rules**:
  * Must contain **User Journeys** (narrative walkthroughs of user journeys) and **User Requirements** (explicit functional rules).
  * Must contain **Success Criteria** (exact user verification definitions of done).
  * **BANNED**: All database schemas, REST endpoint names, code-level parameters, and specific programming language code blocks are strictly prohibited in `SPEC.md`.

### 2. Technical Design (`DESIGN.md`)
* **Objective**: Establishes the software engineering architecture, data maps, and testing strategy.
* **Rules**:
  * Must translate functional journeys in `SPEC.md` into exact technical details: database schemas (e.g. SQLite/Spanner tables), REST API payload parameters, class structures, and data-flow **Mermaid.js** diagrams.
  * Must define the **Verification Strategy**: Outlines unit and integration testing scopes, detailing exactly *what* test scenarios the coder must implement to prove requirements.
  * **BANNED**: block-level code snippets of production programming languages (e.g. Python, TS) are forbidden. Use declarative formats (`json`, `yaml`) or language-agnostic ````pseudocode ```` blocks only.

### 3. Actionable Task Checklist (`TASKS.md`)
* **Objective**: Details the execution steps for implementation.
* **Rules**:
  * Must translate the Technical Design and Verification Strategy into standard BDD/Gherkin checklist tasks (`Given/When/Then`).
  * Must contain **up to 12 task checkboxes** (`[ ]`). If a feature's scope exceeds 12 tasks, execution is blocked. The PM must decompose the feature into modular sub-features (e.g., `part-1`, `part-2`), each in its own isolated branch and worktree.

---

## 🛡️ SDD Execution Controls

### 1. Phase 0: Planning First
* Before writing any code, creating any new files, or making changes to specifications, you MUST draft an `implementation_plan.md` (using the `write_to_file` tool with `IsArtifact=true` and `ArtifactType='implementation_plan'`) and present it for user review. No edits are permitted until this plan is approved.

### 2. No Blind Coding
* **You are strictly forbidden from writing production code or test suites until both `SPEC.md` and `DESIGN.md` have been fully compiled and approved by the user.**

### 3. Spec Reconciliation Protocol (Phase 3)
* The Implementor agent is strictly forbidden from editing `SPEC.md` or `DESIGN.md` directly during coding. 
* If a library boundary, edge case, or logical gap is discovered:
  1. Draft a `spec_change_proposal.md` describing the gap and proposed updates.
  2. Halt execution and present the proposal to the user.
  3. Once approved, the Architect agent merges changes into `SPEC.md`/`DESIGN.md`. Only then can coding resume.

### 4. Workspace & Environment Sandboxing
* **Strict Isolation**: The Architect and Implementor agents are strictly prohibited from executing inside or writing to the top-level repository directory. They must operate exclusively inside their assigned Git worktree subdirectory (`worktrees/<epic-slug>/<feature-slug>/`).
* **Top-Level Protection**: Any file creation, modification, or execution targeting files outside the active worktree directory (e.g., attempting to write via relative path traversal like `../../src/*` or to the top-level folders) is strictly forbidden and will be flagged as a security/permission violation.
* **Project Manager Boundary**: The Project Manager agent is the only agent permitted to operate in the top-level workspace to run branch automation and coordinate worktree setups.

---

## 🧪 Testing & Docstring Standards

### 1. Strict TDD red-Green-Refactor Loops
* Coder must strictly follow the Test-Driven Development (TDD) playbook:
  1. **RED**: Write a minimal failing test first (under `tests/unit/` or `tests/integration/`). Execute test suite and verify failure.
  2. **GREEN**: Implement minimal production code to pass. Verify success.
  3. **REFACTOR**: Clean code structures and confirm tests remain green.
* **No Blind Completes**: You are strictly forbidden from marking a task checkbox `[x]` complete or ending your turn declaring a task finished without physically executing tests and showing the successful passing logs in your transcript.

### 2. Hermetic Test Isolation
* All test suites must be hermetic. **You are strictly forbidden from writing tests that open network sockets or make HTTP calls to external internet endpoints.** All external APIs and third-party integrations must be fully mocked.
* Unit tests (`tests/unit/`) must run in under 10ms and rely 100% on mocks.
* Integration tests (`tests/integration/`) must run against isolated local database sandboxes (e.g. SQLite in-memory).

### 3. Google docstring Compliance
* Every public module, class, and method must contain a strict Google Python Style docstring:
  * Concise, capitalized one-line summary ending in a period.
  * Explicit `Args`, `Returns`, and `Raises` sections detailing parameters, output shapes, and exception conditions.
* Messy PEP 257 formatting errors or undocumented methods will fail the build gate and block task completion.
* **Inline Comment Hygiene**: Banish obvious syntax restatements (e.g. `# loop through list`). Inline comments are permitted exclusively to explain *non-obvious decisions*, performance trade-offs, or third-party workarounds.

---

## 🧼 Document Hygiene & Mutation

* **Surgical Anchoring**: Edits to specs or design files must be anchored surgically to unique headers. Appending updates to the end of documents is strictly prohibited.
* **List sequence**: Modified ordered lists must be re-sequenced programmatically.
* **TOC Sync**: Keep Table of Contents fully synchronized.
* **Linter Hook**: The PM agent automatically runs `mdformat` after every document modification to ensure clean alignments and bullet consistency.
