# Unreal Engine C++ Struct Creation Rules

Rules for declaring and implementing structs in Unreal Engine C++ projects.
These rules apply globally to all UE projects.

---

## Philosophy

Structs in Unreal Engine should be treated as **a set of parameters and functionality** available as a class field or a passed parameter. Typically, UE structs are not heap-allocated — they use the stack, since structs contain only small-volume data and functions.

---

## 1. USTRUCT Macro

The `USTRUCT()` macro is **mandatory**, even if the struct will only be used in C++.

```cpp
USTRUCT()
struct FMyStruct
{
    GENERATED_BODY()
    // ...
};
```

---

## 2. Constructor Invocation

Constructors in code must only be called using **curly braces `{}`**, not parentheses.

The exception is when `()` is intentionally overridden for struct assembly (e.g., `TEqualTo`).

```cpp
// CORRECT
FMyStruct Data{true};
FMyStruct DefaultData{};

// WRONG - use curly braces
FMyStruct Data(true);
```

---

## 3. Field Access Level

By default, struct fields must be **public**. Private fields are allowed when specific data needs to be hidden.

This is different from classes where all fields are private — structs are treated as data types, not encapsulated objects.

---

## 4. UPROPERTY on All Fields

All struct fields **must** be marked with `UPROPERTY()` for data serialization. This includes private fields.

```cpp
public:
    UPROPERTY()
    bool bActive = false;

private:
    UPROPERTY()
    int32 InternalCounter = 0;
```

---

## 5. Blueprint Access

All struct fields **may have unrestricted Blueprint access** (`BlueprintReadOnly`, `BlueprintReadWrite`), since a struct is considered a data type, not an encapsulated object.

This is different from classes, where Blueprint read/write access is forbidden for fields.

```cpp
// Allowed for structs
UPROPERTY(BlueprintReadWrite)
float Speed = 0.0f;
```

---

## 6. Separate Header for Shared Structs

If a struct is used not only by the class in whose header it is declared, but also by other classes, it **must be moved to a separate header file**. This allows including it where needed without pulling in the entire class.

```
// WRONG - struct used by multiple classes but stuck inside one class header
// MyActor.h
struct FSharedData { ... };
class AMyActor { ... };

// CORRECT - shared struct in its own header
// SharedData.h
struct FSharedData { ... };

// MyActor.h
#include "SharedData.h"
```

---

## 7. EmptyData Static Instance

**All structs must have a static `EmptyData` variable — no exceptions, regardless of struct size.** This serves two purposes:

1. **Initialization & default parameters** — can be used to assign as initialization value or default parameter, similar to `FVector::ZeroVector`.
2. **Defensive programming** — allows returning structs by reference even when data was corrupted or not found (see section 8).

```cpp
/** Empty struct instance used for returning by reference in case of logic errors. */
static const FMyStruct EmptyData;
```

The `EmptyData` variable must be defined in the `.cpp` file:

```cpp
const FMyStruct FMyStruct::EmptyData{};
```

---

## 8. Comparison Operator & IsSet()

### Default operator==

Needed primarily to compare with `EmptyData` for error detection.

```cpp
/** Default comparison operator, primarily for comparing with EmptyData. */
bool operator==(const FMyStruct& ComparedMyStruct) const = default;
```

### IsSet() Function

Returns `false` if the current struct equals `EmptyData`.

**The name `IsSet` is fixed and must not be changed**, as assertion macros expect custom structs to have this function for validation.

```cpp
/** Returns false if the current struct equals EmptyData.
 *  Name is fixed — assertion macros expect this function on custom structs. */
bool IsSet() const;
```

Implementation in `.cpp`:

```cpp
bool FMyStruct::IsSet() const
{
    return *this != EmptyData;
}
```

---

## 9. Function Implementations

All struct function definitions must be in the **`.cpp` file**, same as classes. Only templates may have implementations in the header.

---

## 10. Struct Section Order

