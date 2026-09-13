# P001 — Strengthen PaC Protocol Semantics and Conformance

**Status:** Closed
**Scope:** PaC specification, schemas, examples, validation fixtures, and agent documentation
**Planner:** architecture-review
**Created:** 2026-09-13
**PaC version:** v0.3.2
**Current iteration:** 2

## Objective

Strengthen Plan as Code so that its protocol semantics are deterministic, machine-validatable, and suitable for human and AI-agent workflows while preserving its core principles:

* Markdown remains canonical.
* Git remains the system of record.
* Plans have stable identifiers.
* Planner, Implementer, and Verifier responsibilities remain separated.
* Feedback remains append-only.
* Implementation and verification remain distinct.
* No centralized database is required.

The implementation should make PaC a more precise interoperability protocol without turning the core format into a complex project-management system.

## Scope

### Included

* Normalized PaC data model.
* Stable acceptance-criterion identifiers.
* Deterministic task-state derivation.
* Explicit dependency semantics.
* Explicit entity relationships.
* First-class planning-decision representation.
* Finding lifecycle.
* Verification-independence representation.
* Implementation and verification evidence.
* Conformance levels.
* Machine-checkable protocol invariants.
* Conformance fixtures.
* Updated schemas.
* Updated specification.
* Migration guidance.
* Updated agent documentation.

### Excluded

* Centralized PaC service or database.
* Mandatory CLI.
* SaaS functionality.
* Vendor-specific AI-agent integration.
* Replacement of Markdown as the canonical representation.
* General project-management functionality.

## Constraints

* Markdown MUST remain the canonical representation.
* Existing stable identifiers SHOULD remain valid.
* Core PaC usage MUST remain possible without automation.
* New semantics SHOULD be machine-validatable.
* Implementation tasks MUST be executable by the Implementer.
* The Planner MUST NOT be represented as the executor of implementation tasks.
* Verification MUST remain independent of implementation.
* Feedback MUST NOT directly mutate the plan.
* Planning decisions MUST explicitly authorize plan changes.
* A task MUST NOT become `Verified` merely because implementation evidence exists.

# Tasks

## P001-T001 — Implement the normalized PaC data model

**Status:** Verified
**Owner:** Implementer

Implement a normalized logical representation of PaC entities while retaining Markdown as the canonical representation.

The implementation MUST represent, at minimum:

* Plan
* Task
* Acceptance Criterion
* Finding
* Feedback
* Planning Decision
* Implementation Evidence
* Verification Outcome
* Verification Evidence

The implementation MUST establish a deterministic relationship between canonical Markdown and the normalized representation.

```text
Canonical Markdown
        ↓
Normalized PaC Model
        ↓
Validation / Derived State
```

### Acceptance

* [ ] AC-P001-T001-01 — A normalized representation exists for all required PaC entities.
* [ ] AC-P001-T001-02 — Canonical Markdown can be mapped to the normalized representation.
* [ ] AC-P001-T001-03 — The normalized representation does not replace Markdown as the source of truth.
* [ ] AC-P001-T001-04 — Equivalent PaC documents produce equivalent normalized representations.
* [ ] AC-P001-T001-05 — The implementation documents any information that cannot be represented unambiguously.

---

## P001-T002 — Implement stable acceptance-criterion identifiers

**Status:** Verified
**Owner:** Implementer

Extend task acceptance criteria with stable identifiers.

Use the following form:

```text
AC-P001-T002-01
AC-P001-T002-02
```

Acceptance criterion identity MUST remain stable when wording, status, or implementation changes.

Each criterion MUST belong to exactly one task.

### Acceptance

* [ ] AC-P001-T002-01 — Acceptance criteria have stable identifiers.
* [ ] AC-P001-T002-02 — Identifier format is documented and validated.
* [ ] AC-P001-T002-03 — Criterion identity is independent of its text.
* [ ] AC-P001-T002-04 — Each criterion belongs to exactly one task.
* [ ] AC-P001-T002-05 — Verification records can reference criterion IDs.
* [ ] AC-P001-T002-06 — Existing plans have a documented compatibility path.

**Depends on:** P001-T001

---

## P001-T003 — Implement deterministic task-state derivation

**Status:** Verified
**Owner:** Implementer

Implement deterministic derivation of task state from repository artifacts.

