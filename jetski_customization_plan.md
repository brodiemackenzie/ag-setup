# Jetski Customization & Workflow Automation Plan

This document specifies the architecture, rules, and tools designed to customize Jetski (Antigravity) for a strict **Spec-Driven Development (SDD)** and **isolated Git Worktree** workflow. 

It enforces an absolute separation of concerns by establishing a strict **Specification (What/Why) ➔ Design (How) ➔ Tasks (Execution)** pipeline, encapsulating every feature in its own directory containing isolated `SPEC.md`, `DESIGN.md`, and `TASKS.md` documents.

To accommodate strict global directory access controls and ensure maximum developer flexibility, all templates are developed **locally in the workspace** and bound globally to the environment using a simple symlink configuration.

---

## 🏗️ System Architecture Overview

The custom architecture operates on two levels: the **Global Layer** (system-wide installers) and the **Local Layer** (project-specific runtimes).

```mermaid
graph TD
    subgraph Global [Global Layer (~/.gemini/)]
        A[Global project-bootstrap Skill] -->|Executes bootstrap.sh| B[Target Workspace Folder]
        SL[~/.gemini/templates/] -->|Symlinked to local workspace| C
    end
    
    subgraph Local [Local Layer (~/projects/my-app/)]
        B -->|Contains .agents/| D[rules/sdd-workflow.md]
        B -->|Spawns| PM[sdd-project-manager agent]
        B -->|Spawns| ARCH[sdd-architect agent]
        B -->|Spawns| IMPL[sdd-implementor agent]
        
        PM -->|Executes manage_worktree.sh| WT[(Feature Git Worktrees)]
        WT -->|Symlinks Node / Inherits Python| B
    end
    
    subgraph Development [Development Layer (~/projects/ag-setup/)]
        C[ag-setup/templates/] -->|Version-controlled locally| Git[(GitHub Repository)]
    end
```

---

## 📂 Folder & File Structure

```
ag-setup/                                 # Local Workspace Root (Git Repository)
├── jetski_customization_plan.md
├── templates/                            # Master Templates Directory (Pushed to GitHub)
│   ├── sdd-process/                      # Spec-Driven Development Process Template
│   │   └── _agents/                      # The SDD Agent/Skill Capsule
│   │       ├── rules/
│   │       │   └── sdd-workflow.md       # The Core SDD Rules (always_on)
│   │       ├── skills/
│   │       │   ├── worktree-manager/     # Git worktree management skill
│   │       │   │   ├── SKILL.md
│   │       │   │   └── scripts/
│   │       │   │       └── manage_worktree.sh
│   │       │   ├── sdd-proposal-drafter/ # Interview & Proposal playbook (Vision Essence)
│   │       │   │   └── SKILL.md
│   │       │   ├── sdd-spec-writer/      # Interactive Spec Writer (Q&A Functional Journeys)
│   │       │   │   └── SKILL.md
│   │       │   ├── sdd-design-architect/ # Engineering blueprints (Schemas, APIs, Mermaid)
│   │       │   │   └── SKILL.md
│   │       │   ├── sdd-task-generator/   # BDD Gherkin task compiler
│   │       │   │   └── SKILL.md
│   │       │   ├── document-editor/      # Surgical markdown editor playbook
│   │       │   │   └── SKILL.md
│   │       │   ├── tdd-flow/             # Strict Red-Green-Refactor playbook
│   │       │   │   └── SKILL.md
│   │       │   ├── sdd-retrospective/    # Post-merge learnings harvester
│   │       │   │   └── SKILL.md
│   │       │   ├── session-checkpoint/   # State serialization & recovery skill
│   │       │   │   └── SKILL.md
│   │       │   └── docs-compiler/        # Portable offline static wiki portal
│   │       │       └── SKILL.md
│   │       └── agents/
│   │           ├── sdd-architect/        # Pure specification writer (No shell)
│   │           ├── sdd-implementor/      # Rigorous developer & tester (Shell active)
│   │           └── sdd-project-manager/  # Branch organizer & workspace cleaner
│   └── vibe-coding/                      # Rapid Prototyping Vibe-Coding Template (Example)
│       └── _agents/                      # Custom Vibe-Coding Rules & Agent Capsules
└── global/
    └── skills/
        └── project-bootstrap/            # Global Scaffolder Skill (Stored in user home directory)
            ├── README.md
            └── scripts/
                └── bootstrap.sh          # Global project bootstrapper
```

---

