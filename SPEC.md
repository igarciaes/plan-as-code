# Plan as Code Specification

## Version

**PaC v0.4.2**

## 1. Purpose

Plan as Code (PaC) defines a Git-native, human-readable protocol for defining, tracking, and verifying implementation plans.

PaC applies to implementation planning of any repository artifact — source code, documentation, specifications, requirements, architecture, configuration, and more — and is designed for both human and AI-agent workflows.

The goals of PaC are to:

- make implementation plans durable and version controlled;
- provide stable identifiers for plans and tasks;
- separate the Planner and Implementer roles with clear ownership boundaries;
- remain easy for humans to read and edit;
- provide explicit semantics for AI agents;
- keep Git history as the historical timeline;
- make implementation state derivable from repository artifacts;
- minimize merge conflicts;
- allow optional machine validation without making machine formats canonical.

## 2. Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this specification are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

- **MUST** — an absolute requirement.
- **MUST NOT** — an absolute prohibition.
- **SHOULD** — a recommended practice; valid reasons may exist to ignore it, but the implications must be understood.
- **SHOULD NOT** — a discouraged practice; valid reasons may exist to adopt it, but the implications must be understood.
- **MAY** — a permitted, optional practice.

## 3. Core principles

### 3.1 Human-friendly first

Plan artifacts MUST be human-readable. Markdown is the canonical default representation.

### 3.2 Git native

Plan artifacts MUST be version controlled alongside the work they describe. Git and the repository filesystem MUST remain the system of record.

Git history is the historical timeline. The protocol MUST NOT require event records, iteration records, or any other artifact that duplicates history that Git already provides.

### 3.3 Role separation

The Planner owns planning intent and verification. The Implementer owns implementation.

No role MUST modify another role's primary artifact or section.

### 3.4 Distinct operations

Implementation and verification are distinct operations.

**Implemented != Verified.** Only the Planner MAY mark a Task as `Verified`, and only against the Task's Definition of Done.

### 3.5 Stable identity

Plans and tasks MUST have stable identifiers.

Identifiers MUST NOT change when wording, status, or implementation changes.

### 3.6 Derived state

State SHOULD be derived from plan and task artifacts rather than stored in a central mutable record.

Do NOT introduce a database or require a central service.

### 3.7 Merge-conflict minimization

Plan and task artifacts SHOULD be isolated by file to minimize merge conflicts. See Section 12.

## 4. Terminology

### Plan

A durable implementation planning artifact describing the intended outcome of a unit of work, its scope, constraints, and the tasks required to achieve it.

### Task

A unit of planned implementation work within a plan.

### Planner

The role that owns planning intent, planning artifacts, and verification.

### Implementer

The role that owns repository implementation artifacts and implements planned tasks.

### Definition of Done

The observable conditions that MUST be satisfied before the Planner can verify a Task.

### Scope

The set of artifacts covered by a plan, expressed as file paths, directory paths, or other artifact references.

### Constraints

Non-functional or architectural limits that bound how a plan may be implemented.

### Dependency

An ordering constraint between tasks: a task MUST NOT start implementation until the tasks it depends on are implemented.

### Implementation evidence

Git-native references that record how a task was implemented.

### Verification

The Planner's evaluation of a Task's implementation against its Definition of Done.

### Protocol invariant

A normative property of PaC artifacts that MUST hold, with a stable identifier such as `INV-001`.

## 5. Repository model

A repository MAY contain many plans.

The default layout is:

```text
.plan/
├── README.md
├── plans/
│   ├── P002.md
│   └── P003.md
└── tasks/
    ├── P002-T001.md
    ├── P002-T002.md
    └── P003-T001.md
```

Plans and Tasks MUST be independently addressable files:

- each Plan MUST have its own file under `plans/`;
- each Task MUST have its own file under `tasks/`;
- a Task MUST NOT be defined inline in its parent Plan;
- a Task MUST NOT require modification of its parent Plan during implementation.

Repositories MAY define another layout in `.plan/README.md`.

A single global plan file MUST NOT be used to represent multiple unrelated plans.

