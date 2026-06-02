# Docs Compiler Skill Playbook

This skill governs the zero-dependency, high-performance compiling and serving pipeline that translates all markdown specification capsules, proposals, ADRs, and user guides into a portable local Documentation Portal.

---

## Overview

Rather than spinning up long-running servers or relying on Node-heavy static-site compilers, this skill executes a pure Python static page generator. The output is compiled directly into the local workspace under `.docs_build/` and can be opened in any web browser directly using the offline `file://` protocol, maintaining complete local security and mobility.

---

## Playbook

### 1. Setup Environment
The compilation script requires the `markdown` library. The Project Manager agent must ensure the library is installed inside the virtual environment:
```bash
pip install markdown
```

### 2. Running the Compiler
To compile or refresh the documentation portal:
1. Set your current working directory to the project root.
2. Execute the compiler script:
   ```bash
   python3 .agents/skills/docs-compiler/scripts/compile_wiki.py
   ```
   * **Output Directory**: Standalone website files are written to `.docs_build/`.
   * **Landing Page**: The entry point is compiled at `.docs_build/index.html`.

### 3. Auto-Compile Triggers
The Project Manager agent must automatically trigger `python3 .agents/skills/docs-compiler/scripts/compile_wiki.py` immediately after:
* Creating or finishing a new feature specification (`SPEC.md`).
* Finalizing a Technical Design blueprint (`DESIGN.md`).
* Merging and writing a new Architectural Decision Record (`ADR`).
* Writing retrospective continuous lessons to `docs/lessons_learned.md`.

This guarantees that the local offline wiki portal is always perfectly synchronized with the latest specifications.
