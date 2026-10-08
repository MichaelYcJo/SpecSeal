# 1791384154 — review round 3 (verifying, the run's last)

Target `fe3480d26d257d521e40b0aeb86e2159fee9192a`. The diff under review is
round 2's fixes, `be3c452a..b0e52bb2` (23f22eb4 and b0e52bb2), plus f8f8b85a
(the fix table) and fe3480d2 (the close, written with the installed 0.20.0
generator). PR #879 is a draft into `release/v0.21.0`. Round 2's `New units`
is `none`, so this round answers round 2's three verdicts and nothing else.
Probes ran in one `--no-local` clone under `<scratchpad>/1791384154/round-3/`.
The clone, its `.venv`, the probe file, the event payloads and the captured
output are all deleted.

## What this round found

Round 2's three verdicts hold. Nothing this round found needs a fix.

1. The five carriers state one assumption, and state it truly: the cutoff
   is right while no 0.21.0 item is framed after the batch, and whoever
   frames one moves it. None of them says anything wider.
2. The grounds sentence in front of that assumption, in `NOTES_FROM`'s
   comment, says more than the owner's answer did (⬜ 1).
3. The two new survivors are true where they stand, and `survivor-check`
   names exactly those two.
4. Round 2's ⬜ 3 answer holds: the PR's `release` job passes at
   `fe3480d2`, and `chain_check.py` names nothing on `round-1.md` at the
   head or over the merge.
5. Two places outside the diff still describe this run wrongly. They are
   the PR body (⬜ 2) and `overview.md`'s *Not verified* row (⬜ 3). The run
   ends with this round, so nothing later will catch them.

## Round 2's should-fix finding 1: the five carriers say one thing

Read, side by side at `fe3480d2`:

| Carrier | What it says |
|---|---|
| `skills/code-review/scripts/chain_check.py:860-865` | assumes no item of that release is framed after the batch; whoever frames one moves the cutoff past its id in the same change |
| `skills/code-review/orchestration.md:239-241` | assumes no item of that release is framed after the batch; one that is moves the cutoff past its own id in the same change |
| `tests/test_a_note_closes_once_at_the_runs_end.py:47-50` | holds while no item of that release is framed later; `NOTES_FROM` says what moves it |
| ledger N2 | holds while no item of that release is framed after the batch, and the constant's comment says one that is moves it past its own id |
| `changelog.md:21-24` | the eleven items framed with this one are before the cutoff and print; one framed later for this release moves the cutoff past its own id |

All five name the same condition and the same remedy. None widens it. The
two copies the fix left alone, `overview.md:38` and
`skills/implement/orchestration.md:650`, state the value and the batch and
make no claim about later items, so they are not wider either.

I then checked whether the assumption is true today and whether it is the
right one.

- **The batch is what the comment says.** Read: the #834 handoff on
  `chore/834-every-reader-and-record-is-inventoried` lists the eleven items
  as 1791384152 through 1791384162. #834's build is 1791382684, which is
  before the batch.
- **#860's reframe keeps a batch id.** Executed: the work item on
  `fix/860-a-fix-range-is-its-own-commits-across-a-merge` is still
  1791384160, and its reframe commit 4d18c8e0 wrote into that directory. So
  the reframe the orchestrator named does not break the assumption.
- **No id at or past the cutoff exists in any local ref.** Executed: the
  highest on the release branch is 1791384162, and on the #834 and #860
  branches it is 1791382684 and 1791384160.
- **The condition is the right one.** An item's rounds run under 0.20.0's
  `close` only while 0.20.0 is installed, and that is the 0.21.0 build
  window. A 0.22.0 item runs its rounds on `release/v0.22.0`, after 0.21.0
  ships. So "no item of that release framed after the batch" is the whole
  condition, not part of it.
- **The siblings' count is right.** Executed: on `origin/release/v0.21.0`,
  #858's `round-1.md` closes ⬜ 6, 7 and 8 `fixed` and #864's closes ⬜ 3
  and 4 `fixed`. That is the "three" and "two" the comment states.

