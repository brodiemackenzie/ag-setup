#!/usr/bin/env python3
#
# E2E Scenario: Implementor Coding Phase Simulation
# Verifies that the sdd-implementor agent can read specifications,
# write the Flask app code/UI, implement tests, and verify they pass.
#

import os
import shutil
import subprocess
import sys
from sdd_simulator import SDDSimulator

def main():
    sim = SDDSimulator("simulated-implementation-project")
    
    # 1. Setup workspace (uses default strict sandbox permissions)
    sim.setup_workspace()
    
    # 2. Copy process rules & playbooks templates to `.agents`
    templates_src = os.path.join(sim.workspace_dir, "workspace", "templates", "sdd-anchored", "_agents")
    if not os.path.isdir(templates_src):
        templates_src = os.path.join(sim.workspace_dir, ".agents")
    shutil.copytree(
        templates_src,
        os.path.join(sim.temp_path, ".agents"),
        dirs_exist_ok=True
    )

    # 3. Create a python virtual environment inside the workspace and install requirements
    # This simulates having linked python environment inside the sandbox
    sim.log_info("Setting up Python virtual environment and installing packages...")
    subprocess.run(["python3", "-m", "venv", ".venv"], cwd=sim.temp_path)
    
    # Run pip install to install Flask, pytest, and google-genai
    pip_path = os.path.join(sim.temp_path, ".venv", "bin", "pip")
    subprocess.run([pip_path, "install", "flask", "pytest", "pytest-asyncio", "google-genai"], cwd=sim.temp_path, capture_output=True)

    # 4. Seed the specifications from the fixture folder
    sim.log_info("Seeding Guestbook specification documents from fixtures...")
    
    fixture_dir = os.path.join(sim.script_dir, "fixtures", "generative_guestbook")
    docs_dir = os.path.join(sim.temp_path, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    # Copy PROJECT.md
    shutil.copy(
        os.path.join(fixture_dir, "PROJECT.md"),
        os.path.join(docs_dir, "PROJECT.md")
    )
    
    # Create the target epic/feature spec folder
    spec_dir = os.path.join(docs_dir, "sdd", "ep-guest-submissions", "ft-submission-form")
    os.makedirs(spec_dir, exist_ok=True)
    
    # Copy SPEC.md, DESIGN.md, TASKS.md
    for filename in ["SPEC.md", "DESIGN.md", "TASKS.md"]:
        shutil.copy(
            os.path.join(fixture_dir, filename),
            os.path.join(spec_dir, filename)
        )

    # Commit initial spec state
    subprocess.run(["git", "add", "."], cwd=sim.temp_path)
    subprocess.run(["git", "commit", "-m", "seed guestbook specifications", "-q"], cwd=sim.temp_path)

    try:
        # 5. Start implementor conversation
        sim.log_info("Starting Implementor agent coding flow...")
        # Instruct the agent to read the spec and implement the feature
        conv_id = sim.new_conversation(
            "Phase 4 - Sandboxed Implementation: Please read the specifications at docs/sdd/ep-guest-submissions/ft-submission-form/ and implement the tasks checklist in TASKS.md."
        )
        
        # 6. We let the agent cascade execute (it should run its tools to write app.py, templates/index.html, etc. and write pytest tests).
        # We poll or send a follow-up if needed. Since the runner is one-shot, we can send a completion request or check on status.
        # Let's send a request to verify progress
        sim.log_info("Verifying implementation outcomes...")
        
        # 7. Physical File Assertions
        sim.assert_file_exists("app.py")
        sim.assert_file_exists("templates/index.html")
        sim.assert_file_exists("tests/test_app.py")
        
        # Run pytest inside the virtualenv to verify the tests created by the agent pass
        pytest_bin = os.path.join(sim.temp_path, ".venv", "bin", "pytest")
        sim.log_info("Running generated test suite inside virtualenv...")
        test_run = subprocess.run([pytest_bin, "tests/test_app.py"], cwd=sim.temp_path, capture_output=True, text=True)
        
        print(test_run.stdout)
        
        if test_run.returncode != 0:
            sim.log_fail(f"Implementor generated tests failed to execute successfully. Stderr:\n{test_run.stderr}")
            
        sim.log_pass("All implementor-generated tests passed successfully!")

    finally:
        sim.cleanup()

    print("")
    print("\033[1;32m====================================\033[0m")
    print("\033[1;32m SCENARIO 5 (IMPLEMENTATION) PASSED  \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
