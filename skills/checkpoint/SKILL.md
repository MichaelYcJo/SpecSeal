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

# checkpoint — state the blast radius before it is too late to ask

Some operations a commit can undo. These are the ones it cannot: what is
deleted, migrated, or renamed across a tree leaves no equivalent to `git
revert`. The point is not the backup — it is naming what would be lost, out
loud, while the user can still say no.

## When it applies
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
