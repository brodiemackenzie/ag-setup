# Session Checkpoint & State Recovery Playbook

This playbook outlines the protocol for serializing an agent's active conversational state into a local Markdown document, preventing context memory loss during token compactions or loop errors.

---

## Objective
Enable agents to save and restore their exact progress, active objectives, completed tasks, design gaps, and next steps, facilitating seamless context resets and transitions.

---

## The State Serialization Protocol

### 1. Trigger Conditions
An agent must automatically serialize its active state and halt when:
* **Context Bloat Trigger**: The active conversation's token window approaches its limits. (The agent will write the checkpoint and instruct the user to start a fresh chat session).
* **User Pause Trigger**: The user issues "pause", "goodnight", or signals a break in execution.
* **Failure Loop Trigger**: A compiler, test runner, or linter error persists across **3 sequential code modification attempts**.

### 2. Checkpoint File Location
* **File Location**: `.agents/plugins/sdd-harness/history/checkpoint.md` inside the active workspace directory (this file is explicitly ignored in Git).

---

## Checkpoint Template Structure

The checkpoint file must strictly conform to the following outline:

```markdown
# Session Checkpoint: [Epic/Feature Name]

## Active Context & Status
* **Current Epic**: [Epic Slug / Title]
* **Current Feature**: [Feature Slug / Title]
* **Active Goal**: [Explicit current engineering goal]
* **Failure Triggers (if any)**: [Detail of persistent build/compiler errors]

---

## Completed Actions
Review the tasks completed in this session:
1. **Task 1**: Describe what was completed (e.g. *scaffolded router logic*).
2. **Task 2**: Describe what was completed.

---

## Discovered Design Gaps & Edge Cases
* List any roadblocks, library limitations, or user-approved design decisions that modified the specification.

---

## Next Steps
List the immediate, sequential next tasks to execute upon recovery:
1. **Next Task A**: What must be run next.
2. **Next Task B**: Next step.
```

---

## The Recovery / Resume Protocol

To resume execution in a fresh, clean conversation window:
1. The user starts a new chat session.
2. The user inputs: `@/context Resume from checkpoint.`
3. **The Agent's Recovery Steps**:
   * Parse and read `.agents/plugins/sdd-harness/history/checkpoint.md`.
   * Read the active `SPEC.md`, `DESIGN.md`, and `TASKS.md` files in the feature worktree capsule.
   * Read the `docs/lessons_learned.md` to align with historical recommendations.
   * Automatically resume execution at the exact point listed under **Next Steps** in the checkpoint.
4. Present a concise, non-confident summary of the recovered state to the user and wait for their instruction.