What the assumption leaves is round 2's second option, which round 2 put
under *Decisions left* and the fix pass took. The obligation to move the
cutoff reaches a later framer only through these five carriers. If it is
missed, that item's pull request fails `chain-check` with a message that
says to close the note through `round-record notes`, which the installed
0.20.0 does not have. The failure is loud and loses no record, so I record
it here and not as a finding.

## ⬜ 1 · The comment says the owner fixed the scope; the owner declined to split it

`skills/code-review/scripts/chain_check.py:861` reads "The owner fixed the
release's scope at the batch on 2026-10-08, and the rule holds while that
does."

- Read: the owner's answer is the #834 handoff's answer 7, "Release size:
  all eleven work items ship in 0.21.0". It answers question 7, which asked
  whether to split a release of eleven items plus #834's build. The owner
  said not to split. Nothing was said about framing no more.
- Read: the release also carries #834's build (1791382684), which is not in
  the batch. It sits before the cutoff, so the value is unaffected.
- Executed: milestone *release: 0.21.0* still has 26 open issues. #871 to
  #874 are follow-ups the frames asked for, and none is framed.

The value and the assumption are right. Only the grounds overstate what the
owner decided. A reader may conclude that the four follow-ups cannot reach
this release, and that is exactly the case the next sentence warns about.

## ⬜ 2 · The PR body still names the cutoff round 1 moved

Read: PR #879's body, the `chain-check` row of *What changes*, says "for a
work item begun at or after `1791384154`". Round 1's fix moved that value
to `1791384163`, and round 2's fix added the assumption. The body was never
updated. The body's *How it was checked* also says "This pull request's own
review is the first run under the new rule". That is false, for the reason
⬜ 3 gives.

Executed (`gh api`): the repository's squash message is set to
COMMIT_MESSAGES. So the body does not land in `release/v0.21.0`'s history.
It is still what a reader of the pull request and of #837 sees. Editing it
is a GitHub write, which is the orchestrator's act.

## ⬜ 3 · `overview.md` hands a check to rounds that never ran under the rule

`seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/overview.md:29`
lists, under *Not verified*, "`notes`, `close`'s carried note and the two
`chain-check` arms on a real run". It gives "this item's own review rounds
are the first run under the rule" as its premise and the orchestrator,
"over this item's review rounds", as its answerer.

- Read: every close in this run used the installed 0.20.0 generator. The
  spawn prompt says so for fe3480d2, and round 2 says so for 636becce.
- Read: `rounds/round-2-fixes.md` carries rows for ⬜ 2 and ⬜ 3. This
  branch's `close` refuses a row for a note (round 1's verdicts, confirmed
  in round 2). So round 2's close cannot have been this branch's `close`.

This round is the last. The row's answerer will therefore never answer it,
and the row goes to `settle` saying it was covered. This is paperwork under
`seal/specs/`, so it is a correction and stays out of `Needs a fix`.

## Round 2's note 2: the changelog

Closed. Read: `changelog.md:21-24` names the eleven items, says they run
under the previous `close` and print, and says one framed later moves the
cutoff. That is true today. A release-note reader may find the last clause
odd once 0.21.0 ships, but it is not false.

## Round 2's note 3: the `release` job is green at the head

Closed.

- Read: `gh pr checks 879`. `release` passes, in run 37727085383, with
  `headSha` `fe3480d2` and event `pull_request`. Its log reads
  "chain-check: judged as a draft pull request".
