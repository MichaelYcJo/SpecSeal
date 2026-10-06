# Implementation Plan: the broad gate reads a record its pytest plugin wrote (#825)

<!-- seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

<!-- Fill the line above in at the spawn: reading this plan and spawning the
builder IS the approval. The shape is `templates/sdd-routing.md`'s. -->

## Summary

The base comparison stops reading the row's text and pytest's printed lines.
A pytest plugin of the gate's own — the recorder,
`skills/verify/scripts/pytest_record/specseal_pytest_record.py` — is loaded
into every run the gate measures through `PYTHONPATH` and a `-p` in
`PYTEST_ADDOPTS`, keyed by a token fresh per run, and writes one JSON Lines
file per pytest process that claims the key: the session's rootdir and
invocation directory, every test's absolute path and outcome, every failed
collection. The `HEAD` run already happens and now records; on a failing
suite the gate runs the row **once, unchanged** at the base with a second
key and gives each failing file its word from a five-row table over the two
records (`spec.md` Scope 5). Prefix cutting, the JUnit report, the
collect-only proof, the solo runs and the `COMPANY` rule retire with their
cases and their reasons; rule 3 shrinks to what a row's author needs to
know. `spec.md` holds the class, the readings R1–R13 and the scope.

**Reframed 2026-10-06, after round 3.** Phases 1–4 are closed at the
commits their rows name and stay closed. The review run then read a fix of
a fix twice: round 1 found the recorder naming a file outside the rootdir
under another file's name, round 2 found the refusal missing `--pyargs` and
a symlinked rootdir, round 3 found the refusal importing the row's package
too early and the guard missing a collector built below the root — every
finding inside the unit the previous fixes had changed. The frame that did
not hold is one sentence of Scope 1: a line's path is "the rootdir joined
to `report.fspath`". That is pytest's node id read backwards, and the node
id is made FROM the path by a rule with more branches than three rounds of
refusals could enumerate (`spec.md` R16). The redesign reads the path
pytest holds for the node, where the node exists, and carries it on the
report to the process that writes (`spec.md` R14, R15; Alternative N). The
refusal, the guard, the rootdir join and every sentence about them retire;
the layouts those rounds refused are recorded under their own names and get
measured words. Phases 5–7 below are the redesign; the Alternatives table
gains N–T for what it chose and refused.

**This cannot be built in about 45 minutes of wall time, and the plan says
so rather than pretending.** Phase 1 alone is a new module with six
subprocess-driven cases. Phase 2 rewrites `compare_at_base` and re-reads
about sixty end-to-end cases in an 8,353-line module, each of which asserts
a word or a kept file name this work changes. The honest estimate is two to
four hours of smith wall time over four phases, each of which commits on its
own and leaves the tree green, so a run that stops after phase 1 or 2 hands
back something a later session can continue from. If 45 minutes is a hard
bound, phase 1 is what fits in it.

## Technical context

Every coordinate is `read` at a9d7b0e5 unless marked; `spec.md` §*Read by
this frame* holds the pytest and xdist readings R1–R8.

- `skills/verify/scripts/broad_gate.py#gate` (line 3473): `checks[SUITE] =
  run(SUITE, command, root, keep, shell=True)` with no `env`; the chain arm
  below it already takes `env=draft_env(keep)`. The suite run gains
  `env=recording_env(keep, head_key)` the same way. At line 3521 the
  failure loop does `files = failing_files(check.text)` and calls
  `compare_at_base` where `files` is non-empty; this is where the head
  record is read instead, with `failing_files` as the no-record fallback.
- `#run` (line 1424) passes `env` straight to `subprocess.run`, hands a
  shell string through `handed_to_shell` and keeps `<name>.txt`. Unchanged.
