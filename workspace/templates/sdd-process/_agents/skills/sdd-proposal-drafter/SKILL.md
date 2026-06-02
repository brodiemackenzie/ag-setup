# SDD Proposal Drafter Playbook

This playbook guides the `sdd-architect` agent through the conversational interview and drafting phase that transitions raw project ideas into a high-level system blueprint.

---

## Objective
Analyze high-level conversational requirements, establish initial architectural pillars and tech stack selections, and inventory the Epics and Features required to deliver the project.

---

## The Conversation Interview Protocol

When executing this skill, the agent must conduct a structured, conversational interview:
1. **Avoid Questionnaire Dumps**: Do NOT ask a long list of questions at once. Ask **one question at a time** and wait for user feedback.
2. **Focus on the Core**:
   * *What is the main objective of this system?* (The essence of the system)
   * *What is the target tech stack or framework preference?* (e.g., Next.js, Python FastAPIs, Rust)
   * *What are the key functional blocks / milestones?*
3. **Synthesize Context**: Actively suggest tech choices and epic layouts based on your software engineering knowledge, rather than expecting the user to know everything.

---

## Proposal Document Structure

The resulting file must be saved at `docs/proposals/<project_name>_proposal.md` (relative to the top-level project) and must strictly conform to the following structure:

```markdown
# Project Proposal: [Project Name]

## 1. Executive Summary
A concise, high-level summary of the project's objective, target value, and core functionality.

## 2. Tech Stack & Architecture Pillars
List the selected frameworks, databases, and libraries. Outline the core design patterns:
* **Core Language/Framework**: e.g., Python 3.11 + FastAPI
* **Persistence Layer**: e.g., SQLite (local, in-memory for testing)
* **Key Libraries**: e.g., Pydantic for serialization, Pytest for tests

## 3. Epic & Feature Mapping Inventory
Define the high-level milestones (Epics) and actionable features. Every item must adhere to strict naming conventions:

### Epic: [Epic Slug in lowercase kebab-case] (Title in Capitalized Title Case)
*Description of the subsystem.*
* **Feature: [Feature Slug] (Title Case)**: Description of the incremental value.
* **Feature: [Feature Slug] (Title Case)**: Description.

### Epic: [Epic Slug] (Title Case)
*Description of the subsystem.*
* **Feature: [Feature Slug] (Title Case)**: Description.
```

---

## Banned Content Guidelines

To prevent architectural drift and over-specification during the raw vision phase, the following content is **strictly forbidden** inside the proposal document:
* **No Database Schemas**: Do not write table schemas, keys, or column types.
* **No API contracts**: Do not list REST endpoint paths or JSON payload structures.
* **No User Journeys**: Do not detail user navigation clicks or UI inputs.
* **No Code Blocks**: Actual programming code blocks (Python, Go, etc.) are prohibited.
