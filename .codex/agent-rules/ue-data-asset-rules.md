# Unreal Engine C++ DataAsset Creation Rules

Rules for declaring and implementing classes inheriting from `UDataAsset` in Unreal Engine C++ projects.
These rules apply globally to all UE projects.

---

## Philosophy

DataAssets should be treated as **a set of parameters and references to objects/classes for loading that can be swapped out**. For example, weapon configurations for different character classes, or NPC dialogue settings for different quest lines.

DataAssets are configuration containers — they hold data, not logic.

---

## 1. Class Naming

The class name must always end with **`DataAsset`**.

```cpp
// CORRECT
class UWeaponDataAsset : public UDataAsset { ... };
class UCharacterStatsDataAsset : public UDataAsset { ... };
class UDialogueSettingsDataAsset : public UDataAsset { ... };

// WRONG - missing DataAsset suffix
class UWeaponConfig : public UDataAsset { ... };
class UCharacterStats : public UDataAsset { ... };
```

---

## 2. UCLASS Macro

The `UCLASS()` macro is **mandatory**.

```cpp
UCLASS()
class MYGAME_API UMyDataAsset : public UDataAsset
{
    GENERATED_BODY()
    // ...
};
```

---

## 3. Field Access Level

All fields must always be **private**. Blueprint access must be no higher than `EditDefaultsOnly`.

```cpp
// CORRECT
private:
    UPROPERTY(EditDefaultsOnly, Category = "Loot Settings")
    float DropRate = 0.5f;

// WRONG - public field
public:
    UPROPERTY(EditDefaultsOnly)
    float DropRate = 0.5f;

// WRONG - Blueprint read access
private:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly)
    float DropRate = 0.5f;
```

---

## 4. Pointer Types

### Assets & Blueprints: TSoftObjectPtr

Pointers to assets and Blueprints must be **`TSoftObjectPtr`**. Assets must only be loaded when they are actually used (lazy loading).

```cpp
private:
    UPROPERTY(EditDefaultsOnly, Category = "Visuals")
    TSoftObjectPtr<UTexture2D> IconTexture = nullptr;

    UPROPERTY(EditDefaultsOnly, Category = "Visuals")
    TSoftObjectPtr<UStaticMesh> PreviewMesh = nullptr;

    UPROPERTY(EditDefaultsOnly, Category = "Audio")
    TSoftObjectPtr<USoundBase> HitSound = nullptr;
```

### Other DataAssets: TObjectPtr

Pointers to other DataAssets must be **`TObjectPtr`**. This ensures that all required DataAssets with their data are loaded immediately, without pulling in heavy assets.

```cpp
private:
    UPROPERTY(EditDefaultsOnly, Category = "References")
    TObjectPtr<UWeaponDataAsset> WeaponData = nullptr;

    UPROPERTY(EditDefaultsOnly, Category = "References")
    TObjectPtr<UCharacterStatsDataAsset> StatsData = nullptr;
```

### Summary Table

| What is referenced | Pointer type | Why |
|--------------------|-------------|-----|
| Assets (textures, meshes, sounds, etc.) | `TSoftObjectPtr` | Lazy loading — load only when needed |
| Blueprints | `TSoftObjectPtr` | Lazy loading — load only when needed |
| Other DataAssets | `TObjectPtr` | Immediate loading of all DA data, without heavy assets |

---

## 5. TArray with TitleProperty

All `TArray` fields containing structs must have the `meta = (TitleProperty = "FieldName")` setting, so that array elements can be distinguished from each other by name in the editor.

`FieldName` must refer to a field inside the struct that serves as a human-readable identifier.

```cpp
private:
    UPROPERTY(EditDefaultsOnly, Category = "Abilities", meta = (TitleProperty = "AbilityName"))
    TArray<FAbilityEntry> Abilities;

    UPROPERTY(EditDefaultsOnly, Category = "Loot", meta = (TitleProperty = "ItemName"))
    TArray<FLootTableEntry> LootTable;
```

Without `TitleProperty`, array elements in the editor show as generic "Element 0", "Element 1", etc. — making it difficult to distinguish them.

---

## 6. Getter Functions

Getter functions must always have the **`UFUNCTION(BlueprintPure)`** macro for Blueprint access.

**Note:** `UFUNCTION(BlueprintPure)` can be used on getters in any class, but it is **mandatory** specifically for DataAsset getters.

```cpp
public:
    /** Returns the critical hit chance. */
    UFUNCTION(BlueprintPure)
    float GetCriticalHitChance() const;

    /** Returns the icon texture soft reference. */
    UFUNCTION(BlueprintPure)
    TSoftObjectPtr<UTexture2D> GetIconTexture() const;

    /** Returns the weapon data asset. */
    UFUNCTION(BlueprintPure)
    UWeaponDataAsset* GetWeaponData() const;
```

---

## 7. Public Interface

The public interface section may contain not only getters, but also **utility functions**: searching arrays, filtering data, validation, etc.

