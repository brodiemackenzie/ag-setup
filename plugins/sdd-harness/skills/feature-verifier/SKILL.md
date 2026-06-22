---
name: feature-verifier
description: Verify implementation against requirements, run verification tests, and compile the VERIFICATION_REPORT.md.
---

# Feature Verifier Skill Playbook

You must act as the **sdd-technical-lead** (profile `agents/sdd-technical-lead.json`) to execute this playbook.

---

## Playbook Execution

### 1. Scope Gathering
*   Identify the target Epic and Feature to verify.
*   Verify that `docs/sdd/ep-*/ft-*/SPEC.md`, `DESIGN.md`, and `TASKS.md` exist and are `APPROVED`.
*   Parse if the `--auto` flag is present in instructions.

### 2. Verification Testing
1.  Locate and execute the parent test suite runner (e.g. `pytest` or `npm test`) using `run_command`.
2.  Capture and analyze the test output log.
3.  Cross-check every functional requirement (`req-N`) listed in `SPEC.md` against the test results:
    *   Verify that every requirement has at least one corresponding test casing.
    *   Confirm that all tests associated with the requirement are passing.
4.  Classify each requirement as:
    *   `PASS`: Tests executed and passed.
    *   `FAIL`: Associated tests failed.
    *   `UNTESTED`: No associated tests found.

### 3. Compile Verification Report
*   Formulate the `docs/sdd/ep-*/ft-*/VERIFICATION_REPORT.md` following the template below.
*   **Remediation Steps**: If any requirement is marked `FAIL` or `UNTESTED`:
    *   Propose new remediation tasks to fix the code or add missing test cases.
    *   *Guided Mode*: Ask the user to confirm creation of remediation tasks. Upon approval, append them as new task cards (`tsk-N-fix`) to `TASKS.md`.
    *   *Auto Mode*: Write the remediation task cards directly into `TASKS.md`.

---

## Verification Report Template (`VERIFICATION_REPORT.md`)
The generated document must strictly conform to this structure:

```markdown
---
Type: Feature Verification Report
Status: COMPILED
Author: sdd-technical-lead
Date: [Current Date]
---

# Verification Report: [Feature Name]

## 1. Test Suite Results
*   **Command Executed**: [e.g. pytest tests/unit/auth/]
*   **Total Tests**: [e.g. 14]
*   **Passed**: [e.g. 14]
*   **Failed**: [e.g. 0]

## 2. Specification Audit Table
| Requirement ID | Description | Casing Test File | Audit Status |
| :--- | :--- | :--- | :--- |
| `req-1-valid-input` | Validate signups | `tests/test_auth.py` | PASS |
| `req-2-processing` | Execute database write | `tests/test_db.py` | PASS |

## 3. Remediation Tasks (if any)
*   None.
```

---

## 4. Completion
*   Write `docs/sdd/ep-*/ft-*/VERIFICATION_REPORT.md` to disk.
*   If all requirements are `PASS` and no failures are found:
    *   Set `Status` to `VERIFIED`.
    *   Report success: *"Feature verification complete and passed! Suggest loading the PM & EM to compile the retrospective using the retrospective-compiler skill."*
*   If any failures are found:
    *   Set `Status` to `REMEDIATION_REQUIRED`.
    *   Report warning: *"Feature verification failed. Remediation tasks have been appended to TASKS.md. Suggest reloading the Coder to execute the fixes."*
