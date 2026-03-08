# ClaudeRules Durable Patterns

Stable patterns preserved from the ClaudeRules `master` and `mod-state` branches.

## Workflow Patterns

- Route work before editing; do not default to inline execution when a specialized workflow exists.
- Use one orchestrator by default, then add child agents only when the work clearly fans out.
- Keep parent context lean by delegating read-heavy discovery and bounded write slices.
- Define effort budgets up front: retry limits, review-fix cycles, and follow-up ceilings.

## Research Patterns

- Verify APIs and unstable claims against primary sources first.
- Split mixed-domain questions into focused sub-questions and synthesize after verification.
- Report uncertainty explicitly instead of guessing.

## Implementation Patterns

- Separate architecture, implementation, review, and validation phases even when one orchestrator owns the full task.
- Keep review outputs findings-first with file and line references.
- Avoid generated or machine-derived source files unless the task explicitly requires them.

## State And Memory Patterns

- Treat hidden agent runtime state as ephemeral.
- Surface reusable learnings in output and curate them into versioned docs later.
- Prefer documented conventions over invisible agent-specific memory.
