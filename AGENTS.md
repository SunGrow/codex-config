# Global Agent Standards

## Instruction Style

- Keep instructions concise, direct, and durable.
- Prefer actionable constraints over long policy text.
- Avoid duplicate or auto-generated boilerplate guidance.

## Standard Layout

- Use layered guidance: global `AGENTS.md` -> repo `AGENTS.md` -> nested `AGENTS.override.md` where needed.
- Keep domain-specific policy in separate `*-INSTRUCTIONS.md` files and reference them from `AGENTS.md`.
- Keep skills in standard skill folders with `SKILL.md` + `agents/openai.yaml`.

## Project Detection

- Prefer project-local `AGENTS.md` guidance in the active repository scope.
- If a project uses a non-standard instruction filename, configure `project_doc_fallback_filenames` locally in `config.toml`.
- If no project instructions are present, infer project type from repository markers (for example, `.uproject` for Unreal Engine, `config.toml` + `skills/` for Codex config projects).

## Delegation And Context Budget

- Default to hierarchical dispatch for noisy, specialized, or repeatable tasks.
- If a matching skill-specific agent can handle the task, dispatch it instead of doing the work directly.
- Do work directly only when no suitable skill exists, delegation is blocked, or the user explicitly asks for direct handling.
- Keep the parent context lean: pass only required paths, constraints, and expected output.
- Prefer parallel sub-agents for read-heavy work; coordinate write-heavy edits carefully to avoid conflicts.

## Unreal Engine Projects

- Read `~/.codex/UE-INSTRUCTIONS.md` before UE work.
- Use matching UE skills from `~/.codex/skills/`.
- Run `ue-researcher` first for non-trivial UE implementation; use `ue-research-director` for broad research.
- Prefer specialized UE builders/fixers when relevant:
  `ue-class-builder`, `ue-struct-builder`, `ue-data-asset-builder`, `ue-widget-builder`, `ue-enum-builder`, `ue-module-builder`, `ue-logic-writer`, `ue-build-fixer`, `ue-code-reviewer`, `ue-senior-dev`, `ue-debugger`.

## Codex Configuration Projects

- Read `~/.codex/CODEX-CONFIG-INSTRUCTIONS.md` before Codex config work.
- Treat work as Codex config scoped when repository markers include `config.toml` or `config.template.toml` plus a `skills/` directory.
- Use Codex-config skills only for Codex config scoped work unless the user explicitly asks otherwise.
- Prefer specialized Codex-config skills when relevant:
  `codex-skill-optimizer`, `codex-context-specializer`, `skill-creator`, `skill-installer`.

## Research And Analysis Quality

- Verify unstable facts (APIs, versions, release behavior) against primary sources.
- Prefer official documentation and upstream repositories over third-party summaries.
- Include concrete source links and exact version/date context when relevant.

## Other Projects

- No additional global rules.
