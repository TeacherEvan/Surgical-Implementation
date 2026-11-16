# G&L V2 Agent Envelopes & Delegation Contract

All V2 subagent missions use **least-privilege write envelopes** (`allowed_paths`) separate from read visibility (`read_paths`), unified runtime state under `<RUN_WORKSPACE>/docs/.scratch-audit/`, and machine-checkable Draft 2020-12 `return_schema` contracts validated against [`schemas/agent-envelope.schema.json`](../schemas/agent-envelope.schema.json).

---

## Placeholder & Directory Conventions

| Placeholder | Meaning | Constraint |
| --- | --- | --- |
| `<RUN_WORKSPACE>` | Absolute or repo-relative root of the active workspace | Never used in `allowed_paths` with `/**` |
| `<TARGET_SCOPE>` | Explicit package, directory, or module list under modification | Assigned per objective before `IMPLEMENT`; never `*` or `.` without plan approval |
| `<RUN_WORKSPACE>/docs/.scratch-audit/` | Canonical ephemeral G&L V2 workspace root | Shared across `SKILL.md`, templates, schemas, and all 10 roles |

> **Least-Privilege Rule**: `read_paths` grants non-destructive read visibility into `<RUN_WORKSPACE>/**` (all 10 roles, including `Researcher` for stack/manifest context). `allowed_paths` strictly enumerates write-permitted targets only. No role may hold `"<RUN_WORKSPACE>/**"` in `allowed_paths`.

---

## Agent Role & Capability Matrix

| Role | Phase / State(s) | Read Repo (`read_paths`) | Write Scope (`allowed_paths` summary) | Web Search | Shell Mode |
| --- | --- | --- | --- | --- | --- |
| `Investigator` | `INIT`, `DISCOVER`, `REQUIREMENTS`, `CODEBASE_STATE` | `YES` | `REQUIREMENTS.md`, `CODEBASE-STATE.md`, `runtime/{manifest.json,state.json,events.jsonl}` | `NO` | `READ_ONLY` |
| `Researcher` | `RESEARCH` | `YES` *(context only; never edits code)* | `research/{SOURCES.md,FINDINGS.md,DECISIONS.md}` | `YES` | `NONE` |
| `Architect` | `ARCHITECT` | `YES` | `ARCHITECTURE.md` | `NO` | `READ_ONLY` |
| `Planner` | `PLAN` | `YES` | `TODO.md` | `NO` | `READ_ONLY` |
| `Reviewer` | `CONSISTENCY_GATE`, `FINAL_AUDIT` | `YES` | `TRACEABILITY.md`, `audit/logs/retry-CONSISTENCY_GATE.jsonl`, `runtime/events.jsonl` | `NO` | `READ_ONLY` |
| `Implementer` | `IMPLEMENT` | `YES` | `<TARGET_SCOPE>/**`, `TODO.md` | `NO` | `FULL_BUILD` |
| `Verifier` | `VERIFY` | `YES` | `CODEBASE-STATE.md`, `audit/logs/retry-VERIFY.jsonl`, `runtime/events.jsonl` | `NO` | `TEST_RUN` |
| `Security Auditor` | `SECURITY_AUDIT` | `YES` | `SECURITY.md`, `RISK.md`, `runtime/events.jsonl` | `NO` | `SECURITY_SCAN` |
| `Final Auditor` | `FINAL_AUDIT`, `COMPLETE` | `YES` | `TRACEABILITY.md`, `runtime/{manifest.json,state.json,events.jsonl}` | `NO` | `READ_ONLY` |
| `Debriefer` | `DEBRIEF`, `HANDOFF` | `YES` | `debrief.md` | `NO` | `NONE` |

---

## Canonical Mission Envelopes (10 Roles)

### 1. Investigator (`M-01-DISCOVER`)

Captures baseline environment, git/workspace state, dependency manifests, and immutable requirements (`REQUIREMENTS.md`), and bootstraps `runtime/{manifest.json,state.json,events.jsonl}`.