The implementation MUST distinguish:

```text
Planned
In Progress
Implemented
Verified
Blocked
Deferred
Cancelled
```

The implementation MUST define precedence where multiple conditions apply.

At minimum:

```text
Cancelled
Deferred
Blocked
Verified
Implemented
In Progress
Planned
```

The implementation MUST ensure:

```text
Implemented ≠ Verified
```

`Verified` MUST require successful independent verification of the applicable acceptance criteria.

### Acceptance

* [ ] AC-P001-T003-01 — Task state is derived from defined repository artifacts.
* [ ] AC-P001-T003-02 — State precedence is deterministic.
* [ ] AC-P001-T003-03 — `Implemented` requires implementation evidence.
* [ ] AC-P001-T003-04 — `Verified` requires independent verification evidence.
* [ ] AC-P001-T003-05 — Blocking findings affect derived state according to defined semantics.
* [ ] AC-P001-T003-06 — Equivalent repositories produce equivalent derived state.

**Depends on:** P001-T001, P001-T002

---

## P001-T004 — Implement dependency semantics and validation

**Status:** Verified
**Owner:** Implementer

Implement explicit semantics and validation for task relationships.

The implementation MUST support the relationships defined by the revised protocol, including:

```text
depends-on
blocks
requires
conflicts-with
supersedes
```

The implementation MUST validate:

* missing references;
* invalid references;
* self-references;
* dependency cycles;
* invalid relationship combinations.

### Acceptance

* [ ] AC-P001-T004-01 — Supported relationship types are represented.
* [ ] AC-P001-T004-02 — Relationship semantics are documented.
* [ ] AC-P001-T004-03 — Missing references are detected.
* [ ] AC-P001-T004-04 — Invalid cycles are detected.
* [ ] AC-P001-T004-05 — Self-references are detected.
* [ ] AC-P001-T004-06 — Valid dependency graphs pass validation.

**Depends on:** P001-T001

---

## P001-T005 — Implement the PaC relationship graph

**Status:** Verified
**Owner:** Implementer

Implement explicit relationships between PaC entities.

The implementation MUST support traceability equivalent to:

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

Stable identifiers MUST be used as relationship targets.

### Acceptance

* [ ] AC-P001-T005-01 — Core PaC entities can reference each other.
* [ ] AC-P001-T005-02 — Relationship targets use stable IDs.
* [ ] AC-P001-T005-03 — Invalid references are detectable.
* [ ] AC-P001-T005-04 — Plan-to-verification traceability is possible.
* [ ] AC-P001-T005-05 — Finding-to-decision traceability is possible.

**Depends on:** P001-T001, P001-T002, P001-T004

---

## P001-T006 — Implement first-class planning decisions

**Status:** Verified
**Owner:** Implementer

Implement addressable planning decisions using identifiers such as:

```text
P001-D001
P001-D002
```

A decision MUST be able to record:

* context;
* decision;
* rationale;
* affected entities;
* resulting changes.

Decisions MUST support the workflow:

```text
Feedback
    ↓
Planner decision
    ↓
Plan change
```

A feedback item MUST NOT directly modify the plan.

### Acceptance

* [ ] AC-P001-T006-01 — Planning decisions have stable IDs.
* [ ] AC-P001-T006-02 — Decisions can reference findings and feedback.
* [ ] AC-P001-T006-03 — Decisions record rationale.
* [ ] AC-P001-T006-04 — Decisions identify affected entities.
* [ ] AC-P001-T006-05 — Plan changes can be traced to decisions.
* [ ] AC-P001-T006-06 — Feedback cannot directly mutate canonical plan state.

**Depends on:** P001-T005

---

## P001-T007 — Implement the finding lifecycle

**Status:** Verified
**Owner:** Implementer

Implement a defined lifecycle for findings.

The supported states SHOULD include:

```text
Open
Acknowledged
Resolved
Accepted
Invalid
Superseded
```

Findings MUST remain distinct from tasks.

When a finding requires implementation work, the resulting task MUST be explicitly created through the planning process rather than implicitly created by the finding.

### Acceptance

