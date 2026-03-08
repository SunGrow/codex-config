# Durable Memories

This directory stores versioned, human-reviewed learnings that are worth keeping beyond a single task or session.

## Principles

- Prefer markdown notes over hidden agent-specific runtime files.
- Keep entries concise, stable, and easy to audit.
- Store cross-project patterns here.
- Store project-specific knowledge in the relevant repository, not in global memory, unless it truly generalizes.

## Workflow

1. Child agents return reusable learnings in final output.
2. The parent or maintainer decides whether those learnings are durable.
3. Durable items are curated into markdown files here or into project-local docs.

## Seed Notes

- `claude-rules-durable-patterns.md` captures the stable patterns extracted during the ClaudeRules migration.
