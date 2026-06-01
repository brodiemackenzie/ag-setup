# Document Editor Skill Playbook

This playbook teaches the agent surgical, high-precision editing patterns for Markdown files (`SPEC.md`, `DESIGN.md`, `TASKS.md`, etc.), ensuring document structure remains clean and consistent.

---

## Objective
Perform clean text modifications, append items to specific headers surgically (no blind append-to-end), synchronize Tables of Contents, re-number ordered lists, and run formatting linters.

---

## The "Anchor-and-Verify" surgical Edit Protocol

When modifying a specification or design document, you must perform edits surgically using specific line ranges and header blocks rather than rewriting the whole file:

1. **Locate the Anchor**: Locate the exact markdown heading (e.g., `## 3. User Requirements`) or section block containing the text you need to modify.
2. **Determine Line Ranges**: Use `view_file` on the section to establish exact line boundaries before executing replacements.
3. **Targeted Replacements**: Call `replace_file_content` targeting only the specific lines.
4. **Verify Surrounding Content**: After editing, read the lines directly before and after the replaced block to verify that no surrounding text was corrupted or formatting markers broken.

---

## Document Hygiene Rules

To maintain professional documentation, you must strictly follow these rules:

### 1. Sequential List Re-numbering
* If you add, delete, or modify an ordered list item (e.g. `1. Req-1`, `2. Req-2`), you must immediately scan the rest of that list section and re-sequence all following list items to ensure the numbering remains contiguous.

### 2. Bullet Standardization
* Maintain absolute bullet consistency. Use hyphens (`-`) for all bulleted lists throughout the file. Avoid mixing `*` and `-` markers in the same document.

### 3. Table of Contents Synchronization
* If you add, rename, or delete any markdown header (`#`, `##`, `###`), you must update the Table of Contents at the top of the document to accurately reflect the new structure and target links.

### 4. Automated Formatting Hook
* **Action**: Immediately after any markdown file mutation is completed, the Project Manager agent must run the Markdown formatter tool in the terminal:
  ```bash
  mdformat <path_to_file>
  ```
* This automatically corrects micro-formatting variances: correcting misaligned markdown tables, standardizing list bullet symbols, and cleaning excessive blank lines.