- `#compare_at_base` (lines 2178–2396) is replaced from its docstring down.
  What stays: `tempfile.mkdtemp`, `git worktree add --detach`, the
  `finally` that removes the worktree, `kept = os.path.abspath(keep)`, and
  one `run(...)` call inside the function body
  (`tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  counts the calls). What goes is `spec.md` Scope 7.
- `#quote` (line 1809) is read by `#signal` (line 3770) and stays.
  `#failing_files` and `FAILED_RE` (lines 322, 1804) stay as the fallback.
- `HERE` (line 216) is the scripts directory, so the recorder's directory is
  `os.path.join(HERE, "pytest_record")` and survives the tree-copy redirect
  of `#gate_copy`: a tree that ships its own gate ships its own recorder
  beside it.
- **The recorder's floors, by reading pytest's changelog-known names**
  (`read`, not run; Q-M1 measures them): `config.rootpath` 6.1,
  `config.invocation_params` 5.1, `report.location` and `report.fspath`
  older, `pytest_collectreport` older. The module is written for Python
  3.8 syntax because it runs in the row's interpreter, whose version the
  gate does not know.
- **The test module** `tests/test_the_seal_is_taken_once_by_the_sealer.py`:
  `run_gate` (line 881) spawns the gate with `env_without_a_pull_request()`
  plus extras; `base_then_feature` (3990), `verdict_of` (3962, normalises
  `\` to `/`), `collected_at_base` (4020, retires), `REPORTS`/`PROOFS` (NAME NOT IN TREE)
  tables (4041, 4163, retire), the end-to-end cases from 3687 to 5700, the
  corpus `REGRESSED` (5806), `REGRESSED_WORDS` (6056), `word_for` (6143),
  the rule-3 pin (6203). The planted-case helpers are reused as they are.
- `tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT` (lines
  165–184): the `9.1.1` and `3.8.0` exemptions for `broad_gate.py` name
  comments that retire. Whether the test checks liveness of each exemption
  is the smith's to read in that module before moving them.
- **This repository's own suite spawns the gate from inside pytest.** Under
  the sealer the outer gate's `PYTEST_ADDOPTS` already carries `-p
  specseal_pytest_record` and the outer key was taken by the outer pytest,
  so a case's inner gate adds its own key and a repeated `-p` is skipped by
  `import_plugin` (R2). `tests/conftest.py` pops no `PYTEST_*` variable (NAME NOT IN TREE)
  (read, line 473 pops named `GH_*`/`GIT_*` only). S22 is the measurement.
- **The failure scenario of this design, six months on.** pytest renames
  `report.fspath` or stops forwarding collect reports to the xdist
  controller. The recorder then records fewer lines, never more: a file
  with no line is `new` on an exit-0 base and `new?` otherwise, and the
  recorder's own unit cases (S1–S5) go red first. The one way left to a
  wrong `failing on base too` is a forged or appended record (`spec.md`
  §*The class*), which needs a test written against this gate's key. A
  second, a pytest naming files outside its rootdir, was found in round 1
  and is refused: such a session writes no record (*inferred during implementation*).
  **Reframed after round 3:** the second way is closed by construction
  rather than refused — the path is the node's own — and the scenario
  moves. pytest or xdist stops carrying an attribute a hook set on a report
  (R14 reads `__dict__` copied whole, and nothing in pytest's changelog (NAME NOT IN TREE)
  reads otherwise), or a plugin rebuilds reports without it: every such
  line goes unplaced, the record holds fewer files, never a wrong one, the
  `end` line counts what was left out, the gate prints the count, and S23
  goes red first under `-n 2`. A file-less item (R16) is the one node the
  recorder leaves out on purpose, and S27 pins that it says so.

- **The reframe's coordinates, at 0c5b9b2c.** `specseal_pytest_record.py`:
  `Recorder.write` (line 110) holds the guard that retires, its `empty`
  and `isfile` tests included; `Recorder.absolute` (107) is the rootdir
  join that retires; `an_argument_lies_outside_the_rootdir` (157–209) is
  the refusal that retires with its `find_spec`; `pytest_sessionstart`
  (211) stops calling it; `pytest_runtest_logreport` (236) and
  `pytest_collectreport` (248) read the attribute instead of `absolute`;
  the module docstring's two rootdir paragraphs (40–52) go. The two new
  hookwrappers are module-level, beside `pytest_configure` (270), because
  they must run in a worker that registers no `Recorder`. `broad_gate.py`:
  `NO_RECORD_AT_HEAD` (2015) and `NO_RECORD` (2021) reworded; the
  `compare_at_base` docstring paragraph at 2079–2089; `RunRecord` (1869)
  gains an `unplaced` count summed from `end` lines by `read_record`
  (1908), and `failure_lines` (2927) prints the sentence where it is
  non-zero. `templates/config.md` rule 3 (334): the rootdir sentence and
  the "refusals above close every branch" limit. `tests/`: the eight
  refusal cases of the recorder module (319–560) flip to assert the line,
  the two gate cases at 4502 and 4532 flip to assert the measured word, the
  corpus row `("Q3b", "own")` at 6212 is re-derived, the pins at 4231 and
  6325 move. (NAME NOT IN TREE)
- **The floor, by reading.** `item.path` and `collector.path` since pytest
  7.0, `fspath` (a `py.path.local`, `str()` gives the path) before; both
  read through `getattr`. `TestReport.__init__`'s `**extra` and
  `_report_to_json`'s `__dict__` copy predate pytest 6 (the latter's (NAME NOT IN TREE)
  docstring says it came from xdist). Q-M3 measures 7.4, 8.0, 8.1 and 9.1
  with xdist 3.8 on the last, as Q-M1 and Q-M2 did. (NAME NOT IN TREE)

## Alternatives considered

The direction — alternative F of the 0.18.3 frame — is the owner's and is
not re-argued here. These are the choices inside it.

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. `-p specseal_pytest_record` appended to `PYTEST_ADDOPTS`, the module reached through `PYTHONPATH`** | A row that sets `PYTEST_ADDOPTS` or `PYTHONPATH` itself drops the recorder: no record, `new?` (strict, named in rule 3) | **chosen**; the owner's wording, and R1 reads `-p` as honoured from the variable |
| B. `PYTEST_PLUGINS=specseal_pytest_record` instead of `-p` | The same `PYTHONPATH` dependence; trades a row that sets `PYTEST_ADDOPTS` for one that sets `PYTEST_PLUGINS` | not taken; nothing in the records names a row of either kind, so the owner's spelling wins (NAME NOT IN TREE) |
| **C. The claiming process takes the key out of its environment at import; the first session configured in a process claims it** | A test that reads the environment for the key cannot forge a record; a child pytest and an xdist worker inherit no key and record nothing. Costs: a row whose runner `exec`s a second pytest after reading the environment into a copy (constructed only) | **chosen** |
| D. Every process records, keyed; the gate unions them | An inner pytest a test spawns writes a record with the gate's key, which is #789's inner-run class with a new spelling | rejected |
| E. Record on xdist workers too | A second session about the same tests, which the reader would have to merge or refuse | rejected; R5 reads the controller as receiving every report |
| **F. The file as the unit of the word; identity is the realpath made relative to the run's worktree, posix** | Two worktrees never share a prefix, and macOS spells a temp root two ways; `realpath` on both sides closes the second | **chosen**; the words the sealer and smith read stay per file |
| G. The test as the unit (`nodeid`) | A node id moves with a rename or a parametrize change between base and branch; the words a person reads are per file | rejected |
| **H. A file in no base session reads `new` on exit 0 and `new?` otherwise** | A red base with a pre-existing failure elsewhere gives a branch-added file `new?` instead of `new`: noisier, strict. Alternatives were the session's `end` line (misses a later runner the shell never started) and `shouldstop` (misses a part that failed before the runner) | **chosen**; `questions.md` Q1 asks whether the owner wants the noise |
| I. Append the failing files to the base run, or `--lf`, to shorten it | Appending is what made rows collect beyond their files and droppers lose arguments; `-x` makes the not-reached row fire on purpose | rejected |
| J. Keep the `FAILED` fallback beside a head record, for runners that did not load the recorder | Matching a cwd-relative `FAILED` path to a recorded absolute path is the inference this work removes; a mismatch would print a second row for one file | rejected; the fallback runs only where no head record exists |
| K. Run the base where `HEAD` left no record | A base record could be matched to `FAILED` names only by inference | rejected |
| L. Fix #813 and #818 on their own | Both disappear on the measured path with the regexes; the fallback's `FAILED_RE` is widened one character so a spaced path is at least named | the frame's call, as #825 asked |
| M. Record with `item.path` in `pytest_collection_modifyitems` | Not available on the xdist controller; `report.fspath` is on every report (R4, corrected *inferred during implementation* in phase 4 from `report.location`, which names the defining module) | rejected — and the reframe's N is M with the one thing M lacked: a way for the path to reach the controller |

The rows below are the reframe's, after round 3. The direction is still
the owner's; these are the choices inside it that the run's three rounds
showed had to be made again.

| Approach | Failure scenario | Verdict |
|---|---|---|
| **N. The path travels with the report.** Two module-level hookwrappers, on `pytest_runtest_makereport` and `pytest_make_collect_report`, run in every process that loaded the recorder and set the node's own path on the report as a string attribute; the recording process reads that attribute and derives nothing from a node id (`spec.md` R14–R16) | A plugin that builds or rebuilds a report without the attribute, or a pytest that stops copying `__dict__` into a serialized report: the line goes unplaced, counted on the `end` line and printed by the gate — fewer lines, never a wrong one. A worker that did not load the recorder would do the same, and R15 reads that none exists | **chosen**; M's reading was right about the controller and wrong that nothing could carry the path to it (NAME NOT IN TREE) |
| O. Keep the derivation and close round 3's two 🔴 with its paste-ready fixes: a locator that imports nothing, a guard that reads `::` on a `collect` line | Rounds 1, 2 and 3 each closed the branch found and left the next; a fourth and fifth re-derivation of pytest's naming rule have no reason to be the last, and `_pytest/nodes.py` has branches the table did not split (R16). This is the fix of a fix the stop exists to end | rejected; `spec.md` §*Out* names it |
| P. `user_properties` as the carrier instead of an attribute of the recorder's own | Documented and serialized, but `--junitxml` writes every property into the XML a row keeps, so the gate would change a file a person reads; and `CollectReport` has no `user_properties` at all | rejected (NAME NOT IN TREE) |
| Q. `trylast=True` on the recorder's `pytest_sessionstart`, round 3's first try | Closes the one shape round 3 planted and leaves the import ahead of a conftest's own `trylast` hook and of collection wrappers; the import is the defect, not its moment | rejected |
| R. Record on xdist workers after all (E again, now that workers must run a hook) | The attaching hook is not a record: it writes nothing and claims no key. A worker's record would still be a second session about the same tests (E) | rejected; the hooks run there and the controller alone records |
| S. A fallback to `rootdir / fspath` where a report carries no path | The derivation back in, for the reports a plugin rebuilt — which are the reports least likely to be named right by it | rejected; the line is dropped, counted and said |
| T. A word for a test with no file of its own, under its parent's directory | The unit of the word is the file (F); two such items under one directory, one failing at the base and another on the branch, would read `failing on base too` the way two files at one path did | rejected; in no list, counted and said (S27) |
| U. Drop a `test` line whose path is no FILE rather than one whose path is a directory | A module that removes its own file while it runs would have its `setup` line written and its `call` line dropped, so the base's record would hold the file collected and passing: a permissive word for a failure | rejected; the test is `isdir`, so a file that was deleted is still named and a session-parented item is not (NAME NOT IN TREE) |

## Phases

Vertical slices — each phase ends with something runnable and verified, and
each commits on its own. §14 binds phase 2: rule 3, the **New?** bullet and
the docstrings change in the same commit as the words.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The recorder (`spec.md` Scope 1) in its own directory, and `tests/test_the_recorder_writes_what_its_process_ran.py` driving pytest as a subprocess over a scratch project: S1–S5. Q-M1 and Q-M2 answered first, in a probe, and the answers written into the recorder's comment and `phases/phase-1.md`. The structural corpora read: `shipped_python`, `LOADED`, the encoding walk | S1–S5, each seen red as its row says; `bin/test -q tests/test_the_recorder_writes_what_its_process_ran.py tests/test_a_script_says_which_interpreter_it_needs.py tests/test_release_hygiene.py tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` | 27365f10 |
| 2 | The gate (Scope 2–9): `recording_env`, `read_record` and its unit table, the head run recording, the fallback, `compare_at_base` rewritten to one run and the table, the three reasons, the retirements of Scope 7, the posix listing; rule 3 rewritten whole, the **New?** bullet, both docstrings, the pins moved and the retired sentences asserted gone; the release-hygiene exemptions moved; every end-to-end case re-read with its word before and after listed in `phases/phase-2.md` (Scope 8); the S21 probe over this repository's own row | S6–S19 and S21, each seen red as its row says; the narrow modules `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, `tests/test_release_hygiene.py` | 1bc4fb42 |
| 3 | The records (Scope 11): the ledger fragment with its new rows and the `Corrected ·` rows, re-reads through `evidence-check --reverify --into`; the changelog fragment `changelog.md` naming #825, #807, #813, #816, #818 | `evidence-check` clean over the fragment; the fragment names every released row `spec.md` Scope 11 lists | f54635bf |
| 4 | The regression corpus (S20): `REGRESSED_WORDS` re-derived from each layout's `at_base` dictionary, `word_for` reduced to `new`, `on`, `no-record`, `not-reached`, and the case's docstring rewritten to say the word is the base's own | S20; the corpus green; the table of words in `phases/phase-4.md` | 56b4c705 |
| 5 | **The redesign of the recorder** (`spec.md` Scope 1 as reframed, Alternative N). Q-M3 measured first, in a probe, the answer written into the recorder's docstring and `phases/phase-5.md`. Then the two module-level hookwrappers; `write` keeps a `test` line only where it carries a path that is not a directory and a `collect` line only where it carries a path, counts the rest, and the `end` line carries `unplaced`; `absolute`, the guard and `an_argument_lies_outside_the_rootdir` retire with the docstring's rootdir paragraphs. In the same commit (§14): rule 3's rootdir paragraph and its "no third way is known" limit replaced by the two sentences of Scope 9, `compare_at_base`'s docstring paragraph, the changelog fragment's bullet, the pins moved and the retired sentences asserted gone; the eight refusal cases of the recorder module flipped to assert the file under its own path and the two gate cases to assert the measured word (S24), S23, S25, S26 planted, the corpus row `("Q3b", "own")` re-derived from its `at_base`. The release-hygiene corpora re-read for the changed shipped `.py` | S23–S26 each seen red as its row says, at 0c5b9b2c's recorder; `bin/test -q` over `tests/test_the_recorder_writes_what_its_process_ran.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, `tests/test_a_script_says_which_interpreter_it_needs.py`, `tests/test_release_hygiene.py`, `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`; one mutant per new branch through `bin/mutation-check` (NAME NOT IN TREE) | |
| 6 | **The gate says what the record left out** (Scope 6 as reframed; round 3's 🟡 3 and ⬜ 4). `NO_RECORD_AT_HEAD` and `NO_RECORD` name both causes of a missing record; `RunRecord` gains `unplaced`, summed by `read_record` from the `end` lines, and the failure form prints the one sentence where the head record's count is non-zero; the **New?** bullet of `skills/verify/SKILL.md` follows the reasons; pins moved (S27, S28) | S27 and S28 seen red as their rows say; the gate module and `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`; a mutant of the count through `bin/mutation-check` | |
| 7 | **The records.** The ledger fragment's W1, W6 and `Corrected · R4` rows, and any other naming the refusal, rewritten in place — the fragment is this item's own and unreleased, so no `Corrected ·` row is owed — and every coordinate the redesign moved re-read through `evidence-check --reverify --ledger … --checked`; `overview.md`'s divergence table, *Not verified* and fed-back clauses brought to the reframe; `phases/phase-5.md`, `phase-6.md` and `phase-7.md` from `templates/sdd-phase.md`; every `(NAME NOT IN TREE)` marker the reframe wrote in `spec.md`, `plan.md` and `questions.md` removed where the name now exists | `bin/evidence-check --strict .` exit 0 with the records sweep refusing nothing; `bin/correction-check` exit 0; the fragment names no retired unit | |

**The redesign's approval is a second `Approved` line under the first, in
the template's shape, written when `smith` is spawned for phase 5**
(`skills/code-review/orchestration.md` §*A fix of a fix twice sends the
work item back to its framer*). The round record that follows starts the
fix-of-a-fix count at `no`, and `round_record.py new` reads the `Reframed`
line at `spec.md`'s foot before it writes it.

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. What a phase discovers while
it is being built, and needs the next phase to know, goes to
`seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes. **Re-read the Status
column after any rebase**: the commits it names resolve in the worktree that
wrote them and may resolve nowhere else.

## Operational impact

No migration, no new dependency, and no new environment variable a person
sets. The gate sets four for the runs it measures (`PYTHONPATH`,
`PYTEST_ADDOPTS`, `SPECSEAL_RECORD_DIR`, `SPECSEAL_RECORD_KEY`), in the
environment of those runs only.

`CONTRIBUTING.md` §*What a change to a gate must carry*:

- **A test seen red.** Every new case of `spec.md` S1–S19 is run against
  a9d7b0e5's `broad_gate.py`, or against the recorder with the hook body it
  pins deleted, and fails there; the phase records say how each was seen.
- **The failure direction: the gate measures more and infers nothing.**
  `failing on base too` is given from a record written inside the pytest
  process that collected the test, where 0.18.3 gave it from a text proof
  and refused rows the proof could not read. So some rows move from `new?`
  to a measured word (two runners, `sh -c`, `-p no:junitxml`, a silent
  measuring runner, a group), each from the base's own outcome. Every
  failure of the mechanism is strict: no recorder loaded is `new?`, a base
  run that ended before reaching a file is `new?`, and a file in no base
  session on a red base is `new?` where 0.18.3 gave `new`. The one new
  permissive path is a forged record, named in `spec.md` §*The class*.
- **The prompt budget: zero.** Nothing here asks a person anything; `new?`
  is a word in a report.
- **Platform honesty.** This frame executed nothing. Phase 1 measures on
  macOS against pytest 9.1.1 and pytest-xdist 3.8.0 and, through `uvx`,
  against 7.4, 8.0 and 8.1 (Q-M1, Q-M2). Linux and Windows (`PYTHONPATH`
  with `;`, `cmd.exe` handed the row unchanged, the posix listing of S18)
  are CI's three-platform test job to answer; S18 is seen red there.
- **The reframe, against the same four points.** It executed nothing
  either; Q-M3 is phase 5's first act on the same builds. The failure
  direction moves in the permissive direction for exactly the layouts
  rounds 1–3 refused, and each such move is a file recorded under its own
  path with its case asserting the line (S24, S26) — the same bar phase 2
  held every permissive move to. What the recorder leaves out is strict
  and said (S27). The prompt budget stays zero. The time cost does not
  move: two hookwrappers that set one string each, per report.
- **Time.** A green suite costs one small JSON Lines file under the kept
  output. A failing suite costs one more run of the whole row at the base —
  for this repository, the two `ruff` checks and one full `bin/test -q`
  under `-n auto` — in place of 0.18.3's per-file prefix runs and proof
  runs. The cost no longer grows with the number of failing files.
