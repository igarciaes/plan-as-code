"""Tests that conformance fixtures validate as expected.

Runs with:

    python3 -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from validate import validate  # noqa: E402

CONFORMANCE = Path(__file__).resolve().parent.parent / "conformance"

EXPECTED_INVALID = {
    "dependency-cycle": "INV-008",
    "duplicate-plan-id": "INV-001",
    "duplicate-task-id": "INV-002",
    "incomplete-dod": "INV-011",
    "invalid-plan-status": "INV-005",
    "invalid-task-status": "INV-006",
    "missing-dependency": "INV-007",
    "missing-plan-reference": "INV-003",
    "plan-completion": "INV-012",
    "planner-owned-task": "INV-009",
    "unauthorized-verification": "INV-009",
    "verified-without-verification": "INV-010",
    "wrong-location": "INV-013",
}


class FixtureTestCase(unittest.TestCase):
    def test_valid_fixtures_pass(self):
        for root in sorted((CONFORMANCE / "valid").iterdir()):
            with self.subTest(root=root.name):
                self.assertEqual(
                    validate(str(root), {}),
                    [],
                    f"valid fixture {root.name} should have no violations",
                )

    def test_invalid_fixtures_fail_expected_invariant(self):
        for root in sorted((CONFORMANCE / "invalid").iterdir()):
            with self.subTest(root=root.name):
                violations = validate(str(root), {})
                self.assertNotEqual(
                    violations, [], f"invalid fixture {root.name} should fail"
                )
                expected = EXPECTED_INVALID[root.name]
                self.assertIn(
                    expected,
                    {v["invariant"] for v in violations},
                    f"invalid fixture {root.name} should report {expected}",
                )


if __name__ == "__main__":
    unittest.main()