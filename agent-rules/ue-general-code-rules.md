# Unreal Engine C++ General Code Rules

General coding rules and best practices for working with code in Unreal Engine C++ projects.
These rules apply globally to all UE projects.

---

## 1. Conditions & Comparisons

### Extract complex conditions into named bools

If a condition consists of multiple complex comparisons, extract each comparison into a `bool` variable with a name reflecting its meaning. Conditions are not about comparing two numbers — they are about checking a **state**. What matters is the context behind the comparison.

```cpp
// WRONG - hard to read, context is unclear
if (0 < Value)

// CORRECT - context is clear, readable
const bool bValuePositive = 0 < Value;
if (bValuePositive)
```

```cpp
// WRONG - complex condition is hard to parse
if (Character->GetHealth() > 0.0f && Character->GetStamina() > MinStamina && !Character->HasCondition(ECondition::Stunned))

// CORRECT - each condition is named and clear
const bool bAlive = 0.0f < Character->GetHealth();
const bool bEnoughStamina = MinStamina < Character->GetStamina();
const bool bNotStunned = !Character->HasCondition(ECondition::Stunned);

if (bAlive && bEnoughStamina && bNotStunned)
```

### Comparison operator direction

Only use the `<` (less-than) comparison operator pointing **right**. This way values in conditions always go from smaller to larger, making it much clearer what range is being checked on the number line.

```cpp
// CORRECT - values go from smaller to larger (left to right)
if (0.0f < Value)
if (MinValue < CurrentValue)
if (MinRange < Value && Value < MaxRange)

// WRONG - greater-than operator, harder to read ranges
if (Value > 0.0f)
if (CurrentValue > MinValue)
if (Value > MinRange && Value < MaxRange)  // Inconsistent direction
```

**Note:** This rule applies only to ordering comparisons (`<`, `<=`). Equality comparisons (`==`, `!=`) are not affected and follow normal style (e.g., `Pointer == nullptr`, not `nullptr == Pointer`).

---

## 2. Factory Methods

### Naming

All classes created at runtime must have a static factory method:
- **`NewObject_[ClassName]`** — for classes inheriting from `UObject`
- **`NewActor_[ClassName]`** — for classes inheriting from `AActor`

Factory method names must be unique so they can be exposed to Blueprints.

### Purpose

Factory methods hide object initialization inside, eliminating the need to call additional setup functions after creating an instance.

### When NOT required

- Components created in the class constructor — no factory method needed.
- Classes used as `Instanced` in properties — no factory method needed.

### Actor Factory Method with SpawnActorDeferred

If an Actor needs additional parameter initialization, use `SpawnActorDeferred` inside the factory method:

```cpp
ASomeActor* ASomeActor::NewActor_SomeActor(UObject* WorldContextObject,
                                           const float SomeValue)
{
    // Validate incoming parameters
    assertUObjectPointerIsValid_return_value(WorldContextObject, nullptr);

    UWorld* GameWorld = WorldContextObject->GetWorld();
    assertUObjectPointerIsValid_return_value(GameWorld, nullptr);

    // Spawn the actor via SpawnActorDeferred — does not fully initialize
    // the actor and does not trigger BeginPlay() yet
    ASomeActor* NewSomeActor = GameWorld->SpawnActorDeferred<ASomeActor>(
        ASomeActor::StaticClass(), FTransform::Identity);
    assertUObjectPointerIsValid_return_value(NewSomeActor, nullptr);

    // Initialize the required data
    NewSomeActor->SetSomeValue(SomeValue);

    // Complete actor initialization — mandatory step.
    // If initialization is not finished, the actor will not work correctly.
    NewSomeActor->FinishSpawning(FTransform::Identity);

    return NewSomeActor;
}
```

### UObject Factory Method

```cpp
UMyObject* UMyObject::NewObject_MyObject(UObject* Outer,
                                         const FGameplayTag& ObjectTag)
{
    assertUObjectPointerIsValid_return_value(Outer, nullptr);
    assertGameplayTagIsValid_return_value(ObjectTag, nullptr);

    UMyObject* NewObj = NewObject<UMyObject>(Outer);
    assertUObjectPointerIsValid_return_value(NewObj, nullptr);

    NewObj->Initialize(ObjectTag);

    return NewObj;
}
```

---

## 3. Clean Code Practices

### Const local variables

If a variable is not modified after declaration and is initialized at the point of declaration, it **must** be `const`.

```cpp
// CORRECT
const float FinalDamage = BaseDamage * Multiplier;
const FGameplayTag& CharacterTag = Character->GetTag();

// WRONG - value never changes but not marked const
float FinalDamage = BaseDamage * Multiplier;
```

### No while loops

**Never** use `while` or any other loop based on a boolean condition. Such loops can fall into infinite loops if data validation fails. Use **only `for` loops**.

**This is an absolute rule with no exceptions.** If the logic seems to require `while`, restructure it to use a bounded `for` loop instead.

