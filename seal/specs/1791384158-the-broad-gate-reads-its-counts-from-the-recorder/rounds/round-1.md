# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — review round 1

| Field | Value |
|---|---|
| Target SHA | 0876a668d9266f6f2eb6341741e1058c709f68e0 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 880 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (the stale interpreter-registry row that turns CI red on three legs), 🟡 2 (counts short by unplaced reports on the panel and the release note), 🟡 3 (the scale window, which leaves every seal of the 0.21.0 cycle undrawn in this repository, and a recovery that refuses) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the build at 0876a668, against 5623d728, since the release branch's #858 and #864 are not merged in yet. The spawn named six things to attack. First, the failing CI jobs of PR #880, read from their logs. Second, the recorder's category per report against pytest's own counting. Third, the stopped field across exit codes, -x, --maxfail, --stepwise, KeyboardInterrupt and xdist. Fourth, summing several sessions. Fifth, the release seal's refusal paths and the scale retirement's compatibility window. Sixth, the 23 Corrected rows. It also asked for the reviewer's own axes and the eight guard modules once. Facts arrived labelled. Executed by the orchestrator: gh pr checks 880, with the failing macOS, ubuntu and windows-group-2 legs. Read from the smith: Q-M1, the mutations, the stamp hashes, the DRY_RUN seal and the ledger rows. Read: the installed 0.20.0 hook governs this session's stamps.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | CI is red on three legs: the interpreter registry still classifies `seal_stamp.py` for a `zip(..., strict=True)` that #853 removed | `tests/test_a_script_says_which_interpreter_it_needs.py:481` | open | executed: three CI logs at the target SHA and a run in the clone give the same single assertion |
| 🟡 2 | the panel's `suite` row and the release note's `passed` count fewer tests than pytest ran when a report had no file of its own | `skills/verify/scripts/broad_gate.py:2796` | open | read: `path_of` writes no line for an unplaced report, so it counts under no category; 5623d728 read pytest's line, which counted it; branch-caused |
| 🟡 3 | in this repository every seal of the 0.21.0 cycle is left undrawn, and the `seal-stamp --from` the `SEALED` line names refuses as well | `skills/verify/scripts/broad_gate.py:3817` | open | executed: the installed `seal-stamp` exits 2 on a file with no `scale`, and the tree's draws it; read: the installed gate hands over to the tree's copy at `broad_gate.py:3897` |
| ⬜ 4 | a `-x` session whose only failure is its last test reads as stopped, and no reader is told | `skills/verify/scripts/broad_gate.py#RAN_TO_ITS_END` | open | executed: every test ran, `stopped` holds a `failures` entry, `unended` is 1 |
| ⬜ 5 | `category_of` counts reports that pytest's line leaves out | `skills/verify/scripts/pytest_record/specseal_pytest_record.py#category_of` | open | read: pytest 9.1.1 `terminal.py:1450–1453` filters the reports it counts; not reproduced with a real plugin |
| 🟡 6 | a run at `HEAD` that `pytest.exit(returncode=0)` stopped seals with `✓` counts | `skills/verify/scripts/broad_gate.py#panel` | deferred new issue | executed: exit 0, `unended` 1, counts `1 passed`; pre-existing, because pytest printed `1 passed in 0.13s` and 5623d728's text reader took it; the overview's *Not done* names it |
| 🟢 | the recorder's counts equal pytest's printed line | `skills/verify/scripts/broad_gate.py#suite_counts` | confirmed | executed on pytest 9.1.1: plain, `-n 2`, default verbosity, a collection error both ways, subtests |
| 🟢 | the stamp draws the same bytes as 5623d728 at 0.90 | `skills/verify/scripts/seal_stamp.py#admitted` | confirmed | executed: both shapes, the no-disc rung, `admitted` at six budgets |
| 🟢 | the release seal reads an xdist run's record | `.github/scripts/release_seal.py#suite_counts` | confirmed | executed: 92 passed under the seal step's variables with `-n 4`, `(92, 0)` |
| ❓ | the full suite at the target | the row in `seal/config.md` | ❓ out of verified scope | contract §2 gives the broad run to the sealer; the sealer answers it after the rounds |

## Paste-ready fixes