* [ ] AC-P001-T007-01 — Findings have stable identifiers.
* [ ] AC-P001-T007-02 — Finding lifecycle states are represented.
* [ ] AC-P001-T007-03 — Findings can reference affected tasks and acceptance criteria.
* [ ] AC-P001-T007-04 — Findings cannot silently become tasks.
* [ ] AC-P001-T007-05 — Finding disposition can be traced to a planning decision.

**Depends on:** P001-T005, P001-T006

---

## P001-T008 — Implement verification-independence metadata

**Status:** Verified
**Owner:** Implementer

Implement explicit representation of verification independence.

The implementation MUST distinguish self-verification from independent verification.

The protocol SHOULD support levels equivalent to:

```text
Level 0 — Self verification
Level 1 — Separate verification operation
Level 2 — Separate agent/context
Level 3 — Independent actor/model context
Level 4 — Human or externally independent verification
```

A repository MUST be able to specify the minimum level required for `Verified`.

### Acceptance

* [ ] AC-P001-T008-01 — Verification independence level is representable.
* [ ] AC-P001-T008-02 — Self-verification is distinguishable from independent verification.
* [ ] AC-P001-T008-03 — Repository-specific minimum levels are supported.
* [ ] AC-P001-T008-04 — Verification records identify the independence level.
* [ ] AC-P001-T008-05 — State derivation respects the configured verification requirement.

**Depends on:** P001-T003

---

## P001-T009 — Implement standardized evidence references

**Status:** Verified
**Owner:** Implementer

Implement structured references for implementation and verification evidence while preserving Git-native artifacts.

Implementation evidence SHOULD support:

```text
commit
pull-request
file
test
command
artifact
```

Verification evidence SHOULD support:

```text
test-result
command
review
report
artifact
acceptance-evaluation
```

Evidence MUST be linkable to tasks and, where applicable, acceptance criteria.

### Acceptance

* [ ] AC-P001-T009-01 — Implementation evidence types are represented.
* [ ] AC-P001-T009-02 — Verification evidence types are represented.
* [ ] AC-P001-T009-03 — Evidence can reference tasks.
* [ ] AC-P001-T009-04 — Evidence can reference acceptance criteria.
* [ ] AC-P001-T009-05 — Verification evidence records an outcome.
* [ ] AC-P001-T009-06 — Evidence remains usable with ordinary Git repositories.

**Depends on:** P001-T002, P001-T005

---

## P001-T010 — Implement PaC conformance levels

**Status:** Verified
**Owner:** Implementer

Implement explicit conformance levels:

### PaC Core

Canonical plans, stable IDs, tasks, and acceptance criteria.

### PaC Agent

Core plus ownership, feedback, decisions, and agent procedures.

### PaC Verified

Agent plus evidence, findings, and independent verification.

### PaC Automated

Verified plus normalized representation, automated validation, relationship validation, and deterministic state derivation.

The implementation MUST allow a repository or tool to declare its supported level.

### Acceptance

* [ ] AC-P001-T010-01 — Conformance levels are represented.
* [ ] AC-P001-T010-02 — Requirements for each level are explicit.
* [ ] AC-P001-T010-03 — Higher levels build on lower levels.
* [ ] AC-P001-T010-04 — Repository conformance can be declared.
* [ ] AC-P001-T010-05 — Tool conformance can be declared.
* [ ] AC-P001-T010-06 — Core PaC usage remains possible without automation.

**Depends on:** P001-T003, P001-T006, P001-T008, P001-T009

---

## P001-T011 — Implement machine-checkable protocol invariants

**Status:** Verified
**Owner:** Implementer

Implement validation for the protocol's normative invariants.

At minimum:

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
```

### Acceptance

* [ ] AC-P001-T011-01 — Every invariant has a stable identifier.
* [ ] AC-P001-T011-02 — Every invariant is machine-checkable where applicable.
* [ ] AC-P001-T011-03 — Invalid artifacts produce actionable validation failures.
* [ ] AC-P001-T011-04 — Validation covers identity, relationships, state, evidence, and ownership.
* [ ] AC-P001-T011-05 — Invariant validation is covered by automated tests.

**Depends on:** P001-T003, P001-T004, P001-T005, P001-T006, P001-T007, P001-T008, P001-T009

---

## P001-T012 — Implement conformance fixtures

**Status:** Verified
**Owner:** Implementer

Add valid and invalid PaC fixtures covering the protocol.

Recommended structure:

```text
conformance/
├── valid/
│   ├── core/
│   ├── agent/
│   ├── verified/
│   └── automated/
│
└── invalid/
    ├── duplicate-id/
    ├── missing-reference/
    ├── cyclic-dependency/
    ├── invalid-state/
    ├── missing-verification/
    ├── invalid-feedback/
    └── invalid-ownership/
