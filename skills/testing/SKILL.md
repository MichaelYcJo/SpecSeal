---
name: testing
description: Test strategy and implementation — pyramid, coverage priorities, edge-case checklist.
disable-model-invocation: true
---

# /specseal:testing - Test Strategy & Implementation

## Scope
Design test strategy, write tests, improve coverage.

## Test Pyramid

### Unit Tests (base - most tests here)
- Pure functions, business logic
- Fast, isolated, no external deps
- Mock at boundaries only

### Integration Tests (middle)
- Component interactions
- Database queries
- API endpoint handlers
- Use test databases/containers

### E2E Tests (top - fewest tests here)
- Critical user flows only
- Login, checkout, core workflows
- Slower, run less frequently

## Test Quality Checklist
- Tests have descriptive names (should_X_when_Y)
- Each test checks ONE thing
- Tests are independent (no ordering dependency)
- Tests cover happy path AND edge cases
- Tests cover error paths
- No test logic complexity (no if/loops in tests)
- Assertions are specific (not just "no error")

## Rules
- Write failing test BEFORE fixing bugs
- Don't test implementation details, test behavior
- Don't mock what you don't own (wrap it instead)
- Keep tests fast (seconds, not minutes)
- Coverage target: focus on critical paths, not percentages

## Output

```
## Test Strategy: [scope]

**Coverage Gaps**: [what's not tested]
**Priority Tests**: [what to add first]
**Test Plan**:
1. [test description] - [type: unit/integration/e2e]
2. ...

[Generated test code if requested]
```
