# codex-config Publishing Repo

This repository publishes the shareable part of the Codex home config.

## Edit Targets

- Edit `./.codex/` for shareable Codex configuration.
- Keep repo-only docs and deployment helpers in `./docs/` and `./scripts/`.
- Treat `$CODEX_HOME` as a deployed local copy, not the source of truth.

## Sync Rules

1. Make shareable changes in `./.codex/`.
2. Run `./scripts/sync-to-home.ps1 -PruneStale` after repo edits.
3. If live-only experimentation happened in `$CODEX_HOME`, import it intentionally with `./scripts/sync-from-home.ps1`.
4. Do not commit machine-local state such as `config.toml`, auth files, caches, sessions, sqlite files, or migration scratch folders.
