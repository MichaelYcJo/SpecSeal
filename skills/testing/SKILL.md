---
name: testing
description: Walk a test-strategy pass — which level each test belongs at, what to cover first, the edge cases that get missed. Verifying a completion claim is `verify`; chasing one failing test is `debug`.
disable-model-invocation: true
---

# /specseal:testing — put each test where it can actually fail

Coverage counts what ran, not what was checked, so a suite can be green and
prove nothing. Two questions decide the shape: at which level can this break
be observed, and would the test fail if the behavior changed.

The pyramid below is general; its middle tier is where projects differ most,
so read the examples as one filling. **What sits there is whatever this
project's parts have to agree on to work** — a service's database and request
handlers, a client's screens against a fake backend, a CLI's argument parsing
through to its exit codes, a library's public surface against a real consumer,
a pipeline's stages against fixture data.

## Test Pyramid

### Unit Tests (base - most tests here)
- Pure functions, business logic
- Fast, isolated, no external deps
- Mock at boundaries only

### Integration Tests (middle)
- Component interactions — the seams this project actually has
- Real collaborators where the seam is the point (a test database or
  container, a fake server, a temp filesystem, a simulator)
- Examples by project kind: database queries and request handlers; a screen
  driven against a stubbed API; argument parsing through to exit codes; a
  library exercised the way a caller would

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
