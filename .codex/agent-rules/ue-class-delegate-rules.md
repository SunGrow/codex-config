# Unreal Engine C++ Class Delegate Rules

Rules for declaring and using delegates in Unreal Engine C++ classes.
These rules apply globally to all UE projects.

---

## 1. Purpose of Delegates

Delegates allow avoiding additional coupling with other classes that want to execute logic when a certain event occurs. The goal of a delegate is to **maximize abstraction** of the class functionality.

For example, in a score system we don't need to know anything about a widget, or about any other systems that want to know about score changes — we simply add a delegate, and the system remains independent.

```
Score System                    Widget / UI / Other Systems
┌──────────────┐               ┌──────────────────────────┐
│              │  OnScoreChanged│                          │
│  Score Logic ├──────────────►│  Subscribes to delegate  │
│              │   (delegate)  │  Updates UI on callback  │
└──────────────┘               └──────────────────────────┘

The Score System knows nothing about who listens.
```

---

## 2. Delegate Type

Delegates must always be **Dynamic Multicast**, because:
- They may be needed in Blueprints (Dynamic)
- They must allow more than one object to subscribe (Multicast)

```cpp
/** Delegate Declarations */
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnInitializationCompleted);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnScoreChanged, const int32, NewScore);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChanged, const float, NewHealth, const float, OldHealth);
```

---

## 3. Delegate Naming

The delegate name must define **after which event** it will be called. The name always starts with `On` followed by the completed event description.

```cpp
// CORRECT - clearly states the event that occurred
FOnInitializationCompleted      // Fired after initialization completed
FOnActorDestroyed               // Fired after an actor was destroyed
FOnScoreChanged                 // Fired after the score changed
FOnProductionStageFinished      // Fired after a production stage finished
FOnCharacterCreated             // Fired after a character was created

// WRONG - unclear when this fires, or not event-based
FScoreDelegate                  // What event triggers this?
FUpdateWidget                   // This is an action, not an event
FHealthCallback                 // Vague, doesn't describe the event
```

---

## 4. Access Level

Delegates are always **public**, as they are part of the class interface. External systems subscribe to them to react to events.

```cpp
/** Delegates section */
public:
    UPROPERTY(BlueprintAssignable)
    FOnInitializationCompleted OnInitializationCompleted;

    UPROPERTY(BlueprintAssignable)
    FOnScoreChanged OnScoreChanged;
```

---

## 5. UPROPERTY Specifier

Delegate fields must be marked with `UPROPERTY(BlueprintAssignable)` to allow Blueprint subscription.

```cpp
// CORRECT
UPROPERTY(BlueprintAssignable)
FOnScoreChanged OnScoreChanged;

// WRONG - not accessible from Blueprints
FOnScoreChanged OnScoreChanged;
```

---

## 6. Complete Example

```cpp
#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "ScoreSystem.generated.h"

/** Delegate Declarations */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnScoreChanged, const int32, NewScore);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnScoreReset);

/** Manages score tracking independently from any UI or display systems.
 *  Uses delegates to notify subscribers about score changes
 *  without knowing anything about them. */
UCLASS()
class MYGAME_API UScoreSystem : public UObject
{
    GENERATED_BODY()

// ============================================================
// Class Fields
// ============================================================
private:
    UPROPERTY()
    int32 CurrentScore = 0;

    UPROPERTY(EditDefaultsOnly)
    int32 MaxScore = 9999;

// ============================================================
// Delegates
// ============================================================
public:
    UPROPERTY(BlueprintAssignable)
    FOnScoreChanged OnScoreChanged;

    UPROPERTY(BlueprintAssignable)
    FOnScoreReset OnScoreReset;

// ============================================================
// Public Interface
// ============================================================
public:
    /**
     * Adds points to the current score.
     * @param Points Amount of points to add.
     */
    void AddScore(const int32 Points);

    /**
     * Resets the score to zero.
     */
    void ResetScore();
};
```

```cpp
// ScoreSystem.cpp
#include "ScoreSystem.h"

void UScoreSystem::AddScore(const int32 Points)
{
    CurrentScore = FMath::Clamp(CurrentScore + Points, 0, MaxScore);
    OnScoreChanged.Broadcast(CurrentScore);
}

void UScoreSystem::ResetScore()
{
    CurrentScore = 0;
    OnScoreReset.Broadcast();
}
```

---

## Quick Reference

| Rule | Key Point |
|------|-----------|
| Purpose | Decouple systems; class knows nothing about subscribers |
| Type | Always `DECLARE_DYNAMIC_MULTICAST_DELEGATE` |
| Naming | `On` + event description (e.g., `OnScoreChanged`) |
| Access | Always `public` |
| UPROPERTY | Always `BlueprintAssignable` |
