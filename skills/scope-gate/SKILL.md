---
name: scope-gate
description: Close delivery scope with Goal, Inputs / Outputs, Must do, Won't do, and Acceptance before ADRs, tickets, estimates, or implementation. Use for pre-build scope clarification, delivery boundary checks, or requests to create a SCOPE.md baseline.
metadata:
  short-description: Close delivery scope before implementation
---

# Scope Gate

Turn a delivery request into a closed five-field scope card. The card is the handoff baseline for later design and execution. Scope Gate publishes that baseline and stops.

## Operating boundary

- Produce only the five scope sections and their version metadata.
- Stop before ADRs, technical designs, ticket breakdowns, estimates, project plans, or implementation.
- Put solution choices, sequencing, and staffing outside the scope card.
- Use only information present in the request or verified workspace materials.
- Ask before treating a scope-changing unknown as settled.

## Workflow

1. Inspect the request and relevant workspace files. If `SCOPE.md` already exists, read it before deciding whether to update it.
2. Identify unknowns that would change the goal, inputs, outputs, required work, exclusions, or acceptance baseline. Ignore questions that would not change those fields.
3. If scope-changing information is missing, ask all necessary questions in one round using the question protocol below. Stop until the user answers.
4. Draft the card with the five headings and content rules below.
5. Run the completion gate. Revise the draft until every check passes.
6. Write or update `<workspace>/SCOPE.md` using the artifact contract below.
7. Return the five-field card in the user's language. Keep the five English headings unchanged.

## Question protocol

Every question must include:

1. **Brief analysis**: the missing fact and the specific scope field it changes.
2. **Options**: two to four mutually exclusive, executable choices labeled `A` through `D`.
3. **Recommendation**: one option and a one-sentence reason.

Use this shape and translate the labels into the user's language when appropriate:

```markdown
### Question 1: <specific decision>

**Brief analysis:** <gap and affected scope field>

**Options**

- A. <choice>
- B. <choice>
- C. <optional choice>

**Recommendation:** A. <reason>
```

Do not ask generic discovery questions. Ask only when the answer changes the scope baseline.

## Five fields

Keep the headings exactly as written and in this order.

### Goal

State one observable delivery outcome and its boundary. Describe the result, not the implementation.

### Inputs / Outputs

List the available or required inputs first, then the deliverables, their formats, and their finished state. Do not invent paths, access, data, interfaces, or approvals.

### Must do

List the smallest set of obligations required to achieve the goal. Each item must be independently judgeable as complete. Exclude execution steps and task ownership.

### Won't do

Name adjacent work that could reasonably be mistaken for part of this delivery. The scope is closed: omitted work is not implicitly included.

### Acceptance

Give observable, reproducible pass conditions and their evidence. Map every `Must do` item to at least one condition. Replace subjective terms with a check that another person could run.

## Completion gate

Confirm all of the following before writing the file:

- The card contains exactly the five required sections in the required order.
- The goal, required work, exclusions, and acceptance conditions do not contradict one another.
- Every `Must do` item has observable acceptance evidence.
- Every input and output has a source or delivery state that is clear from the request.
- No unresolved scope-changing uncertainty remains in the card.
- The card contains no ADR, technical design, task breakdown, estimate, schedule, or implementation.

If a check fails, ask a protocol-compliant question or leave the file unchanged.

## Workspace artifact

Write the result to `SCOPE.md` in the current workspace root. Use this structure:

```markdown
# Scope: <short name>

- Version: V<major>.<minor>
- First created: YYYY-MM-DD HH:mm
- Updated: YYYY-MM-DD HH:mm

## Goal

...

## Inputs / Outputs

...

## Must do

...

## Won't do

...

## Acceptance

...
```

Apply versioning as follows:

- Use `V1.0` for a new scope, with the same current local time in both timestamp fields.
- Use `V1.1` for clarifications that preserve the goal, required-work baseline, and acceptance baseline. Keep `First created` and update `Updated`.
- Before changing the goal, required-work baseline, or acceptance baseline, ask for explicit confirmation using the question protocol. Then increment the major version, such as `V2.0`, and update `Updated`.
- If an existing `SCOPE.md` belongs to a different delivery, ask whether to replace it. Do not overwrite it before confirmation.
- Keep the file limited to the metadata block and the five required sections.
