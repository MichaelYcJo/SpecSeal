---
name: verify
description: Post-completion verification gate. Auto-triggers on done/complete/PR keywords.
---

# Verification Gate

Run this BEFORE any completion claim (done, fixed, passes, complete).

## Iron Law
NO completion claims without fresh verification evidence.

## Verification Steps

1. **Identify** - What command proves this claim?
2. **Run** - Execute full command (fresh, not cached)
3. **Read** - Read FULL output, check exit code, count failures
4. **Verify** - Does output actually confirm the claim?
   - NO → Report actual state with evidence
   - YES → Make claim with evidence attached

## Evidence Matrix

| Claim | Required Evidence | NOT Sufficient |
|-------|-------------------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Reproduction test passes | "Code looks right" |
| Feature complete | All requirements checked off | Partial test pass |

## Red Flags (STOP if you catch yourself)
- Using "should", "probably", "seems to"
- Expressing satisfaction before running verification
- Attempting commit/PR without verification
- Judging whole by partial evidence

## Output Format

```
Verification: [PASS/FAIL]
Command: [what was run]
Evidence: [key output lines]
[If FAIL]: Actual state: [what's really happening]
```
