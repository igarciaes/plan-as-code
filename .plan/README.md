# Plan as Code

Plans are stored under `plans/` in this repository.

## Layout

Each plan is a single Markdown file under `plans/`.

- Plan IDs follow `P###` (for example `P001`).
- Plan IDs are allocated by scanning `plans/` for existing records and taking the next sequential unused number.
- Task IDs follow `P###-T###` (for example `P001-T001`).
- Finding IDs follow `P###-T###-F###` (for example `P001-T001-F001`).
- Feedback threads are stored under `feedback/`.
- Feedback thread filenames follow the subject ID (for example `P001-T001.md`, `P001-T001-F001.md`, or `P001.md`).
- Feedback item IDs follow `P###-T###-FB###` (for example `P001-T001-FB001`).
- Planning iterations are represented as sections within the plan file.

## Status

This repository uses the full PaC vocabulary from `SPEC.md`.

Task states: Draft, Planned, In Progress, Implemented, Verified, Blocked, Deferred, Cancelled.

## Active plans

None.

## Closed plans

None.