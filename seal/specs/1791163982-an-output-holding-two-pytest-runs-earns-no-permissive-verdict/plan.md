# Implementation Plan: an output holding two pytest runs earns no permissive verdict (#789)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-05 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

## Summary

The base comparison stops reading its words off pytest's printed text. It
asks pytest for a JUnit report at a path the gate chose, appended to every
run at the base. Only the pytest process that received the gate's arguments
writes that file, so nothing a test prints can reach it. A row with a second
runner is found by a collection-only pass over the prefixes after the
runner, and every file of such a row reads `new?`. The 0.18.2 design of
candidates, solo runs and kept files stays; only the reading under it
changes. `spec.md` holds the class and the scope.

## Technical context

- `skills/verify/scripts/broad_gate.py#compare_at_base` walks
  `row_prefixes` per group (the others together, then each candidate alone).
  It stops at the first prefix where `measured_summary` finds pytest's
  summary, or where a solo run is `collected_nothing`, and
  `verdicts_at_base` reads the words. This work replaces the stop test and
  the reader. The groups, the walk and the one `run(...)` call stay.
- `skills/verify/scripts/broad_gate.py#run` joins stdout and stderr, keeps
  `<name>.txt` and takes an `env`. It is unchanged; the collection pass
  passes its environment through `env`.
