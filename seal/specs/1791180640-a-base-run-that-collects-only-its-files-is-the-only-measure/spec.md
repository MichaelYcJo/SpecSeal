# Feature Specification: a base run that collects only its files is the only measure (#789, #812, #807)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#789 (and its comment), #812 and #807, read 2026-10-05 at a3aa139a. This is
a redesign the repository owner chose after the 3+ fix rule
(`routing.md` §*Why this way*). The first build of #789 (work item
`1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict`,
PR #804, closed unmerged, its record on
`origin/fix/789-an-output-holding-two-pytest-runs-earns-no-permissive-verdict`
at a82f8f8f) read the base's verdicts from a JUnit report. It then had to
decide which handed file each failing test in that report belonged to, the
"placement". It fixed placement three times, and a review found a new
layout each time where the permissive word came back. Those layouts were
dotted names that fit another module, offsets, `xunit1`'s `file` naming
where a test is defined, `--junit-prefix`, generated files, a tracked
symlink, and a same-named module confirming a path by prefix.

**The anchor, the owner's decision of 2026-10-05: `failing on base too` is
given only where the base run collected nothing but the files it was
handed.** Then every test that run collected came from a handed file, and
no placement is needed. A run that cannot be shown to have collected only
its files gives the strict word, `new?`.

## The frame in one paragraph

A failing file the base is asked about is run **alone**, so "the files it
was handed" is one file and nothing has to be placed. The run appends
`--junitxml=<path>`, and that report says whether a test failed, whatever a
test printed. Where the report holds a failure, the gate asks pytest one
more question before it gives the permissive word. It re-runs **the whole
row** at the base, with the file inserted after the part that measured it,
and `--collect-only` carried in `PYTEST_ADDOPTS`. Under collection only no
test runs, so no inner run exists to print anything. The word is
`failing on base too` only where that pass shows exactly one pytest session,
and that session listed tests from the handed file and nothing else. Every
other outcome reads `new?` with its reason.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `routing.md` §*Why this way* — the owner's decision of 2026-10-05 | The anchor above. The permissive word needs a run that collected only its files; a run that cannot be shown to have done so reads `new?`. No placement by name, in any form |
| `agents/sealer.md` §*Boundaries* — "`new` and `failing on base too` are the gate's words: it re-ran the failing files at the base to earn them", and `new?` "where no run at the base measured the file" | The words and their meanings do not change. Under this work a run **measures** a file only where it collected nothing else, so the sentence stays true and is not edited (Scope 9) |
| `README.md` §*The chain* flow, "failing on base too → named as a follow-up, does not block"; `skills/verify/SKILL.md` §*The broad gate*, the three words | `failing on base too` is the one permissive word. Every acceptance clause below is about when it may be given |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides between a proof the gate runs itself and `new?`, which sends a person to the base by hand. A measured word is preferred wherever a run can earn it. That is why the proof pass exists rather than giving every multi-file or multi-runner row `new?` |
| `templates/config.md` §*Broad gate* §*Choosing a value — the criterion*, rule 3 | The one home of what the comparison costs a row and which rows it cannot measure. Rewritten whole by this work (Scope 8) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A case seen red, a failure direction, a prompt budget and platform honesty. Answered in `plan.md` §*Operational impact* |
| `skills/agent-contract/SKILL.md` §12, §13, §14, §15 | The class is enumerated by construction below. Every changed reason and rule-3 sentence is pinned in the commit that changes it. Every new case is seen red at a3aa139a |
| Work item `1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory` (0.18.2), `spec.md` Scope 1–6 | What 0.18.2 built and this work keeps: the root's tree nominates and decides nothing; a candidate runs alone; a file run alone that collects nothing at the base reads `new`; the prefixes are found by running |
| `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite` | `compare_at_base` keeps one `run(...)` call. The proof pass goes through that call, as the first build's collection pass did |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from`; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | Released rows this work makes false are corrected by `Corrected ·` rows in `seal/ledger/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure.md`, never by editing `seal/releases/*.md` (Scope 10) |

## Measured by this frame (executed 2026-10-05)

pytest 9.1.1 and pytest-xdist 3.8.0 in a scratch project under the
scratchpad, deleted after the frame; pytest 7.4.4, 8.0.0 and 8.1.1 through
`uvx`; and this repository's own `bin/test` in this worktree, whose `.venv`
it built. `-p no:cacheprovider` throughout. "The collection pass" below is
`PYTEST_ADDOPTS="--collect-only -o verbosity_test_cases=-2 -vv"`.

