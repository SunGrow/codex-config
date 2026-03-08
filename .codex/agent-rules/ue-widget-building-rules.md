# UE Widget Building Rules

## Core Principle

UMG widgets in C++ define **logic and input handling only**. Visual layout is done in **Blueprint** (the WBP_ asset).
**DO NOT** construct widget hierarchy in C++ (no `ConstructWidget`, `AddChild`, slot manipulation in `NativeConstruct`),
**EXCEPT** for dynamic data-driven elements created via `TSubclassOf<>` + `CreateWidget` (see Rule 4).

## Rules

### 1. No C++ Construction of Widget Tree
- Never build the widget's own layout structure programmatically (no creating buttons, text blocks, overlays, etc. in C++).
- Dynamic population of `BindWidget` containers with data-driven elements via `TSubclassOf` is the exception (see Rule 4).

### 2. All UI Elements Must Be `BindWidget` Fields
- Every button, text block, scroll box, overlay, etc. must be a `UPROPERTY` field with `meta=(BindWidget)`.
- The Blueprint designer binds these to actual widget components by matching the field name.

```cpp
UPROPERTY(meta = (BindWidget))
TObjectPtr<UButton> Btn_Submit;

UPROPERTY(meta = (BindWidget))
TObjectPtr<UTextBlock> Txt_Title;

UPROPERTY(meta = (BindWidget))
TObjectPtr<UScrollBox> ScrollBox_Items;
```

### 3. C++ = Logic, Blueprint = Visuals
- C++ handles: button click callbacks, input validation, data binding, delegate broadcasting.
- Blueprint handles: layout, styling, sizing, anchors, animations, visual polish.
- **All widget classes created in C++ MUST be `Abstract`** (`UCLASS(Abstract, Blueprintable, BlueprintType)`). The real working widget is always a Blueprint child where `BindWidget` elements are laid out. This applies to both parent widgets and reusable elements.

### 4. Repeating Elements → Separate Abstract Widget Classes + Dynamic Creation
- If a UI pattern repeats (e.g., button + text input), extract it into its own `UUserWidget` subclass.
- **Base element class MUST be `Abstract`** (`UCLASS(Abstract)`) — the user must create a Blueprint child to define visuals.
- The parent widget stores `TSubclassOf<>` fields (`EditDefaultsOnly`) so the Blueprint designer picks which element class to spawn.
- Creating these elements via `CreateWidget<T>(this, SubclassField)` + `Container->AddChild()` at runtime **IS allowed** — this is the only valid case of programmatic widget creation.

```cpp
// Parent widget — element class chosen in Blueprint
UPROPERTY(EditDefaultsOnly, Category = "Widget")
TSubclassOf<UMyElement_Base> ElementClass = nullptr;

// At runtime — populate a BindWidget container with data-driven elements
UMyElement_Base* Element = CreateWidget<UMyElement_Base>(this, ElementClass);
Element->Initialize(Data);
ContainerBox->AddChild(Element);
```

```cpp
// Element base — MUST be Abstract
UCLASS(Abstract, Blueprintable, BlueprintType)
class UMyElement_Base : public UUserWidget { ... };
```

### 5. Test Widget Element Storage
- Test-only reusable widget elements go in:
  `Source/<MainModule>/Framework/TestCode/Widgets/Elements/` (replace `<MainModule>` with the project's main module name from project `AGENTS.md`)
- Before creating a new element, check this folder for existing ones.

### 6. Update Element Registry
- After creating a new reusable element, update the element list below.

---

## Reusable Element Registry

| Class Name | Location | Description |
|---|---|---|
| `UW_IntInputAction` | `TestCode/Widgets/Elements/` | Button + TextBox input. On click, returns integer only (strips all non-digit characters, removes `.` and `,`). |
