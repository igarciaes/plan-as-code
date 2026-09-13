# Plan as Code (PaC)

Plan as Code (PaC) is a lightweight, Git-native specification for defining implementation plans that can be consumed by humans and AI agents.

## What is Plan as Code?

PaC represents implementation plans as durable, repository-native Markdown artifacts. Plans, tasks, findings, and feedback live in git and evolve through git history. No database and no central service is required — the repository filesystem is the system of record.

## Why does it exist?

Implementation planning is often trapped in chat threads, tickets, and dashboards. PaC makes plans version-controlled, reviewable, and machine-validatable while keeping Markdown as the canonical human-readable format. It gives AI agents explicit roles, ownership boundaries, and deterministic procedures so that planning, implementation, and verification remain separate and auditable.

## How is it related to Review as Code?

PaC follows the conventions and philosophy of [Review as Code (RaC)](https://github.com/igarciaes/review-as-code): SPEC-first normative protocol, stable identifiers, role-based ownership, append-only feedback, derived state, and independent verification. RaC answers "was the work reviewed correctly"; PaC answers "what work is planned and is it being implemented correctly."

## What problem does it solve?

- No durable, repository-native plan artifacts.
- Unclear ownership between planners, implementers, and verifiers.
- Unstable identifiers for plans, tasks, findings, and feedback.
- Plans that cannot be validated or reasoned about by AI agents.
- Merge conflicts caused by central mutable status files and single-file registries.

## How does ownership work?

- The **Planner** owns `.plan/plans/` — objectives, scope, constraints, tasks, dependencies, acceptance criteria, and planning decisions.
- The **Implementer** owns repository implementation artifacts (`src/`, `tests/`, `docs/`, ...).
- The **Verifier** owns verification outcomes — evaluation of acceptance criteria and recorded evidence.

No role modifies another role's primary artifact.

## How do AI agents consume plans?

Agents read the canonical plan artifact, determine their assigned role and ownership boundary, and operate only within it. `AGENTS.md` and `SKILL.md` define deterministic procedures for the Planner, Implementer, and Verifier. Derived state (what is implemented, what is verified) can be computed from plan artifacts without a central registry.

## How does feedback work?

Feedback is append-only, git-managed communication associated with a task, finding, or plan. Each feedback item has a stable ID and an author. Agents append their own items and never rewrite feedback authored by another role. Feedback does not modify a plan directly — the Planner evaluates it and records an explicit decision in the canonical plan.

## How does verification work?

The Verifier independently evaluates the plan's acceptance criteria against repository artifacts. Verification is distinct from implementation: **Implemented != Verified**. Only independent verification can produce a `Verified` state. Verification failures create findings, which can generate feedback.

Verification has explicit independence levels (Level 0 self-verification through Level 4 human or externally independent verification). A repository declares the minimum level required for `Verified` in `.plan/README.md`.

## How does the workflow work?

```text
Planner
   ↓
Implementation Plan
   ↓
Implementer
   ↓
Implementation Evidence
   ↓
Verifier
   ↓
Verification / Findings
   ↓
Planner Decision
   ↓
New or revised implementation task
```

The task list in a canonical plan contains **implementation tasks**; planning and verification activities are not implementation tasks.

## What are the protocol semantics?

PaC v0.2.0 makes the protocol deterministic and machine-validatable:

- a normalized data model (`SPEC.md` §20) that maps canonically from Markdown;
- stable acceptance-criterion identifiers (`AC-P###-T###-NN`);
- deterministic task-state derivation (`SPEC.md` §22);
- explicit dependency and entity relationships;
- first-class planning decisions (`P###-D###`);
- a finding lifecycle;
- verification-independence levels;
- standardized evidence references;
- conformance levels (PaC Core, Agent, Verified, Automated);
- machine-checkable protocol invariants (`SPEC.md` §28), enforced by `tools/validate.py`.

## What is the minimum repository structure?

```text
.plan/
├── plans/
│   └── P001.md
└── feedback/
    └── P001-T001.md
```

## Repository contents

- `SPEC.md` — normative PaC v0.2.0 specification
- `AGENTS.md` — instructions for agents working in this repository
- `SKILL.md` — portable PaC agent skill
- `.plan/` — plan and feedback storage layout
- `examples/` — reference plan records
- `schemas/plan.schema.json` — optional validation schema for plan records
- `schemas/feedback.schema.json` — optional validation schema for feedback threads
- `conformance/` — valid and invalid protocol conformance fixtures
- `tools/validate.py` — dependency-free invariant validator (SPEC §28)
- `tests/` — automated tests for the validator, schemas, and conformance fixtures
- `CHANGELOG.md` — release history (Keep a Changelog)
- `LICENSE` — MIT © 2026 igarciaes and contributors

See `SPEC.md` for the complete protocol.