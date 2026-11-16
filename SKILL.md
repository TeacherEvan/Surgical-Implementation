---
name: surgical-implementation
description: "Use when planning or implementing verified code changes."
version: 1.1.0
author: "TeacherEvan, Fenrie (Lea's AI wolf), Hermes Agent"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: software-development
    tags:
      - implementation
      - engineering
      - planning
      - verification
      - debugging
      - refactoring
      - security-audit
      - traceability
    related_skills:
      - surgical-orchestration
      - surgical-audit
      - surgical-hermesdothealth
      - surgical-investigation
---

# Surgical Implementation

## Overview

End-to-end engineering execution framework running as a deterministic **15-state G&L V2 state machine** (`DISCOVER` → `HANDOFF`, bracketed by `INIT`, `COMPLETE`, and `STOP_AND_REQUEST_USER`). Combines upfront plan discovery, immutable requirement capture, subagent role isolation, architectural design, pre-code consistency checks, bounded verification retries, security/traceability auditing, and grounded debriefing.

---

## When to Use

- Implementing features, migrations, or multi-file refactors requiring structured design and traceability.
- Fixing bugs across backend/frontend/CI boundaries where post-edit regression risk is non-trivial.
- Resuming or completing partial plans inside a repository (`TODO.md`, `docs/plans/*.md`, objective checklists).
- Delivering verified, production-ready changes with evidence-backed sign-off rather than speculative edits.

## When Not to Use

- Pure read-only codebase research or comparative reports without code edits (use `surgical-investigation`).
- Standalone diff auditing with no implementation scope (use `surgical-audit`).
- Orchestrating autonomous multi-repo swarms across independent repositories (use `surgical-orchestration`).

---

## Auxiliary Resources

Load detailed contracts and runbooks on demand rather than preloading into primary context:

| Resource | Purpose |
| --- | --- |
| [Plan Scan Dispatcher](references/plan-scan-dispatcher.md) | Step 0 routing rules and `-g` plan-discovery scan |
| [V2 Governance & Gates](references/v2-governance.md) | State transitions, approval gates, bounded retries, 11-class taxonomy |
| [V2 Agent Envelopes](references/v2-agent-envelopes.md) | Least-privilege envelopes (`read_paths`, `allowed_paths`, JSON `return_schema`) for 10 roles |
| [V2 Artifact Templates](references/v2-artifact-templates.md) | Templates #1–#17 + `manifest.json`, `state.json`, `events.jsonl` contracts |
| [Implementation Pitfalls](references/implementation-pitfalls.md) | Dual-agent conflict, policy consolidation, Webpack/Blender/AST pitfalls |
| [Git Recovery and Scan](references/git-recovery-and-scan.md) | Multi-checkout disambiguation and safe recovery of untracked work |
| [Convex Array Index Match](references/convex-array-index-match.md) | Stable document-ID mutation rule vs positional array indices |
| [Places API Radius](references/places-api-radius.md) | Unit clamping and distance bounds for geolocation queries |
| [Browser Real Profile](references/browser-real-profile.md) | `chrome-devtools` MCP (`--executablePath /usr/bin/brave-browser`) + headless fallback |
| [Skill Update Note](references/skill-update-note.md) | Audit hygiene alignment notes (`surgical-audit`, `.gitignore`, salvage rules) |
| Schema: [Agent Envelope](schemas/agent-envelope.schema.json) | Draft 2020-12 JSON Schema enforcing least-privilege mission envelopes |
| Schema: [Retry Log](schemas/retry-log.schema.json) | Draft 2020-12 JSON Schema for `audit/logs/retry-*.jsonl` records |

---

## Procedure

### Step 0: Plan-Scan Dispatcher (MUST Run First)

> **MANDATORY VERBATIM RULE**: Never answer a user prompt to plan/audit/implement without first scanning the workspace for existing plan documents (`TODO.md`, `docs/plans/*.md`, `REQUIREMENTS.md`), summarizing any incomplete items found, and confirming scope or next action before overwriting prior plans.

Run targeted plan discovery with `-g` (quoting globs for non-POSIX shells; inspect root manifests within 3 levels first):

```bash
rg -l -g 'docs/**/*.md' -i 'todo|objective|tick|plan|WIP|\[x\]|\[ \]' .
```

See [Plan Scan Dispatcher](references/plan-scan-dispatcher.md) for exact routing when incomplete plans vs complete plans exist (escalate review to `surgical-audit` or multi-agent execution to `surgical-orchestration`).

### Steps 1–15: G&L V2 State Machine

Write all ephemeral V2 runtime, audit, and planning artifacts strictly inside `<RUN_WORKSPACE>/docs/.scratch-audit/` — **never** inside this skill directory or production source folders.

