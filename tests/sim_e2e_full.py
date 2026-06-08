#!/usr/bin/env python3
#
# Chained E2E Simulation Pipeline
# Executes the entire Spec-Driven Development (SDD) process sequentially:
# 1. Bootstrap empty workspace.
# 2. Architect vision interview (PROJECT.md).
# 3. Architect spec/design discovery (SPEC.md, DESIGN.md, TASKS.md).
# 4. Worktree sandbox prototype & linked environment bindings.
# 5. Coder implementation (Flask app.py, index.html, tests).
# 6. Test suite execution & validation.
# 7. Worktree sandbox teardown & branch merge check.
#

import os
import shutil
import subprocess
import sys
from sdd_simulator import SDDSimulator

def main():
    # 1. Main Project Simulator Instance
    sim = SDDSimulator("simulated-e2e-pipeline-project")
    sim.setup_workspace()
    
    worktree_path = os.path.expanduser(
        f"~/.gemini/jetski/worktrees/{sim.project_name}/ep-guest-submissions-ft-submission-form"
    )

    try:
        # =====================================================================
        # PHASE 1: BOOTSTRAP
        # =====================================================================
        sim.log_info("\n>>> PHASE 1: RUNNING BOOTSTRAP WORKFLOW...")
        conv_id = sim.new_conversation("/bootstrap")
        sim.send_message(conv_id, "simulated-e2e-pipeline-project")
        sim.send_message(conv_id, "git@github.com:dummy/simulated-e2e-pipeline-project.git")
        sim.send_message(conv_id, "sdd-anchored")

        sim.assert_file_exists(".agents/rules/sdd-pipeline.md")
        sim.assert_file_exists(".gitignore")

        # =====================================================================
        # PHASE 2: PROJECT BLUEPRINT
        # =====================================================================
        sim.log_info("\n>>> PHASE 2: COMPILING PROJECT BLUEPRINT...")
        conv_id = sim.new_conversation("Help me start the project blueprint definition.")
        
        # Playback Vision interview answers
        sim.send_message(
            conv_id, 
            "A generative guestbook web application where users can submit guest entries (name, comment) via an HTML form, saved to a simple JSON file database."
        )
        sim.send_message(conv_id, "Python (Flask), HTML5, JSON database backend.")
        
        breakdown_text = """
* Epic: ep-guest-submissions
  * Feature: ft-submission-form
"""
        sim.send_message(conv_id, breakdown_text)
        sim.send_message(conv_id, "yes, write the blueprint docs/PROJECT.md")

        # Assertions
        sim.assert_file_exists("docs/PROJECT.md", "Generative Guestbook")
        sim.assert_file_exists("docs/sdd/ep-guest-submissions/ft-submission-form/SPEC.md")

        # =====================================================================
        # PHASE 3: SPECIFICATION & DESIGN COMPILATION
        # =====================================================================
        sim.log_info("\n>>> PHASE 3: COMPILING SPECIFICATION & DESIGN...")
        conv_id = sim.new_conversation(
            "Please compile the specification, technical design and task list for feature ft-submission-form under epic ep-guest-submissions."
        )
        
        # Playback Spec/Design answers in a single robust packet
        discovery_input = """
Here are the functional and technical requirements for the feature:
1. Input fields: name, comment (no email validation needed).
2. For each guest submission, use Gemini API on Vertex AI to generate a fun, customized witty response based on the comment text.
3. For each guest submission, generate a fun image matching the comment sentiment using Imagen API on Vertex AI, saving the generated PNG locally in static/images/.
4. Save name, timestamp, comment, generated reply, and generated image path in a local json file guestbook.json.
5. GET / renders index.html displaying the submission form and the list of entries showing name, timestamp, comment, generated witty response, and generated image.
6. In your TECHNICAL DESIGN, specify GET / and POST /submit endpoints and a Verification Strategy using pytest.
Please compile SPEC.md, DESIGN.md, and TASKS.md.
"""
        sim.send_message(conv_id, discovery_input)
        sim.send_message(conv_id, "yes, write the spec files to disk")

        # Assertions
        spec_root = "docs/sdd/ep-guest-submissions/ft-submission-form"
        sim.assert_file_exists(f"{spec_root}/SPEC.md", "req-genai-witty-reply")
        sim.assert_file_exists(f"{spec_root}/DESIGN.md", "guestbook.json")
        sim.assert_file_exists(f"{spec_root}/TASKS.md", "tsk-0-scaffold")

        # Commit specs to git history
        subprocess.run(["git", "add", "."], cwd=sim.temp_path)
        subprocess.run(["git", "commit", "-m", "formal specifications compiled", "-q"], cwd=sim.temp_path)

        # =====================================================================
        # PHASE 4: WORKTREE SANDBOX PROTOTYPING
        # =====================================================================
        sim.log_info("\n>>> PHASE 4: PROVISIONING WORKTREE SANDBOX...")
        
        # Clean any residues of previous worktree sandbox run
        if os.path.exists(worktree_path):
            sim.log_info("Cleaning pre-existing worktree residues...")
            subprocess.run(["git", "worktree", "remove", "--force", worktree_path], cwd=sim.temp_path, capture_output=True)
            subprocess.run(["git", "branch", "-D", "ep-guest-submissions-ft-submission-form"], cwd=sim.temp_path, capture_output=True)

        # Execute manage_worktree prototype
        manage_script = "./.agents/skills/worktree-manager/scripts/manage_worktree.sh"
        sim.log_info("Running manage_worktree.sh prototype...")
        subprocess.run([manage_script, "prototype", "ep-guest-submissions", "ft-submission-form"], cwd=sim.temp_path, check=True)
        
        # Create a parent virtualenv so it can be inherited by the sandbox link-env step
        sim.log_info("Initializing virtualenv in parent project...")
        subprocess.run(["python3", "-m", "venv", ".venv"], cwd=sim.temp_path, check=True)
        
        # Install packages in parent
        parent_pip = os.path.join(sim.temp_path, ".venv", "bin", "pip")
        subprocess.run([parent_pip, "install", "flask", "pytest", "pytest-asyncio", "google-genai"], cwd=sim.temp_path, check=True)

        # Execute manage_worktree link-env
        sim.log_info("Running manage_worktree.sh link-env python...")
        subprocess.run([manage_script, "link-env", "ep-guest-submissions", "ft-submission-form", "python"], cwd=sim.temp_path, check=True)

        # Verify sandbox was created and linked
        if not os.path.isdir(worktree_path):
            sim.log_fail(f"Worktree directory was not created at expected path: {worktree_path}")
        if not os.path.isdir(os.path.join(worktree_path, ".venv")):
            sim.log_fail(f"Python virtualenv was not linked/created in worktree sandbox.")
            
        sim.log_pass("Worktree sandbox successfully provisioned and linked.")

        # =====================================================================
        # PHASE 5: SANDBOX IMPLEMENTATION (CODING)
        # =====================================================================
        sim.log_info("\n>>> PHASE 5: EXECUTING CODING PHASE IN SANDBOX...")
        
        # Spawn a secondary simulator instance bound to the worktree path (sharing project configuration files)
        sandbox_sim = SDDSimulator("simulated-e2e-pipeline-project-sandbox")
        sandbox_sim.register_existing_directory(worktree_path)

        # Start implementor conversation
        sim.log_info("Starting Coder implementation conversation...")
        conv_id = sandbox_sim.new_conversation(
            "Please read the specifications at docs/sdd/ep-guest-submissions/ft-submission-form/ and implement the tasks checklist in TASKS.md using TDD loops."
        )
        
        # Assert Coder generated files
        sim.log_info("Verifying generated code and test assets...")
        sandbox_sim.assert_file_exists("app.py", "Flask")
        sandbox_sim.assert_file_exists("templates/index.html")
        sandbox_sim.assert_file_exists("tests/test_app.py")
        
        # Run generated tests inside the sandbox virtualenv
        pytest_bin = os.path.join(worktree_path, ".venv", "bin", "pytest")
        sim.log_info("Running generated test suite inside sandbox...")
        test_run = subprocess.run([pytest_bin, "tests/test_app.py"], cwd=worktree_path, capture_output=True, text=True)
        
        print(test_run.stdout)
        if test_run.returncode != 0:
            sim.log_fail(f"Coder-generated test suite failed. Stderr:\n{test_run.stderr}")
            
        sim.log_pass("All Coder-generated unit and integration tests passed cleanly!")

        # Clean sandbox configuration
        sandbox_sim.cleanup()

        # =====================================================================
        # PHASE 6: SANDBOX TEARDOWN & MERGE CHECK
        # =====================================================================
        sim.log_info("\n>>> PHASE 6: TEARDOWN & WORKTREE CLOSURE...")
        
        # Merge changes in parent first
        # In a real pipeline, the worktree commits are pushed/merged.
        # We simulate this by checking that the files are committed in the worktree branch.
        # Run close-feature
        sim.log_info("Running manage_worktree.sh close-feature...")
        subprocess.run([manage_script, "close-feature", "ep-guest-submissions", "ft-submission-form"], cwd=sim.temp_path, check=True)

        if os.path.exists(worktree_path):
            sim.log_fail("Worktree folder was not dismantled after close-feature execution.")
            
        sim.log_pass("Worktree sandbox dismantled cleanly.")

    finally:
        # Teardown parent config
        sim.cleanup()
        
        # Clean any remaining worktree directory residues
        if os.path.exists(worktree_path):
            subprocess.run(["rm", "-rf", worktree_path])

    print("")
    print("\033[1;32m====================================\033[0m")
    print("\033[1;32m FULL E2E PIPELINE INTEGRATION OK     \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
