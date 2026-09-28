# Implementation Plan: reading is charged to a `read` family (#642)

<!-- seal/specs/1790562541-reading-is-charged-to-a-read-family/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-28 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

`family` gains a fifth answer, `read`, for a call whose every command only
reads: a read word from #642's list, with nothing else on the line but
neutral words, no write, no heredoc and no substitution. It is judged last,
so the four existing families keep every call they have. First, #635's four
deferred findings are closed in the same passes `read` reads through. One
file of code, `skills/verify/scripts/session_cost.py`, plus its cases, one
`SKILL.md` paragraph, the changelog fragment, the ledger, and two
corrections in records #377 left.

## Technical context

All read at 1fa25931 plus the routing commit cb4a9f33.

- `skills/verify/scripts/session_cost.py#FAMILIES`: four `(name, pattern)`
  pairs. `#family` removes heredoc bodies, then asks `runs_git` for `git` and
  the patterns for the rest, first match wins.
- `#command_words` is one `shlex` walk over `without_comments`' output. It
  tracks substitution depth and yields only command words. `read` needs the
  arguments and redirections of each command too, which the walk sees and
  discards; phase 2 factors it (spec, Data & interfaces).
- `#analyse` calls `family(call["ran"])` for the `by_family` table and the
  repeats filter. Neither call site changes. The repeats filter keeps `test`,
  `lint/type` and `build`, so `read` does not reach it.
- `#report` prints `by_family` generically, so a `read` row prints with no
  edit there.
- `#report_segments` ends with the 0.9.4 and #377 comparability lines.
  `test_the_reading_says_its_family_rows_moved_at_377` pins the second.
- `hooks/cmdline.py` is not reused, for #377's reason: the two trees do not
  import each other (`session_cost.py#newest`), and the gate reads a heredoc
  body as shell.

