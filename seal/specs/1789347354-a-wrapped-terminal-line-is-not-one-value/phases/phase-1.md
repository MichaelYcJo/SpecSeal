# 1789347354-a-wrapped-terminal-line-is-not-one-value — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 1e91894 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Narrow `skills/code-review/scripts/round_record.py#BLOCK_START` to the form
`.github/scripts/issue_claims_check.py` already ships, plus the two fence
openers this module needs, and pin the truncation direction at four shapes.
Re-derive the paste-ready form out of
`seal/specs/1789034970-.../rounds/round-4-report.md` finding 2 rather than
transcribing it: the branch it was measured on, `backup/120-before-rewrite`,
is not in this clone.

## What this phase found

**Three of the four shapes `spec.md` promises red were already green, and the
reason is that the report was written against a different tree.** `spec.md`
§*User scenarios* asks for a case parametrised over `#N`, `**bold**`, `<div>`
and an indented line, *each seen red against the pattern at `5e09345`*.
Measured by applying the constant as written: only the two `#N` shapes
truncate against this branch's base. `[-*+]\s` carries a space requirement, so
`**bold**` never matched it; `<div>` and an indented run of prose match no
alternative at all. The round-4 report's list is true of the widened pattern
`3b228f4` shipped, which this line of history does not carry — `git cat-file`
cannot resolve that commit in this clone.

The arms are kept and each one now says what it was seen red against, in the
parametrisation itself: `base`, `space` — this module's own pattern with one
space requirement dropped, which is the widening `plan.md` §*Alternatives
considered* rejects — `anchor`, and `boundary` for the two that no candidate
pattern ever cut. Two arms are green from birth and say so rather than
implying a demonstration that did not happen.

**A sixth mutation found a gap no case covered, and it is the one
`issue_claims_check.py` pins and this module did not.** Dropping the
whole-line `$` anchor from the three run-of-three alternatives left the entire
module green: without it a line that merely OPENS with a run of markers
matches, and the clause after it is lost. That is the false-positive direction
`seal/ledger.md`'s row for the sibling records as executed by mutation. The
`--- and the rest of the clause is prose` arm was planted for it and is red
under that mutation alone.

**`spec.md` §*The gate answer* is one-directional where the change is not.**
It says *a report that today produces a whole cell is unaffected*. Measured:
five shapes that today join into the cell now stop before it — `---`, `___`,
`***`, a setext underline, and `1)` as an ordered-list delimiter. That is the
swallow direction closing and is exactly what §*Scope* asks for (*Both
directions close at once*), so the change is right and the bullet is the thing
that is wrong. Nothing that today produces a **correct** cell is affected.

**The module holds 107 cases at the base commit, not the 104 `plan.md` and
`spec.md` both state.** Measured by running it: 107 before, 117 after.

**The join strips each continuation line before joining it.** The indented arm
went red on its own assertion the first time it was run, because the
expectation carried the indent. That is a case red for the wrong reason, which
is the thing §15 exists to catch; the expectation now strips, and the comment
beside it records why.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `BLOCK_START`'s bare `#` and its `[-*+]\s` / `\d+\.\s` spelling | The narrowed constant that replaces it, whose comment states which shapes it reaches and which it deliberately joins instead of guessing at |
| The claim, carried by the constant's own comment, that the listed shapes are what a report puts beside a terminal line | The same comment, rewritten: the guard is a narrowing, and the blank line is the only stop that covers every shape |
