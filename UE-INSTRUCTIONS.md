# Unreal Engine 5 - Global Instructions

## Scope

Apply this context only to Unreal Engine repositories (for example, repositories containing `.uproject` files or UE module/plugin structure).

Outside UE scope, do not apply UE routing/skills unless the user explicitly requests them.

## Hierarchical Dispatch (Default)

- Use skill-specific sub-agents as the default execution model for UE work.
- Keep the parent agent focused on task decomposition, acceptance criteria, and final synthesis.
- Dispatch read-heavy tasks in parallel when safe (research, review, log triage); coordinate write-heavy tasks to avoid edit collisions.
- Execute directly only when no suitable UE skill exists or delegation is blocked.

## UE Parallelization Playbook

1. Split by subsystem first (UI, gameplay, data assets, build/debug).
2. Run independent research/review tasks in parallel (`ue-researcher`, `ue-code-reviewer`).
3. Assign non-overlapping file ownership for parallel implementation tasks.
4. Rejoin at integration points, then run one final review/build pass (`ue-code-reviewer`, `ue-build-fixer`).

## UE Decision Handoff

- UE leaf workers (`ue-logic-writer`, `ue-build-fixer`, etc.) should not ask the user directly for yes/no decisions.
- Leaf workers must emit `DECISION_REQUIRED` to their caller when blocked on user intent.
- Caller/orchestrator asks the user, then sends `DECISION_RESULT` back to the leaf worker.
- When in Plan mode, caller should use the dedicated user-input flow; otherwise caller asks directly in normal chat.

## UE Permission Handoff

- UE leaf workers must not ask the user for tool permission prompts directly.
- UE leaf workers must emit `PERMISSION_REQUIRED` when blocked on privileged tool execution.
- Caller/orchestrator owns approval prompts and privileged command execution.
- Caller returns `PERMISSION_RESULT` with `executed`, `denied`, or `unavailable`, then worker continues with normal or fallback path.
- Assume nested workers may not have an approval channel. Always route permission requests through caller.

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
1. Emit `PERMISSION_REQUIRED` to caller with exact command and expected effect.
2. Wait for `PERMISSION_RESULT`.
3. If denied/unavailable, report blocked step and execute or propose the non-privileged fallback path.

## Critical Reminder

- AssertUtils plugin should exist in UE projects. If missing, report it before implementation work.