**The order against item A (#637).** A edits `resume_cuts`,
`segment_slices`, `report_segments`' empty branch and `main`, and the
`SKILL.md` item *A resumed agent is one row per slice*. It is built first.
This branch holds nothing but `seal/specs/1790562541-…/` when A squashes, so
it is rebased onto `release/v0.15.7` **before phase 1**, and that rebase
cannot conflict. What the build then shares with A:

| Unit | A | This item |
|---|---|---|
| `session_cost.py#report_segments` | the empty branch, at its top | the comparability line and its comment, at its foot |
| `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* | the resumed-agent item | a paragraph after the #377 one |
| `tests/test_session_cost.py` | resumed-segment cases | family cases and the comparability case |
| ledger rows on `#report_segments` and the `SKILL.md` section anchor | re-stamped by A | drift again here, and are re-read against the rebased tip in phase 3 |

Everything else this item touches (`FAMILIES`, `HEREDOC`,
`without_heredoc_bodies`, `without_comments`, `command_words`, `runs_git`,
`family`, `analyse`'s docstring) A does not.

**Failure scenario, six months out.** An agent reads through a word not on
the list (`jq`, `cut`, `stat`), or behind a wrapper (`timeout 30 rg`), and
the call reads `other`, as every call does today. The `FAMILIES` comment
states the admission criterion, so adding the word is a one-line change with
a reason. The mirror failure, a write read as `read`, needs a write the
walk cannot see: a `w` command inside a quoted `sed` script, or an awk
program's `print > "f"`. The `read` docstring names both as bounds.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `read` when **any** command word is a read word (the `runs_git` shape) | a pipe into `head`, `tail` or `grep` sits behind nearly every command: `./bin/deploy --wait \| tail -3` and `python3 x.py \| head` become reading. The existing `other`-note case holds that fixture and turns red | rejected. S4 is its mutant |
| `read` when the **first command after `cd`** is a read word (the ticket's measurement) | `ls && rm -rf x` and `grep x f; python3 build.py` become reading | rejected. It is kept as the ticket's upper bound only |
| Match read words by pattern anywhere (the other three families' shape) | `python3 sort.py`, `echo cat` and `rm -r find/` become reading, #200 from the other side | rejected |
| A `python3 -` heredoc family beside `read` | the owner answered no. A vehicle, not a kind of work, and it moves with the `Edit`-versus-shell choice, which confounds #640 | rejected by the owner, 2026-09-28 |
| Judge `read` before `git` or the three pattern families | `ls && git status` becomes reading, and `grep -rn pytest` moves out of `test`, which #642 lists as *what must not break* | rejected. S7 is its mutant |
| Look inside a substitution, as a later `git` rule might | `x=$(rm y); ls` becomes reading, and quoted substitutions cannot be seen, so the family would depend on quoting | rejected. A substitution disqualifies |
| Fall back to a pattern when the tokeniser refuses | there is no older `read` answer to fall back to, and any pattern is the anywhere-match rejected above | rejected. A refused line is not `read` |
| Widen the word list now (`cut`, `tr`, `jq`, `uniq` …) | the numbers stop being comparable with the ticket's, and `uniq in out` writes | rejected for this item. Q3 counts the candidates |
| Leave #635's findings to a later item | `read` reads through the same heredoc pass and the same bounds, so it would inherit finding 1 and the false sentences in finding 2 on the day it ships | rejected. They are phase 1 |
| A second tokeniser pass for arguments | two answers to "what is a command" in one file, which is the split #377's plan refused for heredoc bodies | rejected. One walk |

## Phases

The branch is rebased onto `release/v0.15.7` after item A squashes and
before phase 1. Each phase runs the module it edits
(`bin/test tests/test_session_cost.py`) and the modules that read what it
edited (`grep -l` at the tip for `SKILL.md` readers). Each new case is seen
red first (contract §15), against the rebased base or by reverting the
phase's edit, and the phase record says which. No phase runs the full suite,
lint or typecheck (contract §2); the sealer owns that.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#635's four findings.** `without_heredoc_bodies` joins `\⏎` in an unquoted body before matching the delimiter; the `HEREDOC` comment states the operator-line bound; `without_comments`' and `runs_git`'s docstrings say which direction each bound can fail in (round-3-report §*Paste-ready fixes* 🟡 1 and 🟡 2, taken as the starting text and re-read against the rebased tip). `seal/specs/1790550714-…/overview.md` §*Not done* corrected in place with a dated note (⬜ 3). The changelog fragment is opened with the entry | S9 as a case, red at the rebased base. A mutant that ignores whether the delimiter is quoted turns the third arm red. The existing heredoc, comment and refusal cases pass unchanged | a34c3be3 |
| 2 | **The `read` family.** The walk factored so one pass yields each simple command's words and redirections, with `command_words` derived from it and unchanged. The read rule (spec In §1–§4), judged after the four. Statements in the same commit: `FAMILIES` comment (the fifth family and the admission criterion), `family` docstring, the bounds sentences from phase 1 extended to `read`, `analyse` docstring (the third move), `report_segments`' comparability line and comment (#642), the `SKILL.md` paragraph, the two edited test arms and docstrings, the changelog entry | S1–S8 and S10 as cases, each red before the family exists. Mutants, each killed: *any read word* (S4), no redirection check (S3), no `sed -i` check (S3), no heredoc check (S5), no substitution check (S5), `read` judged first (S7), `/dev/null` accepted for any target (S3), deleting the #642 sentence (S10). S11 holds | f57df573 |
| 3 | **The ledger and the numbers.** `evidence-check` at the tip names the drifted rows; each is re-read against the edit and re-stamped in its own file with a dated note. N2 in `seal/releases/0.15.6.md` corrected in place (⬜ 4). New rows for the read rule, the write exclusions and the finding-1 fix go in `seal/ledger/1790562541-reading-is-charged-to-a-read-family.md`. A `test_tmp_*` probe, deleted after, runs every `*.jsonl` under `~/.claude/projects/*SpecSeal*/` through the base's and the tip's `load` and `family`, and prints: a transitions table in calls and seconds (Q2); `other`'s share of Bash calls and seconds before and after; and the command words that most often keep an otherwise-read line in `other` (Q3). Any number the `SKILL.md` paragraph or the changelog cites is the tip's | S12: `evidence-check`'s exit code read directly (contract §1), with no un-re-read DRIFTED row of this work's. S13: the probe's tables in `phases/phase-3.md` | |

## Operational impact

- No new dependency, environment variable or migration.
- **Compatibility:** the `by family` block may print a new row, and `--json`'s
  `by_family` may carry a `read` key. A reading taken before the release
  that carries #642 has no `read` row, and its `other` row holds those
  calls. `--segments` says so on the page; `SKILL.md` and the changelog say
  so where a person comparing readings meets it. Nothing else printed moves.
- **Squash order:** milestone 50 builds A before this item. The ledger files
  both items may re-stamp (`seal/releases/0.15.6.md` at least) are the
  likely conflict surface only if the two ever run at once. They do not:
  this item's ledger phase runs on a tree that already holds A. If a
  conflict appears anyway, resolve hunk by hunk, never `--ours` or
  `--theirs`, then run `evidence-check`.
