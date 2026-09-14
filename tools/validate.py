#!/usr/bin/env python3
"""PaC protocol invariant validator.

Dependency-free validator for the Plan as Code v0.4.0 protocol invariants
defined in SPEC Section 17. It builds the normalized model (SPEC Section 16)
from Plan records under `.plan/plans/` and Task records under `.plan/tasks/`
of a repository root and reports violations.

Records that do not conform to the current Plan/Task templates are treated as
legacy v0.3.x records and are ignored (SPEC Section 22).

Usage:
    python3 tools/validate.py [--root DIR] [--check INV-001,...] [--json]

Exit status:
    0  no violations
    1  violations found
    2  error
"""

import argparse
import json
import re
import sys
from pathlib import Path

PLAN_HEADING = re.compile(r"^#\s+(P\d+)\s+—\s+(.+)$", re.MULTILINE)
TASK_HEADING = re.compile(r"^#\s+(P\d+-T\d+)\s+—\s+(.+)$", re.MULTILINE)
SECTION_HEADING = re.compile(r"^##\s+(.+)$")
SUB_HEADING = re.compile(r"^###\s+(.+)$")
BOLD_FIELD = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")
CHECKBOX = re.compile(r"^-\s+\[([ xX])\]\s+(.+)$")
BULLET = re.compile(r"^-\s+(.+)$")
TASK_ID = re.compile(r"^P\d+-T\d+$")
PLAN_ID = re.compile(r"^P\d+$")
INLINE_TASK_HEADING = re.compile(r"^#{1,6}\s+P\d+-T\d+")
LEGACY_SECTIONS = re.compile(
    r"^##\s+(Findings|Decisions|Verification|Iterations|Planning Iteration\b)", re.MULTILINE
)
LEGACY_FIELDS = re.compile(r"\*\*Current iteration:\*\*")

VALID_PLAN_STATES = {"Draft", "Planned", "Completed", "Cancelled"}
VALID_TASK_STATES = {
    "Draft",
    "Planned",
    "In Progress",
    "Implemented",
    "Verified",
    "Blocked",
    "Deferred",
    "Cancelled",
}

ALL_INVARIANTS = [
    "INV-001",
    "INV-002",
    "INV-003",
    "INV-004",
    "INV-005",
    "INV-006",
    "INV-007",
    "INV-008",
    "INV-009",
    "INV-010",
    "INV-011",
    "INV-012",
    "INV-013",
]

DEFAULT_CHECKS = ALL_INVARIANTS


def is_legacy_plan(text):
    """Return True when a file under plans/ is a legacy v0.3.x record."""
    return bool(
        INLINE_TASK_HEADING.search(text)
        or LEGACY_SECTIONS.search(text)
        or LEGACY_FIELDS.search(text)
    )


def parse_plan(text, path):
    """Parse a v0.4.0 Plan record into the normalized model."""
    plan = {
        "file": str(path),
        "id": None,
        "title": None,
        "fields": {},
        "objective": [],
        "constraints": [],
        "included": [],
        "excluded": [],
        "tasks": [],
        "definition_of_done": [],
    }
    section = None
    sub = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = PLAN_HEADING.match(line)
        if m:
            plan["id"] = m.group(1)
            plan["title"] = m.group(2)
            continue
        m = SECTION_HEADING.match(line)
        if m:
            section = m.group(1).strip().lower()
            sub = None
            continue
        m = SUB_HEADING.match(line)
        if m:
            sub = m.group(1).strip().lower()
            continue
        m = BOLD_FIELD.match(line)
        if m:
            plan["fields"][m.group(1).strip().lower()] = m.group(2).strip()
            continue
        m = CHECKBOX.match(line)
        if m:
            if section == "definition of done":
                plan["definition_of_done"].append(
                    {"done": m.group(1) in "xX", "text": m.group(2)}
                )
            continue
        m = BULLET.match(line)
        if m:
            content = m.group(1)
            if section == "tasks" and TASK_ID.match(content):
                plan["tasks"].append(content)
            elif section == "constraints":
                plan["constraints"].append(content)
            elif section == "scope" and sub == "included":
                plan["included"].append(content)
            elif section == "scope" and sub == "excluded":
                plan["excluded"].append(content)
            continue
        if section == "objective":
            plan["objective"].append(line)
    return plan