```cpp
// WRONG - can become infinite if condition never changes
while (bProcessing)
{
    ProcessNextItem();
}

// CORRECT - bounded iteration
for (int32 i = 0; i < Items.Num(); ++i)
{
    ProcessItem(Items[i]);
}
```

### Minimize hardcoded values

Minimize all hardcoded values. Use our macro library (and extend it as needed).

```cpp
// WRONG
if (Health < 0.001f)

// CORRECT - use named constants or macros
constexpr float HEALTH_EPSILON = 0.001f;
if (Health < HEALTH_EPSILON)
```

### Static utility functions in FunctionLibrary

All static helper functions that do not belong to a specific class **must** be declared in classes inheriting from `UBlueprintFunctionLibrary`.

```cpp
UCLASS()
class MYGAME_API UMathUtilsLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable)
    static float CalculateArcTrajectory(const FVector& Start,
                                        const FVector& End,
                                        const float ArcHeight);
};
```

### Complex formula documentation

If a complex formula or algorithm is used, the comment must describe it in maximum detail.
- If a wiki link exists — attach it.
- If there is a Confluence page with graphs/diagrams — even better.

```cpp
/**
 * Calculates the ballistic trajectory angle using the projectile motion formula.
 *
 * Formula: angle = arctan((v^2 +/- sqrt(v^4 - g*(g*x^2 + 2*y*v^2))) / (g*x))
 *
 * Where:
 *   v = initial velocity
 *   g = gravity acceleration
 *   x = horizontal distance
 *   y = vertical distance
 *
 * Reference: https://en.wikipedia.org/wiki/Projectile_motion
 * Confluence: https://myteam.atlassian.net/wiki/spaces/GAME/pages/12345
 */
static float CalculateBallisticAngle(const float Velocity,
                                     const float Distance,
                                     const float HeightDiff);
```

### Logging

Use `UE_LOG()` for logging. Avoid printing logs to the screen, as it clutters the viewport and makes it unclear what is being displayed, by whom, and for what purpose.

```cpp
// CORRECT
UE_LOG(LogGame, Warning, TEXT("Character %s failed to find target"), *CharacterName);

// WRONG - clutters the screen
GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Red, TEXT("Error!"));
```

---

## 4. Naming Conventions

### Delta

The word "Delta" is used in physics in two meanings: remaining distance to the endpoint, and step per one cycle. Code requires unambiguous precision:

- **Delta** — use **only** in the context of a step per one cycle (e.g., `DeltaTime`, `DeltaProgress`).
- **Remaining** — use for the remaining distance to the endpoint (e.g., `RemainingDistance`, `RemainingHealth`).

```cpp
// CORRECT
void Tick(const float DeltaTime);              // Step per frame
float RemainingDistance = Target - Current;     // Distance left

// WRONG - ambiguous use of Delta
float DeltaDistance = Target - Current;         // Should be RemainingDistance
```

### Set vs Change

**Set** — used for assigning a new value to a class field. Simple value assignment.

**Change** — used for switching entity states. Includes:
- Validation checks for correct state transitions.
- Launching additional functions and configuring parameters for the transition.

```cpp
// Set — simple value assignment
void SetSpeed(const float NewSpeed) { Speed = NewSpeed; }
void SetName(const FString& NewName) { Name = NewName; }

// Change — state transition with validation and side effects
void ChangeState(const ECharacterState NewState)
{
    assertCondition_return(NewState != ECharacterState::None, "Cannot change to None state");
    assertCondition_return(NewState != CurrentState, "Already in this state");

    // Validate transition is allowed
    {
        const bool bTransitionAllowed = IsTransitionValid(CurrentState, NewState);
        assertCondition_return(bTransitionAllowed, "Invalid state transition");
    }

    // Exit current state
    OnStateExit(CurrentState);

    // Switch state
    const ECharacterState PreviousState = CurrentState;
    CurrentState = NewState;

    // Enter new state
    OnStateEnter(NewState, PreviousState);
}
```

---

## Quick Reference

| # | Rule | Key Point |
|---|------|-----------|
| 1 | Complex conditions | Extract into named `bool` variables for readability |
| 2 | Comparison direction | Always `<` (less-than) for ordering; values go small-to-large. Does not apply to `==`/`!=` |
| 3 | Factory: UObject | `NewObject_[ClassName]` static method |
| 4 | Factory: AActor | `NewActor_[ClassName]` with `SpawnActorDeferred` + `FinishSpawning` |
| 5 | Factory: not needed | Components in constructor; Instanced property classes |
| 6 | Const locals | If not modified after init — must be `const` |
| 7 | No while loops | **Absolute rule, no exceptions.** Only `for` loops; restructure logic if needed |
| 8 | No hardcoded values | Use named constants / macro library |
| 9 | Static helpers | Must be in `UBlueprintFunctionLibrary` subclasses |
| 10 | Complex formulas | Detailed comments + wiki/Confluence links |
| 11 | Logging | `UE_LOG()` only; no on-screen debug messages |
| 12 | Delta | Only for step-per-cycle; use Remaining for distance left |
| 13 | Set vs Change | Set = assign value; Change = state transition with validation |
