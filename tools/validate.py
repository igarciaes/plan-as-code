#!/usr/bin/env python3
"""PaC protocol invariant validator.

Dependency-free validator for the Plan as Code protocol invariants defined in
SPEC Section 28. It builds the normalized model (SPEC Section 20) from plan
records and feedback threads under a repository root and reports violations.

Usage:
    python3 tools/validate.py [--root DIR] [--check INV-001,...] \
        [--min-verification LEVEL] [--json]

The repository may declare a verification minimum in `.plan/README.md` with a
`**Verification minimum:** Level N` (or `N`) line, for example:

    **Verification minimum:** Level 2

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
TASK_HEADING = re.compile(r"^#{2,4}\s+(P\d+-T\d+)\s+—\s+(.+)$")
FINDING_HEADING = re.compile(r"^#{2,4}\s+(P\d+-T\d+-F\d+)\s+—\s+(.+)$")
DECISION_HEADING = re.compile(r"^#{2,4}\s+(P\d+-D\d+)\s+—\s+(.+)$")
VERIFICATION_HEADING = re.compile(r"^#{2,4}\s+(P\d+-T\d+)\s*$")
SECTION_HEADING = re.compile(r"^##\s+(.+)$")
SUB_HEADING = re.compile(r"^#{2,4}\s+(.+)$")
BOLD_FIELD = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")
CHECKBOX = re.compile(r"^-\s+\[([ x])\]\s+(.+)$")
BULLET = re.compile(r"^-\s+(.+)$")
AC_ITEM = re.compile(r"^(AC-P\d+-T\d+-\d+)\s+—\s+(.+)$")
ID_RE = re.compile(r"(P\d+(?:-T\d+)?(?:-F\d+)?(?:-D\d+)?)")
RELATIONSHIP_ITEM = re.compile(r"^(depends-on|blocks|requires|conflicts-with|supersedes)\s+(P\d+-T\d+)$")
FEEDBACK_HEADING = re.compile(r"^#\s+Feedback\s+—\s+(.+)$", re.MULTILINE)
FEEDBACK_ITEM = re.compile(r"^##\s+(P\d+(?:-T\d+)?(?:-F\d+)?-FB\d+)\s+—\s+(.+)$")

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

DEFAULT_CHECKS = ALL_INVARIANTS + ["STATE"]


def parse_plan(text, path):
    """Parse a plan record into the normalized model."""
    plan = {
        "file": str(path),
        "id": None,
        "title": None,
        "fields": {},
        "objective": [],
        "constraints": [],
        "tasks": [],
        "findings": [],
        "decisions": [],
        "verifications": [],
    }
    current = "plan"
    entity = None
    sub = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = PLAN_HEADING.match(line)
        if m:
            plan["id"] = m.group(1)
            plan["title"] = m.group(2)
            current = "plan"
            entity = None
            continue
        m = FINDING_HEADING.match(line)
        if m:
            entity = {"id": m.group(1), "title": m.group(2), "fields": {}, "references": []}
            plan["findings"].append(entity)
            current = "finding"
            sub = None
            continue
        m = DECISION_HEADING.match(line)
        if m:
            entity = {"id": m.group(1), "title": m.group(2), "fields": {}}
            plan["decisions"].append(entity)
            current = "decision"
            sub = None
            continue
        m = TASK_HEADING.match(line)
        if m:
            entity = {"id": m.group(1), "title": m.group(2), "fields": {}, "dependencies": [], "relationships": [], "acceptance": []}
            plan["tasks"].append(entity)
            current = "task"
            sub = None
            continue
        m = VERIFICATION_HEADING.match(line)
        if m:
            entity = {"id": m.group(1), "fields": {}, "evidence": [], "acceptance": []}
            plan["verifications"].append(entity)
            current = "verification"
            sub = None
            continue
        m = SECTION_HEADING.match(line)
        if m:
            current = "section"
            entity = None
            sub = None
            continue
        m = SUB_HEADING.match(line)
        if m:
            sub = m.group(1).strip().lower()
            continue
        m = BOLD_FIELD.match(line)
        if m:
            key = m.group(1).strip().lower()
            value = m.group(2).strip()
            if current == "plan" or (entity is None and current == "section"):
                plan["fields"][key] = value
            elif entity is not None:
                entity["fields"][key] = value
                if key == "depends on" and value:
                    for dep in ID_RE.findall(value):
                        if re.fullmatch(r"P\d+-T\d+", dep):
                            entity["dependencies"].append(dep)
            continue
        m = CHECKBOX.match(line)
        if m:
            text = m.group(2)
            am = AC_ITEM.match(text)
            if current == "task" and entity is not None and sub == "acceptance":
                entity["acceptance"].append(
                    {"id": am.group(1) if am else None, "text": am.group(2) if am else text}
                )
            elif current == "verification" and entity is not None and sub == "acceptance":
                entity["acceptance"].append(text)
            continue
        m = BULLET.match(line)
        if m:
            content = m.group(1)
            if current == "task" and entity is not None and sub != "acceptance":
                rm = RELATIONSHIP_ITEM.match(content)
                if rm:
                    entity["relationships"].append({"type": rm.group(1), "target": rm.group(2)})
                elif re.fullmatch(r"P\d+-T\d+", content):
                    entity["dependencies"].append(content)
            elif current == "verification" and entity is not None and sub == "evidence":
                entity["evidence"].append(content)
            elif current == "finding" and entity is not None:
                for ref in ID_RE.findall(content):
                    entity["references"].append(ref)
            continue
        if current == "section" and entity is None:
            plan["objective"].append(line)
    return plan


def parse_feedback(text, path):
    """Parse a feedback thread into a dict keyed by subject."""
    thread = {"file": str(path), "subject": None, "items": []}
    item = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = FEEDBACK_HEADING.match(line)
        if m:
            thread["subject"] = m.group(1).strip()
            continue
        m = FEEDBACK_ITEM.match(line)
        if m:
            item = {"id": m.group(1), "kind": m.group(2).strip(), "fields": {}, "content": []}
            thread["items"].append(item)
            continue
        m = BOLD_FIELD.match(line)
        if m and item is not None:
            item["fields"][m.group(1).strip().lower()] = m.group(2).strip()
            continue
        if item is not None and not line.startswith("---"):
            item["content"].append(line)
    return thread


def _parse_level(value):
    if not value:
        return None
    m = re.search(r"(\d+)", value)
    return int(m.group(1)) if m else None


def validate_models(plans, threads, config):
    """Run invariant checks over parsed models. Returns a list of violations."""
    violations = []
    checks = set(config.get("checks", DEFAULT_CHECKS))
    min_level = config.get("min_verification", 1)

    task_index = {}
    ac_index = {}
    finding_index = {}
    verification_index = {}
    for plan in plans:
        pid = plan["id"]
        for task in plan["tasks"]:
            task_index[task["id"]] = pid
            for ac in task["acceptance"]:
                if ac["id"]:
                    ac_index.setdefault(ac["id"], []).append(task["id"])
        for finding in plan["findings"]:
            finding_index[finding["id"]] = pid
        for v in plan["verifications"]:
            verification_index.setdefault((pid, v["id"]), []).append(v)

    def add(inv, file, message):
        violations.append({"invariant": inv, "file": file, "message": message})

    if "INV-001" in checks:
        counts = {}
        for p in plans:
            counts[p["id"]] = counts.get(p["id"], 0) + 1
        for pid, n in counts.items():
            if n > 1:
                add("INV-001", plans[0]["file"], f"duplicate Plan ID {pid!r} used {n} times")

    if "INV-002" in checks:
        counts = {}
        for plan in plans:
            for task in plan["tasks"]:
                counts[task["id"]] = counts.get(task["id"], 0) + 1
        for tid, n in counts.items():
            if n > 1:
                add("INV-002", next(p["file"] for p in plans), f"duplicate Task ID {tid!r} used {n} times")

    if "INV-003" in checks:
        for plan in plans:
            for task in plan["tasks"]:
                m = re.fullmatch(r"(P\d+)-T\d+", task["id"])
                if m and m.group(1) != plan["id"]:
                    add(
                        "INV-003",
                        plan["file"],
                        f"Task {task['id']} belongs to Plan {m.group(1)}, not {plan['id']}",
                    )

    if "INV-004" in checks:
        ac_owners = {}
        for plan in plans:
            for task in plan["tasks"]:
                seen_acs = set()
                for ac in task["acceptance"]:
                    if ac["id"] is None:
                        continue
                    m = re.fullmatch(r"AC-(P\d+-T\d+)-\d+", ac["id"])
                    if m and m.group(1) != task["id"]:
                        add(
                            "INV-004",
                            plan["file"],
                            f"Acceptance criterion {ac['id']} in Task {task['id']} belongs to Task {m.group(1)}",
                        )
                    if ac["id"] in seen_acs:
                        add("INV-004", plan["file"], f"duplicate acceptance criterion {ac['id']!r} in Task {task['id']}")
                    seen_acs.add(ac["id"])
                    ac_owners.setdefault(ac["id"], []).append(task["id"])
        for ac_id, owners in ac_owners.items():
            if len(set(owners)) > 1:
                add(
                    "INV-004",
                    plans[0]["file"],
                    f"acceptance criterion {ac_id!r} belongs to more than one task: {', '.join(sorted(set(owners)))}",
                )

    if "INV-005" in checks:
        for plan in plans:
            for task in plan["tasks"]:
                for dep in task["dependencies"]:
                    if dep not in task_index:
                        add("INV-005", plan["file"], f"Task {task['id']} references missing target {dep!r}")
                for rel in task["relationships"]:
                    if rel["target"] not in task_index:
                        add(
                            "INV-005",
                            plan["file"],
                            f"Task {task['id']} relationship {rel['type']} references missing target {rel['target']!r}",
                        )
            for finding in plan["findings"]:
                for ref in finding["references"]:
                    if re.fullmatch(r"P\d+-T\d+", ref) and ref not in task_index:
                        add("INV-005", plan["file"], f"Finding {finding['id']} references missing task {ref!r}")
            for decision in plan["decisions"]:
                affected = decision["fields"].get("affected", "")
                for ref in ID_RE.findall(affected):
                    if re.fullmatch(r"P\d+-T\d+", ref) and ref not in task_index:
                        add("INV-005", plan["file"], f"Decision {decision['id']} references missing task {ref!r}")

    if "INV-006" in checks:
        for plan in plans:
            adj = {}
            known = set(task_index)  # all known tasks, may span plans
            for task in plan["tasks"]:
                adj.setdefault(task["id"], [])
                for dep in task["dependencies"]:
                    if dep in known:
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
                add("INV-006", plan["file"], f"dependency cycle detected: {' -> '.join(cycle)}")

    if "INV-013" in checks:
        for plan in plans:
            for task in plan["tasks"]:
                positive = set()
                conflicts = set()
                for dep in task["dependencies"]:
                    positive.add(dep)
                for rel in task["relationships"]:
                    if rel["type"] in ("depends-on", "requires"):
                        positive.add(rel["target"])
                    elif rel["type"] == "conflicts-with":
                        conflicts.add(rel["target"])
                for target in sorted(positive & conflicts):
                    add(
                        "INV-013",
                        plan["file"],
                        f"Task {task['id']} both depends-on/requires and conflicts-with target {target!r}",
                    )

    if "INV-007" in checks or "INV-008" in checks:
        for plan in plans:
            for task in plan["tasks"]:
                if task["fields"].get("status") != "Verified":
                    continue
                records = verification_index.get((plan["id"], task["id"]), [])
                if not records:
                    if "INV-007" in checks:
                        add(
                            "INV-007",
                            plan["file"],
                            f"Task {task['id']} is Verified but has no verification record",
                        )
                    if "INV-008" in checks:
                        add(
                            "INV-008",
                            plan["file"],
                            f"Task {task['id']} is Verified but has no verification evidence",
                        )
                    continue
                record = records[0]
                level = _parse_level(
                    record["fields"].get("independence") or record["fields"].get("independence level")
                )
                if level is None:
                    level = 1
                if "INV-007" in checks and level < min_level:
                    add(
                        "INV-007",
                        plan["file"],
                        f"Task {task['id']} verification independence level {level} below "
                        f"required minimum {min_level}",
                    )
                if "INV-008" in checks and not record["evidence"]:
                    add(
                        "INV-008",
                        plan["file"],
                        f"Task {task['id']} verification record has no verification evidence",
                    )

    if "INV-009" in checks:
        for plan in plans:
            seen = set()
            for finding in plan["findings"]:
                if not re.fullmatch(r"P\d+-T\d+-F\d+", finding["id"]):
                    add("INV-009", plan["file"], f"finding has malformed stable ID {finding['id']!r}")
                if finding["id"] in seen:
                    add("INV-009", plan["file"], f"duplicate finding ID {finding['id']!r}")
                seen.add(finding["id"])

    if "INV-010" in checks:
        for thread in threads:
            seen = set()
            subject = thread["subject"] or ""
            for item in thread["items"]:
                if item["id"] in seen:
                    add("INV-010", thread["file"], f"duplicate feedback item ID {item['id']!r}")
                seen.add(item["id"])
                if subject and not item["id"].startswith(subject + "-FB"):
                    add(
                        "INV-010",
                        thread["file"],
                        f"feedback item {item['id']} does not belong to subject {subject!r}",
                    )

    if "INV-011" in checks:
        for plan in plans:
            seen = set()
            for decision in plan["decisions"]:
                if not re.fullmatch(r"P\d+-D\d+", decision["id"]):
                    add("INV-011", plan["file"], f"decision has malformed ID {decision['id']!r}")
                if decision["id"] in seen:
                    add("INV-011", plan["file"], f"duplicate decision ID {decision['id']!r}")
                seen.add(decision["id"])
            iteration = plan["fields"].get("current iteration")
            disposition = any(
                f["fields"].get("status") in {"Resolved", "Accepted", "Invalid", "Superseded"}
                for f in plan["findings"]
            )
            if ((iteration and str(iteration).strip().isdigit() and int(iteration) > 1) or disposition) and not plan["decisions"]:
                add(
                    "INV-011",
                    plan["file"],
                    f"plan changes are not traceable to decisions (iteration {iteration!r}, "
                    f"findings disposition present) but no decisions are recorded",
                )

    if "STATE" in checks:
        for plan in plans:
            for task in plan["tasks"]:
                status = task["fields"].get("status", "")
                if status not in VALID_TASK_STATES:
                    add(
                        "STATE",
                        plan["file"],
                        f"Task {task['id']} has invalid status {status!r}; expected one of "
                        f"{', '.join(sorted(VALID_TASK_STATES))}",
                    )

    if "INV-012" in checks:
        for plan in plans:
            if not plan["file"].endswith(".plan/plans/" + plan["id"] + ".md") and ".plan/plans/" not in plan["file"]:
                add("INV-012", plan["file"], f"plan record {plan['id']} is not stored under .plan/plans/")
            for task in plan["tasks"]:
                owner = task["fields"].get("owner", "")
                if owner.lower() == "planner":
                    add(
                        "INV-012",
                        plan["file"],
                        f"Task {task['id']} is owned by the Planner; the Planner MUST NOT execute implementation tasks",
                    )
        for thread in threads:
            if ".plan/feedback/" not in thread["file"]:
                add("INV-012", thread["file"], f"feedback thread {thread['subject']!r} is not stored under .plan/feedback/")

    return violations


def load_repo_config(root):
    cfg = {}
    readme = Path(root) / ".plan" / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        m = re.search(r"\*\*Verification minimum:\*\*\s*(?:Level\s*)?(\d+)", text, re.I)
        if m:
            cfg["min_verification"] = int(m.group(1))
    return cfg


def scan(root):
    """Return (plan_files, feedback_files) under root/.plan/."""
    root = Path(root)
    plans = []
    threads = []
    for p in sorted((root / ".plan").rglob("*.md")):
        if p.name == "README.md":
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if PLAN_HEADING.search(text):
            plans.append((p, text))
        elif FEEDBACK_HEADING.search(text):
            threads.append((p, text))
    return plans, threads


def validate(root, config=None):
    config = dict(config or {})
    repo_cfg = load_repo_config(root)
    config.setdefault("min_verification", repo_cfg.get("min_verification", 1))
    plans, threads = scan(root)
    plan_models = [parse_plan(text, str(p)) for p, text in plans]
    thread_models = [parse_feedback(text, str(p)) for p, text in threads]
    return validate_models(plan_models, thread_models, config)


def main(argv=None):
    parser = argparse.ArgumentParser(description="PaC protocol invariant validator")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--check", default="", help="comma-separated invariant IDs to check (default: all)")
    parser.add_argument("--min-verification", type=int, default=None, help="minimum verification level (default: from .plan/README.md or 1)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    config = load_repo_config(args.root)
    if args.min_verification is not None:
        config["min_verification"] = args.min_verification
    config.setdefault("min_verification", 1)
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