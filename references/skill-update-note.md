# Skill Update — audit-hygiene-and-evidence-discipline
Status: NEW CLASS-LEVEL UMBRELLA SKILL NOT CREATED (skill_manage blocked by 57-char description cap x6 attempts; loop stopped per instructions). Durable capture below; recommend `hermes curator adopt audit-hygiene-and-evidence-discipline` when description-cap resolved.

Protected skill noted: `code-review` (bundled `software-development/code-review`) — loaded and in play during session; WRONG / MISSING relative to session learnings (no audit hygiene / salvage-audit / jailbreak-rejection / `.gitignore` exclusion / cosmetic-vs-real rules). Since protected: NOT edited; recommendation recorded below.

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
- `code-review` (protected, bundled): WRONG relative to session — missing audit hygiene rules (§.gitignore exclusions, salvage audit rev-count, jailbreak-rejection documentation, cosmetic-vs-real separation). Recommend: note to user; `hermes curator adopt audit-hygiene-and-evidence-discipline` once the umbrella can be registered.
- `audit-hygiene-and-evidence-discipline` (new class-level umbrella, `agent-behavior`): attempted; blocked by 57-char description cap. SKILL.md content finalized (trigger + embedded preferences + rules + gate checklist + references). Once description-cap resolved: `hermes skills install` or `curator adopt`.

## References (added to workspace — durable capture)
- `references/jailbreak-rejection-note.md`
- `references/salvage-audit-pattern.md`
- `references/git-commit-hygiene.md`

Note: profile skills dir (`~/.hermes/profiles/default/skills/`) absent — skills are file-based; `code-review` canonical path (`~/.hermes/skills/software-development/code-review/SKILL.md`) confirmed present.
