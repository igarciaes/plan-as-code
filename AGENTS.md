# Agent Instructions

This repository defines the Plan as Code (PaC) specification and reference artifacts.

## Roles of artifacts

| Path | Role |
|------|------|
| `SPEC.md` | Normative PaC v0.1.0 protocol |
| `SKILL.md` | Portable agent skill; conformant with the Agent Skills spec |
| `AGENTS.md` | Repository instructions (this file) |
| `.plan/` | Plan and feedback storage layout |
| `examples/` | Non-normative reference plan records |
| `schemas/plan.schema.json` | Optional validation support |
| `schemas/feedback.schema.json` | Optional validation support for feedback threads |
| `CHANGELOG.md` | Release history (Keep a Changelog) |
| `LICENSE` | MIT — © 2026 igarciaes and contributors |

## Source of truth

`SPEC.md` is the normative source for PaC v0.1.0. When any other artifact conflicts with it, `SPEC.md` wins. Examples, the skill, and the schema are derived and must stay consistent.

## Role Selection

1. Determine the operation you are performing: Plan, Implement, or Verify.
2. Confirm which role you are assigned for that operation.
3. Read `SPEC.md` and `.plan/README.md` before acting.
4. Identify your ownership boundary before writing anything.
5. Do not combine roles in a way that collapses ownership boundaries within a single operation.

## Planner Rules

- An agent acting as Planner owns `.plan/plans/`.
- Record the objective, scope, constraints, tasks, dependencies, and acceptance criteria in the canonical plan.
- Record canonical decisions in the plan.
- Evaluate feedback and record explicit decisions; do not let feedback silently change the plan.
- Preserve stable IDs.
- Do not modify implementation merely to satisfy the plan.
- Do not independently verify implementation you authored.
- Do not modify feedback authored by another role.

## Implementer Rules

- An agent acting as Implementer owns repository implementation artifacts (`src/`, `tests/`, `docs/`, ...).
- Read the complete canonical plan before starting implementation.
- Implement only accepted, planner-owned tasks.
- Record implementation evidence (for example commit SHA, changed files, test command, test result).
- Request clarification through feedback; do not infer requirements from discussion.
- Do not change the objective.
- Do not change acceptance criteria.
- Do not change planner-owned decisions.
- Do not mark implementation as independently verified.

## Verifier Rules

- An agent acting as Verifier owns verification outcomes.
- Independently evaluate repository artifacts against the plan's acceptance criteria.
- Record verification evidence (for example commands, test names, commit references).
- Report findings when verification fails.
- Determine verification status.
- Do not modify implementation merely to make verification pass.
- Do not redefine requirements.
- Do not change the original planning intent.

## Ownership Rules

- Planner owns `.plan/plans/**`.
- Feedback is append-only and author-owned.
- Implementer owns `src/**`, `tests/**`, `docs/**`, and any repository-defined implementation paths.
- Verifier owns verification outputs.
- No role modifies another role's primary artifact.

## Plan Consumption

- An Implementer MUST read the complete plan before starting implementation.
- An Implementer MUST consume the canonical plan rather than infer requirements from discussion.
- Before operating, read `.plan/README.md` for the layout, ID formats, and active plans.
- Check task dependencies before starting work.

## Feedback Rules

- Feedback is append-only communication associated with a task, a finding, or a plan.
- Append feedback as a new item with a new stable ID.
- Record the author role and date.
- Do not reorder existing feedback.
- Do not rewrite feedback authored by another role.
- Feedback does not modify the plan. The Planner records an explicit decision in the canonical plan.

## Verification Rules

- Only independent verification can produce `Verified`.
- Implemented is not Verified.
- Evaluate repository artifacts rather than rely solely on implementation claims.
- If verification fails, create a finding.
- A finding can generate feedback.

## Prohibited Actions

- Modifying another role's primary artifact.
- Changing acceptance criteria.
- Silently modifying the canonical plan in response to feedback.
- Rewriting feedback authored by another role.
- Reordering existing feedback items.
- Claiming verification without evidence.
- Marking your own implementation as independently verified.
- Changing stable IDs when wording or status changes.
- Introducing a database or requiring a central service for state.

## Working in this repository

- Prefer human-readable Markdown and platform-neutral language.
- Do not introduce requirements tied to a specific AI platform into the core specification.
- Work on `main`. Keep commits small and focused with concise, imperative messages (e.g. `docs:`, `feat:`, `fix:`).
- Review `git diff` before committing; stage only intended files; never commit secrets.

## Building and validating

This repository has no build step or automated test suite. Validation is manual:

- confirm `SPEC.md` is coherent and uses normative language;
- ensure `SKILL.md` stays aligned with `SPEC.md` and conformant with the Agent Skills spec (https://agentskills.io/specification), including valid `name`, `description`, and optional `license`/`metadata` frontmatter;
- keep examples consistent with normative format or workflow changes;
- validate examples against `schemas/plan.schema.json` and `schemas/feedback.schema.json` when applicable, using the Markdown-to-schema projection defined in `SPEC.md` §20.1.

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