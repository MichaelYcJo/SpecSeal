# 1791327652-a-base-session-that-died-part-way-is-not-read-as-finished — review round 3

| Field | Value |
|---|---|
| Target SHA | 034fbe4cdbf1a79e11c815f581d9cebacb48a612 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #851 |
| Broad gate | 3c52598e against 3d78c220 |
| Fixes checked by | no fixes to check |
| Fix range | `034fbe4cdbf1a79e11c815f581d9cebacb48a612..034fbe4cdbf1a79e11c815f581d9cebacb48a612`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of #849 is the verifying round for round 2's fixes at `c339dccd..b1de5a0b`, reviewed at 034fbe4c. Round 2's fixes were prose: a comment, one docstring and two moved pins.

The reviewer was asked:
- to open each fix;
- to check that each of the 8 rows of the new `survivors.md` is true;
- to check that the changelog sentence the smith reworded beyond the finding states what rule 3 states;
- to read every workflow of `gh pr checks 851`.

It did not run the full suite.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The comment and one case's docstring say that under `-x` a failed collection exits 1; when the failing file is the last collected, it exits 2 | `skills/verify/scripts/broad_gate.py:1944` | deferred #852 — the exit a stopped session writes is #852's subject, recording why a session stopped; the gate's word is right either way, since exit 2 reads the strict `new?` | #852 — the exit a stopped session writes is #852's subject, recording why a session stopped; the gate's word is right either way, since exit 2 reads the strict `new?`; executed on pytest 9.1.1: 1 with the broken file first, 2 with it last, under `-x` and `--maxfail=1`; read: pytest raises `Failed` only at the next collection's start; the gate's word is right in both, so no defect ships; also at `broad_gate.py:1932` and `tests/test_the_seal_is_taken_once_by_the_sealer.py:4308` |
| ⬜ 2 | The comment says each exit was measured on pytest 6.1, 7.0 and 9.1; exit 3 was read there, not measured | `skills/verify/scripts/broad_gate.py:1940` | deferred #852 — the comment's measured-versus-read wording belongs with #852's exits; round 2's report holds the measurement | #852 — the comment's measured-versus-read wording belongs with #852's exits; round 2's report holds the measurement; read: round 2's ten stops gave 0, 1, 2, 4 and 5 and no 3; its report labels exit 3 on 6.1.0 and 7.0.0 as read; the value is right |
| ⬜ 3 | The overview still gives exit 2 to every failed collection, says the exits were measured on 9.1.1 alone, and leaves round 2 a question it answered | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/overview.md:19` | answered | a correction to this item's `overview.md`, made in the closing commit: row 19 says a failed collection gives 1 under `-x` where another file follows, and names what 6.1 and 7.0 measured; row 32 is closed by round 2's answer; read: rows 19 and 32 unchanged by the fix pass; a correction to the paperwork, outside `Needs a fix` |
| ⬜ 4 | The changelog's reworded sentence names `-x` but not `--maxfail` for the second stop, which rule 3 names | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/changelog.md:18` | answered | a correction to this item's `changelog.md`, made in the closing commit: the stop names `-x` or `--maxfail`, as rule 3 does; read against rule 3; the sentence before the rewording missed it too; a correction to the paperwork, outside `Needs a fix` |
| 🟢 | round 2's blocking finding 1 is closed — no three-part pytest version in `RAN_TO_ITS_END`'s comment | `skills/verify/scripts/broad_gate.py:1940` | confirmed | executed in the clone: the version-timer case passes |
| 🟢 | round 2's blocking finding 2 is closed — the **New?** bullet shares no 15-word run with rule 3, and its pin moved | `skills/verify/SKILL.md:517` | confirmed | executed in the clone: the pasted-passage module and both pins pass; `longest_run` gives 21 words before and none of 15 after |
| 🟢 | round 2's finding 3 is closed where it said exit 2 — every place it named ties exit 2 to a collection without `-x` | `skills/verify/scripts/broad_gate.py:1932` | confirmed | read at `034fbe4c`; what the narrowing now adds about `-x` is ⬜ 1 |
| 🟢 | survivors.md's eight rows are each true, and survivor-check excuses exactly those eight | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/survivors.md:21` | confirmed | executed: `survivor-check` over `c339dccd..359badfc` names eight places, and with `--exempt` over `c339dccd..b1de5a0b` excuses all eight and exits 0; read: each quote against its file |
| 🟢 | The changelog's reworded sentence states rule 3's two stops | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/changelog.md:18` | confirmed | read against rule 3; shares no 15-word run with it (`longest_run`, executed); the missing `--maxfail` is ⬜ 4 |
| 🟢 | round 2's open CI question is answered — every workflow of PR #851 passes at `034fbe4c`, macOS included | PR #851 | confirmed | read: `gh pr checks 851` at 00:33 UTC, eleven checks pass; `tests` run 37551387092 completed with all ten jobs succeeding |

## Paste-ready fixes

```python
#   2 INTERRUPTED -- a `KeyboardInterrupt` or `pytest.exit()` in a test, a
#     failed collection without `--continue-on-collection-errors` (no test
#     runs) that `-x` or `--maxfail` did not stop at the next collection, a
#     failed collection in the last file collected among them, xdist under
#     `-x` or `--maxfail`, and a plugin that sets `shouldstop`. Stopped
#     part-way, and still writes its `end` line.
```
```python
# without xdist that `-x` or `--maxfail` stops exits 1, a failed collection
# under `-x` with another file collected after it among them. That one leaves
# no file partly run while each file's tests run together: it stops in the
```
```python
    """#849 round 1's 🟡 1, at `read_record`. pytest writes an `end` line for
    a session it stopped itself: a `KeyboardInterrupt` or `pytest.exit()` in
    a test, a failed collection and xdist under `-x` give 2 (a failed
    collection under `-x` gives 1 where another file is collected after it),
    a run loop that raised gives 3, an argument refused after the session
    started gives 4.
```
```python
# exit of a session that ran to its end. Each exit above was measured with
# the recorder loaded on pytest 9.1, and every one but 3 on 6.1 and 7.0,
# where 3 was read in pytest's session wrapper (#849 round 2). Two stops
```
```markdown
  its return code, and a run without xdist that `-x` or `--maxfail` stops
  while its order mixes files.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on `tests/test_no_passage_is_pasted_into_a_second_file.py`, the version-timer case and the two pins, in the clone at `034fbe4c` | 11 passed, exit 0 |
| `survivor-check --range c339dccd..359badfc` in the clone | exit 1, eight places, the eight rows of `survivors.md` |
| `survivor-check --range c339dccd..b1de5a0b --exempt` pointing at `survivors.md` | exit 0, all eight excused |
| The pasted-passage module's `longest_run` over SKILL.md, rule 3's file and the changelog fragment, at `c339dccd` and `b1de5a0b` | 21 and 20 words before; none of 15 after |
| A probe run once and deleted: two files, one that cannot import, on pytest 9.1.1, with `-x`, `--maxfail=1`, `--maxfail=2` and nothing | broken file first: 1, 1, 2, 2; broken file last: 2, 2, 2, 2 |
| `gh pr checks 851` at 00:23 and 00:33 UTC, and `gh run view` of run 37551387092 once it completed | at 00:33: all eleven pass; the ten `tests` jobs succeeded, the last (macOS) at 00:33:39 |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: this round did not run it. It is the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:1978` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:3380` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:191` | round 1's 🟡 3 — fixed |
| round-1 | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/phases/phase-1.md:19` | round 1's ⬜ 4 — answered |
| round-1 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:198` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:49` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md:5` | round 1's 🟢 — confirmed |
| round-1 | PR #851 | round 1's ❓ — out of verified scope |
| round-2 | `skills/verify/scripts/broad_gate.py:1941` | round 2's 🔴 1 — fixed |
| round-2 | `skills/verify/SKILL.md:517` | round 2's 🔴 2 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:1931` | round 2's ⬜ 3 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2008` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:3100` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:196` | round 2's 🟢 — confirmed |
| round-2 | `templates/config.md:334` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:206` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
