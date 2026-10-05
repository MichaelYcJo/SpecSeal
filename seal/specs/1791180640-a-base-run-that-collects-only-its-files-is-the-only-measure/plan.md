# Implementation Plan: a base run that collects only its files is the only measure (#789, #812, #807)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-05 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

The base comparison stops deciding which file a failure belongs to. A file
the base is asked about runs alone with `--junitxml` appended, and the
report says whether a test failed. Where one did, the gate re-runs the whole
row at the base with the file inserted after the measuring runner and
`--collect-only` carried in `PYTEST_ADDOPTS`. `failing on base too` is given
only where that pass shows one pytest session, listing the file and nothing
else. A run of several files only ever gives `new`. Every other outcome is
`new?` with its reason. `spec.md` holds the class, the measurements M1–M13
and the scope.

## Technical context

- `skills/verify/scripts/broad_gate.py#compare_at_base` (a3aa139a) walks
  `row_prefixes` once per group: the others together, then each candidate
  alone. It stops at the first prefix where `measured_summary` finds
  pytest's summary, or where a lone run is `collected_nothing`. This work
  replaces the stop test and the reader, adds the fallback from the group
  to lone runs, and adds the proof pass. The candidate split, the walk and
  the one `run(...)` call stay.
- `skills/verify/scripts/broad_gate.py#run` joins stdout and stderr, keeps
  `<name>.txt` and takes an `env`. It is unchanged. The proof pass passes
  its environment through `env`.
- `skills/verify/scripts/broad_gate.py#row_prefixes` returns substrings of
  the row (its docstring: "A prefix is a substring of the row as written"),
  so the rest of the row after prefix *k* is `command[len(prefix):]`, with
  its operator and its quoting intact.
- `skills/verify/scripts/broad_gate.py#quote` quotes the appended
  `--junitxml=<path>` and the inserted file, as it quotes the files today.