- `skills/verify/scripts/broad_gate.py#quote` quotes the appended
  `--junitxml=<path>` exactly as it quotes the files.
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  counts the `run(...)` calls in `compare_at_base`. The collection pass
  reuses the one call. 0.18.2's `overview.md` divergence row 1 is the
  measured reason.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` holds every case:
  `MEASURED_ENDINGS`, `SUMMARIES`, `NOTHING_COLLECTED` and `SUMMARY_LINES`
  are the unit tables over the readers that retire, `INNER_OUTPUT` is the
  end-to-end inner-run case, and the solo-runs pin and the unmeasured-word
  pin hold rule 3 and the reasons.
- `tests/test_release_hygiene.py` names `NOTHING_COLLECTED_RE`, `ERROR_RE`
  and `STOPPED_EARLY_RE`; it moves with them.
- **Measured by the frame, 2026-10-05, pytest 9.1.1 and pytest-xdist 3.8.0**
  (scratch project, deleted; the numbers are in `spec.md` §*The class*). The
  report is written on exit 1, on exit 2 (collection error, as a test with
  an empty `classname` and the dotted path in `name`), on exit 4 (missing
  path, plain) and on exit 5 (missing path, xdist), each with `tests="0"`
  where nothing was collected. Under xdist the controller writes it. Under
  `--collect-only` it is written with `tests="0"`. `-p no:junitxml` makes
  the option a usage error with no report.
- **The failure scenario of this design, six months on.** A runner that
  stops passing `--junitxml` to pytest, such as a wrapper rewritten with
  strict argument parsing, turns every measured word of that row into
  `new?`. That is noisy and safe. A future pytest that names a test
  differently in its report makes the reader place nothing, so files read
  `UNPLACED` and are still never permissive. The one way to a wrong word is
  a runner the collection pass cannot reach (`spec.md` Axis B's limit), and
  rule 3 says so where the row's author reads it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. The issue's proposal: count pytest summaries (or runners) in the branch's output and give every candidate `new?` past one | Every inner kind probed prints a summary, so a pytest-plugin suite reads `new?` everywhere (the comment's warning). "Every candidate" leaves p1b, whose permissive word comes from the group of non-candidates | rejected |
| B. Keep stdout and stderr apart in `run` and read pytest's lines off stdout (the comment's "code half") | Closes member 2 only. Measured: with the base passing everything under `-s` or `--capture=sys`, an inner run on **stdout** still gives `failing on base too`, and `-rN`, `-rP` and `-qq` are unchanged. It also changes the runner every arm shares | rejected |
| C. Cross-check pytest's last summary count against the `FAILED` lines after the last rule | Measured under `-rN`: the inner run's one `FAILED` line and the outer run's `1 failed` agree, so the check passes and the wrong file is named | rejected |
| D. A pytest plugin injected through `PYTEST_PLUGINS` and `PYTHONPATH`, recording each top-level session | Exact, but it loads the gate's code into the row's own interpreter on any Python and pytest version. It alters the branch's run, which CI mirrors. pytester loads it into inner in-process runs too, so it would need nesting detection | rejected — too much mechanism for the guarantee, and a change to the run CI mirrors |
| **E. The report pytest writes for the gate (`--junitxml` appended to every run at the base)** | A runner that does not hand the option on reads `new?` where it used to read a word. A test pytest names in a way the reader cannot place reads `UNPLACED` | **chosen** for members 2 and 3 |
| F. Find each file's runner in a two-runner row by collecting it in each one | One collection run per file per runner, and a rule for a file two runners both collect. More than the issue asks: no permissive word, and `new?` gives that | not taken — `spec.md` §*Out* |
| G. Treat any part after the runner as a possible second runner | Every runner-first row with a trailing lint part goes `new?` | rejected |
| **H. Count the row's runners with a collection-only pass over the prefixes after the runner** | A runner behind a part that exits non-zero at the base under collection alone, or behind `\|\|`, is not counted (`spec.md` Axis B). Measured: no pytest option makes collection exit 0 everywhere | **chosen** for member 1, with the limit named in rule 3 |
| I. Keep the text readers as a fallback where no report is written | The fallback is where every permissive word of the class comes from | rejected |

## Phases

Narrow runs only, by module and `-k`. The full suite, lint and typecheck are
the sealer's, once, after the rounds. Every new case is seen red against
a3aa139a's `broad_gate.py` before it is committed (§15), and the phase
record says how.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The report is the measurement.** Scope 1–3, 5 and 6: `--junitxml` is appended to every run at the base, a prefix settles on its report, the words come from the report reader, the text readers retire, and `NO_RUNNER` is reworded while `UNPLACED` and `NOTHING_TOGETHER` are added. The rule-3 sentences and the **New?** bullet for these change in the same commit, with their pins (Scope 7). The unit tables move to reports built from real pytest output. A probe settles `questions.md` Q1 (this repository's own row) and Q2 (the names) | S1–S6, S9; S5's existing cases by module; the reason and rule-3 pins of S10, each seen red with its sentence deleted; the probe's numbers in `phases/phase-1.md` | c2967fff |
| 2 | **More than one runner reads `new?`.** Scope 4: the collection pass over prefixes *k*+1…*n*, once per comparison, through the one `run` call; `MULTI_RUNNER`; `runners-at-base-<j>` kept. Rule 3's two-runner sentence is replaced, and the cost and the Axis B limit are added, with pins | S7, S8; the `MULTI_RUNNER` pin and the rule-3 pins of S10; the one-shell-site case unchanged | aeff7326 |
| 3 | **The records.** The ledger fragment `seal/ledger/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict.md`: new rows for Scope 1–5, `Corrected ·` rows for `seal/releases/0.18.2.md` D1, D2, `Corrected · B3` and `Corrected · S5` (a claim that went with its code holds the citation alone), and `evidence-check --reverify --into` for every other released row this change drifts. A `survivors.md` row for each removed sentence `survivor-check` finds still standing in a released record. This work item's `changelog.md` fragment. `tests/test_no_real_identifiers.py` and the record-reading modules run narrow | `evidence-check --strict`, survivor-check over `a3aa139a..HEAD`, `correction-check`, `tests/test_no_real_identifiers.py`, and `tests/test_a_record_states_what_the_tree_has.py`, each exit 0 | |

**The changelog fragment is written by phase 3 from what ships, and it is
not finished there.** A fix pass or a post-review fix that changes what the
gate does or says updates `changelog.md` in the same pass. That is a new
condition, a reworded reason, or a moved limit sentence. #797 is the lesson:
three of six 0.18.2 fragments described their build and not what their
rounds shipped.

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

No migration and no new dependency: the report is pytest's built-in
`--junitxml` and it is parsed with the standard library. No new variable for
a person to set. The gate sets `PYTEST_ADDOPTS` only in the environment of
its own collection runs, appended to the value it already has.

- **Compatibility.** A row whose runner does not hand `--junitxml` on to
  pytest reads `new?` (`NO_RUNNER`) where it read a word before. That covers
  a wrapper that drops its arguments, one that rejects unknown options, and
  `-p no:junitxml`. For a wrapper that dropped them the old word was a
  counterfeit `new`. For one that rejects unknown options it was measured,
  and that row pays. Rule 3 tells the row's author to pass the option on.
  A row with two runners reads `new?` for every failing file; before, it
  read the first runner's words, `failing on base too` among them.
- **Cost.** One more argument on every run at the base, and no extra run
  where the runner is the row's last part, which is this repository's row
  and every lint-first row. Where parts follow the runner, there is one
  collection run per later prefix, once per comparison, and only on a
  failing gate. Where the runner does not read `PYTEST_ADDOPTS` (an
  environment a wrapper scrubs), that run collects nothing and runs the
  tests, so it costs a real run. Rule 3 states it.
- **Kept files.** `--keep-output` now also holds a `.xml` beside every
  `suite-at-base-*.txt`, and `runners-at-base-<j>.txt` and `.xml` for the
  collection pass. `NO_RUNNER` names them, and the **New?** bullet's "open
  the kept `suite-at-base-*.txt` files" still holds.
- **Failure direction** (`CONTRIBUTING.md` §*What a change to a gate must
  carry*). Fewer wrong words in both directions, and more `new?`. A file
  reads `failing on base too` only where pytest's own report for the run the
  gate asked about places a failing test on that file alone. Every way the
  reading can fail lands on `new?`: no report, an unplaceable test, two
  runners, a group that collected nothing. That costs a reader one run by
  hand and never lets a failure through. The one remaining path to a wrong
  word is a runner collection alone does not reach, named in rule 3.
- **Prompt budget.** Zero. No question is added, at the gate or anywhere.
- **Platform honesty.** `--junitxml`, its report and `PYTEST_ADDOPTS` are
  pytest's on every platform. The path is quoted by `quote`, and the row
  still goes through `handed_to_shell` inside `run`. Executed on macOS only;
  Linux and Windows (`cmd.exe`) are CI's three-platform job. S6's `sh -c`
  case is POSIX-only and skips with its reason, and the xdist cases skip
  where the fixture's interpreter lacks `xdist`.
- **Siblings cut from a3aa139a.** D (#797) may put its fragment check in
  `broad-gate --preflight`. That is the same `broad_gate.py` and the same
  test module, in the preflight's region, far from `compare_at_base`: a
  textual merge at most. A (#785, #792, #781) changes `evidence-check
  --reverify`, which phase 3 runs. Phase 3 uses whichever behaviour the
  release branch holds when it runs.
