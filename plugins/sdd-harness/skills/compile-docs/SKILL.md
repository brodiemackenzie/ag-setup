---
name: compile-docs
description: Compile markdown specification capsules, proposals, and logs into a portable offline HTML wiki portal.
---

# Compile Docs Skill Playbook

This skill governs the compilation of specifications and designs into a local offline documentation portal.

---

## Playbook

### 1. Setup Environment
Ensure the markdown parser is installed:
```bash
pip install markdown
```

### 2. Running the Compiler
Execute the compiler script:
```bash
python3 .agents/plugins/sdd-harness/skills/compile-docs/scripts/compile_wiki.py
```
   * **Output Directory**: Standalone website files are written to `.docs_build/`.
   * **Landing Page**: The entry point is compiled at `.docs_build/index.html`.

### 3. Auto-Compile Triggers
The Project Manager agent must automatically trigger `python3 .agents/plugins/sdd-harness/skills/docs-compiler/scripts/compile_wiki.py` immediately after:
* Creating or finishing a new feature specification (`SPEC.md`).
* Finalizing a Technical Design blueprint (`DESIGN.md`).
* Merging and writing a new Architectural Decision Record (`ADR`).
* Writing retrospective continuous lessons to `docs/lessons_learned.md`.

This guarantees that the local offline wiki portal is always perfectly synchronized with the latest specifications.