## 📜 Part 1: Implemented Local Customizations (Completed)

The following configurations are fully functional inside the workspace `.agents/` folder:

### 1. SDD Core Rules (`rules/`)
We decompose core constraints into three focused modular rule files:
* **`sdd-pipeline.md`**: Enforces Phase 0 planning-first controls, the Spec ➔ Design ➔ Tasks capsule pipeline sequence, and the strict 12-task limit.
* **`sdd-sandboxing.md`**: Confines Architect and Implementor to active worktree sandboxes, denying top-level workspace modifications.
* **`sdd-tdd-standards.md`**: Enforces strict TDD loops (no blind completes), hermetic mocking limits, and Google docstring hygiene.

### 2. Custom Agents (`agents/`)
* **`sdd-architect`**: Equipped with search and write tools limited strictly to `docs/sdd/`. Denied shell command execution.
* **`sdd-implementor`**: Equipped with code-editing and bash command tools (`run_command` to run test runners), but strictly denied write access to `docs/sdd/`.
* **`sdd-project-manager`**: Governs Git branch hygiene and handles automated worktree and env bindings using local scripts.

### 3. Worktree Manager Skill (`skills/worktree-manager/`)
Hosts the **`manage_worktree.sh`** script, supporting:
* **`prototype <epic> <feature>`**: Provisions an isolated worktree, creates the DEDICATED feature folder under `docs/sdd/<epic>/<feature>/`, and scaffolds blank templates for `SPEC.md`, `DESIGN.md`, and `TASKS.md`.
* **`link-env <epic> <feature>`**: Auto-detects Node.js (symlinks `node_modules`), Python (inherits main `.venv` via `--system-site-packages`), or Rust (symlinks target cache), and binds environments instantly.
* **`close-feature <epic> <feature>`**: Merges the branch, reconciles dependencies back to the main environment, and safely deletes the worktree folder.

---

## 🔮 Part 2: Global Scaffolding Blueprints (To Be Implemented)

The following blueprints define the global automation layer that will be installed globally in the user's home directory:

### 1. Global Bootstrapper (`~/.gemini/config/skills/project-bootstrap/`)
A unified installer designed to initialize standard workspaces either via interactive conversational chat or CLI.
* **Trigger Command**: `/bootstrap` in chat, or run `bootstrap.sh` manually in terminal.
* **Conversational Interview Mode**:
  1. The agent detects `/bootstrap` or `start project` intent.
  2. Interactively collects the project name, GitHub remote SSH URL, and scaffolding framework choice (one question at a time).
  3. Automatically executes the CLI script under the hood using `run_command`.
* **Execution Steps**:
  1. **Directory Provisioning**: Creates the directory `~/projects/<project_name>` and initializes Git.
  2. **Scaffolding**: If `--scaffold` is provided, runs standard generators (e.g. `create-next-app`).
  3. **Nested Git Safeguard**: Runs a recursive scan to find and delete any nested `.git` folders generated by frameworks.
  4. **Git Remote Binds**: Removes template origins and binds `git remote add origin <github_repo_url>`.
  5. **VCS-Safe Config Copying**: Copies the specified process agent templates using `rsync` to exclude internal git tracking metadata:
     ```bash
     rsync -av --exclude='.git' "~/.gemini/config/templates/<process_slug>/_agents/" "~/projects/<project_name>/.agents/"
     ```
  6. **SDD Interview Trigger**: Automatically launches the initial speculative interview to draft the high-level project proposal.

### 2. Version-Controlled Configuration Repository
* **Mechanism**: All templates are version-controlled in the project's root `templates/` directory and pushed to a private GitHub repository (`brodiem/ag-setup`).
* **Installation Flow (Symlink Strategy)**:
  To install templates globally while allowing the agent to edit them locally in the workspace:
  1. Create the global configuration directory in your home folder:
     ```bash
     mkdir -p ~/.gemini/config/
     ```
  2. Symlink the local templates and workflows folders directly to the global directories:
     ```bash
     ln -s ~/projects/ag-setup/templates/ ~/.gemini/config/templates
     ln -s ~/projects/ag-setup/workflows/ ~/.gemini/config/global_workflows
     ```
  *This guarantees that any edits the agent makes locally inside the `ag-setup` workspace are instantly available globally in `~/.gemini/config/templates/` without manual cloning or pulling.*

---

## 🎙️ Part 3: Encapsulated SDD Feature Capsule Pipeline (To Be Implemented)

