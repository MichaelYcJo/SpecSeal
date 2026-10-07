# Review round 2 — a base session that died part-way is not read as finished (#849)

This is the verifying round for round 1's fixes, `e7fc758a..8ce0dc79`. PR #851's
head is `5d21ccd9`, which adds only round 1's record after `8ce0dc79`. I
reviewed it in a `git clone --no-local` at `5d21ccd9`, under this round's
scratchpad directory, which is now removed. Round 1's record and report were
read for their coordinates. Every verdict below was derived again here.

How the findings relate:

```
round 1's fixes
 ├─ finding 1: an `end` exit other than 0, 1, 5 counts as stopped   -> closed, and right on pytest 6.1 and 7.0 too
 │    └─ RAN_TO_ITS_END's comment names "pytest 9.1.1"            -> 🔴 1: the version-timer check goes red in CI
 │    └─ the comment and rule 3 say a failed collection exits 2    -> ⬜ 3: under -x it exits 1, harmlessly
 ├─ finding 2: UNENDED_HERE under the failing list                -> closed
 │    └─ the New? bullet copies rule 3's 21-word passage           -> 🔴 2: the pasted-passage check goes red in CI
 ├─ finding 3: last_sent keyed on id() with the worker held        -> closed
 └─ finding 4 and the 52 re-stamped rows                           -> faithful
```

Both 🔴 are red on PR #851 now: Ubuntu's job and Windows group 2 each fail
the same three cases. Neither is a wrong behaviour of the gate. Each is a
repository-wide check that reads what the fix pass wrote, and the fix pass ran
only its own modules.

## Round 1's verdicts, answered

**Finding 1 is closed.** `read_record` at
`skills/verify/scripts/broad_gate.py:2008` counts a session as stopped where
it has no `end` line or where any `end` line's exit is outside
`RAN_TO_ITS_END`. Executed: all five new cases are red with `e7fc758a`'s gate
and recorder checked out in the clone, apart from the 0, 1 and 5 parameters,
which should pass there. They are green at `5d21ccd9`.

**Finding 2 is closed.** `gate` hands `head.unended` to `failure_lines`, which
prints `UNENDED_HERE` after the unplaced count (`broad_gate.py:3100`).
Executed: the HEAD case is red at `e7fc758a` and green here. Ubuntu's full
run at `5d21ccd9` passes it, and the base cases too.

**Finding 3 is closed.** `path_of` keys `last_sent` on `id(sender)` and stores
the sender in the value
(`skills/verify/scripts/pytest_record/specseal_pytest_record.py:196`).
Executed: the S5 case is red with `e7fc758a`'s recorder. Read: a stored sender
is never freed, so no live object can share its `id()`. A match in the map
therefore means the same object, and nothing is asked of the sender that
could raise.

**Finding 4 is closed.** `phases/phase-1.md:19` reads "The other 27 rows".
Phase 1 changed 30 rows, three of them W5, W8 and D1.

**Round 1's open question about CI is answered.** The `tests` run at
`30ca8903` (run 37545769411) ended with all ten jobs passing, macOS included.

## The new units

`RAN_TO_ITS_END`, `UNENDED_HERE`, the reworded `NO_SUMMARY` and the
`id()`-keyed map behave as their docstrings say. The defect is in two
sentences around them, and neither changes what the gate prints.

### Demoting every exit but 0, 1 and 5 holds on the oldest pytest

The recorder's docstring says it reads only names pytest has had since 6.1,
so 6.1 is the oldest it supports. I read `wrap_session` in pytest 6.1.0 and
7.0.0. Both give the same mapping as 9.1.1:

- `Failed` gives 1.
- `KeyboardInterrupt` and `pytest.exit` give 2, or the chosen `returncode`.
- `UsageError` gives 4, and any other exception gives 3.
- `pytest_sessionfinish` is called with that value whenever `sessionstart` ran.

xdist 2.1.0's `DSession` raises its own `Interrupted`, a `KeyboardInterrupt`,
on `-x` and `--maxfail`, so that gives 2 as well.