- **The first build's code is a source, not a base.** `git show
  a82f8f8f:skills/verify/scripts/broad_gate.py` holds the `--junitxml`
  append, the stale-report removal, the absolute report path and the
  report parse. Those are taken; its placement (report_cases, offsets,
  `spelled`, the tree listing), its collection pass over prefixes and its
  `UNPLACED` and NOTHING_TOGETHER reasons are not. The same commit's test
  module holds the end-to-end cases phase 1 and phase 2 port. Its round
  reports and `post-review-check.md` hold every probe layout, under
  `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/`.
  Read them with `git show`, never by checking the branch out.
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  holds `compare_at_base` to one `run(...)` call; the proof pass reuses it.
- `tests/test_release_hygiene.py` exempts `9.1.1` and `3.8.0` in
  `broad_gate.py` by naming the comments over `ERROR_RE`, `STOPPED_EARLY_RE`
  and `NOTHING_COLLECTED_RE`. Those comments retire, so the exemptions'
  reasons move to the comments that carry M1–M13. A new version token in a
  comment (8.1 for verbosity_test_cases) is that test's question too.
- **The failure scenario of this design, six months on.** A future pytest
  changes the collection-only trailer or the per-file listing. The proof
  reader then finds no trailer or a listing it cannot sum, and every file
  the base fails reads `new?`. That is noisy and strict, and the unit table
  over pytest's own lines says which shape moved. The one way to a wrong
  `failing on base too` is a second runner the pass cannot reach (spec
  Scope 7). That one is the same as at a3aa139a, and rule 3 names it where
  the row's author reads it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Place each failing test of a run of several files on a handed file by the report's names (the first build) | Seven layouts across three rounds and a post-review pass gave `failing on base too` where a3aa139a gave `new`, each through a different guess: a dotted name, an offset, `file`, `--junit-prefix`, a generated file, a symlink, a prefix | rejected by the owner, 2026-10-05 |
| B. Prove collection from the report itself (`xunit1`'s `file`, or `classname`) | `file` is where a test is defined, so a test another module inherits from `h` carries `h` (N1, Q4b). `classname` is the dotted name, so it is placement by name | rejected — measured by the first build's rounds 2 and 3 and its post-review pass |
| C. Drop the report and read the lone run's exit code once collection is proven | A part before the runner that fails under `&&` returns its own 1 with pytest never run. A wrapper may remap the code (`make` returns 2 for any failing recipe). Nothing would show which prefix reached a pytest that took the gate's arguments | rejected; the report stays as the settle signal and the outcome (M10, M11) |
| D. Prove collection over prefix *k* only, and count runners with the first build's collection pass over the other prefixes | Two mechanisms, and the counting one could not see a later runner inside `sh -c` (P7), one given `-p no:junitxml`, or one with its own `--junitxml` (Q8), because it detected a runner by the report it wrote | rejected in favour of E, which counts sessions by what pytest prints under collection and needs no report |
| **E. One whole-row collection pass per file the base fails, `--collect-only` carried in `PYTEST_ADDOPTS`, read for one trailer and a listing of `h` alone** | A runner started without the gate's environment, behind `\|\|`, behind a part that fails under collection, or at verbosity -4 is not counted. A rootdir that is not the run directory, and pytest before 8.1, read `new?`. Every part after the runner runs once more at the base | **chosen** |
| F. A gate-provided pytest plugin through `-p` and `PYTHONPATH`, recording absolute paths per process | Exact, but the gate's code runs in the row's interpreter on any Python and pytest version, and a row that sets `PYTHONPATH` loses it. The first build's framer rejected the same (its Alternative D) | rejected — the direction to take if E's limits are met in practice |
| G. `--rootdir=.` in the pass, so a cd row's listing is in the run directory's terms | With no ini file pytest sets `confcutdir` to the rootdir, so moving it can unload a `conftest.py` above the run directory, and the proof describes a different collection | rejected (read, not run); cd rows whose rootdir differs read `new?` |
| H. One collection pass for every failing file at once | Unsound: a row whose own argument names one handed file (`pytest tests/test_b.py` with `tests/test_a.py` handed) lists only handed files together, while the lone run of `tests/test_a.py` collects `tests/test_b.py` too | rejected (constructed) |
| I. Count pytest summaries in the branch's own output (#789's proposal) | Counts an inner pytester run's summary, so every failing file of a suite that tests a pytest plugin reads `new?` (#789's comment) | rejected |
| J. Per-directory report paths through `$PWD` in `--junitxml` (#807's direction) | `cmd.exe` sets no `PWD`, and a Python wrapper that changes directory leaves `PWD` stale, so two runners collide or one runner splits | rejected |
| K. Give `new?` to every file of a row with more than one runner, whether the base fails it or not | Costs one whole-row collection pass per comparison, on a passing base too, to replace a strict `new` with `new?` | not taken; `questions.md` Q1 |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The measurement: report appended and read for counts; the group and the lone-run table (spec Scope 4); the proof pass and its reader (Scope 5); the retired text readers (Scope 6); the four reasons, rule 3, the **New?** bullet, `compare_at_base`'s docstring and the release-hygiene exemptions, each pinned in the commit that changes it (Scope 8); every 0.18.2 case asserting `failing on base too` re-read under the new rule and listed in `phases/phase-1.md` (S16); S18's probe of this repository's row | S1–S16, each new case seen red at a3aa139a; S14's mutations; the narrow modules `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` and `tests/test_release_hygiene.py` | 6f80c650 |
| 2 | The regression corpus (S17): every layout of the first build's record and its 96-run inner-run matrix, run through the gate at a3aa139a and at phase 1's head; a table of the words in `phases/phase-2.md`; one parametrized end-to-end case planting every layout whose own record calls a `failing on base too` wrong at some SHA (by those tables: P1, P2, P3 ×2, P7 ×3, Q1, Q3, Q3b, Q4, Q5, Q8, Qf ×3, Qs2, R1 ×2, R2, R2b, R3, N1 ×4, N3, N7; the phase re-reads each layout before planting it), under its own row and under FILES_ROW | The table: no permissive word that a3aa139a did not give under the same row, except the named S3–S5 shapes. The planted case, seen red against the first build's gate at fb698f90 where that build regressed | b3137bd3 |
| 3 | The records: the ledger fragment, its new rows and the `Corrected ·` rows of spec Scope 10, re-reads through `evidence-check --reverify --into`; the changelog fragment `changelog.md` | `evidence-check` clean over the fragment; the changelog fragment names #789, #812 and #807, and what the release note reader sees change | |

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

No migration, no new environment variable of this repository's own, and no
new dependency. pytest's `PYTEST_ADDOPTS` is set for the proof pass only.

`CONTRIBUTING.md` §*What a change to a gate must carry*:

- **A test seen red.** Every new case of spec S1–S17 is run against
  a3aa139a's `broad_gate.py` and fails there, or against the first build's
  gate where the case guards its regressions (S17); the phase records say
  how each was seen.
- **The failure direction: the gate allows less.** `failing on base too`,
  the one word that lets a red suite through, is given in strictly fewer
  cases. The cost is `new?` where 0.18.2 gave a correct permissive word:
  rows that collect beyond their arguments, cd rows whose rootdir differs,
  and pytest before 8.1. Each `new?` sends a person to run a file at the
  base by hand. That is the cheaper mistake, because a wrong
  `failing on base too` lets a regression merge as somebody else's. Rule 3
  tells the row's author how to earn the measured word back.
- **The prompt budget: zero.** Nothing here asks a person anything; `new?`
  is a word in a report.
- **Platform honesty.** Measured on macOS against pytest 9.1.1 and
  pytest-xdist 3.8.0 (`spec.md` M1–M13). Linux and Windows (`cmd.exe`,
  `PYTEST_ADDOPTS` through `env`, the inserted quoted path, `rest` after a
  `cmd.exe` cut) are not run by this frame; CI's three-platform test job
  answers them (`questions.md` Q2).
- **Time.** A failing gate costs, per file the base fails, one more run of
  the whole row under collection only. A row whose runner is its last part
  re-runs only the parts before it; this repository's re-runs the two
  `ruff` parts. A base that passes every failing file costs what 0.18.2 cost. A group
  whose base run fails costs one more lone run per file in it.
