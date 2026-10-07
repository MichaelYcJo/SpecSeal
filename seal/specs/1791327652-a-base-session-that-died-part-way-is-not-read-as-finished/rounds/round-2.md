# 1791327652-a-base-session-that-died-part-way-is-not-read-as-finished — review round 2

| Field | Value |
|---|---|
| Target SHA | 5d21ccd925df5ddd16108dcb0dcfeeb2bd48c228 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #851 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `c339dccdcb27f3d2db995de27964ecd66bea1da6..b1de5a0b4bf66b5eed680221a71cf65f24d72218`, 3 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (the version-timer check fails on `broad_gate.py:1941`) and 🔴 2 (the pasted-passage check fails on the **New?** bullet and rule 3) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #849 is the verifying round for round 1's fixes at `e7fc758a..8ce0dc79`, reviewed at 5d21ccd9.

The reviewer was asked to open each fix and to treat round 1's `New units` as a finding surface: `RAN_TO_ITS_END`, `UNENDED_HERE`, the reworded `NO_SUMMARY` and the `id()`-keyed map. It was also asked:
- whether demoting on every `end` exit other than 0, 1 and 5 holds on the oldest pytest the recorder supports;
- whether rule 3's two named limits are honest limits;
- whether the in-place edits to 1791270161's W5, W8, `Corrected · D1` and `Corrected · R4`, and its 52 re-stamped rows, are right;
- to read every workflow of `gh pr checks 851`.

It did not run the full suite.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `RAN_TO_ITS_END`'s comment names pytest "9.1.1", so `test_no_loaded_file_names_a_version_at_or_above_the_running_one` fails on PR #851 | `skills/verify/scripts/broad_gate.py:1941` | **fixed** `d52af030` | fixed at d52af030 — `RAN_TO_ITS_END`'s comment names pytest 6.1, 7.0 and 9.1 in two parts; no other three-part version on the branch outside `seal/` and the changelogs; executed: failing in CI on Ubuntu and Windows group 2 at `5d21ccd9` and in the clone; passes with two-component versions in the clone. Inside a unit round 1's fixes created |
| 🔴 2 | The **New?** bullet and rule 3 share a 21-word run the fix pass wrote into both, so two cases of the pasted-passage module fail on PR #851 | `skills/verify/SKILL.md:517` | **fixed** `d52af030` | fixed at d52af030 — the **New?** bullet is reworded and its pin moved; the bullet, rule 3 and the changelog fragment share no 15-word run, the changelog's copy of a rule-3 sentence included; executed: both cases failing in CI and in the clone, the shared run listed with the module's own helpers; passes with the reworded bullet and its pin in the clone |
| ⬜ 3 | `RAN_TO_ITS_END`'s comment, rule 3, the changelog fragment and one case's docstring say a failed collection gives exit 2; under `-x` it gives 1 | `skills/verify/scripts/broad_gate.py:1931` | **fixed** `d52af030` | fixed at d52af030 — the comment, rule 3 with its pin, the changelog and the case docstring say a failed collection exits 2 only without `-x`; the word the gate gives is unchanged; executed on pytest 6.1.0, 7.0.0 and 9.1.1: `end` 1 and no test line; read: the base record then holds only the failed file, so every word stays right |
| 🟢 | round 1's finding 1 is closed — a base session whose `end` exit is not 0, 1 or 5 reads `new?` | `skills/verify/scripts/broad_gate.py:2008` | confirmed | executed: the new cases are red at `e7fc758a`'s code except the 0, 1 and 5 parameters, and green here; the exit mapping matches on pytest 6.1.0, 7.0.0 and 9.1.1; read: `wrap_session` of 6.1.0 and 7.0.0 |
| 🟢 | round 1's finding 2 is closed — the failure form counts the sessions at `HEAD` that stopped part-way | `skills/verify/scripts/broad_gate.py:3100` | confirmed | executed: the HEAD case is red at `e7fc758a` and green here and in Ubuntu's full run |
| 🟢 | round 1's finding 3 is closed — `last_sent` keyed on `id()` with the sender held | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:196` | confirmed | executed: S5 red at `e7fc758a`'s recorder, green here; read: a held sender cannot be freed, so an `id()` match is the same object |
| 🟢 | round 1's finding 4 is closed — phase 1's re-stamp count | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/phases/phase-1.md:19` | confirmed | read: "The other 27 rows" |
| 🟢 | round 1's open CI question is answered — macOS at `30ca8903` | PR #851 | confirmed | read: run 37545769411, all ten jobs passed |
| 🟢 | The two stops rule 3 names are real limits that need mechanism | `templates/config.md:334` | confirmed | executed on three pytest builds; read: closing either needs a new `end` field and a reader, which a fix pass may not add (`skills/code-review/orchestration.md`); filed under Deferred |
| 🟢 | The edits to 1791270161's W5, W8, `Corrected · D1` and `Corrected · R4` are faithful, and the 52 re-stamped rows changed nothing else | `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md:5` | confirmed | executed: a row-by-row comparison, with text changing in those four rows only; read against `base_word` and rule 3; CI `ledger` passes |
| 🟢 | The overview's two rows left to this round: a replaced worker, and a recorder that stops writing | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:206` | confirmed | read: a held sender cannot be replaced at its address; `give_up` sets `stream` to `None`, so `pytest_sessionfinish` writes no `end` line and the record counts as unended |
| ❓ | `pytest (macos-latest, 3.12)` had not finished | PR #851 | ❓ out of verified scope | read at 00:09 UTC: still pending. The same three cases are expected to fail there, but that has not been read. The orchestrator answers it by reading `gh pr checks 851` after the fix pass pushes, when every job reruns |

