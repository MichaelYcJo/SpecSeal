---
name: confidence-check
description: |
  Readiness check before implementing: does something equivalent already
  exist, is the API verified against the installed version, is the cause of
  the bug actually understood rather than guessed.
  Use when: about to build something non-trivial against an unfamiliar
  library, a suspected duplicate, or a bug whose cause is still a hypothesis.
  NOT for: firing on your own while the smith is driving — its design gate
  invokes this when readiness is the open question. Not for typo, config, or
  one-line changes.
---

# Confidence Check

Run this BEFORE starting any non-trivial implementation.

## 5 Checks (weighted)

1. **No duplicate exists** (25%)
   - Search codebase for similar functionality
   - Check if existing code can be extended instead

2. **Architecture compliant** (25%)
   - Uses existing stack/patterns in the project
   - No unnecessary new dependencies
   - Follows project's established conventions

3. **Official docs reviewed** (20%)
   - Library/framework API verified against current version
   - Breaking changes checked if upgrading

4. **Working reference found** (15%)
   - OSS example or proven pattern identified
   - Not relying on untested approach

5. **Root cause understood** (15%)
   - For bugs: clear understanding of WHY it fails
   - For features: clear understanding of requirements

## Score & Thresholds

Calculate weighted score:
- **≥90%**: Proceed with implementation
- **70-89%**: Present alternatives and gaps to user. Ask before proceeding.
- **<70%**: STOP. List what's missing. Ask user for direction.

## Output Format

```
Confidence: [score]%
✅ [passed checks]
⚠️ [partial checks with gaps]
❌ [failed checks with what's needed]

Recommendation: [Proceed / Ask user / Stop]
```

## Skip When
- Typo/comment fixes
- Simple config changes
- One-line changes with obvious correctness
