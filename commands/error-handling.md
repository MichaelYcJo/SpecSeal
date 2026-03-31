# /error-handling - Error Handling Review & Design

## Principles
- Fail fast at boundaries
- Handle errors at the right level
- Errors are actionable (for devs and users)
- Never swallow errors silently

## Checklist

### Boundary Validation
- User input validated at entry point
- External API responses checked
- File system operations wrapped
- Database queries handled

### Error Propagation
- Errors propagate with context (not just re-thrown)
- Custom error types for domain errors
- Error codes for programmatic handling
- Stack traces preserved in development

### User-Facing
- Error messages are helpful (not "Something went wrong")
- No internal details leaked (stack traces, SQL, paths)
- Actionable: tell user what to do next
- Appropriate HTTP status codes for APIs

### Recovery
- Retry with backoff for transient errors
- Circuit breaker for cascading failures
- Graceful degradation where possible
- Cleanup in finally/defer blocks

## Anti-patterns
- Empty catch blocks
- Catching Exception/Error (too broad)
- Using try-catch for flow control
- Logging error but returning success
- Error handling that hides bugs

## Output

```
## Error Handling Review: [scope]

**Critical** (silent failures, data loss risk)
- file:line — [issue] → [fix]

**Important** (poor UX, debugging difficulty)
- file:line — [issue] → [fix]

**Suggestions**
- [improvements]
```