I also ran ten stops with the recorder loaded on 6.1.0 (Python 3.9), 7.0.0
and 9.1.1. The `end` exits matched on all three: 0, 1, 5, 2, 2, 0, 2, 1, 1
and 4. No supported pytest writes an exit outside 0, 1 and 5 for a session
that ran to its end. None writes 0, 1 or 5 for a stop the rule names, apart
from the two stops rule 3 already names.

### The two named stops are real limits, not a fix pass stopping short

Both stops are reproduced on all three builds. `pytest.exit(…, returncode=0)`
writes `end` 0. A plain run that `-x` stops writes `end` 1 and holds no line
for the files after it.

Closing either one needs the recorder to say *why* the session ended. For
`-x` and `--maxfail` that is `session.shouldfail`, which can be read in
`pytest_sessionfinish`. For `pytest.exit` it is pytest's keyboard-interrupt
hook. Either way the `end` line gets a new field and the gate gets a reader
for it. That is mechanism, and `skills/code-review/orchestration.md` §*A fix
pass adds the unit that pins it* says a fix pass may not add mechanism.

One thing is missing. Round 1 closed finding 1 as `fixed`, and its Deferred
table is empty, so the remainder has no home on the ladder. It sits only in
rule 3 and in the overview's *Not done*. The Deferred table below files it.

### A failed collection under `-x` exits 1, not 2 (⬜ 3)

Measured on 6.1.0, 7.0.0 and 9.1.1. The first collection error sets
`shouldfail`, and pytest's hook at the start of the next collection raises
`Failed`. Four places
say a failed collection gives 2: `RAN_TO_ITS_END`'s comment
(`broad_gate.py:1931`), rule 3, the changelog fragment and the docstring of
`test_a_keyed_session_whose_end_shows_a_stop_is_counted_unended`.

The verdict is still right. No test runs, so the base record holds only the
failed file, which reads `failing on base too`. Every other file is not in
`collected`, so on exit 1 it reads `NOT_REACHED`. Only the sentences are
wrong. A one-word repair would read "a failed collection without `-x`".

### What the overview left for this round

- **A worker replaced inside a live xdist run.** Read: the recorder holds
  every sender it keys, so a replacement can never take a held worker's
  `id()`. Nothing about the run has to be provoked for that to hold.
- **A recorder that stops writing, such as on a full disk.** Read: `write`
  catches `OSError` and calls `give_up`, which sets `stream` to `None`. The
  `write` in `pytest_sessionfinish` then returns without writing, so the
  record has no `end` line and counts as unended. If the `session` line
  itself was lost, there is no keyed record and the file reads `NO_RECORD`.
  Both are on the strict side.

### Considered and not raised

At `HEAD`, a test that kills plain pytest with `os._exit(0)` leaves the suite
exit at 0, so the gate goes green without reading the record. CI's pytest
gives the same answer, and the gate exists to say what CI says. So this is
not the gate's defect.

## 🔴 1 — `RAN_TO_ITS_END`'s comment names a pytest version, and the version-timer check fails

`skills/verify/scripts/broad_gate.py:1941` says the exits were "measured with
the recorder loaded on pytest 9.1.1". Executed: in CI and in the clone,
`tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one`
fails with `skills/verify/scripts/broad_gate.py:1941 names 9.1.1`.

This matters because a failing pytest job blocks the merge. The same module
explains the house rule beside `VERSIONS_OF_ANOTHER_PRODUCT`: the pytest rows
for `broad_gate.py` were retired because the recorder names its builds by two
components. Writing two components follows that rule and needs no exemption.
Executed: with the fix below applied in the clone, the case passes.

## 🔴 2 — the **New?** bullet copies 21 words of rule 3, and the pasted-passage check fails

The fix pass rewrote `skills/verify/SKILL.md:517` and rule 3 of
`templates/config.md` into the same run: "it wrote no `end` line to its
record, because its process died, as plain pytest does on a test that calls".
Executed: `test_no_pair_shares_more_than_it_was_measured_at` and
`test_a_removed_copy_passes_without_a_baseline_edit` fail in CI and in the
clone. They report that the pair shares 7 runs of 15 words where 0 were
measured. That is this one 21-word run, and no other run between the two
files.

