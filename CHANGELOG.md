# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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