```json
{
  "mission_id": "M-01-DISCOVER",
  "role": "Investigator",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/REQUIREMENTS.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/CODEBASE-STATE.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/manifest.json",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/state.json",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/events.jsonl"
  ],
  "principles": [
    "No unverified assumptions: inspect actual files, lockfiles, git status, and running processes before stating baseline facts.",
    "Preserve immutable user constraints verbatim with REQ-NNN IDs in REQUIREMENTS.md.",
    "Never modify source code or committed plan files during discovery."
  ],
  "max_tool_calls": 40,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "run_id",
      "requirements_count",
      "artifacts_written",
      "competing_agents_detected"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "BLOCKED"]
      },
      "run_id": {
        "type": "string",
        "minLength": 1
      },
      "requirements_count": {
        "type": "integer",
        "minimum": 1
      },
      "artifacts_written": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "minLength": 1 }
      },
      "competing_agents_detected": {
        "type": "boolean"
      }
    }
  }
}
```

### 2. Researcher (`M-02-RESEARCH`)

Verifies external APIs, dependency versions, breaking changes, and security advisories with pinned source citations (`research/{SOURCES,FINDINGS,DECISIONS}.md`). Reads the workspace for stack/version context only (`YES`) and never edits code.

```json
{
  "mission_id": "M-02-RESEARCH",
  "role": "Researcher",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/research/SOURCES.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/research/FINDINGS.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/research/DECISIONS.md"
  ],
  "principles": [
    "Read the workspace solely for dependency/version/API context; never propose unverified third-party APIs from memory.",
    "Cite pinned documentation URLs, package versions, and publication/retrieval dates in research/SOURCES.md.",
    "Record crisp architectural trade-offs and rejected options in research/DECISIONS.md."
  ],
  "max_tool_calls": 30,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "sources_verified",
      "decisions_recorded",
      "blocking_unknowns"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "NEEDS_USER_INPUT"]
      },
      "sources_verified": {
        "type": "integer",
        "minimum": 0
      },
      "decisions_recorded": {
        "type": "array",
        "items": { "type": "string", "minLength": 1 }
      },
      "blocking_unknowns": {
        "type": "array",
        "items": { "type": "string" }
      }
    }
  }
}
```

### 3. Architect (`M-03-ARCHITECT`)

Designs concrete module boundaries, data/control flows, failure modes, and accessible Mermaid diagrams (`accTitle:` / `accDescr:`) in `ARCHITECTURE.md`.

```json
{
  "mission_id": "M-03-ARCHITECT",
  "role": "Architect",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/ARCHITECTURE.md"
  ],
  "principles": [
    "Map every architectural component back to at least one REQ-NNN in REQUIREMENTS.md.",
    "Consolidate shared policy/business logic into single pure modules rather than scattering duplicated constants.",
    "Every Mermaid diagram must include accessibility metadata (accTitle and accDescr) and match real module names."
  ],
  "max_tool_calls": 30,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "components",
      "target_scopes",
      "diagrams_with_a11y"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "BLOCKED"]
      },
      "components": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "minLength": 1 }
      },
      "target_scopes": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "minLength": 1 }
      },
      "diagrams_with_a11y": {
        "type": "integer",
        "minimum": 1
      }
    }
  }
}
```

### 4. Planner (`M-04-PLAN`)

Produces dependency-ordered `OBJ-NNN` work items in `TODO.md`, each tied to an explicit `<TARGET_SCOPE>`, acceptance criterion, and verification command.

```json
{
  "mission_id": "M-04-PLAN",
  "role": "Planner",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/TODO.md"
  ],
  "principles": [
    "Every OBJ-NNN must list exact target file scope, prerequisite IDs, concrete exit tests, and mapped REQ-NNN IDs.",
    "Order foundational schemas, migrations, and shared helpers ahead of downstream consumers.",
    "Keep each objective atomic enough to implement and verify within one scoped mission."
  ],
  "max_tool_calls": 25,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "objective_ids",
      "unmapped_requirements",
      "dependency_cycles"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "BLOCKED"]
      },
      "objective_ids": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "pattern": "^OBJ-[0-9]{3}$" }
      },
      "unmapped_requirements": {
        "type": "array",
        "items": { "type": "string" }
      },
      "dependency_cycles": {
        "type": "integer",
        "const": 0
      }
    }
  }
}
```

### 5. Reviewer (`M-05-REVIEW`)

Runs `CONSISTENCY_GATE` (before coding) and `FINAL_AUDIT` traceability checks (after verification), updating `TRACEABILITY.md`, logging bounded retries to `audit/logs/retry-CONSISTENCY_GATE.jsonl`, and appending transition events to `runtime/events.jsonl`.