| # | What was run | What it showed |
|---|---|---|
| M1 | The pass over a row with a handed file, under the row flags none, `-q`, `-v`, `-q -n 2`, `-q --no-header -rN` | One listing line per collected file, `tests/test_a.py: 2`, and one trailer, `2 tests collected in 0.00s`, bare or between `=` rules. Under `-n 2` xdist does not distribute a collection-only run: the controller lists once |
| M2 | The same under `-qq` and `-qqq` | pytest prints no trailer below verbosity -1. With `-v` carried in the environment `-qq` gets its trailer back and `-qqq` does not; with `-vv` both do. Hence `-vv` |
| M3 | A row that collects beyond its file, `pytest -q tests tests/test_a.py` | The listing names every collected file (`tests/test_a.py: 2`, `tests/test_b.py: 1`) and a collection error elsewhere, `3 tests collected, 1 error` |
| M4 | `-q -k a1` | `tests/test_a.py: 1` and `1/2 tests collected (1 deselected)`: the listing is what runs, after deselection |
| M5 | A handed file that fails to import | No listing line; `ERROR tests/test_err.py` in the short summary; trailer `no tests collected, 1 error`; exit 2 |
| M6 | Two runners in one row: `pytest -q h ; cd sub && pytest -q`, and `pytest -q h && sh -c 'cd sub && pytest -q'` | Two trailers. A runner inside `sh -c` inherits `PYTEST_ADDOPTS` |
| M7 | `pytest --version && pytest -q h` | `pytest 9.1.1` and one trailer: the version part is not a session |
| M8 | A `cd sub` row, with `pytest.ini` at the root and with none | With the ini at the root pytest's rootdir is the root and the listing reads `sub/tests/test_a.py: 1`, not the handed `tests/test_a.py`. With no ini it reads `tests/test_a.py: 1` |
| M9 | The `&&` stop: `pytest -q tests/test_err.py && cd sub && pytest -q` | Exit 2 after the first session, so the second runner is never reached. Adding `--continue-on-collection-errors` still exits 1 |
| M10 | The measuring run, `--junitxml` appended: a failing file; a missing file plain and under `-n 2`; a file that fails to import; a passing file | Report `tests=2 failures=1`; `tests=0` with exit 4, and `tests=0` with exit 5 (xdist took 25 s to say so); one `testcase` with an `error` child and an empty `classname`, exit 2; `tests=1`, exit 0 |
| M11 | A failing test that runs pytest in a subprocess and writes that run's output to stderr, under `-q -s`, `-q -rN`, `-qq` and `-q -s -n 2`, report appended | The report names only the outer test, with its failure, in all four. The inner run's `1 passed` is in the text and nowhere in the report |
| M12 | pytest 7.4.4, 8.0.0 and 8.1.1 under the collection pass | 7.4.4 and 8.0.0 do not know verbosity_test_cases and print a tree (`<Module tests/test_a.py>`, `<Function …>`); 8.1.1 prints `tests/test_a.py: 2`. Each prints the trailer |
| M13 | This repository: `bin/test -q tests/test_release_hygiene.py` under the pass, then the whole row `uvx ruff check . && uvx ruff format --check . && bin/test -q tests/test_release_hygiene.py` under it, then `bin/test -q tests/test_release_hygiene.py --junitxml=<scratch path>` | One session, `rootdir` the worktree, listing `tests/test_release_hygiene.py: 50` alone, trailer `50 tests collected`, whole row exit 0. The report is written under `-n auto` with `tests="50"` |

**What M13 settles for this repository's own row.** `bin/test` passes its
arguments straight through and runs pytest at the repository root
(`.github/scripts/run_tests.py#main`, read): a row of `-q` and a file
becomes `pytest -q <file> -n auto`, which collects that file alone. The
runner is the row's last part, so the proof pass is the row as written with
the file appended. It re-runs the two `ruff` parts once per file that fails
at the base. A file that fails at the base and on the branch reads
`failing on base too`. A file the base passes reads `new`. A file the base
lacks reads `new`, from its solo run's `tests=0` with exit 5. A base where
`ruff` fails stops every prefix before the runner, and every file reads
`new?` with the no-runner reason, as it does at a3aa139a.

