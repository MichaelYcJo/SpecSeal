# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — round 5 fixes

The fix pass for `rounds/round-5.md`, written by smith on Opus 5.5, the
redesign run's last. Fix range `b9a4bcff..` the commit that adds this file.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 🟡 1 | fixed | b6079033 |
| 🟡 2 | fixed | b6079033 |
| ⬜ 3 | answered | corrected at b6079033: §A names a reflog range across two braces among the deliberate over-stops, and the brace-shape case pins `git diff HEAD@{1}..HEAD@{0}` and `git log @{u}..@{1}` as stops |
| ⬜ 4 | answered | corrected at bdf65b20: `phases/phase-7.md` writes the 57 must-stop and 20 must-not forms the self-check ran and the tests they come from; ledger S22 and `questions.md` M4 carry 42 of 33,287 |

🟡 1 and 🟡 2 share one change, the orchestrator's: the brace test reads the
command's text, not its words. Each quoted span (`'…'`, `"…"`, `$'…'`,
`$"…"`) and each escape stands in as one space. Then a `{`, later a `,` or a
`..`, later a `}` is a brace, with no word boundary and no nesting read. The
one exception is a `${` whose span holds no brace, `,` or `..`. A segment
reads its words joined, and a brace the text holds and no one segment's
words hold is the command's. `_BRACE_IN_WORD` is gone (NAME NOT IN TREE since round 5's fixes).

- **Red first.** In a scratch clone with the guard from `b9a4bcff`, the
  seven round 5 spellings, eight over-stop pins and the two new `-C`
  parameters were red.
- **Silent forms.** Ten of round 4's 13 still pass, with `echo "${a,}"`
  and `echo ${a},${b}` added. Three now stop (`echo ${a,}`, `echo {a, b}`,
  the same beside a quoted brace), and so do `git log ${x,}` and a brace
  group beside a quoted brace from the S12 case. They are pinned as stops
  and named in §A as deliberate over-stops.
- **Mutations.** Seven of nine were red. A quoted span deleted outright and
  the `$` left out of the span SURVIVED: the exemption takes no `${`
  holding a `,` or a `..`, so a `$` a deleted quote leaves against a `{`
  makes an exempt span only where no brace was.

The count, by phase 7's method: 42 of 33,287 pairs, one git. Round 4's
reading stops 34 of the same pairs, and round 5's lets through none of
them. The eight new ones are seven brace groups holding a comma and one
`${r%..*}`.

`survivor-check --range b9a4bcff..HEAD` reported two places, both written
into `survivors.md` with a quote.