```

### Acceptance

* [ ] AC-P001-T012-01 — Valid fixtures exist for each conformance level.
* [ ] AC-P001-T012-02 — Invalid fixtures exist for each core invariant.
* [ ] AC-P001-T012-03 — Fixtures cover verification requirements.
* [ ] AC-P001-T012-04 — Fixtures cover relationship validation.
* [ ] AC-P001-T012-05 — Fixtures cover state derivation.
* [ ] AC-P001-T012-06 — Fixtures are understandable without specialized tooling.

**Depends on:** P001-T011

---

## P001-T013 — Update PaC schemas

**Status:** Verified
**Owner:** Implementer

Update the repository's schemas to represent the revised PaC model.

Schemas MUST validate the normalized structure without becoming the canonical representation.

Structural validation SHOULD cover:

* identifiers;
* required fields;
* enumerations;
* entity structure.

Semantic validation SHOULD cover:

* references;
* relationships;
* dependencies;
* evidence;
* state requirements.

### Acceptance

* [ ] AC-P001-T013-01 — Schemas represent the revised PaC entities.
* [ ] AC-P001-T013-02 — Identifier formats are validated.
* [ ] AC-P001-T013-03 — Required relationships are represented.
* [ ] AC-P001-T013-04 — Schema validation is consistent with protocol invariants.
* [ ] AC-P001-T013-05 — Schemas remain optional tooling rather than canonical artifacts.

**Depends on:** P001-T001, P001-T002, P001-T005, P001-T011

---

## P001-T014 — Update the PaC specification

**Status:** Verified
**Owner:** Implementer

Update `SPEC.md` to document the implemented protocol semantics.

The specification MUST document:

* normalized data model;
* acceptance criterion identifiers;
* state derivation;
* dependencies;
* relationships;
* planning decisions;
* finding lifecycle;
* verification independence;
* evidence;
* conformance levels;
* invariants;
* migration from v0.1.0.

The specification MUST clearly distinguish normative requirements from recommendations.

### Acceptance

* [ ] AC-P001-T014-01 — `SPEC.md` documents every implemented protocol feature.
* [ ] AC-P001-T014-02 — Normative requirements are distinguishable from recommendations.
* [ ] AC-P001-T014-03 — State derivation is deterministic and documented.
* [ ] AC-P001-T014-04 — Verification independence is documented.
* [ ] AC-P001-T014-05 — Conformance levels are documented.
* [ ] AC-P001-T014-06 — Migration from v0.1.0 is documented.
* [ ] AC-P001-T014-07 — Specification examples conform to the implemented semantics.

**Depends on:** P001-T001 through P001-T013

---

## P001-T015 — Update agent and repository documentation

**Status:** Verified
**Owner:** Implementer

Update:

```text
README.md
AGENTS.md
SKILL.md
.plan/README.md
```

Documentation MUST explain the revised workflow:

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

The documentation MUST make clear that the task list contains implementation tasks rather than planning or verification activities.

### Acceptance

* [ ] AC-P001-T015-01 — Documentation describes the revised workflow.
* [ ] AC-P001-T015-02 — Documentation distinguishes Planner, Implementer, and Verifier responsibilities.
* [ ] AC-P001-T015-03 — Documentation explains implementation versus verification.
* [ ] AC-P001-T015-04 — Documentation explains findings and decisions.
* [ ] AC-P001-T015-05 — Documentation states that PaC tasks represent implementation work.
* [ ] AC-P001-T015-06 — Documentation examples conform to the revised specification.

**Depends on:** P001-T014

---

## Findings

### P001-T014-F001 — Canonical plan P001.md not updated after implementation

**Status:** Resolved
**Severity:** informational

Recorded by the Verifier (`.plan/verification/P001-T014-F001.md`); duplicates review `R001-F003` and feedback `P001-FB001`.

The canonical plan was not updated after implementation. This iteration resolves the inconsistency.

#### References

- P001-T014

#### Resolution

Resolved by `P001-D001`: the canonical plan was updated to record the implemented and verified state, and the plan was closed.

## Decisions

### P001-D001 — Close P001

**Context:** Feedback `P001-FB001` (Implementer) reported that the canonical plan was inconsistent with the repository state after implementation, and `P001-FB002` (Verifier) recorded that all 15 tasks were independently verified at independence Level 2. Informational finding `P001-T014-F001` (mirroring review `R001-F003`) requested the Planner update the plan or explicitly close it.

**Decision:** Authorize the completed P001 implementation and close the plan. Tasks `P001-T001` through `P001-T015` are recorded as `Verified` at independence Level 2 per `.plan/verification/P001.md`.

**Rationale:** Every task satisfies its acceptance criteria; independent verification passed at Level 2; `python3 tools/validate.py --root .` reports no invariant violations; `python3 -m unittest discover -s tests` passes (25 tests); conformance fixtures validate as declared; no unresolved blocking findings remain.

**Affected:** P001, P001-T001, P001-T002, P001-T003, P001-T004, P001-T005, P001-T006, P001-T007, P001-T008, P001-T009, P001-T010, P001-T011, P001-T012, P001-T013, P001-T014, P001-T015

**Resulting changes:** Plan status set to `Closed`; `**PaC version:**` updated to v0.3.2; current iteration advanced to 2; all task statuses set to `Verified`; `## Verification` records added; finding `P001-T014-F001` marked `Resolved`; plan moved to closed plans in `.plan/README.md`.

