---
name: plan-as-code
description: Use to keep Plan as Code (PaC) artifacts conformant with the PaC specification (SPEC.md) when performing draft, approve, implement, verify, or complete operations on durable, Git-native plan and task records. Role-agnostic; the specification is authoritative over this skill.
license: MIT
metadata:
  author: igarciaes
  version: 0.6.2
---

# Plan as Code Skill

## Purpose

Keep PaC artifacts conformant with the Plan as Code specification while an agent performs a draft, approve, implement, verify, or complete operation. This skill defines no roles and no agent behavior: roles, ownership boundaries, lifecycles, and behavior rules are normative in `SPEC.md` and MUST be followed as written there. This skill only orients the agent to the applicable spec sections and provides conformance checks to confirm produced artifacts satisfy the spec.

## Source of truth

`SPEC.md` is authoritative. If this skill or any other artifact conflicts with it, `SPEC.md` wins.

## Operations

PaC defines five operations that execute in sequence: **Draft**, **Approve**, **Implement**, **Verify**, and **Complete**. Before writing anything, determine the assigned operation and role from the request and the repository's `AGENTS.md` and `.plan/README.md`. Perform exactly one operation per turn; do not chain or auto-continue into a subsequent operation. Each operation updates specific artifacts; the responsible role and ownership boundary are defined in `SPEC.md` §13. After executing an operation and before finishing the turn, verify that the produced records conform to `SPEC.md` using the Conformance checks below.

### Draft a plan

The Planner creates the canonical Plan and its Task records, all in `Draft`.

- Artifacts: `.plan/<PlanID>/plan.md` (`SPEC.md` §6) and `.plan/<PlanID>/tasks/<TaskID>.md` (`SPEC.md` §7).
- Reference: `SPEC.md` §5 (layout), §8.1, §9.1, §15 (identifiers), §18.1, §19.
- This operation ends with `Draft` records only. MUST NOT transition the Plan to `Planned` (that is the Approve operation, `SPEC.md` §18.2) and MUST NOT implement any Task.
- Post-operation conformance — verify the created Plan and Task records are all in `Draft`, stored per `INV-013`, and satisfy the Conformance checks below before finishing.

### Approve a plan

The Planner marks the Plan `Planned` and transitions its Tasks from `Draft` to `Planned`.

- Artifacts: Plan status and Task statuses.
- Reference: `SPEC.md` §8.2, §8.5, §9.2, §9.10, §18.2.
- This operation ends with Plan and Task statuses `Planned`. MUST NOT implement, verify, or complete.
- Post-operation conformance — verify the Plan and Task statuses are `Planned`, that the transitions were Planner-owned (`SPEC.md` §8.5, §9.10), and that the records satisfy the Conformance checks below before finishing.

### Implement a plan

The Implementer implements the Plan's Tasks and records evidence.

- Artifacts: Task `## Implementation` and `## Implementation Evidence` sections plus repository implementation artifacts.
- Reference: `SPEC.md` §9.3–9.4, §11, §13.2, §18.3, §19.
- MUST NOT implement Tasks from a Plan that is not `Planned` (`INV-014`). This operation ends with Tasks `Implemented`. MUST NOT verify Tasks or change the Plan status.
- Post-operation conformance — verify the Tasks are `Implemented` with implementation evidence recorded (`SPEC.md` §9.3–9.4, §11) and that the parent Plan is `Planned` (`INV-014`) before finishing.

### Verify a plan

The Planner evaluates implemented Tasks against their Definition of Done and records the result.

- Artifacts: Task `## Verification` section.
- Reference: `SPEC.md` §9.5–9.6, §10, §12, §13.1, §18.4, §19.
- This operation ends with Tasks `Verified` (or `Changes Requested`). MUST NOT implement Tasks or complete the Plan.
- Post-operation conformance — verify the Tasks are `Verified` (or `Changes Requested`) with a complete verification record (`SPEC.md` §12; `INV-009`, `INV-010`, `INV-011`) before finishing.

### Complete a plan

The Planner marks the Plan `Completed` once all required Tasks are `Verified`.

- Artifacts: Plan status.
- Reference: `SPEC.md` §8.3, §8.5, §18.5.
- This operation ends with the Plan `Completed`. MUST NOT implement or verify Tasks.
- Post-operation conformance — verify the Plan is `Completed` only when all required Tasks are `Verified` (`INV-012`) before finishing.

`Cancel` is a separate Planner action (`SPEC.md` §8.4, §9.9) that MAY be taken instead of continuing the sequence.

## Conformance checks

After executing an operation and before finishing the turn, the agent MUST confirm that the produced artifacts conform to `SPEC.md`. The checks below apply after every operation; operation-specific expectations are listed in each operation's post-operation conformance bullet. If any check fails, correct the offending records before finishing.

- **Layout** — each Plan at `.plan/<PlanID>/plan.md`, each Task at `.plan/<PlanID>/tasks/<TaskID>.md` (`SPEC.md` §5; `INV-013`).
- **Plan record** — stable ID, title, status, scope, Planner identity, creation metadata, objective, constraints, task list (`SPEC.md` §6).
- **Task record** — stable ID, title, status, owner, parent Plan reference, objective, Definition of Done (`SPEC.md` §7).
- **Status transitions** — only permitted transitions, owned by the correct role (`SPEC.md` §8.5, §9.10).
- **Draft gate** — a Task MUST NOT be in an implementation or verification state while its parent Plan is `Draft`; a `Draft` Plan must not contain Tasks beyond `Draft` (`INV-014`).
- **Invariants** — `INV-001` through `INV-014` hold (`SPEC.md` §17).
- **Machine validation** — when tooling is present, run `python3 tools/validate.py --root .` and validate records against `schemas/plan.schema.json` and `schemas/task.schema.json` per the projection in `SPEC.md` §20.1.