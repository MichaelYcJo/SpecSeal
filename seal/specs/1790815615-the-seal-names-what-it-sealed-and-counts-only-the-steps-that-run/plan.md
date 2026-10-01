# Implementation Plan: the seal names what it sealed and counts only the steps that run

<!-- seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-10-01 by the repository owner, when `smith` was spawned.

## Summary

Four vertical slices over two scripts and the documents that describe them.
Each slice changes what one surface prints, pins the new text in the same
commit after seeing the pin red, and moves the prose that named the old
text. The record's `Broad gate` cell, `round_record.py`, `chain_check.py`
and every exit code are untouched throughout.

1. The `SEALED`/`NOT SEALED` heads and the hook's label name the branch,
   the base's ref and the pull request, and a recorded seal says to commit
   the cell.
2. The panel names the same things, loses `from` and `row`, prints `gate`
   only where the two copies differ, carries `drifted`, and the sample
   mirrors it.
3. `rounds` says `capped` and counts deferred findings with their homes,
   read through `chain_check.py`'s own record reader.
4. The `workflow` row and its stderr line count only the steps CI runs for
   this base, with `ONLY_AT_MAIN` declared and held against the workflow.

## Technical context

**Where the text is made** (all read 2026-10-01):

- `skills/verify/scripts/broad_gate.py`: `signal` (line 2481; `head =
  f"SEALED   {tree} against {base.commit}"` at 2491, the values dict at
  2495), `panel` (2111–2181), `gate` (2244–2442; `not_sealed` call at 2391,
  `panel` call at 2429, the `signal` write at 2441), `gate_copy` (327),
  `redirect_line`/`main` (352, 2524–2592: the redirect at 2573–2580),
  `coverage_line` (2015), `unanswered` (2004), `skipped_at_main` (1939),
  `SKIPPED_AT_MAIN` (1931), `PARTITION` (1834), `ledger_counts` (2098),
  `failure_lines` (2184), `round_count` (2103), `LEDGER_RE` (233),
  `PANEL_VALUE_WIDTH`/`ELISION` (219–220), the module docstring's stamp
  paragraph (68–82).
- `skills/verify/scripts/seal_stamp.py`: `letter` (363; `"  {label:<8}
  {value}"` is why a `""` label is a continuation line), `not_sealed`
  (414), `label` (603), `SAMPLE_ROWS` (616), `read_values` (529).
- `hooks/sealer-stamp.py#drawings` (96) calls `stamp.label(values)` and
  `stamp.stamp(values["rows"], …)`; nothing else reads the file.
- `skills/code-review/scripts/chain_check.py`: `SHA_RE` (802), `PR_FIELD`/
  `PR_RE` (811–812), `PASS_RE` (386), `NEEDS` (641), `VERDICTS` (354),
  `DEFERRED`/`HOME_WORDS`/`NO_HOME` (399–455), `table_rows` (1232), `field`
  (1179), `verdict_table` (1490), `verdict_of` (1602). The reader object
  those take is the one `round_record.where` builds; `broad_gate.py`
  already loads sibling scripts by path (`load`, line 240), and
  `round_record.py seal` shows how the record on disk is read
  (`read_text`, `reader.readable`, `chain.table_rows`).
- `.github/workflows/hygiene.yml`: the `!= "main"` guards at lines 66, 116,
  135, 347; the `= "main"` guards at 250, 303.
