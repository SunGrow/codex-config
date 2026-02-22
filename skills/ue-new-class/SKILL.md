---
name: ue-new-class
description: Scaffold a new UE5 C++ class following discovered project conventions
---

# Scaffold UE5 C++ Class

Create a new Unreal Engine 5 C++ class (header + implementation) by discovering all project conventions at runtime. Nothing is hardcoded — every convention is detected from AGENTS.md, project files, or existing source code.

## Phase 1: Discovery

Execute these steps in priority order. Earlier sources override later ones.

### Step 1 — AGENTS.md (highest authority)

Walk upward from cwd looking for `AGENTS.md`. If found, extract any of the following that are documented:

- Module name and API macro
- Source directory structure (e.g., `Source/<Module>/` or nested subdirectories)
- Copyright line
- Comment language (e.g., Russian, English, Japanese)
- Coding standards (field rules, section ordering, separator style)
- Include path rules (public include paths, short-form conventions)
- Class prefix patterns

AGENTS.md is the **highest authority** — its rules override anything observed in the codebase (the project may be transitioning to new conventions).

### Step 2 — .uproject + .Build.cs (for anything not in AGENTS.md)

- Walk upward from cwd for `*.uproject`. Read the `Modules` array to get the module name(s) and `EngineAssociation` for the engine version.
- **Plugin awareness:** If cwd is inside a directory containing a `.uplugin` file, use that plugin's module name and its `.Build.cs` instead of the game module.
- **Multi-module:** If there is exactly one module, use it. If there are multiple, let the target directory determine the module, or ask the user.
- Find `Source/<ModuleName>/<ModuleName>.Build.cs` and read it for:
  - `PublicIncludePaths` / `PrivateIncludePaths`
  - Module dependencies
- Derive the API macro using UE convention: `<MODULENAME_UPPERCASE>_API` (e.g., module `MyGame` → `MYGAME_API`).

### Step 3 — Codebase Scan (for conventions not documented anywhere)

Read **3–5 existing `.h` files** in the module's source directory. Infer:
- Copyright header text and format
- Comment language
- Section separator style (e.g., `// ====...`, `// ----...`, or none)
- Section order (constructor, overrides, fields, public interface, etc.)
- Field patterns (private? `UPROPERTY()`? `TObjectPtr<>`? header-initialized?)
- Naming prefix conventions

Read **1–2 existing `.cpp` files**. Infer:
- Include ordering style
- Whether `UE_INLINE_GENERATED_CPP_BY_NAME` is used
- Section separator style in implementation files
- Self-include path format (determines how the `.h` should be included)

### Step 4 — Ask the User

Prompt for any information not provided as skill arguments:
- Class name
- Base class
- Target directory (within the source tree)
- Optional: brief description of the class purpose

Do **not** re-ask for anything already provided as arguments to the skill invocation.

## Phase 2: Generation

### Convention Priority

Apply conventions in this order: **AGENTS.md rules > Observed codebase patterns > Fallback defaults**

### Base Class Include Mapping

Map common base classes to their include paths:

| Base Class | Include |
|---|---|
| `AActor` | `GameFramework/Actor.h` |
| `APawn` | `GameFramework/Pawn.h` |
| `ACharacter` | `GameFramework/Character.h` |
| `APlayerController` | `GameFramework/PlayerController.h` |
| `AGameModeBase` | `GameFramework/GameModeBase.h` |
| `AGameStateBase` | `GameFramework/GameStateBase.h` |
| `AHUD` | `GameFramework/HUD.h` |
| `APlayerState` | `GameFramework/PlayerState.h` |
| `UObject` | `UObject/NoExportTypes.h` |
| `UActorComponent` | `Components/ActorComponent.h` |
| `USceneComponent` | `Components/SceneComponent.h` |
| `UUserWidget` | `Blueprint/UserWidget.h` |
| `UCommonActivatableWidget` | `CommonActivatableWidget.h` |
| `UGameInstanceSubsystem` | `Subsystems/GameInstanceSubsystem.h` |
| `UWorldSubsystem` | `Subsystems/WorldSubsystem.h` |
| `UPrimaryDataAsset` | `Engine/DataAsset.h` |
| `UAttributeSet` | `AttributeSet.h` |
| `UGameplayAbility` | `Abilities/GameplayAbility.h` |

