# /naming - Naming Convention Analysis & Suggestions

## Principles
- Names reveal intent (no mental mapping needed)
- Consistent within project
- Follow language conventions

## By Language

### Python
- Variables/functions: snake_case
- Classes: PascalCase
- Constants: SCREAMING_SNAKE_CASE
- Private: _prefix
- Files: snake_case.py

### TypeScript/JavaScript
- Variables/functions: camelCase
- Classes/interfaces/types: PascalCase
- Constants: SCREAMING_SNAKE_CASE
- Components: PascalCase (files too)
- Hooks: use prefix

### Database
- Tables: snake_case, plural
- Columns: snake_case
- Indexes: idx_{table}_{columns}

### API
- URLs: kebab-case
- JSON fields: camelCase
- Query params: camelCase

## Common Problems
- Inconsistent casing (mixing camelCase and snake_case)
- Abbreviated names (usr, msg, btn) in business logic
- Generic names (data, info, item, result, temp)
- Misleading names (isValid that returns a string)
- Too long (getUserAccountSettingsPreferences)

## Output

```
## Naming Review: [scope]

**Inconsistencies**:
- [current] → [suggested] (reason)

**Improvements**:
- [current] → [suggested] (reason)
```