Before allocating a new plan ID, an agent SHOULD scan the existing plan records and take the next sequential unused ID (for example, the next `P###` number). The allocation convention MAY be documented in `.plan/README.md`.

### 5.1 Plan README

`.plan/README.md` describes the repository's plan layout and conventions.

It SHOULD document:

- the plan layout and the paths of plan and task records;
- the plan ID convention (for example `P###`);
- the task ID convention (for example `P###-T###`);
- the controlled status vocabulary when a subset is used;
- the active plans when useful.

It MAY override the default layout described above.

It MUST remain human-readable and SHOULD be readable by agents for discovery.

## 6. Plan record

A Plan MUST be a single Markdown file under `.plan/plans/`.

A Plan MUST have:

- a stable ID;
- a title;
- a status;
- a scope;
- a Planner identity;
- creation metadata;
- an objective;
- constraints;
- a task list.

A Plan MAY have included and excluded scope items and a Plan Definition of Done.

A Plan ID uses the recommended format `P###` (for example `P001`).

The canonical Plan template is:

````markdown
# P001 — Title

**Status:** Draft
**Scope:** `path/`
**Planner:** planner-agent
**Created:** YYYY-MM-DD
**PaC version:** v0.4.0

## Objective

Describe the intended outcome.

## Scope

### Included

- Item

### Excluded

- Item

## Constraints

- Constraint

## Tasks

- P001-T001
- P001-T002

## Definition of Done

The Plan is ready to be marked `Completed` when:

- [ ] Condition one.
- [ ] Condition two.
````

The template MUST remain intentionally simple.

Do NOT add implementation details unless they are required constraints.

## 7. Task record

A Task MUST be a single Markdown file under `.plan/tasks/`.

A Task MUST have:

- a stable ID;
- a title;
- a status;
- an owner role;
- a reference to its parent Plan;
- an objective;
- a Definition of Done.

A Task MAY have:

- dependencies;
- an implementation description;
- implementation evidence;
- a verification section.

A Task ID uses the recommended format `P###-T###` (for example `P001-T001`).

The canonical Task template is:

````markdown
# P001-T001 — Title

**Status:** Planned
**Owner:** Implementer
**Plan:** P001

## Objective

Describe the required work.

**Depends on:**

- None

## Definition of Done

- [ ] Condition one.
- [ ] Condition two.

## Implementation

Describe the implementation approach, if applicable.

## Implementation Evidence

- Commit: `abc1234`
- Test: `npm test`
- Result: passed

## Verification

**Result:** Pending

**By:** planner-agent
**Date:** YYYY-MM-DD
````

The template MUST remain intentionally simple.

## 8. Plan lifecycle

The Plan lifecycle is:

```text
Draft → Planned → Completed
              ↘ Cancelled
```

The Planner owns the Plan status and MUST advance the Plan through its lifecycle. Only the Planner MAY transition a Plan to `Planned` or `Completed`.

### 8.1 Draft

The Plan is being prepared.

Scope, Tasks, dependencies, and Definition of Done may still change.

### 8.2 Planned

The Plan is ready for implementation.

The Planner MUST mark the Plan `Planned` when it is ready for implementation.

Required Tasks have been identified and the Planner considers the Plan sufficiently defined.

### 8.3 Completed

The Plan has been successfully completed.

The Planner MUST mark the Plan `Completed` when all required Tasks are `Verified`.

A Plan MUST NOT be marked `Completed` while any required Task is not `Verified`.

For the purpose of this rule, a required Task is any Task belonging to the Plan that is not `Cancelled`.

### 8.4 Cancelled

The Plan will not be implemented.

`Cancelled` is a terminal state.

## 9. Task lifecycle

The Task lifecycle is:

```text
Draft → Planned → In Progress → Implemented → Verified
                                      │
                                      ▼
                              Changes Requested
                                      │
                                      ▼
                                In Progress
```

Tasks MAY additionally transition to `Blocked`, `Deferred`, or `Cancelled` according to the rules defined below.

