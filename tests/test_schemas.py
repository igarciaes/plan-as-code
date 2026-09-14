"""Tests that the optional schemas are valid JSON and represent the v0.4.0 model.

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
        for name in ("plan.schema.json", "task.schema.json"):
            with self.subTest(schema=name):
                self.assertIsInstance(self.load(name), dict)

    def test_feedback_schema_removed(self):
        self.assertFalse((ROOT / "schemas" / "feedback.schema.json").exists())

    def test_plan_schema_two_record_model(self):
        plan = self.load("plan.schema.json")
        props = plan["properties"]
        self.assertEqual(set(plan["required"]), {"id", "title", "status", "tasks"})
        for key in ("objective", "constraints", "tasks", "definition_of_done"):
            self.assertIn(key, props)

    def test_plan_schema_status_vocabulary(self):
        plan = self.load("plan.schema.json")
        self.assertEqual(
            set(plan["properties"]["status"]["enum"]),
            {"Draft", "Planned", "Completed", "Cancelled"},
        )

    def test_task_schema_status_vocabulary(self):
        task = self.load("task.schema.json")
        self.assertIn("Changes Requested", task["properties"]["status"]["enum"])
        self.assertIn("Verified", task["properties"]["status"]["enum"])

    def test_task_schema_definition_of_done_and_verification(self):
        task = self.load("task.schema.json")
        props = task["properties"]
        self.assertIn("definition_of_done", props)
        dod = props["definition_of_done"]["items"]
        self.assertIn("done", dod["properties"])
        self.assertIn("plan_id", props)
        self.assertIn("verification", props)
        result = props["verification"]["properties"]["result"]
        self.assertEqual(
            set(result["enum"]),
            {"Pending", "Verified", "Changes Requested"},
        )


if __name__ == "__main__":
    unittest.main()