# /code-review - Structured Code Review

## Scope
Review changed/specified code for issues by severity.

## Checklist

### Critical (block merge)
- Security: injection, XSS, auth bypass, data exposure
- Data loss or corruption risk
- Race conditions, deadlocks
- Broken error handling in critical paths

### Important (should fix)
- SOLID violations
- Missing error handling
- Performance: N+1 queries, unnecessary work, memory leaks
- Missing validation at system boundaries
- Unclear or misleading abstractions

### Minor (nice to have)
- Naming improvements
- Style inconsistencies
- Minor duplication
- Edge case test gaps

## Rules
- Review only what changed (unless full review requested)
- Be specific: `file:line` references
- Provide fix examples for Critical/Important
- Don't nitpick style without a style guide
- Briefly acknowledge good code

## Output

```
## Review: [scope]

**Critical** (N)
- file:line — issue → suggestion

**Important** (N)
- file:line — issue → suggestion

**Minor** (N)
- file:line — issue

**Good**: [what's done well]
**Verdict**: Approve / Request Changes
```
