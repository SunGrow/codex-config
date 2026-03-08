# Agentic Workflow Instructions

## Scope

Apply this context to general software projects, agentic workflow design, and multi-file implementation tasks that are not Unreal-specific.

If a repository is Unreal-specific, follow `UE-INSTRUCTIONS.md` first and use this file only for generic orchestration patterns that still apply.

## Routing

- Prefer direct handling for simple questions, tiny edits, and bounded single-file work.
- Prefer `researcher` for focused technical research or API verification.
- Prefer `research-director` for broad, mixed-domain, or multi-question research.
- Prefer `code-architect` for interface design, system decomposition, and architecture briefs.
- Prefer `code-reviewer` for review-only requests.
- Prefer `senior-dev` for end-to-end implementation that spans multiple files, phases, or validation loops.

## Orchestration Defaults

- Use one orchestrator by default. Add more child agents only when the work clearly fans out.
- Keep the parent context lean: pass paths, constraints, ownership, and expected output only.
- Use `explorer` agents for read-heavy codebase discovery.
- Use `worker` agents for bounded write tasks with explicit file ownership.
- Parallelize independent read-heavy tasks by default. Parallelize write-heavy tasks only with disjoint ownership.

## Escalation Model

- Parent agents own user interaction.
- Child agents must not ask the user directly for decisions or approvals.
- Child agents escalate unresolved choices with `DECISION_REQUIRED`.
- Child agents escalate blocked privileged actions with `PERMISSION_REQUIRED`.
- Parent agents respond with `DECISION_RESULT` or `PERMISSION_RESULT` and continue orchestration.

## Context Budget Rules

- If the task touches more than three files, prefer decomposition before editing.
- If the task mixes architecture, implementation, validation, and research, split those phases explicitly.
- Push deterministic loops, filtering, and batching into shell commands or scripts instead of repeated model turns.
- Do not import Claude transport patterns such as temp-file polling, runner scripts, or restart protocols.

## Validation Expectations

- Define a stopping rule before dispatching child work: max review-fix cycles, max retries, or max follow-up rounds.
- Run one integration validation pass after parallel work rejoins.
- Report only the information the caller needs: outcome, touched files, remaining blockers, and validation results.

## Output Conventions

- Architecture work should end with an `Architecture Brief`.
- Research work should end with a `Research Brief`.
- Implementation orchestration should end with `Implementation Complete` or `Implementation Blocked`.
- Review work should be findings-first, with file and line references.

## Durable Learnings

- Child agents must not modify shared memory or instruction files during normal execution.
- If they discover reusable knowledge, they should return a `Reusable Learnings` section in their final output.
- The parent decides whether to persist those learnings into versioned docs under `docs/` or `memories/`.
