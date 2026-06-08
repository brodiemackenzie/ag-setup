#!/usr/bin/env python3
#
# E2E Scenario: Coder TDD Loop Escape Simulation (Unhappy Path)
# Verifies that when tests fail persistently due to unresolved dependencies or errors,
# the sdd-implementor agent halts after 3 consecutive failures and documents the issue.
#

import os
import shutil
import subprocess
import sys
from sdd_simulator import SDDSimulator

def main():
    sim = SDDSimulator("simulated-loop-escape-project")
    
    # 1. Setup workspace (uses default strict sandbox permissions)
    sim.setup_workspace()
    
    # 2. Copy process rules & playbooks templates to `.agents`
    shutil.copytree(
        os.path.join(sim.workspace_dir, "workspace", "templates", "sdd-anchored", "_agents"),
        os.path.join(sim.temp_path, ".agents"),
        dirs_exist_ok=True
    )

    # 3. Create a python virtual environment inside the workspace and install requirements
    sim.log_info("Setting up Python virtual environment...")
    subprocess.run(["python3", "-m", "venv", ".venv"], cwd=sim.temp_path)
    
    # Install standard test dependencies
    pip_path = os.path.join(sim.temp_path, ".venv", "bin", "pip")
    subprocess.run([pip_path, "install", "flask", "pytest", "pytest-asyncio"], cwd=sim.temp_path, capture_output=True)

    # 4. Seed the specifications and a BROKEN test file (imports a non-existent package)
    sim.log_info("Seeding specifications and a broken test file...")
    
    project_md = """# Project Blueprint: Loop Escape Test
* Tech Stack: python
* Epics:
  * ep-loop-escape
    * ft-broken-imports
"""

    spec_md = """# Functional Specification: Broken Imports

## 1. Objective
Verify that the system halts safely when encountering unresolvable environment dependencies.

## 2. Requirements
* **req-broken-import**: The test suite must verify imports of the internal library `secret_unreleased_gcp_library`.
"""

    design_md = """# Technical Design: Broken Imports

## 1. Verification Strategy
* Unit/Integration Tests (`tests/test_broken.py`):
  * Test must import `secret_unreleased_gcp_library` and assert True.
"""

    tasks_md = """# Actionable Tasks: Broken Imports

This document tracks the TDD implementation steps.

---

## Epic: ep-loop-escape
## Feature: ft-broken-imports

---

## Gherkin BDD Checklist

- [ ] **tsk-0-scaffold ([Ref: Workspace Scaffolding] Setup app folder structure)**
  * **Given** an empty repository
  * **When** app is initialized
  * **Then** running pytest returns success

- [ ] **tsk-1-broken-test ([Ref: Verification Strategy] Implement tests/test_broken.py and verify imports)**
  * **Given** a test requiring 'secret_unreleased_gcp_library'
  * **When** running pytest
  * **Then** the import fails, and the agent halts after 3 retry loops.
"""

    # Pre-write the failing test file in the workspace
    broken_test_py = """# Test file with missing dependency
import pytest
import secret_unreleased_gcp_library

def test_missing_import():
    assert True
"""

    docs_dir = os.path.join(sim.temp_path, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    with open(os.path.join(docs_dir, "PROJECT.md"), "w") as f:
        f.write(project_md)
        
    spec_dir = os.path.join(docs_dir, "sdd", "ep-loop-escape", "ft-broken-imports")
    os.makedirs(spec_dir, exist_ok=True)
    with open(os.path.join(spec_dir, "SPEC.md"), "w") as f:
        f.write(spec_md)
    with open(os.path.join(spec_dir, "DESIGN.md"), "w") as f:
        f.write(design_md)
    with open(os.path.join(spec_dir, "TASKS.md"), "w") as f:
        f.write(tasks_md)

    tests_dir = os.path.join(sim.temp_path, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, "test_broken.py"), "w") as f:
        f.write(broken_test_py)

    # Commit initial state
    subprocess.run(["git", "add", "."], cwd=sim.temp_path)
    subprocess.run(["git", "commit", "-m", "seed loop escape specs and broken test", "-q"], cwd=sim.temp_path)

    try:
        # 5. Start implementor conversation
        sim.log_info("Starting Implementor agent coding flow...")
        conv_id = sim.new_conversation(
            "Please read the specifications at docs/sdd/ep-loop-escape/ft-broken-imports/ and implement the tasks checklist in TASKS.md."
        )
        
        # 6. Physical Assertions on Loop Escape Outcomes
        sim.log_info("Verifying TDD Loop Escape outcomes...")
        
        # Verify that failed_test_summary.md was written
        summary_path = "docs/sdd/ep-loop-escape/ft-broken-imports/failed_test_summary.md"
        sim.assert_file_exists(summary_path, "secret_unreleased_gcp_library")
        sim.assert_file_exists(summary_path, "tsk-1-broken-test")
        
        sim.log_pass("TDD Loop Escape verified successfully! The agent correctly halted and compiled the error summary.")

    finally:
        sim.cleanup()

    print("")
    print("\033[1;32m====================================\033[0m")
    print("\033[1;32m SCENARIO 6 (LOOP ESCAPE) PASSED     \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
