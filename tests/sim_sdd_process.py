#!/usr/bin/env python3
#
# Chained E2E Simulation Pipeline
# Executes the entire Spec-Driven Development (SDD) process sequentially
# by loading prompts, requirements, and assertion contracts from external fixtures.
#

import argparse
import json
import os
import shutil
import subprocess
import sys
from sdd_simulator import SDDSimulator

def main():
    parser = argparse.ArgumentParser(description="Chained E2E Simulation Pipeline")
    parser.add_argument(
        "--fixture",
        default="generative_guestbook.json",
        help="Fixture file name located under tests/fixtures/"
    )
    args = parser.parse_args()

    # Load the specified fixture file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    fixture_path = os.path.join(script_dir, "fixtures", args.fixture)
    if not os.path.isfile(fixture_path):
        print(f"[ERROR] Fixture file not found: {fixture_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading test fixture: {args.fixture}...")
    with open(fixture_path, "r") as f:
        fixture = json.load(f)

    import time
    project_name = f"{fixture['project_name']}-{int(time.time())}"
    blueprint = fixture["blueprint_inputs"]
    specs = fixture["spec_inputs"]
    assertions = fixture["assertions"]

    epic_slug = specs["epic_slug"]
    feature_slug = specs["feature_slug"]
    worktree_slug = f"{epic_slug}-{feature_slug}"

    # 1. Main Project Simulator Instance
    sim = SDDSimulator(project_name)
    sim.setup_workspace()
    
    # Pre-bootstrap sandbox workspace to simulate already-bootstrapped state
    sim.log_info("Pre-bootstrapping sandbox workspace...")
    import shutil
    templates_src = os.path.join(sim.workspace_dir, "workspace", "templates", "sdd-anchored", "_agents")
    if not os.path.isdir(templates_src):
        # Fallback to the active workspace's own .agents folder
        templates_src = os.path.join(sim.workspace_dir, ".agents")
        
    if not os.path.isdir(templates_src):
        sim.log_fail(f"Could not locate templates source folder. Tried framework templates and active .agents folder.")

    shutil.copytree(
        templates_src,
        os.path.join(sim.temp_path, ".agents"),
        dirs_exist_ok=True
    )
    with open(os.path.join(sim.temp_path, ".gitignore"), "w") as f:
        f.write(".agents/history/\nworktrees/\ntarget/\n.venv/\nnode_modules/\n")
        
    subprocess.run(["git", "add", "."], cwd=sim.temp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit (bootstrapped)"], cwd=sim.temp_path, check=True)

    worktree_path = os.path.expanduser(
        f"~/.gemini/jetski/worktrees/{sim.project_name}/{worktree_slug}"
    )

    try:
        # =====================================================================
        # PHASE 2: PROJECT BLUEPRINT
        # =====================================================================
        sim.log_info("\n>>> PHASE 2: COMPILING PROJECT BLUEPRINT...")
        conv_id = sim.new_conversation("Phase 1 - Project Blueprint")
        sim.send_message(conv_id, "/blueprint")
        
        # Playback Vision interview answers from fixture
        sim.send_message(conv_id, blueprint["objective"])
        sim.send_message(conv_id, blueprint["tech_stack"])
        sim.send_message(conv_id, blueprint["breakdown"])
        sim.send_message(conv_id, "yes, write the blueprint docs/PROJECT.md")

        # Assertions
        sim.wait_for_file("docs/PROJECT.md")
        sim.assert_file_exists("docs/PROJECT.md", "Core Objective")
        sim.log_info("INFO: Project Blueprint created successfully at docs/PROJECT.md.")

        # =====================================================================
        # PHASE 3: SPECIFICATION & DESIGN COMPILATION
        # =====================================================================
        sim.log_info("\n>>> PHASE 3: COMPILING SPECIFICATION & DESIGN...")
        sim.log_info(f"INFO: Feature Specification started for epic/feature: {epic_slug}/{feature_slug}.")
        conv_id = sim.new_conversation("Phase 2.1 - Feature Specification")
        sim.send_message(conv_id, "/spec-feature")
        
        # Scope selection
        sim.send_message(conv_id, f"{epic_slug}/{feature_slug}")

        # Playback Spec/Design answers from fixture
        sim.send_message(conv_id, specs["discovery_input"])
        sim.send_message(conv_id, "yes, write the spec files to disk")

        # Assertions
        spec_root = f"docs/sdd/{epic_slug}/{feature_slug}"
        sim.wait_for_file(f"{spec_root}/SPEC.md", contains_text=assertions["spec_contains"])
        sim.log_info(f"INFO: Functional Specification created successfully at {spec_root}/SPEC.md.")
        sim.wait_for_file(f"{spec_root}/DESIGN.md", contains_text=assertions["design_contains"])
        sim.log_info(f"INFO: Technical Design created successfully at {spec_root}/DESIGN.md.")
        sim.wait_for_file(f"{spec_root}/TASKS.md", contains_text=assertions["tasks_contains"])
        sim.log_info(f"INFO: Actionable Task Checklist created successfully at {spec_root}/TASKS.md.")
        sim.assert_file_exists(f"{spec_root}/SPEC.md", assertions["spec_contains"])
        sim.assert_file_exists(f"{spec_root}/DESIGN.md", assertions["design_contains"])
        sim.assert_file_exists(f"{spec_root}/TASKS.md", assertions["tasks_contains"])

        # Commit specs to git history
        subprocess.run(["git", "add", "."], cwd=sim.temp_path)
        subprocess.run(["git", "commit", "-m", "formal specifications compiled", "-q"], cwd=sim.temp_path)
        sim.log_info("INFO: Feature specifications committed to main repository.")

        # =====================================================================
        # PHASE 4: WORKTREE SANDBOX PROTOTYPING
        # =====================================================================
        sim.log_info("\n>>> PHASE 4: PROVISIONING WORKTREE SANDBOX...")
        
        # Clean any residues of previous worktree sandbox run
        if os.path.exists(worktree_path):
            sim.log_info("Cleaning pre-existing worktree residues...")
            subprocess.run(["git", "worktree", "remove", "--force", worktree_path], cwd=sim.temp_path, capture_output=True)
            subprocess.run(["git", "branch", "-D", worktree_slug], cwd=sim.temp_path, capture_output=True)

        # Create a parent virtualenv so it can be inherited by the sandbox link-env step
        sim.log_info(f"INFO: Provisioning sandboxed worktree environment at {worktree_path}...")
        sim.log_info("Initializing virtualenv in parent project...")
        subprocess.run(["python3", "-m", "venv", ".venv"], cwd=sim.temp_path, check=True)
        sim.log_info("INFO: Virtualenv initialized in sandbox.")
        
        # Install packages in parent
        parent_pip = os.path.join(sim.temp_path, ".venv", "bin", "pip")
        sim.log_info("INFO: Installing dependencies in sandbox virtualenv...")
        subprocess.run([parent_pip, "install", "flask", "pytest", "pytest-asyncio", "google-genai"], cwd=sim.temp_path, check=True)
        sim.log_info("INFO: Dependencies successfully installed (using Airlock mirror).")

        # Execute start-feature in chat (letting the PM agent run the shell scripts for us)
        sim.log_info("Running /start-feature workflow...")
        conv_id = sim.new_conversation("Phase 2.2 - Feature Implementation")
        sim.send_message(conv_id, "/start-feature")
        sim.send_message(conv_id, f"{epic_slug}/{feature_slug}")
        res = sim.send_message(conv_id, "yes")

        # Extract the conversation ID of the spawned coder session
        import re
        json_str = json.dumps(res)
        match = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json_str)
        if not match:
            sim.log_fail(f"Could not find coder conversation ID in response: {json_str}")
        coder_conv_id = match.group(0)
        sim.log_info(f"Extracted coder conversation ID: {coder_conv_id}")

        # Verify sandbox was created and linked
        if not os.path.isdir(worktree_path):
            sim.log_fail(f"Worktree directory was not created at expected path: {worktree_path}")
        sim.log_info("INFO: Git worktree created successfully.")
        if not os.path.isdir(os.path.join(worktree_path, ".venv")):
            sim.log_fail(f"Python virtualenv was not linked/created in worktree sandbox.")
            
        sim.log_pass("Worktree sandbox successfully provisioned and linked.")

        # =====================================================================
        # PHASE 5: SANDBOX IMPLEMENTATION (CODING)
        # =====================================================================
        sim.log_info("\n>>> PHASE 5: EXECUTING CODING PHASE IN SANDBOX...")
        sim.log_info("INFO: Code implementation phase started in sandbox.")
        


        # Wait for Coder to finish by polling for expected files
        import time
        sim.log_info("Waiting for Coder to generate files...")
        timeout = 300 # 5 minutes
        start_time = time.time()
        success = False
        while time.time() - start_time < timeout:
            all_exist = True
            for c_file in assertions["code_files"]:
                abs_path = os.path.join(worktree_path, c_file)
                if not os.path.isfile(abs_path):
                    all_exist = False
                    break
            if all_exist:
                success = True
                break
            time.sleep(10)
        
        if not success:
            sim.log_fail("Timeout waiting for Coder to generate files.")
        sim.log_pass("Coder finished generating files.")
        
        # Assert Coder generated files from fixture list
        sim.log_info("Verifying generated code and test assets...")
        for c_file in assertions["code_files"]:
            sim.assert_file_exists(os.path.join(worktree_path, c_file))
        
        # Run generated tests inside the sandbox virtualenv
        pytest_bin = os.path.join(worktree_path, ".venv", "bin", "pytest")
        sim.log_info("Running generated test suite inside sandbox...")
        # Resolve test suite path from fixture assertions if specified
        test_suite = assertions.get("test_suite", f"tests/test_{feature_slug.replace('ft-', '').replace('-', '_')}.py")
        test_run = subprocess.run([pytest_bin, test_suite], cwd=worktree_path, capture_output=True, text=True)
        
        print(test_run.stdout)
        if test_run.returncode != 0:
            sim.log_fail(f"Coder-generated test suite failed. Stderr:\n{test_run.stderr}")
            
        sim.log_pass("All Coder-generated unit and integration tests passed cleanly!")
        sim.log_info("INFO: Sandbox test suite passed successfully.")



        # =====================================================================
        # PHASE 6: SANDBOX TEARDOWN & MERGE CHECK
        # =====================================================================
        sim.log_info("\n>>> PHASE 6: TEARDOWN & WORKTREE CLOSURE...")
        sim.log_info("INFO: Feature close-out and merge review started.")
        
        # Run close-feature in chat (letting the PM agent dismantle the branch for us)
        sim.log_info("Running /close-feature workflow...")
        conv_id = sim.new_conversation("Phase 2.3 - Feature Close")
        sim.send_message(conv_id, "/close-feature")
        sim.send_message(conv_id, f"{epic_slug}/{feature_slug}")

        if os.path.exists(worktree_path):
            sim.log_fail("Worktree folder was not dismantled after close-feature execution.")
            
        sim.log_pass("Worktree sandbox dismantled cleanly.")
        sim.log_info("INFO: Sandboxed worktree dismantled and cleaned up.")
        sim.log_info("INFO: E2E Simulation Pipeline completed successfully.")

    finally:
        # Teardown parent config
        sim.cleanup()
        
        # Clean any remaining worktree directory residues
        if os.path.exists(worktree_path):
            subprocess.run(["rm", "-rf", worktree_path])

    print("")
    print("\033[1;32m====================================\033[0m")
    print(f"\033[1;32m PIPELINE OK FOR FIXTURE: {args.fixture} \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