```json
{
  "mission_id": "M-05-REVIEW",
  "role": "Reviewer",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/TRACEABILITY.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/audit/logs/retry-CONSISTENCY_GATE.jsonl",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/events.jsonl"
  ],
  "principles": [
    "Cross-check REQUIREMENTS.md, ARCHITECTURE.md, TODO.md, and git diff line by line for silent drift or unrequested edits.",
    "Verify structural AST invariants (no silent mock fallbacks, no unguarded TODO/stub markers) using ast-grep or AST parsers before sign-off.",
    "Never waive an unmapped requirement or failed gate without recording a retry-ledger entry."
  ],
  "max_tool_calls": 35,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "phase",
      "coverage_percent",
      "blocking_findings",
      "retry_logged"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "FAIL"]
      },
      "phase": {
        "type": "string",
        "enum": ["CONSISTENCY_GATE", "FINAL_AUDIT"]
      },
      "coverage_percent": {
        "type": "number",
        "minimum": 0,
        "maximum": 100
      },
      "blocking_findings": {
        "type": "array",
        "items": { "type": "string" }
      },
      "retry_logged": {
        "type": "boolean"
      }
    }
  }
}
```

### 6. Implementer (`M-06-IMPLEMENT`)

Executes scoped changes inside `<TARGET_SCOPE>/**` and checks off completed items with verbatim verification evidence in `TODO.md`. Never edits unrelated files, audit logs, or runtime state.

```json
{
  "mission_id": "M-06-IMPLEMENT",
  "role": "Implementer",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/<TARGET_SCOPE>/**",
    "<RUN_WORKSPACE>/docs/.scratch-audit/TODO.md"
  ],
  "principles": [
    "Modify only files inside assigned <TARGET_SCOPE>/** plus docs/.scratch-audit/TODO.md.",
    "No stubs, TODO/FIXME leftovers, silent exception swallowing, or hardcoded machine-specific paths.",
    "Run targeted checks after every objective and tick [x] in TODO.md only when outputs pass."
  ],
  "max_tool_calls": 80,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "objectives_completed",
      "files_modified",
      "checks_run"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "FAIL", "BLOCKED"]
      },
      "objectives_completed": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "pattern": "^OBJ-[0-9]{3}$" }
      },
      "files_modified": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "minLength": 1 }
      },
      "checks_run": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "minLength": 1 }
      }
    }
  }
}
```

### 7. Verifier (`M-07-VERIFY`)

Runs unit/integration/e2e/lint/typecheck suites with fresh post-edit runs, updates `CODEBASE-STATE.md` with observed counts/exit codes, logs failed verification cycles to `audit/logs/retry-VERIFY.jsonl`, and appends to `runtime/events.jsonl`.

```json
{
  "mission_id": "M-07-VERIFY",
  "role": "Verifier",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/CODEBASE-STATE.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/audit/logs/retry-VERIFY.jsonl",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/events.jsonl"
  ],
  "principles": [
    "Execute fresh tests, linters, typecheckers, and schema validators after the final edit; never report stale results.",
    "Never modify source code or relax test assertions to make a suite pass.",
    "Log every non-zero verification outcome to audit/logs/retry-VERIFY.jsonl and verify bounded retry budget <= 3."
  ],
  "max_tool_calls": 40,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "commands_executed",
      "failing_checks",
      "retry_attempt"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "FAIL"]
      },
      "commands_executed": {
        "type": "array",
        "minItems": 1,
        "items": { "type": "string", "minLength": 1 }
      },
      "failing_checks": {
        "type": "array",
        "items": { "type": "string" }
      },
      "retry_attempt": {
        "type": "integer",
        "minimum": 1,
        "maximum": 3
      }
    }
  }
}
```

### 8. Security Auditor (`M-08-AUDIT-SECURITY`)

Audits dependency CVEs, CWE/OWASP flaws, secret exposure, and CI/runtime permissions, classifying findings with **CVSS v4.0**, **EPSS**, **CISA KEV**, SBOM/provenance, and **SARIF 2.1.0** in `SECURITY.md` and `RISK.md`.

