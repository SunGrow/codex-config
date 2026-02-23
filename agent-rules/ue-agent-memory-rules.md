# Agent Memory Management Rules

Rules for how agents store and retrieve persistent knowledge across sessions.

---

## Two Memory Scopes

Every agent has access to two memory locations:

| Scope | Path | What goes here |
|-------|------|----------------|
| **Generic** (cross-project) | `C:\Users\Admin\.claude\agent-memory\<agent-name>\MEMORY.md` | Universal UE patterns, API quirks, tool usage tips — knowledge that applies to ANY project |
| **Project-specific** | `<project-memory-dir>\<agent-name>_memory.md` | Project paths, class names, build commands, known bugs, project conventions — knowledge that applies ONLY to the current project |

The **project memory directory** path can be found in the project's `MEMORY.md` file (look for the `memory/` directory path in the auto-loaded context).

---

## What Goes Where

### Generic Memory (agent-memory)
- UE engine API behaviors and quirks (e.g., "FText doesn't support defaulted operator==")
- Universal coding patterns (e.g., "Plugin dependency requires both Build.cs AND .uplugin entries")
- Common include paths for engine/plugin headers
- Tool usage tips (e.g., "build timeout should be 600000ms")
- Patterns that would apply in a different project with the same engine version

### Project-Specific Memory (project memory)
- Build commands with project paths
- Known project-specific bugs and their status
- Project file paths and directory structure
- Project-specific class names, component references, subsystem references
- Plugin configurations specific to the project (e.g., CatUI include paths)
- Any knowledge that mentions a concrete project name, file path, or class unique to this project

### Decision Test
> **"Would this knowledge be useful if I started working on a completely different UE project tomorrow?"**
> - **Yes** → Generic memory
> - **No** → Project-specific memory

---

## Workflow: Writing Memory

1. **Determine the scope** using the decision test above.
2. **Check for existing entries** in the target file — avoid duplicates.
3. **Write to the correct file:**
   - Generic → `C:\Users\Admin\.claude\agent-memory\<agent-name>\MEMORY.md`
   - Project-specific → `<project-memory-dir>\<agent-name>_memory.md`
     - If this file doesn't exist yet, create it with a header: `# <Agent Display Name> — <Project Name> Project Memory`
4. **Never mix scopes** — if a discovery has both generic and project-specific parts, split them and write to both files.

---

## Workflow: Reading Memory

On every session start:
1. Your **generic MEMORY.md** is auto-loaded into context (no action needed).
2. **Check if a project-specific memory file exists** for you: look for `<agent-name>_memory.md` in the project's memory directory. If it exists, **read it** before starting work.

---

## Examples

```
GENERIC (agent-memory):
  "AssertUtils macros: #include "AssertUtils/Assert.h" (NOT #include "Assert.h")"
  → Applies to any project using AssertUtils

PROJECT-SPECIFIC (project memory):
  "Build command: ...OfficeStrategyEditor Win64 Development -Project=..."
  → Only applies to OfficeStrategy project

GENERIC:
  "FText does not support C++20 defaulted operator=="
  → UE engine behavior, applies everywhere

PROJECT-SPECIFIC:
  "FOfficeNotificationData needed explicit operator== due to FText field"
  → Specific struct in a specific project
```
