# Specialized Context Quality Checklist

Use this checklist after adding or editing a `*-INSTRUCTIONS.md` context.

## Scope

- Context clearly defines where it applies.
- Scope markers are concrete and repo-detectable.
- Out-of-scope behavior is explicit.

## Delegation And Context Budget

- Delegation-first rule is explicit.
- Parent/orchestrator context is kept minimal.
- Fallback conditions for direct execution are explicit.

## Skill Routing

- Routing table maps real tasks to existing skills.
- Routing avoids generic overlap when a specialized skill exists.
- Skills are scoped to the intended project/domain context.

## Validation

- Changed skills were validated with `quick_validate.py`.
- Changed skill roots were audited with `codex-skill-optimizer`.
- Validation commands and outcomes are captured in the final report.

## Maintainability

- No legacy provider-only terms unless intentionally required.
- Paths are portable (`$CODEX_HOME` or relative paths).
- Instructions remain concise and operational.
