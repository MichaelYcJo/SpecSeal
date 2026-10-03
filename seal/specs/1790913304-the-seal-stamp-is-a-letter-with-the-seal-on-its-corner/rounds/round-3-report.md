# 1790913304 — review round 3 report

Ran by `specseal:warden on claude-opus-5-5`, at `2fe8af6ef9a9d068d9e18f6957e878b434c4978f`.
This is a verifying round. Its target is round 2's fix range
`0bef982a..483c3770`, six commits. `git diff --stat 483c3770..HEAD` touches
`handoff.md` and `rounds/round-2.md` only, so nothing after the fix range is
code. The work ran in a `git clone --no-local` of the worktree checked out at
the target SHA, under this round's own scratch directory. The worktree was
only read, and this report is the one file written in it. The clone, the
probe and its logs were removed before handover.

## What this round was asked

Round 3 is the run's last round, a verifying round at `2fe8af6e` over round 2's fix range `0bef982a..483c3770`. Round 2's `New units` reads none, so the round opened no fresh finding surface. For each of round 2's five ⬜ verdicts it was asked whether the cited commit closes it: 6 at `81e4730f`, 7 at `ea36c24f`, 8 at `2988a974`, 9 at `efe1c949`, and 10, answered as a correction to the ledger at `483c3770`. It re-ran the mutations that had survived round 2, against the new cases and against the cases at `0bef982a`. It measured the gate-failure report over every gate pair, and end to end through `hooks/dispatch.py` with two gates failing on text outside the BMP. It was told not to run `claude -p` or write a settings file, and to run only the touched test modules.

## In one view

```
round 2's findings                               this round
  6  A3 case blind to a claimed, unprinted file  --->  closed: the mutation is red on the case, green on the old one
  7  oldest-first and exactly-at-budget unpinned --->  closed: both survivors red on the ladder case, green on the old one
  8  reserve in code points; cap cut code points --->  closed: two astral gates write 909, as ASCII does; the old cut wrote 1,309
  9  admitted's docstring names a dead scale     --->  closed; one line of the reflow is 113 columns (finding 11, cosmetic)
 10  ledger B2 carries the dead clause           --->  closed: B1 and B2 say what the code does, evidence-check 0 drifted
```

Every verdict round 2 recorded as closed is closed. The one thing this round
opened is ⬜, and nothing needs a fix.

## 1. Finding 6 is closed: the A3 case now sees a file claimed and not printed

Executed. The hook was mutated to claim every ready file (`ready[:carried]`
to `ready`). It then prints one stamp and renames all twelve files.
`test_seals_past_what_one_message_carries_wait_for_the_next_turn` goes red
under it. The same case taken from `0bef982a` stays green under the same
mutation, so the new label check is what catches it.

Read. The check compares each block's first line with `label` of the files
this turn claimed, `before` up to `len(drawn_now)`. Each fixture file carries
its own `tree`, so the labels differ from file to file. A turn that claims
twelve files and prints one has one label against twelve expected, and the
count alone turns it red.

## 2. Finding 7 is closed: oldest-first and exactly-at-the-budget are pinned

Executed. Both mutations round 2 found surviving were applied to the floor
pass of `admitted`: `break` made `continue`, and `>` made `>=`. Each turns
`test_the_ladder_steps_down_in_order_and_ends_with_no_disc` red. The case
taken from `0bef982a` stays green under both.

Read. In `[one, big, one]` at `past`, `big` has sixty more rows, and round 2
measured a block of that shape over 9,000 units even at 0.75. So `big` does
not fit beside `one`, and only `continue` would carry the third block past it.
The single seal at `len(at[0.75])` fits by exactly zero, so the `>=` mutation
drops its disc. Both assertions turn on the defect they name.

## 3. Finding 8 is closed: the cap counts UTF-16 units, and two gates stay inside the reserve

Read. `first_line` (`hooks/dispatch.py:319`) adds two for a character above
U+FFFF and one otherwise, stops before the character that would pass
`MESSAGE_CAP`, and so never splits a pair. A lone surrogate counts one. That
matches `admitted`'s `surrogatepass` count and what the harness gives the
`\ud800` escape that `json.dumps` writes. `describe` passes the message
through `flat`, which only joins whitespace, so nothing after the cut makes
it longer. `first_line` still makes one `splitlines` call, which is the count
`tests/test_every_reader_ends_a_line_where_gfm_does.py` holds it to.

Executed by construction. `dispatch.describe` was run over every gate in
every group it belongs to, for both phases. The message was `first_line` of
500 ASCII characters and of 500 U+1D54F. The longest report for one, two and
three gates was:

| Cut | Text | `ModuleNotFoundError` | `PendingDeprecationWarning` |
|---|---|---|---|
| `first_line` as fixed | ASCII or U+1D54F | 533 · 909 · 1,274 | 539 · 921 · 1,292 |
| the code-point cut before `2988a974` | U+1D54F | 733 · 1,309 · 1,874 | 739 · 1,321 · 1,892 |

Those are the figures the comment above `MESSAGE_RESERVE` and ledger B1 give.
`PendingDeprecationWarning` is the longest built-in exception name, at 25
characters.

