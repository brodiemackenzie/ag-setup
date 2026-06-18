# Git Conflict Reconciliation Playbook

This playbook guides the `sdd-project-manager` agent on how to surgically resolve Git merge conflicts encountered during feature branch closures or merges.

---

## Objective
Detect merge conflict states, analyze histories to identify the intent of conflicting commits, surgically remove git inline conflict markers, and restore the parent branch to a clean, passing state.

---

## 🏛️ Reconciling Conflicts (Step-by-Step)

When a git merge subcommand fails with conflict markers:

### Step 1: Identify Conflicted Files
*   Run `git status` using the terminal tool.
*   Locate files with state `both modified` (conflicted files).

### Step 2: Diffs & History Context Audit (Intent Check)
Before editing any conflicted file, you **MUST** run context lookups to understand the parent branch intent:
1.  **Check commits history**: Run `git log -n 5 <file_path>` on the conflicted file to see what commits occurred in the parent branch since branching.
2.  **Verify specs alignment**: Open `docs/sdd/ep-<epic>/ft-<feature>/SPEC.md` and `DESIGN.md` in the parent repository. The approved specifications are your **source of truth**. Any code conflict must resolve in favor of the spec rules.

### Step 3: Parse and Resolve Conflict Markers
*   Open the conflicted file using `view_file` and locate the conflict blocks:
    ```
    <<<<<<< HEAD
    Parent Branch Segment (Active main code)
    =======
    Feature Branch Segment (Sandbox coder changes)
    >>>>>>> branch-name
    ```
*   Decide how to resolve the segments:
    *   If the parent branch made general refactorings (e.g. naming changes) but your feature code is required, merge them surgically (e.g. keeping both features under the new variable names).
    *   If the conflict is in a specification file (`SPEC.md` / `DESIGN.md`), resolve the files to align with the latest approved design decisions.
*   Use `replace_file_content` or `multi_replace_file_content` to surgically remove the markers (`<<<<<<<`, `=======`, `>>>>>>>`) and replace the conflict blocks with the resolved clean code.

### Step 4: Validate and Stage
1.  Run the tests (e.g., `pytest` or system checks) to verify that your resolved code compiles and passes successfully.
2.  Run `git add <resolved_file>` for each resolved file.
3.  Once all files are resolved, commit the merge:
    ```bash
    git commit -m "merge branch and resolve conflicts for ep-<epic> ft-<feature>"
    ```

---

## 🚨 Escalation Boundary (When to Await User)

You must halt the automated merge immediately and ask the user for manual guidance in the chat if:
*   A file was **deleted in the parent branch** but modified/created in the feature branch.
*   The conflict spans hundreds of lines of complex logic that might introduce regression risks.
*   Resolving the conflict requires shifting specifications or designs.
