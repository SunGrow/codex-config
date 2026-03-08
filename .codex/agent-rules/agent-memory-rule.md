# Agent Memory Management Rules

Rules for capturing durable learnings in Codex without relying on hidden per-agent runtime state.

---

## Default Policy

- Do not edit shared memory or instruction files during normal task execution.
- Child agents surface reusable knowledge in their final output instead of persisting it directly.
- Parents decide whether a learning is durable enough to store under `docs/` or `memories/`.

---

## Storage Model

| Scope | Location | What belongs here |
|---|---|---|
| Generic | `$CODEX_HOME/memories/` | Stable patterns that apply across projects |
| Project-specific | Project-local docs or memory files referenced by that project's `AGENTS.md` | Paths, commands, conventions, and recurring issues unique to one codebase |

Use versioned markdown docs rather than hidden, agent-specific runtime files.

---

## Decision Test

Ask:

> Would this still be useful in a different project or a later session after the current task is gone?

- Yes: candidate for generic durable notes
- No: candidate for project-local notes or do not persist

---

## What To Save

- Stable workflow patterns confirmed more than once
- Reliable API quirks, dependency requirements, and migration notes
- Project conventions that are expensive to rediscover
- Repeat blockers and their proven fixes

## What Not To Save

- Task-local scratch state
- Incomplete or unverified conclusions
- Duplicates of `AGENTS.md` or instruction files
- Secrets, credentials, or machine-specific runtime artifacts

---

## Reusable Learnings Format

When a child agent discovers durable knowledge, return it in this format:

```md
## Reusable Learnings
- Generic: <stable pattern or rule>
- Project: <repo-specific convention or command>
```

Parents can then curate those items into versioned docs when appropriate.
