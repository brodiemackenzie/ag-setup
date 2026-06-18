# SDD Project Blueprint Playbook

This playbook guides the `sdd-architect` agent through the conversational interview and drafting phase that transitions raw project ideas into a root-level guiding document (`PROJECT.md`).

---

## Objective
Conduct a high-level conversational interview to capture the project's core objective, target audience, success criteria, features, out-of-scope boundaries, tech stack, and Epic/Feature component breakdown. Compile these results into `PROJECT.md` at the project's root level to serve as the master guidance file.

---

## The Conversation Interview Protocol

When executing this skill, the agent must conduct a structured, conversational interview:
0. **Plan-First Alignment (CRITICAL)**: Before conducting the interview or drafting files, compile a Plan Asset outlining the scope of the interview, present it to the user in chat, and explicitly request feedback.
1. **Avoid Questionnaire Dumps**: Do NOT ask a long list of questions at once. Ask **one question at a time** and wait for user feedback.
2. **Focus on the Core**:
   * *What is the main objective of this system?*
   * *Who is the target audience, and what are the key success metrics?*
   * *What are the key functional features we must deliver?*
   * *What is explicitly out of scope for this phase?*
   * *What are the preferred tech stack languages, frameworks, or databases?*
3. **Synthesize Context**: Actively suggest stack components and epic layouts based on your software engineering knowledge, rather than expecting the user to provide all details.

---

## PROJECT.md Document Structure

The resulting file must be saved in the project's documentation folder (`docs/PROJECT.md`) and must strictly conform to the following structure:

```markdown
---
Approval Status: PROPOSED
Approved By: [User LDAP]
Date: [YYYY-MM-DD]
---

# Project Proposal: [Project Title in Capitalized Title Case]

[A concise, high-level summary paragraph describing the system scope and core delivery value.]

## 1. Core Objective
[Clear explanation of the system's target purpose and dynamic execution logic.]

## 2. Target Audience & Success Criteria
- **Target Audience**: [List of users, developers, or roles target by the solution.]
- **Success Criteria**:
  - [Metric 1 (e.g., JIT Bootstrapping)]: [Measurable threshold, e.g., completes in < 1.5s]
  - [Metric 2 (e.g., Compatibility)]: [Integration parameters]

## 3. Core Features
- [Feature Block 1]: [Detailed explanation of key user-facing or backend capability.]
- [Feature Block 2]: [Detailed explanation.]

## 4. Out of Scope
- [Exclusion 1]: [Specific deferred component or boundary definition.]
- [Exclusion 2]: [Assumptions / integrations handled externally.]

## 5. High-Level Tech Stack
- **Frontend**: [Framework, styling conventions, libraries]
- **Backend**: [Languages, frameworks, target SDKs]
- **Data / Semantic Layer**: [Databases, query compilers, custom tools]
- **DevOps / Verification**: [Testing libraries, shell run scripts]

## 6. Epic / Feature Component Breakdown

### Epic: ep-[epic-slug-in-lowercase-kebab-case] ([Epic Title in Title Case])
[Brief description of this epic component/subsystem's role.]
* **Feature: ft-[feature-slug-in-lowercase-kebab-case] ([Feature Title in Title Case])**: [Explanation of the incremental feature value.]
* **Feature: ft-malloy-mcp (Malloy MCP Connection)**: [Example explanation.]

## 7. Open Questions
- [ ] [Open technical debate or decision item 1.]
- [ ] [Open technical debate or decision item 2.]
```

---

## Banned Content Guidelines

To prevent architectural drift and over-specification during the raw vision phase, the following content is **strictly forbidden** inside the `PROJECT.md` document:
* **No Database Schemas**: Do not write table schemas, keys, or column types.
* **No API contracts**: Do not list REST endpoint paths or JSON payload structures.
* **No User Journeys**: Do not detail user navigation clicks or UI inputs.
* **No Code Blocks**: Actual programming code blocks (Python, Go, etc.) are prohibited.
