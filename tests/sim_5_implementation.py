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
    shutil.copytree(
        os.path.join(sim.workspace_dir, "workspace", "templates", "sdd-anchored", "_agents"),
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

    # 4. Seed the specifications for ep-guest-submissions/ft-submission-form
    sim.log_info("Seeding Guestbook specification documents...")
    
    project_md = """# Project Blueprint: Generative Guestbook
* Tech Stack: python, html, json
* Epics:
  * ep-guest-submissions
    * ft-submission-form
"""

    spec_md = """# Functional Specification: Submission Form

## 1. Objective
Implement a guestbook web app where visitors can submit comments. For each submission, the app uses generative AI to produce a fun customized reply and an image matching the comment's tone.

## 2. User Journeys
* **Submit Guestbook Entry**: Visitor enters their name and comment, then clicks Submit. The page reloads, showing their entry along with a witty AI response and a dynamically generated image.

## 3. Requirements
* **req-form-ui**: Simple HTML form with fields for `name` and `comment`.
* **req-genai-witty-reply**: Generate a fun, customized thank you response using the Gemini API based on the user's comment.
* **req-genai-image**: Construct a fun prompt, generate an image using Imagen, save it locally in `static/images/`, and display it next to the entry.
* **req-data-storage**: Store name, timestamp, comment, generated reply, and generated image file path in `guestbook.json`.
* **req-display**: Display all past entries on the home page in reverse chronological order.
"""

    design_md = """# Technical Design: Submission Form

## 1. Data Models & Schemas
### Database File: `guestbook.json`
Array of objects:
```json
[
  {
    "name": "Jane Doe",
    "comment": "Had an amazing weekend in the nature reserve!",
    "timestamp": "2026-06-08T12:00:00Z",
    "generated_comment": "Glad nature recharged you! Hope you didn't get chased by squirrels!",
    "image_path": "/static/images/jane_doe_17178888.png"
  }
]
```

## 2. API & Integration Contracts
### GET /
Renders index.html showing submission form and past guest entries.

### POST /submit
Parameters (Form POST): `name`, `comment`.
Calls Vertex AI Gemini and Imagen, saves image to `static/images/`, appends entry to `guestbook.json`, and redirects to `/`.

## 3. Verification Strategy
* Unit/Integration Tests (`tests/test_app.py`):
  * `test_home_page`: GET `/` returns 200.
  * `test_valid_submission`: POST `/submit` with valid parameters returns 302 redirect.
  * Mocks: Mock the `google.genai.Client` text and image generation calls to return stable mock responses and dummy image bytes, allowing hermetic offline testing.
"""

    tasks_md = """# Actionable Tasks: Submission Form

This document tracks the TDD implementation steps. Tasks must be checked off sequentially by the implementor.

---

## Epic: ep-guest-submissions (Guest Submissions)
## Feature: ft-submission-form (Submission Form)

---

## Gherkin BDD Checklist

- [ ] **tsk-0-scaffold ([Ref: Workspace Scaffolding] Initialize folder structure and Flask app)**
  * **Given** an empty repository
  * **When** Flask, pytest, and google-genai are installed and app.py is initialized
  * **Then** the server starts and running pytest returns success

- [ ] **tsk-1-genai-service ([Ref: AI Service] Implement Gemini & Imagen client bindings)**
  * **Given** a GenAI helper service module
  * **When** called with a guest comment
  * **Then** returns a fun thank-you string and generates/saves a local PNG file

- [ ] **tsk-2-routes ([Ref: Flask Routes] Implement GET and POST routes)**
  * **Given** a local guestbook.json persistence file
  * **When** GET / or POST /submit are requested
  * **Then** entries are successfully read or appended with generated AI fields

- [ ] **tsk-3-ui ([Ref: HTML Form] Create frontend template templates/index.html)**
  * **Given** the Flask server
  * **When** GET / is requested
  * **Then** templates/index.html is rendered containing input fields, past entries, AI replies, and generated images
"""

    docs_dir = os.path.join(sim.temp_path, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    with open(os.path.join(docs_dir, "PROJECT.md"), "w") as f:
        f.write(project_md)
        
    spec_dir = os.path.join(docs_dir, "sdd", "ep-guest-submissions", "ft-submission-form")
    os.makedirs(spec_dir, exist_ok=True)
    with open(os.path.join(spec_dir, "SPEC.md"), "w") as f:
        f.write(spec_md)
    with open(os.path.join(spec_dir, "DESIGN.md"), "w") as f:
        f.write(design_md)
    with open(os.path.join(spec_dir, "TASKS.md"), "w") as f:
        f.write(tasks_md)

    # Commit initial spec state
    subprocess.run(["git", "add", "."], cwd=sim.temp_path)
    subprocess.run(["git", "commit", "-m", "seed guestbook specifications", "-q"], cwd=sim.temp_path)

    try:
        # 5. Start implementor conversation
        sim.log_info("Starting Implementor agent coding flow...")
        # Instruct the agent to read the spec and implement the feature
        conv_id = sim.new_conversation(
            "Please read the specifications at docs/sdd/ep-guest-submissions/ft-submission-form/ and implement the tasks checklist in TASKS.md."
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