This matters for the same reason as 🔴 1. It also undoes what the check is
for: two homes for one sentence drift apart on the next edit. The fix below
rewords the bullet so that no run reaches 15 words. It also updates the pin
in `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`. Executed:
with both edits applied in the clone, the passage module and that pin pass.

After either fix, the ledger rows citing the changed units will drift: U1
for `RAN_TO_ITS_END`, if its hash covers the comment, and U3 and 1791270161's
W8 for the SKILL.md section and the pinned test. `evidence-check --reverify`
re-stamps them.

## The in-place ledger edits and the re-stamped rows

Executed: I compared 1791270161's fragment between `e7fc758a` and `8ce0dc79`
row by row.

- 53 rows changed, and 52 of them changed their anchors.
- Text changed in exactly four rows: W5, W8, `Corrected · R4` and
  `Corrected · D1`. D1 changed text only, which accounts for the 53rd row.
- The other 49 rows changed only anchor hashes and the `2026-10-07` stamp.

Read: each new clause matches the code and the documents.

- W5 orders `unplaced_red` before `unended`, as `base_word` does.
- W8 names the two stops and the count at `HEAD`.
- R4's "the limits it names rather than closes" fits a rule that now names
  three limits.
- D1 adds the `end` exit to the ways `new` becomes `new?`.

CI's `ledger` job passes at `5d21ccd9`.

## Regression tests to plant

None. Both 🔴 were caught by cases that already exist, and CI ran them. What
was missing was a run of them before the handover. That run is the sealer's
broad gate, and it is not yet due.

## Facts for the evidence ledger

- U1's Executed cell can add that the `end` exits match on pytest 6.1.0
  (Python 3.9), 7.0.0 and 9.1.1 with the recorder loaded. This was measured
  by #849 round 2.
- On all three builds, a failed collection under `-x` writes `end` 1 and no
  test line.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `RAN_TO_ITS_END`'s comment names pytest "9.1.1", so `test_no_loaded_file_names_a_version_at_or_above_the_running_one` fails on PR #851 | `skills/verify/scripts/broad_gate.py:1941` | open | executed: failing in CI on Ubuntu and Windows group 2 at `5d21ccd9` and in the clone; passes with two-component versions in the clone. Inside a unit round 1's fixes created |
