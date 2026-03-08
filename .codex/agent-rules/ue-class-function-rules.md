# Unreal Engine C++ Class Function Rules

Rules for declaring and implementing functions in Unreal Engine C++ classes.
These rules apply globally to all UE projects.

---

## 1. No Empty Overrides

Do not override functions if there will be no implementation. For example, `BeginPlay()` or `Tick()` in `AActor` must be removed if they are not used.

```cpp
// WRONG - empty override with no logic
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
}

// CORRECT - just remove the override entirely if not needed
```

---

## 2. Static Functions

If a function does not work with the instance directly (does not read or modify class fields), it must be a `static` function.

```cpp
// CORRECT - does not access any class members
static float CalculateDamage(const float BaseDamage, const float Multiplier);

// WRONG - should be static since it doesn't use class fields
float CalculateDamage(const float BaseDamage, const float Multiplier);
```

**Exception:** If a function must be `virtual` for overriding in subclasses, `virtual` takes priority over `static` (they are mutually exclusive). In this case the function remains non-static even if it doesn't access class fields in the base class.

---

## 3. Const Functions

If a function does not modify data, it must be `const`.

```cpp
// CORRECT
float GetSpeed() const;
FGameplayTag GetClassTag() const;
bool IsValidState() const;

// WRONG - reads data but not marked const
float GetSpeed();
```

---

## 4. BlueprintImplementableEvent as Delegate

If a function has the `UFUNCTION(BlueprintImplementableEvent)` specifier, it is considered a delegate. Its name must follow delegate naming conventions (see [Delegate Rules](ue-class-delegate-rules.md)) — prefixed with `On` and describing the event after which it fires.

```cpp
// CORRECT - follows delegate naming
UFUNCTION(BlueprintImplementableEvent)
void OnScoreChanged(const int32 NewScore);

UFUNCTION(BlueprintImplementableEvent)
void OnInitializationCompleted();

// WRONG - does not follow delegate naming
UFUNCTION(BlueprintImplementableEvent)
void UpdateScoreWidget(const int32 NewScore);
```

---

## 5. Function Parameter Rules

### 5.1 Pass-by-Copy vs. Pass-by-Reference

| Type | How to pass |
|------|-------------|
| Basic types (`bool`, `int32`, `float`, `double`, `uint8`, etc.) | By copy with `const` |
| Enums | By copy with `const` |
| Custom types (all UE structs: `FVector`, `FGameplayTag`, etc.) | By `const` reference |

```cpp
// CORRECT
void SetValue(const float NewValue);
void SetState(const EMyState NewState);
void ApplyTag(const FGameplayTag& Tag);
void SetTransform(const FTransform& NewTransform);

// WRONG - struct by copy
void SetTransform(const FTransform NewTransform);
// WRONG - basic type by reference
void SetValue(const float& NewValue);
```

### 5.2 Const Parameters

- All parameters passed by copy must be `const`.
- All parameters passed by reference that are **not** OUT parameters must be `const`.

```cpp
void ProcessData(const int32 Count, const FGameplayTag& Tag);
```

### 5.3 OUT Parameters

- All OUT parameters must have the prefix `Out_` in their name.
- If an OUT parameter must have initial values on entry that will be reassembled within the function, it must have the prefix `InOut_`.

```cpp
/** Finds actors by tag and writes them to the output array. */
void FindActorsByTag(const FGameplayTag& SearchTag,
                     TArray<AActor*>& Out_FoundActors);

/** Recalculates the existing container data in-place. */
void RecalculateData(const float Multiplier,
                     FMyDataContainer& InOut_DataContainer);
```

### 5.4 Name Collision with Class Fields

If a parameter name matches a class field name and the parameter will be used to assign to that field, add the `New` prefix to the parameter name.

```cpp
private:
    UPROPERTY()
    float Speed = 0.0f;

public:
    /** Sets new speed value. */
    void SetSpeed(const float NewSpeed) { Speed = NewSpeed; }
```

### 5.5 Multi-Parameter Formatting

If a function has **more than 2 parameters**, all parameters must be written in a column, aligned under the first parameter. This applies to both `.h` and `.cpp` files.

```cpp
// Header (.h)
void ProcessCharacter(const FGameplayTag& CharacterTag,
                      const float BaseStat,
                      const bool bApplyModifiers);

// Implementation (.cpp)
void UMyClass::ProcessCharacter(const FGameplayTag& CharacterTag,
                                const float BaseStat,
                                const bool bApplyModifiers)
{
    // Implementation
}
```

---

## 6. Return Value Rules

### 6.1 Basic Types

Basic types are returned by copy.

```cpp
float GetSpeed() const;
int32 GetCount() const;
bool IsValid() const;
```

### 6.2 Structs

Structs are returned by `const` reference.

```cpp
const FGameplayTag& GetClassTag() const;
const FTransform& GetSpawnTransform() const;
```

### 6.3 Optional Data

If there is a chance that struct data may not exist for return by reference (e.g., when searching an array for data that might be absent), use one of these approaches:

**Option A:** Return `TOptional<>`
```cpp
TOptional<FMyData> FindDataByTag(const FGameplayTag& SearchTag) const;
```

**Option B:** Return a static empty instance `::EmptyData`
```cpp
static const FMyData EmptyData;

const FMyData& FindDataByTag(const FGameplayTag& SearchTag) const
{
    // ...
    return EmptyData; // If not found
}
```

### 6.4 Blueprint Return Value Naming

If a function returns a value and must be accessible in Blueprints, always add `UPARAM(DisplayName = "...")` to provide a clean display name in the Blueprint graph.

```cpp
UFUNCTION(BlueprintCallable)
UPARAM(DisplayName = "Character Tag")
FGameplayTag GetCharacterTag() const;

UFUNCTION(BlueprintCallable)
UPARAM(DisplayName = "Is Valid")
bool CheckValidity() const;
```

---

## Quick Reference

| Rule | Key Point |
|------|-----------|
| Empty overrides | Remove unused overrides (`BeginPlay`, `Tick`, etc.) |
| Static | Function doesn't use class fields -> make it `static` (`virtual` takes priority if override needed) |
| Const | Function doesn't modify data -> make it `const` |
| BlueprintImplementableEvent | Treated as delegate; use `On` prefix naming |
| Basic type params | Pass by copy with `const` |
| Struct params | Pass by `const` reference |
| OUT params | Prefix `Out_` or `InOut_` |
| Name collision | Add `New` prefix when param matches field name |
| >2 params | Column-aligned under first parameter |
| Return basic type | By copy |
| Return struct | By `const` reference |
| Missing data | Use `TOptional<>` or `::EmptyData` |
| Blueprint return | Add `UPARAM(DisplayName = "...")` |
