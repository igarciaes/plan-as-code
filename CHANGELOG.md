# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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