# Unreal Engine C++ Defensive Programming Rules

Rules for data validation and defensive programming in Unreal Engine C++ projects.
These rules apply globally to all UE projects.

**Required plugin:** `AssertUtils` must be connected to every project. If it is missing — report this immediately before proceeding with any code work.

**Reference:** "Code Complete" by Steve McConnell, Chapter "Defensive Programming", page 182.

---

## Philosophy

Defensive programming is a powerful tool that increases code writing time by only 1%-5%, while protecting against the majority of bugs and enabling higher quality code.

**Core principle:** All function parameters, pointers, references, and results of any actions (e.g., asset loading) must always be validated. If any deviation from the norm is detected, it is considered a serious error that must be highlighted via a breakpoint — through our internal asserts from the `AssertUtils` plugin.

**If an error is detected:** the code must handle it, report what the problem is, and exit the function to prevent further execution with broken data.

---

## 1. Validating Function Parameters (Incoming Data)

All function parameters must be checked for correctness.

### If parameters are invalid:

1. **Assert** — to signal the problem and break execution.
2. **Describe the error** — so logs make it easier to understand what went wrong (if the assert name alone is insufficient).
3. **Exit the function** — to:
   - Prevent the function from working with incorrect data.
   - Prevent potential editor crashes.

```cpp
void UMyClass::ProcessCharacter(const FGameplayTag& CharacterTag,
                                const float Multiplier)
{
    assertGameplayTagIsValid_return(CharacterTag);
    assertCondition_return(Multiplier > 0.0f, "Multiplier must be positive");

    // Safe to proceed — parameters are validated
    // ...
}
```

### If parameters can legitimately be set incorrectly (e.g., Game Designer has access):

1. **Check and log** the issue.
2. **Assert** — but only if this is **not called every frame or every second**.
3. **Clamp the data** to acceptable range after validation.

```cpp
void UMyClass::SetDifficulty(const float NewDifficulty)
{
    if (NewDifficulty < 0.0f || NewDifficulty > 1.0f)
    {
        UE_LOG(LogGame, Warning, TEXT("Difficulty value %.2f is out of [0, 1] range. Clamping."), NewDifficulty);
        // Assert only if not called frequently
        ensureMsgf(false, TEXT("Difficulty out of range: %f"), NewDifficulty);
    }

    Difficulty = FMath::Clamp(NewDifficulty, 0.0f, 1.0f);
}
```

---

## 2. Validating Variables Inside Functions (Data Obtained in Function Body)

### Pointers

All object pointers must be constantly checked for validity. If a pointer is invalid — throw an error via ensure (assert).

```cpp
void UMyClass::ActivateComponent()
{
    UActorComponent* Component = GetOwner()->FindComponentByClass<UMyComponent>();
    assertUObjectPointerIsValid_return(Component);

    Component->Activate();
}
```

### Value Ranges

If obtained values must be within a certain range — validate them and throw an error on deviation.

```cpp
void UMyClass::ApplyDamage(const float RawDamage)
{
    const float CalculatedDamage = CalculateFinalDamage(RawDamage);
    assertCondition_return(CalculatedDamage >= 0.0f, "Calculated damage is negative");

    Health -= CalculatedDamage;
}
```

---

## 3. Validation in Loops

### When execution can continue (partial failure)

If a loop iterates over data where some entries may be invalid but others can still work (e.g., processing buff effects that may have expired), error handling must **not** cause a full function exit. Instead:
- **Breakpoint** (assert) on the invalid entry.
- **Log the error.**
- **Continue** to the next iteration.

```cpp
void UMyClass::ProcessBuffs(const TArray<FBuffEntry>& Buffs)
{
    bool bAnyProcessed = false;

    for (const FBuffEntry& Buff : Buffs)
    {
        if (!Buff.IsSet())
        {
            ensureMsgf(false, TEXT("Invalid buff entry found in array. Skipping."));
            continue;
        }

        ApplyBuff(Buff);
        bAnyProcessed = true;
    }

    // If at least one should have been processed but none were — this is an error
    assertCondition_return(bAnyProcessed, "No valid buff entries found. At least one was expected.");
}
```

### When at least one result is mandatory

If iterating through data where at least one entry **must** succeed (e.g., finding at least one valid spawn point), and none is found — this is an error. Throw an assert and stop execution.

```cpp
const FSpawnPoint* UMyClass::FindAvailableSpawnPoint(const TArray<FSpawnPoint>& SpawnPoints)
{
    for (const FSpawnPoint& SpawnPoint : SpawnPoints)
    {
        if (SpawnPoint.bAvailable)
        {
            return &SpawnPoint;
        }
    }

    // None found — this should never happen
    ensureMsgf(false, TEXT("No available spawn point found. At least one must exist."));
    return nullptr;
}
```

---

## 4. Return Values on Error

When a function must return a value but an error occurred, return an appropriate default:

