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
    "duplicate-id": "INV-002",
    "missing-reference": "INV-005",
    "cyclic-dependency": "INV-006",
    "invalid-state": "STATE",
    "missing-verification": "INV-007",
    "invalid-feedback": "INV-010",
    "invalid-ownership": "INV-012",
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
                self.assertNotEqual(violations, [], f"invalid fixture {root.name} should fail")
                expected = EXPECTED_INVALID[root.name]
                self.assertIn(
                    expected,
                    {v["invariant"] for v in violations},
                    f"invalid fixture {root.name} should report {expected}",
                )


if __name__ == "__main__":
    unittest.main()