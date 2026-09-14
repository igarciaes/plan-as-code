# Plan as Code (PaC)

Plan as Code (PaC) is a lightweight, Git-native specification for defining implementation plans that can be consumed by humans and AI agents.

## What is Plan as Code?

PaC represents implementation plans as durable, repository-native Markdown artifacts. Plans and tasks live in git and evolve through git history. No database and no central service is required — the repository filesystem is the system of record, and Git history is the historical timeline.

## Why does it exist?

Implementation planning is often trapped in chat threads, tickets, and dashboards. PaC makes plans version-controlled, reviewable, and machine-validatable while keeping Markdown as the canonical human-readable format. It gives AI agents explicit roles, ownership boundaries, and deterministic procedures so that planning and implementation remain separate and auditable.

## How is it related to Review as Code?

PaC follows the conventions and philosophy of [Review as Code (RaC)](https://github.com/igarciaes/review-as-code): SPEC-first normative protocol, stable identifiers, role-based ownership, derived state, and clear separation of operations. RaC answers "was the work reviewed correctly"; PaC answers "what work is planned and is it being implemented correctly."

## What problem does it solve?

- No durable, repository-native plan artifacts.
- Unclear ownership between planners and implementers.
- Unstable identifiers for plans and tasks.
- Plans that cannot be validated or reasoned about by AI agents.
- Merge conflicts caused by central mutable status files, single-file registries, and inline task definitions.

## How does the model work?

PaC defines exactly two roles and two canonical records:

- **Planner** — owns planning intent and verification.
- **Implementer** — owns repository implementation artifacts and implements tasks.
- **Plan** — a single Markdown file under `.plan/plans/`.
- **Task** — a single Markdown file under `.plan/tasks/`, one file per Task.

Tasks carry a **Definition of Done**, implementation evidence, and Planner verification. No separate feedback, finding, decision, or verification records are required; Git history provides the historical timeline.

## How does ownership work?

- The **Planner** owns `.plan/plans/` and the planning and verification sections of Task records — objectives, scope, constraints, task definitions, Definition of Done, and verification.
- The **Implementer** owns repository implementation artifacts (`src/`, `tests/`, `docs/`, ...) and the implementation, evidence, and lifecycle-state sections of Task records.

No role modifies another role's primary artifact or section.

## How do AI agents consume plans?

Agents read the canonical Plan and Task artifacts, determine their assigned role and ownership boundary, and operate only within it. `AGENTS.md` and `SKILL.md` define deterministic procedures for the Planner and Implementer. State (what is implemented, what is verified) is recorded in the records and can be checked without a central registry.

## How does implementation work?

The Implementer reads the complete canonical Plan, implements accepted Tasks, and records implementation evidence (commits, changed files, test commands, test results) in each Task. When complete, the Task is marked `Implemented`.

## How does verification work?

The Planner evaluates an `Implemented` Task against its Definition of Done and records the result in the Task. Verification is distinct from implementation: **Implemented != Verified**. Successful verification marks the Task `Verified`; failed verification marks it `Changes Requested` with the reason recorded, and implementation resumes.

## How does the workflow work?

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

The task list in a canonical Plan contains **implementation tasks**; planning and verification activities are not implementation tasks.

## What are the protocol semantics?

PaC v0.4.0 is deliberately simple:

- two roles and two canonical records;
- one independent file per Task;
- explicit Plan and Task lifecycles;
- a Definition of Done instead of acceptance criteria;
- Planner-owned verification;
- Git history as the historical timeline;
- section-level ownership to minimize merge conflicts;
- a normalized model (Plan and Task only);
- machine-checkable protocol invariants (SPEC §17), enforced by `tools/validate.py`.

## What is the minimum repository structure?

```text
.plan/
├── README.md
├── plans/
│   └── P001.md
└── tasks/
    └── P001-T001.md
```

## Repository contents

- `SPEC.md` — normative PaC v0.4.0 specification
- `AGENTS.md` — instructions for agents working in this repository
- `SKILL.md` — portable PaC agent skill
- `.plan/` — plan and task storage layout
- `examples/` — reference plan and task records
- `schemas/plan.schema.json` — optional validation schema for plan records
- `schemas/task.schema.json` — optional validation schema for task records
- `conformance/` — valid and invalid protocol conformance fixtures
- `tools/validate.py` — dependency-free invariant validator (SPEC §17)
- `tests/` — automated tests for the validator, schemas, and conformance fixtures
- `CHANGELOG.md` — release history (Keep a Changelog)
- `LICENSE` — MIT © 2026 igarciaes and contributors

See `SPEC.md` for the complete protocol.