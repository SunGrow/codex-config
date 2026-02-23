# Unreal Engine C++ Class Field Rules

Rules for declaring and managing class fields in Unreal Engine C++ classes.
These rules apply globally to all UE projects.

---

## 1. Access Level

All fields must be in the **private** section only. This guarantees maximum data encapsulation.

If child classes need access to fields, provide `Get`/`Set` functions instead.

```cpp
// Header (.h)
private:
    UPROPERTY(EditDefaultsOnly)
    float Speed = 100.0f;

public:
    /** Returns current speed value. */
    float GetSpeed() const;

    /** Sets a new speed value. */
    void SetSpeed(const float NewSpeed);
```

```cpp
// Implementation (.cpp)
float UMyClass::GetSpeed() const
{
    return Speed;
}

void UMyClass::SetSpeed(const float NewSpeed)
{
    Speed = NewSpeed;
}
```

**Note:** Even trivial getters/setters must have their implementation in `.cpp`. No inline implementations in `.h` (except templates).

---

## 2. UPROPERTY Macro

All fields **must** be marked with `UPROPERTY()`. This ensures:
- Data serialization
- Reflection access
- Ability to apply additional property settings (metadata, replication, etc.)

---

## 3. Blueprint Access

Fields may only be exposed to Blueprints for **editing** via:
- `EditDefaultsOnly` — editable on class defaults only
- `EditInstanceOnly` — editable on placed instances only

Fields must **never** be readable or writable from Blueprint code (`BlueprintReadOnly`, `BlueprintReadWrite`), as this violates encapsulation.

```cpp
// CORRECT
UPROPERTY(EditDefaultsOnly)
float MaxHealth = 100.0f;

// WRONG - violates encapsulation
UPROPERTY(EditDefaultsOnly, BlueprintReadOnly)
float MaxHealth = 100.0f;
```

---

## 4. Field Initialization

All fields must be initialized **in the header file**, not in the constructor.

```cpp
// CORRECT - initialized in header
private:
    UPROPERTY()
    float Speed = 100.0f;

    UPROPERTY()
    int32 Count = 0;

    UPROPERTY()
    TObjectPtr<AActor> TargetActor = nullptr;
```

```cpp
// WRONG - initialized in constructor
UMyClass::UMyClass()
{
    Speed = 100.0f;  // Should be in the header
    Count = 0;       // Should be in the header
}
```

### Custom Type Verification

When initializing a field of a custom type (enum, struct, etc.), you **MUST read the type's header file** to verify:
- For enums: that the default value actually exists in the enum
- For structs: that initialization syntax matches its constructors

**NEVER guess or assume enum values.** Always verify against source.

```cpp
// WRONG - assumed "Normal" exists without checking the enum definition
UPROPERTY()
ENotificationPriority Priority = ENotificationPriority::Normal;  // "Normal" doesn't exist!

// CORRECT - verified against the actual enum definition in NotificationPriority.h
UPROPERTY()
ENotificationPriority Priority = ENotificationPriority::None;
```

---

## 5. Bool Fields

### Naming
- All bool variables, fields, and parameters must always start with `b`.
- The name must **not** contain verbs (`Is`, `Can`, `Are`, `Has`, `Should`, etc.).
- A bool must represent an on/off state concept.

```cpp
// CORRECT
UPROPERTY(EditDefaultsOnly)
bool bActive = false;

UPROPERTY()
bool bVisible = true;

UPROPERTY()
bool bLocked = false;

// WRONG - contains verbs
bool bIsActive = false;
bool bCanMove = true;
bool bHasTarget = false;
```

### Two-State Values

If a bool represents two distinct different states (e.g., left/right side, day/night), it must be refactored into an `enum` for better readability.

```cpp
// WRONG - two different states as bool
bool bLeftSide = true;

// CORRECT - use enum for distinct states
UENUM()
enum class ESide : uint8
{
    Left,
    Right
};

UPROPERTY()
ESide CurrentSide = ESide::Left;
```

---

## 6. TObjectPtr

`TObjectPtr` is used **only** for pointer fields of classes and structs. It allows the editor to load faster and better manage resources when loading assets and blueprints.

**IMPORTANT:** `TObjectPtr` must **not** be used in function code (local variables, parameters, return types), as it serves no purpose there and has no effect on code execution.

```cpp
// CORRECT - TObjectPtr for class fields
private:
    UPROPERTY()
    TObjectPtr<AActor> OwnerActor = nullptr;

    UPROPERTY(EditDefaultsOnly)
    TObjectPtr<UDataAsset> ConfigAsset = nullptr;

// CORRECT - raw pointer in function code
void UMyClass::ProcessActor()
{
    AActor* FoundActor = GetOwner();  // NOT TObjectPtr
    if (FoundActor)
    {
        // ...
    }
}

// WRONG - TObjectPtr in function code
void UMyClass::ProcessActor()
{
    TObjectPtr<AActor> FoundActor = GetOwner();  // Pointless here
}
```

---

## Quick Reference

| Rule | Key Point |
|------|-----------|
| Access level | Always `private`; use Get/Set for child access |
| UPROPERTY | Required on all fields (serialization + reflection) |
| Blueprint access | Only `EditDefaultsOnly` / `EditInstanceOnly`; never `BlueprintReadOnly`/`ReadWrite` |
| Initialization | Always in the header, never in the constructor |
| Bool naming | Prefix `b`; no verbs; represents on/off state |
| Bool two-state | Refactor to `enum` if it represents two distinct states |
| TObjectPtr | Only for class/struct pointer fields; never in function code |
