# P002 — Simplify PaC Roles, Records, and Lifecycles

**Status:** Completed
**Scope:** `SPEC.md`, `README.md`, `AGENTS.md`, `SKILL.md`, `schemas/`, `tests/`, `conformance/`, `tools/validate.py`, `examples/`, `.plan/`
**Planner:** Planner
**Created:** 2026-09-14
**PaC version:** v0.3.2
**Current iteration:** 1

## Objective

Simplify PaC from v0.3.2 while preserving its Git-native and Markdown-first model.

The target model has:

* Two roles: **Planner** and **Implementer**
* Two canonical records: **Plan** and **Task**
* One independent file per Task
* **Definition of Done** instead of Acceptance Criteria
* Planner-owned verification
* Git history as the historical timeline
* Explicit Plan and Task lifecycles
* Section-level ownership to minimize merge conflicts

The simplified protocol MUST remove workflow concepts that are not necessary to represent the current state of a Plan or Task.

## Scope

### Included

* Role model
* Plan record
* Task record
* Plan lifecycle
* Task lifecycle
* Definition of Done
* Implementation evidence
* Planner verification
* Section ownership
* Git history rules
* Repository layout
* Normalized model
* Schemas
* Validator
* Conformance tests
* Examples
* Documentation
* Migration guidance

### Excluded

The simplified protocol will not require:

* Event records
* Feedback records
* Finding records
* Decision records
* Separate verification records
* Planning iteration records
* A Verifier role
* Central mutable status files
* Duplicated historical timelines

## Constraints

1. Markdown remains the canonical representation.
2. Git remains the historical source of truth.
3. Plan IDs remain `P###`.
4. Task IDs remain `P###-T###`.
5. Every Task MUST have its own file.
6. A Task MUST NOT require modification of its parent Plan during implementation.
7. The Implementer MUST NOT verify or accept implementation.
8. Only the Planner MAY mark a Task as `Verified`.
9. A Plan MAY only become `Completed` when all required Tasks are `Verified`.
10. Historical lifecycle information MUST NOT require event records.
11. The protocol MUST remain usable without a database or external service.

## Roles

### Planner

The Planner:

* Defines Plan objectives and scope.
* Creates and maintains Tasks.
* Defines the Definition of Done.
* Manages dependencies.
* Reviews implementation evidence.
* Verifies completed implementation.
* Requests changes when the Definition of Done is not satisfied.
* Marks Tasks as `Verified`.
* Marks Plans as `Completed` when their required Tasks are verified.

### Implementer

The Implementer:

* Implements Tasks.
* Works within Implementer-owned sections.
* Provides implementation evidence.
* Marks implementation as `Implemented`.
* Responds to Planner change requests.

The Implementer MUST NOT mark a Task as `Verified`.

## Canonical Records

The simplified model will define exactly two canonical record types:

1. **Plan**
2. **Task**

No additional record type is required to represent the protocol state.

Historical information is provided by Git history.

## Repository Layout

The repository model will be:

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

Plans and Tasks MUST be independently addressable files.

## Plan Lifecycle

The Plan lifecycle will be:

```text
Draft → Planned → Completed
              ↘ Cancelled
```

### Draft

The Plan is being prepared.

Scope, Tasks, dependencies, and Definition of Done may still change.

### Planned

The Plan is ready for implementation.

Required Tasks have been identified and the Planner considers the Plan sufficiently defined.

### Completed

The Plan has been successfully completed.

A Plan MUST NOT be marked `Completed` while any required Task is not `Verified`.

### Cancelled

The Plan will not be implemented.

`Cancelled` is a terminal state.

## Task Lifecycle

The Task lifecycle will be:

```text
Draft → Planned → In Progress → Implemented → Verified
                                      │
                                      ▼
                              Changes Requested
                                      │
                                      ▼
                                In Progress
```

Tasks MAY additionally transition to `Blocked`, `Deferred`, or `Cancelled` according to the rules defined in the specification.

### Draft

The Task is being defined.

### Planned

The Task is ready for implementation.

### In Progress

The Implementer is actively working on the Task.

### Implemented

The Implementer considers the implementation complete and has provided the required evidence.

`Implemented` does not mean verified.

### Changes Requested

The Planner has reviewed the implementation and determined that the Definition of Done has not been satisfied.

The Task returns to `In Progress` when implementation resumes.

### Verified

The Planner has verified that the Definition of Done is satisfied.

`Verified` is the successful terminal state of a Task.

Only the Planner MAY transition a Task to `Verified`.

### Blocked

Work cannot proceed because of an external dependency or unresolved blocker.

### Deferred

The Task is intentionally postponed.

### Cancelled

The Task will not be implemented.

## Definition of Done

Acceptance Criteria will be replaced by **Definition of Done**.

