# SDD Specification Writer Playbook

This playbook guides the `sdd-architect` agent through the transition from **Feature Proposal ➔ Functional Specification (SPEC.md)** inside an active Git worktree feature capsule.

---

## Objective
Compile a comprehensive, plain-English Functional Specification document defining the user journeys, business rules, and success criteria for a single actionable feature.

---

## The Spec Discovery Interview Protocol

Before drafting `SPEC.md`, the agent must gather precise business rules from the user:
1. **Targeted Spec Q&A**: Formulate **3-5 highly targeted, technical-functional questions** regarding the feature's user experience.
2. **Scope Focus**:
   * *Error Handling*: What should happen if an validation fails or a service is offline?
   * *UI/UX Flow*: What are the exact logical steps the user takes?
   * *Out-of-scope Elements*: What are the explicit boundaries that are *not* being implemented in this version?
3. **Halt for Input**: Present these questions to the user and halt execution. Do NOT generate the specification until the user provides input.

---

## Specification Document Structure

The resulting file must be saved at `docs/sdd/<epic-slug>/<feature-slug>/SPEC.md` inside the active worktree capsule, conforming to the following structure:

```markdown
# Specification: [Feature Title in Title Case]

## 1. Objective
A plain-English explanation of what the feature accomplishes, why it is being added, and the value it delivers.

## 2. User Journeys
A set of narrative step-by-step scenarios describing exactly how users interact with the system:
* **Scenario: [Scenario Name]**
  1. User performs Action A.
  2. System responds with Outcome B.
  3. User completes Action C.

## 3. User Requirements
Explicit, numbered functional rules that the implementation must enforce:
1. **Req-1 (Requirement Title)**: Detail of the functional rule.
2. **Req-2 (Requirement Title)**: Detail of the functional rule.

## 4. Success Criteria
Plain-English definitions of done mapping back to user verification:
* **Criteria-1**: When the user performs X, they must see Y.
```

---

## Banned Content Guidelines (Abstract Specs)

To prevent technical implementation details from polluting the functional specifications, the following content is **strictly forbidden** inside `SPEC.md`:
* **No Database Schemas or Column names**: Do not specify tables, columns, or database keys.
* **No API/REST Endpoints**: REST paths (e.g. `GET /api/v1/users`) and parameter payloads are prohibited.
* **No Code Blocks**: Fenced blocks of actual programming languages are banned.
