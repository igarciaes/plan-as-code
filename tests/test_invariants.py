"""Automated tests for the PaC v0.4.0 protocol invariant validator (SPEC Section 17).

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


PLAN = """# P001 — Valid Plan

**Status:** Planned
**Scope:** `src/`
**Planner:** planner-agent
**Created:** 2026-09-14
**PaC version:** v0.4.0

## Objective

Objective text.

## Constraints

- Constraint.

## Tasks

- P001-T001
- P001-T002

## Definition of Done

- [ ] Plan condition.
"""

TASK = """# {tid} — Task title

**Status:** {status}
**Owner:** {owner}
**Plan:** {plan}

## Objective

Description.

**Depends on:**

- {depends}

## Definition of Done

{dod}

## Implementation

Implementation text.

## Implementation Evidence

- Commit: `abc1234`
- Test: `npm test`
- Result: passed

## Verification

{verification}
"""

VERIFIED_VERIFICATION = """**Result:** Verified

**By:** planner-agent

**Date:** 2026-09-14

All conditions satisfied.
"""

PENDING_VERIFICATION = """**Result:** Pending

**By:** planner-agent

**Date:** 2026-09-14
"""


def dod(items):
    return "\n".join(f"- [{m}] {t}" for m, t in items)


def task(tid, plan="P001", status="Planned", owner="Implementer", depends="None",
         dod_items=(), verification=PENDING_VERIFICATION):
    return TASK.format(
        tid=tid,
        status=status,
        owner=owner,
        plan=plan,
        depends=depends,
        dod=dod(dod_items) if dod_items else "- [ ] Criterion one.",
        verification=verification,
    )


def write_repo(root, files):
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def clean_repo(plans, tasks):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    files = {}
    for i, content in enumerate(plans, start=1):
        files[f".plan/plans/P{i:03d}.md"] = content
    for name, content in tasks.items():
        files[f".plan/tasks/{name}"] = content
    write_repo(root, files)
    return root, tmp


class ValidatorTestCase(unittest.TestCase):
    def violations(self, root, invariant=None):
        vs = validate(str(root), {})
        if invariant is None:
            return vs
        return [v for v in vs if v["invariant"] == invariant]

    def test_clean_repo_has_no_violations(self):
        root, tmp = clean_repo(
            [PLAN],
            {
                "P001-T001.md": task("P001-T001", dod_items=[(" ", "Criterion one.")]),
                "P001-T002.md": task("P001-T002", depends="P001-T001", dod_items=[(" ", "Criterion two.")]),
            },
        )
        self.assertEqual(validate(str(root), {}), [])
        tmp.cleanup()

    def test_inv001_duplicate_plan_ids(self):
        root, tmp = clean_repo(
            [PLAN, PLAN],
            {"P001-T001.md": task("P001-T001")},
        )
        self.assertTrue(self.violations(root, "INV-001"))
        tmp.cleanup()

    def test_inv002_duplicate_task_ids(self):
        root, tmp = clean_repo(
            [PLAN],
            {"P001-T001.md": task("P001-T001"), "P001-T001-dup.md": task("P001-T001")},
        )
        self.assertTrue(self.violations(root, "INV-002"))
        tmp.cleanup()

    def test_inv003_missing_plan_reference(self):
        root, tmp = clean_repo(
            [PLAN],
            {"P001-T001.md": task("P001-T001", plan="P999")},
        )
        self.assertTrue(self.violations(root, "INV-003"))
        tmp.cleanup()

    def test_inv004_task_prefix_mismatch(self):
        root, tmp = clean_repo(
            [PLAN],
            {"P002-T001.md": task("P002-T001", plan="P001")},
        )
        self.assertTrue(self.violations(root, "INV-004"))
        tmp.cleanup()

    def test_inv005_invalid_plan_status(self):
        root, tmp = clean_repo(
            [PLAN.replace("**Status:** Planned", "**Status:** Active")],
            {"P001-T001.md": task("P001-T001")},
        )
        self.assertTrue(self.violations(root, "INV-005"))
        tmp.cleanup()

    def test_inv006_invalid_task_status(self):
        root, tmp = clean_repo(
            [PLAN],
            {"P001-T001.md": task("P001-T001", status="Almost Done")},
        )
        self.assertTrue(self.violations(root, "INV-006"))
        tmp.cleanup()

    def test_inv007_missing_dependency(self):
        root, tmp = clean_repo(
            [PLAN],
            {"P001-T001.md": task("P001-T001", depends="P001-T999")},
        )
        self.assertTrue(self.violations(root, "INV-007"))
        tmp.cleanup()

    def test_inv008_dependency_cycle(self):
        root, tmp = clean_repo(
            [PLAN],
            {
                "P001-T001.md": task("P001-T001", depends="P001-T002"),
                "P001-T002.md": task("P001-T002", depends="P001-T001"),
            },
        )
        self.assertTrue(self.violations(root, "INV-008"))
        tmp.cleanup()

    def test_inv009_planner_owns_implementation_task(self):
        root, tmp = clean_repo(
            [PLAN],
            {"P001-T001.md": task("P001-T001", owner="Planner")},
        )
        self.assertTrue(self.violations(root, "INV-009"))
        tmp.cleanup()

    def test_inv009_implementer_self_verifies(self):
        verified = VERIFIED_VERIFICATION.replace("planner-agent", "implementer-agent")
        root, tmp = clean_repo(
            [PLAN],
            {
                "P001-T001.md": task(
                    "P001-T001",
                    status="Verified",
                    owner="implementer-agent",
                    dod_items=[("x", "Criterion one.")],
                    verification=verified,
                )
            },
        )
        self.assertTrue(self.violations(root, "INV-009"))
        tmp.cleanup()

    def test_inv010_verified_without_verification_record(self):
        root, tmp = clean_repo(
            [PLAN],
            {
                "P001-T001.md": task(
                    "P001-T001",
                    status="Verified",
                    dod_items=[("x", "Criterion one.")],
                    verification=PENDING_VERIFICATION,
                )
            },
        )
        self.assertTrue(self.violations(root, "INV-010"))
        tmp.cleanup()

    def test_inv011_incomplete_definition_of_done(self):
        root, tmp = clean_repo(
            [PLAN],
            {
                "P001-T001.md": task(
                    "P001-T001",
                    status="Verified",
                    dod_items=[("x", "Criterion one."), (" ", "Criterion two.")],
                    verification=VERIFIED_VERIFICATION,
                )
            },
        )
        self.assertTrue(self.violations(root, "INV-011"))
        tmp.cleanup()

    def test_inv012_plan_completion_requires_verified_tasks(self):
        completed = PLAN.replace("**Status:** Planned", "**Status:** Completed")
        root, tmp = clean_repo(
            [completed],
            {
                "P001-T001.md": task("P001-T001", status="Implemented", dod_items=[(" ", "Criterion one.")]),
                "P001-T002.md": task("P001-T002", depends="P001-T001"),
            },
        )
        self.assertTrue(self.violations(root, "INV-012"))
        tmp.cleanup()

    def test_inv013_task_not_in_tasks_dir(self):
        root, tmp = clean_repo(
            [PLAN],
            {"P001-T001.md": task("P001-T001")},
        )
        wrong = root / ".plan" / "plans" / "P001-T001.md"
        wrong.write_text((root / ".plan" / "tasks" / "P001-T001.md").read_text())
        (root / ".plan" / "tasks" / "P001-T001.md").unlink()
        self.assertTrue(self.violations(root, "INV-013"))
        tmp.cleanup()

    def test_legacy_v03x_plan_is_ignored(self):
        single = PLAN.replace("- P001-T002\n", "")
        root, tmp = clean_repo(
            [single],
            {"P001-T001.md": task("P001-T001")},
        )
        legacy = root / ".plan" / "plans" / "P099.md"
        legacy.write_text(
            "# P099 — Legacy\n\n"
            "**Status:** Closed\n"
            "**Current iteration:** 1\n\n"
            "## Tasks\n\n"
            "## P099-T001 — Old inline task\n\n"
            "**Status:** Verified\n"
            "#### Acceptance\n\n- [ ] AC-P099-T001-01 — Old criterion.\n\n"
            "## Findings\n\nNo findings.\n\n"
            "## Verification\n\nPending.\n"
        )
        self.assertEqual(validate(str(root), {}), [])
        tmp.cleanup()


if __name__ == "__main__":
    unittest.main()