## Verification

Independent verification recorded in `.plan/verification/P001.md` (Verifier: `verifier-agent`, date 2026-09-13). Verdict: all 15 tasks satisfy their acceptance criteria; no blocking findings.

### P001-T001

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `2da77af`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T001-01 — A normalized representation exists for all required PaC entities.
- [x] AC-P001-T001-02 — Canonical Markdown can be mapped to the normalized representation.
- [x] AC-P001-T001-03 — The normalized representation does not replace Markdown as the source of truth.
- [x] AC-P001-T001-04 — Equivalent PaC documents produce equivalent normalized representations.
- [x] AC-P001-T001-05 — The implementation documents any information that cannot be represented unambiguously.

---

### P001-T002

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `eb3cba1`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T002-01 — Acceptance criteria have stable identifiers.
- [x] AC-P001-T002-02 — Identifier format is documented and validated.
- [x] AC-P001-T002-03 — Criterion identity is independent of its text.
- [x] AC-P001-T002-04 — Each criterion belongs to exactly one task.
- [x] AC-P001-T002-05 — Verification records can reference criterion IDs.
- [x] AC-P001-T002-06 — Existing plans have a documented compatibility path.

---

### P001-T003

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `9d90051`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T003-01 — Task state is derived from defined repository artifacts.
- [x] AC-P001-T003-02 — State precedence is deterministic.
- [x] AC-P001-T003-03 — `Implemented` requires implementation evidence.
- [x] AC-P001-T003-04 — `Verified` requires independent verification evidence.
- [x] AC-P001-T003-05 — Blocking findings affect derived state according to defined semantics.
- [x] AC-P001-T003-06 — Equivalent repositories produce equivalent derived state.

---

### P001-T004

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `dede8ee`
- Command: `python3 tools/validate.py --root conformance/invalid/missing-reference`
- Command: `python3 tools/validate.py --root conformance/invalid/cyclic-dependency`
- Command: `python3 tools/validate.py --root conformance/invalid/invalid-combination`
- Result: each reports its declared invariant (INV-005, INV-006, INV-013)

#### Acceptance

- [x] AC-P001-T004-01 — Supported relationship types are represented.
- [x] AC-P001-T004-02 — Relationship semantics are documented.
- [x] AC-P001-T004-03 — Missing references are detected.
- [x] AC-P001-T004-04 — Invalid cycles are detected.
- [x] AC-P001-T004-05 — Self-references are detected.
- [x] AC-P001-T004-06 — Valid dependency graphs pass validation.

---

### P001-T005

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `5b8d9ea`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T005-01 — Core PaC entities can reference each other.
- [x] AC-P001-T005-02 — Relationship targets use stable IDs.
- [x] AC-P001-T005-03 — Invalid references are detectable.
- [x] AC-P001-T005-04 — Plan-to-verification traceability is possible.
- [x] AC-P001-T005-05 — Finding-to-decision traceability is possible.