1. **`INIT` → `DISCOVER` (`Investigator`)**: Bootstrap `docs/.scratch-audit/runtime/{manifest.json,state.json,events.jsonl}` and `CODEBASE-STATE.md`. Inspect git worktrees, runtime versions, test commands, **dual-agent workspace contention** (`ps aux | grep -E 'opencode|antigravity|agy'`), and **orphaned dev/test servers** (`lsof` / `ps aux | grep serve_dist`) before editing.
2. **Requirements (`REQUIREMENTS`, `Investigator`)**: Lock numbered user constraints (`REQ-NNN`) and out-of-scope rules in `docs/.scratch-audit/REQUIREMENTS.md`. Ambiguous requirements trigger `STOP_AND_REQUEST_USER`.
3. **External Research (`RESEARCH`, `Researcher`)**: Verify third-party APIs, CVEs, and SDK changes (freshness **<= 14 days**) into `research/{SOURCES,FINDINGS,DECISIONS}.md`.
4. **Codebase Baseline (`CODEBASE_STATE`, `Investigator`)**: Finalize current architecture, dependency versions, build/test baselines, and open debt in `CODEBASE-STATE.md`.
5. **Architecture (`ARCHITECT`, `Architect`)**: Define module boundaries, pure shared policy modules, failure modes, and accessible Mermaid diagrams (`accTitle:`/`accDescr:`) in `ARCHITECTURE.md`.
6. **Planning (`PLAN`, `Planner`)**: Break down dependency-ordered `OBJ-NNN` steps in `TODO.md`, assigning each an explicit `<TARGET_SCOPE>`, prerequisite list, and executable verification command.
7. **Pre-Code Consistency Gate (`CONSISTENCY_GATE`, `Reviewer`)**: Cross-check `REQUIREMENTS.md`, `CODEBASE-STATE.md`, `ARCHITECTURE.md`, and `TODO.md` into `TRACEABILITY.md` (`max_consistency_retries: 5`; log retries to `audit/logs/retry-CONSISTENCY_GATE.jsonl`). Obtain plan approval (`APPROVAL_REQUIRED`) on high-risk scope before `IMPLEMENT`.
8. **Scoped Implementation (`IMPLEMENT`, `Implementer`)**: Edit strictly inside `<TARGET_SCOPE>/**` + `TODO.md`. No stubs, bare `except` fallbacks, or hardcoded machine paths. Tick `[x]` in `TODO.md` only after item checks pass.
9. **Verification & Bounded Retries (`VERIFY`, `Verifier`)**: Run unit, integration, linter, typechecker, and `ast-grep` / static checks (`<= 3` cycles per `verification_attempts`, logging failures with the 11-class failure taxonomy to `audit/logs/retry-VERIFY.jsonl`). Exceeding 3 cycles triggers `STOP_AND_REQUEST_USER`.
10. **Security Audit (`SECURITY_AUDIT`, `Security Auditor`)**: Score findings with **CVSS v4.0 + EPSS + CISA KEV**, SBOM/secret checks, and **SARIF 2.1.0** in `SECURITY.md` + `RISK.md`. Critical or unmitigated KEV findings force `BLOCKED`.
11. **Final Audit (`FINAL_AUDIT`, `Final Auditor` + `Reviewer`)**: Cross-check git diff, test evidence, and requirements in `TRACEABILITY.md`, and close `runtime/{manifest.json,state.json,events.jsonl}` with `READY`, `READY_WITH_WARNINGS`, `NOT_READY`, or `BLOCKED`.
12. **Debrief & Handoff (`DEBRIEF` → `HANDOFF` → `COMPLETE`, `Debriefer`)**: Write grounded summary, observed verification counts, OTel `trace_id`/`span_id` references, and rollback steps to `docs/.scratch-audit/debrief.md`.

| State Group | Owning Role(s) | Primary Outputs (`docs/.scratch-audit/`) | Gate Mode |
| --- | --- | --- | --- |
| `INIT`, `DISCOVER`, `REQUIREMENTS`, `CODEBASE_STATE` | `Investigator` | `REQUIREMENTS.md`, `CODEBASE-STATE.md`, `runtime/*` | `AUTO` / `STOP_AND_REQUEST_USER` |
| `RESEARCH`, `ARCHITECT`, `PLAN` | `Researcher`, `Architect`, `Planner` | `research/*`, `ARCHITECTURE.md`, `TODO.md` | `REVIEW` |
| `CONSISTENCY_GATE` | `Reviewer` | `TRACEABILITY.md`, `audit/logs/retry-CONSISTENCY_GATE.jsonl` | `APPROVAL_REQUIRED` |
| `IMPLEMENT` | `Implementer` | `<TARGET_SCOPE>/**`, `TODO.md` | `AUTO` |
| `VERIFY` | `Verifier` | `CODEBASE-STATE.md`, `audit/logs/retry-VERIFY.jsonl` | `AUTO` |
| `SECURITY_AUDIT`, `FINAL_AUDIT`, `COMPLETE` | `Security Auditor`, `Final Auditor`, `Reviewer` | `SECURITY.md`, `RISK.md`, `TRACEABILITY.md`, `runtime/*` | `BLOCKED` or `READY*` |
| `DEBRIEF`, `HANDOFF` | `Debriefer` | `debrief.md` | `AUTO` |

---

## Artifact Destination & Governance

- All `docs/.scratch-audit/` files belong to the target run workspace (and stay `.gitignore`d unless explicitly requested). Keep production trees clean of temporary scratch files.
- Every subagent mission receives a least-privilege JSON envelope conforming to [agent-envelope.schema.json](schemas/agent-envelope.schema.json) — `allowed_paths` must never contain `"<RUN_WORKSPACE>/**"`.
- All runtime JSON (`manifest.json`, `state.json`, `events.jsonl`) and retry JSONL records must validate against the Draft 2020-12 schemas before marking `COMPLETE`.

---

## Verification

Before reporting completion to the user:

1. Re-run the full relevant test, lint, typecheck, and schema suites **after the final edit**; report only directly observed counts, exit codes, and paths.
2. Verify modified artifacts are saved/committed where requested (never run `git push` unless explicitly instructed) and read back live outputs/files to confirm what landed.
3. Confirm no temporary files or unrequested edits remain outside `<TARGET_SCOPE>` and `docs/.scratch-audit/`.

---

## Related Skills

`surgical-orchestration` · `surgical-audit` · `surgical-hermesdothealth` · `surgical-investigation`

## Author

TeacherEvan, Fenrie (Lea's AI wolf), Hermes Agent

## License

MIT
