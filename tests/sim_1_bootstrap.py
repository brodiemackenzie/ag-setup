#!/usr/bin/env python3
#
# E2E Scenario: Greenfield Project Bootstrapping
#

from sdd_simulator import SDDSimulator

def main():
    sim = SDDSimulator("simulated-bootstrap-project")
    
    # Setup fresh git workspace
    sim.setup_workspace()
    
    try:
        # Start bootstrap conversation
        conv_id = sim.new_conversation("/bootstrap")
        
        # Playback interview answers
        sim.send_message(conv_id, "simulated-bootstrap-project")
        sim.send_message(conv_id, "git@github.com:dummy/simulated-bootstrap-project.git")
        sim.send_message(conv_id, "sdd-anchored")
        
        # Assertions
        sim.assert_file_exists(".agents/rules/sdd-pipeline.md")
        sim.assert_file_exists(".gitignore")
        
        # Confirm that no tech boilerplate (requirements.txt) was pre-scaffolded
        import os
        if os.path.exists(os.path.join(sim.temp_path, "requirements.txt")):
            sim.log_fail("requirements.txt was pre-scaffolded by bootstrap.sh, violating empty spec-first bootstrap rules.")
        
    finally:
        sim.cleanup()
        
    print("")
    print("\033[1;32m====================================\033[0m")
    print("\033[1;32m SCENARIO 1 (BOOTSTRAP) PASSED       \033[0m")
    print("\033[1;32m====================================\033[0m")

if __name__ == "__main__":
    main()
