# Safety Rules

## 3+ Fix Rule (detailed)
After 3 fix attempts on the same bug:
1. STOP immediately — no "one more try"
2. Review architecture — is the pattern fundamentally wrong?
3. Escalate to user — present what was tried, what failed, why

**Signals of architectural problem:**
- Each fix creates a new problem elsewhere
- Fix requires "major refactoring"
- Same symptom keeps returning in different forms

## Verification Gate (detailed)
Before ANY completion claim (done, fixed, passes, works):
1. IDENTIFY — what command proves this claim?
2. RUN — execute it fresh (not cached output)
3. READ — full output, exit code, failure count
4. VERIFY — does output actually confirm claim?

**NOT sufficient evidence:**
| Claim | Insufficient | Required |
|-------|-------------|----------|
| Tests pass | Previous run, "should pass" | Fresh test output: 0 failures |
| Build OK | Linter passing | Build command: exit 0 |
| Bug fixed | "Code looks right" | Reproduction test passes |
| Feature done | Partial test pass | All acceptance criteria checked |

**Red flags — stop if you catch yourself:**
- "should", "probably", "seems to" → run the command
- Satisfaction before verification → run the command
- Commit without verification → run the command

## Security Essentials
- Stop immediately on security incident → run /security-audit and escalate to the user