| 🔴 2 | The **New?** bullet and rule 3 share a 21-word run the fix pass wrote into both, so two cases of the pasted-passage module fail on PR #851 | `skills/verify/SKILL.md:517` | open | executed: both cases failing in CI and in the clone, the shared run listed with the module's own helpers; passes with the reworded bullet and its pin in the clone |
| ⬜ 3 | `RAN_TO_ITS_END`'s comment, rule 3, the changelog fragment and one case's docstring say a failed collection gives exit 2; under `-x` it gives 1 | `skills/verify/scripts/broad_gate.py:1931` | open | executed on pytest 6.1.0, 7.0.0 and 9.1.1: `end` 1 and no test line; read: the base record then holds only the failed file, so every word stays right |
| 🟢 | round 1's finding 1 is closed — a base session whose `end` exit is not 0, 1 or 5 reads `new?` | `skills/verify/scripts/broad_gate.py:2008` | confirmed | executed: the new cases are red at `e7fc758a`'s code except the 0, 1 and 5 parameters, and green here; the exit mapping matches on pytest 6.1.0, 7.0.0 and 9.1.1; read: `wrap_session` of 6.1.0 and 7.0.0 |
| 🟢 | round 1's finding 2 is closed — the failure form counts the sessions at `HEAD` that stopped part-way | `skills/verify/scripts/broad_gate.py:3100` | confirmed | executed: the HEAD case is red at `e7fc758a` and green here and in Ubuntu's full run |
| 🟢 | round 1's finding 3 is closed — `last_sent` keyed on `id()` with the sender held | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:196` | confirmed | executed: S5 red at `e7fc758a`'s recorder, green here; read: a held sender cannot be freed, so an `id()` match is the same object |
| 🟢 | round 1's finding 4 is closed — phase 1's re-stamp count | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/phases/phase-1.md:19` | confirmed | read: "The other 27 rows" |
| 🟢 | round 1's open CI question is answered — macOS at `30ca8903` | PR #851 | confirmed | read: run 37545769411, all ten jobs passed |
| 🟢 | The two stops rule 3 names are real limits that need mechanism | `templates/config.md:334` | confirmed | executed on three pytest builds; read: closing either needs a new `end` field and a reader, which a fix pass may not add (`skills/code-review/orchestration.md`); filed under Deferred |
| 🟢 | The edits to 1791270161's W5, W8, `Corrected · D1` and `Corrected · R4` are faithful, and the 52 re-stamped rows changed nothing else | `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md:5` | confirmed | executed: a row-by-row comparison, with text changing in those four rows only; read against `base_word` and rule 3; CI `ledger` passes |
| 🟢 | The overview's two rows left to this round: a replaced worker, and a recorder that stops writing | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:206` | confirmed | read: a held sender cannot be replaced at its address; `give_up` sets `stream` to `None`, so `pytest_sessionfinish` writes no `end` line and the record counts as unended |
| ❓ | `pytest (macos-latest, 3.12)` had not finished | PR #851 | ❓ out of verified scope | read at 00:09 UTC: still pending. The same three cases are expected to fail there, but that has not been read. The orchestrator answers it by reading `gh pr checks 851` after the fix pass pushes, when every job reruns |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Two stops `RAN_TO_ITS_END` cannot see: `pytest.exit` with code 0, 1 or 5, and a plain run that `-x` or `--maxfail` stops, which writes 1. Closing them needs a new `end` field and a reader for it. Round 1's fix pass named them in rule 3 and the overview's *Not done*, but filed them nowhere | rung 2 candidate: #834, the 0.21.0 inventory to take before any reader or record changes; the `end` line is one of those records | the 0.21.0 run that takes #834's inventory, because adding the field changes a record that inventory must list first |

## Paste-ready fixes

### 🔴 1

```python
# Any other value is a return code `pytest.exit` or a plugin chose, and is no
# exit of a session that ran to its end. Each exit above was measured with
# the recorder loaded on pytest 6.1, 7.0 and 9.1 (#849 round 2). Two stops
```

### 🔴 2

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

Needs a fix: yes — 🔴 1 (the version-timer check fails on `broad_gate.py:1941`) and 🔴 2 (the pasted-passage check fails on the **New?** bullet and rule 3)
Loses a record or crashes: no

## Proof block

Files opened in this round:

- `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/rounds/round-1.md`, `rounds/round-1-report.md` (head), `overview.md`, `changelog.md`, `phases/phase-1.md`
- `skills/verify/scripts/broad_gate.py` (`RunRecord`, `RAN_TO_ITS_END`, `read_record`, `UNENDED_AT_BASE`, `base_word`, `compare_at_base`, `failure_lines`, `UNENDED_HERE`, `NO_SUMMARY`, `gate`'s suite branch)
- `skills/verify/scripts/pytest_record/specseal_pytest_record.py` (whole)
- `skills/verify/SKILL.md` (the **New?** bullet), `templates/config.md` (rule 3)
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_recorder_writes_what_its_process_ran.py` and `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` (the fix diff), `tests/test_release_hygiene.py` (`VERSIONS_OF_ANOTHER_PRODUCT`), `tests/test_no_passage_is_pasted_into_a_second_file.py` (its helpers)
- `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md`, `seal/ledger/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished.md`, `seal/releases/0.15.3.md` (A5)
- `skills/code-review/orchestration.md` (§*A fix pass adds the unit that pins it*), `docs/review-chain-spec.md` (§*Where a leftover goes*), `templates/sdd-phase.md` (§*What this phase removes*)
- pytest 6.1.0 and 7.0.0's main module (`wrap_session`), pytest-xdist 2.1.0's `dsession.py`
- CI: `gh pr checks 851`, the job logs of Ubuntu and Windows group 2 of run 37549327262, run 37545769411
