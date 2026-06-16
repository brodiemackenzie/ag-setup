# JetSki & Antigravity Agentic Framework Manual

This manual explains the core architecture, execution flow, and configuration layers of JetSki and Antigravity's multi-agent pair programming framework.

---

## 🏛️ 1. Core Principle: The Agentic Loop

An agent in JetSki / Antigravity is not just a stateless LLM chat session. It is a structured execution loop combining four core components:

```
  ┌──────────────────────────────────────────────────────┐
  │                   Active Agent Loop                  │
  │                                                      │
  │   ┌───────────┐     ┌───────────┐     ┌───────────┐  │
  │   │    LLM    │ ──> │   Tools   │ ──> │ Sandbox   │  │
  │   │  Context  │     │ (Command/ │     │ (Worktree │  │
  │   │ (Prompt)  │ <── │  Files)   │ <── │  Files)   │  │
  │   └───────────┘     └───────────┘     └───────────┘  │
  │                           │                          │
  │                           ▼                          │
  │                    ┌─────────────┐                   │
  │                    │ Permissions │                   │
  │                    │ (config.json│                   │
  │                    └─────────────┘                   │
  └──────────────────────────────────────────────────────┘
```

1. **LLM Context Engine**: Underpinned by Google Gemini models, maintaining a rich, structured history of messages, recent files, and environment metadata.
2. **Deterministic Tools**: Access to advanced filesystem, code search, browser, subagent, and command execution capabilities.
3. **Filesystem Sandbox**: Rigid directory confines (such as isolated Git worktrees) keeping the agent's operations safely contained.
4. **Permission Guardrails**: Granular, absolute path verification rules configured at both global (`config.json`) and workspace levels.

---

## 📂 2. The Core Layers of Agent Configuration

JetSki achieves separation of concerns and mitigates token consumption by dividing agent instructions into three distinct layers: **Profiles**, **Rules**, and **Skills**.

| Layer | Format | Scope | Purpose | Example |
| :--- | :--- | :--- | :--- | :--- |
| **1. Profiles** | `.json` | Per Agent Role | Defines capabilities, tools, and write boundaries. | `sdd-architect.json` |
| **2. Rules** | `.md` | System-Wide / Project | Always-on safety, communication, and coding guidelines. | `global-rules.md` |
| **3. Skills** | `SKILL.md` | On-Demand Playbook | Specific procedural tutorials loaded dynamically for a task. | `sdd-spec-writer/` |

### A. Agent Profiles (`*.json`)
Agent profiles define the persona, restrictions, and interface capabilities of specific roles.
* **Location**: `.agents/agents/`
* **Structure**:
  * `"system_prompt"`: Declares the core responsibilities and constraints of the role.
  * `"tools"`: Defines an `allowlist` of permitted tools and a `denylist` of blocked tools (e.g., blocking `run_command` for Architect roles).
  * `"permissions"`: Defines specific absolute/relative `write_paths` the agent is allowed to modify.

### B. Rules (`*.md`)
Rules are always-on behavioral, communication, and code hygiene constraints that are injected directly into the agent's system context.
* **Global Rules** (`~/.gemini/config/rules/`): Enforce system-wide practices (e.g., *Plan-First Rule*, *Workflow-Only Commits*, *Surgical Editing*).
* **Local Rules** (`.agents/rules/`): Enforce project-specific pipelines (e.g., `sdd-pipeline.md` for Spec-Design-Tasks phases, `sdd-tdd-standards.md` for test rigor).

### C. Skills / Playbooks (`SKILL.md`)
To prevent token context bloat, deep playbooks and step-by-step instructions are offloaded to **Skills**.
* **Dynamic Loading**: Agents only read these markdown guidelines and execute related scripts on-demand when they start a specific task (e.g., running `/bootstrap` dynamically loads the bootstrap skill).
* **Self-Correction**: Playbooks contain built-in self-checks, structural templates (e.g., how to format `SPEC.md`), and banned content rules.

---

## 🛡️ 3. The Sandbox & Git Worktree Isolation Pattern

To allow coding agents to run compilers, build suites, and modify files safely in parallel, JetSki utilizes **Git Worktrees** to enforce absolute isolation.

```
~/projects/my-app/                        <-- Root Repository
├── .git/
├── .agents/                              <-- Master templates (rules/ & skills/)
└── worktrees/
    └── sdd-epic/
        └── feature-name/                 <-- Confined Sandbox Workspace
            ├── src/
            ├── tests/
            └── docs/sdd/epic/feature/    <-- Local specs / tasks / designs
```

* **Confinement**: A subagent spawned to work on a feature operates *strictly* within the subfolder `/worktrees/<epic>/<feature>/`.
* **Path Locks**: Path parameters are resolved relative to the worktree root. Any tool call targeting paths outside the sandbox is instantly blocked by the permission manager as a boundary violation.
* **Hermetic Environments**: The Coder agent is responsible for initializing its own local runtime dependencies (e.g. creating virtualenvs and installing packages) inside the worktree jail during the first scaffolding task. Pre-provisioning or symlinking dependencies is avoided to maintain strict isolation.

---

## 🎙️ 4. Async Multi-Agent Orchestration & Communication

When coordinating complex workflows (like SDD), JetSki relies on a parent-to-child async messaging lifecycle:

```
┌───────────────┐          1. invoke_subagent          ┌────────────────┐
│ Parent Agent  │ ───────────────────────────────────> │ Sandboxed Child│
│  (Orchestrator│                                      │ (Architect/    │
│  / PM role)   │ <─────────────────────────────────── │ Implementor)   │
└───────────────┘        2. send_message (Done)        └────────────────┘
```

1. **Spawning (`invoke_subagent`)**: The parent orchestrator (acting as `sdd-project-manager`) calls the `invoke_subagent` tool, specifying:
   * The target agent configuration profile (e.g., `sdd-architect`).
   * The sandboxed workspace branch (`branch` mode to bind a dedicated worktree).
   * A clear, actionable initial prompt.
2. **Non-Blocking Execution**: The child agent runs autonomously in the background. The parent agent does **not** poll or run loops; it yields execution and goes idle.
3. **Reactive Wakeup**: When the child agent completes its design task, compiles its checkpoint, or requires user feedback, it uses the `send_message` tool to report back to the parent. The JetSki system automatically wakes up the parent agent, providing the full transcript and results.

---

## 💡 5. Core Best Practices for Developers
* **Always version-control playbooks**: Keep your `.agents/skills/` checked in. It guarantees that your AI team moves in sync with your codebase changes.
* **Plan-First Hook is King**: Never let an agent edit files without generating an Implementation Plan or Task Checklist asset first. This allows you to correct direction and maintain control *before* any code is modified.
* **Confine coder agents**: Keep your `sdd-implementor` restricted to the worktree sandbox, and only let the `sdd-project-manager` handle main repository mergers.