- Executed: this branch's `chain_check.py --baseline
  origin/release/v0.21.0` at `fe3480d2` exits 0 as a draft. As ready it
  exits 1, on two errors: `Broad gate` reads `not yet`, and `Pass` sits
  beside `nobody`. Both are on `round-2.md`, and both clear when this
  round's record and the sealer's run land. Neither names `round-1.md`.
- Executed: the same check over a probe merge of `fe3480d2` into
  `d712a632` gives the same result. `d712a632` is the release branch tip
  that GitHub reports, and the merge is what CI checks out.

`round-1.md:36` still carries the glyph in a 🟢 row. `check_round` reads
only the last record, so this round's record has to carry no blocking glyph
in any confirmed row, and it carries none. The cell still reads wrong to
anyone who opens round 1. Round 2 already judged that optional.

## The two survivors

Both are true where they stand.

- `routing.md:17`, "The owner pressed `automation` for every 0.21.0 work
  item in one batch". Read: the #834 handoff's *The owner's batch
  (2026-10-07)* says routing for every 0.21.0 work item is `automation`. The
  sentence says nothing about the cutoff.
- `chain_check.py:739`, "rule, so the first records held to it are the ones
  written under it.". Read: it belongs to `REOPEN_FROM = 1788597030`. Read:
  1788597030 is the work item of #161's branch, which `seal/releases/0.8.1.md`
  records as adding the reopening walk. So the value is the id of the item
  that added its rule, which is what the sentence assumes.

Executed: `survivor-check --range be3c452a..fe3480d2` names exactly these
two places and exits 1. With `--exempt survivors.md` it exits 0, and both
are excused. Over `origin/release/v0.21.0...fe3480d2` with the same
exemptions it exits 0, with one excused place (`agents/smith.md:199`).

## Carried, not re-established

- The smith's "12 modules, 553 passed", `rider_check.py` exit 0 and
  `evidence-check --strict` exit 0 (read, from the hand-back). I ran the
  three modules the fix touches. CI's `ledger` job passes at `fe3480d2`.
- Round 2's chain-check over the merge with `main` as the baseline, where
  the siblings' five notes print. I re-counted the notes but did not rerun
  that baseline.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `NOTES_FROM`'s comment says the owner fixed the release's scope at the batch; the owner's answer 7 declined to split the release, the release also carries #834's build (1791382684, before the batch), and #871 to #874 sit unframed in its milestone | `skills/code-review/scripts/chain_check.py:861` | open | read: the #834 handoff, answer 7 and question 7; executed: the milestone holds 26 open issues. The value and the assumption are right; only the grounds overstate |
| ⬜ 2 | PR #879's body names the cutoff `1791384154`, which round 1 moved, and calls this review the first run under the new rule | `PR #879 body:19` | open | read: `gh pr view 879`; executed: the squash message is COMMIT_MESSAGES, so the body does not reach git history. A GitHub write, the orchestrator's |
| ⬜ 3 | `overview.md`'s *Not verified* row hands the real-run check to this item's own rounds, which all closed with the installed 0.20.0 generator | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/overview.md:29` | open | read: `round-2-fixes.md` carries rows for two notes, which this branch's `close` refuses; a correction, not counted by `Needs a fix` |
| 🟢 | round 2's should-fix finding 1 is closed — the five carriers state one assumption, no item of the release framed after the batch, and one remedy, and none says more | `skills/code-review/scripts/chain_check.py:868` | confirmed | read: the five side by side; executed: no work-item id at or past 1791384163 in any local ref, #860's reframe keeps 1791384160, and the siblings' fix-word notes are three and two |
| 🟢 | round 2's note 2 is closed — the changelog names the eleven items and what moves the cutoff | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/changelog.md:21` | confirmed | read |
| 🟢 | round 2's note 3 is closed — the `release` job is green at the head and nothing names `round-1.md` | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/rounds/round-1.md:36` | confirmed | read: CI `release` passes at `fe3480d2`, judged as draft; executed: `chain_check.py` at the head and over the merge, draft exit 0, ready exit 1 on `Broad gate` and `Pass` beside `nobody` only |
| 🟢 | the two survivors b0e52bb2 adds are true where they stand | `seal/specs/1791384154-a-records-finding-closes-once-at-the-runs-end/survivors.md:12` | confirmed | executed: `survivor-check` names exactly those two and exits 0 with the exemptions; read: `REOPEN_FROM` is 1788597030, the item that added the reopening |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_a_note_closes_once_at_the_runs_end.py`, `tests/test_docs_line_wrap.py` and `tests/test_the_rules_have_one_owner.py`, in the clone at `fe3480d2` | 134 passed, exit 0 |
| `survivor-check --range be3c452a..fe3480d2`, bare | exit 1; two places, `routing.md:17` and `chain_check.py:739` |
| the same with `--exempt` over this item's `survivors.md` | exit 0; both excused |
| `survivor-check --range origin/release/v0.21.0...fe3480d2` with the same exemptions | exit 0; one excused, `agents/smith.md:199` |
| `chain_check.py --baseline origin/release/v0.21.0` at `fe3480d2`, draft and ready event payloads | draft exit 0, a notice for `Pass` beside `nobody` on `round-2.md`; ready exit 1, `Broad gate` at `not yet` and `Pass` beside `nobody`, both on `round-2.md`; nothing on `round-1.md` |
| a probe merge of `fe3480d2` into `d712a632` (the base tip GitHub reports), then the same two runs | the same exits and the same messages |
| the notes rows of #858's and #864's records on `origin/release/v0.21.0` | #858 round 1: notes 6 to 8 `fixed`; #864 round 1: notes 3 and 4 `fixed`; every other note `answered` |
| work-item directories on the release, #834 and #860 branches | highest 1791384162; #860's is 1791384160 |
| `gh pr checks 879`, read and not run by this round | at `fe3480d2`: `release`, `ledger`, `lint` and `arm-check-grammar (3.13)` pass; the pytest legs and `arm-check-grammar (3.14)` were still pending when read |
| `gh api` reads: PR #879's base and merge, the release branch tip, the repository's squash setting, milestone 58 | base tip `d712a632`; squash message COMMIT_MESSAGES; 26 open issues |
| the full suite, repository-wide lint and typecheck (the sealer's broad gate) | not yet: no run has happened at any SHA of this branch. The sealer answers it, and its spawn is now due |

## Paste-ready fixes

### ⬜ 1

`skills/code-review/scripts/chain_check.py:860-862`:

```python
# WHAT IT ASSUMES: that no item of that release is framed after the batch.
# On 2026-10-08 the owner kept the release at the batch and #834's build
# (1791382684, framed before it) instead of splitting it, while #871-#874
# sit in its milestone unframed. An item framed later for the same release
```

### ⬜ 2

PR #879's body, the `chain-check` row of *What changes*:

```
| `chain-check` | — | fails a ready pull request over an open note, and, for a work item begun at or after `1791384163` (one past 0.21.0's batch, whose rounds run under 0.20.0's `close`; an item framed later for this release moves it), over a note closed `fixed` |
```

And the sentence in *How it was checked*:

```
This pull request's rounds ran under the installed 0.20.0 `close`, so the first run under the new rule is the first work item reviewed after 0.21.0 is installed. #860 and #866 edit neighbouring lines of `close` and `chain_check.py` (`overview.md` §*Not verified*).
```

### ⬜ 3

`overview.md:29`:

```
| `notes`, `close`'s carried note and the two `chain-check` arms on a real run, through a warden's report rather than a fixture. This item's rounds closed with the installed 0.20.0 generator, so none of them ran under the rule | the orchestrator of the first work item reviewed after 0.21.0 is installed |
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## The gate that is now due

