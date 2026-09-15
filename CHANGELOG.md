# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.5.0] - 2026-09-15

### Changed

- `SKILL.md` now requires post-operation conformance verification after each operation: the Conformance checks section mandates that the agent confirms the produced records conform to `SPEC.md` (including running `tools/validate.py` and the schemas when tooling is present) before finishing a turn, and each of the five operation subsections lists its operation-specific post-operation conformance expectations. Skill `metadata.version` bumped to `0.6.2`.

- Review R002 accepted findings implemented. `SPEC.md` §3.3 and `README.md` rewrite the ownership prohibition as "A role MUST NOT modify another role's primary artifact or section" (`F001`). §9.10 adds outgoing transitions for `Blocked` (`→ In Progress`) and `Deferred` (`→ Planned`) and restricts the `Blocked`/`Deferred` source states to `Planned | In Progress | Implemented` so they cannot violate `INV-014` (`F002`, `F003`). §13.1 removes the undefined "Planner Decision" entry (`F004`). Plan-level Definition of Done is removed: stripped from the §6 template, the §20.1 projection, and `plan.schema.json`; completion stays Task-based (`F005`). §18.3, `SKILL.md`, and `README.md` replace the undefined "accepted Tasks" with "the Plan's Tasks" (`F007`). §8 lifecycle diagram notes `Cancelled` is reachable from any state (`F008`), §22 intro points at v0.5.0 (`F009`), and §8.4 plus `INV-014` state that cancelling a Plan requires cancelling its Tasks (`F014`).
- Derived artifacts restamped to v0.5.0 and aligned with the normative version: `**PaC version:**` in `examples/`, `conformance/`, and `.plan/P003/plan.md`, the `tools/validate.py` docstring, `README.md`, `.plan/README.md`, and `tests/` (`F006`). `README.md` minimum-repository-structure block updated to the per-plan default layout of SPEC §5 (`F010`).
- `schemas/plan.schema.json` and `schemas/task.schema.json` `required` arrays aligned with the §6/§7 MUST fields (Plan: `scope`, `planner`, `created`, `objective`, `constraints`; Task: `objective`), and all conformance fixture plans gain a `## Constraints` section (`F011`).
- `tools/validate.py` `INV-010` now requires a verification `date` on `Verified` and `Changes Requested` Tasks per §12; two new unit tests cover the checks (`F012`).
- Conformance fixture plan titles corrected from `Plan for P00` to `Plan for P001` (`F013`).

### Notes

- Protocol consistency patch implementing the accepted findings of review R002; PaC protocol version remains v0.5.0, no release tagged.

- `SPEC.md` renames the fifth operation from `Close a plan` to `Complete a plan`, aligning the operation name with the `Completed` Plan status (`SPEC.md` §18, §21). `SKILL.md` (skill `metadata.version` bumped to `0.6.1`), `AGENTS.md`, `README.md`, and `.plan/README.md` updated accordingly.
- `SPEC.md` defines five one-at-a-time operations — Draft, Approve, Implement, Verify, Complete — in `§18` and mandates that agents perform exactly one operation per turn without chaining. The implementation gate is made explicit in `§8.2`, `§9.2`, `§9.3`, and `§19`: an Implementer MUST NOT begin implementation of a Task whose parent Plan is not `Planned`. New invariant `INV-014` (A Task is not implemented before its parent Plan is `Planned`) is machine-checked by `tools/validate.py`, covered by a new `conformance/invalid/draft-plan-implementation` fixture and unit tests, and listed in `§21` conformance. `SKILL.md` and `AGENTS.md` updated to the five-operation model with one operation per turn.
- `SKILL.md` reframed as a role-agnostic operations and conformance guide: it no longer defines Planner/Implementer procedures or agent behavior (role definitions, ownership boundaries, lifecycles, and behavior rules remain normative in `SPEC.md`). It now orients agents to the applicable `SPEC.md` sections per operation and provides conformance checks for the produced artifacts. Skill `metadata.version` bumped to `0.6.0`.
- `AGENTS.md` no longer re-encodes role behavior; it defers to `SPEC.md` (§3, §8, §9, §11–13, §18, §19) and keeps only repository-specific guidance and validation conventions.
- `README.md` notes that role behavior is normative in `SPEC.md` and that `AGENTS.md`/`SKILL.md` defer to it.
- Default record layout moved to one directory per Plan: `.plan/<PlanID>/plan.md` for the Plan record and `.plan/<PlanID>/tasks/<TaskID>.md` for Tasks, replacing the flat `.plan/plans/` and `.plan/tasks/` directories. `SPEC.md` §5, §6, §7, and §22.3, `INV-013` in `tools/validate.py`, `SKILL.md`, `AGENTS.md`, `README.md`, `.plan/README.md`, `examples/`, `conformance/`, and `tests/` updated accordingly. This repository's records migrated to the new layout; legacy v0.3.x records remain unchanged and ignored by the validator.
- `SPEC.md` and `SKILL.md` version bumped to v0.5.0.
- `SKILL.md` and `AGENTS.md` clarify the host-mode boundary: a host planning gate (e.g. opencode Plan mode) approval covers only the creation/update of Plan and Task records and is not PaC plan approval; implementation begins only in a separate, planner-approved Implementer turn.
- `SKILL.md` and `AGENTS.md` require a single PaC operation and role per invocation: the agent must not chain `Plan → Implement → Verify` in one turn, and "create a plan record" means act as Planner, write the Plan and Task records in `Draft` status, and stop.
- `SPEC.md` clarifies the status model so agents start newly created Plans and Tasks in `Draft`: the Plan (`§8`) and Task (`§9`) lifecycle sections add explicit transition tables with owner and trigger, the canonical Task template now opens in `Draft`, `§18` splits plan finalization (`Draft → Planned`) into its own step, and `§21` conformance requires the `Draft`-first convention. `SKILL.md`, `AGENTS.md`, `.plan/README.md`, and a new `conformance/valid/draft` fixture updated accordingly.