## The class, enumerated by construction

**The defect is one sentence: the gate gave the permissive word to a file
on the strength of a failure it could not show was that file's.** The first
build's three rounds and its post-review pass each found a new way the
"whose" could be wrong, because each way was a guess from a name. This
design asks the question differently. A word is given only where the "whose"
needs no answer, because the run collected one file.

So the paths to `failing on base too` are enumerated from the new code's
construction, not from layouts. A file `h` reads it only where all of these
hold:

1. **`h` ran alone.** A run of several files gives `new` to all of them
   where every test passed, and otherwise sends each file to run alone. No
   permissive word ever comes from a run of more than one file.
2. **The first prefix whose last part wrote the gate's report** at the
   path the gate chose is the measuring run, and that report holds at least
   one `testcase` with a `failure` or `error` child.
3. **The proof pass shows one session**: exactly one trailer, read after
   ANSI colour sequences are removed.
4. **That session listed only `h`**: every listing line names `h`, and the
   counts on them add up to the trailer's collected (selected) count.
5. **Any collection error is `h`'s**: where the trailer counts errors, it
   counts one, and an `ERROR` line names `h` and no other path.

Each way the word could still be wrong is a way to fake 3, 4 or 5. Every
such way is named in Scope 7 as a limit or closed by a case below:

- **A second runner the pass does not see**, which fakes 3. It is one
  started without the gate's environment (`tox`, `nox`, `env -i`, a
  container); a row that sets `PYTEST_ADDOPTS` itself; one behind `||`; one
  behind a part that exits non-zero under collection alone (M9, including
  `h`'s own collection error); and one at verbosity -4 or below, which
  prints no trailer even with `-vv`. Each is a limit, named in rule 3.
- **A listing line that names `h` but is another file**, which fakes 4.
  The listing is pytest's node id, relative to its rootdir, and `h` is
  relative to the directory the branch's runner ran in (`FAILED` lines are
  cwd-relative). Where the two directories differ, `h`'s own tests are
  listed under another name (M8), so 4 fails and the word is `new?`. They
  coincide only in a run that dropped `h` and collected a same-named file
  under its rootdir, and such a runner collected that file under the name
  the branch's `FAILED` line gave it. This is read, not measured, and is
  named.
- **A line no pytest wrote**: text from a part that is not pytest, shaped
  like a trailer or a listing line. Shaped like a trailer, it adds a second
  session, so 3 fails (strict). Shaped like a listing line naming `h`, it
  breaks the count in 4 unless its number makes up the difference. This is
  constructed only, and needs a part printing pytest's collection lines
  about a file it did not collect.

