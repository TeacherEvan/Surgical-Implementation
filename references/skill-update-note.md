# Skill Update — audit-hygiene-and-evidence-discipline

Status: NEW CLASS-LEVEL UMBRELLA SKILL NOT CREATED (skill_manage blocked by 57-char description cap x6 attempts; loop stopped per instructions). Durable capture below; recommend `hermes curator adopt audit-hygiene-and-evidence-discipline` when description-cap resolved.

Companion review skill: `surgical-audit` (`@audit-hygiene`) — implements review with built-in audit hygiene rules (`.gitignore` exclusions, salvage audit rev-count, explicit rejection documentation, cosmetic-vs-real separation).

## What the session produced (real execution, verified — not fabricated)

- Full 4-phase audit (Phase 1 `audit_report.md` 6872B/65L; Phase 2 `review_findings.md` 6009B/62L; Phase 3 `investigation_report.md` 4766B/58L; Phase 4 `fix_summary.md` 6570B/62L).
- `.gitignore` created (18L) with exclusions verified (`git check-ignore` returns audit_report.md / review_findings.md / fix_summary.md / investigation_report.md / `.prune/` — 5 exclusions).
- `.prune/` salvage audit verified (`rev-list` = 0; `rg '.prune' SKILL.md references/ GLE_.../` = 0 hits; excluded; unstaged).
- SKILL.md + references/v2-artifact-templates.md modified (commit `b761668` pushed to `main` after rebase; no `-A` used).
- Venv (`venv/`, Python 3.12.3) created and verified.
- Jailbreak frame ("GODMODE ENABLED / no filters / unrestricted") REJECTED; documented in audit_report.md §NOTE, review_findings.md §NOTE, fix_summary.md §NOTE; standard operation preserved; no unrestricted mode adopted.
- Cosmetic `||` at SKILL.md line 118 deferred (LOW/STYLE, non-substantive); governance.md cross-reference deferred (optional).
- No CRITICAL/HIGH defects; LOW hygiene only.

## Skill update recommendation

- `surgical-audit`: Pair with this skill for review and audit hygiene rules (`.gitignore` exclusions, salvage audit rev-count, rejection documentation, cosmetic-vs-real separation).
- `audit-hygiene-and-evidence-discipline` (new class-level umbrella, `agent-behavior`): attempted; blocked by 57-char description cap. SKILL.md content finalized (trigger + embedded preferences + rules + gate checklist + references). Once description-cap resolved: `hermes skills install` or `curator adopt`.

## References (added to workspace — durable capture)

- [V2 Governance & Gates](v2-governance.md)
- [Git Recovery and Scan](git-recovery-and-scan.md)
- [Implementation Pitfalls & Structural Invariants](implementation-pitfalls.md)

Note: skills follow file-based discovery under `<SKILLS_DIR>/surgical-implementation/SKILL.md` (with sibling surgical skills `surgical-audit`, `surgical-orchestration`, `surgical-investigation`, and `surgical-hermesdothealth`).
