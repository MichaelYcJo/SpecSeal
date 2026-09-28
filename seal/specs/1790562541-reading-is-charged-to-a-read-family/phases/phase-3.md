# 1790562541-reading-is-charged-to-a-read-family — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | see `plan.md`'s Status cell for phase 3 |
| Ran by | unknown — the spawn prompt did not hand the value over, and a segment's own account of itself is the one filler the template refuses |

## What this phase was asked

The ledger and the numbers. `evidence-check` at the tip names the drifted
rows; each is re-read against the edit and re-stamped in its own file with a
dated note. N2 in `seal/releases/0.15.6.md` corrected in place with a
`Corrected 2026-09-28` note (#635's finding 4, which lives there and not in
`seal/ledger/`). New rows for the read rule, the write exclusions and the
finding-1 fix go in `seal/ledger/1790562541-reading-is-charged-to-a-read-family.md`.
A `test_tmp_*` probe, deleted after, runs every transcript under
`~/.claude/projects/-Users-michael-Documents-GitHub-SpecSeal*/` through the
base's and the tip's `family`, and prints the transitions table in calls and
seconds (Q2), `other`'s share before and after, and the command words that
keep an otherwise-read line in `other` (Q3). Counts in the records, never
contents. The changelog entry names which published family rows move.

## What this phase found

**The corpus movement (executed 2026-09-28, probe
`test_tmp_read_corpus.py`, run once from the session's scratchpad and
deleted with the two module copies it loaded).** d71265b9's `family`, which
is the rebased base without this item, against b08670b6..c0cf72d5's, which
is the tip's code, on the calls the tip's `load` returns. 374 transcripts,
363 holding a Bash call, 24,223 Bash calls, 172,386 seconds.

| base | tip | calls | seconds |
|---|---|---|---|
| `other` | `read` | 7,819 | 5,221 |
| `git` | `git` | 6,458 | 45,750 |
| `other` | `other` | 5,991 | 54,667 |
| `test` | `test` | 3,447 | 64,985 |
| `lint/type` | `lint/type` | 456 | 1,620 |
| `build` | `build` | 52 | 142 |

No other transition occurs, so `read` took nothing from the four families,
and phase 1's heredoc join moved no call. `other` falls from 13,810 calls
(57.0%) and 59,889 s (34.7%) to 5,991 calls (24.7%) and 54,667 s (31.7%).
The seconds barely move because a read is fast, 0.67 s a call. `other` led
the Bash seconds in 170 of the 363 transcripts and leads in 123.

**What keeps a tip-`other` line out of `read` (Q3), in lines.** Another
command word beside a read word, 2,518; a heredoc or here-string, 2,502; a
substitution or backtick, 630; no read word at all, 327; a write, 14. The
command words most often beside a read word: `cut` 777, `python3` 578,
`evidence-check` 429, `python` 184, `survivor-check` 179, `tr` 66, `rm` 64,
`sleep` 58, `uniq` 54, `unverified-check` 52, `fold` 44, `timeout` 38,
`session-cost` 32, `round-record` 32, `cp` 28, `claude` 23, `rev` 19,
`mkdir` 17, `command` 16, `pgrep` 15, `deferral-check` 12, `which` 11,
`settle` 11, `broad-gate` 10, `uv` 9. `cut`, `tr` and `uniq` are the
candidates the admission criterion would take; the frame named them, and
the count is the owner's to act on.

**The ticket's 8,328 against 7,819.** #642's figure was an upper bound
twice over: taken at 2037cf0, before #377 took 3,691 of those calls to
`git`, and under *first after `cd`*. This rule is stricter and the corpus
has grown, so the two are not comparable one for one, and the spec made no
promise of a figure.

**The ledger (executed; `evidence-check` read directly, exit 0 lenient and
exit 0 under `--strict`, 2,578 ok and nothing drifted, at the tree this
record is committed with).** Before the re-read it named 23 drifted anchors
over nine files, which are 26 rows. Each was re-read against this item's
edit and carries a dated `Re-read 2026-09-28 by work item 1790562541 (#642)`
note; `--reverify` was then scoped with `--ledger` to those nine files and
the new fragment, and it re-stamped 38 anchors outside the fragment, every
one of them in that set. The set matches the frame's expected one: `#analyse`
in ten rows; `#family`, `#command_words`, `#runs_git`, `#without_comments`,
`#without_heredoc_bodies` and `#report_segments` in 0.15.6 N1–N6;
`#FAMILIES` and `#family` in 0.9.4 S1 and S2; the `SKILL.md` section in
twelve rows; and the two edited test cases. `#HEREDOC` did not drift,
because its comment is not part of the anchored unit. Two rows outside the
frame's list, A4 and A6 of item A's fragment, drifted because A landed
first and anchors the same `report_segments` and `SKILL.md` section.

**Three rows were corrected in place, not only re-read.** N2 (#635's
finding 4, as the round wrote it). N3, because the edit made its clause
false: the body no longer ends at the first line equal to the delimiter
when that line was joined to a continued one. N1, because *the other three
families* stopped being a count of anything once `FAMILIES` holds five.

**F5 in `seal/releases/0.8.0.md` stays in the state its #300 note
recorded.** The paragraph this item adds carries `(#642)`, an issue number
of the kind that note already says breaks the absence's wholeness; it
carries none of the case's three literals, and the case is green.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| N1's *the other three families still match anywhere* | the same clause, naming the three and `read` |
| N2's unqualified *never answers worse than the anchored rule* | the same clause, narrowed to a quote the shell leaves unmatched |
| N3's body ending at the first line equal to the delimiter, unconditionally | the same clause with the join, and R5 in this item's fragment |
| the probe and the module copies it loaded | nothing; its numbers are the tables above, R7, and the changelog fragment |