### Notes

- Normative change to the default record layout; PaC protocol version bumped to v0.5.0. No release tagged; version files updated in working tree only.
- Normative workflow change: the three broad operations (Plan, Implement, Verify) are refined into five one-at-a-time operations (Draft, Approve, Implement, Verify, Complete) and a new protocol invariant `INV-014` forbids implementing a Task before its parent Plan is `Planned`. PaC protocol version remains v0.5.0; no release tagged.
- Non-normative documentation change to `SKILL.md`, `AGENTS.md`, and `README.md`; the PaC protocol remains v0.5.0 with no changes to protocol semantics, formats, or invariants.

## [v0.4.2] - 2026-09-14

Plan P003 — Enforce Status Transition Ownership for Tasks and Plans (completed).

### Changed

- Plan P003 verified and closed: all five Tasks are `Verified` by the Planner, the Plan is marked `Completed`, and `P003` is moved from Active to Closed plans in `.plan/README.md`.

### Notes

- Documentation-only patch; the PaC protocol remains v0.4.0-compliant with no changes to protocol semantics or invariants.

## [v0.4.1] - 2026-09-14

Plan P003 — Enforce Status Transition Ownership for Tasks and Plans.

### Changed

- `SPEC.md` §8 and §9 make status-transition ownership explicit: the Planner owns the Plan status and MUST mark the Plan `Planned` when it is ready for implementation and `Completed` when all required Tasks are `Verified`; the Implementer owns the Task's implementation lifecycle state and MUST mark the Task `In Progress` when beginning implementation and `Implemented` when the implementation and its evidence are complete.
- `SKILL.md` Planner and Implementer procedures now instruct the corresponding status updates.
- `examples/` Plan and Task records updated to demonstrate the explicit transitions (`Planned`/`Completed` Plans; `In Progress`/`Implemented` Tasks).

### Notes

- Patch release; the PaC protocol remains v0.4.0-compliant with no changes to protocol semantics or invariants.

## [v0.4.0] - 2026-09-14

Plan P002 — Simplify PaC Roles, Records, and Lifecycles.

### Changed

- `SPEC.md` rewritten for the simplified model: two roles (Planner, Implementer), two canonical records (Plan, Task), one independent file per Task under `.plan/tasks/`, Definition of Done replacing acceptance criteria, Planner-owned verification, explicit Plan and Task lifecycles, section-level ownership, and Git history as the historical timeline.
- `tools/validate.py` rewritten for the v0.4.0 record templates and invariants `INV-001` through `INV-013`. Legacy v0.3.x records that do not conform to the current templates are ignored (SPEC §22).
- `README.md`, `AGENTS.md`, `SKILL.md`, and `.plan/README.md` updated for the two-role, two-record model.
- `examples/` rewritten as independent Plan and Task records.
- `tests/` and `conformance/` rebuilt for the new model and invariants.

### Added

- `schemas/task.schema.json` for independent Task records.
- `changes-requested` lifecycle state in the Task state vocabulary.

### Removed

- Verifier role; verification is now Planner-owned.
- Feedback, finding, decision, verification, and iteration records from the normative model.
- Acceptance criteria and acceptance-criterion identifiers.
- Conformance levels and verification-independence levels.
- Typed relationships (`blocks`, `requires`, `conflicts-with`, `supersedes`); `depends-on` remains.
- `schemas/feedback.schema.json`.

### Notes

