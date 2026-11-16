"""Tests for surgical-implementation schemas, envelopes, conformance, and mirrors."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCHEMA_DIR = ROOT / "GLE_Software_Engineering_Auditor_V2_ULTIMATE" / "runtime"
SCHEMAS_DIR = ROOT / "schemas"
REFERENCES_DIR = ROOT / "references"


def _extract_section(markdown: str, heading_pattern: str) -> str:
    """Return body of matching markdown H2/H3 section up to the next sibling heading."""
    match = re.search(heading_pattern, markdown, flags=re.MULTILINE)
    assert match is not None, f"Heading matching {heading_pattern!r} not found"
    start = match.end()
    level = match.group(0).lstrip().split(" ", 1)[0]
    next_heading = re.search(
        rf"^{re.escape(level)}\s+", markdown[start:], flags=re.MULTILINE
    )
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end]


def _extract_fenced_blocks(text: str, lang: str) -> list[str]:
    """Return contents of fenced code blocks matching a language tag."""
    pattern = rf"```{re.escape(lang)}\n(.*?)\n```"
    return re.findall(pattern, text, flags=re.DOTALL)


def _load_schema(path: Path) -> dict[str, Any]:
    """Load a JSON Schema file and validate it against Draft 2020-12."""
    schema: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return schema


def _validate_instance(instance: Any, schema: dict[str, Any]) -> None:
    """Validate an instance with Draft 2020-12 validator."""
    validator = jsonschema.Draft202012Validator(schema)
    validator.validate(instance)


def test_runtime_templates_12_to_14_match_schemas() -> None:
    """Templates #12-#14 in v2-artifact-templates.md must validate cleanly."""
    templates_md = (REFERENCES_DIR / "v2-artifact-templates.md").read_text(
        encoding="utf-8"
    )

    manifest_sec = _extract_section(templates_md, r"^## 12\. runtime/manifest\.json$")
    manifest_blocks = _extract_fenced_blocks(manifest_sec, "json")
    assert len(manifest_blocks) == 1
    manifest_obj: dict[str, Any] = json.loads(manifest_blocks[0])
    manifest_schema = _load_schema(RUNTIME_SCHEMA_DIR / "manifest.schema.json")
    _validate_instance(manifest_obj, manifest_schema)

    example_obj: dict[str, Any] = json.loads(
        (RUNTIME_SCHEMA_DIR / "manifest.example.json").read_text(encoding="utf-8")
    )
    _validate_instance(example_obj, manifest_schema)

    # Negative mutant: unevaluatedProperties: false rejects unknown fields
    bad_manifest = copy.deepcopy(manifest_obj)
    bad_manifest["unexpected_field"] = True
    with pytest.raises(jsonschema.ValidationError):
        _validate_instance(bad_manifest, manifest_schema)

    state_sec = _extract_section(templates_md, r"^## 13\. runtime/state\.json$")
    state_blocks = _extract_fenced_blocks(state_sec, "json")
    assert len(state_blocks) == 1
    state_obj: dict[str, Any] = json.loads(state_blocks[0])
    state_schema = _load_schema(RUNTIME_SCHEMA_DIR / "state.schema.json")
    _validate_instance(state_obj, state_schema)

    with pytest.raises(jsonschema.ValidationError):
        _validate_instance({"state": "UNKNOWN_BOGUS_STATE"}, state_schema)

    events_sec = _extract_section(templates_md, r"^## 14\. runtime/events\.jsonl$")
    events_blocks = _extract_fenced_blocks(events_sec, "jsonl")
    assert len(events_blocks) == 1
    events_schema = _load_schema(RUNTIME_SCHEMA_DIR / "events.schema.json")
    lines = [ln for ln in events_blocks[0].splitlines() if ln.strip()]
    assert len(lines) >= 2
    for line in lines:
        event_obj = json.loads(line)
        _validate_instance(event_obj, events_schema)

    bad_event = json.loads(lines[0])
    bad_event["state"] = "NOT_A_VALID_STATE"
    with pytest.raises(jsonschema.ValidationError):
        _validate_instance(bad_event, events_schema)


def test_retry_log_example_matches_schema() -> None:
    """Retry ledger example in v2-governance.md must match retry-log.schema.json."""
    gov_md = (REFERENCES_DIR / "v2-governance.md").read_text(encoding="utf-8")
    retry_sec = _extract_section(gov_md, r"^## 2\. Bounded-Retry Ledger")
    blocks = _extract_fenced_blocks(retry_sec, "json")
    assert len(blocks) >= 1
    retry_obj: dict[str, Any] = json.loads(blocks[0])
    retry_schema = _load_schema(SCHEMAS_DIR / "retry-log.schema.json")
    _validate_instance(retry_obj, retry_schema)

    bad_retry = copy.deepcopy(retry_obj)
    del bad_retry["corrective_action"]
    with pytest.raises(jsonschema.ValidationError):
        _validate_instance(bad_retry, retry_schema)