```cpp
public:
    /** Returns the ability matching the given tag. */
    UFUNCTION(BlueprintPure)
    const FAbilityEntry& FindAbilityByTag(const FGameplayTag& SearchTag) const;

    /** Returns all abilities matching the filter tags. */
    UFUNCTION(BlueprintPure)
    TArray<FAbilityEntry> GetFilteredAbilities(const FGameplayTagContainer& FilterTags) const;
```

---

## Complete Example

### Header (CharacterArchetypeDataAsset.h)

```cpp
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "GameplayTagContainer.h"
#include "ArchetypeAbility.h"
#include "CharacterArchetypeDataAsset.generated.h"

/** Forward Declarations */
class UAbilitySetDataAsset;

/** Holds configurable parameters for a character archetype.
 *  Used to swap character settings (stats, visuals, abilities)
 *  without modifying game logic. */
UCLASS()
class MYGAME_API UCharacterArchetypeDataAsset : public UDataAsset
{
    GENERATED_BODY()

// ============================================================
// Class Fields
// ============================================================
private:
    UPROPERTY(EditDefaultsOnly, Category = "General")
    FGameplayTag ArchetypeTag;

    UPROPERTY(EditDefaultsOnly, Category = "Stats")
    int32 MaxHealth = 100;

    UPROPERTY(EditDefaultsOnly, Category = "Stats")
    float MovementSpeed = 600.0f;

    UPROPERTY(EditDefaultsOnly, Category = "Visuals")
    TSoftObjectPtr<UTexture2D> PortraitIcon = nullptr;

    UPROPERTY(EditDefaultsOnly, Category = "Visuals")
    TSoftObjectPtr<USkeletalMesh> CharacterMesh = nullptr;

    UPROPERTY(EditDefaultsOnly, Category = "References")
    TObjectPtr<UAbilitySetDataAsset> AbilitySetData = nullptr;

    UPROPERTY(EditDefaultsOnly, Category = "Abilities", meta = (TitleProperty = "AbilityName"))
    TArray<FArchetypeAbility> Abilities;

// ============================================================
// Public Interface
// ============================================================
public:
    /** Returns the archetype gameplay tag. */
    UFUNCTION(BlueprintPure)
    const FGameplayTag& GetArchetypeTag() const;

    /** Returns the maximum health for this archetype. */
    UFUNCTION(BlueprintPure)
    int32 GetMaxHealth() const;

    /** Returns the movement speed. */
    UFUNCTION(BlueprintPure)
    float GetMovementSpeed() const;

    /** Returns the portrait icon soft reference. */
    UFUNCTION(BlueprintPure)
    TSoftObjectPtr<UTexture2D> GetPortraitIcon() const;

    /** Returns the ability set data asset. */
    UFUNCTION(BlueprintPure)
    UAbilitySetDataAsset* GetAbilitySetData() const;

    /**
     * Finds an ability by its gameplay tag.
     * @param SearchTag The tag to search for.
     */
    UFUNCTION(BlueprintPure)
    const FArchetypeAbility& FindAbilityByTag(const FGameplayTag& SearchTag) const;
};
```

### Implementation (CharacterArchetypeDataAsset.cpp)

```cpp
#include "CharacterArchetypeDataAsset.h"

const FGameplayTag& UCharacterArchetypeDataAsset::GetArchetypeTag() const
{
    return ArchetypeTag;
}

int32 UCharacterArchetypeDataAsset::GetMaxHealth() const
{
    return MaxHealth;
}

float UCharacterArchetypeDataAsset::GetMovementSpeed() const
{
    return MovementSpeed;
}

TSoftObjectPtr<UTexture2D> UCharacterArchetypeDataAsset::GetPortraitIcon() const
{
    return PortraitIcon;
}

UAbilitySetDataAsset* UCharacterArchetypeDataAsset::GetAbilitySetData() const
{
    return AbilitySetData;
}

const FArchetypeAbility& UCharacterArchetypeDataAsset::FindAbilityByTag(const FGameplayTag& SearchTag) const
{
    for (const FArchetypeAbility& Ability : Abilities)
    {
        if (Ability.AbilityTag == SearchTag)
        {
            return Ability;
        }
    }
    return FArchetypeAbility::EmptyData;
}
```

---

## Quick Reference

| # | Rule | Key Point |
|---|------|-----------|
| 1 | Class naming | Must end with `DataAsset` |
| 2 | `UCLASS()` | Mandatory macro |
| 3 | Field access | Always `private`, max `EditDefaultsOnly` for BP |
| 4 | Asset pointers | `TSoftObjectPtr` — lazy loading |
| 5 | DataAsset pointers | `TObjectPtr` — immediate loading without heavy assets |
| 6 | TArray structs | Always `meta = (TitleProperty = "FieldName")` |
| 7 | Getters | Always `UFUNCTION(BlueprintPure)` |
| 8 | Public interface | Getters + utility functions (search, filter, validate) |
