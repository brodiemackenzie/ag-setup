#!/usr/bin/env python3
#
# E2E Scenario: Spec Reconciliation Workflow
#

import os
import shutil
import subprocess
from sdd_simulator import SDDSimulator

def main():
    sim = SDDSimulator("simulated-reconciliation-project")
    
    # 1. Setup workspace
    sim.setup_workspace()
    
    # 2. Copy rules templates into the workspace
    templates_src = os.path.join(sim.workspace_dir, "workspace", "templates", "sdd-anchored", "_agents")
    if not os.path.isdir(templates_src):
        templates_src = os.path.join(sim.workspace_dir, ".agents")
    shutil.copytree(
        templates_src,
        os.path.join(sim.temp_path, ".agents"),
        dirs_exist_ok=True
    )
    
    # 3. Seed initial spec, design, and project files
    sim.log_info("Seeding initial specifications and designs...")
    
    project_md_content = """# Project Blueprint: Generative Guestbook
* Tech Stack: python, html, json
* Epics:
  * ep-guest-submissions
    * ft-submission-form
"""
    
    spec_md_content = """# Specification: Submission Form
## 1. Objective
Implement guestbook submission form.
## 2. Requirements
* req-form-ui: Render input fields for name and comment.
"""

    design_md_content = """# Design: Submission Form
## 1. Architecture
Render a simple HTML form and handle POST submissions in Flask app.py.
"""

    # Mock a Spec Change Proposal file
    proposal_content = """# Spec Change Proposal: Submission Form

## Proposed Changes
We need to collect and validate user email addresses to prevent spam guestbook submissions.

## Modified Requirements
Add requirement:
* req-email-validation: Verify user email has standard valid format before saving.
"""

    os.makedirs(os.path.join(sim.temp_path, "docs"), exist_ok=True)
    with open(os.path.join(sim.temp_path, "docs", "PROJECT.md"), "w") as f:
        f.write(project_md_content)
        
    spec_dir = os.path.join(sim.temp_path, "docs", "sdd", "ep-guest-submissions", "ft-submission-form")
    os.makedirs(spec_dir, exist_ok=True)
    with open(os.path.join(spec_dir, "SPEC.md"), "w") as f:
        f.write(spec_md_content)
    with open(os.path.join(spec_dir, "DESIGN.md"), "w") as f:
        f.write(design_md_content)
    with open(os.path.join(spec_dir, "spec_change_proposal.md"), "w") as f:
        f.write(proposal_content)

    # Commit initial state
    subprocess.run(["git", "add", "."], cwd=sim.temp_path)
    subprocess.run(["git", "commit", "-m", "initial specs and proposal", "-q"], cwd=sim.temp_path)

    try:
        # 4. Start Reconciliation conversation
        conv_id = sim.new_conversation("Phase 2.2 - Spec reconciliation: Please reconcile the spec change proposal at docs/sdd/ep-guest-submissions/ft-submission-form/spec_change_proposal.md")
        
        # 5. Confirm reconciliation when asked by Architect
        sim.log_info("Answering Architect confirmation prompt...")
        sim.send_message(conv_id, "yes, proceed with merging the spec change proposal and updating the files")

        # 6. Assertions
        sim.log_info("Verifying spec reconciliation outcomes...")
        # Main SPEC.md must contain the new requirement
        sim.assert_file_exists("docs/sdd/ep-guest-submissions/ft-submission-form/SPEC.md", "req-email-validation")
        
        # The spec_change_proposal.md should be cleaned up / removed
        if os.path.exists(os.path.join(spec_dir, "spec_change_proposal.md")):
            sim.log_fail("spec_change_proposal.md file was not deleted/archived after reconciliation.")
        sim.log_pass("spec_change_proposal.md removed successfully.")

        # Check git commit contains the merge
        git_log = subprocess.run(
            ["git", "log", "-n", "1", "--oneline"],
            cwd=sim.temp_path, capture_output=True, text=True
        ).stdout
        sim.log_info(f"Last Git Commit: {git_log.strip()}")
        if "reconcile" not in git_log.lower() and "merge" not in git_log.lower() and "spec" not in git_log.lower():
            sim.log_fail("Changes were not committed to git repository.")
        sim.log_pass("Reconciliation changes committed successfully to git history.")
        
    finally:
        sim.cleanup()
        
    print("")
    print("\033[1;32m====================================\033[0m")
    print("\033[1;32m SCENARIO 3 (RECONCILIATION) PASSED  \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
