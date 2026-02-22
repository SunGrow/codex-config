# Codex Configuration - Global Instructions

## Scope

Apply this context only to Codex configuration repositories.

Treat work as Codex-config scoped when at least two markers are present:
- `config.toml` or `config.template.toml`
- `skills/` with one or more `SKILL.md` files
- root `AGENTS.md` or `CODEX-CONFIG-INSTRUCTIONS.md`

Outside this scope, do not apply Codex-config skills unless the user explicitly requests them.

## Delegation-First Rule

- If a suitable skill-specific agent exists, dispatch that skill first.
- Keep orchestration context compact: pass file paths, constraints, and required outputs only.
- Prefer short, structured child outputs: changed files, validations run, blockers.
- Fall back to direct edits only when no suitable skill exists or delegation is blocked.

## Skill Routing

| Task | Preferred Skill |
|---|---|
| Audit and optimize skill quality/compliance | `codex-skill-optimizer` |
| Create or update specialized context docs and routing | `codex-context-specializer` |
| Create or refactor a skill from scratch | `skill-creator` |
| Install curated or repo-based skills | `skill-installer` |

## Codex Config Standards

- Keep `AGENTS.md` as the primary instruction file.
- Keep specialized contexts in separate `*-INSTRUCTIONS.md` files and reference them from `AGENTS.md`.
- Keep shared defaults in `config.template.toml`; keep machine-local values in local `config.toml`.
- Prefer `$CODEX_HOME` and env vars over hardcoded user paths.
- Remove legacy provider-specific wording unless explicitly required.

## Validation Workflow

Run this sequence after config or skill changes:

1. Validate touched skills:
   `python skills/.system/skill-creator/scripts/quick_validate.py <skill-path>`
2. Audit touched skill sets:
   `python skills/codex-skill-optimizer/scripts/audit_codex_skills.py --root <skills-root>`
3. Re-run audits after fixes and ensure no remaining errors.
4. Summarize exact commands and outputs in final report.