```diff
--- a/tests/test_a_script_says_which_interpreter_it_needs.py
+++ b/tests/test_a_script_says_which_interpreter_it_needs.py
@@ CLASSIFIED = {
     "skills/verify/scripts/session_cost.py": "deferred, seal/follow-up.md (#226)",
-    "skills/verify/scripts/seal_stamp.py": (
-        "guarded -- it refuses at entry with a sentence naming the floor, the "
-        "block copied from round_record.py; `zip(..., strict=True)` in "
-        "`admitted` (#717) is 3.10's"
-    ),
 }
```
```python
# skills/verify/scripts/broad_gate.py, suite_counts — the guard, and one
# sentence added to its docstring: "…, where a report was counted under no
# category because it had no file of its own (`unplaced`), or where no
# report was counted at all."
    if (
        not record.sessions
        or record.unread
        or record.unplaced
        or not record.counts
    ):
        return None
```
```python
# .github/scripts/release_seal.py, suite_counts — after the `unended` refusal
    if record.unplaced:
        raise ValueError(
            f"{record.unplaced} of the suite's tests and collections had no "
            "file of their own and were counted under no category"
        )
```
```python
# skills/verify/scripts/broad_gate.py, signal — fix A, in the values dict
        # Read by nothing since #853. Written for one release so that a
        # `Stop` hook or a `seal-stamp` older than #853, which refuses a file
        # without a numeric `scale`, still draws what this gate writes: the
        # installed copy hands a tree that ships the gate to the tree's own
        # copy, while the hook stays the installed one. Drop it once the
        # installed plugin is 0.21.0 or later.
        "scale": 0.9,
```
```text
# skills/verify/scripts/broad_gate.py, RAN_TO_ITS_END's comment — one sentence
# after the measurement sentence
# One over-strictness is named rather than closed: pytest sets `shouldfail`
# after the test that reaches `-x` or `--maxfail`, last test or not, so a
# session whose limit fell on its last test ran every test and still reads
# unended.
```
```python
# skills/verify/scripts/pytest_record/specseal_pytest_record.py, category_of — first lines
        if not getattr(report, "count_towards_summary", True):
            return ""
```

## Executed probes

| What was run | Result |
|---|---|
| `gh api repos/MichaelYcJo/SpecSeal/actions/runs/37708644744` | head SHA 0876a668, conclusion failure |
| `gh api …/actions/jobs/{113088994233,113088994399,113088994254}/logs` | each: 1 failed, the interpreter case; macOS 12765 passed, ubuntu 12774 passed, windows group 2 6693 passed |
| `bin/test` in a `--no-local` clone at the target, over the eight guard modules and `tests/test_a_script_says_which_interpreter_it_needs.py` | `1 failed, 456 passed`; the one failure is the CI case, and the eight guard modules are green |
| probe file named test_tmp_probe.py: pytest 9.1.1 over a tree with pass, fail, skip, xfail, xpass, strict xpass, setup and teardown errors, two module-level skips and an import error, with `--continue-on-collection-errors`, read through the clone's `read_record` and `suite_counts` | plain, `-n 2` and default verbosity: pytest `3 failed, 2 passed, 3 skipped, 1 xfailed, 1 xpassed, 4 errors` and the gate the same; without the flag: `2 skipped, 1 error` on both sides, exit 2, an `interrupt` entry |
| the same probe: pytest 9 `subtests`, one failing subtest | `2 failed, 1 subtests passed` on both sides |
| the same probe: `-x` with the last test failing | exit 1, `1 failed, 2 passed`, a `failures` entry, `unended` 1 |
| the same probe: `pytest.exit(returncode=0)` plain, then under `-n 2` | plain: exit 0, an `exit` entry, counts `1 passed`, `unended` 1; xdist: exit 3, `stopped` empty, `unended` 1 |
| the same probe: `-n 2 -x` and `-n 2 --maxfail=1` | exit 2, an `interrupt` and a `failures` entry each |
| the same probe: `--sw` with `-p no:cacheprovider` | exit 4, a probe error and not a reading |
| the installed `seal-stamp --from` on a values file with no `scale`, then the tree's `seal_stamp.py --from` | installed: exit 2, "`scale` is not a number"; tree: exit 0 |
| `stamp` and `admitted` loaded from 5623d728 and from the target | equal in both shapes, on the no-disc rung and at budgets 100 to 50,000 |
| the recorder and release-seal test modules under the seal step's four variables, `-n 4`, then `.github/scripts/release_seal.py#suite_counts` on that record | 92 passed; `(92, 0)`, `unended` 0, `unread` 0, `unplaced` 0 |
| `bin/evidence-check --strict .` in the worktree, with this report on disk | exit 0, 0 refused |
| `round_record.py new` over this report, in a second scratch clone, as a parse check | exit 0; the verdict rows, both terminal lines and every fence were read |
| the broad gate (full suite, lint, typecheck) | not yet: the sealer's, once, after the rounds |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 6: a run at `HEAD` that pytest stopped with exit 0 seals with counts | a new issue, as the overview's *Not done* proposes | the owner, who files it |
| `deferred_home`'s docstring still cites `suite_counts`' clock | #866's branch, per `plan.md` §*Seams* | #866's smith |
