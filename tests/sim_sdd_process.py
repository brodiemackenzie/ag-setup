#!/usr/bin/env python3
#
# Stateful E2E Simulation Pipeline
# Executes the Spec-Driven Development (SDD) process step-by-step
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
    parser.add_argument(
        "--stage",
        choices=["blueprint", "specs", "worktree", "implement", "close"],
        required=True,
        help="Execute a single stage of the E2E simulation step-by-step"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Load the specified fixture file
    fixture_path = os.path.join(script_dir, "fixtures", args.fixture)
    if not os.path.isfile(fixture_path):
        print(f"[ERROR] Fixture file not found: {fixture_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading test fixture: {args.fixture}...")
    with open(fixture_path, "r") as f:
        fixture = json.load(f)

    stage = args.stage

    # Setup project variables and dynamic paths
    active_project_id = os.environ.get("ANTIGRAVITY_PROJECT_ID")
    if active_project_id:
        # Running inside an active workspace container
        temp_path = os.getcwd()
        project_name = os.path.basename(temp_path)
    else:
        # Standalone sandbox mode fallback
        project_name = fixture["project_name"]
        temp_path = os.path.join(script_dir, "..", "sandbox", project_name)

    specs = fixture["spec_inputs"]
    epic_slug = specs["epic_slug"]
    feature_slug = specs["feature_slug"]
    worktree_slug = f"{epic_slug}-{feature_slug}"

    if stage == "implement":
        # In implement stage, we are executing inside the checked-out worktree directory
        worktree_path = os.getcwd()
    else:
        worktree_path = os.path.expanduser(
            f"~/.gemini/jetski/worktrees/{project_name}/{worktree_slug}"
        )

    # Initialize Simulator
    if active_project_id:
        sim = SDDSimulator(project_name)
        sim.project_id = active_project_id
        sim.temp_path = temp_path
    else:
        import uuid
        project_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, project_name))
        sim = SDDSimulator(project_name)
        sim.project_id = project_uuid
        sim.temp_path = temp_path
        sim.config_path = os.path.join(os.path.expanduser("~/.gemini/config/projects"), f"{sim.project_id}.json")
        # Force re-registration of the project config file to ensure daemon visibility
        sim.register_existing_directory(sim.temp_path)

    # -------------------------------------------------------------------------
    # STAGE: blueprint
    # -------------------------------------------------------------------------
    if stage == "blueprint":
        sim.log_info("\n>>> STAGE: BLUEPRINT...")
        blueprint = fixture["blueprint_inputs"]
        conv_id = sim.new_conversation("Phase 1 - Project Blueprint")
        sim.send_message(conv_id, "/blueprint")
        sim.send_message(conv_id, blueprint["objective"])
        sim.send_message(conv_id, blueprint["tech_stack"])
        sim.send_message(conv_id, blueprint["breakdown"])
        sim.send_message(conv_id, "yes, write the blueprint docs/PROJECT.md")

        # Assertions
        sim.wait_for_file("docs/PROJECT.md", contains_text="Core Objective")
        sim.assert_file_exists("docs/PROJECT.md", "Core Objective")
        sim.log_pass("Project Blueprint created successfully.")

        return

    # -------------------------------------------------------------------------
    # STAGE: specs
    # -------------------------------------------------------------------------
    elif stage == "specs":
        sim.log_info("\n>>> STAGE: SPECS...")
        assertions = fixture["assertions"]
        conv_id = sim.new_conversation("Phase 2.1 - Feature Specification")
        sim.send_message(conv_id, "/spec-feature")
        sim.send_message(conv_id, f"{epic_slug}/{feature_slug}")
        sim.send_message(conv_id, specs["discovery_input"])
        sim.send_message(conv_id, "yes, write the spec files to disk")

        # Assertions
        spec_root = f"docs/sdd/{epic_slug}/{feature_slug}"
        sim.wait_for_file(f"{spec_root}/SPEC.md", contains_text=assertions["spec_contains"])
        sim.wait_for_file(f"{spec_root}/DESIGN.md", contains_text=assertions["design_contains"])
        sim.wait_for_file(f"{spec_root}/TASKS.md", contains_text=assertions["tasks_contains"])
        sim.assert_file_exists(f"{spec_root}/SPEC.md", assertions["spec_contains"])

        # Commit specs to git history
        subprocess.run(["git", "add", "."], cwd=sim.temp_path)
        subprocess.run(["git", "commit", "-m", "formal specifications compiled", "-q"], cwd=sim.temp_path)
        sim.log_pass("Feature specifications committed.")

        return

    # -------------------------------------------------------------------------
    # STAGE: worktree
    # -------------------------------------------------------------------------
    elif stage == "worktree":
        sim.log_info("\n>>> STAGE: WORKTREE...")
        if os.path.exists(worktree_path):
            sim.log_info("Cleaning pre-existing worktree residues...")
            subprocess.run(["git", "worktree", "remove", "--force", worktree_path], cwd=sim.temp_path, capture_output=True)
            subprocess.run(["git", "branch", "-D", worktree_slug], cwd=sim.temp_path, capture_output=True)

        conv_id = sim.new_conversation("Phase 2.2 - Feature Implementation")
        sim.send_message(conv_id, "/start-feature")
        res = sim.send_message(conv_id, f"{epic_slug}/{feature_slug}")

        # Extract Coder conv ID
        import re
        json_str = json.dumps(res)
        match = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', json_str)
        if not match:
            sim.log_fail(f"Could not find coder conversation ID in response: {json_str}")
        coder_conv_id = match.group(0)
        sim.log_info(f"Extracted coder conversation ID: {coder_conv_id}")

        if not os.path.isdir(worktree_path):
            sim.log_fail(f"Worktree directory was not created: {worktree_path}")
        sim.log_pass("Git worktree created successfully.")

        return

    # -------------------------------------------------------------------------
    # STAGE: implement
    # -------------------------------------------------------------------------
    elif stage == "implement":
        sim.log_info("\n>>> STAGE: IMPLEMENTATION...")
        assertions = fixture["assertions"]

        # Run direct file assertions inside the current directory (the worktree folder)
        for c_file in assertions["code_files"]:
            sim.assert_file_exists(os.path.join(worktree_path, c_file))

        if not os.path.isdir(os.path.join(worktree_path, ".venv")):
            sim.log_fail("Python virtualenv was not created by the Coder.")
        sim.log_info("INFO: Python virtualenv exists.")

        # Run tests inside the active worktree directory
        pytest_bin = os.path.join(worktree_path, ".venv", "bin", "pytest")
        sim.log_info("Running generated test suite...")
        test_suite = assertions.get("test_suite", f"tests/test_{feature_slug.replace('ft-', '').replace('-', '_')}.py")
        test_run = subprocess.run([pytest_bin, test_suite], cwd=worktree_path, capture_output=True, text=True)
        print(test_run.stdout)
        if test_run.returncode != 0:
            sim.log_fail(f"Coder test suite failed. Stderr:\n{test_run.stderr}")
        sim.log_pass("All coder-generated tests passed cleanly!")
        return

    # -------------------------------------------------------------------------
    # STAGE: close
    # -------------------------------------------------------------------------
    elif stage == "close":
        sim.log_info("\n>>> STAGE: CLOSE...")
        conv_id = sim.new_conversation("Phase 2.3 - Feature Close")
        sim.send_message(conv_id, "/close-feature")
        sim.send_message(conv_id, f"{epic_slug}/{feature_slug}")

        if os.path.exists(worktree_path):
            sim.log_fail("Worktree folder was not dismantled.")
        
        sim.log_pass("Worktree sandbox dismantled cleanly.")

        # Final cleanup (only cleans config JSON in standalone mode)
        if not active_project_id:
            sim.cleanup()
        
        if os.path.exists(worktree_path):
            subprocess.run(["rm", "-rf", worktree_path])

        sim.log_info("E2E Simulation Pipeline completed successfully.")
        return

if __name__ == "__main__":
    main()