## Paste-ready fixes

```python
# Any other value is a return code `pytest.exit` or a plugin chose, and is no
# exit of a session that ran to its end. Each exit above was measured with
# the recorder loaded on pytest 6.1, 7.0 and 9.1 (#849 round 2). Two stops
```
```markdown
  the record cannot say the file passed. A session of the base that
  stopped part-way reads the same way: its record holds no `end` line,
  because the process died, which plain pytest does on a test that calls
  `os._exit`, or its recorder stopped writing; or its `end` line
  shows an exit other than 0, 1 or 5, as a `KeyboardInterrupt` or
  `pytest.exit()` in a test and xdist under `-x` give. It is a question about the
```
```python
        "A session of the base that stopped part-way reads the same way: its "
        "record holds no `end` line, because the process died, which plain "
        "pytest does on a test that calls `os._exit`, or its recorder "
        "stopped writing; or its `end` line shows an exit other than 0, 1 or "
        "5, as a `KeyboardInterrupt` or `pytest.exit()` in a test and xdist "
        "under `-x` give.",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on the recorder module and the gate module, filtered to the fix's cases, in the clone at `5d21ccd9` | 55 passed |
| The fix's five new cases with `e7fc758a`'s `broad_gate.py` and recorder checked out in the clone | 10 failed, 3 passed (the 0, 1 and 5 parameters) |
| A probe script, run once and deleted, running ten stops with the recorder loaded on pytest 6.1.0 (Python 3.9), 7.0.0 and 9.1.1 | identical on all three: ok 0, failing 1, none collected 5, `KeyboardInterrupt` 2, `pytest.exit()` 2, `pytest.exit` with code 0 gives 0, collection error 2, collection error under `-x` 1, `-x` on a failing test 1 (no line for the second file), `-k "("` 4 |
| The same on pytest 6.1.0 under Python 3.11 | no record: 6.1.0's assertion rewriter cannot collect on 3.11; not evidence either way |
| 1791270161's fragment compared row by row, `e7fc758a` to `8ce0dc79` | 53 rows changed, 52 anchor sets changed; text changed in W5, W8, `Corrected · R4` and `Corrected · D1` only |
| `gh pr checks 851` at 00:03, 00:05, 00:07, 00:08 and 00:09 UTC | at 00:09: `ledger`, `lint`, `release`, both `arm-check-grammar`, and Windows groups 1, 3 and 4 pass; Ubuntu and Windows group 2 fail; macOS pending |
| The logs of the failed Ubuntu and Windows group 2 jobs | each 3 failed: the version-timer case and the two pasted-passage cases; Ubuntu 12984 passed |
| `gh run view` of run 37545769411 at `30ca8903` | all ten jobs succeeded |
| The three failing cases in the clone at `5d21ccd9` | 3 failed |
| The same, with the pasted-passage module, the version case and the gate module's pins, after the paste-ready fixes were applied in the clone | 53 passed |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: this round did not run it. It is the sealer's, once, after the rounds settle, and it comes due when a round leaves nothing open; this one leaves 🔴 1 and 🔴 2 |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Two stops `RAN_TO_ITS_END` cannot see: `pytest.exit` with code 0, 1 or 5, and a plain run that `-x` or `--maxfail` stops, which writes 1. Closing them needs a new `end` field and a reader for it. Round 1's fix pass named them in rule 3 and the overview's *Not done*, but filed them nowhere | rung 2 candidate: #834, the 0.21.0 inventory to take before any reader or record changes; the `end` line is one of those records | the 0.21.0 run that takes #834's inventory, because adding the field changes a record that inventory must list first |