The Implementer owns the Task's implementation lifecycle state (`In Progress`, `Implemented`) and MUST advance the Task through it. Only the Planner MAY transition a Task to `Verified`.

### 9.1 Draft

The Task is being defined.

### 9.2 Planned

The Task is ready for implementation.

### 9.3 In Progress

The Implementer is actively working on the Task.

The Implementer MUST mark the Task `In Progress` when beginning implementation.

### 9.4 Implemented

The Implementer considers the implementation complete and has provided the required evidence.

The Implementer MUST mark the Task `Implemented` when the implementation and its evidence are complete.

`Implemented` does not mean verified.

### 9.5 Changes Requested

The Planner has reviewed the implementation and determined that the Definition of Done has not been satisfied.

The Task returns to `In Progress` when implementation resumes.

The reason for a failed verification MUST be recorded in the Task's verification section.

### 9.6 Verified

The Planner has verified that the Definition of Done is satisfied.

`Verified` is the successful terminal state of a Task.

Only the Planner MAY transition a Task to `Verified`.

### 9.7 Blocked

Work cannot proceed because of an external dependency or unresolved blocker.

### 9.8 Deferred

The Task is intentionally postponed.

### 9.9 Cancelled

The Task will not be implemented.

`Cancelled` is a terminal state.

## 10. Definition of Done

A Task's Definition of Done describes the observable conditions that must be satisfied before the Planner can verify the Task.

The Definition of Done is part of the Task record.

Typical conditions include:

- Implementation is complete.
- Required tests pass.
- Required documentation is updated.
- Implementation evidence is provided.
- Planner verification is complete.

The Definition of Done replaces acceptance criteria. No separate Acceptance Criterion records or IDs exist.

Each condition is represented as a checkbox in the Task record. A condition is satisfied when its checkbox is checked.

Before marking a Task `Verified`, the Planner MUST confirm that every Definition of Done condition is satisfied.

## 11. Implementation

Implementation details belong to the Task record.

The Implementer owns:

- `Implementation`
- `Implementation Evidence`
- the Task's implementation lifecycle state

Implementation evidence MAY reference:

- Git commits
- Pull requests
- Changed files
- Test commands
- Test results
- Build results
- Generated artifacts

## 12. Verification

Verification belongs to the Task record and is owned by the Planner.

The Planner verifies the implementation against the Task's Definition of Done.

Successful verification results in:

```text
Implemented → Verified
```

Failed verification results in:

```text
Implemented → Changes Requested
```

The reason for a failed verification MUST be recorded in the Task.

The verification section MUST record:

- the result (`Verified`, `Changes Requested`, or `Pending`);
- the verifier (the Planner identity);
- the date.

No separate Verification record or Verification ID exists.

The Implementer MUST NOT mark a Task as `Verified`.

## 13. Section ownership

Section-level ownership is used to minimize merge conflicts.

### 13.1 Planner-owned sections

- Plan status
- Plan objective
- Plan scope
- Plan constraints
- Task definitions
- Definition of Done
- Verification
- Planner Decision

### 13.2 Implementer-owned sections

- Task implementation
- Implementation evidence
- Task implementation lifecycle state

The Implementer MUST NOT authoritatively modify Planner verification.

The Implementer MUST NOT mark a Task `Verified`.

The same person or agent MAY perform different roles at different times, but MUST respect the ownership boundaries of the current operation.

## 14. Merge-conflict minimization

The following rules are normative:

1. Each Plan MUST have its own file.
2. Each Task MUST have its own file.
3. Implementing a Task MUST NOT require editing the parent Plan.
4. Implementers SHOULD modify only the Task they are implementing.
5. Planners SHOULD modify only the relevant Plan or Task.
6. Shared mutable status files SHOULD NOT be required.
7. Historical state MUST NOT be duplicated into event logs.
8. Changes SHOULD remain as localized as practical.
9. Git history provides the historical timeline.

## 15. Identifiers

The protocol defines two identifier formats:

```text
P###          (for example P001)
P###-T###     (for example P001-T001)
```

The following identifier forms are removed from the protocol:

