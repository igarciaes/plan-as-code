# Agent Instructions

This repository defines the Plan as Code (PaC) specification and reference artifacts.

## Roles of artifacts

| Path | Role |
|------|------|
| `SPEC.md` | Normative PaC v0.4.0 protocol |
| `SKILL.md` | Portable agent skill; conformant with the Agent Skills spec |
| `AGENTS.md` | Repository instructions (this file) |
| `.plan/` | Plan and task storage layout |
| `examples/` | Non-normative reference plan and task records |
| `schemas/plan.schema.json` | Optional validation support for plan records |
| `schemas/task.schema.json` | Optional validation support for task records |
| `conformance/` | Valid and invalid protocol conformance fixtures |
| `tools/validate.py` | Dependency-free invariant validator (SPEC §17) |
| `tests/` | Automated tests for the validator and conformance fixtures |
| `CHANGELOG.md` | Release history (Keep a Changelog) |
| `LICENSE` | MIT — © 2026 igarciaes and contributors |

## Source of truth

`SPEC.md` is the normative source for PaC v0.4.0. When any other artifact conflicts with it, `SPEC.md` wins. Examples, the skill, and the schemas are derived and must stay consistent.

## Role Selection

1. Determine the operation you are performing: Plan, Implement, or Verify.
2. Confirm which role you are assigned for that operation.
3. Read `SPEC.md` and `.plan/README.md` before acting.
4. Identify your ownership boundary before writing anything.
5. Do not combine roles in a way that collapses ownership boundaries within a single operation.

## Planner Rules

- An agent acting as Planner owns `.plan/plans/` and the planning and verification sections of Task records.
- Record the objective, scope, constraints, tasks, dependencies, and Definition of Done in the canonical records.
- Create and maintain Tasks under `.plan/tasks/`.
- Evaluate completed implementation against the Task Definition of Done.
- Mark Tasks as `Verified` only after the Definition of Done is satisfied.
- Mark Plans as `Completed` only when all required Tasks are `Verified`.
- Record the reason when verification fails and mark the Task `Changes Requested`.
- Preserve stable IDs.
- Do not modify implementation merely to satisfy the plan.
- Do not execute implementation tasks.

## Implementer Rules

- An agent acting as Implementer owns repository implementation artifacts (`src/`, `tests/`, `docs/`, ...) and the implementation, evidence, and lifecycle-state sections of Task records.
- Read the complete canonical Plan before starting implementation.
- Implement only accepted, planner-owned tasks.
- Record implementation evidence (commit SHA, changed files, test command, test result) in the Task.
- Mark the Task `Implemented` when the work and evidence are complete.
- Do not change the objective.
- Do not change the Definition of Done.
- Do not mark a Task as `Verified`.
- Do not authoritatively modify Planner verification.

## Ownership Rules

- Planner owns `.plan/plans/**` and the planning and verification sections of `.plan/tasks/**`.
- Implementer owns `src/**`, `tests/**`, `docs/**`, the repository-defined implementation paths, and the implementation and evidence sections of `.plan/tasks/**`.
- No role modifies another role's primary artifact or section.

## Plan Consumption

- An Implementer MUST read the complete Plan before starting implementation.
- An Implementer MUST consume the canonical Plan rather than infer requirements from discussion.
- Before operating, read `.plan/README.md` for the layout, ID formats, and active plans.
- Check task dependencies before starting work.

## Workflow

```text
Planner
   ↓
Plan and Tasks
   ↓
Implementer
   ↓
Implementation Evidence
   ↓
Planner
   ↓
Verified / Changes Requested
```

## Verification Rules

- Only the Planner MAY mark a Task as `Verified`.
- `Implemented` is not `Verified`.
- Verification evaluates the Task's Definition of Done.
- Failed verification MUST record the reason in the Task and mark it `Changes Requested`.
- A Plan MAY only become `Completed` when all required Tasks are `Verified`.

## Prohibited Actions

- Modifying another role's primary artifact or section.
- Changing the objective or Definition of Done.
- Marking a Task as `Verified` as the Implementer.
- Executing implementation Tasks as the Planner.
- Claiming verification without evidence.
- Changing stable IDs when wording or status changes.
- Introducing a database or requiring a central service for state.
- Duplicating Git history into event or iteration records.

## Working in this repository

- Prefer human-readable Markdown and platform-neutral language.
- Do not introduce requirements tied to a specific AI platform into the core specification.
- Work on `main`. Keep commits small and focused with concise, imperative messages (e.g. `docs:`, `feat:`, `fix:`).
- Review `git diff` before committing; stage only intended files; never commit secrets.

## Building and validating

This repository has no build step. Validation is manual plus a dependency-free test suite:

- run `python3 tools/validate.py --root .` to check protocol invariants (SPEC §17) against `.plan/`;
- run `python3 -m unittest discover -s tests` for the automated validator, schema, and conformance fixture tests;
- confirm `SPEC.md` is coherent and uses normative language;
- ensure `SKILL.md` stays aligned with `SPEC.md` and conformant with the Agent Skills spec (https://agentskills.io/specification), including valid `name`, `description`, and optional `license`/`metadata` frontmatter;
- keep examples consistent with normative format or workflow changes;
- validate examples against `schemas/plan.schema.json` and `schemas/task.schema.json` when applicable, using the Markdown-to-schema projection defined in `SPEC.md` §20.1;
- keep `conformance/` fixtures valid for their declared intent.

## Adopting PaC

When a repository uses Plan as Code, read its `.plan/README.md` when present for the plan layout, ID formats, controlled vocabulary, and active plans before operating.

## Change discipline

When changing a normative concept, update all affected artifacts together:

- `SPEC.md` — the normative protocol;
- `SKILL.md` — if agent behavior changes;
- `examples/` — if normative format or workflow changes;
- `schemas/` — if structured validation is affected;
- `CHANGELOG.md` — add an entry.

Do not change examples or the skill in a way that contradicts `SPEC.md`.

## Versioning and releases

- The version is tracked in `SPEC.md` (`## Version`) and `CHANGELOG.md`.
- Use Semantic Versioning and Keep a Changelog format.
- To release: commit the changes, add a dated `CHANGELOG.md` entry, create an annotated tag (`git tag -a vX.Y.Z -m "..."`), then push the branch and tag.