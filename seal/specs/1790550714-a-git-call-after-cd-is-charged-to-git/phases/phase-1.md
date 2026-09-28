# 1790550714-a-git-call-after-cd-is-charged-to-git — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 0fca8c5 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`git` by command word, on the text `family` already reads. A helper
tokenises with `shlex` (POSIX, `punctuation_chars`, newline as punctuation)
and yields each command word by the spec's In §1 rule. `family` answers `git`
when any command word's basename is `git` or `gh`, and falls back to the old
anchored pattern on `ValueError`. `FAMILIES` order stays. The sentence
corrections ride in the same commit: the `FAMILIES` comment, the `family`
docstring with the rule and its three bounds, the `analyse` docstring's *one
exception*, the `--segments` comparability line naming 0.15.6 and #377, a
`skills/verify/SKILL.md` paragraph beside #300's, and the changelog entry.
Cases S1 to S6 and S10, each seen red, and the named mutants.

## What this phase found

**The frame does not hold on naming 0.15.6.** `tests/test_release_hygiene.py`
refuses a loaded file that names a version at or above the running one (0.15.5
now), so `0.15.6` in `session_cost.py` and `SKILL.md` failed the narrow run on
four lines. 0.15.5 is refused as well, because the rule is *at or above*. The
existing `0.9.4` line was added on 2026-09-13, after 0.9.4 had shipped, and the
timer check landed on 2026-09-18. So the printed line, the docstring and the
`SKILL.md` paragraph name #377 and point to `CHANGELOG.md`, where this
work item's fragment is gathered under the release that carries it. S10's case
asserts that wording and is named `…_moved_at_377`. The changelog fragment
keeps `0.15.6`, because `seal/specs/` is outside the scanned set and the
fragment is gathered into that version's section.

**The fallback is narrower than the spec's sentence, because the walk is
lazy.** `command_words` yields as it reads, so `git log 'x` answers `git` from
its first word before the tokeniser raises. The anchored pattern decides only a
line that is refused before its first word is finished (`git'x`). An eager walk
would send `cd /x && git log 'x` to the pattern, and the pattern answers
`other` there, which is worse. The docstring states it, and the case has one
arm per mutant (escape, eager, `other` on refusal).

**`#` is an ordinary character to the tokeniser here.** `shlex`'s own comment
handling starts a comment inside a word (`a#b`), which bash does not, and it
consumes the newline that ends the comment, which would join the next line's
command onto it. Phase 2 measures whether a word-start comment rule is worth
adding, since that is where comment lines followed by a `git` line reach
`family`.

**The repeats figures cannot move in this phase.** They keep only `test`,
`lint/type` and `build`, and this rule moves calls between `other` and `git`
alone. The first draft of the `analyse` docstring and the `SKILL.md` paragraph
said they could, and both were corrected before the commit. Phase 2's heredoc
change is what moves them.

Mutation (executed, `test_tmp_mutate.py` in the session scratchpad, restored
from kept bytes and verified byte-for-byte, `tests/__pycache__` cleared
between): twelve mutants, all killed. Unanchoring to `\b(git|gh)\b` turns S4
and S6 red. Letting the error escape, walking eagerly and answering `other` on
refusal each turn S6 red. Dropping `(` from the separators, `do` from the
reserved words, the assignment skip or the basename each turn S3 red. Letting a
redirection separate, or reading `$(` as a subshell, turns S4 red. Checking
`git` first turns S5 red. Deleting the new line turns S10 red.

Seen red before green (executed): S1, S3 and S10 failed against the unchanged
`family` and report. S4, S5 and S6 pass on the old code by design, because
they pin today's answers, and each was seen red through its mutant above.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the `analyse` docstring's *`span_s` is the one exception* | the same docstring, now *Two rules moved after readings were published*, naming #300 and #377 |