- Acceptance Criterion IDs
- Feedback IDs
- Finding IDs
- Decision IDs
- Verification IDs
- Iteration IDs
- Event IDs

Identifiers MUST NOT change when wording, status, or implementation changes.

Create a new ID only for a logically distinct entity; do NOT create a new task ID merely because wording changes.

## 16. Normalized model

The simplified normalized model contains only Plan and Task.

Markdown remains the canonical representation (Section 3.1); the normalized model is a derived, machine-checkable projection used for validation.

### 16.1 Plan

```text
Plan
├── id
├── status
├── objective
├── scope
├── constraints
└── tasks
```

### 16.2 Task

```text
Task
├── id
├── plan_id
├── status
├── owner
├── objective
├── depends_on
├── definition_of_done
├── implementation
├── implementation_evidence
└── verification
```

Implementation evidence and verification are Task data, not separate entities.

### 16.3 Deterministic projection

Canonical Markdown MUST map to the normalized model through the projection defined in Section 20.1.

```text
Canonical Markdown
        ↓
Normalized PaC Model
        ↓
Validation / Derived State
```

### 16.4 Optionality

The normalized model is optional tooling. It MUST NOT replace Markdown as the source of truth. A repository MUST remain fully usable with only Markdown and Git.

## 17. Protocol invariants

The following invariants MUST hold for conforming PaC artifacts. Each invariant has a stable identifier.

```text
INV-001 — Plan IDs are unique.
INV-002 — Task IDs are unique.
INV-003 — Every Task references a Plan that exists.
INV-004 — Task ID prefix matches its parent Plan.
INV-005 — Plan status is valid.
INV-006 — Task status is valid.
INV-007 — Dependency targets exist.
INV-008 — Dependency cycles are rejected.
INV-009 — Only the Planner marks a Task Verified.
INV-010 — Verified requires a Planner verification record; Changes Requested requires a recorded reason.
INV-011 — A Verified Task satisfies its Definition of Done.
INV-012 — A Plan is Completed only when all required Tasks are Verified.
INV-013 — Records are stored in the defined layout.
```

### 17.1 Checkability

- Every invariant MUST be machine-checkable where applicable.
- Invalid artifacts MUST produce actionable validation failures that identify the invariant and the offending artifact.
- Validation MUST cover identity, relationships, state, evidence, and ownership.
- Invariant validation MUST be covered by automated tests.

## 18. Workflow

### 18.1 Create a plan

The Planner creates a Plan record for a defined objective and scope.

### 18.2 Define tasks

The Planner defines Tasks, dependencies, constraints, and Definition of Done.

### 18.3 Implement

The Implementer reads the complete canonical Plan and implements accepted Tasks, recording implementation evidence in each Task.

### 18.4 Verify

The Planner evaluates each implemented Task against its Definition of Done and records the result in the Task.

### 18.5 Evolve

Plans and Tasks evolve over time. Git history provides the historical evolution. Stable IDs are preserved (Section 15).

## 19. Agent interoperability

Agents MUST distinguish:

```text
Intended work (Task)
Implementation
Verification
```

These concepts are not interchangeable.

Agents MUST determine their current operation and ownership boundary before writing.

Agents MUST:

- preserve stable IDs;
- read the complete canonical Plan before starting implementation;
- record implementation evidence when acting as Implementer;
- record verification results in the Task when acting as Planner.

Agents MUST NOT:

- change the objective, scope, or Definition of Done;
- implement a Task outside the assigned role;
- mark a Task as `Verified` when acting as Implementer;
- modify another role's primary artifact or section;
- claim verification without evidence.

### 19.1 Discovery

Before operating, an agent SHOULD:

1. read repository instructions such as `AGENTS.md`;
2. locate `.plan/README.md` if present and read it for layout, ID formats, and active plans;
3. locate the applicable Plan and Task records;
4. identify the agent's assigned role and corresponding ownership boundary;
5. identify the assigned Task;
6. check Task dependencies;
7. execute only allowed work within the ownership boundary;
8. record evidence and stop at the role boundary.

