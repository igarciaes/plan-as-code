# P002 — Fix Authentication Regression

**Status:** Completed
**Scope:** `src/auth/`, `tests/auth/`
**Planner:** planner-agent
**Created:** 2026-09-14
**PaC version:** v0.5.0

## Objective

Restore existing password authentication, which regressed when OAuth was introduced, without redefining the OAuth feature.

## Scope

### Included

- `src/auth/` regression fix.
- `tests/auth/` regression tests.

### Excluded

- New authentication features.

## Constraints

- Existing password authentication MUST remain functional.
- OAuth behavior from P001 MUST NOT regress.

## Tasks

- P002-T001