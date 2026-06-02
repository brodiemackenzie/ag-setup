# Spec-Driven Development (SDD) Workspace Scaffolding Blueprint

This repository contains a highly optimized, fully version-controlled, and sandboxed Spec-Driven Development (SDD) environment template for AI coding agents (such as Jetski/Antigravity). 

It establishes an absolute separation of concerns by enforcing a strict **Specification (What/Why) ➔ Design (How) ➔ Tasks (Execution)** pipeline, confining coding agents to isolated Git worktrees, and compiling documentation into a zero-dependency local offline HTML portal.

---

## 🏛️ Architecture Overview

The custom architecture operates on two levels: the **Global Layer** (system-wide installers and templates) and the **Local Layer** (project-specific sandboxed runtimes).

```mermaid
graph TD
    subgraph Global [Global Layer (~/.gemini/)]
        A[Global project-bootstrap Skill] -->|Executes bootstrap.sh| B[Target Workspace Folder]
        SL[~/.gemini/config/workspace/] -->|Symlinked to local workspace| C
    end
    
    subgraph Local [Local Layer (~/projects/my-app/)]
        B -->|Contains .agents/| D[rules/ & agents/ & skills/]
        B -->|Spawns| PM[sdd-project-manager agent]
        B -->|Spawns| ARCH[sdd-architect agent]
        B -->|Spawns| IMPL[sdd-implementor agent]
        
        PM -->|Executes manage_worktree.sh| WT[(Feature Git Worktrees)]
        WT -->|Symlinks node_modules / python env| B
    end
    
    subgraph Development [Development Layer (~/projects/ag-setup/)]
        C[ag-setup/workspace/] -->|Version-controlled locally| Git[(GitHub Repository)]
    end
```

---

## 🎯 Problems Solved

1. **Token Context Bloat**: Instead of injecting monolithic rule files (12,000+ characters) on every turn, rules are decomposed into three small modular files (each < 2,500 chars). Extensive playbooks and templates are offloaded to **Skills** which are only read on-demand by the agents when executing specific tasks.
2. **Git History Pollution**: Custom agents are strictly prohibited from executing inside or writing to the top-level workspace. They operate strictly within isolated Git worktrees under `worktrees/`, ensuring that parallel branches never collide.
3. **Lack of Testing Rigor**: Core rules ban "blind completes" in the TDD loop. Implementor agents are strictly forbidden from checking off tasks without executing tests and capturing passing console logs directly in the conversation history.
4. **Secure, Zero-Dependency Spec Portals**: Eliminates heavy documentation servers or framework dependencies (like MkDocs). Spec documents and Mermaid charts are compiled recursively into a portable `.docs_build/` directory browseable completely offline in any browser via the local `file://` protocol.

---

## 📂 Repository Directory Layout

```
ag-setup/
├── README.md                               # This onboarding manual and guide
├── jetski_customization_plan.md            # Detailed Antigravity customization plan
├── sandbox/                                # Git-ignored sandbox directory for local dry-run tests
│   └── mock-project/                       # Clean bootstrapped mock project replica
├── global/                                 # GLOBAL LAYER (Linked system-wide to ~/.gemini/)
│   ├── global_workflows/
│   │   └── bootstrap.md                    # The conversational /bootstrap command
│   └── skills/
│       └── project-bootstrap/
│           ├── README.md                   # Bootstrapper CLI manual
│           └── scripts/
│               └── bootstrap.sh            # Global installer script
└── workspace/                              # WORKSPACE LAYER (rsync'd to new projects)
    └── sdd-process/                        # SDD Process Template (Copied to new projects)
        └── _agents/
            ├── agents/
            │   ├── sdd-architect.json      # Specification & Design compiler JSON blueprint
            │   ├── sdd-implementor.json    # TDD Implementor & Coder JSON blueprint
            │   └── sdd-project-manager.json# Branch & Git worktree coordinator JSON blueprint
            ├── rules/
            │   ├── sdd-pipeline.md         # Modular rule: Phase 0 planning & Spec-Design-Tasks
            │   ├── sdd-sandboxing.md       # Modular rule: Strict active worktree relative locks
            │   └── sdd-tdd-standards.md    # Modular rule: Strict TDD loops & docstring lints
            └── skills/
                ├── docs-compiler/          # Standalone offline wiki compiler
                ├── document-editor/        # Surgical Anchor-and-Verify markdown editor
                ├── sdd-design-architect/   # Schemas, contracts, & ADR triggers
                ├── sdd-proposal-drafter/   # executive summary & Epic layouts
                ├── sdd-retrospective/      # Post-merge git parsing & lessons learned appending
                ├── sdd-spec-writer/        # Discovery specs Q&A interviews
                ├── sdd-task-generator/     # BDD Gherkin checklist compilers (12-task limit)
                ├── session-checkpoint/     # Token-compaction state recovery checkpoints
                ├── tdd-flow/               # Red-Green-Refactor loops
                └── worktree-manager/       # Worktree lifecycle shell manager (manage_worktree.sh)
```

