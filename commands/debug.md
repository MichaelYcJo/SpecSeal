# /debug - Systematic Debugging

## Trigger
Test failures, error investigation, unexpected behavior.

## Process

### Phase 1: Understand
- Read FULL error message and stack trace
- Reproduce the issue
- Identify recent changes that might be related
- Collect evidence: logs, state, environment

### Phase 2: Locate
- Find working examples of similar code
- Compare working vs broken
- Narrow down: binary search the problem area
- Check boundaries: inputs → processing → outputs

### Phase 3: Hypothesize & Test
- ONE hypothesis at a time
- Minimal test to confirm/deny
- If denied → new hypothesis (don't patch)

### Phase 4: Fix
- Write failing test first
- Minimal change to fix
- Verify: new test passes, existing tests still pass

## Rules
- Be systematic, not random
- One change at a time
- 3 fix attempts failed → STOP (3+ Fix Rule)
- Document what was tried

## Output

```
Bug: [description]
Root cause: [why]
Fix: [what changed]
Verification: [test results]
```
