#!/usr/bin/env python3
"""Validate required assets and schemas in the bundled G&L V2 package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

root: Path = Path(__file__).resolve().parents[1]
required: list[str] = [
    "docs/V2-CONTRACT.md",
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


def main() -> int:
    """Validate bundled V2 artifacts, objectives, and runtime JSON schemas."""
    missing = [p for p in required if not (root / p).exists()]
    if missing:
        print("MISSING:")
        for p in missing:
            print(" -", p)
        return 1

    todo = (root / "artifacts/TODO.md").read_text(encoding="utf-8")
    count = todo.count("- [ ] OBJ-")
    if count < 10:
        print(f"TODO has only {count} objectives; minimum is 10", file=sys.stderr)
        return 1

    for schema in ("manifest.schema.json", "state.schema.json", "events.schema.json"):
        json.loads((root / "runtime" / schema).read_text(encoding="utf-8"))

    print("Package validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