Executed end to end. In the clone, `worktree-guard.py` and
`implementer-mark.py` were made to raise U+1D54F text at load, and
`hooks/dispatch.py pre-agent` wrote their two records. `hooks/dispatch.py
stop` then drew one values file of the A3 fixture's size. The report took 870
units with its separator and the message 7,386. With the old cut restored the
same run gave a report of 1,270 units. Beside a stamp at `MESSAGE_BUDGET`
that is 10,270, past the limit.

The new assertions in `test_a_message_is_its_first_line_and_capped` were each
shown red. Four mutations of `first_line` were run: every character counted
as one unit, `> 0xFFFF` made `>=`, `units > MESSAGE_CAP` made `>=`, and the
old code-point cut. Each is red on the case, and each is green on the case
from `0bef982a`. `break` made `continue` survives, and it is equivalent: once
past the cap the count only grows, so no later character is kept. The fix
pass recorded the same survivor and the same reason in ledger B1.

## 4. Finding 9 is closed, with one line left long

Read. `admitted`'s docstring now says a scale below 0.75 is refused before a
block reaches it, which `check_scale` inside `drawings` does. The dead clause
is gone. The reflow left
`skills/verify/scripts/seal_stamp.py:632` at 113 columns, where the rest of
the docstring wraps under 80. Ruff's selection in `ruff.toml` leaves out
`E501` and `ruff format` does not rewrap docstrings, so no check fails on it.
That is finding 11.

## 5. Finding 10 is closed: the ledger says what the code does

Read. B2 no longer carries *or a file's own smaller scale*. Its `admitted`
anchor moved to the re-stamped hash, and a dated `Corrected` note names
round 2's four changes. B1 now says 909 UTF-16 units, and it adds
`MESSAGE_CAP` and `first_line` to its grounds and the gate-failure case to
its cases.

Executed. `bin/evidence-check .` in the clone reports 3,521 ok, 0 drifted and
0 broken, and the work item's fragment alone reports 65 ok.

## Finding this round opened

### ⬜ 11 — One line of `admitted`'s reflowed docstring is 113 columns

`skills/verify/scripts/seal_stamp.py:632`, written at `efe1c949`. The line
*the highest rung the others leave room for: its own scale first, then each
of `SCALE_LADDER`, never above its* was not rewrapped when the clause before
it changed. No check reads docstring width here, and the behaviour and the
claim are right. The release ships no defect if it stands.

**Block or defer.** It does not block the pull request. It is in a unit this
run's own fixes created, so under `docs/review-chain-spec.md` §*The cap
bounds rounds, and not the fixes of the round it stopped* it is the branch's
to fix if anyone does. A fix would cost a verifying round for a rewrap. Left
in this record, it can ride the next edit of `admitted`.

## What this round did not verify

- **Whether the harness counts a character outside the BMP as two.** Round 1's
  fix pass measured it with `claude -p`, and B1 holds the figures. This round
  was told not to run `claude -p`, so the code's count is verified and the
  harness's is not. The orchestrator answers it. Carried from round 2's ❓.
- **An exception type name longer than the built-ins'.** `handoff.md` leaves
  this to the orchestrator: `record` writes the type name uncapped. Read, as a
  coordinate this round adds rather than as a finding: the longest exception
  class the plugin's own hooks and scripts define is `NoMutationDefined`, 28
  characters, so by arithmetic two gates failing with it write about 927, still
  inside 1,000. Only a type name from outside the plugin can pass it.
- **The broad gate.** Not yet. It belongs to the sealer once the rounds
  settle. This round leaves nothing open that needs a fix, so the sealer's
  spawn comes due once this round's record is written.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 6 is closed — the A3 case holds each turn's labels to exactly the files it claimed | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:583` | confirmed | Executed: the hook claiming every ready file turns the case red, and the case from `0bef982a` stays green under it |
| 🟢 | round 2's finding 7 is closed — oldest-first carrying and a single seal exactly at the budget are pinned | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:689` | confirmed | Executed: the floor's `break` to `continue` and `>` to `>=` each turn the ladder case red, and the case from `0bef982a` stays green under both |
| 🟢 | round 2's finding 8 is closed — `first_line` cuts at 200 UTF-16 units, so two gates write 909 whatever their text | `hooks/dispatch.py:319` | confirmed | Executed: every gate pair gives 909 and three gates 1,274, ASCII and U+1D54F alike, against 1,309 under the old cut; end to end 870 against 1,270; four mutations red, the equivalent `break` survives |
| 🟢 | round 2's finding 9 is closed — `admitted`'s docstring no longer names a scale below 0.75 | `skills/verify/scripts/seal_stamp.py:630` | confirmed | Read: `check_scale` in `drawings` refuses it first; finding 11 is the reflow's long line |
| 🟢 | round 2's finding 10 is closed — ledger B1 and B2 say what the code does, re-stamped | `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md` | confirmed | Read; executed: `bin/evidence-check .` 3,521 ok, 0 drifted, 0 broken |
| ⬜ 11 | one line of `admitted`'s reflowed docstring is 113 columns, where the rest wraps under 80 | `skills/verify/scripts/seal_stamp.py:632` | open | Read: no check reads docstring width (`E501` is not selected); does not block, and is the branch's under the cap rule if fixed |
| ❓ | whether the harness counts a character outside the BMP as two UTF-16 units | `skills/verify/scripts/seal_stamp.py:213` | ❓ out of verified scope | Measured by round 1's fix pass with `claude -p`, which this round was told not to run; carried from round 2; the orchestrator answers it |