## 20. Human-readable format

Markdown is the canonical default format.

Machine-readable representations MAY be generated for validation or automation but SHOULD NOT replace the human-readable plan artifact.

### 20.1 Markdown-to-schema projection

The optional schemas in `schemas/` are machine-readable projections of the Markdown records. This section defines how each projection is derived.

Plan record (`schemas/plan.schema.json`):

| Markdown element | Schema property |
|------------------|-----------------|
| `# P001 — Title` heading | `id` (`P001`) and `title` (text after the em dash) |
| `**Status:**` | `status` |
| `**Scope:**` | `scope` |
| `**Planner:**` | `planner` |
| `**Created:**` | `created` |
| `**PaC version:**` | `pac_version` |
| `## Objective` section content | `objective` |
| `## Scope` `### Included` items | `included` (array of strings) |
| `## Scope` `### Excluded` items | `excluded` (array of strings) |
| `## Constraints` section items | `constraints` (array of strings) |
| `## Tasks` list items | `tasks` (array of task IDs) |
| `## Definition of Done` checkbox list | `definition_of_done` (array of `{done, text}`) |

Task record (`schemas/task.schema.json`):

| Markdown element | Schema property |
|------------------|-----------------|
| `# P001-T001 — Title` heading | `id` (`P001-T001`) and `title` (text after the em dash) |
| `**Status:**` | `status` |
| `**Owner:**` | `owner` |
| `**Plan:**` | `plan_id` |
| `## Objective` section content | `objective` |
| `**Depends on:**` items | `depends_on` (array of task IDs) |
| `## Definition of Done` checkbox list | `definition_of_done` (array of `{done, text}`) |
| `## Implementation` section content | `implementation` |
| `## Implementation Evidence` items | `implementation_evidence` (array of strings) |
| `## Verification` `**Result:**` | `verification.result` |
| `## Verification` `**By:**` | `verification.by` |
| `## Verification` `**Date:**` | `verification.date` |
| `## Verification` section content | `verification.reason` |

Fields that appear in the Markdown but have no schema property (for example links or narrative prose) are not projected.

## 21. Conformance

A PaC implementation conforms to v0.4.0 when it:

1. supports multiple plan records per repository;
2. provides stable plan and task IDs;
3. preserves Planner and Implementer ownership boundaries;
4. distinguishes implementation from verification;
5. provides a human-readable plan representation;
6. requires a Definition of Done for Tasks;
7. restricts `Verified` to the Planner;
8. derives state from plan and task artifacts without a central mutable registry;
9. uses Git history as the historical timeline.

## 22. Migration from v0.3.x

This section documents how existing PaC v0.3.x artifacts can be migrated to v0.4.0. Migration SHOULD preserve stable identifiers.

### 22.1 Roles

The Verifier role is removed. Verification is performed by the Planner. Existing verification records SHOULD be folded into the affected Task's `## Verification` section.

### 22.2 Records

Feedback, finding, decision, verification, and iteration records are no longer canonical. Their content MAY be:

- recorded directly in the relevant Plan or Task where it affects the current state; or
- left in place as historical records; Git history preserves them.

Validators MAY ignore records that do not conform to the current record templates.

### 22.3 Tasks

v0.3.x plans defined Tasks inline. In v0.4.0, each Task MUST have its own file under `.plan/tasks/`.

### 22.4 Acceptance criteria

v0.3.x acceptance criteria become Definition of Done conditions. The `AC-P###-T###-NN` identifiers are removed.

### 22.5 Dependencies

v0.3.x typed relationships (`blocks`, `requires`, `conflicts-with`, `supersedes`) are removed. `depends-on` remains the only dependency form.

### 22.6 No automatic rewrite

Migration MUST NOT require an automated rewrite. Existing valid v0.3.x records remain readable; the structure above is the target model.

## 23. Fundamental invariant

> The Planner defines what and determines whether. The Implementer defines how.

The same human or agent MAY perform multiple roles at different times, but MUST NOT collapse ownership boundaries within a single operation.