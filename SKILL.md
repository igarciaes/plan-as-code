---
name: plan-as-code
description: Use to perform Plan as Code (PaC) operations — plan, implement, verify, and provide feedback — for implementation work with durable, Git-native plan artifacts. Follow SPEC.md when present; the specification is authoritative over this skill.
license: MIT
metadata:
  author: igarciaes
  version: 0.3.1
---

# Plan as Code Agent Skill

## Goal

Plan, implement, and verify implementation work through durable, Git-native plan artifacts with clear Planner, Implementer, and Verifier ownership boundaries.

## Inputs

- Repository instructions (`AGENTS.md`).
- Plan layout instructions (`.plan/README.md`) when present.
- The canonical plan record under `.plan/plans/`.
- Applicable feedback threads under `.plan/feedback/`.
- The assigned role for the current operation.

## Outputs

- A canonical plan record (Planner).
- Implementation changes with recorded evidence (Implementer).
- Verification outcomes with recorded evidence (Verifier).
- Append-only feedback items (any role).

## Workflow

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

The task list in a canonical plan contains **implementation tasks**. Planning and verification activities are not implementation tasks.

1. Read plan.
2. Validate role.
3. Identify owned artifacts.
4. Identify assigned task.
5. Check dependencies.
6. Execute allowed work.
7. Record evidence.
8. Stop at role boundary.

## Planner Procedure

1. Read `.plan/README.md` and confirm you act as Planner.
2. Create or update the canonical plan under `.plan/plans/`.
3. Record the objective, scope, constraints, tasks, dependencies, and acceptance criteria.
4. Allocate stable IDs (`P###`, `P###-T###`) by scanning existing records.
5. Evaluate feedback and record an explicit decision; do not let feedback silently change the plan.
6. Preserve stable IDs across iterations.
7. Stop before modifying implementation merely to satisfy the plan.
8. Stop before independently verifying implementation you authored.

## Implementer Procedure

1. Read `.plan/README.md` and confirm you act as Implementer.
2. Read the complete canonical plan before starting.
3. Implement only accepted, planner-owned tasks.
4. Check task dependencies before starting work.
5. Record implementation evidence (commit SHA, changed files, test command, test result).
6. Request clarification through your own feedback items; do not infer requirements from discussion.
7. Do not change the objective, acceptance criteria, or planner-owned decisions.
8. Do not mark implementation as independently verified.
9. Stop before modifying the canonical plan.

## Verifier Procedure

1. Read `.plan/README.md` and confirm you act as Verifier.
2. Read the canonical plan and the current task states.
3. Independently evaluate repository artifacts against the acceptance criteria.
4. Record reproducible verification evidence (commands, test names, commit references).
5. If verification fails, create a finding with a stable ID (`P###-T###-F###`).
6. Determine verification status.
7. Do not modify implementation merely to make verification pass.
8. Stop before redefining requirements or changing the planning intent.

## Decision Rules

- Feedback does not automatically modify a plan.
- A plan change results only from an explicit Planner decision.
- The Implementer consumes the canonical plan rather than inferring requirements from discussion.
- Do not create a new task ID merely because wording changes; create a new ID only for a logically distinct entity.
- Task state MUST be derived deterministically from repository artifacts (SPEC Section 22).
- `Verified` requires independent verification satisfying the repository's configured verification requirement (SPEC Section 26).
- Protocol invariants (SPEC Section 28) MUST be machine-checkable; when tooling is present, run it (for example `python3 tools/validate.py --root .`).

## Feedback Rules

- Feedback is append-only communication associated with a task, a finding, or a plan.
- Append feedback to the thread for the subject (`P001-T001`, `P001-T001-F001`, or `P001`).
- Give each new item a new stable ID (`P001-T001-FB003`).
- Record the author role and date.
- Do not reorder existing feedback.
- Do not rewrite feedback authored by another role.

## Completion Criteria

- Planner: the canonical plan records the objective, scope, constraints, tasks, dependencies, acceptance criteria, and any explicit decisions.
- Implementer: accepted tasks are implemented with recorded evidence; clarification was requested through feedback when needed.
- Verifier: acceptance criteria were independently evaluated with reproducible evidence; failures produced findings.
- Implemented is not Verified. Only independent verification can produce `Verified`.