## Executed probes

| What was run | Result |
|---|---|
| pytest with `-n auto` over the three modules the fix range touched (stamp, sealer, gate failure), in the clone, with the main checkout's `.venv` | 329 passed, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone; then `--ledger` on the work item's fragment | `total: 3521 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow`, exit 0; the fragment 65 ok |
| `dispatch.describe` over every gate, every group it is in and both phases, with `first_line` of 500 ASCII and of 500 U+1D54F; the report for one, two and three gates, separator included | as fixed: 533 · 909 · 1,274 with `ModuleNotFoundError`, 539 · 921 · 1,292 with `PendingDeprecationWarning`, both texts alike; the code-point cut over U+1D54F: 733 · 1,309 · 1,874 and 739 · 1,321 · 1,892 |
| `hooks/dispatch.py pre-agent` with `worktree-guard.py` and `implementer-mark.py` raising U+1D54F text at load, then `hooks/dispatch.py stop` over one values file | two records written; the report 870 units with separator, the message 7,386; under the old cut the report 1,270, which beside `MESSAGE_BUDGET` is 10,270, past the limit |
| Eight mutations, each against the fix range's case for it | hook claims every ready file: A3 case red · floor `break` to `continue`: ladder case red · floor `>=`: ladder case red · every character one unit: cap case red · `>= 0xFFFF`: red · `units >= MESSAGE_CAP`: red · the old code-point cut: red · `first_line`'s `break` to `continue`: green, equivalent |
| The same eight against the cases at `0bef982a` | all green, so the fix range's new lines are what turn each one red |
| The full suite, lint and typecheck (the broad gate) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:577` | round 2's ⬜ 6 — fixed, confirmed here |
| round-2 | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:679` | round 2's ⬜ 7 — fixed, confirmed here |
| round-2 | `skills/verify/scripts/seal_stamp.py:229` | round 2's ⬜ 8 — fixed, confirmed here |
| round-2 | `skills/verify/scripts/seal_stamp.py:627` | round 2's ⬜ 9 — fixed, confirmed here |
| round-2 | `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md` | round 2's ⬜ 10 — answered, confirmed here |
| round-2 | `skills/verify/scripts/seal_stamp.py:213` | round 2's ❓ — still out of verified scope |
| round-1 | `skills/verify/scripts/seal_stamp.py:548` | round 1's ⬜ 4 — deferred to #720, carried and not re-derived |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `record` writes an exception's type name uncapped, so a type name from outside the plugin longer than about 30 characters can pass the reserve with two gates (predates #717; the plugin's own longest is 28) | `handoff.md` §*Open, and who answers*, not yet placed in an issue or PR #719's body | the orchestrator |

## Paste-ready fixes

### ⬜ 11

```python
    The owner's rule of 2026-10-02 (`questions.md` Q6), which replaced one
    rung for the whole message: a seal keeps its disc rather than share a
    message without it. So the message carries as many of the oldest blocks
    as fit together WITH the disc, each at 0.75 — a scale below it is
    refused before a block reaches here — and then each, oldest first, at
    the highest rung the others leave room for: its own scale first, then
    each of `SCALE_LADDER`, never above its own scale. The blocks past
    those are not drawn here; the hook leaves their files pending, and the
    next `Stop` draws them whole.
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, at `2fe8af6e` in the worktree and the clone:

- `hooks/dispatch.py`: lines 45–62, `GROUPS` (72–101), `run_gate` (106–136), `first_line` and `record` (315–380), `describe` and `draw` (400–505), `report` and `main` (505–570)
- `hooks/sealer-stamp.py`: `drawings` and the head of `main` (100–160)
- `skills/verify/scripts/seal_stamp.py`: lines 200–250 and 610–700; `write_values`'s head (834–846)
- `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`: lines 21–34, 72–74, 200–262, 492–500, 540–715
- `tests/test_a_gate_that_fails_says_so.py`: the fix range's hunk (557–571)
- `tests/test_every_reader_ends_a_line_where_gfm_does.py`: lines 585–600 and 700–735
- the fix range's whole diff `0bef982a..483c3770`, the ledger fragment's B1 and B2 included
- `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/`: `rounds/round-1.md` whole, `rounds/round-1-report.md` lines 1–30, `rounds/round-2.md` whole, `rounds/round-2-report.md` whole, `handoff.md`, `routing.md`, `questions.md`, `overview.md`, and `changelog.md` lines 10–40
- `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped*
- `ruff.toml`'s selection, `bin/test`, `.github/scripts/run_tests.py`'s venv lines, `.github/workflows/test.yml`'s ruff steps
