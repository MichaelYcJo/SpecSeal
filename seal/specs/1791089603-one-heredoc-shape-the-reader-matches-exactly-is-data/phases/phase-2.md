# 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 9c48f115 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The gate: `main` reads the reduced text for commits, and `is_git_commit` too
if it has a caller (Q5). The corpus row Q1 moves, in
`tests/test_no_shape_the_base_stops_reads_silent.py` and in
`tests/test_an_automation_run_meets_no_commit_prompt.py`'s four measured
shapes. Gate cases for S1–S5, S7 and S8, with #760's must-stop lists and the
findings table rebuilt as fixtures. S1 and S2 red at `e141980a`. Never touch
`hooks/cmdline_base.py`.

## What this phase found

**Q5: no caller, so the reduction sits in `main` alone** (executed, `grep -rn
is_git_commit` over `hooks tests bin skills docs`: the definition and
nothing else). `is_git_commit` is left as it was.

**What `main` reads with the reduced text, and what it does not.** The commit
reading (`commit_invocations`) and the unparsed fallback's `git`/`commit`
substring test read the reduced text. `tokens.is_plain`, `has_marker` and
`judge` read the command as written, as `spec.md`'s interface section says.
The fallback had to move with the walk: a Python body mentioning both words,
followed by a suffix the splitter cannot finish, would otherwise still stop on
the session's own directory. `test_the_reduction_reaches_the_unparsed_fallback`
pins it, and a mutation putting the fallback back on the command turned it
red alone.

**Four strings of the reader's clause list read silent at the base too,
because their commit was in the wrong place.** Run through the gate from a
declared session directory, a commit after the terminator is judged where it
lands, which is the declared directory, and is silent; that is not what a
"fails clause X" string is about. The four were a commit after a
backslash-newline in a program's suffix, a commit in a here-string in a
suffix, an arithmetic shift beside a commit, and an unterminated quote in a
WORD (which hides the whole command from the base reading). The first three
now carry the commit in the body and a harmless suffix. The fourth is gone
from the list: it fails clause D and B at once, and the base reads nothing
in it. #760's "a backslash-newline splitting the opener" row had the same
fault, and now writes its commit into the first body, which the base reads.
None of the four is a base gap this work owns. The here-string one is a real
base reading (the gate does not read a here-string's text as shell) that
nothing in this work touches.

**Red at the base, executed.** With `main`'s reduction removed by
`bin/mutation-check`, 66 of the 72 selected cases failed: S1, both S2 cases,
every slot of S4's silent half (57), three of six S7 suffixes, the fallback
case, and the moved row in both modules. The six that stayed green are S3,
which pins the base's stop, the three S7 suffixes where the line stops either
way, and two cases of the automation module about a refusal's text, which the
`-k refusal` selection also matched.

**The ledger.** `main`, the corpus and the measured shapes moved nine
released rows. Six are re-read and hold (E1, E2, E6, E17, E18, G8: the press,
the overflow catch and the plainness read are untouched). Three are corrected
rather than re-read, because the moved row falsifies them as written: E3 (the
four measured shapes), E7 (nothing the base stops reads silent) and I10 (the
same, for `1790660768`'s generated corpus). I10's correction is labelled
**read**: the 11,393-command corpus and the three sessions it names were not
re-run, so how many of their commands are the one shape is not counted.

The ten rows still drifted are not this branch's: `templates/config.md`,
`tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT` and
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py#fake_venv` drift on
`release/v0.18.1` at `edee5ca2`, and this branch does not touch them.

**Two names in the frame are #760's and not in this tree**:
`_quoted_delimiter` and `heredoc_data` · NAME NOT IN TREE. The records check refused them, so the
lines in `spec.md` and `questions.md` that name them now say whose they are and
carry `NAME NOT IN TREE`.

**The narrow run.** Phase 2's modules and S9's list together: 1,717 passed,
77 skipped, in 352 s (executed).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The corpus row "measured: a patch whose body loops over a commit string", from `tests/test_no_shape_the_base_stops_reads_silent.py#corpus` and `tests/test_an_automation_run_meets_no_commit_prompt.py#measured` | `tests/test_no_shape_the_base_stops_reads_silent.py#moved_row`, pinned silent by `test_the_moved_row_reads_silent` and `test_the_fourth_measured_shape_is_silent_under_the_press` |
