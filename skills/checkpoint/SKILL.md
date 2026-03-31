---
name: checkpoint
description: Safety checkpoint before risky operations. Triggers on refactor/delete/migrate keywords.
---

# Checkpoint

Create a safety point before risky operations.

## When to Trigger
- Refactoring (>3 files)
- Deleting files/code
- Migration/schema changes
- Large-scale renaming
- Changing core abstractions

## Steps

1. **Assess risk**
   - What could go wrong?
   - Is this reversible?
   - What's the blast radius?

2. **Create safety net**
   - Ensure all changes are committed (or stashed)
   - Note the current commit hash
   - List files that will be affected

3. **Confirm with user**
   - Present: what will change, what could break, rollback plan
   - Get explicit approval before proceeding

4. **After completion**
   - Verify nothing unintended changed
   - Run tests
   - Confirm rollback path still works

## Output Format

```
Risk: [LOW/MEDIUM/HIGH]
Affected: [file count] files
Rollback: [git reset --hard HASH / other plan]
Proceed? (waiting for user confirmation)
```