If the base class is not in this table, search the codebase or engine headers to find the correct include.

### Generate .h File

Assemble the header using discovered conventions:
1. Copyright header (if discovered; omit if not)
2. `#pragma once`
3. Includes: `CoreMinimal.h`, base class header, project includes, then `<ClassName>.generated.h` last
4. Forward declarations (if needed)
5. Class doc-comment (if description provided, in discovered language)
6. `UCLASS()` declaration with discovered API macro
7. `GENERATED_BODY()`
8. Sections in discovered order with discovered separator style

### Generate .cpp File

Assemble the implementation using discovered conventions:
1. Copyright header (matching .h style)
2. Self-include (using the path format observed in existing .cpp files)
3. `UE_INLINE_GENERATED_CPP_BY_NAME(<ClassName>)` if observed or engine version is 5.1+
4. Additional includes
5. Constructor implementation
6. Sections matching .h order with matching separator style

### Fallback Defaults (when nothing is discovered)

| Value | Default |
|---|---|
| Copyright | Omit entirely |
| Comment language | English |
| Section separators | None (minimal layout) |
| Section order | Constructor → Overrides → Fields (private) → Public interface |
| Field style | Private, `UPROPERTY()`, `TObjectPtr<>` for pointers, initialized in header |
| `UE_INLINE_GENERATED_CPP_BY_NAME` | Include (standard since UE 5.1) |
| API macro | `<MODULENAME_UPPERCASE>_API` |

## Coding Conventions (Fallback Defaults)

These are standard UE5 conventions used when **neither AGENTS.md nor codebase scan** provides a project-specific rule. Discovered conventions always take priority.

### Fields
- Always private with `UPROPERTY()`
- `TObjectPtr<>` for pointer fields (not raw pointers)
- Initialize in header, not in constructor
- `EditDefaultsOnly` or `EditInstanceOnly` — never `BlueprintReadWrite` (exception: MVVM FieldNotify)
- Bool prefix: `b` — no verbs (`bActive`, not `bIsActive`)
- One blank line between each field

### Functions
- Delete unused overrides (empty `BeginPlay`, empty `Tick`)
- Use `static` if function doesn't access instance members
- Use `const` if function doesn't modify data
- Params: copy+const for primitives/enums, reference+const for structs
- Out params: `Out_`/`InOut_` prefix
- More than 2 params: stack vertically, aligned to first param
- Factory methods: `NewObject_ClassName` for UObjects, `NewActor_ClassName` for Actors

### Comments
- `/** */` doc-comments in headers only
- `//` comments in `.cpp` only

### Defensive Programming
- Validate all inputs: assert → log → return early with safe default
- Always handle `default:` in switch
- Use `for` loops, avoid `while`
- Use `<` only for comparisons (values left-to-right: small → large)

### Structs (if generating)
- `USTRUCT()` + `GENERATED_BODY()`
- Public fields with `UPROPERTY()`
- Include: `static const FMyStruct EmptyData;`
- Include: `bool operator==(const FMyStruct&) const = default;`
- Include: `bool IsSet() const;`

### Enums (if generating)
- `enum class EName : uint8`
- Always start with `None`

### Delegates (if generating)
- Always Dynamic Multicast
- Public, `BlueprintAssignable`
- Named as events: `OnSomethingCompleted`

### Data Assets (if generating)
- Private fields with `EditDefaultsOnly`
- Getters as `UFUNCTION(BlueprintPure)`
- `TSoftObjectPtr<>` for heavy assets, `TObjectPtr<>` for other Data Assets
- Arrays: `meta = (TitleProperty = "FieldName")`
- Override `GetPrimaryAssetId()` returning `FPrimaryAssetId("TypeName", GetFName())`

## After Scaffolding

Report what was created (file paths and class name) and remind the user to:
1. Register the class in a Blueprint if needed
2. Add any necessary config entries (e.g., `DefaultEngine.ini` for Data Assets)