def test_agent_envelopes_least_privilege_and_schema() -> None:
    """All 10 envelopes must satisfy agent-envelope.schema.json and least privilege."""
    envelopes_md = (REFERENCES_DIR / "v2-agent-envelopes.md").read_text(
        encoding="utf-8"
    )
    assert "principals" not in envelopes_md.lower(), (
        "Spelling error 'principals' present"
    )
    assert not re.search(r"\|\s*`Researcher`\s*\|[^|\n]*\|\s*NO\s*\|", envelopes_md), (
        "Researcher Read Repo contradiction (NO instead of YES)"
    )

    envelope_schema = _load_schema(SCHEMAS_DIR / "agent-envelope.schema.json")
    blocks = _extract_fenced_blocks(envelopes_md, "json")
    assert len(blocks) == 10, f"Expected 10 agent envelopes, found {len(blocks)}"

    by_role: dict[str, dict[str, Any]] = {}
    for raw in blocks:
        env: dict[str, Any] = json.loads(raw)
        _validate_instance(env, envelope_schema)
        jsonschema.Draft202012Validator.check_schema(env["return_schema"])
        assert "<RUN_WORKSPACE>/**" not in env["allowed_paths"]
        assert "<RUN_WORKSPACE>/*" not in env["allowed_paths"]
        by_role[env["role"]] = env

    expected_roles = {
        "Investigator",
        "Researcher",
        "Architect",
        "Planner",
        "Reviewer",
        "Implementer",
        "Verifier",
        "Security Auditor",
        "Final Auditor",
        "Debriefer",
    }
    assert set(by_role) == expected_roles

    # Role boundary invariants
    assert any(
        p.endswith("/REQUIREMENTS.md") for p in by_role["Investigator"]["allowed_paths"]
    )
    assert any(
        p.endswith("/runtime/manifest.json")
        for p in by_role["Investigator"]["allowed_paths"]
    )
    assert any(p.endswith("/debrief.md") for p in by_role["Debriefer"]["allowed_paths"])
    assert not any(
        p.endswith("/debrief.md") for p in by_role["Final Auditor"]["allowed_paths"]
    ), "Final Auditor must not collide with Debriefer on debrief.md"
    assert (
        "<RUN_WORKSPACE>/<TARGET_SCOPE>/**" in by_role["Implementer"]["allowed_paths"]
    )
    for ro_role in (
        "Researcher",
        "Architect",
        "Planner",
        "Reviewer",
        "Verifier",
        "Debriefer",
    ):
        assert (
            "<RUN_WORKSPACE>/<TARGET_SCOPE>/**" not in by_role[ro_role]["allowed_paths"]
        )

    # Negative mutant: wildcard write scope must fail schema validation
    wildcard_env = copy.deepcopy(by_role["Planner"])
    wildcard_env["allowed_paths"] = ["<RUN_WORKSPACE>/**"]
    with pytest.raises(jsonschema.ValidationError):
        _validate_instance(wildcard_env, envelope_schema)


def test_skill_markdown_hygiene_paths_and_links() -> None:
    """SKILL.md and active references/docs stay <=250 lines, clean, and link-valid."""
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    lines = skill_text.splitlines()
    assert len(lines) <= 250, f"SKILL.md is {len(lines)} lines (> 250)"

    # Runtime workspace path unification
    assert "docs/.scratch-audit/" in skill_text
    assert ".agent-audit/" not in skill_text
    assert "--glob 'docs/**/*.md'" not in skill_text
    assert "-g 'docs/**/*.md'" in skill_text

    # No personal paths or legacy unportable refs across active docs/references
    check_files: list[Path] = [
        ROOT / "SKILL.md",
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        *sorted(REFERENCES_DIR.glob("*.md")),
        *sorted((ROOT / "docs" / "plans").glob("*.md")),
    ]
    forbidden_patterns = (
        "/home/",
        "/Users/",
        "Devil-sDelight",
        "code-review",
        "verify-before-planning-gaps",
        "~/.hermes/profiles/",
        "skill_view(",
    )
    for file_path in check_files:
        text = file_path.read_text(encoding="utf-8")
        for pat in forbidden_patterns:
            assert pat not in text, f"Forbidden string {pat!r} found in {file_path}"

    # Verify every markdown relative link in SKILL.md resolves cleanly
    for target in re.findall(r"\]\((references/[^)#]+|schemas/[^)#]+)\)", skill_text):
        assert (ROOT / target).is_file(), f"Dead link in SKILL.md: {target}"

    # Ensure every file in references/ is indexed by SKILL.md
    for ref_file in sorted(REFERENCES_DIR.glob("*.md")):
        rel = f"references/{ref_file.name}"
        assert rel in skill_text, f"{rel} missing from SKILL.md Auxiliary Resources"