- Tests: `tests/test_the_seal_is_taken_once_by_the_sealer.py` (4018 lines;
  `sealed_values`, `signal_lines`, `row_of`, `values_files`; the #475 cases
  752–885; the #400 cases 2370–2520), `tests/test_the_gate_asks_the_range_ci_will_ask.py`
  (549–592, 786–799), `tests/test_the_gate_names_every_step_ci_runs.py`
  (`FIXTURE_WORKFLOW` 509, `panel_rows` 529, the A6 case 551, `HISTORICAL_ROWS`
  696, the #473 block 896–1055 with `SKIPS_AT_MAIN` and `workflow_step` from
  `tests/conftest.py` 145), `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`
  (`values()` fixture 27–60, label pins 246/294/315),
  `tests/test_a_gate_that_fails_says_so.py` (old-shape values at 593, label
  prefix at 621).

**Constraints the design is chosen under.**

- A panel value is 23 columns and is cut at the frame with no marker
  (`letter`); the whole stamp is 81 columns at 0.90. Four of the ticket's
  values are 26–33 columns.
- `panel` is drawn on success alone, so every exit code on it is 0 and,
  under `--strict`, so are `drifted` and `broken`.
- The values file is written by the tree's gate and read by the installed
  hook, which may be a release older: new keys must be ignorable, and
  every row must stay a `[str, str]` pair.
- The redirect in `main` is a subprocess with the same argv; the child has
  no channel to the parent today but the environment.
- `chain_check.py` is the one reader of a round record. A second verdict
  parser in the gate is the split this repository's docstrings refuse
  everywhere (`hooks/config.py`'s argument, `broad_gate.py#rows_read`).

**What breaks in six months.** A fifth step gains a `!= "main"` guard and
nobody extends `ONLY_AT_MAIN`: the guard case (A13) goes red, which is the
intended failure. A sixth separator spelling (`·`) creeps into a panel value
from a ticket: the width case still holds, and the ASCII rule is one
sentence in `panel`'s docstring that a reviewer may or may not read — named,
not closed. A step whose guard is on something other than the base
(`github.event_name`, a label) is outside both lists, as `SKIPPED_AT_MAIN`'s
docstring already says of itself; the class stays open for the next kind.
The `gate` row's content comparison reads one file; a tree that changed
`chain_check.py` and not `broad_gate.py` prints no row, which is the stated
bound of *the tree's gate* meaning the one file the ticket names.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Widen `PANEL_WIDTH` so the ticket's one-line values fit (36 → about 46) | The stamp goes from 81 to about 91 columns, past what the owner looked at when the 0.90 scale was chosen over six renderings (#400); a narrower terminal wraps the disc, which the computed-circle argument exists to make impossible | Rejected; `questions.md` Q1 carries it as the owner's to reverse |
| The ticket's one-row form, `tree 3b76ca2a (feat/585-...)`, elided to fit | Exactly 23 columns leaves twelve for the branch name; this branch's name reads `feat/666-the` and the base's ref `...e/v0.16.0`, which tells a reader less than the row it replaces | Rejected; a continuation line gives the name the full 23 |
| Name the base by the spelling the caller typed (`release/v0.16.0`), as the ticket's example shows | #423's reader could not tell a fresh base from a local ref a week behind it, and the resolved ref is the only thing on the stamp that says which; the given spelling is what the `moved_line` already compares it to | Rejected; the tree wins, `spec.md` Grounding row 2 |
| Print `gate` only where a redirect happened (tree copy ran) | In this repository every seal is redirected, so the row prints on every stamp and says nothing, which is the owner's complaint; everywhere else it never prints | Rejected |
| Print `gate` only where the two copies' **versions** differ | Within a release cycle the tree's `plugin.json` equals the installed one until the release pull request bumps it, so a branch that changed the gate — the #475 case — prints no row exactly when it matters | Rejected |
| Compare the two copies' **bytes**, the installed path handed to the child in the environment | Reads one file, so a tree that changed a sibling arm and not `broad_gate.py` hides the row; and a tree copy invoked directly has no installed path to compare to | **Chosen**; both bounds stated in `gate_copy`'s docstring, and the direct invocation prints the row (says more when unsure) |
| Drop `row` as a constant and change nothing under `suite` | Reads as the frame deciding what the owner may see; `chain exit 0` is as constant and was kept, so the principle would be half-applied | Rejected; the exit continues under `suite`, which is the ticket's fold within the width |
| Read `capped` off the presence of `deferred` verdicts | A finding deferred mid-run by choice (to `seal/follow-up.md`) is not a capped run; and a capped run whose every open finding was fixed on the branch has no deferral | Rejected; `Needs a fix: yes` on a record `seal` accepted is the tree's own definition (`skills/verify/SKILL.md`), and the deferred count is read from the table regardless |
| Read the base guards off `hygiene.yml` at run time and derive the count | A second reader of inline shell in the gate, which `PARTITION`'s comment and #473's spec both refuse as a second reading of one question; and it would run in every repository whose workflow happens to carry the job name | Rejected; declare `ONLY_AT_MAIN` and hold it with a case, as `SKIPPED_AT_MAIN` is held |
| A column in `PARTITION` saying when each step runs, instead of a second tuple | Changes the three-tuple every existing case and `mirrored()` read, for four rows; the existing tuple already set the shape for a base-keyed list | Rejected for this item; worth revisiting if a third kind of guard ever appears |
| Keep `·` and `→` on the panel as the ticket spells them | A console that is not UTF-8 is what the letter twin exists for, and `reconfigure(errors="replace")` turns both into `?` there | Rejected; ASCII ` . ` (already the `ledger` row's) and `->` |
| Put the drifted count on the panel only | On a drawn panel it is 0 by `--strict`; the refusal the ticket calls common is seen on `NOT SEALED`, where the `total:` line is the last line of output and `failure_lines` quotes the first eight | Both: the panel row as asked, and the failure form's `ledger` entry ends with the `total:` line |
| Look the pull request number up through `gh` where the record reads `not yet opened` | The gate reads no network and carries no token, which is `PARTITION`'s own reason for not mirroring the milestone step | Rejected; `item` prints the id alone |

## Phases

Vertical slices — each phase ends with something runnable and verified.
Each phase drafts its ledger rows and writes them to
`seal/ledger/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run.md`
at its boundary, with its `phases/phase-N.md`, and each pin is seen red
before it is committed (contract §15; say in the phase record how).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The lines name what they sealed, and a recorded seal says to commit the cell** (S1, S2). `broad_gate.py`: a `branch_name(root)` reader (`git symbolic-ref --short -q HEAD`, `None` when detached); `signal`'s head and `not_sealed`'s head in the `<branch> @ <tree> against <ref> @ <commit>` shape with the detached and bare-commit collapses; the values dict gains `branch` and `pr` (the `PR` row read through `chain_check.PR_RE`, which phase 3's reader shares); one new constant printed after the `SEALED` line on a recorded seal. `seal_stamp.py`: `not_sealed` takes the names; `label` reads them and falls back. Docs: `agents/sealer.md` exit-0 bullet; `skills/code-review/orchestration.md` §*The stamp is drawn for you* names the new line beside the `SEALED` one; `broad_gate.py` docstring paragraph *The failure form is …* | `tests/test_the_seal_is_taken_once_by_the_sealer.py` (A1–A3: `signal_lines` assertions at 2370–2400 and the `NOT SEALED` cases; a new case for the commit line, and its absence on `NOT SEALED` and without `--record`); `tests/test_the_gate_asks_the_range_ci_will_ask.py` A6 (575–578) and A7 (581–592); `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` label pins (246, 294–295, 315) moved to the new shape plus one case for the fallback; `tests/test_a_gate_that_fails_says_so.py` line 621 **unchanged and green** (A15's compatibility); document pins for the two sentences, seen red with the sentence deleted | 15f6ff39 |
| 2 | **The panel names the branch, the base's ref and the work item, and loses the rows that said nothing** (S3, S6 for the panel). `panel`: the continuation rows for `tree`/`base` with head/tail elision; `item`; `gate` conditional on a byte comparison, the installed path handed over by `main`'s redirect in the environment; `from` and `row` removed; `suite`'s `exit N` continuation; `ledger_counts` carries `drifted` and `ledger` continues; `failure_lines` ends a failing `ledger` with its `total:` line; a width guard asserting every value ≤ `PANEL_VALUE_WIDTH` at the point rows are built. `seal_stamp.py`: `SAMPLE_ROWS` mirrors the panel. Docs: `agents/sealer.md` (the `gate` paragraph, *base beside `from`*), `docs/the-broad-gate.md` #475 paragraph, `skills/verify/SKILL.md`'s *names the ref beside the commit* sentence, `broad_gate.py` module/`panel`/`gate_copy` docstrings, the `SAMPLE_ROWS` comment. Ledger: `0.12.2` R5 re-read, `0.15.1` G2 corrected in place, `0.15.7` N5 extended | `tests/test_the_seal_is_taken_once_by_the_sealer.py`: `test_the_values_file_holds_this_runs_panel` (A5) rewritten to S3's sequence; the #475 cases 817–885 (A8, four shapes: identical copy, differing copy, no gate, direct invocation); A7 `item` cases; A9 `suite`/`ledger` cases and the `ledger` failure-form case (A4's second half); a width case over the longest inputs rendered through `stamp(shape=True)` (A6); A16 sample-vs-panel. `tests/test_the_gate_asks_the_range_ci_will_ask.py` 549–572 (`("from", …)` becomes the `base` continuation; the rendered regex reads the row under `base`) and 786–799 (the document pin names the row that now carries the ref). `tests/test_the_gate_names_every_step_ci_runs.py` `HISTORICAL_ROWS` (A14) and `panel_rows`. `test_the_panel_renders_its_rows_and_its_blanks` gains a `""`-labelled row. Each pin red first | 998adaea |
| 3 | **`rounds` says capped and counts the deferred findings with their homes** (S4). `broad_gate.py` loads `chain_check.py` by path and reads the item's last record from the working tree the way `round_record.seal` does: `Needs a fix` through `field`, the verdict rows through `verdict_table`/`verdict_of`, homes deduplicated in table order; `rounds <R> . capped` and the `<k> deferred -> <homes>` continuation; the `PR` read of phase 1 moves onto this reader if phase 1 wrote a narrower one. `round_count` stays the count. Docs: `agents/sealer.md` exit-0 bullet names the row; `broad_gate.py` module docstring (*the round count*) | New cases in `tests/test_the_seal_is_taken_once_by_the_sealer.py` over fixture records (A10): the capped shape with two `deferred #664`, two homes, a `deferred (no home)`, `Needs a fix \| no` with no deferral, a record with no `## Verdicts`, a `broad-gate.md` home; the width case of phase 2 extended with the longest `rounds` continuation; `questions.md` Q2's measurement run and recorded in `phases/phase-3.md` | 8a724d2d |
| 4 | **The `workflow` row and its line count only the steps that run for this base** (S5, S6 for the count). `ONLY_AT_MAIN` beside `SKIPPED_AT_MAIN` with the four names; `base_is_main(given)` shared with `skipped_at_main`; `steps_for(workflow, given)`; `unanswered`, `coverage_line`, `panel` keyed on it; the stderr line's clause naming how many steps are left out for this base and why. Docs: `skills/verify/SKILL.md` §*A seal says what it did not answer* and §*What the count does not say*; `agents/sealer.md`'s release-pull-request paragraph; `docs/the-broad-gate.md` (the #468 paragraph gains the sentence that a step CI does not run for this base is outside the count); `PARTITION`'s comment block | `tests/test_the_gate_names_every_step_ci_runs.py`: a twin of the `SKIPS_AT_MAIN` guard case over `!= "main"` (A13, both sides, seen red by editing a guard in a fixture copy); the A6 case (551) with `FIXTURE_WORKFLOW` gaining a guarded step and the base passed; cases over the real workflow's names for `4 of 9` and `8 of 11` (A11, A12) with the stderr clause pinned; the #473 cases 959–1012 still green; `test_a_seal_that_answers_every_step_says_so` keyed on the base. `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_the_gate_reads_the_given_base_exactly_once` (467) — `base.given` gains readers, so that case's count moves and says why | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **No migration, no new dependency, no new environment variable a person
  sets.** The one new variable is set by `main` for its own child on the
  redirect and read by nobody else.
- **Compatibility across the install boundary.** The values file the tree's
  gate writes is drawn by whichever hook is installed; the installed 0.16.0
  hook ignores `branch` and `pr` and draws the new rows under its old
  label. A pending file written before this change draws today's label
  through the new `label`. Both directions are asserted (A15).
- **The sealer's report changes by one line** (the commit-the-cell line),
  which `agents/sealer.md` already tells it to pass on whole.
- **Failure direction and prompt budget** (`CONTRIBUTING.md`): the gate
  blocks nothing it did not block and allows nothing it did not allow; no
  exit code moves; zero questions reach a person.
- **A sibling branch, `feat/638-…` (`broad-gate --preflight`), edits the same
  file into the same release.** Its hunks are expected in `gate`/`main`
  (running the record arms first) and this item's in `panel`, `signal`,
  the partition block and `seal_stamp.py`; whichever squashes second merges
  `origin/release/v0.17.0` in — never a rebase, because every round record
  names the branch's commits by `Target SHA` (`docs/release-checklist.md` §0)
  — and re-takes its seal, as `docs/the-broad-gate.md` §*Nothing edits
  between the broad seal and the PR* requires. (Corrected by the
  orchestrator before approval, where the frame said rebase.)
- **The changelog fragment** goes in this directory's `changelog.md`; it says
  what a person now sees on the stamp, the two lines, and the count, in that
  order.
