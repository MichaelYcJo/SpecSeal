# /clean-code - Clean Code Review

## Focus Areas

### Naming
- Variables/functions reveal intent
- No mental mapping needed (no single-letter vars except loops)
- Consistent vocabulary (don't mix get/fetch/retrieve)
- Boolean names are predicates (isActive, hasPermission, canEdit)

### Functions
- Do one thing (Single Responsibility)
- <20 lines preferred, <50 max
- <4 parameters (use object for more)
- No side effects hidden in the name
- Command-query separation

### Error Handling
- Don't return null when you can throw/return Result
- Don't pass null as argument
- Fail fast at boundaries
- Error messages are actionable

### Comments
- Code should be self-documenting
- Comments explain WHY, not WHAT
- Delete commented-out code
- TODOs have ticket references

### Structure
- Files have single focus
- Related code is close together
- Imports are organized
- Dead code is removed

## Rules
- Apply to changed code, not entire codebase
- Respect project's existing patterns
- Practical over dogmatic

## Output

```
## Clean Code Review: [scope]

**Naming**: [issues found]
**Functions**: [issues found]
**Error Handling**: [issues found]
**Structure**: [issues found]

Priority fixes:
1. [most impactful fix]
2. ...
```
