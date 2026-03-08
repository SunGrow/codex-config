# UE Agent Memory Rules

This file is retained as a UE-facing compatibility entrypoint.

The canonical Codex policy now lives in `agent-memory-rule.md`.

---

## UE-Specific Guidance

- Keep shared memory read-only during normal UE task execution.
- Return durable discoveries in a `Reusable Learnings` section so the caller can decide whether they belong in `memories/` or in a project-local doc.
- Treat engine quirks, module dependency pairings, and reusable Blueprint/MCP workflows as generic candidates.
- Treat build commands, project paths, subsystem names, and repo-specific architecture notes as project-local candidates.

## Decision Test

> Would this still help on a different Unreal project?

- Yes: generic durable note
- No: project-local note, or do not persist
