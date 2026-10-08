# 1791384154 — review round 2 (verifying)

Target `636beccedfadcecd610732e920ac7d9a796c6ba7`. The diff under review is
round 1's fixes, `e10a7c35..38696bb0` (7706e367, 9a37a02d, 0966de0e,
38696bb0), plus e03b8a54 (the fix table) and 636becce (the close). PR #879 is
a draft into `release/v0.21.0`. The run is governed by the installed 0.20.0
rules. Probes ran in two `--no-local` clones under
`<scratchpad>/1791384154/round-2/`. Every probe file, both clones and the
venv `bin/test` built inside the first clone are deleted.

## What this round found

Round 1's eight verdicts hold, with one exception: the cutoff.

1. Seven of the eight closures are real. The rider reproduces its three
   answers at the base and at the head, the redesign refusal and the five
   `notes` sentences each go red when their code is changed, and the
   paperwork rows read correctly.
2. The cutoff works for the siblings that exist. I merged
   `origin/release/v0.21.0` (#858 and #864) into the head and ran this
   branch's `chain_check.py`. Five ⬜ rows closed `fixed` print as notices
   and nothing fails. Before the fix, all five would have been errors.
3. The premise behind the new value is still false (🟡 1). "One past the
   batch, so the first records held to it are written under it" assumes no
   0.21.0 work item is framed after the batch. The 0.21.0 milestone still
   has about ten open issues with no work item. Each of them, once framed,
   gets an id above the cutoff while its rounds still run under 0.20.0's
   `close`, which is the trap round 1 found. The changelog repeats the claim
   (⬜ 2).
4. The PR's `release` check is red at the target, and the cause is round 1's
   own record rather than the code (⬜ 3). It clears once round 2's record is
   the last one.

## 🟡 1 · The cutoff holds for the batch and not for a 0.21.0 item framed after it

`NOTES_FROM = 1791384163` at `skills/code-review/scripts/chain_check.py:863`
is the unix second 2026-10-07 14:42:43 UTC. The comment above it says the
first records held to it "are written under it". Here, "under it" means
rounds run by a `close` that refuses a ⬜ row, and that `close` does not
exist for anyone until 0.21.0 is installed.

- Executed: `date +%s` read 1791432483 at the time of this round. That is
  48,000 seconds past the cutoff, so any work item framed today is held to
  the rule.
- Read: milestone *release: 0.21.0* has 26 open issues. The batch accounts
  for 11 of them (1791384152 through 1791384162). #834, #844, #852, #853,
  #856, #857 and #871–#874 have no work item yet.
- Executed: after the merge, #864's round-1.md lines 30 and 31 also hold a ⬜
  closed `fixed`, and #858's lines 33 to 35 do too. So two of the two merged
  siblings closed a ⬜ on a fix word under 0.20.0's `close`. That is the
  normal result of the installed tool, not a rare slip.

A 0.21.0 item framed from now on is red at its own pull request the moment
it closes a ⬜ `fixed`. CI checks the merge with `release/v0.21.0`, which by
then carries this rule. The release pull request into `main` is red over the
same record. The person who meets the error followed the installed tool, and
the record has to be rewritten by hand.

Round 1's fix is correct for the batch that exists. This finding is about
the class the fix did not reach (contract §12).

The paste-ready fix takes the option that is a value change and nothing
more: hold the cutoff past anything this release can frame. Every prose copy
moves in the same commit. The other option is a decision and sits under
*Decisions left* below.

## ⬜ 2 · The changelog says every 0.21.0 work item is before the cutoff

`seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/changelog.md:21`
ends with "every 0.21.0 work item is before that and prints". That is true
today and false for the first item framed from the open milestone. The
release gathers this fragment as it stands. It moves with 🟡 1's fix.

## ⬜ 3 · The PR's `release` check is red over a 🔴 glyph in round 1's 🟢 row

- Read: `gh pr checks 879` at 636becce. Every pytest leg passes (ubuntu,
  macOS, Windows groups 1–4), and so do lint, ledger and arm-check-grammar.
  `release` fails.
- Executed: this branch's `chain_check.py` in the clone reproduces the
  failure, both as a draft and as ready. `round-1.md:36` is a 🟢 row whose
  Finding cell reads "an open 🔴 or 🟡 still holds `nobody`".
  `chain_check.open_blocking` reads a 🔴 anywhere in the row as open unless
  its verdict is a closing word, and `confirmed` is not one. When
  e10a7c35 committed the record, `Pass` was unticked and the row was
  harmless. The 0.20.0 `close` at 636becce ticked `Pass` over it.
- Read: `check_round` runs `open_blocking` on the last record only
  (`chain_check.py:5501`). So the failure clears when round-2.md becomes the
  last record, as long as round 2's own 🟢 rows carry no 🔴. This report's
  rows carry none.

#408 decided that the whole row is read, and #437 tells the reviewer to keep
the glyph out of a carried row. Neither the rule nor the checker is at fault
here; round 1's reviewer broke the rule. Correcting the cell is optional once
round 2 is the last record. The record would still read wrong to the next
person who opens it.

## Round 1's verdicts, one by one

- **Finding 1 (the rider).** Closed. Executed: `bin/test` over the rider
  module passes inside the eight-module run. A probe re-measured the three
  answers the rider records, at `5623d728` and at HEAD. Both gave one
  invocation for line 77 alone in a heredoc body, one with everything above
  it, and `_hides_a_commit` True. The probe used an unquoted `cat > … <<EOF`
  body. The rider does not name its exact shape, so this is my reading of
  "a heredoc body". Read: the stamp now reads `"## Phases"@0805cac3`, and
  CI's rider cases pass on ubuntu and on Windows group 1.
- **Finding 2 (the cutoff).** Closed for #858 and #864, open for the class.
  🟡 1 above is the answer.
- **Finding 3 (a stopped run's notes).** Closed. Read: the refusal sits in
  `build` directly after the `reframed_after` refusal. It fires only on the
  record right after the `second` (`previous_pair == stopped`), and it reads
  the stopped run through `run_of_last`, which `notes` uses too. Executed:
  with `if left:` changed to `if False:`,
  `test_the_redesign_waits_for_the_stopped_runs_notes` fails, and it passes
  when restored.
- **Finding 4 (the policy sentence).** Closed. Read:
  `docs/review-chain-spec.md:244-248` now says a ⬜ closes through `notes`
  and a 🟡 in its fix table, both `answered`, never `fixed`. That agrees with
  `close`'s ⬜ refusal and with `agents/warden.md`. Executed:
  `tests/test_docs_line_wrap.py` passes in the eight-module run.
- **Finding 5 (the unpinned refusals).** Closed. Executed: I changed each of
  the five sentences in `round_record.py` in turn (outside the run, unknown
  id, bad `Round` cell, unresolvable `--at`, already closed).
  `test_notes_names_each_row_it_cannot_apply_and_writes_nothing` failed on
  each change and passed when restored. Read: the docstring of
  `test_a_row_for_a_finding_that_is_not_a_note_is_refused` now names the case
  that asserts the already-closed refusal.
- **Finding 6 (the ledger re-reads).** Closed. Read: `Corrected · S10` and
  `Corrected · S13` replace the two `Re-read ·` rows. Each says what changed
  and cites `seal`, `close` and the cases that show it. CI `ledger` passes.
- **Finding 7 (warden.md:348).** Closed. Read: the sentence now excepts a ⬜
  the run still carries.
- **Finding 8 (orchestration.md:196).** Closed. Read: both the owner file and
  the policy now read "a ⬜ like any other".

## The smith's flag on finding 3: is this a fix pass adding a rule?

`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins
it* says "A fix pass may not add mechanism. Not a rule, not a checker, not a
template section, not a walk."

I judge that the refusal is not the mechanism that section refuses.

- It closes a hole in mechanism this branch's own build created, and that
  mechanism has not shipped yet.
- It is one branch inside an existing unit, beside a refusal of the same
  shape at the same point.
- It reuses `open_notes`, `run_of_last` and `named_notes` and adds no reader.
- The round that follows reads it, which is this round.

The case the section measured (#153/#150) built a rule, a reader and two
cases. This one adds one branch and one case. The alternative was `deferred
<home>` for a defect in code that has not shipped, which would ship a known
hole.

What the section does not do is define "mechanism", so its wording cannot
tell this case from the one it forbids. That is the section's gap, not this
fix's.

## The round 1 units nobody had reviewed

- `a_run_stopped_with_a_note` is the old case's setup moved into a helper
  that pytest does not collect. Read: the body is unchanged, and
  `test_a_stopped_run_closes_its_notes_at_the_second` now calls it.
- `test_the_redesign_waits_for_the_stopped_runs_notes` asserts the refusal
  exits 2, writes nothing, names round-3 and the open note, and names the
  `notes` command. After `notes` closes the note, it asserts the record is
  written. Executed: it goes red with the refusal removed.
- `test_notes_names_each_row_it_cannot_apply_and_writes_nothing` asserts
  exit 2, the sentence, and unchanged records for each of the five
  refusals. Executed: it goes red under each of five mutations.

I found nothing in these three units that needs a fix.

## The merge with the two merged siblings

Executed in a second clone: `origin/release/v0.21.0` (d712a632) merged into
636becce, pull-request heads fetched, and this branch's `chain_check.py` run
three ways.

| Baseline and state | Siblings | Errors |
|---|---|---|
| `release/v0.21.0`, draft | not touched by the diff, not read | round-1.md:36 (⬜ 3) only |
| `release/v0.21.0`, ready | same | round-1.md:36, plus `Broad gate` at `not yet` and `Pass` beside `nobody`, both expected before this round and the seal |
| `main`, ready (the release PR) | #858: ⬜ 6–8 `fixed`, notice. #864: ⬜ 3–4 `fixed`, notice. No open ⬜ in either run | the same three on this item only |

Neither merged sibling turns red, and arm B (an open ⬜ in the current run)
finds nothing in either. #860 and #866 are still not in `release/v0.21.0`, so
round 1's ❓ stands.

## Carried, not re-established

- The smith's "19 modules, 1,241 passed; 9 mutations red" (read, from the
  hand-back). I re-ran six mutations of my own, listed below.
- The smith's check that no work-item id at or above 1791384163 exists in
  any ref. Executed: over every branch and pull-request head I fetched, the
  highest id is 1791384162.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The cutoff's premise, that the first records held to it are written under the rule, is false for any 0.21.0 work item framed after the batch: its id passes 1791384163 while its rounds run under 0.20.0's `close`, which admits a ⬜ closed `fixed`; round 1's finding 2 is closed for #858 and #864 only | `skills/code-review/scripts/chain_check.py:863` | open | executed: `date +%s` is 1791432483; the merged clone shows #858 and #864 closed five ⬜ rows `fixed` between them under 0.20.0. Read: milestone 0.21.0 has about ten open issues with no work item |
| ⬜ 2 | The changelog fragment says every 0.21.0 work item is before the cutoff and prints | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/changelog.md:21` | open | read; false for the first item framed from the open milestone |
| ⬜ 3 | A carried confirmation in round 1's record quotes a blocking glyph in its Finding cell, so the `release` check fails at 636becce now that `close` ticked `Pass` | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/rounds/round-1.md:36` | open | executed: this branch's `chain_check.py` errors on line 36 as draft and as ready. Read: CI `release` fails on the same line; it clears when round-2.md is the last record |
| 🟢 | round 1's blocking finding is closed — the rider on smith's Phases section is re-measured and re-stamped | `agents/smith.md:87` | confirmed | executed: rider module passes; a probe gives 1, 1 and True at `5623d728` and at HEAD. Read: CI rider cases pass |
| 🟢 | round 1's finding 2 is closed for the merged siblings — #858 and #864 print and do not fail | `skills/code-review/scripts/chain_check.py:863` | confirmed | executed: chain-check over the merge, baselines `release/v0.21.0` and `main`; five notices, no sibling error. The class is finding 1 of this round |
| 🟢 | round 1's finding 3 is closed — `new` refuses the redesign's first record over the stopped run's open note | `skills/code-review/scripts/round_record.py:2626` | confirmed | executed: the case is red with the refusal disabled and green restored. Read: not the mechanism the fix-pass section refuses (see the prose) |
| 🟢 | round 1's finding 4 is closed — the policy sends a record-located note to `notes` and never to a fix word | `docs/review-chain-spec.md:246` | confirmed | read; executed: the line-wrap module passes |
| 🟢 | round 1's finding 5 is closed — the five `notes` refusals are pinned | `tests/test_a_note_closes_once_at_the_runs_end.py:644` | confirmed | executed: each of five sentence mutations red, restored green |
| 🟢 | round 1's finding 6 is closed — `Corrected · S10` and `Corrected · S13` replace the re-reads | `seal/ledger/1791384154-a-records-finding-closes-once-at-the-runs-end.md:19` | confirmed | read; CI `ledger` passes |
| 🟢 | round 1's finding 7 is closed — warden.md excepts a carried note from the answer every earlier finding needs | `agents/warden.md:348` | confirmed | read |
| 🟢 | round 1's finding 8 is closed — the owner file and the policy both read *a ⬜ like any other* | `skills/code-review/orchestration.md:196` | confirmed | read |
| 🟢 | round 1's new units read correctly and pin what they claim | `tests/test_a_note_closes_once_at_the_runs_end.py:566` | confirmed | read; executed: both new cases red under mutation |
| ❓ | The merge with #860 and #866, which edit `close` and `chain_check.py` beside these lines | `skills/code-review/scripts/round_record.py:4401` | ❓ out of verified scope | neither is in `release/v0.21.0` yet; the orchestrator answers it when it integrates them |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight modules the spawn named, in the clone at 636becce | 435 passed, exit 0 |
| this branch's `chain_check.py --baseline origin/release/v0.21.0` at 636becce, draft and ready event payloads | exit 1 both; the error is round-1.md:36; ready adds `Broad gate` and `Pass` beside `nobody` |
| a probe merge of `origin/release/v0.21.0` (d712a632) into 636becce, then `chain_check.py` with baseline `release/v0.21.0` (draft, ready) and `main` (ready) | exit 1 each, on this item's three errors only; #858's ⬜ 6–8 and #864's ⬜ 3–4 closed `fixed` print as notices |
| a probe re-measuring the rider: `commit_invocations` over line 77 alone and with everything above, and `_hides_a_commit` over the file, at `5623d728` and HEAD | 1, 1, True at both |
| a probe changing each of the five `notes` refusal sentences, then disabling the redesign refusal, each followed by its case | all six red (exit 1); both cases green after restore |
| `gh pr checks 879`, read and not run by this round | at 636becce: every pytest leg, lint, ledger and arm-check-grammar pass; `release` fails on round-1.md:36 |
| work-item ids across every fetched branch and pull-request head | highest is 1791384162; none at or above 1791384163 |
| the full suite, repository-wide lint and typecheck (the sealer's broad gate) | not yet: no run has happened at any SHA of this branch. The sealer answers it after the rounds settle |

## Paste-ready fixes

### 🟡 1

`skills/code-review/scripts/chain_check.py`, the comment and constant at
852-863. The value is 2027-01-01 00:00 UTC, past anything 0.21.0 can frame.

```python
# Where a note closed on a fix word becomes an error, as the unix second in a
# work item's directory name. NOT the id of the work item that added the rule,
# which is what the other cutoffs use: every work item framed before the
# release that ships this rule is installed runs its rounds under the
# installed 0.20.0 `close`, which demands a fix-table row for a ⬜ and admits
# `fixed` -- #858's round 1 closed three that way and #864's two. That moment
# is the release's tag, which no id known today names, so the cutoff is held
# past anything this release can frame (round 2's 🟡 1 of #837). The
# reasoning is otherwise `STRICT_FROM`'s. Measured 2026-10-07: 35 ⬜ rows of
# 14 committed records closed `fixed` before it, and they print.
NOTES_FROM = 1798761600
```

`tests/test_a_note_closes_once_at_the_runs_end.py:47-50`:

```python
# Past anything 0.21.0 can frame: its items run under 0.20.0's `close`
# (round 2's 🟡 1 of #837).
AT_THE_CUTOFF = "seal/specs/1798761600-an-item-under-the-rule"
BEFORE_THE_CUTOFF = "seal/specs/1798761599-an-item-before-the-rule"
```

`skills/code-review/orchestration.md:236-240`:

```
word is an error for a work item begun at or after `1798761600` — past
anything the release that ships the rule can frame, since every item framed
before it is installed runs its rounds under the previous `close` — and a
notice before it, and a ⬜ still open on a record of the run is an error at a
ready pull request and a notice on a draft.
```

The same value moves in `skills/implement/orchestration.md:650`, ledger N2,
`overview.md:38` and the changelog (⬜ 2).

### ⬜ 2

`changelog.md:20-21`:

```
  an open note and, for a work item begun at or after `1798761600`, over a
  note closed `fixed` — every work item framed before this release is
  installed is before that and prints. A record whose only open rows are notes now reads
```

### ⬜ 3

`round-1.md:36`, the Finding cell, glyphs written as words:

```
| 🟢 | The landing leaves only open notes out: an open blocking or should-fix finding still holds `nobody`, and `Pass` is derived from every word | `skills/code-review/scripts/round_record.py:2595` | confirmed | read: `build` and `close` filter by `carried_ids`, which takes only `note_rows`' open notes |
```

## Decisions left

- **Which cutoff for 🟡 1.** The options are below. The orchestrator settles
  it with the repository owner.
  - Hold it past the release (the paste above). The cost is that arm A is a
    notice for every 0.21.0 item. Under 0.21.0's tools that arm fires only
    on a hand edit, since `close` refuses a ⬜ row and `notes` refuses
    `fixed`.
  - Keep 1791384163 and frame no further 0.21.0 work item before the
    release, or tell every orchestrator of one to close a ⬜ `answered`. The
    second half is a written rule that only the installed plugin's documents
    would carry, and the installed documents are 0.20.0's.

## Regression tests to plant

- `tests/test_a_note_closes_once_at_the_runs_end.py`: the cutoff pair moves
  with `NOTES_FROM` (🟡 1). The parametrised case already holds both sides
  and is red at any other value.

## Facts for the evidence ledger

- N2 restated at the new value with the corrected premise (🟡 1).

Needs a fix: yes — 🟡 1 (the cutoff holds for the batch, not for a 0.21.0
work item framed after it)
Loses a record or crashes: no

## Proof block

- Opened: `rounds/round-1.md`, `rounds/round-1-fixes.md`,
  `rounds/round-1-report.md`, `routing.md`; the diff `e10a7c35..38696bb0`
  in full outside the ledger, and the ledger's word diff; the ledger
  fragment's N14, N15, `Corrected · S10` and `Corrected · S13`;
  `chain_check.py` at `open_blocking`, `check_round`, `carried_notes`, the
  cutoffs at 540-863, `main`'s arguments and the event-payload reader;
  `round_record.py` `build` at 2560-2650 and `notes`' refusals at 4925-4972;
  `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins
  it*; `agents/smith.md:70-130`; `docs/release-checklist.md` §2;
  `.github/workflows/hygiene.yml:180-220`; `bin/test`; #858's round-2-report
  verdict table (read only).
- Executed: the eight named modules once; chain-check at the head and over
  the merge; the rider, mutation and id probes; `gh pr checks 879` and the
  failing run's log (read).
- Not run: the full suite, lint and typecheck (the sealer's).
