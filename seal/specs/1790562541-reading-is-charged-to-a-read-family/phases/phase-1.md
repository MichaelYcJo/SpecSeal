# 1790562541-reading-is-charged-to-a-read-family — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | a34c3be3 |
| Ran by | unknown — the spawn prompt did not hand the value over, and a segment's own account of itself is the one filler the template refuses |

## What this phase was asked

#635's four deferred findings, closed first because `read` reads through the
same heredoc pass and the same bounds. `without_heredoc_bodies` joins `\⏎`
in an unquoted body before matching the delimiter; the `HEREDOC` comment
states the operator-line bound; `without_comments`' and `runs_git`'s
docstrings say in which direction each bound can fail, from round 3's
paste-ready text re-read against the rebased tip. The #377 overview's
*Not done* sentence corrected in place with a dated note. The changelog
fragment opened. Finding 4, N2, is phase 3's.

Specific to this spawn: the plan was framed before item A (#637, squashed
as #649) landed, so open `session_cost.py` at the rebased tip before
building and say here whether anything in the plan moved.

## What this phase found

**The frame holds at the rebased tip (read, d71265b9).** A's hunks in
`session_cost.py` are the module docstring's usage lines,
`segment_slices`, `measure_segments`, `report_breaches`, the top of
`report_segments`, `emit` and `main`. None of `FAMILIES`, `HEREDOC`,
`without_heredoc_bodies`, `without_comments`, `command_words`, `runs_git`,
`family` or `analyse` is touched, and `report_segments`' foot, the 0.9.4 and
#377 comparability lines that phase 2 extends, is byte-identical. The one
fact in the frame that moved is incidental: the spec reads *there is no
`seal/ledger/` directory at 1fa25931*, and at the rebased tip there is one,
holding A's fragment and another item's. It changes nothing: this item's
fragment is a new file in it, and N2 still lives in
`seal/releases/0.15.6.md`.

**Bash was asked before the join was built (executed, bash on darwin).**
`cat <<EOF⏎body \⏎EOF⏎echo after⏎EOF` prints `body EOF` and `echo after`,
so the unquoted body closes at the second `EOF`. Under `<<'EOF'` the
backslash is kept and the body closes at the first, and `body \\` under an
unquoted delimiter closes at the first as well.

**The paste-ready guard `end < len(command)` was dropped as an equivalent
mutant.** It kept the last line of the command from joining, but a join
there ends the walk exactly as a failed comparison does, since the
delimiter pattern cannot end in `\`. A unit no case can turn red has nothing
behind it, so it is not in the tree.

**Round 3's text needed a fifth arm.** Its four shapes left a mutant that
never resets the carried text alive (every arm either closes on the joined
line or never closes). `cat <<EOF⏎body \⏎more⏎EOF⏎git push` → `git` is the
arm that kills it.

**The docstrings' examples were run, not only read (executed).**
`x="$(echo "; git log")"` and `echo $(ls)#'⏎git push'` are `git`, and
`cat <<EOF \⏎&& git push⏎x⏎EOF` is `other`, at a34c3be3.

Red first: `test_a_continued_line_in_an_unquoted_heredoc_body_closes_nothing`
failed at d71265b9's code with its first arm (`assert 'git' == 'other'`),
and the first two arms answer `git` there. Mutants, each run against the
heredoc cases alone and each exit 1: the delimiter's quoting ignored, the
parity of the backslash run ignored, the carried text never reset, no join,
and the carried text dropped.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the #377 overview's claim that each bound *answers as the rule before #377 did* | the corrected sentence and its `Corrected 2026-09-28` note in the same paragraph |
| `without_comments`' *neither worse than the rule before #377* and `runs_git`'s *an unmatched quote never answers worse* | the replacing sentences in those docstrings |
