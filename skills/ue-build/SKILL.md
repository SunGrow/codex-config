---
name: ue-build
description: Build the current Unreal Engine project (Development Editor, Win64)
---

# Build UE Project

Build the current Unreal Engine project for Development Editor (Win64). All project details are discovered at runtime — nothing is hardcoded.

## Discovery Chain

Follow these steps **in order**, stopping as soon as you have a complete build command.

### Step 1 — Check AGENTS.md

Walk upward from cwd looking for a `AGENTS.md` file. If found, search for a `## Build` heading (or similar) containing a fenced code block with `Build.bat`. If found:
- Use that command **verbatim**.
- Resolve any relative `.uproject` paths relative to the directory containing AGENTS.md.
- **Skip directly to Execution.**

### Step 2 — Find .uproject

Walk upward from cwd looking for a `*.uproject` file. When found:
- `ProjectName` = filename without extension (e.g., `MyGame.uproject` → `MyGame`)
- Open the file and read the `EngineAssociation` field to get the engine version.
- If `EngineAssociation` is a GUID (indicates a source build), ask the user for the UE engine path directly.

### Step 3 — Locate UE Installation

Try these locations in order to find `Engine\Build\BatchFiles\Build.bat`:

1. `C:\Program Files\Epic Games\UE_<version>\`
2. `D:\Program Files\Epic Games\UE_<version>\`
3. Environment variable `UNREAL_ENGINE_DIR` or `UE_ROOT`
4. If none found, ask the user for the path.

### Step 4 — Construct Build Command

```
"<UE_Install>\Engine\Build\BatchFiles\Build.bat" <ProjectName>Editor Win64 Development -Project="<absolute_path_to_uproject>"
```

## Execution

1. **Show the full command to the user** and ask for confirmation before running (since it was dynamically constructed). If the command came verbatim from AGENTS.md, run it directly without asking.
2. Run the command via Bash with a 10-minute timeout.

## Output

- **Success:** State "Build succeeded" and note the warning count if any.
- **Failure:** List only the error lines (not the full log). Group errors by file if there are multiple.
