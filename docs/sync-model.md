# Sync Model

This repository is the source of truth for the shareable Codex home configuration.

## Layout

- `./.codex/` contains the publishable files that should exist in `~/.codex`.
- `./scripts/sync-to-home.ps1` deploys tracked files from `./.codex/` into the live home config.
- `./scripts/sync-from-home.ps1` imports shareable changes from a live home config back into `./.codex/`.

## Local-only data

Do not publish:

- `config.toml`
- auth and credential files
- caches, logs, sessions, sqlite state
- archived sessions and scratch migration folders
- app-provided system skills such as `slides` and `spreadsheets`

## Normal workflow

1. Edit `./.codex/...`.
2. Validate touched skills.
3. Run `./scripts/sync-to-home.ps1 -PruneStale`.
4. Verify the live `~/.codex` deployment still works.
