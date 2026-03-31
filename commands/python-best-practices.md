# /python-best-practices - Python Code Review

## Review Areas

### Type Hints
- Function signatures typed
- Complex types use TypeAlias
- Optional vs Union usage
- Generic types where appropriate

### Project Structure
- Package manager: uv preferred
- pyproject.toml for configuration
- Proper __init__.py exports
- Clear module boundaries

### Patterns
- Context managers for resource management
- Dataclasses/Pydantic for data containers
- Enums for fixed choices
- Generators for lazy iteration
- pathlib over os.path

### Testing
- pytest over unittest
- Fixtures for setup/teardown
- Parametrize for multiple cases
- Proper mocking (patch at usage, not definition)

### Async
- asyncio patterns correct
- No sync calls in async context
- Proper task management
- Async context managers

### Performance
- List comprehensions over map/filter
- f-strings over .format()
- Appropriate data structures (set for membership, dict for lookup)
- Profile before optimizing

## Output

```
## Python Review: [scope]

**Issues by priority**:
1. [issue] at file:line → [fix]

**Suggestions**:
- [improvement]
```
