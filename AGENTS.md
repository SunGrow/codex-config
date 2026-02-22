# Global Agent Standards

## Instruction Style

- Keep instructions concise, direct, and durable.
- Prefer actionable constraints over long policy text.
- Avoid duplicate or auto-generated boilerplate guidance.

## Project Detection

- Prefer project-local `AGENTS.md` guidance in the active repository scope.
- If a project uses a non-standard instruction filename, configure `project_doc_fallback_filenames` locally in `config.toml`.
- If no project instructions are present, infer project type from repository markers (for example, `.uproject` for Unreal Engine).

## Unreal Engine Projects

- Read `~/.codex/UE-INSTRUCTIONS.md` before UE work.
- Use matching UE skills from `~/.codex/skills/`.
- Run `ue-researcher` first for non-trivial UE implementation; use `ue-research-director` for broad research.
- Prefer specialized UE builders/fixers when relevant:
  `ue-class-builder`, `ue-struct-builder`, `ue-data-asset-builder`, `ue-widget-builder`, `ue-enum-builder`, `ue-module-builder`, `ue-logic-writer`, `ue-build-fixer`, `ue-code-reviewer`, `ue-senior-dev`, `ue-debugger`.

## Research And Analysis Quality

- Verify unstable facts (APIs, versions, release behavior) against primary sources.
- Prefer official documentation and upstream repositories over third-party summaries.
- Include concrete source links and exact version/date context when relevant.

## Other Projects

- No additional global rules.