Nothing this round found needs a fix. The three notes above are carried to
the run's end. The installed 0.20.0 `close` still takes a note in its fix
table, so close them `answered` (with `corrected at <sha>` where corrected),
never `fixed`. What comes due next is the sealer's spawn for the broad gate.
It is not a run for the session reading this report to assemble.

Needs a fix: no
Loses a record or crashes: no

## Proof block

- Opened: `rounds/round-2.md`, `rounds/round-2-report.md`,
  `rounds/round-2-fixes.md`, `routing.md`, `handoff.md`, `survivors.md`,
  `changelog.md:1-30`, `overview.md:19-45`; the diff `be3c452a..fe3480d2`
  in full outside the ledger, and the ledger's word diff;
  `chain_check.py` at 728-752, 835-875 (`NOTES_FROM`) and 4615-4700
  (`carried_notes`); `skills/code-review/orchestration.md:215-245`;
  `.github/workflows/hygiene.yml:180-225`; the #834 handoff on
  `chore/834-every-reader-and-record-is-inventoried`; the siblings' notes
  rows on `origin/release/v0.21.0`; `bin/test`'s header and
  `survivor-check --help`; PR #879's body.
- Executed: the three modules once; `survivor-check` three ways;
  `chain_check.py` at the head and over the merge, draft and ready; the
  ref and id probes; the `gh` reads named above.
- Not run: the full suite, lint and typecheck (the sealer's).
