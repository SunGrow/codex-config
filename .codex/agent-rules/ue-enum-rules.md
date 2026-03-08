# Unreal Engine C++ Enumeration Creation Rules

Rules for declaring and using enumerations in Unreal Engine C++ projects.
These rules apply globally to all UE projects.

---

## 1. UENUM Macro

The `UENUM()` macro is **mandatory**, even if the enum will only be used in C++.

```cpp
UENUM()
enum class EMyEnum : uint8
{
    None,
    Value1
};
```

---

## 2. Declaration Format

Enums must **only** be declared as `enum class EName : uint8`.

If more variants are needed than `uint8` (255) can hold, a wider type may be used (`uint16`, `uint32`).

```cpp
// CORRECT
UENUM()
enum class EMyEnum : uint8 { ... };

// CORRECT - if more than 255 values needed
UENUM()
enum class ELargeEnum : uint16 { ... };

// WRONG - not enum class
UENUM()
enum EMyEnum { ... };

// WRONG - missing underlying type
UENUM()
enum class EMyEnum { ... };
```

---

## 3. Mandatory None Value

All enums **must** have `None` as the first value. `None` is required so that data can be checked for validity.

```cpp
UENUM()
enum class EWeaponType : uint8
{
    None,       // Required first value for validity checks
    Sword,
    Bow,
    Staff
};
```

---

## 4. No Numeric Assignments

Enum values must **not** have explicit numeric assignments. Let the compiler assign values automatically.

```cpp
// CORRECT
UENUM()
enum class EItemRarity : uint8
{
    None,
    Common,
    Uncommon,
    Rare
};

// WRONG - explicit numeric values
UENUM()
enum class EItemRarity : uint8
{
    None = 0,
    Common = 4,
    Uncommon = 8,
    Rare = 12
};
```

---

## 5. No MaxValue

Do **not** add a `MaxValue` or `MAX` entry to enums.

```cpp
// WRONG
UENUM()
enum class EMyEnum : uint8
{
    None,
    Value1,
    Value2,
    MaxValue    // Do not add this
};
```

---

## 6. Separate Header for Shared Enums

If an enum is used not only by the class in whose header it is declared, but also by other classes, it **must be moved to a separate header file**. This allows including it where needed without pulling in the entire class.

```
// WRONG - enum used by multiple classes but stuck inside one class header
// MyActor.h
enum class EItemRarity : uint8 { ... };
class AMyActor { ... };

// CORRECT - shared enum in its own header
// ItemRarity.h
enum class EItemRarity : uint8 { ... };
```

---

## 7. State Pattern Consideration

If an enum describes **object states**, consider whether those states should be refactored into separate classes using the **State pattern** instead of remaining as enum values.

```cpp
// Simple enum is fine for small, simple state sets
UENUM()
enum class EDoorState : uint8
{
    None,
    Open,
    Closed,
    Locked
};

// But if states have complex behavior, consider the State pattern instead
// e.g., ECharacterBehaviorMode with different logic per state
// -> Refactor into UStateControl subclasses
```

---

## 8. Getting Enum Value as String

To get an enum value as `FString`, use the following function:

```cpp
UEnum::GetValueAsString(TEXT("ModuleName.EnumName"), EnumVariable);
```

Where:
- **ModuleName** — the name of the module where the enum is defined
- **EnumName** — the full enum class name including the `E` prefix
- **EnumVariable** — the variable of the enum type being read

```cpp
// Example
FString EnumNameAsString = UEnum::GetValueAsString(
    TEXT("MyGame.EItemRarity"), ItemRarity);
```

---

## 9. Support Function Library

If an enum has associated support/utility functions used across different parts of the project, a **separate function library** must be created for them. The enum header must include a reference comment pointing to that library file.

```cpp
// ItemRarity.h
#pragma once

#include "ItemRarity.generated.h"

/** Defines the rarity tier for items and loot.
 *  See UItemRarityLibrary for utility functions. */
UENUM()
enum class EItemRarity : uint8
{
    None,
    Common,
    Uncommon,
    Rare
};
```

```cpp
// ItemRarityLibrary.h
#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "ItemRarity.h"
#include "ItemRarityLibrary.generated.h"

/** Utility functions for EItemRarity enum. */
UCLASS()
class MYGAME_API UItemRarityLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    /** Returns the next higher rarity tier. */
    UFUNCTION(BlueprintCallable)
    static EItemRarity GetNextRarity(const EItemRarity Rarity);

    /** Returns the display name for a rarity tier. */
    UFUNCTION(BlueprintCallable)
    static FString GetRarityDisplayName(const EItemRarity Rarity);
};
```

---

## Complete Example

### Header (WeaponType.h)

```cpp
#pragma once

#include "WeaponType.generated.h"

/** Defines available weapon types in the game.
 *  See UWeaponTypeLibrary for utility functions. */
UENUM()
enum class EWeaponType : uint8
{
    None,
    Sword,
    Bow,
    Staff,
    Dagger
};
```

### Usage

```cpp
// Declaring a field
UPROPERTY(EditDefaultsOnly)
EWeaponType WeaponType = EWeaponType::None;

// Validity check
if (WeaponType != EWeaponType::None)
{
    // Valid weapon type
}

// Getting string representation
FString WeaponName = UEnum::GetValueAsString(
    TEXT("MyGame.EWeaponType"), WeaponType);
```

---

## Quick Reference

| # | Rule | Key Point |
|---|------|-----------|
| 1 | `UENUM()` macro | Mandatory, even for C++-only enums |
| 2 | Declaration | Always `enum class EName : uint8` (wider type only if >255 values) |
| 3 | None value | Mandatory first value for validity checks |
| 4 | No numeric values | Never assign explicit numbers to enum values |
| 5 | No MaxValue | Do not add `MaxValue` / `MAX` entry |
| 6 | Separate header | Move to own `.h` if used by multiple classes |
| 7 | State pattern | Consider refactoring state enums into State pattern classes |
| 8 | String conversion | `UEnum::GetValueAsString(TEXT("Module.EName"), Variable)` |
| 9 | Support functions | Create a separate `UBlueprintFunctionLibrary`; add reference in enum header |
