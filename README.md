# codex-config

This repository publishes the shareable part of your Codex home configuration.

## Layout

- `./.codex/` is the source-of-truth tree for files that belong in `$CODEX_HOME` (typically `~/.codex`).
- `./scripts/sync-to-home.ps1` deploys tracked files from `./.codex/` into the live home config.
- `./scripts/sync-from-home.ps1` imports shareable changes from the live home config back into `./.codex/`.
- `./docs/sync-model.md` documents the repo/deploy boundary.
- `./.github/workflows/gitleaks.yml` keeps secret scanning on the publishing repo.

## Working model

1. Edit shareable files under `./.codex/`.
2. Keep machine-local state in the real home folder only:
   - `config.toml`
   - auth files
   - caches, logs, sessions
   - sqlite state
   - scratch migration imports
3. Run `./scripts/sync-to-home.ps1 -PruneStale` after changes.
4. Validate touched skills before committing.

## First-time setup

```powershell
Set-Location C:\Users\LazyF\Documents\Development\codex-tools\codex-config
.\scripts\sync-to-home.ps1 -PruneStale
if (-not (Test-Path C:\Users\LazyF\.codex\config.toml)) {
    Copy-Item .\.codex\config.template.toml C:\Users\LazyF\.codex\config.toml
}
```

## Validation

Validate touched skills:

```powershell
python .\.codex\skills\.system\skill-creator\scripts\quick_validate.py <skill-path>
```

Audit the full shared skill tree:

```powershell
python .\.codex\skills\codex-skill-optimizer\scripts\audit_codex_skills.py --root .\.codex\skills
```
