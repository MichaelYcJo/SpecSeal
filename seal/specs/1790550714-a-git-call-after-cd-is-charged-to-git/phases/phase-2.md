# 1790550714-a-git-call-after-cd-is-charged-to-git — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | ca8f4e0 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The text the shell ran. `load` keeps the unflattened command beside
`command`, and `analyse` classifies from it at both `family` sites. `family`
removes each heredoc body up to its closing line (`<<-` strips leading tabs,
the operator's own line is kept, and with no closing line the cut runs to the
end as before), and reads what follows with every family. The sentence
corrections ride in the same commit: the `HEREDOC` comment, the `family`
docstring (body, not rest), the heredoc case's docstring, and the `SKILL.md`
paragraph and changelog entry extended with members 3 and 4 and the `test`
movement. S7 and S8 as cases, red at 2037cf0; S9 and S11 unchanged; a mutant
that classifies from `command` turns S7 red.

## What this phase found

**The new key is `ran`, and a call with no command string holds the flattened
dump.** The spec says such a call holds "the same JSON dump `command` holds".
Taken literally that is the flattened dump, and it keeps the repeats filter's
reading of non-Bash calls exactly as it was, which the spec puts out of scope.

**Q2 is closed, answered by reading.** Every `analyse` call receives slices of
`load`'s own list (`#measure_cycles`, `#segment_slices`, `main`), and no test
or script builds a call dict. So `analyse` reads `call["ran"]` directly, with
no fallback to `command`: a fallback nothing reaches is a unit no mutant can
kill.

**Phase 1's repeats sentence became false here, and was corrected in this
commit.** The repeats keep `test`, `lint/type` and `build`, and a test run
after a heredoc now counts. So the `analyse` docstring, the `--segments` line,
`SKILL.md` and the changelog now say the repeats figures move, and in which
direction: they can only have read low. Every family can only gain text from
this change. What is read now is a superset of what the operator cut left.

**`#` stays an ordinary character, measured rather than assumed.** A
word-start comment rule was the candidate phase 1 left open. Over the 23,195
Bash `tool_use` blocks under `~/.claude/projects/*SpecSeal*/` (executed, a
probe in the session scratchpad, deleted), the tokeniser refuses 23 once
heredoc bodies are removed. One of them has a comment line with an
apostrophe, which is the only thing the rule would recover. The frame's 213
refusals were measured before bodies were removed.

**The tokeniser's own comment handling is a trap, and a case now pins it.**
Its comment branch consumes the newline that ends a comment, so
`cd /x  # into the tree⏎git status` would join the `git` line onto the `cd`.
With `commenters` left at the default, that case goes red.

**Two shapes were added after the first cases were written, because the
mutants showed they were missing.** A line `⇥EOF` under a plain `<<` does not
close the body, and only a case where it would change the answer tells
"strip tabs under `<<-`" from "always strip". The trailing-comment shape above
is the other.

Mutation (executed, `test_tmp_mutate.py` phase 2, restored from kept bytes
and verified byte-for-byte, `tests/__pycache__` cleared between): thirteen
mutants, all killed. Reading `command` at the table site, reading it at the
repeats site, and storing the flat text as `ran` each turn S7 red, the
repeats one through `repeat_exact_s`. Cutting at the operator again turns S8
and S7 red. Never stripping tabs, always stripping them, and dropping the
operator's line each turn S8 red. Restarting the search at 0 turns S8 and S7
red. Keeping an unclosed heredoc whole turns S8 and the #200 heredoc case red.
Treating a newline as whitespace turns S8, the newline case and S7 red, and
restoring the tokeniser's comment handling turns the newline case red.
Printing `ran` in `slowest` turns S7 red (S11's arm). Deleting the page's
heredoc sentence turns S10 red.

Seen red before green (executed): S8 and S7 failed against phase 1's code,
and the newline case answered `other` for all three of its first shapes under
2037cf0's `family`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `family` cutting from the heredoc operator to the end whenever an operator is found | `without_heredoc_bodies`, which cuts to the end only where no closing line follows, and the `HEREDOC` comment that says so |
| phase 1's sentence that the repeats figures do not move | the `analyse` docstring, the `--segments` line, `SKILL.md` and the changelog, which now say they move and in which direction |