---

### P001-T006

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `e70de95`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T006-01 — Planning decisions have stable IDs.
- [x] AC-P001-T006-02 — Decisions can reference findings and feedback.
- [x] AC-P001-T006-03 — Decisions record rationale.
- [x] AC-P001-T006-04 — Decisions identify affected entities.
- [x] AC-P001-T006-05 — Plan changes can be traced to decisions.
- [x] AC-P001-T006-06 — Feedback cannot directly mutate canonical plan state.

---

### P001-T007

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `6c67fa5`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T007-01 — Findings have stable identifiers.
- [x] AC-P001-T007-02 — Finding lifecycle states are represented.
- [x] AC-P001-T007-03 — Findings can reference affected tasks and acceptance criteria.
- [x] AC-P001-T007-04 — Findings cannot silently become tasks.
- [x] AC-P001-T007-05 — Finding disposition can be traced to a planning decision.

---

### P001-T008

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `0447a14`
- Command: `python3 tools/validate.py --root conformance/valid/automated`
- Result: OK (declared verification minimum Level 3 respected)

#### Acceptance

- [x] AC-P001-T008-01 — Verification independence level is representable.
- [x] AC-P001-T008-02 — Self-verification is distinguishable from independent verification.
- [x] AC-P001-T008-03 — Repository-specific minimum levels are supported.
- [x] AC-P001-T008-04 — Verification records identify the independence level.
- [x] AC-P001-T008-05 — State derivation respects the configured verification requirement.

---

### P001-T009

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `71b3399`
- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T009-01 — Implementation evidence types are represented.
- [x] AC-P001-T009-02 — Verification evidence types are represented.
- [x] AC-P001-T009-03 — Evidence can reference tasks.
- [x] AC-P001-T009-04 — Evidence can reference acceptance criteria.
- [x] AC-P001-T009-05 — Verification evidence records an outcome.
- [x] AC-P001-T009-06 — Evidence remains usable with ordinary Git repositories.

---

### P001-T010

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `30bd87f`
- Command: `python3 tools/validate.py --root conformance/valid/core`
- Command: `python3 tools/validate.py --root conformance/valid/agent`
- Command: `python3 tools/validate.py --root conformance/valid/verified`
- Command: `python3 tools/validate.py --root conformance/valid/automated`
- Result: OK for all four levels

#### Acceptance

- [x] AC-P001-T010-01 — Conformance levels are represented.
- [x] AC-P001-T010-02 — Requirements for each level are explicit.
- [x] AC-P001-T010-03 — Higher levels build on lower levels.
- [x] AC-P001-T010-04 — Repository conformance can be declared.
- [x] AC-P001-T010-05 — Tool conformance can be declared.
- [x] AC-P001-T010-06 — Core PaC usage remains possible without automation.

---

### P001-T011

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `2a9c0e8`
- Commit: `5026b05`
- Command: `python3 tools/validate.py --root .`
- Command: `python3 -m unittest discover -s tests`
- Result: OK; 25 passed

#### Acceptance

- [x] AC-P001-T011-01 — Every invariant has a stable identifier.
- [x] AC-P001-T011-02 — Every invariant is machine-checkable where applicable.
- [x] AC-P001-T011-03 — Invalid artifacts produce actionable validation failures.
- [x] AC-P001-T011-04 — Validation covers identity, relationships, state, evidence, and ownership.
- [x] AC-P001-T011-05 — Invariant validation is covered by automated tests.

---

### P001-T012

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `77135c9`
- Command: `python3 -m unittest discover -s tests`
- Result: 25 passed (valid fixtures pass; invalid fixtures report declared invariants)

#### Acceptance

- [x] AC-P001-T012-01 — Valid fixtures exist for each conformance level.
- [x] AC-P001-T012-02 — Invalid fixtures exist for each core invariant.
- [x] AC-P001-T012-03 — Fixtures cover verification requirements.
- [x] AC-P001-T012-04 — Fixtures cover relationship validation.
- [x] AC-P001-T012-05 — Fixtures cover state derivation.
- [x] AC-P001-T012-06 — Fixtures are understandable without specialized tooling.

