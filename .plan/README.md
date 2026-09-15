# Plan as Code

Plans and Tasks are stored under `.plan/` in this repository.

## Layout

Each Plan has its own directory under `.plan/` named after its Plan ID. The Plan record is stored as `plan.md` in that directory, and each Task is a single Markdown file under the Plan's `tasks/` directory.

```text
.plan/
├── README.md
├── P002/
│   ├── plan.md
│   └── tasks/
│       ├── P002-T001.md
│       └── P002-T002.md
└── P003/
    ├── plan.md
    └── tasks/
        └── P003-T001.md
```

- Plan IDs follow `P###` (for example `P001`).
- Plan IDs are allocated by scanning `.plan/` for existing plan directories and taking the next sequential unused number.
- Task IDs follow `P###-T###` (for example `P001-T001`).
- Task filenames follow the Task ID (for example `.plan/P001/tasks/P001-T001.md`).
- Every Task references its parent Plan in a `**Plan:**` field.

## Status

This repository uses the full PaC v0.5.0 vocabulary from `SPEC.md`.

Plan states: Draft, Planned, Completed, Cancelled.

Task states: Draft, Planned, In Progress, Implemented, Verified, Changes Requested, Blocked, Deferred, Cancelled.

Newly created Plans and Tasks start in `Draft`. Marking a Plan `Planned` (and its Tasks from `Draft` to `Planned`) is a separate, explicit Planner action performed when the Plan is ready for implementation.

## Migration status

This repository is migrating from PaC v0.3.x. The following are pending Planner action and are intentionally left untouched:

- `plans/P001.md` and `plans/P002.md` still use the v0.3.x format with inline Tasks, and their Tasks have not yet been moved to per-plan `tasks/` directories. Their records are stored as `.plan/P001/plan.md` and `.plan/P002/plan.md`.
- Legacy v0.3.x records remain under `feedback/` and `verification/`.

The invariant validator ignores records that do not conform to the current templates.

## Active plans

None.

## Completed plans

- P003 — Enforce Status Transition Ownership for Tasks and Plans.
- P001 — Strengthen PaC Protocol Semantics and Conformance.
- P002 — Simplify PaC Roles, Records, and Lifecycles.