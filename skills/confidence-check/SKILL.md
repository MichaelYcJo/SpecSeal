---
name: confidence-check
description: |
  Readiness check before implementing: does something equivalent already
  exist, is the API verified against the installed version, is the cause of
  the bug actually understood rather than guessed. Reports which checks are
  unsatisfied — no score, since any single miss is the whole answer.
  Use when: about to build something non-trivial against an unfamiliar
  library, a suspected duplicate, or a bug whose cause is still a hypothesis.
  NOT for: firing on your own while the smith is driving — its design gate
  invokes this when readiness is the open question. Not for typo, config, or
  one-line changes.
---

# confidence-check — is the ground under this actually known?

Three things get assumed at the start of implementation and are wrong often
enough to be worth a minute: that nothing equivalent already exists, that
the API is what you remember, and that the bug's cause is understood rather
than guessed. Settle them before writing, not after.

## Five checks

1. **No duplicate exists**
   - Search codebase for similar functionality
   - Check if existing code can be extended instead

2. **Architecture compliant**
   - Uses existing stack/patterns in the project
   - No unnecessary new dependencies
   - Follows project's established conventions

3. **Official docs reviewed**
   - Library/framework API verified against current version
   - Breaking changes checked if upgrading

4. **Working reference found**
   - OSS example or proven pattern identified
   - Not relying on untested approach

5. **Root cause understood**
   - For bugs: clear understanding of WHY it fails
   - For features: clear understanding of requirements

## What to do with the answers

**Any check unsatisfied — say which, and ask.** All five satisfied — proceed.
That is the whole rule, and it is what the old weighted score already encoded:
the weights summed to 85 without any one of them, so a single miss could never
reach the "proceed" band. The percentage carried no information the list of
failed checks did not, while looking like a measurement.

It also invited the wrong move. A number can be nudged — one check called
"partial" instead of "failed" lifts the total past a threshold, and nothing in
the report shows that happened. A named unsatisfied check cannot be nudged; it
is either answered or still open.

An unsatisfied check is **not** a reason to stop. It is a thing to say out loud
before writing code, so the person who can settle it gets the chance. Most are
settled in one exchange.

## Output format

```
Ready:      <checks satisfied, one line each>
Not ready:  <check> — <what is missing, and what would settle it>
Unknowable here: <check> — <who can answer>

<Proceeding / Asking first>, because <the one sentence that follows from above>.
```

Never report a check as satisfied because it was skipped. A check nobody walked
is "not ready", the same as one that failed — the reader cannot tell the two
apart otherwise, and only one of them is safe.

## Skip When
- Typo/comment fixes
- Simple config changes
- One-line changes with obvious correctness
