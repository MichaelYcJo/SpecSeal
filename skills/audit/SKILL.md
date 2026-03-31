---
name: audit
description: Validate project-specific rules that linters can't catch.
---

# Audit

Check project-specific rules defined in `.claude/audit-rules/`.

## How It Works

1. **Check for rules**: Look for `.claude/audit-rules/*.md` files
2. **If no rules exist**: Suggest bootstrapping with common patterns
3. **If rules exist**: Validate each rule against the codebase

## Rule File Format

Each `.claude/audit-rules/[name].md` defines:
- **Pattern**: What to check (regex, file pattern, or description)
- **Expected**: What should be true
- **Severity**: critical / warning / info

## Built-in Checks (always run)
- No hardcoded secrets (API keys, passwords, tokens)
- No `console.log` in production code (unless logging library)
- No TODO/FIXME in code being committed

## Managing Rules

- `audit manage add` - Add a new rule interactively
- `audit manage list` - Show all active rules
- `audit manage remove` - Remove a rule

## Output Format

```
## Audit Results

✅ Passed: [N] rules
⚠️ Warnings: [N]
❌ Violations: [N]

[For each violation:]
❌ [rule name] - [severity]
   [file:line] [what's wrong]
   Fix: [suggestion]
```
