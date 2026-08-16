#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md",
    "README.md",
    "agents/investigator.md",
    "agents/researcher.md",
    "agents/architect.md",
    "agents/planner.md",
    "agents/reviewer.md",
    "agents/implementer.md",
    "agents/verifier.md",
    "agents/security-auditor.md",
    "agents/final-auditor.md",
    "agents/debriefer.md",
    "artifacts/REQUIREMENTS.md",
    "artifacts/CODEBASE-STATE.md",
    "artifacts/ARCHITECTURE.md",
    "artifacts/TODO.md",
    "artifacts/debrief.md",
    "audit/TRACEABILITY.md",
    "audit/SECURITY.md",
    "audit/RISK.md",
    "research/SOURCES.md",
    "research/FINDINGS.md",
    "research/DECISIONS.md",
    "runtime/manifest.schema.json",
    "runtime/state.schema.json",
    "runtime/events.schema.json",
]
missing = [p for p in required if not (root/p).exists()]
if missing:
    print("MISSING:")
    for p in missing: print(" -", p)
    raise SystemExit(1)

todo = (root/"artifacts/TODO.md").read_text()
count = todo.count("- [ ] OBJ-")
if count < 10:
    raise SystemExit(f"TODO has only {count} objectives; minimum is 10")

for schema in ["manifest.schema.json","state.schema.json","events.schema.json"]:
    json.loads((root/"runtime"/schema).read_text())

print("Package validation: PASS")
