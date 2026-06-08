#!/usr/bin/env python3
#
# E2E Scenario: Project Manager Git Merge Conflict Resolution (Unhappy Path)
# Verifies that when a sandbox merge conflict occurs during branch closure,
# the sdd-project-manager agent uses the reconciliation playbook to run checks,
# clean markers, commit the resolved state, and successfully close the sandbox.
#

import os
import shutil
import subprocess
import sys
from sdd_simulator import SDDSimulator

def main():
    sim = SDDSimulator("simulated-conflict-project")
    
    # 1. Setup workspace (uses default strict sandbox permissions)
    sim.setup_workspace()
    
    # 2. Copy process rules & playbooks templates to `.agents`
    shutil.copytree(
        os.path.join(sim.workspace_dir, "workspace", "templates", "sdd-anchored", "_agents"),
        os.path.join(sim.temp_path, ".agents"),
        dirs_exist_ok=True
    )

    worktree_path = os.path.expanduser(
        f"~/.gemini/jetski/worktrees/{sim.project_name}/ep-guest-submissions-ft-submission-form"
    )
    manage_script = "./.agents/skills/worktree-manager/scripts/manage_worktree.sh"

    # 3. Create initial conflicting asset file in parent main branch
    sim.log_info("Creating initial base file in parent branch...")
    docs_dir = os.path.join(sim.temp_path, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    conflicted_file_path = os.path.join(docs_dir, "spec.md")
    with open(conflicted_file_path, "w") as f:
        f.write("objective: standard base guestbook\n")

    # Commit initial state in main
    subprocess.run(["git", "add", "."], cwd=sim.temp_path)
    subprocess.run(["git", "commit", "-m", "initial base commit", "-q"], cwd=sim.temp_path)

    # 4. Spawn the Git worktree branch sandbox
    sim.log_info("Provisioning Git worktree branch sandbox...")
    subprocess.run([manage_script, "prototype", "ep-guest-submissions", "ft-submission-form"], cwd=sim.temp_path, check=True)

    # Verify worktree folder exists
    if not os.path.isdir(worktree_path):
        sim.log_fail("Worktree folder was not provisioned correctly.")

    # 5. Create Parent Modifications (Main Branch)
    sim.log_info("Creating modifications in parent branch (main)...")
    with open(conflicted_file_path, "w") as f:
        f.write("objective: parent modified guestbook\n")
    subprocess.run(["git", "add", "."], cwd=sim.temp_path)
    subprocess.run(["git", "commit", "-m", "update base in main branch", "-q"], cwd=sim.temp_path)

    # 6. Create Sandbox Modifications (Feature Branch)
    sim.log_info("Creating conflicting modifications in sandbox feature branch...")
    sandbox_conflicted_file = os.path.join(worktree_path, "docs", "spec.md")
    with open(sandbox_conflicted_file, "w") as f:
        f.write("objective: sandbox modified guestbook\n")
    # Commit changes inside the sandbox feature branch
    subprocess.run(["git", "add", "."], cwd=worktree_path)
    subprocess.run(["git", "commit", "-m", "update spec in feature branch", "-q"], cwd=worktree_path)

    try:
        # 7. Trigger /close-feature workflow in the parent repository
        # This will fail on git merge due to conflicts, triggering the PM's reconciliation playbook.
        sim.log_info("Running /close-feature workflow in chat to resolve conflict...")
        conv_id = sim.new_conversation("/close-feature")
        sim.send_message(conv_id, "ep-guest-submissions/ft-submission-form")

        # 8. Physical Assertions on Merge Conflict Outcomes
        sim.log_info("Verifying Git conflict reconciliation outcomes...")
        
        # Verify sandbox was deleted
        if os.path.exists(worktree_path):
            sim.log_fail("Sandbox worktree folder was not dismantled after closing.")

        # Verify parent file does not contain conflict markers and has clean resolved content
        with open(conflicted_file_path, "r") as f:
            content = f.read()
            
        if "<<<<<<" in content or "=======" in content or ">>>>>>" in content:
            sim.log_fail(f"Conflict markers were not cleaned up. File content:\n{content}")
            
        # Assert the agent successfully merged the text
        if "modified guestbook" not in content:
            sim.log_fail(f"Merged file does not contain the resolved content. Content:\n{content}")
            
        sim.log_pass("Git conflict reconciliation playbook executed successfully! Conflict resolved and branch merged.")

    finally:
        # Cleanup
        sim.cleanup()
        if os.path.exists(worktree_path):
            subprocess.run(["rm", "-rf", worktree_path])

    print("")
    print("\033[1;32m====================================\033[0m")
    print("\033[1;32m SCENARIO 7 (CONFLICT RESOLUTION) OK \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
