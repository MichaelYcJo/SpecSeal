# /react-best-practices - React Performance & Patterns

## Component Design

### State Management
- Lift state only as high as needed
- Use appropriate tool: useState < useReducer < context < external store
- Don't sync state (derive instead)
- Avoid redundant state

### Rendering
- Memoize expensive calculations (useMemo)
- Stable callback references (useCallback) when passed to children
- Don't over-memoize (measure first)
- Key prop: stable, unique identifiers (not array index)

### Effects
- useEffect for synchronization, not events
- Clean up subscriptions and timers
- Avoid unnecessary dependencies
- Don't fetch data in useEffect (use framework's data fetching)

### Composition
- Prefer composition over props drilling
- Use children and render props for flexibility
- Compound components for related UI
- Don't abstract too early

## Patterns to Avoid
- Props drilling >3 levels
- God components (>300 lines)
- useEffect for derived state
- Inline object/function creation in JSX (when performance matters)
- Boolean prop explosion (use variant/compound patterns)

## Rules
- Check React version and available features
- Server Components: prefer over client when possible
- Measure before optimizing
- Follow project's existing patterns

## Output

```
## React Review: [scope]

**Critical** (performance/correctness)
- [issue] at file:line → [fix]

**Important** (maintainability)
- [issue] at file:line → [fix]

**Suggestions**
- [pattern improvement]
```
