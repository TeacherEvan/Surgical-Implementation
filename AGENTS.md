# AGENTS.md — Surgical-Implementation

Guidance for AI coding agents working inside the `Surgical-Implementation` repository or loading the `surgical-implementation` skill.

## Scope & Boundaries

- This repository owns the **`surgical-implementation`** skill (`SKILL.md`, `references/`, `schemas/`) plus repository-only validation, CI, and bundled reference package (`GLE_Software_Engineering_Auditor_V2_ULTIMATE/`, `docs/`, `tests/`, `scripts/`, `.github/`).
- Never modify sibling repositories (`Surgical-Pruning/`, `Surgical-Investigation/`, etc.) unless explicitly assigned.
- Never run `git push` unless explicitly asked by the user.

## Runtime & Workspace Contract

- All ephemeral V2 planning, audit, and runtime state belongs inside `<RUN_WORKSPACE>/docs/.scratch-audit/`, **never** inside this skill directory.
- Do not grant `<RUN_WORKSPACE>/**` inside any role's `allowed_paths` in [`references/v2-agent-envelopes.md`](references/v2-agent-envelopes.md); keep `read_paths` and write-only `allowed_paths` strictly separated.
- Keep `SKILL.md` <= 250 lines with portable bare `related_skills` IDs (`^[a-z0-9-]+$`) and valid local references.

## Commands & Validation Gates

Run checks cleanly without polluting the checkout with cache directories (`python3 -B`, `--no-cache`, `/tmp` cache dirs):

- Skill conformance gate: `python3 -B scripts/conform.py`
- Bundled V2 package validator: `python3 -B GLE_Software_Engineering_Auditor_V2_ULTIMATE/scripts/validate-package.py`
- Schema validation: `check-jsonschema --check-metaschema schemas/*.schema.json GLE_Software_Engineering_Auditor_V2_ULTIMATE/runtime/*.schema.json`
- Test suite: `pytest -o cache_dir=/tmp/pytest-impl -v tests/`
- Lint & format: `ruff check --no-cache . && ruff format --check --no-cache .`
- Strict typing: `mypy --strict --cache-dir /tmp/mypy-impl scripts/ GLE_Software_Engineering_Auditor_V2_ULTIMATE/scripts/ tests/`
- Shell & workflow lint: `shellcheck -x scripts/sync-skill.sh && yamllint .github/workflows/skill-ci.yml`
- Mirror verification: `bash scripts/sync-skill.sh verify`
