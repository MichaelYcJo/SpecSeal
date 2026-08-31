---
name: build-fix
description: |
  Resolve build, compile, and type-check errors at their cause instead of
  suppressing them.
  Use when: the build does not produce output — type errors, missing modules,
  syntax or config failures.
  NOT for: code that compiles but behaves wrong (that is `debug`).
---

# build-fix — fix the cause, never the message

Nothing runs yet, so there is nothing to reproduce — the compiler already
told you where it stopped. The failure mode here is suppression: a cast, an
`any`, an ignore comment makes the message go away and leaves the defect.
The first error is usually the only real one; the rest are its shadow.

## Process

1. **Read the full error** - Don't fix based on first line alone
2. **Categorize**
   - Type error → Check type definitions, imports
   - Missing module → Check dependencies, paths
   - Syntax error → Check recent changes
   - Config error → Check build config files
3. **Fix root cause** - Not symptoms
4. **Verify** - Run full build again after fix

## Rules

- Fix ONE error category at a time (cascade errors are common)
- After fixing, re-run build to check for new errors
- If same error persists after 2 attempts → re-examine approach
- If 3+ attempts fail → invoke 3+ Fix Rule (STOP, ask user)

## Common Traps
- Fixing type errors by adding `any` or `as unknown`
- Suppressing errors with `@ts-ignore` or `# type: ignore`
- Fixing import errors by creating empty stub files
- These are symptoms, not fixes. Find the real cause.

## Output Format

```
Error: [category] - [summary]
Root cause: [why it's happening]
Fix: [what was changed]
Build: [PASS/FAIL after fix]
```