| Return type | Default on error |
|-------------|-----------------|
| Array index (`int32`) | `INDEX_NONE` |
| Object pointer | `nullptr` |
| Struct (by value) | Static `EmptyData` instance |
| Struct (by reference) | Static `EmptyData` instance |
| `TOptional<>` | Empty optional (unset) |

```cpp
int32 UMyClass::FindElementIndex(const FGameplayTag& SearchTag) const
{
    for (int32 i = 0; i < Elements.Num(); ++i)
    {
        if (Elements[i].Tag == SearchTag)
        {
            return i;
        }
    }
    return INDEX_NONE;
}

const FMyStruct& UMyClass::FindData(const FGameplayTag& Tag) const
{
    for (const FMyStruct& Data : DataArray)
    {
        if (Data.Tag == Tag)
        {
            return Data;
        }
    }

    ensureMsgf(false, TEXT("Data not found for tag: %s"), *Tag.ToString());
    return FMyStruct::EmptyData;
}
```

---

## 5. TOptional<>

`TOptional<>` is a powerful struct that explicitly signals that data may be compromised. Use it everywhere data might not be set:

| Use case | Example |
|----------|---------|
| Return values when function doesn't guarantee valid data | `TOptional<FMyData> FindData()` |
| Pointers to classes | `TOptional<UMyClass*>` |
| Pointers to structs (when copying is expensive or direct modification needed) | `TOptional<FMyStruct*>` — not references |
| Pointers to standard-type class fields (when direct modification needed) | `TOptional<float*>` — not references |
| Values (except array indices — use `INDEX_NONE` for those) | `TOptional<float>` |
| Class fields that have no value at instance startup | `TOptional<FGameplayTag> CachedTag;` |

```cpp
// Return value — function doesn't guarantee data exists
TOptional<FCharacterData> UMyClass::FindCharacterData(const FGameplayTag& Tag) const
{
    for (const FCharacterData& Data : Characters)
    {
        if (Data.CharacterTag == Tag)
        {
            return Data;
        }
    }
    return {};  // Empty optional
}

// Class field that has no value at startup
private:
    UPROPERTY()
    TOptional<FGameplayTag> ActiveAbilityTag;

// Checking
void UMyClass::UseAbility()
{
    assertCondition_return(ActiveAbilityTag.IsSet(), "ActiveAbilityTag was not set before UseAbility call");
    // Safe to use ActiveAbilityTag.GetValue()
}
```

---

## 6. Switch Default Branch

Always use the `default` branch in `switch` statements as an **error signal**. This is necessary to highlight when an enum value was missed during handling.

```cpp
switch (CurrentState)
{
    case EMyState::None:
        break;

    case EMyState::Active:
        ProcessActive();
        break;

    case EMyState::Paused:
        ProcessPaused();
        break;

    default:
        ensureMsgf(false, TEXT("Unhandled state: %s"),
            *UEnum::GetValueAsString(TEXT("MyModule.EMyState"), CurrentState));
        break;
}
```

---

## 7. Validation Code Formatting (Scope Rule)

### Single-line check — leave as-is

```cpp
assertUObjectPointerIsValid_return(SomePointer);
```

### Multi-line check — wrap in a scope block

If a validation takes more than one line, wrap it in an additional scope `{}`. This allows collapsing all validation blocks in the editor and focusing on the important logic.

```cpp
void UMyClass::ProcessData()
{
    // Single-line check — leave as-is
    assertUObjectPointerIsValid_return(OwnerActor);

    // Multi-line check — wrap in scope for collapsibility
    {
        if (!IsValid(SomePointer))
        {
            ResetState();
            DoSomethingElse();
            return;
        }
    }

    // Multi-line check — another example
    {
        if (DataArray.Num() == 0)
        {
            UE_LOG(LogGame, Error, TEXT("DataArray is empty in %s"), *GetName());
            ensureMsgf(false, TEXT("DataArray must not be empty"));
            return;
        }
    }

    // Actual logic starts here, with all validations collapsed above
    for (const FMyData& Data : DataArray)
    {
        // Process data...
    }
}
```

---

## Quick Reference

| # | Rule | Key Point |
|---|------|-----------|
| 1 | Function params | Always validate; assert + describe error + return |
| 2 | GD-accessible params | Log + assert (if not per-frame) + `FMath::Clamp` |
| 3 | Pointers in body | Always check validity; assert on failure |
| 4 | Value ranges | Validate expected ranges; assert on deviation |
| 5 | Loops (partial fail) | Assert + log + `continue`; don't exit function |
| 6 | Loops (must find one) | Assert + exit if nothing found |
| 7 | Return on error | `INDEX_NONE`, `nullptr`, `EmptyData`, empty `TOptional` |
| 8 | `TOptional<>` | Use for any data that may not be set |
| 9 | Switch default | Always an error signal for unhandled enum values |
| 10 | Scope rule | 1-line check: as-is; multi-line: wrap in `{}` for collapsibility |
| 11 | **AssertUtils plugin** | **Must be present in every project; report if missing** |
