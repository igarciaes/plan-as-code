"""Automated tests for the PaC protocol invariant validator (SPEC Section 28).

Runs with the standard library test runner:

    python3 -m unittest discover -s tests

Also runs under pytest when available, since the cases are unittest.TestCase.
"""

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from validate import validate  # noqa: E402


VALID_PLAN = """# P001 — Valid Plan

**Status:** Active
**Scope:** `src/`
**Planner:** planner-agent
**Created:** 2026-09-13
**PaC version:** v0.2.0
**Current iteration:** 1

## Objective

Objective text.

## Constraints

- Constraint.

## Tasks

### P001-T001 — Task one

**Status:** Implemented
**Owner:** Implementer

Description.

**Depends on:**

- None

#### Acceptance

- [ ] AC-P001-T001-01 — Criterion one.
- [ ] AC-P001-T001-02 — Criterion two.

---

### P001-T002 — Task two

**Status:** Planned
**Owner:** Implementer

Description.

**Depends on:**

- P001-T001

#### Acceptance

- [ ] AC-P001-T002-01 — Criterion one.

---

## Findings

No findings.

---

## Decisions

No decisions.

---

## Verification

Pending.
"""

VERIFIED_PLAN = """# P001 — Verified Plan

**Status:** Active
**Scope:** `src/`
**Planner:** planner-agent
**Created:** 2026-09-13
**PaC version:** v0.2.0
**Current iteration:** 1

## Objective

Objective text.

## Tasks

### P001-T001 — Task one

**Status:** Verified
**Owner:** Implementer

Description.

**Depends on:**

- None

#### Acceptance

- [ ] AC-P001-T001-01 — Criterion one.

---

## Findings

No findings.

---

## Verification

### P001-T001

**Status:** Verified

**Verifier:** verifier-agent

**Independence:** Level 2

#### Evidence

- Command: `python3 tools/validate.py --root .`
- Result: passed

#### Acceptance

- [x] AC-P001-T001-01 — Criterion one.
"""


def write_repo(root, files):
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def run(root):
    return validate(str(root), {})


class ValidatorTestCase(unittest.TestCase):
    def make_repo(self, plans, feedback=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        files = {}
        for i, plan in enumerate(plans, start=1):
            files[f".plan/plans/P{i:03d}.md"] = plan
        for name, content in (feedback or {}).items():
            files[f".plan/feedback/{name}"] = content
        write_repo(root, files)
        return root

    def violations_for(self, root, invariant):
        return [v for v in run(root) if v["invariant"] == invariant]

    def test_valid_plan_has_no_violations(self):
        root = self.make_repo([VALID_PLAN])
        self.assertEqual(run(root), [])

    def test_inv001_duplicate_plan_ids(self):
        root = self.make_repo([VALID_PLAN, VALID_PLAN])
        self.assertTrue(self.violations_for(root, "INV-001"))

    def test_inv002_duplicate_task_ids(self):
        dup = VALID_PLAN.replace(
            "### P001-T002 — Task two", "### P001-T001 — Task two"
        )
        root = self.make_repo([dup])
        self.assertTrue(self.violations_for(root, "INV-002"))

    def test_inv003_task_belongs_to_plan(self):
        wrong = VALID_PLAN.replace("P001-T002", "P002-T002").replace(
            "AC-P001-T002-01", "AC-P002-T002-01"
        )
        root = self.make_repo([wrong])
        self.assertTrue(self.violations_for(root, "INV-003"))

    def test_inv004_acceptance_belongs_to_task(self):
        wrong = VALID_PLAN.replace("AC-P001-T002-01", "AC-P001-T001-01")
        root = self.make_repo([wrong])
        self.assertTrue(self.violations_for(root, "INV-004"))

    def test_inv005_missing_reference(self):
        wrong = VALID_PLAN.replace("P001-T001\n\n#### Acceptance", "P001-T999\n\n#### Acceptance")
        root = self.make_repo([wrong])
        self.assertTrue(self.violations_for(root, "INV-005"))

    def test_inv006_dependency_cycle(self):
        cyc = VALID_PLAN.replace(
            "**Depends on:**\n\n- P001-T001", "**Depends on:**\n\n- P001-T001"
        )
        cyc = cyc.replace(
            "### P001-T001 — Task one\n\n**Status:** Implemented",
            "### P001-T001 — Task one\n\n**Status:** Implemented",
        )
        cyc = cyc.replace(
            "**Depends on:**\n\n- None\n\n#### Acceptance",
            "**Depends on:**\n\n- P001-T002\n\n#### Acceptance",
            1,
        )
        root = self.make_repo([cyc])
        self.assertTrue(self.violations_for(root, "INV-006"))

    def test_inv007_verified_without_verification_record(self):
        no_record = VERIFIED_PLAN.split("## Verification")[0] + "## Verification\n\nPending.\n"
        root = self.make_repo([no_record])
        self.assertTrue(self.violations_for(root, "INV-007"))

    def test_inv007_min_verification_level(self):
        root = self.make_repo([VERIFIED_PLAN])
        write_repo(
            root,
            {".plan/README.md": "**Verification minimum:** Level 3\n"},
        )
        self.assertTrue(self.violations_for(root, "INV-007"))

    def test_inv008_verified_without_evidence(self):
        no_evidence = VERIFIED_PLAN.replace("- Command: `python3 tools/validate.py --root .`\n- Result: passed\n", "")
        root = self.make_repo([no_evidence])
        self.assertTrue(self.violations_for(root, "INV-008"))

    def test_inv009_duplicate_finding_id(self):
        with_finding = VALID_PLAN + """
## Findings

### P001-T001-F001 — Finding one

**Status:** Open
**Severity:** Blocking

### P001-T001-F001 — Finding two

**Status:** Open
**Severity:** Blocking
"""
        root = self.make_repo([with_finding])
        self.assertTrue(self.violations_for(root, "INV-009"))

    def test_inv010_duplicate_feedback_item(self):
        feedback = """# Feedback — P001-T001

## P001-T001-FB001 — Clarification

**Author:** Implementer
**Date:** 2026-09-13

Question?

---

## P001-T001-FB001 — Clarification

**Author:** Planner
**Date:** 2026-09-13

Answer.
"""
        root = self.make_repo([VALID_PLAN], feedback={"P001-T001.md": feedback})
        self.assertTrue(self.violations_for(root, "INV-010"))

    def test_inv011_plan_change_without_decision(self):
        changed = VALID_PLAN.replace("**Current iteration:** 1", "**Current iteration:** 2")
        root = self.make_repo([changed])
        self.assertTrue(self.violations_for(root, "INV-011"))

    def test_inv012_planner_owns_implementation_task(self):
        owned = VALID_PLAN.replace("**Owner:** Implementer", "**Owner:** Planner")
        root = self.make_repo([owned])
        self.assertTrue(self.violations_for(root, "INV-012"))


if __name__ == "__main__":
    unittest.main()