# Codex Portable Config

This repository packages shareable Codex configuration and instruction files so a team can run a consistent setup on different machines.

## What this repo contains

- `AGENTS.md`: global instruction policy loaded by Codex.
- `UE-INSTRUCTIONS.md`: Unreal Engine workflow guidance referenced by `AGENTS.md`.
- `MIGRATED_CLAUDE_INDEX.md`: map of migrated Claude assets/skills.
- `config.template.toml`: portable starter config (copy to `config.toml` locally).
- `skills/`: installed skills that can be invoked by name.
- `docs/REFERENCES.md`: official docs and local documentation pointers.

## Quick setup

1. Clone this repo into your Codex home folder.
2. Create your local config from the template.
3. Customize local-only values (trusted project paths, notify command, shell path).

Windows (PowerShell):

```powershell
git clone <your-repo-url> $env:USERPROFILE\.codex
Set-Location $env:USERPROFILE\.codex
Copy-Item config.template.toml config.toml
```

macOS/Linux:

```bash
git clone <your-repo-url> ~/.codex
cd ~/.codex
cp config.template.toml config.toml
```

## How to instruct Codex with these configs

1. Put cross-project rules in `AGENTS.md`.
2. Put project-specific rules in a project-local `CLAUDE.md` (or `.claude/CLAUDE.md`).
3. Keep instructions explicit:
   - state the environment and constraints;
   - call out required tools/skills by name;
   - define expected output and validation steps.
4. For Unreal work, keep UE-specific guidance in `UE-INSTRUCTIONS.md` and reference it from `AGENTS.md`.

## How to use skills

1. Skills live under `skills/<skill-name>/SKILL.md`.
2. Ask for a skill by name in your prompt (for example, `ue-build-fixer`).
3. Add custom skills by creating a new folder with a `SKILL.md` file.

## Portability notes

- `config.toml` is intentionally ignored because it is machine-specific.
- Runtime/secrets/log files are ignored by `.gitignore`.
- Prefer env vars (`$CODEX_HOME`, `%USERPROFILE%`) instead of hard-coded user paths.

## Documentation references

See `docs/REFERENCES.md` for official Codex docs and local reference files included in this repo.
