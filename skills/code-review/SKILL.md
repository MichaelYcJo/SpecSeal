---
name: code-review
description: Structured code review with severity-based findings.
---

# Code Review

## Review Checklist

### Critical (must fix before merge)
- Security vulnerabilities (injection, XSS, auth bypass)
- Data loss risk
- Race conditions / concurrency bugs
- Broken error handling in critical paths

### Important (should fix)
- SOLID principle violations
- Missing error handling
- Performance issues (N+1 queries, unnecessary re-renders)
- Missing input validation at boundaries
- Unclear abstractions

### Minor (nice to have)
- Naming improvements
- Code style inconsistencies
- Minor duplication
- Missing edge case tests

## Rules
- Review ONLY changed code (don't review the whole file unless asked)
- Be specific: file:line, not vague descriptions
- Provide fix examples for Critical/Important findings
- Don't nitpick style if project has no style guide
- Acknowledge what's done well (briefly)

## Output Format

```
## Review: [scope]

**Critical** (N)
- [file:line] [issue] → [fix suggestion]

**Important** (N)
- [file:line] [issue] → [fix suggestion]

**Minor** (N)
- [file:line] [issue]

**Good**: [brief positive note]
**Verdict**: [Approve / Request changes]
```
