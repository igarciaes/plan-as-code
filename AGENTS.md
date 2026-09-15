# Agent Instructions

This repository defines the Plan as Code (PaC) specification and reference artifacts.

## Roles of artifacts

| Path | Role |
|------|------|
| `SPEC.md` | Normative PaC v0.5.0 protocol |
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

`SPEC.md` is the normative source for PaC v0.5.0. When any other artifact conflicts with it, `SPEC.md` wins. Examples, the skill, and the schemas are derived and must stay consistent.

## Roles, ownership, and operations

Roles, ownership boundaries, lifecycles, and the five operations (Draft a plan, Approve a plan, Implement a plan, Verify a plan, Complete a plan) are normative in `SPEC.md` (§3, §8, §9, §11–13, §18, §19). This repository does not redefine agent behavior; agents MUST follow `SPEC.md` as written. Before operating:

1. Determine the operation (Draft, Approve, Implement, Verify, or Complete) and the assigned role for it.
2. Read `.plan/README.md` for the layout, ID formats, controlled vocabulary, and active plans.
3. Read the applicable Plan and Task records.
4. Identify the ownership boundary (`SPEC.md` §13) before writing anything.
5. Perform exactly one operation per turn in the sequence Draft → Approve → Implement → Verify → Complete; do not chain or auto-continue into the next operation, and do not implement any Task before the Plan is `Planned`.

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