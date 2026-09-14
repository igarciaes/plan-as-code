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
    "Changes Requested",
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
        has_plan = PLAN_HEADING.search(text)
        has_task = TASK_HEADING.search(text)
        if has_plan and not has_task:
            if is_legacy_plan(text):
                continue
            plans.append(parse_plan(text, p))
        elif has_task:
            tasks.append(parse_task(text, p))
    return plans, tasks


def validate_models(plans, tasks, config):
    """Run invariant checks over parsed models. Returns a list of violations."""
    violations = []
    checks = set(config.get("checks", DEFAULT_CHECKS))

    def add(inv, file, message):
        violations.append({"invariant": inv, "file": file, "message": message})

    plan_index = {}
    for plan in plans:
        plan_index.setdefault(plan["id"], []).append(plan)
    task_index = {}
    for task in tasks:
        task_index.setdefault(task["id"], []).append(task)

    if "INV-001" in checks:
        for pid, group in plan_index.items():
            if len(group) > 1:
                add(
                    "INV-001",
                    group[0]["file"],
                    f"duplicate Plan ID {pid!r} used {len(group)} times",
                )

    if "INV-002" in checks:
        for tid, group in task_index.items():
            if len(group) > 1:
                add(
                    "INV-002",
                    group[0]["file"],
                    f"duplicate Task ID {tid!r} used {len(group)} times",
                )

    if "INV-003" in checks:
        for task in tasks:
            plan_id = task["fields"].get("plan", "")
            if not plan_id:
                add(
                    "INV-003",
                    task["file"],
                    f"Task {task['id']} does not reference a parent Plan",
                )
            elif plan_id not in plan_index:
                add(
                    "INV-003",
                    task["file"],
                    f"Task {task['id']} references missing Plan {plan_id!r}",
                )
        for plan in plans:
            for tid in plan["tasks"]:
                if tid not in task_index:
                    add(
                        "INV-003",
                        plan["file"],
                        f"Plan {plan['id']} references missing Task {tid!r}",
                    )

    if "INV-004" in checks:
        for task in tasks:
            m = re.fullmatch(r"(P\d+)-T\d+", task["id"])
            plan_id = task["fields"].get("plan", "")
            if m and plan_id and m.group(1) != plan_id:
                add(
                    "INV-004",
                    task["file"],
                    f"Task {task['id']} belongs to Plan {m.group(1)}, not {plan_id!r}",
                )

    if "INV-007" in checks:
        for task in tasks:
            for dep in task["depends_on"]:
                if dep not in task_index:
                    add(
                        "INV-007",
                        task["file"],
                        f"Task {task['id']} depends on missing Task {dep!r}",
                    )

    if "INV-008" in checks:
        adj = {}
        for task in tasks:
            adj.setdefault(task["id"], [])
            for dep in task["depends_on"]:
                if dep in task_index:
                    adj.setdefault(dep, [])
                    adj[task["id"]].append(dep)
        gray = set()
        black = set()
        cycles = []

        def dfs(node, path):
            gray.add(node)
            path.append(node)
            for nb in adj.get(node, []):
                if nb in gray:
                    idx = path.index(nb)
                    cycles.append(path[idx:] + [nb])
                elif nb not in black:
                    dfs(nb, path)
            gray.discard(node)
            black.add(node)
            path.pop()

        for tid in list(adj):
            if tid not in gray and tid not in black:
                dfs(tid, [])
        for cycle in cycles:
            add("INV-008", tasks[0]["file"] if tasks else "<none>", f"dependency cycle detected: {' -> '.join(cycle)}")

    if "INV-012" in checks:
        for plan in plans:
            if plan["fields"].get("status") != "Completed":
                continue
            for tid, group in task_index.items():
                task = group[0]
                if task["fields"].get("plan", "") != plan["id"]:
                    continue
                if task["fields"].get("status") not in ("Verified", "Cancelled"):
                    add(
                        "INV-012",
                        plan["file"],
                        f"Plan {plan['id']} is Completed but required Task {tid} is "
                        f"{task['fields'].get('status', '')!r} (not Verified)",
                    )

    if "INV-013" in checks:
        for plan in plans:
            p = Path(plan["file"])
            if p.parent.name != "plans" or ".plan" not in p.parts or p.name != plan["id"] + ".md":
                add(
                    "INV-013",
                    plan["file"],
                    f"Plan record {plan['id']} is not stored at .plan/plans/{plan['id']}.md",
                )
        for task in tasks:
            p = Path(task["file"])
            if p.parent.name != "tasks" or ".plan" not in p.parts or p.name != task["id"] + ".md":
                add(
                    "INV-013",
                    task["file"],
                    f"Task record {task['id']} is not stored at .plan/tasks/{task['id']}.md",
                )

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

    if "INV-011" in checks:
        for task in tasks:
            status = task["fields"].get("status", "")
            verified = status == "Verified" or task["verification"]["result"] == "Verified"
            if not verified:
                continue
            unchecked = [
                item["text"] for item in task["definition_of_done"] if not item["done"]
            ]
            if unchecked:
                add(
                    "INV-011",
                    task["file"],
                    f"Task {task['id']} is Verified but its Definition of Done has "
                    f"unchecked condition(s): {', '.join(unchecked)}",
                )
            if not task["definition_of_done"]:
                add(
                    "INV-011",
                    task["file"],
                    f"Task {task['id']} is Verified but has no Definition of Done",
                )

    if "INV-009" in checks:
        for task in tasks:
            owner = task["fields"].get("owner", "")
            status = task["fields"].get("status", "")
            verifier = task["verification"]["by"]
            if owner.lower() == "planner":
                add(
                    "INV-009",
                    task["file"],
                    f"Task {task['id']} is owned by the Planner; the Planner MUST NOT execute implementation tasks",
                )
            verified = status == "Verified" or task["verification"]["result"] == "Verified"
            if verified and verifier and owner and verifier.lower() == owner.lower():
                add(
                    "INV-009",
                    task["file"],
                    f"Task {task['id']} was marked Verified by its Implementer "
                    f"({owner}); only the Planner MAY mark a Task Verified",
                )

    if "INV-010" in checks:
        for task in tasks:
            status = task["fields"].get("status", "")
            ver = task["verification"]
            if status == "Verified" and ver["result"] != "Verified":
                add(
                    "INV-010",
                    task["file"],
                    f"Task {task['id']} has status Verified but its verification result "
                    f"is {ver['result']!r}",
                )
            if status == "Verified" and not ver["by"]:
                add(
                    "INV-010",
                    task["file"],
                    f"Task {task['id']} is Verified but has no Planner verification record",
                )
            if ver["result"] == "Verified" and status != "Verified":
                add(
                    "INV-010",
                    task["file"],
                    f"Task {task['id']} has verification result Verified but status is "
                    f"{status!r}; Implemented does not imply Verified",
                )
            if status == "Changes Requested":
                if ver["result"] != "Changes Requested":
                    add(
                        "INV-010",
                        task["file"],
                        f"Task {task['id']} has status Changes Requested but its verification "
                        f"result is {ver['result']!r}",
                    )
                if not ver["reason"]:
                    add(
                        "INV-010",
                        task["file"],
                        f"Task {task['id']} is Changes Requested but no reason is recorded",
                    )
            if ver["result"] == "Changes Requested" and status != "Changes Requested":
                add(
                    "INV-010",
                    task["file"],
                    f"Task {task['id']} has verification result Changes Requested but status "
                    f"is {status!r}",
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