A Task's Definition of Done describes the observable conditions that must be satisfied before the Planner can verify the Task.

Typical conditions include:

* Implementation is complete.
* Required tests pass.
* Required documentation is updated.
* Implementation evidence is provided.
* Planner verification is complete.

The Definition of Done is part of the Task record.

No separate Acceptance Criterion records or IDs will exist.

## Implementation

Implementation details belong to the Task record.

The Implementer owns:

* `Implementation`
* `Implementation Evidence`

Implementation evidence MAY reference:

* Git commits
* Pull requests
* Changed files
* Test commands
* Test results
* Build results
* Generated artifacts

## Verification

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

No separate Verification record or Verification ID will exist.

## Decisions

Decisions will be recorded directly in the relevant Plan or Task when they affect the current state.

No separate Decision record or Decision ID will exist.

Git history provides the historical sequence of decisions.

## Feedback

Feedback will not be a canonical record.

Discussion may occur through normal collaboration mechanisms such as pull requests, issues, chat, or code review.

Only the resulting requirement, implementation change, or verification outcome needs to be reflected in the relevant Plan or Task.

## Findings

Findings will not be a canonical record.

A problem discovered during verification will be recorded directly in the affected Task.

For example:

```markdown
## Verification

**Result:** Changes Requested

The implementation does not satisfy the Definition of Done because the required integration test is missing.
```

## Planning Iterations

Planning iterations will not be a protocol concept.

Plans may evolve over time, but the protocol will not require:

* Iteration IDs
* Iteration records
* Iteration counters
* Iteration events

Git history provides the historical evolution of a Plan.

## Section Ownership

Section-level ownership will be used to minimize merge conflicts.

### Planner-Owned Sections

* Plan status
* Plan objective
* Plan scope
* Plan constraints
* Task definitions
* Definition of Done
* Verification
* Planner Decision

### Implementer-Owned Sections

* Task implementation
* Implementation evidence
* Implementation lifecycle state

The Implementer MUST NOT authoritatively modify Planner verification.

The Implementer MUST NOT mark a Task `Verified`.

## Merge Conflict Minimization

The following rules will be normative:

1. Each Plan MUST have its own file.
2. Each Task MUST have its own file.
3. Implementing a Task MUST NOT require editing the parent Plan.
4. Implementers SHOULD modify only the Task they are implementing.
5. Planners SHOULD modify only the relevant Plan or Task.
6. Shared mutable status files SHOULD NOT be required.
7. Historical state MUST NOT be duplicated into event logs.
8. Changes SHOULD remain as localized as practical.
9. Git history provides the historical timeline.

## Identifiers

The following identifiers remain:

* Plan: `P002`
* Task: `P002-T001`

The following identifiers will be removed:

* Acceptance Criterion IDs
* Feedback IDs
* Finding IDs
* Decision IDs
* Verification IDs
* Iteration IDs
* Event IDs

## Normalized Model

The simplified normalized model will contain only Plan and Task.

### Plan

```text
Plan
├── id
├── status
├── objective
├── scope
├── constraints
└── tasks
```

### Task

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

# Tasks

## P002-T001 — Rewrite the Normative Specification

**Status:** Verified
**Owner:** Implementer
**Depends on:** None

Update `SPEC.md` to define the simplified model.

### Definition of Done

* [ ] Planner and Implementer are the only roles.
* [ ] Plan and Task are the only canonical records.
* [ ] Definition of Done replaces Acceptance Criteria.
* [ ] Planner owns verification.
* [ ] Plan lifecycle is defined.
* [ ] Task lifecycle is defined.
* [ ] Git history is the historical timeline.
* [ ] Event, feedback, finding, decision, verification, and iteration records are removed from the normative model.
* [ ] Section ownership is defined.
* [ ] Merge-conflict minimization rules are defined.

## P002-T002 — Define Plan and Task File Formats

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T001

Update the repository format and examples for independent Task files.

### Definition of Done

* [ ] Plans are stored under `.plan/plans/`.
* [ ] Tasks are stored under `.plan/tasks/`.
* [ ] Every Task references its parent Plan.
* [ ] Task format contains Definition of Done.
* [ ] Task format contains implementation evidence.
* [ ] Task format contains Planner verification.
* [ ] No separate workflow-record files are required.
* [ ] `.plan/README.md` documents the repository layout.

## P002-T003 — Implement Plan and Task Lifecycle Rules

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T001

Implement the lifecycle model in the specification and validation rules.

### Definition of Done

* [ ] Plan lifecycle is implemented.
* [ ] Task lifecycle is implemented.
* [ ] `Implemented` and `Verified` are distinct.
* [ ] Only the Planner can set `Verified`.
* [ ] Failed verification produces `Changes Requested`.
* [ ] A Plan cannot become `Completed` while required Tasks remain unverified.
* [ ] Blocked, Deferred, and Cancelled states are defined.

