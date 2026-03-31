---
name: learn
description: Capture hard-won debugging insights and project patterns for future sessions.
---

# Learn

Record problem-solving insights that are worth remembering.

## Save Criteria (must meet ALL)
1. **Non-Googleable** - Can't find answer in 5-min search
2. **Project-specific** - Tied to this codebase/setup
3. **Hard-won** - Required real debugging effort
4. **Actionable** - Includes specific files, lines, code

## What to Save
- Bug patterns unique to this project
- Non-obvious configuration requirements
- Architectural decisions and their reasons
- Dependency quirks and workarounds
- Performance pitfalls discovered through profiling

## What NOT to Save
- General programming knowledge
- Standard library usage
- Anything in official docs
- Temporary workarounds (save the real fix instead)

## Storage
Save to: `~/.claude/projects/<project>/memory/`
- Use semantic filenames: `auth-session-quirk.md`, `db-connection-pool.md`
- Keep each file focused on one insight
- Update existing files rather than creating duplicates

## Format

```markdown
# [Short descriptive title]

## Problem
[What went wrong]

## Root Cause
[Why it happened - specific to this project]

## Solution
[What fixed it - with file paths and code]

## Prevention
[How to avoid this in the future]
```
