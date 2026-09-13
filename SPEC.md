# Plan as Code Specification

## Version

**PaC v0.2.1**

## 1. Purpose

Plan as Code (PaC) defines a Git-native, human-readable protocol for defining, tracking, and verifying implementation plans.

PaC applies to implementation planning of any repository artifact — source code, documentation, specifications, requirements, architecture, configuration, and more — and is designed for both human and AI-agent workflows.

The goals of PaC are to:

- make implementation plans durable and version controlled;
- provide stable identifiers for plans, tasks, findings, and feedback;
- separate the Planner, Implementer, and Verifier roles with clear ownership boundaries;
- remain easy for humans to read and edit;
- provide explicit semantics for AI agents;
- keep feedback append-only and decision-relevant;
- record explicit planning decisions rather than inferring requirements from discussion;
- support independent implementation and verification;
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

### 3.3 Role separation

The Planner owns planning intent. The Implementer owns implementation. The Verifier owns verification outcomes.

No role MUST modify another role's primary artifact.

### 3.4 Explicit decisions

Feedback does not automatically modify a plan.

A plan change MUST result from an explicit Planner decision. The Implementer MUST consume the canonical plan rather than infer requirements from discussion.

### 3.5 Independent verification

Implementation and verification are distinct operations.

**Implemented != Verified.** Only independent verification can produce a `Verified` task state.

### 3.6 Stable identity

Plans, tasks, findings, and feedback items MUST have stable identifiers.

Identifiers MUST NOT change when wording, status, or implementation changes.

### 3.7 Append-only feedback

Feedback MUST be append-only and owned by its author.

An agent MUST NOT rewrite feedback authored by another role.

### 3.8 Derived state

State SHOULD be derived from plan artifacts rather than stored in a central mutable record.

Do NOT introduce a database or require a central service.

### 3.9 Merge-conflict minimization

Plan and feedback artifacts SHOULD be isolated by file to minimize merge conflicts. See Section 18.

## 4. Terminology

### Plan

A durable implementation planning artifact describing the intended outcome of a unit of work, its scope, constraints, and the tasks required to achieve it.

### Task

A unit of planned implementation work within a plan.

### Finding

A discovered issue that prevents successful completion or verification. A finding is not a task. A task represents intended work; a finding represents a discovered deviation or failure.

### Feedback

Append-only communication associated with a task, a finding, or a plan.

### Feedback item

A feedback record within a feedback thread. Each feedback item has a stable identifier.

### Feedback thread

The ordered set of feedback items associated with a single subject (a plan, task, or finding).

### Feedback author

The person or agent who wrote a feedback item. The author owns their own feedback items.

### Planning iteration

One revision of a plan that preserves the stable identities of its plans, tasks, and findings.

### Planner

The role that owns planning intent and planning artifacts.

### Implementer

The role that owns repository implementation artifacts and implements planned tasks.

### Verifier

The role that independently evaluates acceptance criteria and records verification outcomes.

### Acceptance criteria

Observable conditions that must be satisfied before a task is considered implemented.

### Scope

The set of artifacts covered by a plan, expressed as file paths, directory paths, or other artifact references.

### Constraints

Non-functional or architectural limits that bound how a plan may be implemented.

### Implementation evidence

Git-native references that record how a task was implemented.

### Planning decision

An explicit, recorded Planner determination that changes or confirms the canonical plan.

### Acceptance criterion identifier

A stable identifier of the form `AC-P###-T###-NN` that identifies a single acceptance criterion within a task. Criterion identity is independent of its text.

### Verification outcome

A recorded Verifier determination of whether a task's acceptance criteria were satisfied, including its verification-independence level and evidence references.

### Verification evidence

Git-native references that record how a task was verified.

### Entity relationship