```cpp
/** Describes the purpose and essence of the struct.
 *  Why does this struct exist?
 *  What is its main goal? */
USTRUCT()
struct FMyStruct
{
    GENERATED_BODY()

// ============================================================
// Constructors
// ============================================================
/** Constructors section. Always public. */
public:
    FMyStruct(const bool bNewMyStructField);

    FMyStruct();

// ============================================================
// Fields
// ============================================================
/** Fields section. Always public by default. */
public:
    UPROPERTY()
    bool bMyStructField = false;

    UPROPERTY()
    FVector SomeVector = FVector::ZeroVector;

// ============================================================
// EmptyData & Validation
// ============================================================
/** Static empty instance for error detection and defensive programming. */

    /** Empty struct used for returning by reference in case of logic errors. */
    static const FMyStruct EmptyData;

    /** Default comparison operator, primarily for comparing with EmptyData. */
    bool operator==(const FMyStruct& ComparedMyStruct) const = default;

    /** Returns false if the current struct equals EmptyData.
     *  Name is fixed — assertion macros expect this function on custom structs. */
    bool IsSet() const;

// ============================================================
// Private Functions
// ============================================================
/** Private functions section. */
private:
    void PrivateFunction();

// ============================================================
// Public Interface
// ============================================================
/** Public interface section. */
public:
    void ActivateMyStruct();
};
```

---

## Complete Example

### Header (MyStruct.h)

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"
#include "MyStruct.generated.h"

/** Holds character stat data for a single attribute.
 *  Used as a lightweight data container passed between
 *  the trait system and UI components. */
USTRUCT()
struct FCharacterStatData
{
    GENERATED_BODY()

// ============================================================
// Constructors
// ============================================================
public:
    FCharacterStatData(const FGameplayTag& NewStatTag,
                       const float NewBaseValue);

    FCharacterStatData();

// ============================================================
// Fields
// ============================================================
public:
    UPROPERTY(EditDefaultsOnly)
    FGameplayTag StatTag;

    UPROPERTY(EditDefaultsOnly)
    float BaseValue = 0.0f;

    UPROPERTY()
    float CurrentValue = 0.0f;

// ============================================================
// EmptyData & Validation
// ============================================================
    static const FCharacterStatData EmptyData;

    bool operator==(const FCharacterStatData& ComparedData) const = default;

    /** Returns false if the current struct equals EmptyData.
     *  Name is fixed — assertion macros expect this function on custom structs. */
    bool IsSet() const;

// ============================================================
// Private Functions
// ============================================================
private:
    float ClampValue(const float RawValue) const;

// ============================================================
// Public Interface
// ============================================================
public:
    /**
     * Applies a modifier to the current value.
     * @param Modifier The modifier value to apply.
     */
    void ApplyModifier(const float Modifier);

    /**
     * Resets current value to base value.
     */
    void ResetToBase();
};
```

### Implementation (MyStruct.cpp)

```cpp
#include "MyStruct.h"

const FCharacterStatData FCharacterStatData::EmptyData{};

FCharacterStatData::FCharacterStatData(const FGameplayTag& NewStatTag,
                                       const float NewBaseValue)
    : StatTag(NewStatTag)
    , BaseValue(NewBaseValue)
    , CurrentValue(NewBaseValue)
{
}

FCharacterStatData::FCharacterStatData()
{
}

bool FCharacterStatData::IsSet() const
{
    return *this != EmptyData;
}

float FCharacterStatData::ClampValue(const float RawValue) const
{
    return FMath::Max(RawValue, 0.0f);
}

void FCharacterStatData::ApplyModifier(const float Modifier)
{
    CurrentValue = ClampValue(CurrentValue + Modifier);
}

void FCharacterStatData::ResetToBase()
{
    CurrentValue = BaseValue;
}
```

---

## Quick Reference

| # | Rule | Key Point |
|---|------|-----------|
| 1 | USTRUCT macro | Mandatory, even for C++-only structs |
| 2 | Constructor call | Always `{}` curly braces, never `()` |
| 3 | Field access | Public by default; private allowed when needed |
| 4 | UPROPERTY | Required on all fields, including private |
| 5 | Blueprint access | Unrestricted (struct = data type) |
| 6 | Separate header | Move to own `.h` if used by multiple classes |
| 7 | EmptyData | Static const instance on **every** struct, no exceptions |
| 8 | IsSet() | Fixed name; returns `false` if equals EmptyData. Mandatory on all structs |
| 9 | Implementations | Always in `.cpp` (except templates) |
| 10 | Section order | Constructors -> Fields -> EmptyData/Validation -> Private -> Public |
