# Implementation Pitfalls & Structural Invariants

Consolidated field-tested engineering pitfalls, AST invariants, and host/environment gotchas encountered across complex implementation runs.

---

## 1. Concurrency & Workspace Hygiene

- **Dual-agent workspace conflict**: When multiple agents or editor instances target the same repo, `git` lockfiles (`index.lock`) or untracked temp edits collide silently. Check active agent processes during `DISCOVER` (`ps aux | grep -E 'opencode|antigravity|agy'`), verify git status/branches, and never kill or overwrite another active agent's checkout without explicit user coordination.
- **Orphaned dev/preview servers**: Long-running servers left on test ports cause Playwright, curl checks, or E2E runs to hit stale code. Inspect listening ports and stray server processes (`lsof -i :<port>` or `ss -ltnp`, `ps aux | grep serve_dist`) before launching verification suites.
- **Git checkout confusion & untracked files**: Two local clones of the same project cause edits in the wrong tree or lost commits. Follow [Git Recovery and Scan](git-recovery-and-scan.md) (`git remote -v`, `git status -sb`, `git worktree list`) before modifying code.

---

## 2. Architecture, Scope & Policy Integrity

- **A tunable rule belongs in one pure policy module**: Never scatter magic numbers, feature thresholds, rate limits, or allowlists across React components, route handlers, and background workers. Extract one pure, unit-tested policy module and import it everywhere so tweaks happen in one place.
- **Single-source contract alignment**: Schema enums, template examples, and state tables drift easily when edited separately. Validate all structured docs against Draft 2020-12 JSON Schemas (`check-jsonschema` / `pytest`) as part of verification.
- **Silent mock/stub fallbacks & placeholder leaks**: Never hide unimplemented paths behind dummy objects, bare `except Exception: pass`, `TODO` / `FIXME` stubs, or mock returns in production code. Use `ast-grep` (e.g., `sg -p 'except Exception: pass' -l python`) or static linters to catch silent fallbacks before `FINAL_AUDIT`.
- **Plan-scan & shell flag precision**: `rg` expects `-g` (not `--glob` in compact rules unless consistently supported), and quoted glob patterns prevent shell expansion bugs; see [Plan Scan Dispatcher](plan-scan-dispatcher.md).
- **Non-POSIX shell & environment quoting**: Fish shells, active Conda environments, and Windows/WSL bridges alter PATH and globbing (`$status` vs `$?`, unquoted `$()`). Prefer explicit interpreter invocations (`python3 -B`, `bash -lc`) and quote variable expansions (`"$var"`).

---

## 3. Domain, Build & Asset Pipelines

- **Convex array index vs identity matching**: Positional index matching corrupts mutations when clients filter or reorder lists. Always key updates by stable document ID; see [Convex Array Index Match](convex-array-index-match.md).
- **External API radius/unit assumptions**: Geolocation and map providers mix meters vs kilometers (`50000` m max radius in Places API) and clamp inputs silently. Check boundaries explicitly; see [Places API Radius](places-api-radius.md).
- **Webpack bundle budget vs Three.js / heavy 3D assets**: Default asset size hints (`244 KiB`) fail CI or silently bloat builds when bundling `three` and WebGL chunks. Configure tree-shaken ES imports (`three/examples/jsm/...`), split async dynamic `import()` chunks for scenes/loaders, and tune `performance.hints` / chunk budgets consciously.
- **Blender headless pipeline for game assets**: Never assume a GUI display server exists during asset export. Run `blender --background <scene.blend> --python <export_script.py>`, pin output format (`.glb`/`.gltf`), normalize scale/axis orientation (`+Y` up), and verify exported file presence and vertex/material counts from CLI.

---

## 4. Browser, Verification & Definition of Done

- **Real-profile Chromium & DevTools inspection**: Headless inspection should prefer `chrome-devtools` MCP (`--executablePath /usr/bin/brave-browser`) when inspecting real browser profiles, cookies, or DOM/network traces, falling back cleanly when no GUI profile exists; see [Browser Real Profile](browser-real-profile.md).
- **"Done" means committed and, when it ships, deployed and read back**: Passing local unit tests does not finish a deployable change. When the task involves shipping, commit clean changes (never `git push` unless explicitly requested), verify the deployed/installed target (or synced skill mirror), and read back the live endpoint/file from disk/HTTP to confirm what actually landed.
- **Post-edit test integrity & fresh runs**: Always re-run full verification (`pytest`, `ruff`, `mypy`, builds) after the *final* edit; never relax or skip assertions to force green builds, and never rely on pre-edit test outputs.