A typed connection between two PaC entities (for example a Task dependency, or a Finding's reference to a Task), addressed by stable identifiers.

### Dependency

A typed ordering or availability constraint between tasks (for example `depends-on`, `blocks`, `requires`, `conflicts-with`, `supersedes`).

### Conformance level

A named tier of PaC conformance (Core, Agent, Verified, Automated) defining the protocol features a repository or tool supports.

### Protocol invariant

A normative property of PaC artifacts that MUST hold, with a stable identifier such as `INV-001`.

## 5. Repository model

A repository MAY contain many plans.

The default layout is:

```text
.plan/
├── README.md
├── plans/
│   ├── P001.md
│   ├── P002.md
│   └── P003.md
└── feedback/
    ├── P001-T001.md
    └── P001-T001-F001.md
```

Repositories MAY define another layout in `.plan/README.md`.

A single global plan file MUST NOT be used to represent multiple unrelated plans.

Before allocating a new plan ID, an agent SHOULD scan the existing plan records and take the next sequential unused ID (for example, the next `P###` number). The allocation convention MAY be documented in `.plan/README.md`.

### 5.1 Plan README

`.plan/README.md` describes the repository's plan layout and conventions.

It SHOULD document:

- the plan layout and the paths of plan records;
- the feedback layout and the paths of feedback threads;
- the plan ID convention (for example `P###`);
- the task ID convention (for example `P###-T###`);
- the finding ID convention (for example `P###-T###-F###`);
- the feedback item ID convention (for example `P###-T###-FB###`);
- how planning iterations are represented;
- the controlled status vocabulary when a subset is used;
- the active plans when useful.

It MAY override the default layout described above.

It MUST remain human-readable and SHOULD be readable by agents for discovery.

## 6. Plans

Each plan MUST be a single Markdown file under `.plan/plans/`.

A plan MUST have:

- a stable ID;
- a title;
- a status;
- a scope;
- a Planner identity;
- creation metadata;
- a planning iteration;
- an objective;
- constraints;
- tasks.

A plan MAY have findings, decisions, and verification sections.

The recommended plan template is defined in Section 8.

A plan ID uses the recommended format `P###` (for example `P001`).

## 7. Tasks

A task represents a unit of planned implementation work within a plan.

A task MUST have:

- a stable ID;
- a title;
- a status;
- an owner role;
- a description;
- acceptance criteria.

Each acceptance criterion MUST have a stable identifier (Section 21).

A task MAY have:

- dependencies;
- scope;
- constraints;
- findings;
- implementation references;
- verification references.

A task ID uses the recommended format `P###-T###` (for example `P001-T001`).

## 8. Plan format

The canonical plan template is:

````markdown
# P001 — Title

**Status:** Draft
**Scope:** `path/`
**Planner:** planner-agent
**Created:** YYYY-MM-DD
**PaC version:** v0.2.0
**Current iteration:** 1

## Objective

Describe the intended outcome.

## Scope

Describe included and excluded artifacts.

### Included

- Item

### Excluded

- Item

## Constraints

- Constraint

## Tasks

### P001-T001 — Task title

**Status:** Planned
**Owner:** Implementer

Describe the required work.

**Depends on:**

- None

#### Acceptance

- [ ] AC-P001-T001-01 — Criterion one
- [ ] AC-P001-T001-02 — Criterion two

---

## Findings

No findings.

---

## Decisions

No decisions.

---

## Verification

Pending.
````

The template MUST remain intentionally simple.

Do NOT add implementation details unless they are required constraints.

## 9. Planning iterations

Plans MUST support evolution without changing stable IDs.

A planning iteration is one revision of a plan. Iterations are represented as human-readable sections or records within the plan file, for example:

```markdown
## Iteration 1 — Initial Plan

Initial task definition.

## Iteration 2 — Clarification

Clarified provider extension requirements.

## Iteration 3 — Verification Follow-up

Addressed verification finding.
```

The following IDs MUST remain stable across iterations:

```text
P001
P001-T001
P001-T001-F001
```

Do NOT create a new task ID merely because wording changes.

Create a new ID only for a logically distinct entity.

## 10. Task states

The normative task states are:

```text
Draft
Planned
In Progress
Implemented
Verified
Blocked
Deferred
Cancelled
```

The semantics are:

| State       | Meaning                             |
| ----------- | ----------------------------------- |
| Draft       | Task is incomplete                  |
| Planned     | Task is approved for implementation |
| In Progress | Implementation has started          |
| Implemented | Implementer reports completion      |
| Verified    | Independent verification succeeded  |
| Blocked     | Progress cannot continue            |
| Deferred    | Work intentionally postponed        |
| Cancelled   | Work intentionally abandoned        |

**Implemented != Verified.**

Only independent verification can produce the `Verified` state. An Implementer MUST NOT mark a task as Verified.

Deterministic derivation of task state from repository artifacts is defined in Section 22.

## 11. Feedback

Feedback represents append-only communication associated with a task, a finding, or a plan.

A feedback thread MUST be stored outside the plan record, in the repository's feedback layout (Section 5), using the naming convention:

```text
<subject-id>.md
```

For example:

```text
P001-T001.md
P001-T001-F001.md
P001.md
```

A feedback item MUST have:

- a stable ID;
- an author;
- a date;
- content.

A feedback item MUST NOT silently modify the canonical plan.

Each feedback item MUST have a stable identifier within its thread. The recommended feedback item ID format is derived from the subject ID:

```text
P001-T001-FB001
P001-T001-FB002
P001-T001-F001-FB001
```

Feedback items MUST be append-only. New items MUST receive new stable IDs. Previously recorded items MUST retain their original IDs and content.

Feedback items are owned by their author. A Planner MUST NOT modify an Implementer's feedback items, and an Implementer MUST NOT modify a Planner's feedback items.

Example:

```markdown
# Feedback — P001-T001

## P001-T001-FB001 — Clarification

**Author:** Implementer
**Date:** YYYY-MM-DD

Does the provider abstraction need to support
multiple providers initially?

---

## P001-T001-FB002 — Decision

**Author:** Planner
**Date:** YYYY-MM-DD

The first implementation MUST support one provider.

The abstraction SHOULD support future providers.
```

## 12. Decision recording

Feedback does not automatically modify a plan.

The canonical decision rule is:

```text
Feedback
   │
   ▼
Planner evaluates
   │
   ▼
Explicit decision
   │
   ▼
Canonical plan update
```

A plan change MUST result from an explicit Planner decision.

The Implementer MUST consume the canonical plan rather than infer requirements from discussion.

Decisions SHOULD record the outcome and a concise rationale. The plan record SHOULD record the result of a discussion, not reproduce the discussion.

### 12.1 Decision records

A planning decision MUST have a stable identifier of the form:

```text
P###-D###   (for example P001-D001)
```

Decision identifiers MUST remain stable across planning iterations.

A decision record MUST capture:

- **context** — the circumstances or feedback leading to the decision;
- **decision** — the Planner's determination;
- **rationale** — why the decision was made;
- **affected entities** — the stable IDs of the plans, tasks, or acceptance criteria affected;
- **resulting changes** — the changes made to the canonical plan.

A decision MAY reference the findings and feedback items that informed it. Plan changes MUST be traceable to decisions.

The workflow is:

```text
Feedback
    ↓
Planner decision
    ↓
Plan change
```

A feedback item MUST NOT directly modify the plan.

Example decision record:

````markdown
## Decisions

### P001-D001 — Restrict initial provider support

**Context:** Feedback in the P001-T001 thread asked whether multiple providers must be supported initially.
**Decision:** The first implementation MUST support one provider.
**Rationale:** Limits scope while preserving the abstraction for future providers.
**Affected:** P001-T001
**Resulting changes:** Constraint "only one provider initially" added to P001-T001.
````

## 13. Ownership

### 13.1 Planner

The Planner owns:

```text
.plan/plans/
```

The Planner is responsible for:

- objectives;
- scope;
- constraints;
- tasks;
- dependencies;
- acceptance criteria;
- planning decisions.

The Planner MUST NOT:

- modify implementation merely to satisfy the plan;
- independently verify implementation they authored;
- modify another author's feedback.

### 13.2 Implementer

The Implementer owns repository implementation artifacts:

```text
src/
tests/
docs/
```

The Implementer is responsible for:

- implementing tasks;
- adding tests;
- recording implementation evidence when required;
- requesting clarification through feedback.

The Implementer MUST NOT:

- change the objective;
- change acceptance criteria;
- change planner-owned decisions;
- mark implementation as independently verified.

### 13.3 Verifier

The Verifier owns verification outcomes.

The Verifier is responsible for:

- evaluating acceptance criteria;
- recording verification evidence;
- reporting findings;
- determining verification status.

The Verifier MUST NOT:

- modify implementation merely to make verification pass;
- redefine requirements;
- change the original planning intent.

### 13.4 General

The same person or agent MAY perform different roles at different times, but MUST respect the ownership boundaries of the current operation.

## 14. Workflow

### 14.1 Create a plan

The Planner creates a plan record for a defined objective and scope.

### 14.2 Planning iteration

The Planner defines tasks, dependencies, constraints, and acceptance criteria.

### 14.3 Clarification

Participants MAY exchange substantive clarification through feedback threads (Section 11).

### 14.4 Decision

The Planner evaluates feedback and records an explicit decision in the canonical plan (Section 12).

### 14.5 Implementation

The Implementer reads the canonical plan and implements accepted tasks, recording implementation evidence (Section 16).

### 14.6 Verification

The Verifier independently evaluates the acceptance criteria and records verification outcomes (Section 17).

### 14.7 Findings

If verification fails or progress is prevented, a finding is created (Section 25).

### 14.8 Additional iterations

If further work is required, the plan continues with another planning iteration. Stable IDs are preserved (Section 9).

## 15. Workflow model

```text
Planner
  │
  │ owns intent and planning
  ▼
Plan Artifact
  │
  │ consumed by
  ▼
Implementer
  │
  │ owns implementation
  ▼
Repository Artifacts
  │
  │ independently evaluated by
  ▼
Verifier
  │
  ▼
Verification Outcome
```

And every role MUST stop at its ownership boundary:

```text
Planner
  │
  └── defines what

Implementer
  │
  └── defines how

Verifier
  │
  └── determines whether
```

## 16. Implementation evidence

Implementation evidence SHOULD reference Git-native artifacts.

Examples:

```text
Commit SHA
Pull request
Changed file
Test command
Test result
```

Do NOT create a mandatory implementation database.

The exact storage location for implementation evidence MAY be configured. The default implementation SHOULD avoid requiring additional mutable files.

### 16.1 Evidence reference types

Implementation evidence SHOULD use one of the following reference types:

```text
commit
pull-request
file
test
command
artifact
```

A structured implementation evidence reference SHOULD record:

- **type** — one of the reference types above;
- **value** — a Git-native reference (for example a commit SHA or file path);
- **task** — the task the evidence implements;
- **acceptance** — the acceptance criteria it satisfies, where applicable.

Implementation evidence MUST be linkable to the task it implements and, where applicable, to the acceptance criteria it satisfies.

Example:

````markdown
## Implementation Evidence

### P001-T001

**Commit:** `abc1234`

**Changed:**

- `src/auth/provider.ts`
- `tests/auth/provider.test.ts`

**Tests:**

```text
npm test
```

**Result:** Passed
````

## 17. Verification

The Verifier MUST evaluate the plan's acceptance criteria.

Example:

```markdown
## Verification

### P001-T001

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `abc1234`
- Test: `npm test`
- Result: passed

#### Acceptance

- [x] OAuth authentication succeeds.
- [x] Authentication failures are handled.
- [x] Existing authentication remains functional.
```

If verification fails, create a finding.

### 17.1 Verification evidence

Verification evidence SHOULD use one of the following reference types:

```text
test-result
command
review
report
artifact
acceptance-evaluation
```

Each verification evidence reference MUST record an outcome. Verification evidence MUST be linkable to the task and, where applicable, to the acceptance criteria it evaluates. Verification records MUST identify the verification-independence level used (Section 26).

Example:

```markdown
### P001-T001-F001 — Authentication regression

**Status:** Open
**Severity:** Blocking

Existing password authentication fails.

#### Expected

Existing authentication MUST remain functional.

#### Evidence

```text
npm test -- auth
```

Result: failure.
```

## 18. Merge-conflict minimization

### Rule 1

One plan per file.

```text
plans/P001.md
plans/P002.md
```

Do NOT use a single file (for example `plans.yaml`) containing every plan.

### Rule 2

One feedback subject per file.

```text
feedback/P001-T001.md
feedback/P001-T002.md
```

### Rule 3

Append feedback.

Do NOT reorder existing feedback.

Do NOT rewrite another author's feedback.

### Rule 4

Avoid central mutable status files.

Do NOT create:

```text
status.yaml
dashboard.json
tasks.yaml
```

if multiple agents need to modify them.

State SHOULD be derived from plan artifacts.

## 19. Ownership enforcement

Ownership enforcement SHOULD initially be advisory.

The recommended advisory ownership mapping is:

```text
.plan/plans/**

Planner-owned

.plan/feedback/**

Append-only
Author-owned

src/**
tests/**

Implementer-owned

verification outputs

Verifier-owned
```

Repository-specific implementation paths MUST NOT be made mandatory in this specification. Repositories MUST be able to define their own implementation paths.

Optional configuration MAY be added later, for example:

```yaml
ownership:
  planner:
    - ".plan/plans/**"

  implementer:
    - "src/**"
    - "tests/**"

  verifier:
    - ".plan/verification/**"
```

## 20. Normalized data model

This section defines a normalized logical representation of PaC entities. Markdown remains the canonical representation (Section 3.1); the normalized model is a derived, machine-checkable projection used for validation and deterministic state derivation.

### 20.1 Purpose

The normalized model:

- provides a single, deterministic representation of the PaC entities that appear across plan records and feedback threads;
- establishes an unambiguous relationship between canonical Markdown and the normalized form;
- supports machine validation and deterministic derivation of task state without replacing Markdown as the system of record;
- documents any information that cannot be represented unambiguously.

### 20.2 Entities

A normalized PaC model comprises the following entities:

| Entity | Description | Key fields |
|--------|-------------|------------|
| Plan | A durable implementation planning artifact | `id`, `title`, `status`, `scope`, `planner`, `created`, `pac_version`, `current_iteration`, `objective`, `constraints`, `tasks` |
| Task | A unit of planned implementation work | `id`, `title`, `status`, `owner`, `description`, `dependencies`, `acceptance`, `findings`, `implementation_evidence`, `verification_outcomes` |
| Acceptance Criterion | An observable condition a task must satisfy | `id`, `text`, `task` |
| Finding | A discovered deviation or failure | `id`, `title`, `status`, `severity`, `description`, `references`, `disposition` |
| Feedback | An append-only thread associated with a subject | `subject_id`, `items` |
| Feedback Item | A single append-only record within a thread | `id`, `author`, `date`, `kind`, `content` |
| Planning Decision | An explicit recorded Planner determination | `id`, `context`, `decision`, `rationale`, `affected`, `resulting_changes` |
| Implementation Evidence | A Git-native reference recording how a task was implemented | `type`, `value`, `tasks`, `acceptance` |
| Verification Outcome | A Verifier determination for a task | `task`, `result`, `independence_level`, `verifier`, `evidence` |
| Verification Evidence | A Git-native reference recording how a task was verified | `type`, `value`, `outcome`, `tasks`, `acceptance` |

The details of the relationship and dependency types are defined in Sections 23 and 24.

### 20.3 Deterministic projection

Canonical Markdown MUST map to the normalized model through the projection defined in Section 29.1. The projection:

- MUST produce the same normalized representation for equivalent Markdown documents;
- MUST NOT be required to reproduce narrative prose, hyperlinks, or other non-projectable content;
- MUST document any information that cannot be represented unambiguously.

```text
Canonical Markdown
        ↓
Normalized PaC Model
        ↓
Validation / Derived State
```

### 20.4 Optionality

The normalized model is optional tooling. It MUST NOT replace Markdown as the source of truth. A repository MUST remain fully usable with only Markdown and Git.

## 21. Acceptance criterion identifiers

Each acceptance criterion MUST have a stable identifier of the form:

```text
AC-P###-T###-NN
```

For example:

```text
AC-P001-T002-01
AC-P001-T002-02
```

The identifier is allocated by the Planner and MAY be allocated sequentially within a task.

The following rules apply:

- Criterion identity MUST remain stable when wording, status, or implementation changes.
- Each criterion MUST belong to exactly one task.
- The identifier format MUST be documented and validated.
- Verification records MUST be able to reference criterion identifiers (Section 17).
- Acceptance criteria MUST NOT be reused across tasks; moving a criterion between tasks changes its identity and requires a new identifier.

### 21.1 Compatibility path

Plans recorded before acceptance-criterion identifiers were defined SHOULD assign identifiers to existing acceptance criteria by task order during migration. Once assigned, identifiers MUST remain stable.

## 22. Deterministic task-state derivation

Task state MUST be derivable from repository artifacts rather than stored in a central mutable record (Section 3.8).

### 22.1 Inputs

The derivation MAY use the following repository artifacts:

- the canonical plan record, including the task status recorded by the owning role;
- implementation evidence references (Section 16);
- verification outcomes and verification evidence (Sections 17 and 26);
- findings associated with the task (Section 25);
- recorded planning decisions (Section 12).

The derived state MUST be one of:

```text
Draft
Planned
In Progress
Implemented
Verified
Blocked
Deferred
Cancelled
```

### 22.2 Precedence

Where multiple conditions apply, the derivation MUST apply the following precedence, highest first:

```text
Cancelled
Deferred
Blocked
Verified
Implemented
In Progress
Planned
Draft
```

### 22.3 Requirements

- `Implemented` requires implementation evidence.
- `Verified` requires independent verification evidence that satisfies the repository's configured verification requirement (Section 26).
- `Implemented` MUST NOT imply `Verified`.
- A blocking finding MUST prevent the affected task from being derived as `Verified` or `Implemented` until it is resolved, accepted, or superseded (Section 25).
- The derivation MUST produce the same derived state for equivalent repositories.

## 23. Dependencies

A task MAY declare relationships to other tasks. Each relationship MUST use one of the following types:

```text
depends-on
blocks
requires
conflicts-with
supersedes
```

### 23.1 Relationship semantics

| Type | Direction | Meaning |
|------|-----------|---------|
| `depends-on` | task → target | The task MUST NOT start implementation until the target is implemented. |
| `blocks` | task → target | The task impedes progress of the target until the task is completed. |
| `requires` | task → target | The task requires an artifact or outcome produced by the target. |
| `conflicts-with` | task → target | The task and the target MUST NOT be implemented or active in the same scope at the same time. |
| `supersedes` | task → target | The task replaces the target; the target is no longer the intended work. |

`requires` is stricter than `depends-on`: it additionally asserts that the target's outcome is available to the task.

### 23.2 Validation

Relationships MUST be validated for:

- missing references — a reference to a task that does not exist;
- invalid references — a reference that does not resolve to a Task entity or violates the reference format;
- self-references — a task referencing itself;
- dependency cycles — a cycle among `depends-on` or `requires` relationships;
- invalid relationship combinations — combinations that contradict the semantics (for example a task both `depends-on` and `conflicts-with` the same target).

### 23.3 Representation

A task MAY declare typed relationships in a `**Relationships:**` field, one per bullet, using `<type> <target>` form:

```text
**Relationships:**

- conflicts-with P001-T002
- requires P001-T003
```

The `**Depends on:**` field is shorthand for `depends-on` relationships and MUST be treated as `depends-on` when validating.

Valid dependency graphs MUST pass validation. Detection of these conditions is machine-checkable (Section 28).

## 24. Entity relationships

PaC entities MUST be able to reference each other through typed relationships addressed by stable identifiers.

### 24.1 Supported relationships

The normalized model MUST support traceability equivalent to:

```text
Plan
 └── Task
      ├── Acceptance Criterion
      ├── Implementation Evidence
      ├── Verification Outcome
      └── Finding

Finding
 └── Feedback
      └── Planning Decision
```

### 24.2 Rules

- Relationship targets MUST use stable identifiers (for example `P001-T002`, `AC-P001-T002-01`, `P001-T001-F001`, `P001-D001`).
- Invalid references MUST be detectable by validation (Section 28).
- Plan-to-verification traceability MUST be possible: a Plan leads to Tasks, each with Verification Outcomes that reference Acceptance Criteria and Verification Evidence.
- Finding-to-decision traceability MUST be possible: a Finding leads to Feedback, and a Feedback thread leads to a Planning Decision.

## 25. Finding lifecycle

A finding has a defined lifecycle. The supported states are:

```text
Open
Acknowledged
Resolved
Accepted
Invalid
Superseded
```

The semantics are:

| State | Meaning |
|-------|---------|
| Open | Discovered, not yet dispositioned. |
| Acknowledged | Recognized by the responsible role. |
| Resolved | The deviation was corrected. |
| Accepted | The deviation is tolerated by explicit decision. |
| Invalid | The finding was rejected as not valid. |
| Superseded | The finding was replaced by another finding. |

### 25.1 Rules

- Findings MUST remain distinct from tasks. A task represents intended work; a finding represents a discovered deviation or failure.
- Findings MUST have stable identifiers (Section 3.6).
- A finding MUST be able to reference the affected tasks and acceptance criteria.
- When a finding requires implementation work, the resulting task MUST be explicitly created through the planning process rather than implicitly created by the finding.
- A finding's disposition MUST be traceable to a planning decision (Section 12).
- A blocking finding MUST affect derived task state as defined in Section 22.

## 26. Verification independence

Verification MUST distinguish self-verification from independent verification.

### 26.1 Independence levels

The protocol supports the following levels:

| Level | Name | Meaning |
|-------|------|---------|
| 0 | Self verification | The Implementer verifies their own work. |
| 1 | Separate verification operation | A distinct verification operation is performed. |
| 2 | Separate agent/context | Verification is performed in a separate agent session or context. |
| 3 | Independent actor/model context | Verification is performed by an actor or model independent of the Implementer. |
| 4 | Human or externally independent verification | A human or external party verifies the work. |

### 26.2 Requirements

- A repository MUST be able to specify the minimum level required for `Verified`.
- The minimum level MAY be declared in `.plan/README.md` or in the plan record.
- Verification records MUST identify the independence level used.
- State derivation MUST respect the configured verification requirement (Section 22).

## 27. Conformance levels

The protocol defines four conformance levels. Higher levels build on lower levels.

### PaC Core

Canonical plans, stable IDs, tasks, and acceptance criteria.

### PaC Agent

Core plus ownership, feedback, decisions, and agent procedures.

### PaC Verified

Agent plus evidence, findings, and independent verification.

### PaC Automated

Verified plus normalized representation, automated validation, relationship validation, and deterministic state derivation.

### 27.1 Rules

- A repository MUST be able to declare its supported conformance level.
- A tool MUST be able to declare its supported conformance level.
- Core PaC usage MUST remain possible without automation.
- The declaration MAY be recorded in `.plan/README.md` or in a plan record.

## 28. Protocol invariants

The following invariants MUST hold for conforming PaC artifacts. Each invariant has a stable identifier.

```text
INV-001 — Plan IDs are unique.
INV-002 — Task IDs are unique.
INV-003 — Every Task belongs to a Plan.
INV-004 — Every Acceptance Criterion belongs to one Task.
INV-005 — Relationship targets exist.
INV-006 — Invalid dependency cycles are rejected.
INV-007 — Verified requires independent verification.
INV-008 — Implementation evidence cannot alone produce Verified.
INV-009 — Findings have stable IDs.
INV-010 — Feedback is append-only.
INV-011 — Plan changes are traceable to decisions.
INV-012 — Artifact ownership boundaries are respected.
INV-013 — Contradictory relationship combinations are rejected.
```

### 28.1 Checkability

- Every invariant MUST be machine-checkable where applicable.
- Invalid artifacts MUST produce actionable validation failures that identify the invariant and the offending artifact.
- Validation MUST cover identity, relationships, state, evidence, and ownership.
- Invariant validation MUST be covered by automated tests.

## 29. Human-readable format

Markdown is the canonical default format.

Machine-readable representations MAY be generated for validation or automation but SHOULD NOT replace the human-readable plan artifact.

### 29.1 Markdown-to-schema projection

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
| `**Current iteration:**` | `current_iteration` (integer) |
| `## Objective` section content | `objective` |
| `## Constraints` section items | `constraints` (array of strings) |
| `### P001-T001 — Task title` heading | task `id` (`P001-T001`) and task `title` |
| Task `**Status:**` | task `status` |
| Task `**Owner:**` | task `owner` |
| Task description paragraph | task `description` |
| Task `**Depends on:**` items | task `dependencies` (array of strings) |
| Task `**Relationships:**` items | task `relationships` (array of strings in `<type> <target>` form) |
| Task `#### Acceptance` checkbox list | task `acceptance` (array of objects with `id` derived from the leading `AC-...-NN` marker and `text` from the item text without the `- [ ]` marker) |
| `### P001-T001-F001 — Finding title` heading under `## Findings` | finding `id` and finding `title` |
| Finding `**Status:**` | finding `status` (finding lifecycle, Section 25) |
| Finding `**Severity:**` | finding `severity` |
| Finding `#### References` items | finding `references` (array of stable IDs) |
| Finding `#### Resolution` content | finding `resolution` |
| `### P001-D001 — Decision title` heading under `## Decisions` | decision `id` (`P001-D001`) and decision `title` |
| Decision `**Context:**` line | decision `context` |
| Decision `**Decision:**` line | decision `decision` |
| Decision `**Rationale:**` line | decision `rationale` |
| Decision `**Affected:**` line | decision `affected` (array of stable IDs) |
| Decision `**Resulting changes:**` line | decision `resulting_changes` |
| `### P001-T001` heading under `## Verification` | verification `task` (`P001-T001`) |
| Verification `**Status:**` | verification `status` |
| Verification `**Verifier:**` line | verification `verifier` |
| Verification `**Independence:** Level N` line | verification `independence_level` (integer 0–4) |
| Verification `#### Evidence` items | verification `evidence` (array of `{type, value}` references) |
| Verification `#### Acceptance` checkbox list | verification `acceptance` (array of `{id, result}`) |

Fields that appear in the Markdown but have no schema property (for example links or narrative prose) are not projected.

Feedback thread (`schemas/feedback.schema.json`):

| Markdown element | Schema property |
|------------------|-----------------|
| `# Feedback — P001-T001` heading | `subject_id` (`P001-T001`) |
| `## P001-T001-FB001 — Clarification` heading | item `id` (the full `P001-T001-FB001`, derived from the subject ID and the `FB###` number; for finding-scoped threads, for example `P001-T001-F001-FB001`) and item `kind` (text after the em dash) |
| `**Author:**` line | item `author` |
| `**Date:**` line | item `date` |
| Item content paragraph | item `content` |

## 30. Agent interoperability

Agents MUST distinguish:

```text
Intended work (Task)
Discovered deviation (Finding)
Clarification (Feedback)
Decision
Implementation
Verification
```

These concepts are not interchangeable.

Agents MUST determine their current operation and ownership boundary before writing.

Agents MUST:

- preserve stable IDs;
- read the complete canonical plan before starting implementation;
- record canonical decisions in the plan when acting as Planner;
- record reproducible verification evidence when acting as Verifier;
- evaluate repository artifacts rather than rely solely on implementation claims when acting as Verifier.

Agents MUST NOT:

- change acceptance criteria;
- implement a task outside the assigned role;
- modify feedback authored by another role;
- claim verification without evidence;
- modify another role's primary artifact.

### 30.1 Discovery

Before operating, an agent SHOULD:

1. read repository instructions such as `AGENTS.md`;
2. locate `.plan/README.md` if present and read it for layout, ID formats, and active plans;
3. locate the applicable plan record and any applicable feedback threads;
4. identify the agent's assigned role and corresponding ownership boundary;
5. identify the assigned task;
6. check task dependencies;
7. execute only allowed work within the ownership boundary;
8. record evidence and stop at the role boundary.

## 31. Conformance

Conformance levels are defined in Section 27.

A PaC implementation conforms to v0.2.0 when it:

1. supports multiple plan records per repository;
2. provides stable plan, task, finding, and feedback IDs;
3. preserves Planner/Implementer/Verifier ownership boundaries;
4. distinguishes intended work from discovered findings;
5. distinguishes feedback from decisions;
6. distinguishes implementation from verification;
7. provides a human-readable plan representation;
8. supports append-only, git-managed feedback records;
9. derives state from plan artifacts without a central mutable registry.

## 32. Migration from v0.1.0

This section documents how existing PaC v0.1.0 artifacts can be migrated to v0.2.0. Migration SHOULD preserve stable identifiers.

### 32.1 Acceptance criteria

v0.1.0 acceptance criteria are plain checkbox items without identifiers. During migration, assign identifiers in task order using the form `AC-<plan>-<task>-<nn>` (Section 21). Once assigned, identifiers MUST remain stable.

### 32.2 Findings

v0.1.0 findings with a `**Status:**` of `Open`, `Resolved`, or another value SHOULD be mapped to the lifecycle vocabulary (Section 25). Unrecognized statuses SHOULD map to `Open` until dispositioned.

### 32.3 Decisions

v0.1.0 decision discussions recorded only in feedback threads SHOULD be promoted to `## Decisions` records with `P###-D###` identifiers where they resulted in a plan change (Section 12).

### 32.4 Verification

v0.1.0 verification records SHOULD be extended with `**Independence:**` levels (Section 26) and structured evidence references (Section 17). Verification records without a stated level are treated as Level 1 (separate verification operation).

### 32.5 Conformance

A repository MAY declare its conformance level (Section 27). Migration to a higher level than the repository previously supported is a separate decision.

### 32.6 No automatic rewrite

Migration MUST NOT require an automated rewrite. Existing valid v0.1.0 records remain readable; the identifiers and structure above are additive.

## 33. Fundamental invariant

> The Planner defines what. The Implementer defines how. The Verifier determines whether.

The same human or agent MAY perform multiple roles at different times, but MUST NOT collapse ownership boundaries within a single operation.