---

### P001-T013

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `7b25e26`
- Command: `python3 -m unittest discover -s tests`
- Result: 25 passed (schema tests included)

#### Acceptance

- [x] AC-P001-T013-01 — Schemas represent the revised PaC entities.
- [x] AC-P001-T013-02 — Identifier formats are validated.
- [x] AC-P001-T013-03 — Required relationships are represented.
- [x] AC-P001-T013-04 — Schema validation is consistent with protocol invariants.
- [x] AC-P001-T013-05 — Schemas remain optional tooling rather than canonical artifacts.

---

### P001-T014

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `a00f71b`
- Command: `python3 tools/validate.py --root .`
- Result: OK

#### Acceptance

- [x] AC-P001-T014-01 — `SPEC.md` documents every implemented protocol feature.
- [x] AC-P001-T014-02 — Normative requirements are distinguishable from recommendations.
- [x] AC-P001-T014-03 — State derivation is deterministic and documented.
- [x] AC-P001-T014-04 — Verification independence is documented.
- [x] AC-P001-T014-05 — Conformance levels are documented.
- [x] AC-P001-T014-06 — Migration from v0.1.0 is documented.
- [x] AC-P001-T014-07 — Specification examples conform to the implemented semantics.

---

### P001-T015

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Review: `R001`
- Commit: `ab2391a`
- Command: `python3 tools/validate.py --root .`
- Command: `python3 -m unittest discover -s tests`
- Result: OK; 25 passed

#### Acceptance

- [x] AC-P001-T015-01 — Documentation describes the revised workflow.
- [x] AC-P001-T015-02 — Documentation distinguishes Planner, Implementer, and Verifier responsibilities.
- [x] AC-P001-T015-03 — Documentation explains implementation versus verification.
- [x] AC-P001-T015-04 — Documentation explains findings and decisions.
- [x] AC-P001-T015-05 — Documentation states that PaC tasks represent implementation work.
- [x] AC-P001-T015-06 — Documentation examples conform to the revised specification.

## Planning Iteration 1

This iteration establishes the implementation sequence:

```text
P001-T001
Normalized model
       ↓
P001-T002
Acceptance criterion IDs
       ↓
P001-T003
State derivation
       ↓
P001-T004
Dependencies
       ↓
P001-T005
Relationship graph
       ↓
P001-T006
Decisions
       ↓
P001-T007
Findings
       ↓
P001-T008
Verification independence
       ↓
P001-T009
Evidence
       ↓
P001-T010
Conformance
       ↓
P001-T011
Invariants
       ↓
P001-T012
Fixtures
       ↓
P001-T013
Schemas
       ↓
P001-T014
Specification
       ↓
P001-T015
Documentation
```

All tasks represent **implementation work**.

The Planner owns the plan and subsequent planning decisions. The Implementer owns execution of the tasks. The Verifier independently evaluates the resulting implementation.

## Planning Iteration 2 — Closure

Iteration 2 records the disposition of post-implementation feedback and the plan's completion:

* Feedback `P001-FB001` (Implementer) and `P001-FB002` (Verifier) were evaluated by the Planner and dispositioned through decision `P001-D001`.
* All 15 implementation tasks are recorded as `Verified` at independence Level 2.
* Informational finding `P001-T014-F001` is `Resolved`.
* The plan is `Closed`; all completion criteria are met.

Stable IDs are preserved across iterations: `P001`, `P001-T001` through `P001-T015`, `P001-T014-F001`, and `P001-D001`.

## Completion Criteria

P001 is complete when:

* all implementation tasks satisfy their acceptance criteria;
* the revised PaC semantics are implemented;
* machine-checkable invariants pass;
* conformance fixtures pass;
* schemas are consistent with the protocol;
* `SPEC.md` accurately describes the implementation;
* migration guidance is available;
* repository and agent documentation is updated;
* independent verification confirms the implementation;
* no unresolved blocking findings remain.

All completion criteria above are met as of iteration 2 (2026-09-13): all 15 tasks satisfy their acceptance criteria and are independently verified at Level 2; machine-checkable invariants pass; conformance fixtures and schemas validate; `SPEC.md` accurately describes the implementation; migration guidance and documentation are updated; no unresolved blocking findings remain. The plan is closed.