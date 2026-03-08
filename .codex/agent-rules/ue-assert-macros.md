# AssertUtils Macros Reference

Source: `Plugins/AssertUtils/Source/AssertUtils/Assert.h`
Include: `#include "AssertUtils/Assert.h"`

## Naming Convention

`assert<CheckName>_<behavior>(args...)`

## Behaviors (suffixes)

| Suffix | Effect |
|--------|--------|
| `_return(args..., optionalReturnValue)` | Logs + returns from function. `_return()` for void, `_return(value)` for non-void |
| `_ignore(args...)` | Logs only, execution continues |
| `_withBreak(args...)` | Logs + `break` (use inside loops) |
| `_withContinue(args...)` | Logs + `continue` (use inside loops) |

## All Available Check Names

### Flow Control
| Macro | Args | Checks |
|-------|------|--------|
| `assertNeverReached` | (none) | Unconditional fail — code path should never execute |
| `assertDefaultImplementationIsOverriden` | (none) | Base implementation should be overridden |

### Pointers & Objects
| Macro | Args | Checks |
|-------|------|--------|
| `assertUObjectPointerIsValid` | `(pointer)` | UObject* is non-null and not pending kill |
| `assertUObjectPointerIsNotValid` | `(pointer)` | UObject* IS null or pending kill |
| `assertSmartPointerIsValid` | `(smartPointer)` | TSharedPtr/TWeakPtr is valid |
| `assertSmartPointerIsNotValid` | `(smartPointer)` | TSharedPtr/TWeakPtr is NOT valid |
| `assertSoftPointerIsValid` | `(softPointer)` | TSoftObjectPtr is valid |
| `assertSoftPointerIsNotValid` | `(softPointer)` | TSoftObjectPtr is NOT valid |
| `assertIsNull` | `(rawPointer)` | Raw pointer IS null |
| `assertIsNotNull` | `(rawPointer)` | Raw pointer is NOT null |

### Interfaces
| Macro | Args | Checks |
|-------|------|--------|
| `assertScriptInterfaceIsValid` | `(scriptInterface)` | TScriptInterface is valid |
| `assertScriptInterfaceIsNotValid` | `(scriptInterface)` | TScriptInterface is NOT valid |
| `assertUnrealInterfaceIsImplemented` | `(uObject, TInterface)` | UObject implements UInterface |
| `assertNativeInterfaceIsImplemented` | `(uObject, TInterface)` | UObject implements native C++ interface |

### Custom Structs & Optionals
| Macro | Args | Checks |
|-------|------|--------|
| `assertCustomStructIsSet` | `(CustomStruct)` | Struct's `IsSet()` returns true |
| `assertOptionalHasValue` | `(optional)` | TOptional has a value |
| `assertOptionalHasNoValue` | `(optional)` | TOptional does NOT have a value |

### Strings & Names
| Macro | Args | Checks |
|-------|------|--------|
| `assertStringIsEmpty` | `(value)` | FString IS empty |
| `assertStringIsNotEmpty` | `(value)` | FString is NOT empty |
| `assertNameIsAssigned` | `(value)` | FName is not NAME_None |
| `assertGameplayTagIsValid` | `(value)` | FGameplayTag is valid (not empty) |

### Comparisons (two values)
| Macro | Args | Checks |
|-------|------|--------|
| `assertIsEqual` | `(left, right)` | left == right |
| `assertIsNotEqual` | `(left, right)` | left != right |
| `assertIsGreater` | `(left, right)` | left > right |
| `assertIsGreaterOrEqual` | `(left, right)` | left >= right |
| `assertIsLess` | `(left, right)` | left < right |
| `assertIsLessOrEqual` | `(left, right)` | left <= right |

### Boolean
| Macro | Args | Checks |
|-------|------|--------|
| `assertIsTrue` | `(value)` | value is true |
| `assertIsFalse` | `(value)` | value is false |

### Containers
| Macro | Args | Checks |
|-------|------|--------|
| `assertIndexIsInArrayBounds` | `(index, arr)` | Index within array bounds |
| `assertContainerContainsElement` | `(container, element)` | Container has element |
| `assertContainerDoesNotContainElement` | `(container, element)` | Container lacks element |
| `assertContainerIsNotEmpty` | `(container)` | Container has elements |
| `assertContainerIsEmpty` | `(container)` | Container is empty |

### Networking / Authority
| Macro | Args | Checks |
|-------|------|--------|
| `assertHasAuthority` | `(actor)` | Actor has network authority |
| `assertIsLocallyControlled` | `(pawn)` | Pawn is locally controlled |
| `assertIsLocalController` | `(controller)` | Controller is local |

### Data Tables & AI
| Macro | Args | Checks |
|-------|------|--------|
| `assertDataTableRowIsFound` | `(dataTable, row, rowName)` | DataTable row exists |
| `assertBlackboardKeyIsValid` | `(blackboard, keyName)` | Blackboard key is valid |

## Common Mistakes
- **`assertCondition_return` DOES NOT EXIST** — use `assertIsTrue_return(boolExpr)` instead
- There is NO generic "condition" macro — always pick a specific check name from the list above
