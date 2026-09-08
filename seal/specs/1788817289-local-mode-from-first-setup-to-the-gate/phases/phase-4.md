# 1788817289-local-mode-from-first-setup-to-the-gate — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `1ef820b` |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Point the preset's routing rule at the bootstrap, so a session in a repository
that has never carried `seal/` reaches the mode question before it writes the
file that creates the root — and cover the route in
`tests/test_first_setup_asks_once.py`, whose cases all read the skill and none
read the preset block.

## What this phase found

**The assertion has to be about ORDER, not presence.** #151's own reading of
this fix is that a conditional put into a block meant to be read straight
through only helps a session that notices the condition applies. So the case
reads what sits BEFORE the instruction to write the file, and a sentence
appended after it would fail — which is the shape of the fix, not a detail of
the test.

**The cases read the installer's span, not the file.** `install.sh` extracts
between `<!-- specseal:start -->` and `<!-- specseal:end -->` with `awk`, so a
sentence written below the end marker reaches this repository and reaches no
user. A whole-file read cannot tell those two apart, and that difference is
the whole of #151's mechanism.

**`seal mode` with no argument is the instruction, and it was executed to
find out.** Both forms write the row; `seal mode <the same mode>` also prints
the entire switch narrative — staging, resets, what a teammate loses — which
is not what somebody who has just answered the question needs to read. The
bare form reports the folder, the row, and that they agree.

**Two counts in the READMEs were already stale and this phase could not leave
them.** *Four of the seven gates* and *the four hooks that read it* were
written before `implementer-mark` and `implementer-notice` joined the table.
Adding a row without touching them would have made a wrong number wronger, so
the lists are named out and the counts corrected to seven of ten. That is the
`offer_header` lesson one file over: a written-down count is a second thing to
keep in step.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/implement/SKILL.md` §Bootstrap's *Do **not** write that config row here* | replaced in the same paragraph by an instruction to run `seal mode`; `tests/test_first_setup_asks_once.py#test_the_bootstrap_records_the_answer_it_was_given` asserts the old sentence is gone as well as the new one present, because a widened instruction beside the old refusal is a document that argues with itself |
