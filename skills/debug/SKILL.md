---
name: debug
description: |
  Find the cause of wrong behavior: reproduce, locate, one hypothesis at a
  time, then a failing test before the fix.
  Use when: the code runs but produces the wrong result, or a test fails.
  NOT for: build, compile, or type-check errors — nothing runs there, so
  there is nothing to reproduce (that is `build-fix`).
---

# debug — one hypothesis at a time, and a failing test before the fix

The code runs and produces the wrong answer, which means it can be
reproduced — and a bug you cannot reproduce is a bug you cannot claim to
have fixed. Changing several things at once destroys the only signal you
have: which change mattered.

## Phase 1: Understand (before touching code)
- Read the FULL error message and stack trace
- Reproduce the issue (write a failing test if possible)
- Check recent changes that might have caused it
- Collect evidence: logs, error output, state

## Phase 2: Locate
- Find working examples of similar code in the codebase
- Compare working vs broken - what's different?
- Binary search: narrow down the problem area
- Check inputs and outputs at each boundary

## Phase 3: Hypothesize
- Form ONE hypothesis at a time
- Design minimal test to confirm/deny
- If denied → new hypothesis (don't patch the old one)

## Phase 4: Fix
- Write a failing test that reproduces the bug
- Make the minimal change to fix it
- Verify: failing test now passes
- Verify: no other tests broke

## Rules
- Never guess-and-check randomly. Be systematic.
- One change at a time. Verify after each.
- If 3 fix attempts fail → STOP (3+ Fix Rule). The problem may be architectural.
- Document what you tried and what you learned.

## Output Format

```
Bug: [description]
Root cause: [why it happens]
Fix: [what was changed]
Test: [how it's verified]
```
