# SDD Harness: 8-Step Pipeline Runbook

This runbook guides you through using the Spec-Driven Development (SDD) process harness. The pipeline is driven by a highly specialized team of 4 AI agents executing 8 distinct steps, ensuring that business objective alignment and code verification gates are satisfied before any production code is written or merged.

---

## 1. Core Architecture

### A. Rules vs. Playbooks (Skills)
*   **Rules (`rules/`)**: Universal, static guardrails that are **always active** (e.g. sandbox write-path boundaries, TDD loops, tool execution bans).
*   **Playbooks (`skills/`)**: Dynamic, on-demand step-by-step procedures (e.g. conducting requirements discovery interviews). They are loaded only when the corresponding phase is active.

### B. User Interface Alignment (Agent Profiles)
*   **Slash Commands** (e.g. `/start-feature`) execute the playbook play.
*   **Agent Profiles** (e.g. `sdd-implementor.json`) configure the physical container constraints (tool access, write paths).
*   **CRITICAL STEP**: Before executing any slash command in your chat session, **you must select the corresponding Agent Profile in your chat panel settings**. This ensures that the platform physically blocks the agent if it attempts to violate its write-path boundaries.

---

## 2. The 8-Step SDD Sequence

Follow the steps below in sequence to plan, design, implement, and verify your features:

### Step 0: Startup Discovery
*   **Agent Profile**: Any
*   **Command**: (None, executed automatically on startup)
*   **Action**: Start a new chat thread. The agent automatically executes the programmatic status report script (`status_report.sh`).
*   **Result**: Displays a markdown table of your specification status and recommends the next step.

### Step 1: Project Blueprinting
*   **Agent Profile**: `sdd-product-manager`
*   **Command**: `/blueprint`
*   **Objective**: Compiles high-level project vision, tech stacks, and Epic breakdowns into `docs/PROJECT.md` and scaffolds empty feature subfolders.
*   **Modes**:
    *   *Guided (Default)*: PM conducts a one-question-at-a-time vision interview.
    *   *Auto*: `/blueprint --auto` ➔ Generates the blueprint directly based on a brief description.

### Step 2: Codebase Grounding
*   **Agent Profile**: `sdd-engineering-manager`
*   **Command**: `/code-analysis`
*   **Objective**: Scans the existing codebase for architectures and utility conventions, writing `docs/sdd/CODE_ANALYSIS.md`. (Skip this step for greenfield setups).
*   **Modes**:
    *   *Guided*: EM asks what folders to scan, proposes findings.
    *   *Auto*: `/code-analysis --auto` ➔ Performs scans and writes the grounding report directly.

### Step 3: Feature Specification
*   **Agent Profile**: `sdd-product-manager`
*   **Command**: `/spec-feature <epic_slug>/<feature_slug>`
*   **Objective**: Conducts functional requirements discovery and compiles `SPEC.md` under the feature capsule folder.
*   **Modes**:
    *   *Guided*: PM conducts user stories, requirements (`req-N`), and acceptance criteria discovery.
    *   *Auto*: `/spec-feature <feature_slug> --auto` ➔ Generates functional specs autonomously.

### Step 4: Technical Design
*   **Agent Profile**: `sdd-engineering-manager`
*   **Command**: `/design-feature <epic_slug>/<feature_slug>`
*   **Objective**: Designs API contracts, models, schemas, and verification strategies, writing `DESIGN.md`. Maps contracts directly back to spec requirement IDs (`req-N`).
*   **Modes**:
    *   *Guided*: EM conducts a technical architecture interview.
    *   *Auto*: `/design-feature <feature_slug> --auto` ➔ Autonomously drafts design specifications.

### Step 5: Execution Planning
*   **Agent Profile**: `sdd-technical-lead`
*   **Command**: `/task-generator <epic_slug>/<feature_slug>`
*   **Objective**: Decomposes specs and designs into a sequential, actionable BDD Gherkin task checklist (`TASKS.md`) capped at 12 cards.
*   **Modes**:
    *   *Guided*: TL asks about task granularity preferences.
    *   *Auto*: `/task-generator <feature_slug> --auto` ➔ Decomposes tasks autonomously.

### Step 6: Specification Audit (EM Gate)
*   **Agent Profile**: `sdd-engineering-manager`
*   **Command**: `/audit-tasks <epic_slug>/<feature_slug>`
*   **Objective**: EM audits the BDD task checklist against the technical design.
*   **Result**: EM signs off the checklist by writing the `EM_AUDIT: APPROVED` header block to `TASKS.md`. **This sign-off is required to open the sandbox.**
*   **Modes**:
    *   *Auto*: `/audit-tasks <feature_slug> --auto` ➔ Autonomously checks and signs off the checklist.

### Step 7: Sandboxed Execution (Coder)
1.  **Open Sandbox**: Load the `sdd-implementor` profile in the parent repository and run `/open-feature <epic_slug>/<feature_slug>`. The Coder commits specs, runs `/worktree create`, and registers the sandbox in the Hub.
2.  **TDD Loop**: Switch to the newly provisioned sandbox Project in your Hub sidebar. Load the `sdd-implementor` profile, run `/start-feature`, and execute Red-Green-Refactor loops task by task. The Coder must output physical passing test logs in chat before checking off boxes in `TASKS.md`.
3.  **Close Sandbox**: Switch back to the parent project in Jetski Hub. Load the `sdd-implementor` profile and run `/close-feature <epic_slug>/<feature_slug>` to fast-forward merge the code and dismantle the worktree directory.

### Step 8: Code Verification
*   **Agent Profile**: `sdd-technical-lead`
*   **Command**: `/verify-feature <epic_slug>/<feature_slug>`
*   **Objective**: TL runs the test suite, cross-checks functional requirements, and compiles `VERIFICATION_REPORT.md` (marked `VERIFIED` or `REMEDIATION_REQUIRED`).

### Step 9: Retrospective & Learning Loop
*   **Agent Profile**: `sdd-engineering-manager` or `sdd-product-manager`
*   **Command**: `/retrospective <epic_slug>/<feature_slug>`
*   **Objective**: EM/PM scans execution checkpoint logs, Git history logs, and test failures. Appends actionable learning points to the global `docs/LESSONS_LEARNED.md` registry to guide future runs.
