---
name: codex-context-specializer
description: "Create or refactor specialized Codex project contexts (`*-INSTRUCTIONS.md`) and wire scoped skill routing in `AGENTS.md`. Use for new domain contexts, context-scope cleanup, and delegation-first context-budget optimization."
---

# Codex Context Specializer

## Overview

Use this skill to create and maintain specialized context documents for Codex-config repositories without bloating the main instruction surface.

## Workflow

1. Identify the target domain and scope markers.
2. Generate a context scaffold with `scripts/create_specialized_context.py`.
3. Update `AGENTS.md` to reference the new context and define routing boundaries.
4. Add or refine domain skill routing and delegation-first rules.
5. Add or refine decision/permission handoff policy (caller-owned user prompts and privileged execution).
6. Validate any touched skills and run skill audits.
7. Return a concise change summary with file paths and commands.

## Commands

Create a new specialized context scaffold:

```bash
python scripts/create_specialized_context.py --domain codex-config --output CODEX-CONFIG-INSTRUCTIONS.md --marker config.toml --marker skills/ --route codex-skill-optimizer="Audit and optimize Codex skills" --route codex-context-specializer="Create and refine specialized contexts"
```

Write to a temporary file first:

```bash
python scripts/create_specialized_context.py --domain backend --output tmp/BACKEND-INSTRUCTIONS.md --marker pyproject.toml --marker services/
```

Overwrite an existing context file:

```bash
python scripts/create_specialized_context.py --domain codex-config --output CODEX-CONFIG-INSTRUCTIONS.md --force
```

## Delegation Policy

- If a suitable skill exists for a subtask, dispatch it first.
- Keep parent orchestration context minimal.
- Execute directly only if no suitable skill exists or delegation is blocked.

## Handoff Policy

- Contexts must define both decision handoff (`DECISION_REQUIRED`/`DECISION_RESULT`) and permission handoff (`PERMISSION_REQUIRED`/`PERMISSION_RESULT`).
- Permission requests from leaf workers must route through caller; leaf workers should not prompt user approvals directly.
- If approval is unavailable in runtime policy, require explicit fallback behavior.

## Quality Checks

After context or routing edits:

1. Validate each changed skill:
   `python skills/.system/skill-creator/scripts/quick_validate.py <skill-path>`
2. Audit changed skill roots:
   `python skills/codex-skill-optimizer/scripts/audit_codex_skills.py --root <skills-root>`
3. Use `references/context-quality-checklist.md` for manual review.
