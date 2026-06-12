#!/usr/bin/env python3
#
# E2E Scenario: Architect Vision Interview and Blueprint Generation
#

import os
import shutil
import subprocess
from sdd_simulator import SDDSimulator

def main():
    sim = SDDSimulator("simulated-blueprint-project")
    
    # 1. Setup workspace
    sim.setup_workspace()
    
    # 2. Copy rules templates into the workspace to simulate a bootstrapped state
    sim.log_info("Seeding rules templates to simulate bootstrapped workspace...")
    templates_src = os.path.join(sim.workspace_dir, "workspace", "templates", "sdd-anchored", "_agents")
    if not os.path.isdir(templates_src):
        templates_src = os.path.join(sim.workspace_dir, ".agents")
    shutil.copytree(
        templates_src,
        os.path.join(sim.temp_path, ".agents"),
        dirs_exist_ok=True
    )
    # Commit these template rules
    subprocess.run(["git", "add", "."], cwd=sim.temp_path)
    subprocess.run(["git", "commit", "-m", "simulate bootstrap done", "-q"], cwd=sim.temp_path)

    try:
        # 3. Start Blueprint creation conversation
        conv_id = sim.new_conversation("/blueprint Phase 1 - Project Blueprint")
        
        # 4. Playback Architect Vision Interview answers
        sim.log_info("Answering Question 1: Core Objective...")
        sim.send_message(conv_id, "A generative guestbook web application where users can submit guest entries (name, comment) via an HTML form, saved to a simple JSON file database, with a generative AI summary of all comments.")
        
        sim.log_info("Answering Question 2: Tech Stack...")
        sim.send_message(conv_id, "Python (Flask), HTML5, JSON database backend.")
        
        sim.log_info("Answering Question 3: Epics and Features Breakdown...")
        breakdown_text = """
* Epic: ep-guest-submissions
  * Feature: ft-submission-form
* Epic: ep-generative-summary
  * Feature: ft-summary-engine
"""
        sim.send_message(conv_id, breakdown_text)
        
        # 5. Playback confirmation to write the blueprint
        sim.log_info("Confirming blueprint generation...")
        sim.send_message(conv_id, "yes, write the blueprint docs/PROJECT.md")

        # 6. Assertions
        sim.log_info("Verifying generated outputs...")
        sim.assert_file_exists("docs/PROJECT.md", "A generative guestbook web application")
        sim.assert_file_exists("docs/PROJECT.md", "ep-guest-submissions")
        sim.assert_file_exists("docs/PROJECT.md", "ft-submission-form")
        
        # Check that Epic/Feature directory capsules are scaffolded
        sim.assert_file_exists("docs/sdd/ep-guest-submissions/ft-submission-form/SPEC.md")
        sim.assert_file_exists("docs/sdd/ep-guest-submissions/ft-submission-form/DESIGN.md")
        sim.assert_file_exists("docs/sdd/ep-guest-submissions/ft-submission-form/TASKS.md")
        
    finally:
        sim.cleanup()
        
    print("")
    print("\033[1;32m====================================\033[0m")
    print("\033[1;32m SCENARIO 2 (BLUEPRINT) PASSED       \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