To guarantee absolute architectural consistency, the design process is broken down into a sequential, multi-stage pipeline where each step is powered by a **highly specialized custom skill**.

### The 3-Tier Feature Lifecycle:
`Interactive Interview ➔ 1. Proposal (Essence) ➔ 2. Spec (Journeys) ➔ 3. Design (Architecture) ➔ 4. Tasks (BDD Cards) ➔ 5. Code & Test`

```
docs/
├── proposals/
│   └── project_proposal.md                   # High-Level Project Vision
└── sdd/
    └── <epic-slug>/
        ├── adr/                              # Epic-specific architectural decisions
        └── <feature-slug>/                   # THE ENCAPSULATED FEATURE CAPSULE
            ├── SPEC.md                       # Functional User Journeys
            ├── DESIGN.md                     # Technical blueprints
            ├── TASKS.md                      # Actionable Gherkin checklists
            └── adr/                          # Feature-specific decisions
```

---

### 1. The Proposal Drafter Skill (`skills/sdd-proposal-drafter/`)
Governs the transition from **Interview ➔ Proposal**.
* **Interview Playbook**: The agent conducts a structured, conversational interview about project goals and tech stacks.
* **Proposal Template**: Generates a high-level, brief `docs/proposals/<project_name>_proposal.md` outlining ONLY:
  * *Project Objective & Essence*
  * *Architectural Pillars & Target Tech Stack*
  * *Epic & Feature Map Inventory*
* **Banned Content**: Database schemas, REST parameters, and detailed user journeys.

---

### 2. The Spec Writer Skill (`skills/sdd-spec-writer/`)
Governs the transition from **Proposal ➔ Functional Specification** for an individual feature capsule.
* **Interactive Spec Q&A Playbook**: Before writing the specification, the agent asks you **3-5 highly targeted questions** about the feature's target experience (e.g. specific error handling, navigation flows, out-of-scope details).
* **Spec Template**: Writes `docs/sdd/<epic-slug>/<feature-slug>/SPEC.md` containing:
  * *Objective*: Plain-English feature goal.
  * *User Journeys*: Step-by-step narrative walkthroughs of the user experience.
  * *User Requirements*: Explicit list of functional rules.
  * *Success Criteria*: Functional definitions of done.
* **Banned Content**: Zero technical design details (no database names, no REST endpoints, no programming code blocks).

---

### 3. The Design Architect Skill (`skills/sdd-design-architect/`)
Governs the transition from **Specification ➔ Technical Design**.
* **Design Blueprint Compiler**: Translates the plain-English journeys in `SPEC.md` into exact software engineering contracts.
* **Design Template**: Writes `docs/sdd/<epic-slug>/<feature-slug>/DESIGN.md` containing:
  * *Database Schemas & API Contracts*: Formatted markdown tables with explicit data types.
  * *Visual Architecture*: Mermaid.js diagrams (flowcharts, state diagrams, entity maps).
  * *Verification Strategy*: Specific test cases (unit and integration test scopes) mapped to each requirement.
* **ADR Auto-Trigger**: If dependency, database schema, or design pattern shifts are introduced, automatically drafts a modular ADR in `adr/` *prior* to finalizing the design.

---

### 4. The Task Generator Skill (`skills/sdd-task-generator/`)
Governs the transition from **Technical Design ➔ Task Lists**.
* **BDD Task Compiler**: Translates technical schemas and verification flows into standard BDD Gherkin checklists (`[ ] Given/When/Then`).
* **Tasks Template**: Writes `docs/sdd/<epic-slug>/<feature-slug>/TASKS.md` containing a clean, simple checklist of **up to 12 task checkboxes**, facilitating fast development loops and immediate progress monitoring.

---

## 🧼 Part 4: Document Hygiene & Automated Formatting (To Be Implemented)

Markdown files are treated with the same strictness as source code, using physical mutation playbooks and automated formatters to prevent formatting drift.

### 1. Strict Document Mutation Rules (Rules Layer)
The agent must adhere to these strict structural layout rules inside `.agents/rules/sdd-workflow.md`:
* **Strict Header Anchoring**: Updates or tasks must be written directly under their respective headings. Inserting random updates at the end of files is strictly prohibited.
* **List Hygiene**:
  * **Sequential Re-numbering**: If an ordered list item is modified, the agent must renumber and update all subsequent items in that block.
  * **Bullet Standardization**: Consistent bullet markers (`-` or `*`) must be maintained throughout.