---

## 🚀 Global Installation & Setup

To install these templates globally so you can use the bootstrapper CLI to initialize new projects instantly:

1. **Create the Global Antigravity Folder**:
   ```bash
   mkdir -p ~/.gemini/config/
   ```
2. **Symlink Your Workspace Templates & Workflows**:
   ```bash
   ln -s ~/projects/ag-setup/workspace/ ~/.gemini/config/workspace
   ln -s ~/projects/ag-setup/global/global_workflows/ ~/.gemini/config/global_workflows
   ```
   *This guarantees that any improvements or modifications you make locally inside your version-controlled `ag-setup` workspace (such as workspace template modifications or new slash commands) are instantly active globally on your machine without manual copy-pasting. Note that you should NOT pre-create the target folders 'workspace' or 'global_workflows' inside '~/.gemini/config/' as the symlink creation will establish them automatically.*

---

## 🛠️ Tooling & Command Manual

### 1. The Project Bootstrapper (`bootstrap.sh` / `/bootstrap`)
The bootstrapper CLI and conversational workflow automate greenfield directory creation under `~/projects/`, clean framework git files, bind target origin remotes, and safely rsync process templates without duplicate git history metadata.

#### 🎙️ Option A: Interactive `/bootstrap` (Recommended)
If you are in a chat session with Jetski/Antigravity, simply type:
```
/bootstrap
```
The agent will take the lead and conversationally collect the three required inputs (Project Name, GitHub Remote SSH URL, and scaffolding choice) **one at a time** in chat, and execute the installer automatically on your behalf. No terminal commands to remember!

#### 💻 Option B: CLI Command Script
Run the script manually in your terminal:
* **Location**: `global/skills/project-bootstrap/scripts/bootstrap.sh`
* **Usage**:
  ```bash
  ./global/skills/project-bootstrap/scripts/bootstrap.sh <project_name> <github_repo_url> [--process <process_slug>] [--scaffold <framework>]
  ```
* **Arguments**:
  * `<project_name>`: The directory name under `~/projects/` (or a relative path like `./sandbox/my-app` if initializing a test sandbox).
  * `<github_repo_url>`: The GitHub URL to bind as `origin`.
* **Options**:
  * `--process`: The template slug inside `~/.gemini/config/workspace/` (defaults to `sdd-process`).
  * `--scaffold`: Framework boilerplate setup: `nextjs` (Npx generator), `python` (Venv, requirements, basic pytest setup), or `none` (default).

---

### 2. The Git Worktree Lifecycle Manager (`manage_worktree.sh`)
The worktree manager governs the sandboxed lifecycle of individual epic/feature branches, dynamic library bindings, and safe post-testing branch closures.

* **Location**: `.agents/skills/worktree-manager/scripts/manage_worktree.sh`
* **Usage**:
  ```bash
  .agents/skills/worktree-manager/scripts/manage_worktree.sh <subcommand> <epic_slug> <feature_slug>
  ```

#### Subcommands:
1. **`prototype`**:
   * Creates a new Git branch `feature/<epic_slug>/<feature_slug>`.
   * Provisions an isolated Git worktree directory under `worktrees/<epic_slug>/<feature_slug>/`.
   * Automatically scaffolds empty, GFM-compliant spec blueprints inside the worktree's feature folder: `docs/sdd/<epic_slug>/<feature_slug>/SPEC.md`, `DESIGN.md`, and `TASKS.md`.
2. **`link-env`**:
   * Detects local technology stacks and binds local environments: dynamic symlinking of root parent `node_modules`, inherited system virtualenvs (`python3 -m venv --system-site-packages`), or shared Rust cargo target caches.
3. **`close-feature`**:
   * Verifies tests, prunes, and deletes the Git worktree folder from the filesystem (`git worktree remove --force`).
   * Cleans up the Git branch mapping index cleanly.

---

### 3. The Docs Wiki Compiler (`compile_wiki.py`)
The compiler recursively scans all markdown documents (specifications, ADRs, retrospectives) inside your workspace, translates Markdown markup into HTML, extracts Mermaid fenced blocks, computes relative depth prefix offsets, and generates a browseable static HTML portal.

* **Location**: `.agents/skills/docs-compiler/scripts/compile_wiki.py`
* **Usage**:
  Ensure the `markdown` library is active in your Python virtualenv (`pip install markdown`), then run:
  ```bash
  python3 .agents/skills/docs-compiler/scripts/compile_wiki.py
  ```
* **Verification**:
  Open `.docs_build/index.html` in any web browser. Test the client-side search filtering, verify relative depth links in the sidebar, and audit dynamic Mermaid diagrams rendered as standard vector graphics (SVGs) instantly!
