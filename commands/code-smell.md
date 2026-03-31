# /code-smell - Detect Code Smells

## Scope
Identify maintainability issues and anti-patterns.

## Smell Categories

### Structural
- **God class/function**: >200 lines class, >50 lines function
- **Feature envy**: Method uses another class's data more than its own
- **Data clump**: Same group of fields appears in multiple places
- **Primitive obsession**: Using primitives where value objects fit

### Behavioral
- **Long parameter list**: >4 parameters
- **Switch/if chains**: >3 branches on same type
- **Temporal coupling**: Methods must be called in specific order
- **Boolean blindness**: Boolean params that hide meaning

### Dependency
- **Circular dependencies**: A → B → A
- **Inappropriate intimacy**: Classes know too much about each other
- **Shotgun surgery**: One change requires editing many classes

## Rules
- Focus on the most impactful smells first
- Suggest specific refactoring for each (extract method, introduce parameter object, etc.)
- Don't flag things that are intentional trade-offs
- Consider project context (prototype vs production)

## Output

```
## Code Smells: [scope]

**High Impact** (N)
- [smell] at file:line — [why it matters] → [refactoring suggestion]

**Medium Impact** (N)
- [smell] at file:line → [suggestion]

**Low Impact** (N)
- [smell] at file:line
```
