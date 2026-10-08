# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — round 1 fixes

The fix pass for `rounds/round-1.md`, written by smith on Opus 5.5. Fix range
`2f0d14b3..` the commit that adds this file.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 🔴 1 | fixed | 89bca43f |
| 🔴 2 | fixed | 89bca43f, 151a0ad0 |
| 🟡 3 | fixed | e60d35da |
| 🟡 4 | fixed | cd7027df |
| ⬜ 5 | answered | No spelling of this kind switches a branch: bash makes `git rebase main 'feature x'` of `git rebase {main,'feature x'}`, which git refuses, as the report executed. Changing `_BRACE`'s word test would add a rule for a shape with no consequence, so it is left, and the report's entry is where the next reader of `_BRACE` finds the gap |
| ⬜ 6 | fixed | aee5615a |

🔴 1: the guard's half of the braced forms now runs on every platform, and
only bash's half is skipped where `shell_probe("bash")` finds no shell, so
the Windows leg still asserts that none of the four is listed.

🟡 3: the rule reads the word's comma alternatives rather than the text
`git`, so `cat {.gitignore,README.md}` stays silent; the report's `"git" in
t` would have stopped it in every dirty tree, and a mutation to that text
test is red on the case planted for it.

⬜ 6: the docstring now names ANSI-C quoting as where the reader and bash
disagree, in both directions. The disagreement itself is unchanged: the
grant direction predates #868, and the refusal direction names the waiver
typed in front, which still waives.