- Migration of this repository's own `P002.md` plan (and its Tasks) from the v0.3.x format to `.plan/tasks/` is a Planner-owned action and is pending. Legacy records under `.plan/feedback/` and `.plan/verification/` remain in place.
- Plan P002 closed: independent verification recorded all 9 tasks (P002-T001 through P002-T009) as satisfying their Definition of Done. Plan status set to `Completed`, per-task verification records added, and `P002` moved to closed plans in `.plan/README.md`.

## [v0.3.3] - 2026-09-14

### Changed

- Plan P001 closed: canonical plan updated to record the implemented and verified state (all 15 tasks `Verified` at independence Level 2), decision `P001-D001` authorizing completion, `P001-T014-F001` resolved, and the plan moved to closed plans in `.plan/README.md`.

## [v0.3.2] - 2026-09-13

### Added

- Independent verification outcome for plan P001 under `.plan/verification/`: all 15 tasks (P001-T001 through P001-T015) recorded as `Verified` at independence Level 2 with reproducible evidence (closed review `R001`, invariant validator, automated test suite, conformance fixtures), and informational finding `P001-T014-F001` recording that the canonical plan `P001.md` is not yet updated (Planner-owned, tracking `R001-F003` / `P001-FB001`).
- Feedback `P001-FB002` appended to `.plan/feedback/P001.md` summarizing the verification outcome.

## [v0.3.1] - 2026-09-13

### Changed

- Review R001 closed with no outstanding findings: findings F001 (SPEC §30.1 heading) and F002 (INV-013 relationship combinations) verified; F003 (canonical plan update) closed as deferred with follow-up tracked in `.plan/feedback/P001.md`.

## [v0.3.0] - 2026-09-13

### Added

- Typed relationship representation `**Relationships:**` for tasks (`SPEC.md` §23.3), machine-checkable invariant `INV-013` (`SPEC.md` §28) rejecting contradictory relationship combinations, matching `tools/validate.py` support, `schemas/plan.schema.json` task `relationships` projection (`SPEC.md` §29.1), and an `invalid-combination` conformance fixture.

### Fixed

- `SPEC.md` §30 subsection heading misnumbered as `### 21.1 Discovery`; renamed to `### 30.1 Discovery` (review R001 finding F001).

## [v0.2.1] - 2026-09-13

### Added

- Review as Code records for the P001 implementation review (`R001`) under `.review/` — review metadata and findings F001–F003.

## [v0.2.0] - 2026-09-13

### Added

- Normative PaC v0.2.0 semantics in `SPEC.md`: normalized data model (§20), stable acceptance-criterion identifiers (§21), deterministic task-state derivation (§22), explicit dependencies (§23), entity relationship graph (§24), finding lifecycle (§25), verification-independence levels 0–4 (§26), conformance levels Core/Agent/Verified/Automated (§27), machine-checkable protocol invariants INV-001–INV-012 (§28), and migration guidance from v0.1.0 (§32).
- First-class planning decisions with stable `P###-D###` identifiers (§12.1).
- Standardized implementation and verification evidence reference types (§16.1, §17.1).
- Dependency-free invariant validator `tools/validate.py` and an automated `tests/` suite.
- Conformance fixtures under `conformance/` for every conformance level and every core invariant.
- Updated optional schemas (`schemas/plan.schema.json`, `schemas/feedback.schema.json`) representing the revised model.

### Changed

- `SPEC.md`, `SKILL.md`, `AGENTS.md`, `README.md`, and `.plan/README.md` updated for the revised workflow, conformance levels, and verification requirements.
- Reference examples updated to the revised format (acceptance-criterion identifiers, decisions, verification independence).

## [v0.1.0] - 2026-09-13

Initial Plan as Code (PaC) specification and reference artifacts.

### Added

- Normative PaC v0.1.0 specification (`SPEC.md`) defining plans, tasks, findings, feedback, planning iterations, role ownership (Planner, Implementer, Verifier), task states, canonical decision rules, implementation evidence, verification, and merge-conflict minimization rules.
- Repository layout `.plan/` with `plans/` and `feedback/` directories and a layout README.
- Agent instructions (`AGENTS.md`) with role selection, per-role rules, ownership rules, plan consumption, feedback rules, verification rules, and prohibited actions.
- Portable agent skill (`SKILL.md`) conformant with the Agent Skills spec, covering Planner, Implementer, and Verifier procedures.
- Reference examples (`examples/`): OAuth feature plan with dependency, feedback, and verification (`P001.md`, `P001-T001.md`); verification failure and recovery (`P002.md`); plan evolution across iterations with stable IDs (`P003.md`).
- Optional validation schemas (`schemas/plan.schema.json`, `schemas/feedback.schema.json`) as machine-readable projections of the Markdown artifacts.
- `README.md`, `LICENSE` (MIT), and `CHANGELOG.md`.