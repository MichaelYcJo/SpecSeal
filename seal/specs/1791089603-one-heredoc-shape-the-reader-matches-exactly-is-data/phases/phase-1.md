# 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b21cb44a |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The reader, `hooks/one_heredoc.py`, written fresh: clauses A–F as a grammar
over line 1, a raw line split, the `<<` count and the reduced text, with no
reuse of `_heredoc_split`, `drop_comments` or #760's delimiter-quoting
helper for the decision. Unit cases for every slot of clause B and a string failing each of
A–E (S4's reader half). The agreement test over a generated corpus in the
real bash and zsh on this machine (`/bin/bash` 3.2, zsh 5.9), directly and
through `eval` (S6), executing harmless strings with a marker file and no
commit. Red shown by deleting each ban in turn.

## What this phase found

**The frame holds.** Every clause was buildable as written. `is_git_commit`
has no caller in `hooks/`, `tests/`, `bin/`, `skills/` or `docs/` (Q5, by
`grep`, executed), so phase 2 touches `main` alone.

**Two choices the spec left to the build.**

- The reader returns the body each line WITH its newline, not joined. Joined,
  an empty body and a body of one empty line are the same string, and the
  shell writes them differently. The agreement test compares bytes, so it
  needs the exact form.
- A program whose terminator is followed only by newlines has no suffix: the
  reduced text is the first line alone, the same as a sink's. Clause F says
  "where a suffix exists", and a run of newlines runs nothing.

**The agreement test, measured (Q3, executed).** The corpus is 696 strings:
two delimiters, four first lines (`cat >`, `cat >>`, `tee -a`, and a `cd` to
a single-quoted directory then `tee` to a single-quoted file), 29 bodies and
three endings. The reader admits 552, exactly those without a clause-A byte.
bash 3.2.57 and zsh 5.9 cut all 552 where the reader does, directly and
through `eval`: four runs, 2,208 shell runs, no disagreement. bash 5.x is not
installed here, so its answer comes from CI's ubuntu leg at the pull request.

The first version ran six first lines and took 135 s for the module under
`-p no:xdist`. Dropping `tee` without `-a` and `cd sub && cat >` brought it
to the four above, and the module then took 20.4 s of wall time under
`bin/test`'s default `-n auto`. Neither dropped line exercises an axis the
four left keep: the shell cuts a body while it parses, before the consumer
runs.

**Red, each clause (executed, `bin/mutation-check`).** Twelve mutations of
the reader against the unit module, each red: deleting the CR, the NUL and
the backslash-newline ban one at a time; the `<<` count; the sink's
empty-rest rule; the exact terminator comparison (made a stripped one); a
glued `>` added to the sinks; any non-blank word after `python3 -`; a blank
and a dash in D; any two words joined by `&&` or `;` as LEAD; the text-type
check; the program's suffix dropped. The oracle itself was shown able to
fail by stripping each body line's trailing blanks: red in all four
shell runs.

**Two bans the shells here do not need, measured.** With the
backslash-newline ban deleted, and separately with the CR ban deleted, the
agreement test stays green on bash 3.2.57 and zsh 5.9: both keep a
backslash-newline and a CR literal in a single-quoted body, and neither
takes a line ending in CR for the terminator. A hand probe agreed for the
case the corpus cannot admit, a backslash-newline right before the
terminator line. So both bans are conservative on these two shells, and the
unit cases are what hold them. That is a measurement for `plan.md`'s
alternative H, not a reason to lift either ban: bash 5.x and the
`drop_comments` readings #760 met are not in it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