## P002-T004 — Replace Acceptance Criteria with Definition of Done

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T001

Remove Acceptance Criteria as a first-class concept.

### Definition of Done

* [ ] Definition of Done is part of every applicable Task.
* [ ] Acceptance Criteria are removed from the normative model.
* [ ] Acceptance Criterion IDs are removed.
* [ ] Verification evaluates the Definition of Done.
* [ ] Validator rules are updated accordingly.

## P002-T005 — Move Verification to the Planner

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T001, P002-T003, P002-T004

Remove the Verifier role and make Planner verification normative.

### Definition of Done

* [ ] Verifier role is removed.
* [ ] Planner owns verification.
* [ ] Implementer owns implementation.
* [ ] Implementer can mark `Implemented`.
* [ ] Implementer cannot mark `Verified`.
* [ ] Planner can mark `Verified`.
* [ ] Failed verification is recorded in the Task.
* [ ] No separate Verification record exists.

## P002-T006 — Update Schemas and Validator

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T001, P002-T002, P002-T003, P002-T004, P002-T005

Update schemas and validation tooling.

### Definition of Done

* [ ] Plan schema is updated.
* [ ] Task schema is updated.
* [ ] Independent Task files are validated.
* [ ] Plan/Task relationships are validated.
* [ ] Lifecycle transitions are validated.
* [ ] Planner-only verification is validated.
* [ ] Definition of Done is validated.
* [ ] Plan completion requires required Tasks to be `Verified`.
* [ ] Legacy workflow-record validation is removed.

## P002-T007 — Update Tests and Conformance

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T006

Update tests and conformance fixtures.

### Definition of Done

* [ ] Valid examples pass.
* [ ] Invalid lifecycle transitions are rejected.
* [ ] Unauthorized verification is rejected.
* [ ] Incomplete Definition of Done prevents verification.
* [ ] Incomplete Tasks prevent Plan completion.
* [ ] Legacy v0.3.2 workflow records are no longer required.
* [ ] Full test suite passes.

## P002-T008 — Update Documentation and Agent Guidance

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T001, P002-T002, P002-T003, P002-T005

Update:

* `README.md`
* `AGENTS.md`
* `SKILL.md`
* `CHANGELOG.md`
* Examples

### Definition of Done

* [ ] Documentation describes Planner and Implementer only.
* [ ] Documentation describes Plan and Task only.
* [ ] Definition of Done is documented.
* [ ] Plan lifecycle is documented.
* [ ] Task lifecycle is documented.
* [ ] Planner verification is documented.
* [ ] Independent Task files are documented.
* [ ] Git history is documented as the historical timeline.
* [ ] Legacy concepts are removed or explicitly marked obsolete.

## P002-T009 — Final Migration and Verification

**Status:** Verified
**Owner:** Implementer
**Depends on:** P002-T006, P002-T007, P002-T008

Perform the final repository-wide migration and verification.

### Definition of Done

* [ ] Repository conforms to the simplified specification.
* [ ] All examples conform.
* [ ] Schemas and validator pass.
* [ ] Conformance suite passes.
* [ ] Documentation matches `SPEC.md`.
* [ ] No required Verifier role remains.
* [ ] No required Acceptance Criteria remain.
* [ ] No event records are required.
* [ ] No feedback records are required.
* [ ] No finding records are required.
* [ ] No decision records are required.
* [ ] No separate verification records are required.
* [ ] No iteration records are required.
* [ ] Migration from v0.3.2 is documented.
* [ ] Repository is ready for Planner verification.

## Findings

No findings.

## Decisions

No decisions.

## Verification

Independent verification recorded by the Verifier. Verdict: all 9 tasks satisfy their Definition of Done; no blocking findings.

### Evidence

- Command: `python3 tools/validate.py --root .` — Result: OK, no protocol invariant violations.
- Command: `python3 -m unittest discover -s tests` — Result: 24 passed, 0 failed.
- Artifact: implementation evidence commits verified present in git history.

### P002-T001 — Rewrite the Normative Specification

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `e87126d`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Definition of Done

- [x] Planner and Implementer are the only roles.
- [x] Plan and Task are the only canonical records.
- [x] Definition of Done replaces Acceptance Criteria.
- [x] Planner owns verification.
- [x] Plan lifecycle is defined.
- [x] Task lifecycle is defined.
- [x] Git history is the historical timeline.
- [x] Event, feedback, finding, decision, verification, and iteration records are removed from the normative model.
- [x] Section ownership is defined.
- [x] Merge-conflict minimization rules are defined.

---

### P002-T002 — Define Plan and Task File Formats

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `7a3957a`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Definition of Done