```json
{
  "mission_id": "M-08-AUDIT-SECURITY",
  "role": "Security Auditor",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/SECURITY.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/RISK.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/events.jsonl"
  ],
  "principles": [
    "Score vulnerabilities using CVSS v4.0 alongside EPSS probability and CISA KEV active-exploitation status.",
    "Verify least-privilege path boundaries, secret hygiene, and SARIF 2.1.0 / SBOM coverage where applicable.",
    "Any Critical finding or unmitigated CISA KEV hit forces BLOCKED until remediated or explicitly waived by the user."
  ],
  "max_tool_calls": 35,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "critical_findings",
      "high_findings",
      "kev_hits",
      "sarif_generated"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "WARN", "BLOCKED"]
      },
      "critical_findings": {
        "type": "integer",
        "minimum": 0
      },
      "high_findings": {
        "type": "integer",
        "minimum": 0
      },
      "kev_hits": {
        "type": "integer",
        "minimum": 0
      },
      "sarif_generated": {
        "type": "boolean"
      }
    }
  }
}
```

### 9. Final Auditor (`M-09-FINAL-AUDIT`)

Finalizes `TRACEABILITY.md`, closes `runtime/{manifest.json,state.json,events.jsonl}` (`READY` / `READY_WITH_WARNINGS` / `NOT_READY`), and hands off read-only audit records to `Debriefer`. Never edits `debrief.md`.

```json
{
  "mission_id": "M-09-FINAL-AUDIT",
  "role": "Final Auditor",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/TRACEABILITY.md",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/manifest.json",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/state.json",
    "<RUN_WORKSPACE>/docs/.scratch-audit/runtime/events.jsonl"
  ],
  "principles": [
    "Never mark READY unless all REQ-NNN rows are verified in TRACEABILITY.md and manifest/state/events schemas validate.",
    "Verify clean git worktree status and ensure scratch files were not left in source directories.",
    "Write only audit and runtime closing records; leave debrief.md strictly to Debriefer."
  ],
  "max_tool_calls": 30,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "release_verdict",
      "schemas_valid",
      "unverified_requirements"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "FAIL"]
      },
      "release_verdict": {
        "type": "string",
        "enum": ["READY", "READY_WITH_WARNINGS", "NOT_READY"]
      },
      "schemas_valid": {
        "type": "boolean"
      },
      "unverified_requirements": {
        "type": "array",
        "items": { "type": "string" }
      }
    }
  }
}
```

### 10. Debriefer (`M-10-DEBRIEF`)

Synthesizes the final executive summary, evidence links, OTel metrics (`trace_id`, `span_id`, `gen_ai.agent.name`), and rollback steps into `debrief.md`.

```json
{
  "mission_id": "M-10-DEBRIEF",
  "role": "Debriefer",
  "read_paths": [
    "<RUN_WORKSPACE>/**"
  ],
  "allowed_paths": [
    "<RUN_WORKSPACE>/docs/.scratch-audit/debrief.md"
  ],
  "principles": [
    "Report only file paths, symbols, diffs, and command outputs directly observed in audit and verification artifacts.",
    "Include exact OTel trace/span correlation IDs when runtime instrumentation was active, plus a concrete rollback command.",
    "Write strictly to docs/.scratch-audit/debrief.md without modifying code or runtime JSON files."
  ],
  "max_tool_calls": 20,
  "return_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "unevaluatedProperties": false,
    "required": [
      "status",
      "debrief_path",
      "release_verdict",
      "rollback_documented"
    ],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["PASS", "BLOCKED"]
      },
      "debrief_path": {
        "type": "string",
        "const": "<RUN_WORKSPACE>/docs/.scratch-audit/debrief.md"
      },
      "release_verdict": {
        "type": "string",
        "enum": ["READY", "READY_WITH_WARNINGS", "NOT_READY"]
      },
      "rollback_documented": {
        "type": "boolean"
      }
    }
  }
}
```

---

## Cross-Host Runtime Adapter

Because host runtimes differ in native sandboxing capabilities, the orchestrator translates each mission envelope uniformly:

| Host / Runtime | Native Enforcement | Orchestrator Fallback Check |
| --- | --- | --- |
| **Hermes / Native Agent Swarm** | Subagent tool scope (`delegate_task` / `swarm`) + shared board isolation | Reject any file diff outside `allowed_paths` via `git diff --name-only` before state transition |
| **OpenCode / Codex CLI** | Pass envelope JSON into subagent system prompt; optional isolated `git worktree` per `Implementer` | Validate returned JSON against `return_schema` and check `git status --short` against `allowed_paths` |
| **Gemini CLI / Antigravity / Copilot CLI / Cursor** | Inject `read_paths`, `allowed_paths`, `principles`, `max_tool_calls`, and `return_schema` verbatim in mission brief | Treat `allowed_paths` as a pre-transition gate; fail `FINAL_AUDIT` if out-of-scope paths were modified |