def test_conform_and_validate_package_pass() -> None:
    """Both conform.py and validate-package.py must pass cleanly."""
    conform_res = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "conform.py"), str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert conform_res.returncode == 0, conform_res.stdout + conform_res.stderr
    assert "PASS  Surgical-Implementation" in conform_res.stdout

    pkg_script = (
        ROOT
        / "GLE_Software_Engineering_Auditor_V2_ULTIMATE"
        / "scripts"
        / "validate-package.py"
    )
    pkg_res = subprocess.run(
        [sys.executable, "-B", str(pkg_script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert pkg_res.returncode == 0, pkg_res.stdout + pkg_res.stderr
    assert "Package validation: PASS" in pkg_res.stdout


def test_sync_skill_hermetic_mirror_prune_and_verify(tmp_path: Path) -> None:
    """sync-skill.sh must exclude docs/scripts/GLE_*, prune stale assets, and verify."""
    if shutil.which("rsync") is None:
        pytest.skip("rsync not installed")

    repo = tmp_path / "repo"
    repo.mkdir()
    for fname in ("SKILL.md", "README.md", "LICENSE", "AGENTS.md"):
        shutil.copy2(ROOT / fname, repo / fname)
    for folder in ("references", "schemas"):
        shutil.copytree(ROOT / folder, repo / folder)
    (repo / "scripts").mkdir()
    shutil.copy2(ROOT / "scripts" / "sync-skill.sh", repo / "scripts" / "sync-skill.sh")
    shutil.copy2(ROOT / "scripts" / "conform.py", repo / "scripts" / "conform.py")
    (repo / "docs" / "plans").mkdir(parents=True)
    (repo / "docs" / "plans" / "stale.md").write_text(
        "repo-only doc\n", encoding="utf-8"
    )
    (repo / "GLE_Software_Engineering_Auditor_V2_ULTIMATE").mkdir()
    (repo / "GLE_Software_Engineering_Auditor_V2_ULTIMATE" / "README.txt").write_text(
        "repo-only package\n", encoding="utf-8"
    )

    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "ci@example.com"], cwd=repo, check=True
    )
    subprocess.run(["git", "config", "user.name", "CI"], cwd=repo, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True
    )

    fake_home = tmp_path / "home"
    target_rel = ".hermes/skills/software-development/surgical-implementation"
    install_dir = fake_home / target_rel
    install_dir.mkdir(parents=True)
    # Seed legacy stale files + preserved _archive artifact
    (install_dir / "Readme.md").write_text("legacy mixed case\n", encoding="utf-8")
    (install_dir / "docs").mkdir()
    (install_dir / "docs" / "drift.md").write_text("stale drift\n", encoding="utf-8")
    (install_dir / "scripts").mkdir()
    (install_dir / "scripts" / "conform.py").write_text("# stale\n", encoding="utf-8")
    (install_dir / "_archive").mkdir()
    (install_dir / "_archive" / "keep.txt").write_text("preserved\n", encoding="utf-8")

    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    env["SKILL_TARGETS"] = target_rel

    sync_script = str(repo / "scripts" / "sync-skill.sh")
    pre_check = subprocess.run(
        ["bash", sync_script, "check"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert pre_check.returncode == 1

    sync_res = subprocess.run(
        ["bash", sync_script, "sync"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert sync_res.returncode == 0, sync_res.stdout + sync_res.stderr

    verify_res = subprocess.run(
        ["bash", sync_script, "verify"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert verify_res.returncode == 0, verify_res.stdout + verify_res.stderr

    # Pruned stale assets & preserved _archive
    assert not (install_dir / "Readme.md").exists()
    assert not (install_dir / "docs").exists()
    assert not (install_dir / "scripts").exists()
    assert not (install_dir / "GLE_Software_Engineering_Auditor_V2_ULTIMATE").exists()
    assert (install_dir / "_archive" / "keep.txt").read_text(
        encoding="utf-8"
    ) == "preserved\n"
    assert (install_dir / "README.md").is_file()
    assert (install_dir / "schemas" / "agent-envelope.schema.json").is_file()
