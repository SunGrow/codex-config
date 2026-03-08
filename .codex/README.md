# Codex Home Config

This directory is the shareable source tree for the live `~/.codex` home configuration.

## What this repo contains

- `AGENTS.md`: global instruction policy loaded by Codex.
- `AGENTIC-WORKFLOW-INSTRUCTIONS.md`: generic multi-agent workflow and orchestration guidance.
- `RESEARCH-INSTRUCTIONS.md`: shared research and source-verification guidance.
- `UE-INSTRUCTIONS.md`: Unreal Engine workflow guidance referenced by `AGENTS.md`.
- `CODEX-CONFIG-INSTRUCTIONS.md`: Codex-config workflow and routing guidance referenced by `AGENTS.md`.
- `config.template.toml`: portable starter config (copy to `config.toml` locally).
- `skills/`: installed skills that can be invoked by name.
- `memories/`: curated durable learnings stored as versioned markdown.
- `docs/REFERENCES.md`: official docs and upstream references.
- `.github/workflows/gitleaks.yml`: automated secret scanning.

## Deployment

The publishing repo that owns this tree should deploy it into the live home folder with `scripts/sync-to-home.ps1`. Keep `config.toml`, auth files, caches, session history, and sqlite state in the live home folder only.

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

## Instruction model

1. Put cross-project rules in this repo's `AGENTS.md`.
2. Put project-specific rules in a project-local `AGENTS.md`.
3. For deep subtrees, use nested `AGENTS.override.md` for local overrides.
4. Use `project_doc_fallback_filenames` only when a project uses a non-standard instruction filename.
5. Keep instructions explicit:
   - state the environment and constraints;
   - call out required tools/skills by name;
   - define expected output and validation steps.
6. For Unreal work, keep UE-specific guidance in `UE-INSTRUCTIONS.md` and reference it from `AGENTS.md`.
7. For generic multi-agent coding work, keep orchestration guidance in `AGENTIC-WORKFLOW-INSTRUCTIONS.md`.
8. For research-heavy work, keep shared sourcing rules in `RESEARCH-INSTRUCTIONS.md`.
9. For Codex-config work, keep config-specific guidance in `CODEX-CONFIG-INSTRUCTIONS.md` and reference it from `AGENTS.md`.
10. Default to hierarchical dispatch for specialized/noisy tasks to protect parent context budget.
11. Use caller-mediated handoffs: `DECISION_REQUIRED`/`DECISION_RESULT` for choices, `PERMISSION_REQUIRED`/`PERMISSION_RESULT` for privileged tools.

## Standard Skills Layout

- Repo-scoped standard layout: `.agents/skills/<skill-name>/SKILL.md`.
- This repository is a global Codex home config, so skills live in `skills/` for this setup.
- Keep every skill folder minimal: `SKILL.md`, optional `agents/openai.yaml`, optional `scripts/`, `references/`, `assets/`.

## Getting Depth Plus Parallelism

1. Request decomposition first (subtasks + owners + outputs).
2. Require parallel execution for independent subtasks.
3. Require ownership partitioning for write-heavy subtasks.
4. Require one integration pass with validation and concise findings.

## Configuration model

- Keep portable defaults in `config.template.toml`.
- Keep machine-specific values in `config.toml` (ignored by git).
- Use top-level `web_search = "live" | "cached" | "disabled"`.
- Do not use deprecated `[tools].web_search`.
- Enable stable features by default in shared config.

## How to use skills

1. Skills live under `skills/<skill-name>/SKILL.md`.
2. Ask for a skill by name in your prompt (for example, `ue-build-fixer`).
3. Add custom skills by creating a new folder with a `SKILL.md` file.

## Portability notes

- Runtime/secrets/log files are ignored by `.gitignore`.
- Prefer env vars (`$CODEX_HOME`, `%USERPROFILE%`) instead of hard-coded user paths.

## Documentation references

See `docs/REFERENCES.md` for official Codex docs and upstream links.
