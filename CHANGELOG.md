# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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