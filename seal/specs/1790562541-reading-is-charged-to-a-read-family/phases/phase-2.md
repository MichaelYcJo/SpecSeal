# 1790562541-reading-is-charged-to-a-read-family — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | f57df573 |
| Ran by | unknown — the spawn prompt did not hand the value over, and a segment's own account of itself is the one filler the template refuses |

## What this phase was asked

The `read` family. The walk factored so one pass yields each simple
command's words and redirections, with `command_words` derived from it and
unchanged. The read rule of spec In §1–§4, judged after the four existing
families. In the same commit, every statement it makes true: the `FAMILIES`
comment with the admission criterion, `family`'s docstring, the bounds
sentences extended to `read`, `analyse`'s docstring (a third move),
`report_segments`' comparability line naming #642, the `SKILL.md`
paragraph, the two edited test arms and docstrings, and the changelog
entry. The rule stays side-effect-free, as the frame says, and nothing is
built for #640.

## What this phase found

**`case` and `esac` are not neutral words (a divergence from spec In §1,
recorded under Q4).** The spec's neutral set lists both. But a `case` arm's
`)` does not put the next word in command position, which is `runs_git`'s
third stated bound, so `case $x in a) rm f;; esac; ls` has `ls` as its only
command word besides `case` and `esac`, and would read as reading. That is
In §3's own principle, *what the walk cannot see is not `read`*, applied to
the grammar rather than to a substitution. `esac` is only ever reached
after a `case`, so it goes with it. The case arm pins it.

**The hidden-from-the-walk test is a text match, not the walk.**
`without_comments` rewrites a quoted operator to a letter before the walk
runs, so `"$(ls)"` reaches the walk as `$_ls_` and the walk cannot tell it
from a quoted `'$('`. The rule therefore searches the text for `<<`, `$(`,
`` ` ``, `<(` and `>(` before walking. A quoted or commented one keeps the
line out as well, which is the direction every funnel in this file takes.
It is not a second answer to *what is a command*: the walk remains the only
place command words, arguments and operators come from.

**`read` is judged on the command as recorded, heredoc bodies kept.**
`without_heredoc_bodies` matches a here-string, `<<< "$y"`, as an operator
whose delimiter is `$y` and cuts from there to the end, which removes the
`<<` the rule needs to see. On the stripped text `grep x <<< "$y"` read as
`grep x <`, which is `read`. The mutant that hands `only_reads` the
stripped text is killed by that arm.

**Long options are matched by the prefixes GNU's parser accepts (§12's
class, beyond the spec's literal list).** `sed --in s/a/b/ f` is an in-place
edit, and so is `sort --out g f` a write. `abbreviates` takes any prefix of
three characters or more, with or without `=value`, so `--` alone, the end
of options, is not read as one (`sed -n 1p -- f` and `sort -- f` are
`read`).

**Two guards were dropped as equivalent mutants (f57df573).** An operator
token right after a redirection already fails the harmless-target test, and
a redirection with no target is a syntax error bash runs nothing for. The
second means `cat f >` now reads as `read`. It ran nothing, so nothing is
mischarged.

**How each new case was seen red.** The positive cases — the ticket's
instance and the read-only shapes, the transcript case, and the edited
`W=/w; …` arm — failed at d8dc866c, where `family` had no `read` to return
(3 failed, 135 passed). The comparability case failed before its sentence
was written. The walk's own case could not run at d8dc866c, where
`shell_words` did not exist. The negative cases (writes, more than reading,
hidden, neutral alone) assert *not `read`*, which holds trivially before
the family exists, so each was seen red under its mutant instead.

**Mutants, each applied alone to f57df573's code, the module run, and the
bytes restored from a kept copy (executed; every one exit 1):** any read
word decides; no redirection check; no `sed -i` check; `sed` cluster read
as a leading `-i` only; `sed` long option exact; `abbreviates` without the
`=` split; without the length guard; no `sort -o` check; `sort` long option
exact; no `find` check; no `awk` check; no `--include`; no heredoc check;
no substitution check; no backtick check; no process-substitution check;
`read` judged first; `/dev/null` accepted for any target; a duplication
accepted onto any target; onto `-` refused; a duplication target accepted
after any operator; no guard for an argument before any command; `reads`
always true; no basename; the tokeniser's refusal escaping; the walk
yielding no arguments; the walk yielding words inside a substitution; the
walk yielding an empty operator; `read` judged on the stripped text; and
the #642 sentence changed. Thirty mutants, thirty killed.

**Narrow runs at f57df573 (executed).** `bin/test tests/test_session_cost.py`
exit 0, 140 passed. The twenty modules that name `verify/SKILL`,
`session_cost` or `session-cost` (`grep -l` at the tip), exit 0, 860
passed, 7 skipped, at b08670b6. `tests/test_release_hygiene.py`,
`tests/test_no_real_identifiers.py` and
`tests/test_a_rider_reaches_its_file.py`, exit 0, 85 passed. `ruff check`
and `ruff format --check` on the two edited Python files, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `analyse`'s *Two rules moved after readings were published* | the same paragraph, now *Three*, with the #642 paragraph after the #377 one |
| `family`'s *the other three by their patterns* | the same docstring, naming the three and `read` |
| `case` and `esac` from the spec's neutral set | `NEUTRAL_WORDS`' comment, this record, and Q4 |
