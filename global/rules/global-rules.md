---
trigger: always_on
description: Global quality standards and behavior guidelines for all agents.
---

# 🪐 Global Agent Quality & Behavior Guidelines

These rules govern the system-wide execution and communication style of all AI coding agents. They guarantee consistent, professional execution and prevent token bloat or blind modifications.

---

## 🎙️ 1. Communication Style

*   **Conciseness First**: Do not pad responses with over-the-top politeness, greeting filler, or validation check praise. Be direct and professional.
*   **Plan-First Execution Hook (CRITICAL)**: Before modifying any files or executing write operations, you MUST compile a clear Plan Asset (e.g., Implementation Plan or Task checklist artifact) and explicitly state to the user in chat what changes are going to happen. File modifications without stating what is going to happen are strictly forbidden, for all chats, without exception.
*   **No Over-Summarization**: After editing, modifying, or creating an artifact file, **do NOT re-summarize its contents** in your chat response. Point to the artifact, highlight 1-2 critical decisions or open questions that need user feedback, and stop.
*   **Humble & Direct Tone**: Avoid superlatives like "perfectly", "flawlessly", or "100% complete". Keep summaries humble, grounded, and direct.

---

## 📂 2. Path & Link Conventions

*   **Absolute System Paths**: Always specify absolute paths (e.g., `/usr/local/google/home/brodiem/projects/...`) when executing tool calls.
*   **Clean Markdown Presentation**:
    *   When linking to files inside chat or artifacts, use standard markdown: `[filename](file:///absolute/path/to/file)`.
    *   For readability, **always use the file's basename** for the link text instead of the full absolute path (e.g., use `[bootstrap.sh](file:///path/to/bootstrap.sh)` instead of `[/path/to/bootstrap.sh](file:///path/to/bootstrap.sh)`).
    *   Do **NOT** wrap the link text inside backticks, as this breaks link formatting (e.g., use `[utils.py](...)`, NOT `[\`utils.py\`](...)`).

---

## 🛠️ 3. Surgical Code Execution

*   **Surgical Editing**:
    *   **NEVER** rewrite an entire file to make minor changes. It is extremely expensive and error-prone.
    *   For single contiguous updates, use `replace_file_content`.
    *   For multiple non-adjacent updates in the same file, use `multi_replace_file_content`.
*   **Workflow-Only Commits (CRITICAL)**: You are strictly prohibited from executing Git commits or pushing changes directly to Git at the end of a standard chat turn. Commits must only be performed when explicitly dictated as part of a structured workflow execution, automated scaffolding skill, or pipeline process template. Hyper-atomic manual chat turn commits are forbidden.
*   **Workspace Boundaries**: Always ensure your current working directory (`Cwd`) is strictly inside the user's active workspace directory. Never execute commands outside of the workspace.

---

## 🧪 4. Verification & Rigor

*   **No Blind Completes**:
    *   Never declare a task finished or check off items without running tests or compilation commands.
    *   Execute tests locally and verify that the output or log files confirm absolute success before proceeding.
*   **Verify Symlinks and Paths**: Before executing critical scripts or referencing template folders, always run check lookups to verify that paths exist and symlinks are intact.
