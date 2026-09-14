---
name: plan-as-code
description: Use to perform Plan as Code (PaC) operations — plan, implement, and verify — for implementation work with durable, Git-native plan and task artifacts. Follow SPEC.md when present; the specification is authoritative over this skill.
license: MIT
metadata:
  author: igarciaes
  version: 0.4.0
---

# Plan as Code Agent Skill

## Goal

Plan, implement, and verify implementation work through durable, Git-native Plan and Task artifacts with clear Planner and Implementer ownership boundaries.

## Inputs

- Repository instructions (`AGENTS.md`).
- Plan layout instructions (`.plan/README.md`) when present.
- The canonical Plan record under `.plan/plans/`.
- The applicable Task records under `.plan/tasks/`.
- The assigned role for the current operation.

## Outputs

- A canonical Plan record and Task records (Planner).
- Implementation changes with recorded evidence (Implementer).
- Verified Tasks and Completed Plans (Planner).

## Workflow

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

The task list in a canonical Plan contains **implementation tasks**. Planning and verification activities are not implementation tasks.

1. Read the plan.
2. Validate role.
3. Identify owned artifacts.
4. Identify assigned task.
5. Check dependencies.
6. Execute allowed work.
7. Record evidence.
8. Stop at role boundary.

## Planner Procedure

1. Read `.plan/README.md` and confirm you act as Planner.
2. Create or update the canonical Plan under `.plan/plans/` and Tasks under `.plan/tasks/`.
3. Record the objective, scope, constraints, tasks, dependencies, and Definition of Done.
4. Allocate stable IDs (`P###`, `P###-T###`) by scanning existing records.
5. Preserve stable IDs across iterations.
6. Verify implemented Tasks against their Definition of Done.
7. Mark Tasks `Verified` only when the Definition of Done is satisfied; otherwise record the reason and mark the Task `Changes Requested`.
8. Mark Plans `Completed` only when all required Tasks are `Verified`.
9. Stop before modifying implementation merely to satisfy the plan.

## Implementer Procedure

1. Read `.plan/README.md` and confirm you act as Implementer.
2. Read the complete canonical Plan before starting.
3. Implement only accepted, planner-owned tasks.
4. Check task dependencies before starting work.
5. Record implementation evidence (commit SHA, changed files, test command, test result) in the Task.
6. Mark the Task `Implemented` when the work and evidence are complete.
7. Do not change the objective or the Definition of Done.
8. Do not mark a Task as `Verified`.
9. Stop before modifying Planner verification or the canonical Plan.

## Decision Rules

- The Implementer consumes the canonical Plan rather than inferring requirements from discussion.
- Do not create a new task ID merely because wording changes; create a new ID only for a logically distinct entity.
- `Implemented` is not `Verified`. Only the Planner MAY mark a Task `Verified`.
- A Plan MAY only become `Completed` when all required Tasks are `Verified`.
- Protocol invariants (SPEC Section 17) MUST be machine-checkable; when tooling is present, run it (for example `python3 tools/validate.py --root .`).

## Completion Criteria

- Planner: the canonical Plan and Task records record the objective, scope, constraints, tasks, dependencies, and Definition of Done.
- Implementer: accepted tasks are implemented with recorded evidence; tasks are marked `Implemented`.
- Planner: implemented tasks are verified against the Definition of Done, and Plans become `Completed` when all required Tasks are `Verified`.
- Implemented is not Verified. Only Planner verification can produce `Verified`.