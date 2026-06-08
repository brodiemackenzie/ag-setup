# SDD Lessons Learned Registry

This document tracks architectural and implementation lessons compiled during project retrospectives. Agents must review this registry prior to drafting new specifications.

---

## Epic: ep-e2e-evaluation | Feature: ft-simulation-pipeline
* **Date**: 2026-06-08
* **Specification Gap Discovered**:
  * The transition from specifications to coding relies on strict path boundaries. If sandboxing rules are not absolute, the Coder agent can write files to the parent workspace or alter templates to bypass test failures.
  * We implemented the "Strict Process Boundaries (No Cheating)" rule to prevent agents from modifying specification files or rules templates to force tests to pass.
* **Bugs & Gotchas**:
  * **Bug b/521465559 (Platform Limitation)**: The `agentapi` CLI tool cannot be used headlessly in IDE mode because the server-side `projectsStore` is uninitialized, triggering nil pointer panics on Connect-RPC requests.
  * **Workaround**: Developers must verify workflows manually in the IDE Chat UI using slash commands (`/bootstrap`, `/blueprint`, `/spec-feature`, `/start-feature`, `/close-feature`) which call internal APIs directly.
* **Architectural Recommendations**:
  * **TDD Loop Escapes**: Always enforce a 3-retry limit on failed tests in Coder loops to prevent token/credit burn. If 3 consecutive failures occur, compile a `failed_test_summary.md` and halt for human feedback.
  * **Git Conflict Resolution**: PM agents can automatically resolve merge conflicts if equipped with playbooks to check parent git diffs and surgically replace inline markers (`<<<<<<<`, `=======`, `>>>>>>>`).
