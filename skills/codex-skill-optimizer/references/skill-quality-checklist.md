# Codex Skill Quality Checklist

Use this checklist for manual improvements after running the audit script.

## Trigger Quality

- `description` states both what the skill does and when to use it.
- `description` mentions concrete triggers (file types, task verbs, scenarios).
- `description` avoids filler and avoids project-specific assumptions unless required.
- `agents/openai.yaml` has a concise `short_description` (25-64 chars).
- `agents/openai.yaml` includes `display_name` and `default_prompt`.
- `default_prompt` references the skill token (for example `$skill-name`).

## Context Efficiency

- `SKILL.md` body stays lean; move bulky detail into `references/`.
- Prefer deterministic scripts for repetitive or fragile operations.
- Remove verbose preambles that do not change behavior.
- Keep one clear workflow; avoid duplicated instructions.

## Modern Codex Conventions

- Use `AGENTS.md` references, not legacy `CLAUDE.md`.
- Avoid hardcoded local user paths; prefer `$CODEX_HOME` or relative paths.
- Avoid stale migration wording or provider-specific legacy labels.
- Keep naming neutral and reusable across projects.

## Workflow Rigor

- Steps are ordered and actionable.
- Safety boundaries are explicit (what can be auto-fixed vs manual only).
- Output expectations are explicit (severity, file paths, actionable plan).
- Validation commands are included and runnable.

## Progressive Disclosure

- Core workflow in `SKILL.md`.
- Detailed rule tables/examples in `references/`.
- Deterministic operations in `scripts/`.
- Avoid deeply nested references; link directly from `SKILL.md`.

## Review Before Commit

- Run audit without fixes and review findings.
- Run audit with `--apply` only when safe.
- Re-run audit and ensure severity targets are met.
- Run skill validator:
  `python skills/.system/skill-creator/scripts/quick_validate.py <skill-folder>`
