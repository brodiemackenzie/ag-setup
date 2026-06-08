# Actionable Tasks: Submission Form

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
