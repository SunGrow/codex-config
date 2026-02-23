# Unreal Engine C++ Class Creation Rules

Standard coding rules for creating new C++ classes in Unreal Engine projects.
These rules apply globally to all UE projects.

---

## 1. Header Comment Format

- All comments in `.h` files **must** use the `/** */` format.
- `//` comments are only used in `.cpp` files.

```cpp
/** This is the correct comment format for header files.
 *  Multi-line comments continue with an asterisk. */
```

---

## 2. Include Order

Includes in the header file must follow this order:

```cpp
/** Standard and additional Epic Games includes */
#include "CoreMinimal.h"
#include "GameplayTagContainer.h"

/** Project includes */
#include "MyOtherClass.h"

/** Generated header - always last */
#include "MyClass.generated.h"
```

---

## 3. Forward Declarations

```cpp
/** Forward Declarations */
class ASomeActor;
class USomeComponent;
```

---

## 4. Delegate Declarations

```cpp
/** Delegate Declarations */
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FSimpleClassDelegate);
```

---

## 5. Helper Enumerations

```cpp
/** Helper Enumerations */
UENUM(BlueprintType)
enum class EMyEnum : uint8
{
    None,
    OptionA,
    OptionB
};
```

---

## 6. Helper Structs

All function implementations must be in the `.cpp` file, **except templates**.

```cpp
/** Helper Structs */
USTRUCT(BlueprintType)
struct FMyStruct
{
    GENERATED_BODY()

    void SomeFunction(); // Implementation in .cpp
};
```

---

## 7. Class Declaration

All function implementations must be in the `.cpp` file, **except templates**.

### Class Structure (in order):

```cpp
/** Describes the purpose and essence of the class.
 *  Why does this class exist?
 *  What is its main goal?
 *  How does it work? */
UCLASS()
class MODULEMACROS_API UMyClass : public UObject
{
    GENERATED_BODY()

// ============================================================
// Debug Section
// ============================================================
/** Debug functions and data section.
 *  All debug functions and fields must have the DEBUG_ prefix.
 *  The entire section must be wrapped in WITH_EDITOR. */
#if WITH_EDITOR
public:
    void DEBUG_SomeFunction();
    void DEBUG_AnotherFunction();
    float DEBUG_Value;
#endif

// ============================================================
// Overridden Functions & Constructors
// ============================================================
/** Overridden functions from the parent class and constructors.
 *  Access level is determined by necessity or mirrors the parent class. */

/** Private overrides first */
private:
    virtual void SomeFunction() override;

/** Then public overrides and constructors */
public:
    virtual void SomeFunction2() override;
    UMyClass();

// ============================================================
// Class Fields
// ============================================================
/** Class fields section.
 *  - Fields may have EditDefaultsOnly or EditInstanceOnly access
 *    (depending on the class usage type) for easy configuration.
 *  - Fields must NOT be readable or writable from Blueprint code,
 *    as this violates encapsulation.
 *  - All fields must be UPROPERTY(). This ensures data serialization,
 *    reflection access, and the ability to apply additional property settings.
 *  - Leave a blank line after each field to prevent them from blending
 *    into a wall of text. */
private:
    UPROPERTY(EditDefaultsOnly)
    FGameplayTag ClassTag;

    /** Always use TObjectPtr for pointer fields that are class members. */
    UPROPERTY()
    TObjectPtr<AActor> SomeActorPointer = nullptr;

    UPROPERTY()
    EMyEnum EnumVariable = EMyEnum::None;

// ============================================================
// Delegates
// ============================================================
/** Class delegates section always in public. */
public:
    UPROPERTY(BlueprintAssignable)
    FSimpleClassDelegate OnDelegateCalled;

// ============================================================
// Private Functions
// ============================================================
/** Private functions section. */
private:
    void Foo();

// ============================================================
// Public Interface
// ============================================================
/** Public interface section (public class functions).
 *  Placed last so you can scroll to the bottom of the file
 *  and immediately see the class interface.
 *  All public interface functions must have doc-string comments. */
public:
    /**
     * Starts playing music.
     */
    void PlayMusic();

    /**
     * Returns the object velocity.
     * @param bSomeBoolValue Some example bool parameter.
     * @param SomeTag Some example gameplay tag.
     */
    virtual void GetVelocity(const bool bSomeBoolValue, const FGameplayTag& SomeTag);
};
```

---

## 8. Function Parameter Formatting

If a function has **more than 2 parameters**, all parameters must be written in a column, aligned under the first parameter. This rule applies to **both `.h` and `.cpp` files**.

### Header example:
```cpp
    /**
     * Returns some data.
     * @param bSomeBoolValue Some example bool parameter.
     * @param SomeTag Some example gameplay tag.
     * @param SomeFloat Some example float parameter.
     */
    virtual void GetSomeData(const bool bSomeBoolValue,
                             const FGameplayTag& SomeTag,
                             const float SomeFloat);
```

### Implementation example (.cpp):
```cpp
void UMyClass::GetSomeData(const bool bSomeBoolValue,
                           const FGameplayTag& SomeTag,
                           const float SomeFloat)
{
    // Implementation
}
```

---

## Quick Reference Summary

| # | Rule | Key Point |
|---|------|-----------|
| 1 | Header comments | `/** */` only in `.h`; `//` only in `.cpp` |
| 2 | Include order | Epic includes -> Project includes -> `.generated.h` |
| 3 | Forward declarations | After includes, before delegates |
| 4 | Delegate declarations | After forward declarations |
| 5 | Helper enumerations | After delegates |
| 6 | Helper structs | After enums; implementations in `.cpp` |
| 7 | Class declaration | Debug -> Overrides -> Fields -> Delegates -> Private -> Public |
| 8 | Parameter formatting | >2 params -> column-aligned under first param |

### Field Rules
- All fields: `UPROPERTY()`
- Access: `EditDefaultsOnly` or `EditInstanceOnly` (never Blueprint read/write)
- Pointers: Always `TObjectPtr<T>`
- Spacing: Blank line between each field
- All implementations in `.cpp` (except templates)
