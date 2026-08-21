---
name: checkpoint
description: |
  Establish a rollback point before an operation that is hard to undo, and
  get explicit approval with the blast radius stated.
  Use when: deleting files, migrating schemas, renaming across the codebase,
  or changing a core abstraction — where reverting later is not just a git
  command.
  NOT for: ordinary refactors that a commit already makes reversible.
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