**What the first build's class becomes.** Every placement layout (P1, P2,
Q1, Q3, Q3b, Q4, Q4b, Q4c, Q5, Qf, R1, R2, R2b, R3, N1, N1b, N1c, N3, N4,
N6, N7) is a row that collects beyond its file, or a file whose base
failure lives in another module. In the first case 4 fails, because the
listing names the other files. In the second, `h` run alone holds no
failing test. Neither needs the layout to be recognised. The multi-runner
layouts (P3, P7 in its three variants, Q8, Qs2, #761's p1 and p1b) fail 3,
because their second runner inherits `PYTEST_ADDOPTS`. That covers #807's
two members: a later runner inside a part that drops its arguments (M6),
and one given `-p no:junitxml`, since the pass needs no report. It also
covers round 2's own `--junitxml` member (Q8).

## Scope

### In

1. **Every run at the base appends `--junitxml=<path>`** after the files,
   as one quoted argument (`quote`). The path is absolute, in the kept
   directory, under the run's own stem: `suite-at-base-<k>.xml`,
   `suite-at-base-<k>-<n>.xml`. A stale file at that path is removed before
   the run. Kept from the first build, with its two cases (a stale report
   settles nothing; a relative `--keep-output` under a `cd`).
2. **A prefix settles where its report was written and parses.** The text
   is no longer asked whether pytest ran. Where no prefix writes one, each
   file of that run reads the no-runner reason (`NO_RUNNER`, reworded to
   name the report). Kept from the first build. A part that drops its
   arguments, `-p no:junitxml` and a wrapper that refuses the option read
   `new?`; at a3aa139a they read `new`.
3. **The report is read for counts, never for names.** These are the
   `testcase` elements, and among them the ones with a `failure` or `error`
   child. `classname`, `name` and `file` are not read. `-o
   junit_family=xunit1` is not appended. It is one pure function of (report
   text) → (tests, failing). It accepts a `testsuites` root or a bare
   `testsuite`, and treats a report that does not parse as no report.
4. **The groups.** 0.18.2's split is kept: a failing file the base's root
   tree lacks is a candidate and runs alone; every other failing file runs
   in one group first. The group's report decides one thing only. Where it
   holds at least one test, none failing, and the run exited 0, every file
   of the group reads `new`. In every other case, each file of the group
   runs alone: a failure, an error, no test, a non-zero exit. A run alone of
   file `h`, at its settling prefix, reads:

   | Report | Exit | Word |
   |---|---|---|
   | written, no `testcase` | 4 or 5 | `new` (the base has no test in `h` where the row runs it; 0.18.2's `collected_nothing`, now off the report) |
   | written, no `testcase` | other | `new?`, the not-ended reason (below) |
   | written, tests, none failing | 0 | `new` |
   | written, tests, none failing | non-zero | `new?`, the not-ended reason: the run ended with that exit and its report names no failing test |
   | written, a failing or erroring test | any | the proof pass (Scope 5) |
   | not written at any prefix | — | `new?`, `NO_RUNNER` |

5. **The proof pass.** Where a run alone of `h` settles at prefix *k* with a
   failing test, the gate runs `prefix_k + " " + quote(h) + rest`, where
   `rest` is the row after prefix *k* as written (`row_prefixes` returns
   substrings, so it is `command[len(prefix_k):]`). It runs in the same
   scratch worktree, with the gate's environment and
   ` --collect-only -o verbosity_test_cases=-2 -vv` appended to whatever
   `PYTEST_ADDOPTS` already holds. It goes through the one `run(...)` call
   and is kept as `collected-at-base-<n>.txt` beside the run it proves. Its
   reader is one pure function of (text, `h`) → proven, or the reason it is
   not. It removes ANSI colour sequences, then applies the five conditions
   of the class above:
   - exactly one trailer, `(no tests collected( \(D deselected\))?|N tests?
     collected|S/N tests collected \(D deselected\))(, M errors?)? in Ts`,
     with an optional `(h:mm:ss)` and optional `=` padding (pytest 9.1.1's
     _build_collect_only_summary_stats_line, read);
   - every line of the shape `<path>: <count>` names `h`, and the counts
     add up to the trailer's collected count (S where deselection shows S/N);
   - errors: none, or one, with a line `ERROR <h>` or `ERROR <h> - …` and
     no `ERROR` line naming another path.

   Proven → `failing on base too`. Not proven → `new?` with one of two
   reasons. MULTI_RUNNER is used where the count of trailers is not one,
   and says the row ran pytest more than once (or not at all) when told to
   collect only. The beyond reason is used for everything else, and says
   the run collected tests beyond `h`, or its collection could not be read.
   Each reason names its kept file and how a row earns the word (Scope 8).
   The proof runs only where the base fails `h`, so a passing base costs
   nothing new. It runs once per such file, not once per prefix.
6. **The text readers that decided words retire**: `PYTEST_SUMMARY_RE`,
   `SHORT_SUMMARY_RE`, `NOTHING_COLLECTED_RE`, `NOTHING_COLLECTED_EXITS`
   where nothing else reads it, `ERROR_RE`, `STOPPED_EARLY_RE`,
   `measured_summary`, `collected_nothing`, and `verdicts_at_base` as a text
   reader. `FAILED_RE` and `failing_files` stay, because they read the
   branch's own run (Out, Axis C). `STOPPED_EARLY` as a reason is replaced
   by the not-ended reason of Scope 4. The unit tables over the retired
   readers (`MEASURED_ENDINGS`, `SUMMARIES`, `NOTHING_COLLECTED`,
   `SUMMARY_LINES` and the cases over them in
   `tests/test_the_seal_is_taken_once_by_the_sealer.py`) become tables over
   the report reader and the proof reader, covering the same shapes.
   `tests/test_release_hygiene.py`'s `9.1.1` and `3.8.0` exemptions name
   the comments over the retired constants. They move to the comments that
   now carry the measurement, with M1–M13's facts.
7. **Named limits, each stated in rule 3 word for word as it ships**, every
   one strict except the two marked:
   - a row whose runner collects beyond the files appended to it
     (`pytest -q tests`, `pytest -q tests/unit` with a file appended): every
     file the base fails reads `new?`. **This is the anchor, not a defect.**
     A row earns the word by letting the appended files be pytest's only
     paths, `pytest -q` with `testpaths` in the ini rather than
     `pytest -q tests`;
   - a run whose pytest rootdir is not the directory its runner ran in
     (M8: a `cd sub` row with the ini at the root, or an ini below the run
     directory): `new?` for every file the base fails, where 0.18.2 gave a
     correct `failing on base too` (Q10, Q11);
   - pytest older than 8.1, which does not know verbosity_test_cases
     (M12): `new?` for every file the base fails;
   - a row that sets `PYTEST_ADDOPTS` itself, or runs at verbosity -4 or
     below: `new?` where it hides the pass;
   - **a second runner the pass does not reach or does not reach with the
     gate's environment** (the class above): its file can read
     `failing on base too` from the measuring runner's directory.
     **Permissive, named, and the same as at a3aa139a**;
   - **a two-runner row where the base passes `h` under the first
     runner**: `new` from the wrong runner. Strict, and the same as at
     a3aa139a. `questions.md` Q1 asks whether to buy `new?` for it;
   - every part of the row after the measuring runner runs as written, at
     the base, under collection only, once per file the base fails. That
     includes parts the branch's own run never reached because `&&` stopped
     at its failing suite. Writes inside the scratch worktree go with it;
     anything outside it does not. Rule 3 states this as the cost.
8. **What a person reads changes, and is documented and pinned in the same
   commit (§14):**
   - `templates/config.md` rule 3, rewritten whole. It covers how the runner
     is found (by its report), the solo run, the proof pass, the anchor, how
     a row earns the word, the cost (one more run of every prefix up to the
     runner per failing file; one whole-row collection run per file the base
     fails), and every limit of Scope 7. Its pin in
     `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py::test_each_rule_is_carried_with_the_reason_it_is_a_rule`
     ("until one prints pytest's summary") moves to the new reason sentence;
   - `skills/verify/SKILL.md` §*The broad gate*, the **New?** bullet. Its
     causes become the report not written, a run that collected beyond the
     file or ran pytest more than once, and a run that ended without naming
     a failure. It still sends the reader to the kept files and to the base
     by hand. Its pin moves with it;
   - every reason (`NO_RUNNER` reworded, the not-ended reason, the beyond
     reason, MULTI_RUNNER), each starting `NOT_MEASURED` and pinned whole
     in `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`;
   - `compare_at_base`'s docstring, rewritten whole, and the comments over
     every constant that stays. The module docstring keeps "`new?` with the
     reason no run measured it", which is pinned;
   - `test_the_one_counterfeit_the_gate_cannot_see_is_named` pins a shape · NAME NOT IN TREE
     that is no longer a counterfeit. It becomes the case that the shape
     reads `NO_RUNNER` (S8), and its sentence pins go with the rule-3
     rewrite.
9. **Read and not edited, with the grounds** (the first build's own first
   frame missed both README editions, so every place is listed):
   `README.md` (the sealer row, "`new?` with the reason, where no run at the
   base measured the file"; the flow line "new? → not measured at the
   base"), `README.ko.md` (the same two, in Korean), `agents/sealer.md`
   §*Boundaries* and its report list, `agents/smith.md` (the paragraph
   beginning "When the sealer reports a failure"). Each says `new?` means
   no run at the base measured the file. Under the anchor a run measures a
   file only where it collected nothing else, so each stays true. The words
   and what a person does with each are unchanged.
10. **The records.** The ledger fragment
    `seal/ledger/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure.md`
    holds the new rows. It also holds `Corrected ·` rows for every released
    row whose claim this makes false. Read by this frame and false under
    Scope 1–8: `seal/releases/0.18.2.md` rows D1 (`collected_nothing`), D2
    (rule 3's costs and limits), `Corrected · B3` (the walk stops at
    pytest's summary line) and `Corrected · S5` (what decides is pytest's
    summary); and `seal/releases/0.18.1.md` row B4 ("the two reasons are
    pinned whole", read again in 0.18.2 as `Re-read · B4`). 0.18.1's own B3
    was already corrected by 0.18.2's `Corrected · B3`, so the correction
    goes to that row. `evidence-check` finds any others, and re-reads go
    through `--reverify --into`. The changelog fragment
    is `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/changelog.md`.
    Any later fix pass that changes behaviour updates it too (#797).

### Out, and why

| Left out | Why | Who answers |
|---|---|---|
| Any placement of a report's test on a handed file (dotted names, offsets, `file`, the tree) | The anchor. The first build's every reopening came from it | decided by the owner, 2026-10-05 |
| Recovering cd rows whose rootdir is not the run directory, with `--rootdir=.` in the pass | Measured design reading, not run: with no ini file pytest sets `confcutdir` to the rootdir, so moving the rootdir can unload a `conftest.py` above the run directory. The proof would then describe a different collection from the run it proves. `plan.md` Alternatives, G | decided here; the repository owner if such a row is met (a new issue) |
| A gate-provided pytest plugin recording absolute paths per process | Exact, but it puts the gate's code in the row's interpreter through `PYTHONPATH`, which a row may set itself. The first build's framer rejected it as too much mechanism (its `plan.md` Alternative D), and the pass reaches the same guarantee for the rows the anchor admits. `plan.md` Alternatives, F | decided here; the direction to take if Scope 7's limits are met in practice |
| Telling a two-runner row's `new` apart from the right one when the base passes | Costs one whole-row collection pass per comparison, failing base or not. The anchor is about the permissive word | `questions.md` Q1, a person |
| The branch's own list of failing files (Axis C): an inner run's `FAILED` line adds a file | The branch's run is the row as written. The added file is then measured alone like any other, and the gate fails either way (round 3 of #761, confirmed by the first build) | decided by #761's round 3 |
| A failing file whose path holds a space (#813), a test outside pytest's rootdir handed by a name the base lacks (N5) | Strict at every SHA, and filed separately | #813; the orchestrator for N5 |
| `( … )` and `{ …; }` groups and compound commands in `row_prefixes` | Unchanged from #747 | as those items left them |

## User scenarios & acceptance *(mandatory)*

Every gate case lives in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
and is built with its `base_then_feature`, `verdict_of` and
`run_gate(repo, keep=…)`. `SUITE_ROW` collects `tests`. A new FILES_ROW
is the same row without `tests`, so it collects only what it is handed;
`suite_row(xdist)` gains its files-only twin. "Seen red" means the case
was run against a3aa139a's `broad_gate.py` and failed there (§15).

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The anchor, earned | FILES_ROW, plain and xdist. The base fails `tests/test_two.py`, and so does the branch. Then it reads exactly `failing on base too`, and `collected-at-base-1.txt` is kept with one trailer and the one listing line | executed; seen red on the kept-file assertion (a3aa139a gives the word without a proof pass) |
| S2 | The anchor, refused | `SUITE_ROW`, the same base. Then `new?` with the beyond reason | executed; seen red (a3aa139a: `failing on base too`) |
| S3 | #789 member 2 | `FILES_ROW -s`, plain and xdist. The base's failing `tests/test_err.py` runs a pytest subprocess on fd 2 that fails `tests/test_g.py`; the base passes `tests/test_g.py`; the branch fails both. Then `tests/test_err.py` reads `failing on base too` and `tests/test_g.py` `new` | executed; seen red (a3aa139a: `new` and `failing on base too`) |
| S4 | An inner run on stdout beside a passing base | As S3 with the base passing everything and the inner run on fd 1, under `-s` and `--capture=sys`. Then both read `new` | executed; seen red |
| S5 | #789 member 3, no rule of pytest's own | S3's base under `-rN` and `-rP` without `-s`; and S4's passing base under `-rP` | executed; seen red |
| S6 | #789 member 3, no summary line | FILES_ROW with `-qq`: a passing base reads `new` (a3aa139a: `NO_RUNNER`); S1's failing base reads `failing on base too`, which shows the proof's `-vv` | executed; seen red on the first param |
| S7 | #789 member 1 and #807: a second runner | The base fails `tests/test_y.py` at the root. Rows: `FILES_ROW && cd sub && FILES_ROW` (p1b), `FILES_ROW && sh -c 'cd sub && FILES_ROW'` (P7), `sh -c '{SUITE_ROW}' && FILES_ROW` (P3, a dropper first), and a first runner given `-p no:junitxml` and one given its own `--junitxml` (Q8). Then the file reads MULTI_RUNNER in each | executed; seen red where a3aa139a gave `failing on base too` (p1b, P7) and on the reason elsewhere |
| S8 | A part that drops the gate's arguments | `sh -c '{FILES_ROW}'` (POSIX only, skipped with its reason on Windows), and `FILES_ROW -p no:junitxml` alone, with a passing base. Then `NO_RUNNER`, never `new` | executed; replaces `test_the_one_counterfeit_the_gate_cannot_see_is_named`; seen red (`new`) · NAME NOT IN TREE |
| S9 | Parts that are not pytest | `python -c pass && FILES_ROW` (lint-first) and `FILES_ROW && python -c "<append a marker>"` (runner-first), with a failing base. Then `failing on base too` in both, and the marker shows the part after the runner ran once in the proof pass | executed; seen red on the marker |
| S10 | A cd row | `cd sub && FILES_ROW` with an ini in `sub` reads `failing on base too`; with the ini at the root it reads the beyond reason (M8) | executed; seen red on the second param |
| S11 | A file that fails to import at the base | FILES_ROW: `failing on base too`, proven through its `ERROR` line; `SUITE_ROW` with another failing module: the beyond reason | executed; seen red on the second |
| S12 | A file the base has no test in | Missing at the base, and present with no test, plain and xdist. Then `new` from the report's `tests=0` with exit 4 or 5 | executed; the 0.18.2 cases keep their words |
| S13 | The group | Two failing files the base carries, both passing at the base: `new` from one run, and no solo file kept. One passing and one failing: each runs alone, and the words are `new` and `failing on base too` | executed |
| S14 | The two readers | Unit tables. Report reader: a failure, an error, a skip, a collection error, `tests=0`, a bare `testsuite`, an unparseable file. Proof reader: one session listing `h`, two sessions, no trailer (`-qqq` without `-vv`), deselection, an error naming `h`, an error naming another path, a listing naming another path, a count that does not add up, colour codes, and pytest 8.0's tree. Each row gives its outcome | executed; mutations each turn a row red: drop the trailer count, drop the sum check, drop the error check |
| S15 | The texts | Rule 3, the **New?** bullet and the four reasons are pinned whole or by their deciding sentence | executed; each pin seen red with its sentence deleted |
| S16 | The 0.18.2 and earlier cases | Every case asserting `failing on base too` is listed in `phases/phase-1.md` with its row. Each one under `SUITE_ROW` either moves to FILES_ROW, keeping the word, or asserts the beyond reason, and the record says which. Every other word assertion is unchanged | executed |
| S17 | The regression corpus | Every layout of the first build's record, run at a3aa139a and at this work's head: P1–P7, Q1–Q12, Qf, Qs, Qs2, R1–R6, P7-both, P7-mixed, P7-p1b, N1–N8, and the 96-run inner-run matrix. Then none reads `failing on base too` unless a3aa139a gave it there too, or the layout's own record says the base fails that file under the runner the branch reported it from (S3–S5's shapes). Each such layout is named | executed — phase 2 (`plan.md`) |
| S18 | This repository's own row | M13's three runs, repeated through the gate with a file failing at the base | executed — a phase-1 probe, not a planted case (the suite does not run `uvx`) |

## Data & interfaces

- `compare_at_base(root, base, command, files, keep)`: the signature and
  the `{file: word}` return are unchanged, and it keeps one `run(...)` call.
- New pure functions beside it: the report reader (report text → tests and
  failing, or none) and the proof reader (pass text and `h` → proven, or
  the reason). Both are unit-tested on their own.
- Reasons, each opening `NOT_MEASURED`: `NO_RUNNER` (reworded), the
  not-ended reason (replacing `STOPPED_EARLY`), the beyond reason and
  MULTI_RUNNER. The smith names the two new constants.
- Kept files: `suite-at-base-<k>[-<n>].txt` and `.xml` as above, where
  *n* numbers every file run alone, candidate or group fallback; and
  `collected-at-base-<n>.txt` for the proof pass of the *n*-th.
- The proof pass's environment is the gate's own, with
  ` --collect-only -o verbosity_test_cases=-2 -vv` appended to
  `PYTEST_ADDOPTS`, passed through `run`'s existing `env`.

## Open questions → questions.md

`questions.md` beside this file. One row is a person's and does not block:
its default is what this frame builds. The others are a measurement's or
the work's.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-05 by framer, before the build.
