# Plan as Code

Plans and Tasks are stored under `plans/` and `tasks/` in this repository.

## Layout

Each Plan is a single Markdown file under `plans/`, and each Task is a single Markdown file under `tasks/`.

- Plan IDs follow `P###` (for example `P001`).
- Plan IDs are allocated by scanning `plans/` for existing records and taking the next sequential unused number.
- Task IDs follow `P###-T###` (for example `P001-T001`).
- Task filenames follow the Task ID (for example `tasks/P001-T001.md`).
- Every Task references its parent Plan in a `**Plan:**` field.

## Status

This repository uses the full PaC v0.4.0 vocabulary from `SPEC.md`.

Plan states: Draft, Planned, Completed, Cancelled.

Task states: Draft, Planned, In Progress, Implemented, Verified, Blocked, Deferred, Cancelled.

## Migration status

This repository is migrating from PaC v0.3.x. The following are pending Planner action and are intentionally left untouched:

- `plans/P001.md` and `plans/P002.md` still use the v0.3.x format with inline Tasks, and their Tasks have not yet been moved to `tasks/`.
- Legacy v0.3.x records remain under `feedback/` and `verification/`.

The invariant validator ignores records that do not conform to the current templates.

## Active plans

- P002 — Simplify PaC Roles, Records, and Lifecycles.

## Closed plans

- P001 — Strengthen PaC Protocol Semantics and Conformance.