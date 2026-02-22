# Unreal Engine 5 - Global Instructions

## Scope

Apply this context only to Unreal Engine repositories (for example, repositories containing `.uproject` files or UE module/plugin structure).

Outside UE scope, do not apply UE routing/skills unless the user explicitly requests them.

## Hierarchical Dispatch (Default)

- Use skill-specific sub-agents as the default execution model for UE work.
- Keep the parent agent focused on task decomposition, acceptance criteria, and final synthesis.
- Dispatch read-heavy tasks in parallel when safe (research, review, log triage); coordinate write-heavy tasks to avoid edit collisions.
- Execute directly only when no suitable UE skill exists or delegation is blocked.

## UE5 Environment

- UE engine path is project-specific. Check project docs (for example `AGENTS.md`, `MEMORY.md`) for the exact path.
- Legacy imported coding rule files are expected at `$CODEX_HOME/agent-rules/`.
- If `CODEX_HOME` is not set, defaults are `%USERPROFILE%\.codex` on Windows and `~/.codex` on macOS/Linux.

## Workflow Preference

Use an orchestrator mindset:
- Plan the architecture and break work into tasks.
- Select the most relevant migrated UE skill for each task.
- Review outputs against rule files before finalizing.
- Prefer `ue-senior-dev` for full implementation pipelines.

## Skill Routing

| Task | Preferred Skill |
|---|---|
| Create class / add fields / add functions | `ue-class-builder` |
| Create struct / add fields | `ue-struct-builder` |
| Create DataAsset / add fields + getters | `ue-data-asset-builder` |
| Create widget / add BindWidget elements | `ue-widget-builder` |
| Create enum / create FunctionLibrary | `ue-enum-builder` |
| Create new plugin or module | `ue-module-builder` |
| Write implementation logic / algorithms | `ue-logic-writer` |
| Build project and fix compilation errors | `ue-build-fixer` |
| Validate code against all project rules | `ue-code-reviewer` |
| Full implementation pipeline (logic -> review -> build) | `ue-senior-dev` |
| Debug runtime issues, trace bugs | `ue-debugger` |
| UE API / subsystem research | `ue-researcher` / `ue-research-director` |

## Pipeline Guidance

- For end-to-end implementation, prefer `ue-senior-dev`.
- For runtime bugs, prefer `ue-debugger`.
- For uncertain APIs and patterns, run `ue-researcher` first.

## Permission Failure Handling

If required filesystem or command permissions are blocked:
1. Stop the current workflow.
2. Report which step/tool was blocked.
3. Ask the user whether to escalate permissions or choose an alternative path.

## Critical Reminder

- AssertUtils plugin should exist in UE projects. If missing, report it before implementation work.
