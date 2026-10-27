# Scope Gate

**Close the scope before the code.**

[简体中文](README.zh-CN.md)

Scope Gate is a small Codex skill that turns a delivery request into a closed five-field scope card before implementation starts. It fixes the goal, inputs and outputs, required work, exclusions, and acceptance conditions in `SCOPE.md`, then stops at the design handoff.

![Scope Gate demo](docs/demo.gif)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skill: Codex](https://img.shields.io/badge/Skill-Codex-111827.svg)](https://developers.openai.com/codex/skills/)
[![Scope fields: 5](https://img.shields.io/badge/Scope_fields-5-0f766e.svg)](skills/scope-gate/SKILL.md)

## Why Scope Gate

Requirements often expand between the first prompt and the first commit. The model starts designing, splitting tickets, or writing code before the delivery boundary is settled. Scope Gate creates one compact checkpoint:

```text
request -> five-field scope -> SCOPE.md -> design and delivery
```

The value is not another document. It is a closed baseline that later work can be checked against.

- Five fixed fields keep the scope review short.
- Explicit exclusions expose adjacent work before it enters the delivery.
- Observable acceptance conditions prevent "done" from becoming subjective.
- A versioned `SCOPE.md` preserves the agreed baseline in the workspace.
- A hard stop keeps ADRs, tickets, estimates, and implementation out of scope review.

Scope Gate is deliberately narrow. It does not claim to replace requirements engineering, architecture review, or project management.

## Quick Start

Prerequisites: a Codex installation that supports skills. See the [Codex skills documentation](https://developers.openai.com/codex/skills/).

Copy the skill folder into your Codex skills directory:

```powershell
$source = Resolve-Path ".\skills\scope-gate"
$destination = Join-Path $env:USERPROFILE ".codex\skills\scope-gate"
Copy-Item -LiteralPath $source -Destination $destination -Recurse
```

If `CODEX_HOME` points to a custom directory, place the folder at `$CODEX_HOME\skills\scope-gate` instead. Restart or reload Codex if the new skill is not discovered immediately.

Invoke it explicitly:

```text
Use $scope-gate to scope this request before implementation.
```

The skill can also be selected when a request clearly needs delivery scope clarification.

## Example

Input:

```text
Add CSV import validation to the admin app so malformed customer files
are rejected before data is written.
```

Scope Gate produces the five-field card and writes it to `SCOPE.md`. See the complete [example scope](examples/SCOPE.md).

```markdown
## Goal

Reject malformed customer CSV files before any row is persisted.

## Inputs / Outputs

- Input: a customer CSV file and the documented import schema.
- Output: a validation result that identifies rejected rows and prevents partial writes.

## Must do

- Validate the file against the documented schema before persistence.

## Won't do

- Redesigning the import interface.

## Acceptance

- A malformed fixture produces a failed validation result and persists zero rows.
```

## Guardrails

| Field | Required content |
| --- | --- |
| `Goal` | One observable delivery outcome and its boundary |
| `Inputs / Outputs` | Available or required inputs and finished deliverables |
| `Must do` | The minimum required obligations |
| `Won't do` | Adjacent work explicitly excluded |
| `Acceptance` | Reproducible pass conditions for every required item |

The skill stops before ADRs, technical designs, ticket breakdowns, estimates, schedules, and implementation. If a user asks for one of those, that is a separate task.

Scope-changing questions use a fixed protocol: brief impact analysis, two to four mutually exclusive options, and one recommendation.

## Compatibility and Validation

Scope Gate follows the Codex skill layout:

```text
skills/scope-gate/
|-- SKILL.md
`-- agents/
    `-- openai.yaml
```

Repository checks:

```powershell
python tests/validate_scope.py
python -m unittest discover -s tests -v
```

The structural checks cover frontmatter, the frozen five-heading contract, metadata, example scope, routing fixtures, metadata file, and README assets. The package is also checked with OpenAI's `skill-creator` validation script. These checks do not prove model behavior in every runtime; live agent evaluation remains separate.

## Contributing

Keep changes aligned with the single purpose: close delivery scope, then stop.

A contribution should:

1. Preserve the five headings and their order.
2. Preserve the question protocol and versioning rules.
3. Add or update routing fixtures when invocation behavior changes.
4. Run both validation commands above.
5. Explain any change that strengthens or relaxes the stop boundary.

Feature expansion into ADRs, planning, estimates, or implementation is outside this project's scope.

## License

[MIT](LICENSE)
