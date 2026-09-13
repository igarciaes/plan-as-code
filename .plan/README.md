# Plan as Code

Plans are stored under `plans/` in this repository.

## Layout

Each plan is a single Markdown file under `plans/`.

- Plan IDs follow `P###` (for example `P001`).
- Plan IDs are allocated by scanning `plans/` for existing records and taking the next sequential unused number.
- Task IDs follow `P###-T###` (for example `P001-T001`).
- Acceptance criterion IDs follow `AC-P###-T###-NN` (for example `AC-P001-T001-01`).
- Decision IDs follow `P###-D###` (for example `P001-D001`).
- Finding IDs follow `P###-T###-F###` (for example `P001-T001-F001`).
- Feedback threads are stored under `feedback/`.
- Feedback thread filenames follow the subject ID (for example `P001-T001.md`, `P001-T001-F001.md`, or `P001.md`).
- Feedback item IDs follow `P###-T###-FB###` (for example `P001-T001-FB001`).
- Planning iterations are represented as sections within the plan file.

## Status

This repository uses the full PaC vocabulary from `SPEC.md`.

Task states: Draft, Planned, In Progress, Implemented, Verified, Blocked, Deferred, Cancelled.

## Conformance

This repository targets the revised PaC v0.2.0 semantics (see `SPEC.md`). It MAY declare a conformance level and a verification minimum using the following lines:

```markdown
**Conformance:** PaC Automated
**Verification minimum:** Level 2
```

- `**Conformance:**` declares the conformance level (PaC Core, Agent, Verified, or Automated) per `SPEC.md` §27.
- `**Verification minimum:**` declares the minimum verification-independence level required for `Verified` per `SPEC.md` §26. The invariant validator (`tools/validate.py`) reads this value.

## Active plans

None.

## Closed plans

- P001 — Strengthen PaC Protocol Semantics and Conformance.