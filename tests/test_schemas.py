"""Tests that the optional schemas are valid JSON and represent the revised model.

Runs with:

    python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class SchemaTestCase(unittest.TestCase):
    def load(self, name):
        with (ROOT / "schemas" / name).open(encoding="utf-8") as fh:
            return json.load(fh)

    def test_schemas_are_valid_json(self):
        for name in ("plan.schema.json", "feedback.schema.json"):
            with self.subTest(schema=name):
                self.assertIsInstance(self.load(name), dict)

    def test_plan_schema_represents_revised_entities(self):
        plan = self.load("plan.schema.json")
        props = plan["properties"]
        for section in ("tasks", "findings", "decisions", "verifications", "conformance"):
            self.assertIn(section, props)

    def test_plan_schema_acceptance_ids(self):
        plan = self.load("plan.schema.json")
        ac = plan["properties"]["tasks"]["items"]["properties"]["acceptance"]["items"]
        self.assertEqual(ac["properties"]["id"]["pattern"], "^AC-P[0-9]+-T[0-9]+-[0-9]+$")

    def test_plan_schema_finding_lifecycle(self):
        plan = self.load("plan.schema.json")
        status = plan["properties"]["findings"]["items"]["properties"]["status"]
        self.assertEqual(
            set(status["enum"]),
            {"Open", "Acknowledged", "Resolved", "Accepted", "Invalid", "Superseded"},
        )

    def test_plan_schema_verification_independence(self):
        plan = self.load("plan.schema.json")
        level = plan["properties"]["verifications"]["items"]["properties"]["independence_level"]
        self.assertEqual((level["minimum"], level["maximum"]), (0, 4))

    def test_feedback_schema_append_only_items(self):
        feedback = self.load("feedback.schema.json")
        item = feedback["properties"]["items"]["items"]
        self.assertIn("id", item["required"])


if __name__ == "__main__":
    unittest.main()