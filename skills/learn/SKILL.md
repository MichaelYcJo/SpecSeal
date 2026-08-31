---
name: learn
description: |
  Record an insight that cost real debugging effort and cannot be recovered
  from a search — project-specific causes, dependency quirks, the reason
  behind an architectural choice.
  Use when: something was just figured out the hard way and the next session
  would otherwise pay for it again.
  NOT for: narrating ordinary work, anything a search answers in five
  minutes, or facts the code and git history already carry.
---

# learn — write down only what a search cannot return

Most of what a session discovers is recoverable: the code holds it, git
holds it, a search answers it in five minutes. What is not recoverable is
the thing that cost hours and leaves no trace — the dependency quirk, the
reason an abstraction is shaped that way. Record that and nothing else.

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
