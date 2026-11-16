# Surgical Implementation (`surgical-implementation` v1.1.0)

**Verification-driven software implementation skill powered by the G&L V2 15-state engineering state machine.**

Part of the [Agent-Surgery-Skills](https://github.com/TeacherEvan/Agent-Surgery-Skills) family — alongside `surgical-orchestration`, `surgical-audit`, `surgical-hermesdothealth`, and `surgical-investigation`.

---

## What It Does

1. **Plan-Scan Dispatcher (Step 0)**: Always scans existing plans (`TODO.md`, `docs/plans/*.md`, `REQUIREMENTS.md`) with `rg -g` before creating redundant plans or overwriting work.
2. **G&L V2 State Machine (`INIT` → `DISCOVER` → ... → `HANDOFF` → `COMPLETE`)**:
   - Captures baseline code/worktree state, active agent contention, and orphaned servers in `DISCOVER`.
   - Locks immutable `REQ-NNN` requirements (`Investigator`) and <=14-day external research (`Researcher`).
   - Enforces modular architecture (`Architect`), atomic `OBJ-NNN` planning (`Planner`), and pre-code traceability (`Reviewer` at `CONSISTENCY_GATE`).
   - Isolates edits strictly to `<TARGET_SCOPE>` (`Implementer`), verifies with bounded retries <= 3 (`Verifier`), audits AST invariants (`Reviewer`), evaluates **CVSS v4.0 + EPSS + CISA KEV + SARIF 2.1.0** (`Security Auditor`), certifies `TRACEABILITY.md` (`Final Auditor`), and emits a grounded report (`Debriefer`).
3. **Least-Privilege Agent Envelopes**: All 10 subagent roles separate read visibility (`read_paths`) from minimal write targets (`allowed_paths`) and return Draft 2020-12 structured outputs validated against [`schemas/agent-envelope.schema.json`](schemas/agent-envelope.schema.json).
4. **Unified Ephemeral Workspace**: Active G&L V2 run artifacts, retry logs, and runtime telemetry live strictly inside the target repository's `<RUN_WORKSPACE>/docs/.scratch-audit/`, keeping source trees and skill installations clean.

---

## Repository Layout

```text
Surgical-Implementation/
├── SKILL.md                          # Core skill definition (v1.1.0, <=250 lines)
├── README.md                         # Repository documentation
├── AGENTS.md                         # AI agent engineering conventions & gates
├── LICENSE                           # MIT License
├── references/                       # On-demand contracts, runbooks, & pitfalls
│   ├── v2-governance.md              # State machine, gates, retries, 11-class taxonomy
│   ├── v2-agent-envelopes.md         # 10 least-privilege mission envelopes & runtime adapter
│   ├── v2-artifact-templates.md      # Templates #1–#17 + runtime schema examples
│   ├── plan-scan-dispatcher.md       # Step 0 routing rules & `-g` scan command
│   ├── implementation-pitfalls.md    # Dual-agent, policy, AST, Three.js, Blender, Done rules
│   ├── git-recovery-and-scan.md      # Untracked work recovery & clone disambiguation
│   ├── convex-array-index-match.md   # Document ID vs positional array index mutations
│   ├── places-api-radius.md          # Geolocation API radius/unit bounds
│   ├── browser-real-profile.md       # chrome-devtools MCP & headless Chromium fallbacks
│   └── skill-update-note.md          # Audit-hygiene notes aligned with surgical-audit
├── schemas/                          # Standalone Draft 2020-12 JSON Schemas
│   ├── agent-envelope.schema.json    # Mission envelope schema (forbids wildcard writes)
│   └── retry-log.schema.json         # Bounded-retry JSONL entry schema
├── scripts/                          # Repo-only validation & local-install mirror tooling
│   ├── conform.py                    # Canonical family conformance checker
│   └── sync-skill.sh                 # Mirror & byte-verify into all local agent install roots
├── tests/                            # Behavioural, schema, envelope & mirror tests
│   └── test_surgical_implementation.py
├── GLE_Software_Engineering_Auditor_V2_ULTIMATE/
│   └── ...                           # Bundled V2 reference package & runtime schemas
├── docs/plans/                       # Historical design & implementation records
└── .github/workflows/skill-ci.yml    # GitHub Actions CI gate
```

---

## Local Validation & Sync

```bash
# 1. Family conformance check
python3 -B scripts/conform.py

# 2. Bundled V2 package validation
python3 -B GLE_Software_Engineering_Auditor_V2_ULTIMATE/scripts/validate-package.py

# 3. Behavioural, schema, envelope & mirror tests
pytest -o cache_dir=/tmp/pytest-impl -v tests/

# 4. Static lint, format, strict types, schemas & CI YAML
ruff check --no-cache .
ruff format --check --no-cache .
mypy --strict --cache-dir /tmp/mypy-impl scripts/ GLE_Software_Engineering_Auditor_V2_ULTIMATE/scripts/ tests/
check-jsonschema --check-metaschema schemas/*.schema.json GLE_Software_Engineering_Auditor_V2_ULTIMATE/runtime/*.schema.json
shellcheck -x scripts/sync-skill.sh
yamllint .github/workflows/skill-ci.yml

# 5. Mirror into local agent skill directories & verify byte parity
bash scripts/sync-skill.sh sync
bash scripts/sync-skill.sh verify
```

---

## License & Author

MIT License — see [LICENSE](LICENSE).  
Authors: TeacherEvan, Fenrie (Lea's AI wolf), Hermes Agent.
