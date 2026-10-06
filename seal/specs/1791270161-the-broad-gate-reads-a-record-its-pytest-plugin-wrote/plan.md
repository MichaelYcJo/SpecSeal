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
  `report.location` or stops forwarding collect reports to the xdist
  controller. The recorder then records fewer lines, never more: a file
  with no line is `new` on an exit-0 base and `new?` otherwise, and the
  recorder's own unit cases (S1–S5) go red first. The one way to a wrong
  `failing on base too` is a forged or appended record (`spec.md` §*The
  class*), which needs a test written against this gate's key.

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
| M. Record with `item.path` in `pytest_collection_modifyitems` | Not available on the xdist controller; `report.location` is on every report (R4) | rejected |

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
- **Time.** A green suite costs one small JSON Lines file under the kept
  output. A failing suite costs one more run of the whole row at the base —
  for this repository, the two `ruff` checks and one full `bin/test -q`
  under `-n auto` — in place of 0.18.3's per-file prefix runs and proof
  runs. The cost no longer grows with the number of failing files.
