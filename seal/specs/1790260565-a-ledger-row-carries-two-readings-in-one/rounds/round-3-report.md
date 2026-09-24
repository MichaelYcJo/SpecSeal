# 1790260565-a-ledger-row-carries-two-readings-in-one — review round 3 report

Verifying round, and the last. Target SHA 0eb461fd; the surface is round 2's
fix range `8eb70840..4a3e4635` (d7320980, 135efd8a, 4a3e4635), plus the close
commit 0eb461fd, which touches only the round-2 report and record. Round 2's
record names no new unit, and the fix range adds none: d7320980 edits one
entry of `EDIT_OUTCOMES`, and the other two commits edit ledger rows. Nothing
outside that diff was re-reviewed. Worked in a `--no-local` clone at the
target SHA, deleted after the round.

## What the fix pass claimed, and what the code does

**Round 2's ⬜ 1 is closed.** d7320980 claims the needle now carries the act
as well as the premise, and goes red with the act deleted from a scratch
copy. I re-ran that rather than taking it (executed). The widened needle
occurs once in `CONTRIBUTING.md`, whitespace collapsed. With the act deleted
and the premise kept, the guides' case goes red and names the needle
(1 failed). The same happens with the premise deleted and the act kept. With
the file restored, the guides' case and the owner's case both pass. The
half of the bullet that round 2 found unheld is held now.

**Round 2's ⬜ 2 is closed.** 135efd8a appends
`tests/test_a_merge_cannot_silently_drop_a_correction.py#EDIT_OUTCOMES@69099dff`
to E1's grounds (read: it occurs once in `seal/releases/0.15.1.md`). The
anchor resolves `ok`: `evidence-check` over the release file and the work
item's fragment reports 201 ok, 0 drifted and 0 broken, one more than round
2's 200, which is the new anchor (executed). The check can fail. With the
hash replaced by `00000000` in the clone, the same run names
`EDIT_OUTCOMES` DRIFTED (executed). The commit order holds the claim that the
row was stamped after the needle fix: 135efd8a follows d7320980, and
69099dff is the unit's hash at the target. The orchestrator's correction at
0eb461fd, which gives 69099dff as the hash in the round-2 report's ledger
line, matches the tree.

**Round 2's ⬜ 3 is closed.** 4a3e4635 replaces the parenthesis in E1's and
E2's newest notes with *commit 950db9ef's message; reproduced by round 2's
reviewer, `rounds/round-2.md`* (read, both rows). Both sources hold what they
are cited for. Commit 950db9ef's message says each needle was seen red with
its sentence deleted from a scratch copy (read). `rounds/round-2.md`'s first
probe row records the thirteen deletions, each red in the right case (read).
The notes no longer cite `rounds/round-1.md`.

**The rest of the tree around the fix is unchanged in effect.**
`correction-check --range 8eb70840...0eb461fd` exits 0; the range has no
merge commit (executed). `evidence-check .` over the whole tree exits 0
(executed). The three modules the fix range and this report reach pass:
108 passed (executed).

Two things I looked at and do not report as findings (read):

- Round 2's record still carries `f810196e` in the ⬜ 2 grounds cell and in
  its second paste-ready fence. That was the hash at 103b0974, the SHA round 2
  read, and the same cell says the row was stamped after ⬜ 1 so the hash is
  the final unit's. The record is accurate about what its round computed.
- E1 carries no dated note for the anchor 135efd8a added. Adding an anchor
  is not a re-stamp of an edited one, and the row's claim does not change
  with it. The newest note already names `EDIT_OUTCOMES` as what holds the
  two outcomes.

## Regression tests to plant

None. This round's fix was a stronger needle in an existing case, and it was
seen red here in both directions (act deleted, premise deleted).

## Facts for the evidence ledger

None new. E1's `EDIT_OUTCOMES@69099dff` is already in the row and resolves.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's ⬜ 1 is closed — `CONTRIBUTING.md`'s re-stamp needle holds the act as well as the premise | `tests/test_a_merge_cannot_silently_drop_a_correction.py:754` | confirmed | Executed: needle count 1, whitespace collapsed; act deleted with premise kept → guides' case 1 failed, needle named; premise deleted → 1 failed; restored → guides' and owner's cases pass |
| 🟢 | round 2's ⬜ 2 is closed — E1 anchors `EDIT_OUTCOMES` at the final unit's hash | `seal/releases/0.15.1.md` | verified | Executed: `evidence-check` over the release file and the fragment 201 ok, 0 drifted, 0 broken; hash set to `00000000` → DRIFTED on `EDIT_OUTCOMES`. Read: 135efd8a follows d7320980 |
| 🟢 | round 2's ⬜ 3 is closed — E1's and E2's newest notes cite commit 950db9ef's message and `rounds/round-2.md` | `seal/releases/0.15.1.md` | confirmed | Read: 950db9ef's message records the red runs; round 2's first probe row records the thirteen deletions; neither note cites `rounds/round-1.md` any more |
| 🟢 | the fix range creates no new unit, as round 2's `New units` row says | `tests/test_a_merge_cannot_silently_drop_a_correction.py:747` | confirmed | Read: d7320980 edits one string of an existing entry; 135efd8a and 4a3e4635 edit ledger rows |

## Executed probes

| What was run | Result |
|---|---|
| A probe named with the test_tmp prefix, run once in the clone and deleted: the widened `CONTRIBUTING.md` needle counted, whitespace collapsed | 1 |
| The same probe: `evidence-check --reverify .` and its line break deleted from `CONTRIBUTING.md`, premise kept, then the guides' case | 1 failed, the widened needle named; file restored |
| The same probe: the premise *the claim still holds and you have re-read it* deleted, act kept, then the guides' case | 1 failed, the widened needle named; file restored |
| The same probe: the guides' case and the owner's case on the restored tree | 1 passed each; `git status` in the clone empty |
| The same probe: E1's `EDIT_OUTCOMES@69099dff` set to `@00000000`, then `bin/evidence-check --ledger seal/releases/0.15.1.md .` | exit 1, `EDIT_OUTCOMES` DRIFTED; file restored |
| `bin/evidence-check --ledger seal/releases/0.15.1.md --ledger` the work item's fragment `.` | 201 ok, 0 drifted, 0 broken, exit 0 |
| `bin/evidence-check .` | exit 0 |
| `bin/correction-check --range 8eb70840...0eb461fd` | exit 0: no merge commit in the range |
| `bin/test -q -p no:xdist tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_release_hygiene.py tests/test_no_real_identifiers.py` | 108 passed, exit 0 |
| The broad gate: full suite, lint and format over the finished branch | not yet: it has not been run, and it is the sealer's |

Nothing this round opened needs a fix, and every verdict of round 2 is
closed. The broad gate comes due now: the sealer's spawn, over 0eb461fd or
whatever commit this report's record lands on.

Needs a fix: no

Loses a record or crashes: no

## Proof block

Opened in the clone at 0eb461fd:
`tests/test_a_merge_cannot_silently_drop_a_correction.py` (700–800; `EDIT_OUTCOMES` at 747),
`CONTRIBUTING.md` (220–223), `bin/test` (head), the output of
`bin/evidence-check --help`. Opened in the worktree:
`seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/rounds/round-2.md`,
`seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/rounds/round-2-report.md`,
the diff `8eb70840..0eb461fd` (which carries E1 and E2 whole), and the
messages of 950db9ef, d7320980, 135efd8a, 4a3e4635 and 0eb461fd.
