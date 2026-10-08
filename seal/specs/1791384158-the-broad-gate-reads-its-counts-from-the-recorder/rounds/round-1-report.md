# Round 1 report — 1791384158, the broad gate reads its counts from the recorder (#869, #852, #853)

- Target SHA: 0876a668d9266f6f2eb6341741e1058c709f68e0 (the clone's `git rev-parse HEAD`, executed)
- Base: `origin/release/v0.21.0`; diff `5623d728...0876a668`
- Round: 1, a finding round over the whole branch. No earlier round exists.

## How the findings relate

```
CI is red on three legs              -> 🔴 1  one stale registry row; the narrow set the
                                              handoff ran did not include its module
the record now feeds the counts      -> 🟡 2  a test with no file of its own drops out of
                                              the panel and the release note (branch-caused)
the values file loses `scale`        -> 🟡 3  in this repository every seal of the 0.21.0
                                              cycle is left undrawn, and the named recovery
                                              refuses as well
the record observes stops            -> ⬜ 4  one over-strictness nobody named
                                     -> 🟡 6  deferred: a HEAD run pytest.exit(0) stopped
                                              still seals with counts (pre-existing)
```

The core of the work holds. On pytest 9.1.1 and pytest-xdist 3.8.0 the
gate's counts equal pytest's printed line on every tree I built, plain and
under `-n 2`. The stamp draws byte for byte what 5623d728 drew at 0.90, and
the release seal reads an xdist run's record correctly.

## Findings

### 🔴 1 · CI is red on all three platforms, and the cause is one registry row

Executed: `gh api repos/MichaelYcJo/SpecSeal/actions/jobs/<id>/logs` for the
three failing jobs of run 37708644744, whose head SHA is the target (`gh api
…/actions/runs/37708644744`, executed). Each leg has exactly one failure, and
it is the same case:

- macOS, 3.12: `1 failed, 12765 passed, 89 skipped`
- ubuntu, 3.12: `1 failed, 12774 passed, 80 skipped`
- windows, `--group 2`: `1 failed, 6693 passed, 37 skipped`

The failing case is
`tests/test_a_script_says_which_interpreter_it_needs.py#test_no_shipped_script_needs_more_than_the_floor_without_saying_so`.
It asserts `['skills/verify/scripts/seal_stamp.py'] no longer carry the
construct they were classified for; drop the row rather than leaving a
classification of nothing`. The row at
`tests/test_a_script_says_which_interpreter_it_needs.py:481` classifies
`skills/verify/scripts/seal_stamp.py` for `zip(..., strict=True)` in
`admitted`. #853's rewrite of `admitted` removed that `zip`, so the row now
classifies nothing. I reproduced it in the clone (executed, see probes).

Why it matters: the pull request cannot merge on a red suite. The cause is
also a handoff gap. The smith's narrow set ran the eight guard modules, and
this module is not one of them, although it is the registry that keys on a
construct inside a shipped script. A change to a shipped script's constructs
should run this module too.

The fix is to drop the row. The floor guard in `seal_stamp.py` stays: the
hook relies on it to refuse cleanly, and the case's first half does not ask
for a row where no construct is found.

### 🟡 2 · The panel and the release note count fewer tests than pytest ran when a test has no file of its own

Read. The recorder writes no line for a report it cannot place
(`skills/verify/scripts/pytest_record/specseal_pytest_record.py#path_of`
returns None and the report is only added to `unplaced`). Such a report
therefore counts under no category. pytest's own line counts it. So
`skills/verify/scripts/broad_gate.py#suite_counts` prints a total short by
up to `unplaced`, and `.github/scripts/release_seal.py#suite_counts` returns
a `passed` that is short by the same amount.

This is branch-caused. At 5623d728 the panel read pytest's printed line,
which includes those tests. The overview lists it under *Not done* with "To
file", but a regression this branch introduces is this branch's to close.

The cost is a false number in two places a person trusts: the sealed
stamp's `suite` row and the published release note. The release seal's
docstring promises the opposite: "a record nobody can read is never a zero".

The fix follows the shape the branch already uses for an unread line.
`suite_counts` returns None where `record.unplaced` is not 0, so the panel
reads `exit <n>` and the failure form, which already prints `UNPLACED` with
the count, prints no count. The release seal refuses in the same words it
uses for an unread line.

One thing to check before taking the release half: whether this
repository's own full suite has any unplaced report. The 92-test sample I
ran has none (`unplaced 0`), but the full suite was not run here. If it
has one, the release seal would refuse every release until that test gets a
file.

### 🟡 3 · In this repository no stamp is drawn during the 0.21.0 cycle, and `seal-stamp --from` refuses as well

The spec names a window (Scope 5): a values file the tree's gate writes
meets the installed 0.20.0 hook, which refuses it for the missing `scale`
and leaves it pending. It then says `bin/seal-stamp --from <path>`, "which
the `SEALED` line already names, draws it at once". The `SEALED` line does
not name `bin/seal-stamp`. It names the bare command `seal-stamp --from`
(`skills/verify/scripts/broad_gate.py#NO_SESSION_FOUND`, `#DRAWN_AT_TURN_END`).

Executed: `which -a seal-stamp` resolves to the installed 0.20.0 plugin's
`bin/seal-stamp`. Run on a values file with no `scale`, that copy exits 2
with "`scale` is not a number. Nothing was drawn." The tree's
`skills/verify/scripts/seal_stamp.py --from` draws the same file and exits 0.

So the recovery that `docs/the-broad-gate.md` §*Where the stamp is drawn*
now names, in the sentence this branch added at lines 175–179, fails in the
exact case that sentence describes.

The window is also larger than "this repository alone, between merging this
work and the owner's next plugin update" suggests. In a tree that ships the
gate, the installed `broad-gate` hands the run over to the tree's own copy
(`skills/verify/scripts/broad_gate.py:3897–3907`, `shipped_gate`). That
covers every seal of every work item merged into `release/v0.21.0`,
including this item's own seal, taken in this worktree. The orchestrator's
statement that "the installed 0.20.0 gate is what runs this session's seals"
holds for the hook. It does not hold for the gate. Each of those seals is
left pending. After the update, the new hook draws them one per `Stop`
(`admitted`'s budget), each one stale.

Nothing is lost: the `Broad gate` cell is written either way. The defect is
a stamp that silently does not appear, together with a documented recovery
that refuses.

The cheapest fix closes the window rather than documenting it. `signal`
keeps writing a constant `scale` for one release. Every reader in this tree
already ignores it, and a hook or `seal-stamp` older than #853 then draws
the file. The alternative is to keep the window and correct the sentence:
the installed `seal-stamp` is as old as the hook, so in this repository the
stamp is drawn with the tree's `bin/seal-stamp --from <path>`. Both are
listed under *Decision left* below.

### ⬜ 4 · A `-x` run whose only failure is its last test reads as stopped

Executed (probe, plain pytest 9.1.1, `-x`, three tests with the last one
failing): every test ran, pytest printed `1 failed, 2 passed`, and the
`end` line carries `stopped: [{"by": "failures", "what": "stopping after 1
failures"}]`, so `unended` is 1. pytest sets `shouldfail` after the test
that reaches the limit, whether or not any test is left.

The direction is safe, because it turns `new` into `new?` and never the
other way. Rule 3 already names its one other over-strictness (a red
session's passing unplaced reports). This one is named nowhere: not in
`RAN_TO_ITS_END`'s comment, not in rule 3, and not in the recorder's
docstring. A person reading `UNENDED_HERE` on a run that finished will look
for a stop that did not happen. Naming it in `RAN_TO_ITS_END`'s comment is
enough.

### ⬜ 5 · The recorder counts reports that pytest's line leaves out

Read. pytest's summary line counts only the reports whose
`count_towards_summary` is true (`_get_reports_to_display`, `_pytest/terminal.py:1450–1453` in pytest 9.1.1). NAME NOT IN TREE

`category_of` does not consult it, so a plugin report that sets it to
false is counted by the gate and not by pytest. pytest 9's built-in
subtests do not set it, and my subtests probe matched (`2 failed, 1
subtests passed` on both sides). I did not run a plugin that does set it.
One guard in `category_of` closes the gap, and it is ⬜ because I know of no
such plugin in this repository's runs.

### 🟡 6 · deferred · A run at `HEAD` that `pytest.exit(returncode=0)` stopped still seals, with counts on the panel

Executed: a probe where the second of three tests calls `pytest.exit('bye',
returncode=0)` exits 0. The record says `stopped: [{"by": "exit", …}]` and
`unended` is 1. `suite_counts` gives `1 passed`, and the panel would print
`✓ 1 passed` over a run whose third test never ran.

This is not branch-caused. pytest itself printed `1 passed in 0.13s` before
its `Exit` banner, so 5623d728's text reader produced the same row. The
overview names it under *Not done*. It is deferred with the owner as its
answerer, as the overview says. A panel-only guard (`suite_counts` not
consulted where `run.unended`) is one line, but whether the gate should seal
at all over such a run is the larger question the overview raises.

### What the account claimed and what I found

| Claim (overview, handoff, prompt) | Found | How |
|---|---|---|
| the eight guard modules are green | holds: 456 passed across them and the ninth module, and the one failure is in the ninth | executed |
| the handoff's narrow set was enough | does not hold: CI is red on a module outside it (🔴 1) | executed (CI logs, clone) |
| the record's counts equal pytest's line (Q-M1, S5) | holds on 9.1.1 plain, `-n 2`, default verbosity, a collection error with and without `--continue-on-collection-errors`, and pytest 9 subtests | executed |
| the stamp's bytes are unchanged | holds: `stamp` both shapes, the no-disc rung and `admitted` at six budgets equal 5623d728's at 0.90 | executed |
| the release seal reads the record (`DRY_RUN` printed 72 passed) | holds: under the seal step's four variables and `-n 4`, two modules gave 92 passed, and `.github/scripts/release_seal.py#suite_counts` returned `(92, 0)` | executed |
| 23 `Corrected ·` and 78 `Re-read ·` rows | the counts hold; A5, C2, U1 and U4 read against the code hold | executed (count), read (rows) |
| two self-found gaps "to file" | one is branch-caused and is 🟡 2 here; the other is pre-existing and deferred (🟡 6) | read and executed |
| the installed 0.20.0 gate runs this session's seals | holds for the hook and not for the gate (🟡 3) | read |
| xdist under `-x` and `--maxfail` is observed | holds: both an `interrupt` and a `failures` entry, exit 2 | executed |
| `pytest.exit()` in an xdist worker is exit 3 with no entry | holds: exit 3, `stopped: []`, `unended` 1 through the exit net | executed |

Not probed, and therefore not judged: `--stepwise`. My probe ran it with
`-p no:cacheprovider`, so pytest refused it with exit 4. The smith's case
`test_a_plugins_stop_is_written_as_a_stop` covers it, and CI ran that case
green.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside
  `test_counts_the_record_cannot_vouch_for_are_none`: a `RunRecord` with
  `sessions` 1, `counts` `{"passed": 2}` and `unplaced` 1 gives
  `suite_counts` None. Red at the target.
- `tests/test_the_release_seal_is_drawn.py`, in
  `test_a_record_that_cannot_vouch_for_the_counts_is_a_failure_never_a_zero`:
  a keyed record whose `end` line carries `"unplaced": 1` is refused. Red at
  the target.
- For 🟡 3 under fix A: `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_values_file_holds_this_runs_panel`
  asserts the constant `scale` is written, and a case asserts the 0.20.0
  `read_values` contract holds (a number, not a bool).

## Facts for the evidence ledger

- `seal-stamp` on `PATH` is the installed plugin's copy, not the tree's. In a
  tree that ships the gate, the installed `broad-gate` hands over to the
  tree's copy (`skills/verify/scripts/broad_gate.py#main`, `shipped_gate`).
  The tree's gate and the installed hook can therefore differ inside one
  session.
- With `-x`, pytest sets `shouldfail` when the last test reaches the limit,
  so `stopped` is non-empty for a session that ran every test (probe above).

## Decision left

🟡 3 has two shapes, and the spec chose to name the window rather than close
it:

- **A, close it.** `signal` writes `"scale": 0.9` for one release, read by
  nothing in this tree. The installed hook draws every seal of the cycle.
  Cost: one field kept one release longer, and Corrected · N5 and the S13
  `"scale" not in values` assertion change.
- **B, keep it and correct the recovery.** `docs/the-broad-gate.md` says the
  installed `seal-stamp` refuses too, and names the tree's `bin/seal-stamp
  --from <path>`. Cost: every seal of the 0.21.0 cycle is drawn by hand or
  in a burst after the update.

The criterion is `CLAUDE.md` §*The goal a design is chosen against*: A needs
no person and B needs one per seal.

## Not verified

| Item | Who answers |
|---|---|
| The full suite, lint and typecheck at the fixed SHA | the sealer, once, after the rounds settle |
| Whether this repository's full suite has an unplaced report (decides 🟡 2's release half) | the sealer's run, read off its record's `end` lines |
| The `seal` job's suite step on a real tag | the next release's `seal` job, read by the owner |

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

Every probe file, tree, record and fixture, both scratch clones and the
clone's virtual environment were deleted before this report was handed
over.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 6: a run at `HEAD` that pytest stopped with exit 0 seals with counts | a new issue, as the overview's *Not done* proposes | the owner, who files it |
| `deferred_home`'s docstring still cites `suite_counts`' clock | #866's branch, per `plan.md` §*Seams* | #866's smith |

## Paste-ready fixes

### 🔴 1

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

### 🟡 2

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

### 🟡 3

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

### ⬜ 4

```text
# skills/verify/scripts/broad_gate.py, RAN_TO_ITS_END's comment — one sentence
# after the measurement sentence
# One over-strictness is named rather than closed: pytest sets `shouldfail`
# after the test that reaches `-x` or `--maxfail`, last test or not, so a
# session whose limit fell on its last test ran every test and still reads
# unended.
```

### ⬜ 5

```python
# skills/verify/scripts/pytest_record/specseal_pytest_record.py, category_of — first lines
        if not getattr(report, "count_towards_summary", True):
            return ""
```

Needs a fix: yes — 🔴 1 (the stale interpreter-registry row that turns CI
red on three legs), 🟡 2 (counts short by unplaced reports on the panel and
the release note), 🟡 3 (the scale window, which leaves every seal of the
0.21.0 cycle undrawn in this repository, and a recovery that refuses)
Loses a record or crashes: no

## Proof block

Files opened this round: `seal/specs/1791384158-the-broad-gate-reads-its-counts-from-the-recorder/spec.md`, `overview.md`, `survivors.md`; `seal/ledger/1791384158-the-broad-gate-reads-its-counts-from-the-recorder.md` (rows A5, C2, U1, U4 and the row counts); the diff of `skills/verify/scripts/broad_gate.py`, `skills/verify/scripts/pytest_record/specseal_pytest_record.py`, `skills/verify/scripts/seal_stamp.py`, `hooks/sealer-stamp.py`, `bin/seal-stamp`, `.github/scripts/release_seal.py`, `.github/workflows/publish-release.yml`, `docs/release-checklist.md`, `docs/the-broad-gate.md`, `agents/sealer.md`, `templates/config.md`, `skills/verify/SKILL.md`; `skills/verify/scripts/broad_gate.py` lines 3725–3760, 3814–3828, 3847–3935; `skills/verify/scripts/seal_stamp.py` lines 80–130; the recorder lines 130–460; `tests/test_a_script_says_which_interpreter_it_needs.py` lines 470–555; `tests/test_the_seal_is_taken_once_by_the_sealer.py` lines 3216–3250; `.github/workflows/publish-release.yml` lines 80–116; the installed 0.20.0 `seal_stamp.py#read_values`; in pytest 9.1.1, the terminal reporter's lines 625–640 and 1416–1453, the reports module's lines 160–175 and the subtests module's lines 355–420; `seal/config.md`'s `Broad gate` row; `assets/seals/README.md` lines 18–24.