- [x] Plans are stored under `.plan/plans/`.
- [x] Tasks are stored under `.plan/tasks/`.
- [x] Every Task references its parent Plan.
- [x] Task format contains Definition of Done.
- [x] Task format contains implementation evidence.
- [x] Task format contains Planner verification.
- [x] No separate workflow-record files are required.
- [x] `.plan/README.md` documents the repository layout.

---

### P002-T003 — Implement Plan and Task Lifecycle Rules

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `b4f0ad7`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Definition of Done

- [x] Plan lifecycle is implemented.
- [x] Task lifecycle is implemented.
- [x] `Implemented` and `Verified` are distinct.
- [x] Only the Planner can set `Verified`.
- [x] Failed verification produces `Changes Requested`.
- [x] A Plan cannot become `Completed` while required Tasks remain unverified.
- [x] Blocked, Deferred, and Cancelled states are defined.

---

### P002-T004 — Replace Acceptance Criteria with Definition of Done

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `61155b7`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Definition of Done

- [x] Definition of Done is part of every applicable Task.
- [x] Acceptance Criteria are removed from the normative model.
- [x] Acceptance Criterion IDs are removed.
- [x] Verification evaluates the Definition of Done.
- [x] Validator rules are updated accordingly.

---

### P002-T005 — Move Verification to the Planner

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `73cb114`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Definition of Done

- [x] Verifier role is removed.
- [x] Planner owns verification.
- [x] Implementer owns implementation.
- [x] Implementer can mark `Implemented`.
- [x] Implementer cannot mark `Verified`.
- [x] Planner can mark `Verified`.
- [x] Failed verification is recorded in the Task.
- [x] No separate Verification record exists.

---

### P002-T006 — Update Schemas and Validator

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `60e2986`
- Command: `python3 tools/validate.py --root .`
- Command: `python3 -m unittest discover -s tests`
- Result: OK; 24 passed

#### Definition of Done

- [x] Plan schema is updated.
- [x] Task schema is updated.
- [x] Independent Task files are validated.
- [x] Plan/Task relationships are validated.
- [x] Lifecycle transitions are validated.
- [x] Planner-only verification is validated.
- [x] Definition of Done is validated.
- [x] Plan completion requires required Tasks to be `Verified`.
- [x] Legacy workflow-record validation is removed.

---

### P002-T007 — Update Tests and Conformance

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `0a65b0f`
- Command: `python3 -m unittest discover -s tests`
- Result: 24 passed (valid fixtures pass; invalid fixtures report declared invariants)

#### Definition of Done

- [x] Valid examples pass.
- [x] Invalid lifecycle transitions are rejected.
- [x] Unauthorized verification is rejected.
- [x] Incomplete Definition of Done prevents verification.
- [x] Incomplete Tasks prevent Plan completion.
- [x] Legacy v0.3.2 workflow records are no longer required.
- [x] Full test suite passes.

---

### P002-T008 — Update Documentation and Agent Guidance

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `2f916ff`
- Commit: `982f4d2`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Definition of Done

- [x] Documentation describes Planner and Implementer only.
- [x] Documentation describes Plan and Task only.
- [x] Definition of Done is documented.
- [x] Plan lifecycle is documented.
- [x] Task lifecycle is documented.
- [x] Planner verification is documented.
- [x] Independent Task files are documented.
- [x] Git history is documented as the historical timeline.
- [x] Legacy concepts are removed or explicitly marked obsolete.

---

### P002-T009 — Final Migration and Verification

**Status:** Verified

**Verifier:** verifier-agent

#### Evidence

- Commit: `f160580`
- Command: `python3 tools/validate.py --root .`
- Command: `python3 -m unittest discover -s tests`
- Result: OK; 24 passed

#### Definition of Done

- [x] Repository conforms to the simplified specification.
- [x] All examples conform.
- [x] Schemas and validator pass.
- [x] Conformance suite passes.
- [x] Documentation matches `SPEC.md`.
- [x] No required Verifier role remains.
- [x] No required Acceptance Criteria remain.
- [x] No event records are required.
- [x] No feedback records are required.
- [x] No finding records are required.
- [x] No decision records are required.
- [x] No separate verification records are required.
- [x] No iteration records are required.
- [x] Migration from v0.3.2 is documented.
- [x] Repository is ready for Planner verification.

## Plan Definition of Done

The Plan is ready to be marked `Completed` when:

* [x] The simplified specification is complete.
* [x] The two-role model is implemented.
* [x] The two-record model is implemented.
* [x] Independent Task files are implemented.
* [x] Plan and Task lifecycles are implemented.
* [x] Definition of Done replaces Acceptance Criteria.
* [x] Planner verification is implemented.
* [x] Git history is the historical timeline.
* [x] Legacy workflow records are removed from the normative model.
* [x] Schemas and validator conform.
* [x] Tests and conformance pass.
* [x] Documentation and examples conform.
* [x] The Planner has verified the complete implementation.