* **TOC Sync**: Table of Contents must instantly mirror heading modifications.

### 2. The "Anchor-and-Verify" Playbook (`skills/document-editor/`)
A specialized markdown editing skill that teaches the agent to read outlines, locate exact line ranges surgically, and apply replacements without corrupting surrounding formats.

### 3. Automated Markdown Formatting (Tool Layer)
* **Tooling**: Integrated use of **`mdformat`** (opinionated Markdown formatter) inside the local environment.
* **Automation Hook**: The `sdd-project-manager` runs `mdformat <path_to_file>` immediately after *every* specification, design, or task file modification, correcting misaligned tables, broken indentation, and inconsistent list bullets.

---

## 🧱 Part 5: Abstract Specification & Pseudo-code Guidelines (To Be Implemented)

To protect specifications from codebase bloating, specifications are strictly separated from production coding languages.

### 1. Abstract Code Constraints (Rules Layer)
* **Forbid Production Code Blocks in Specs**: Block-level code snippets of actual programming languages (e.g., ` ```python `, ` ```typescript `) are strictly forbidden in `SPEC.md` or `DESIGN.md` documents under the `docs/sdd/` folder.
* **Declarative Payloads Only**: Static, declarative mock blocks (such as ` ```json ` or ` ```yaml `) are permitted for schemas and API sample payloads.
* **Standardized Structured Pseudo-code**: If logic must be shown, the agent is strictly required to write in a standard, language-agnostic ` ```pseudocode ` format using generic logical selectors (`METHOD`, `FOR EACH`, `IF/THEN/ELSE`).

### 2. VCS Reference Separation Pattern
If a concrete implementation script or coding mock is absolutely necessary:
* **Location**: Saved under the local skill's reference directory (e.g. `.agents/skills/my-skill/references/example.py`).
* **Linking**: The design/spec file links to it using an absolute file path (`[example.py](file:///.agents/skills/my-skill/references/example.py)`), preserving document abstraction.

---

## 🏷️ Part 6: Prescriptive Naming Conventions (To Be Implemented)

Consistent naming boundaries are enforced across branches, folders, and checklist tasks to guarantee complete traceability.

### 1. Epic Naming Conventions (High-Level Subsystems)
* **Rule**: Clear, high-level, domain-focused Noun-Phrases representing whole subsystems.
* **Workspace Slugs / Folders**: Lowercase `kebab-case` (e.g. `backend-agent-service`).
* **Document/Git Titles**: Capitalized `Title Case` (e.g. `Backend Agent Service`).

### 2. Feature Naming Conventions (Actionable Increments)
* **Rule**: Active Present-Tense Verb + Noun phrases stating explicit value delivered.
* **Workspace Slugs / Files**: Lowercase `kebab-case` (e.g. `parse-few-shot-examples`).
* **Document/Git Titles**: Capitalized `Title Case` (e.g. `Parse Few-Shot Examples`).

### 3. Task Naming Conventions (Atomic Deliverables)
* **Rule**: Every task item in `TASKS.md` is Gherkin-aligned, starting with a clear active verb and referencing its design mapping.
* **Format**: `[Ref: SubsystemNode] <Active Verb> <Objective>. Given <Context>, When <Action>, Then <Outcome>.`

### 4. Version Control Alignment
All branch provisioning and worktree directories strictly mirror Epic and Feature slugs:
* **Git Branch Name**: `feature/<epic-slug>/<feature-slug>`
* **Worktree Directory Path**: `worktrees/<epic-slug>/<feature-slug>/`
* **SDD Feature Directory**: `docs/sdd/<epic-slug>/<feature-slug>/`

---

## 🧪 Part 7: Test-Driven Development (TDD) Playbook Skill (To Be Implemented)
The Implementor Agent strictly follows the atomic **Red-Green-Refactor** TDD playbook for every single checkbox task in `TASKS.md`:
1. **Parse Task Contract**: Locate the Gherkin BDD task checkbox in `TASKS.md`.
2. **RED Phase**: Draft a minimal failing test case in `tests/unit/` or `tests/integration/`. Run the test suite and verify a clean failure.
3. **GREEN Phase**: Write only the minimal production logic to pass the test. Run tests and verify clean success.
4. **REFACTOR Phase**: Refactor codebase structure and ensure tests remain green.
5. **Check off Task**: Check off the task `[x]` in `TASKS.md` and proceed to the next task.

---

## 🛡️ Part 8: Testing & Verification Responsibility Principles (To Be Implemented)

Testing structures are cleanly decoupled to prevent slow system integration runs from bottlenecking lightning-fast developer feedback:
* `tests/unit/`: Lightning-fast unit tests relying 100% on **mocks** (no active network or DB sockets allowed). Runs in under 10ms.
* `tests/integration/`: Local sandboxed testing representing compiled module interactions running against isolated local in-memory DB sandboxes.
* **Hermetic Constraint**: Direct network sockets or live HTTP calls to external internet endpoints are strictly forbidden in any test suite. All interfaces must be mocked.
* **Boundary Ownership Matrix**:
  * **Implementor Agent**: Owns **Unit Tests** and **Integration Tests**.
  * **Architect Agent**: Owns the **Verification Strategy** inside the feature's `DESIGN.md`. The Implementor writes tests to satisfy this strategy (no grading own homework).

---

## 🗂️ Part 9: Architectural Decision Records (ADRs) & Auto-Trigger Rules (To Be Implemented)

To prevent Git merge conflicts across isolated worktrees, ADRs are saved in a hierarchical folder layout matching the Epic/Feature context:
```
docs/
└── sdd/
    ├── proposals/
    └── <epic-slug>/
        ├── adr/                      # Epic-specific ADRs
        │   └── 0001-database.md
        └── <feature-slug>/
            └── adr/                  # Feature-specific ADRs
                └── 0001-parser.md
```
The `sdd-design-architect` agent automatically triggers a new ADR whenever dependency changes, database schema changes, design pattern shifts, or design debates are introduced.

---

## 🔄 Part 10: Post-Merge Agent Retrospectives & Continuous Learning (To Be Implemented)
Immediately upon branch merging, the `sdd-project-manager` runs the retrospective skill:
* **Lessons Learned Compilation**: Writes these lessons to a local file at `./docs/lessons_learned.md`.
* **Architect Ingestion**: The `sdd-architect` is instructed to parse this `lessons_learned.md` file at the beginning of every new feature design, preventing identical design traps.

---

## ✂️ Part 11: Task Decomposition & Micro-Feature Isolation (To Be Implemented)
* Feature Specifications are strictly capped at **12 Gherkin task checkboxes** inside `TASKS.md`.
* If a feature requires more than 12 tasks, the PM agent blocks compilation and splits the spec into modular, sequential sub-features (e.g. `feature-slug-part-1`, `feature-slug-part-2`), each provisioned in its own isolated Git worktree.

---

## 💾 Part 12: Session Checkpoint & Recovery Protocol (To Be Implemented)
Allows the agent to serialize its active context into a standardized Markdown file `.agents/history/checkpoint.md` (ignored in Git).
* **Triggers**: Token counts approach limits (instructs user to start a clean chat), User "pause" commands, or loop compiler errors persisting across 3 sequential attempts.
* **Recovery**: Starting a fresh conversation with `@/context Resume from checkpoint.` loads rules, specs, and the checkpoint, restoring context instantly with zero detail loss.

---

## 📚 Part 13: Pure-Play Static HTML Wiki Skill (To Be Implemented)

To present design specs, ADRs, proposals, and guides in a beautifully styled, highly responsive, and navigable format, we establish a zero-dependency custom static Documentation Portal.

### 1. Pure HTML Static Navigation vs. Live Servers
Rather than running background server processes or heavy frameworks like MkDocs, we compile Markdown directly into navigable, static HTML files using a custom Python compiler designed for offline browsing.
* **Pros of Pure Static HTML Wiki**:
  * **Zero-Dependency**: Runs purely in Python using the standard `markdown` library.
  * **No Active Services**: Zero background processes or listening ports, keeping development local and ultra-secure.
  * **Universal Portability**: Compiled directories (`.docs_build/`) can be opened directly using the `file://` protocol in any browser, copied, or shared without server dependencies.
  * **Mermaid.js Dynamic Rendering**: Renders complex Mermaid diagrams directly inside standard browsers using a global CDN script, completely bypassing strict CORS and ES module limitations.
  * **Hard-Compiled Sidebar & search**: Embeds the computed hierarchical navigation sidebar into every single compiled page with an instant, client-side JavaScript text filter running 100% in browser.

### 2. The Wiki Compiler Skill (`skills/docs-compiler/`)
Provides the `sdd-project-manager` agent with playbooks to generate the portable local wiki.
* **Structure**:
  * `compile_wiki.py`: Scans `docs/` recursively, translates markdown, converts Mermaid code blocks to `<pre class="mermaid">` tags, computes relative depth navigation offsets, embeds sidebars, and compiles output HTMLs to `.docs_build/`.
* **Execution Steps**:
  1. Installs standard markdown parser: `pip install markdown` inside the virtual environment.
  2. Scaffolds directories: Creates `docs/index.md` (landing page), `docs/sdd/`, `docs/adr/`, and `docs/guides/`.
  3. Compiles site: Runs `python3 compile_wiki.py` manually or configures agents to auto-compile when specs are updated.

---

## 🖋️ Part 14: Code Documentation & Docstring Linting Strategy (To Be Implemented)

To ensure uniform codebase readability, a programmatic code documentation standard is enforced.
* **Mandatory Docstrings**: Every python module, class, and public method must have a Google Python Style docstring (`Args`, `Returns`, `Raises` sections).
* **Inline Hygiene**: Obvious syntax comments are banned. Comments are allowed exclusively to document *non-obvious* decisions or package workarounds.
* **Lint Gate**: Validated via `pydocstyle` or `ruff` docstring checks inside the test verification step. Compliance failures will block task completion.

---

## 🧪 Verification Strategy

Once the global bootstrapper and prescriptive skills are implemented, their robustness will be verified through these tests:

1. **Greenfield Init Test**:
   Run `bootstrap.sh test-project git@github.com:user/test-project.git`. Verify Git initialized, origin remote correct, and `.agents/` templates copied cleanly from the specified local process templates directory.
2. **Framework Scaffold Test**:
   Run `bootstrap.sh nextjs-project git@github.com:user/nextjs-project.git --scaffold nextjs`. Verify Next.js generated, and nested framework `.git` folders deleted safely.
3. **Encapsulated Feature Directory Scaffolding Test**:
   Run `manage_worktree.sh prototype epic-slug feature-slug`. Verify Git worktree created and blank templates for `SPEC.md`, `DESIGN.md`, and `TASKS.md` scaffolded strictly inside `docs/sdd/epic-slug/feature-slug/`.
4. **Functional Spec Banned-Content Audit**:
   Write a `SPEC.md` containing SQL queries or class definitions. The validation script must throw an immediate architectural lint error, blocking design and task phases.
5. **Specification Q&A Discovery Test**:
   Draft a spec. Verify the agent pauses execution, prompts the user with conversational feature questions, and integrates user responses into functional journeys in `SPEC.md` prior to writing `DESIGN.md`.
6. **Abstract Design Code Restriction Test**:
   Draft a `DESIGN.md` containing Python code blocks. The validation lint check must fail and require the agent to convert them to ````pseudocode ```` or move them to `references/` before merging.
7. **BDD Task Checklist Alignment Test**:
   Verify `TASKS.md` contains up to 12 checkboxes utilizing standard Gherkin Given/When/Then structures mapped to design nodes.
8. **Naming Conventions Validation Test**:
   Attempt to create a branch named `fix-bug` or a task named `edit file`. The project manager pre-flight check must reject and block execution.
9. **Atomic TDD Execution Test**:
   Verify in transcript that: (a) test file created before production code, (b) test runner logs a failing RED output, (c) minimal GREEN code written to pass.
10. **Hermetic Test Verification**:
    Verify that any active network socket call in unit/integration tests (outside of local mock handlers) fails the build immediately.
11. **ADR Auto-Trigger Test**:
     Simulate a conversation requesting to swap SQLite for PostgreSQL. Verify that the Architect agent immediately triggers a file write creating the ADR in the correct subfolder `docs/adr/epics/mock-epic/features/mock-feat/0001-use-postgresql.md` *prior* to modifying specs.
12. **Task Decomposition Test**:
     Draft a `TASKS.md` containing 18 tasks. Verify the PM blocks execution, flags as over-scoped, and generates a sub-feature decomposition plan.
13. **Retrospective Learnings Test**:
    Close a feature. Verify git diff parsed, retrospective harvested, and lessons appended to `./docs/lessons_learned.md`.
14. **Docs Server Lifecycle Test**:
     Trigger the documentation compiler skill. Verify `markdown` installs, relative offsets are computed, and `compile_wiki.py` generates a portable website in `.docs_build/` that opens directly under `file://` protocol in any browser with functioning sidebar filters and Mermaid renders.
15. **Docstring Linter Check Test**:
     Draft a Python file with PEP 257 violations. Verify `ruff` throws a compilation failure lint error, successfully blocking task completion.
