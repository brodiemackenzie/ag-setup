# Spec-Driven Development (SDD) Workspace Scaffolding Blueprint

This repository contains a highly optimized, fully version-controlled, and sandboxed Spec-Driven Development (SDD) environment template for AI coding agents (such as Jetski/Antigravity). 

It establishes an absolute separation of concerns by enforcing a strict **Specification (What/Why) ➔ Design (How) ➔ Tasks (Execution)** pipeline, confining coding agents to isolated Git worktrees, and compiling documentation into a zero-dependency local offline HTML portal.

---

## 🏛️ Architecture Overview

The custom architecture operates on two levels: the **Global Layer** (system-wide installers and templates) and the **Local Layer** (project-specific sandboxed runtimes). For an in-depth guide on JetSki agent profiles, rules, skills, and sandboxed communication lifecycle, read the [Core Agent Framework Manual](file:///usr/local/google/home/brodiem/projects/ag-setup/docs/agent_framework_manual.md).

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
        WT -.->|Reads Parent Specs (Read-Only)| B
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
├── docs/
│   ├── PROJECT.md                          # High-Level Project Guiding Document
│   └── agent_framework_manual.md           # Core JetSki & Antigravity Agentic Framework Manual
├── sandbox/                                # Git-ignored sandbox directory for local dry-run tests
│   └── mock-project/                       # Clean bootstrapped mock project replica
├── global/                                 # GLOBAL LAYER (Linked system-wide to ~/.gemini/)
│   ├── global_workflows/
│   │   └── bootstrap.md                    # The conversational /bootstrap command
│   ├── rules/
│   │   └── global-rules.md                 # Global always-on rules and guidelines
│   └── skills/
│       └── project-bootstrap/
│           ├── README.md                   # Bootstrapper CLI manual
│           └── scripts/
│               └── bootstrap.sh            # Global installer script
└── workspace/                              # WORKSPACE LAYER (rsync'd to new projects)
    └── templates/                          # Workspace templates folder
        └── sdd-anchored/                    # SDD Process Template (Copied to new projects)
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
                    ├── sdd-project-blueprint/  # docs/PROJECT.md & Epic layouts
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
2. **Symlink Your Workspace Templates, Workflows & Rules**:
   ```bash
   ln -s ~/projects/ag-setup/workspace/ ~/.gemini/config/workspace
   ln -s ~/projects/ag-setup/global/global_workflows/ ~/.gemini/config/global_workflows
   ln -s ~/projects/ag-setup/global/rules/ ~/.gemini/config/rules
   ```
   *This guarantees that any improvements or modifications you make locally inside your version-controlled `ag-setup` workspace (such as workspace template modifications, rules, or new slash commands) are instantly active globally on your machine without manual copy-pasting. Note that you should NOT pre-create the target folders 'workspace', 'global_workflows', or 'rules' inside '~/.gemini/config/' as the symlink creation will establish them automatically.*

3. **Import Custom Plugins**:
   Import the `project-orchestration` plugin to register the `/project-create` slash command:
   ```bash
   jetski plugins import ~/projects/ag-setup/plugins/project-orchestration/ --force
   ```
4. **Authorize Global Read-Only Workspace Access**:

   Since process templates, modular rules, and playbooks are symlinked directly from your version-controlled `ag-setup` repository, you **MUST** grant all active agents permission to read this folder. Run this safe one-liner to configure it without exposing write permissions:
   ```bash
   python3 -c "
   import json, os
   path = os.path.expanduser('~/.gemini/config/config.json')
   os.makedirs(os.path.dirname(path), exist_ok=True)
   data = {}
   if os.path.exists(path):
       try:
           with open(path, 'r') as f: data = json.load(f)
       except: pass
   data.setdefault('permissions', {}).setdefault('allow', [])

   read_rule = 'read_file(/usr/local/google/home/brodiem/projects/ag-setup)'
   write_rule = 'write_file(/usr/local/google/home/brodiem/projects/ag-setup)'

   if read_rule not in data['permissions']['allow']:
       data['permissions']['allow'].append(read_rule)
   if write_rule in data['permissions']['allow']:
       data['permissions']['allow'].remove(write_rule)

   with open(path, 'w') as f: json.dump(data, f, indent=2)
   print('Successfully added ag-setup to global read-only allowlist!')
   "
   ```

---

## 🎙️ Chat Slash Commands (The SDD Chat Lifecycle)

When chatting with the AI agent inside the workspace, you can use conversational slash commands to run each phase of the SDD process. The agent will execute all filesystem setups, git worktree bindings, and code verifications on your behalf:

1.  **`/blueprint`**: Triggers the Architect Vision Interview, compiles the high-level project goals (`docs/PROJECT.md`), and scaffolds empty directory capsule structures.
2.  **`/spec-feature`**: Prompts you for an Epic/Feature scope, conducts the requirements discovery interview, and compiles `SPEC.md`, `DESIGN.md`, and `TASKS.md` inside the feature capsule.
3.  **`/start-feature`**: Commits all approved specifications in the parent repo, provisions an isolated Git branch worktree (`worktrees/`), links dynamic runtimes (Python/Node), registers the project in Jetski Hub, and starts the implementation conversation.
4.  **`/close-feature`**: Dismantles the feature worktree, prunes branch mappings, and checks git status.

---

## 🛠️ Tooling & Command Manual

### 1. The Project Creator (`/project-create`)
The `/project-create` slash command creates a new project directory under `~/projects/` (or at a specified absolute path), initializes Git, and registers the project in Jetski Hub.

#### 🎙️ Usage in Chat
Simply type the command with the project name:
```
/project-create my-new-project
```
Or specify an absolute path:
```
/project-create my-new-project /usr/local/google/home/brodiem/projects/my-custom-path
```

---

### 2. The Legacy Project Bootstrapper (`bootstrap.sh` / `/bootstrap`) [DEPRECATED]
*Note: This command is kept for reference. Use `/project-create` instead.*

The legacy bootstrapper CLI and conversational workflow automate greenfield directory creation, remote origin binding, and template copying.

#### 🎙️ Option A: Interactive `/bootstrap`
Type `/bootstrap` in chat to conversationally initialize a project with full template scaffolding.

#### 💻 Option B: CLI Command Script
Run manually:
* **Location**: `global/skills/project-bootstrap/scripts/bootstrap.sh`
* **Usage**:
  ```bash
  ./global/skills/project-bootstrap/scripts/bootstrap.sh <project_name> <github_repo_url> [--process <process_slug>]
  ```

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
2. **`close-feature`**:
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