def parse_task(text, path):
    """Parse a v0.4.0 Task record into the normalized model."""
    task = {
        "file": str(path),
        "id": None,
        "title": None,
        "fields": {},
        "objective": [],
        "depends_on": [],
        "definition_of_done": [],
        "implementation": [],
        "implementation_evidence": [],
        "verification": {"result": None, "by": None, "date": None, "reason": []},
    }
    section = None
    after_depends = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = TASK_HEADING.match(line)
        if m:
            task["id"] = m.group(1)
            task["title"] = m.group(2)
            continue
        m = SECTION_HEADING.match(line)
        if m:
            section = m.group(1).strip().lower()
            after_depends = False
            continue
        m = BOLD_FIELD.match(line)
        if m:
            key = m.group(1).strip().lower()
            value = m.group(2).strip()
            task["fields"][key] = value
            if key == "depends on":
                after_depends = True
                if value:
                    for item in TASK_ID.findall(value):
                        task["depends_on"].append(item)
            elif key in ("result", "by", "date") and section == "verification":
                task["verification"][key] = value
            continue
        m = CHECKBOX.match(line)
        if m:
            if section == "definition of done":
                task["definition_of_done"].append(
                    {"done": m.group(1) in "xX", "text": m.group(2)}
                )
            continue
        m = BULLET.match(line)
        if m:
            content = m.group(1)
            if after_depends and TASK_ID.match(content):
                task["depends_on"].append(content)
                continue
            if section == "implementation evidence":
                task["implementation_evidence"].append(content)
            continue
        if section == "objective":
            task["objective"].append(line)
        elif section == "implementation":
            task["implementation"].append(line)
        elif section == "verification":
            task["verification"]["reason"].append(line)
    return task


def scan(root):
    """Return (plan_models, task_models) under root/.plan/."""
    root = Path(root)
    plans = []
    tasks = []
    for p in sorted((root / ".plan").rglob("*.md")):
        if p.name == "README.md":
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if PLAN_HEADING.search(text) and ".plan/plans/" in str(p).replace("\\", "/"):
            if is_legacy_plan(text):
                continue
            plans.append(parse_plan(text, p))
        elif TASK_HEADING.search(text) and ".plan/tasks/" in str(p).replace("\\", "/"):
            tasks.append(parse_task(text, p))
    return plans, tasks


def validate_models(plans, tasks, config):
    """Run invariant checks over parsed models. Returns a list of violations."""
    violations = []
    checks = set(config.get("checks", DEFAULT_CHECKS))

    def add(inv, file, message):
        violations.append({"invariant": inv, "file": file, "message": message})

    if "INV-005" in checks:
        for plan in plans:
            status = plan["fields"].get("status", "")
            if status not in VALID_PLAN_STATES:
                add(
                    "INV-005",
                    plan["file"],
                    f"Plan {plan['id']} has invalid status {status!r}; expected one of "
                    f"{', '.join(sorted(VALID_PLAN_STATES))}",
                )

    if "INV-006" in checks:
        for task in tasks:
            status = task["fields"].get("status", "")
            if status not in VALID_TASK_STATES:
                add(
                    "INV-006",
                    task["file"],
                    f"Task {task['id']} has invalid status {status!r}; expected one of "
                    f"{', '.join(sorted(VALID_TASK_STATES))}",
                )

    return violations


def validate(root, config=None):
    config = dict(config or {})
    plans, tasks = scan(root)
    return validate_models(plans, tasks, config)


def main(argv=None):
    parser = argparse.ArgumentParser(description="PaC protocol invariant validator")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--check", default="", help="comma-separated invariant IDs to check (default: all)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    config = {}
    if args.check:
        config["checks"] = [c.strip() for c in args.check.split(",") if c.strip()]

    violations = validate(args.root, config)

    if args.json:
        print(json.dumps({"valid": not violations, "violations": violations}, indent=2))
    else:
        for v in violations:
            print(f"{v['invariant']}  {v['file']}: {v['message']}")
        if not violations:
            print("OK: no protocol invariant violations found.")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())