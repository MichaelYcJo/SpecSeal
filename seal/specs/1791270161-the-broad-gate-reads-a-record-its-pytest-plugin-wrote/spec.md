# Feature Specification: the broad gate reads a record its pytest plugin wrote (#825)

<!-- seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#825 and its comments, #807, #813, #815, #816 and #818, read 2026-10-06 at
a9d7b0e5 (the tip of `release/v0.20.0`). This is the fifth design of the
base comparison and the owner chose its direction in the issue: alternative
F of the 0.18.3 frame (`git show
v0.18.3:seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/plan.md`,
Alternatives), "the direction to take if E's limits are met in practice".
#815 and #816 are those limits met.

**The defect, in one sentence.** To give `failing on base too`, the gate has
to know which pytest process, in which directory, produced each outcome it
reads, and four designs in a row (#758, #787, the unmerged #804, #814) each
inferred that from the row's text and from what pytest printed, moving the
guess one level up each time. Rule 3 of `templates/config.md` grew from 71
to 1341 words over 0.18.x, most of it limits of the inference.

**The anchor, the owner's direction of 2026-10-06.** The gate stops
inferring. A small pytest plugin of the gate's own, loaded into every run it
measures and keyed by a value the gate makes fresh per run, records per
pytest session the rootdir, the invocation directory and every test's
absolute path and outcome. The gate runs the whole row once at `HEAD` (as it
already does) and once at the base, and compares the two records. **The
permissive word needs a record carrying that run's key.** A runner that left
none gives no evidence and its files read `new?`. Every failure of the
mechanism falls on the strict side.

Below, "the recorder" is that plugin: the word *plugin* already names this
Claude Code plugin throughout the repository, and a second meaning in the
same files is what `tests/test_one_word_one_meaning.py` exists to refuse.

## The frame in one paragraph

Before the `Broad gate` row runs, the gate prepends the recorder's directory
to `PYTHONPATH`, appends ` -p specseal_pytest_record` to `PYTEST_ADDOPTS`,
and sets `SPECSEAL_RECORD_DIR` to an absolute directory under the kept
output and `SPECSEAL_RECORD_KEY` to a fresh token. Every pytest the row
starts loads the recorder; the one that finds the key claims it and takes
it out of its own environment, so a pytest it spawns in turn (a test that
runs pytest, an xdist worker) loads the recorder and records nothing. The
recorder writes one JSON Lines file per claiming process: a session line,
one line per test report and per failed collection, each with the file's
absolute path, and an end line. On a failing suite the gate reads `HEAD`'s
record for the failing files, runs the row **once, unchanged** at the base
with a second key, reads the base's record and gives each file its word
from a five-row table. No file is appended to any run, no prefix is cut, no
printed line is read for a verdict, and no `--collect-only` proof exists.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #825, the owner's direction of 2026-10-06 | The anchor: a recorder keyed per run, the whole row once at the base, the permissive word only from a keyed record, every failure of the mechanism strict. This frame does not reopen the direction; `plan.md` Alternatives records what it chose inside it |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides between a word the gate measures and `new?`, which sends a person to the base by hand. The recorder measures rows the collect-only proof had to refuse (two runners, `sh -c`, `-p no:junitxml`, a measuring runner whose output goes to a file), so fewer rows stop a person |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A case seen red, a stated failure direction, a prompt budget and platform honesty. Answered in `plan.md` §*Operational impact* |
| `templates/config.md` §*Broad gate* §*Choosing a value — the criterion*, rule 3 | The one home of what the comparison costs a row and which rows it cannot measure. Rewritten whole by this work (Scope 9); the pin in `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written` moves with it |
| `docs/the-broad-gate.md` §*One act, one owner* — the sealer "judges nothing" and hands the words on | The words and what a person does with each are unchanged. `docs/the-broad-gate.md` carries no clause about the base comparison, and this work adds none: a `docs/` clause is `settle`'s to fold after the release (`skills/implement/SKILL.md` §*Document layout*) |
| `agents/sealer.md` §*Boundaries* ("`new` and `failing on base too` are the gate's words: it re-ran the failing files at the base to earn them"; `new?` "where no run at the base measured the file"); `agents/smith.md` ("the gate re-ran those files there"); `README.md` and `README.ko.md` §*The chain* flow | Read and not edited (Scope 10). The row at the base runs those files where it collects them, and `new?` still means no run at the base measured the file |
| `skills/agent-contract/SKILL.md` §12, §13, §14, §15 | The class is enumerated by construction below. Every changed reason, rule-3 sentence and **New?** bullet is pinned in the commit that changes it. Every new case is seen red at a9d7b0e5 |
| `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite` | `compare_at_base` keeps one `run(...)` call. It makes one run now, so the case holds by construction |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from`; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | Released rows this work makes false are corrected by `Corrected ·` rows in `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md`, never by editing `seal/releases/*.md` (Scope 11) |
| `tests/test_a_script_says_which_interpreter_it_needs.py#shipped_python`, `tests/test_release_hygiene.py#LOADED`, `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` | A new shipped `.py` under `skills/` enters three corpora: no `zip(..., strict=)` or `.UTC` without a classification, no version-shaped token without an exemption keyed on the file, and every `open` names `encoding="utf-8"` |

## Read by this frame, and what each reading settles

Nothing in this section was executed. Each row is `read`, at the path it
names, in the built environment at `/Users/x/…/.venv` (pytest 9.1.1,
pytest-xdist 3.8.0, execnet 2.1.2). Rows marked *measurement* are left to
the smith's phase 1 and are rows of `questions.md`.

| # | What was read | What it settles |
|---|---|---|
| R1 | `_pytest/config/__init__.py#_preparse`: `PYTEST_ADDOPTS` is split and prepended to the arguments, then `consider_preparse(args, exclude_only=False)` reads every `-p`, then `consider_env()` reads `PYTEST_PLUGINS`; `PYTEST_DISABLE_PLUGIN_AUTOLOAD` gates only setuptools entry points | A `-p <module>` carried in `PYTEST_ADDOPTS` loads the recorder before any conftest, and a row that disables autoload does not stop it. Confirmed on 9.1.1 by reading; 7.4, 8.0 and 8.1 are a *measurement* (Q-M1) (NAME NOT IN TREE) |
| R2 | `#import_plugin`: `importlib.import_module(importspec)`, and a module already registered under that name is skipped (`get_plugin(modname) is not None`) | The recorder is reached through `sys.path`, so `PYTHONPATH` is the carrier, and a `-p` repeated by an outer gate run (this repository's own suite spawning the gate) is harmless |
| R3 | `_pytest/pytester.py:707`: `mp.delenv("PYTEST_ADDOPTS", raising=False)` | A `pytester`-driven inner run never loads the recorder at all; the key rule below covers the subprocess kind |
| R4 | `_pytest/nodes.py#Item.location`: `(relfspath, lineno, name)` with `relfspath` relative to `config.rootpath` through `bestrelpath`; `_pytest/reports.py#BaseReport.fspath`: the nodeid up to `::` | A report carries its node id's path, `fspath`, relative to the rootdir for a file under it, on the controller as well as in a plain run, so `rootdir / fspath` is the absolute path of the module that collected the test, for a test report and a `CollectReport` alike. Neither needs `item.path`, so the recorder reads reports only. Corrected, *inferred during implementation*: `location[0]` comes from `reportinfo()` and names the module that DEFINES the test function, which gave a file the base passes `failing on base too` in the corpus (phase 4); and a file outside the rootdir is named against the argument that reached it, so a session handed such a path writes no record (round 1) |
| R5 | `xdist/remote.py` `__channelexec__`: a worker is a child process that inherits `os.environ` and prepends its import path to `PYTHONPATH`; `xdist` forwards every worker's test and collect reports to the controller's `pytest_runtest_logreport` and `pytest_collectreport` | The controller alone records a whole `-n auto` run; workers find no key (the controller took it) and record nothing. That the controller sees every collect report under `-n 2` is a *measurement* (Q-M2) (NAME NOT IN TREE) |
| R6 | `_pytest/main.py#Session.shouldstop`, `shouldfail` | Available to the recorder, and not needed: the base run's exit code decides the not-reached rule below |
| R7 | `.github/scripts/run_tests.py#main`: `subprocess.run(command, cwd=str(root))` with no `env` | `bin/test` hands the gate's environment through to pytest unchanged, so this repository's own row records |
| R8 | `skills/verify/scripts/broad_gate.py#run`: `subprocess.run(handed, cwd=root, shell=shell, env=env)`; `#gate`: `checks[SUITE] = run(SUITE, command, root, keep, shell=True)` with no `env`; `#draft_env` builds an environment for the chain arm from `os.environ` | The suite run gains an environment the same way the chain arm has one. One `run` keeps one shell site |
| R9 | `#compare_at_base` at a9d7b0e5: the candidate split, `row_prefixes`, the group, the lone-run table, the proof pass, `proof_refused`, `report_counts`, the five reasons, `COLLECT_ONLY`, `OWN_LISTING`, `JUNIT_REPORT`, the six regexes; `#quote` is also read at `#signal` (`command = quote(path)`) | What retires (Scope 7) and what stays: `quote` stays because `signal` reads it; `FAILED_RE` and `failing_files` stay as the fallback of Scope 4 |
| R10 | `tests/test_the_seal_is_taken_once_by_the_sealer.py`: 220 cases, of which about sixty from `test_a_failing_test_is_not_sealed_and_is_new_when_the_base_passes` (line 3687) to `test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives` (line 6156) drive `compare_at_base`; `verdict_of` normalises `\` to `/`; `REGRESSED_WORDS` spells words as `beyond:n`, `multi:n`, `company`, `new`, `on` | The size of phase 2 and phase 4. `verdict_of`'s normalisation can go once the listing is posix (Scope 5); `word_for` loses three kinds |
| R11 | `tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT`: `("skills/verify/scripts/broad_gate.py", "9.1.1")` and `("…", "3.8.0")` name the comments over `JUNIT_REPORT`, `COLLECT_ONLY` and `COLLECTED_RE` | Those comments retire with their constants, so the two exemptions move to the recorder's own comment where it names the builds it was measured on, or go where no token remains |
| R12 | `tests/test_one_word_one_meaning.py`: the guarded words are `seal`, `segment`, `pact`, `signatory` | *plugin* is not guarded; this spec still says *recorder* for the pytest plugin, because every document here already uses *plugin* for the Claude Code plugin |
| R13 | `templates/config.md` rule 3 at a9d7b0e5, 1341 words; `changelog/0.18.3.md` §*Fixed*, §*Changed*; `seal/releases/0.18.1.md` B2–B4, `0.18.2.md` D1, D2, `0.18.3.md` R1–R5 and its `Corrected ·` rows | What the records say today, and which released rows this makes false (Scope 11) |

## The class, enumerated by construction

**A file reads `failing on base too` only where a record carrying the base
run's key holds a failing test or a failed collection whose absolute path,
made relative to the base's worktree, is that file.** The record is written
by code the gate ships, inside the pytest process that collected the test,
from the path pytest itself attached to the report. There is no "whose" to
infer: the process that failed the test is the process that wrote the line.

Each way the word could still be wrong is a way to put a false line into a
keyed record, and each is named:

- **A record left by something other than the measured run.** The key is
  fresh per run and the record directory is under this run's kept output,
  so a stale record from an earlier run, a `--keep-output` directory
  reused, or a test that writes into the directory can only match by
  forging the key. A test that reads `SPECSEAL_RECORD_KEY` cannot: the
  claiming recorder took it out of the environment before the first test
  ran. A test that reads the file the recorder is writing could append to
  it; this is constructed only, needs a test written against this gate,
  and is named rather than closed.
- **A path pytest attached to the wrong file.** The report's path is where
  pytest collected the test (R4); a test a module inherits from a helper
  is reported under the module that collected it, not the helper that
  defines it. This is the opposite of `xunit1`'s `file`, which is why the
  0.18.3 frame's Alternative B lost, and it is what makes placement by
  name unnecessary here.
- **Two files at one relative path.** Two runners in two directories report
  different absolute paths, and relative to the worktree they stay
  different. They coincide only for one file, which is one file. Corrected,
  *inferred during implementation* (round 1): a pytest handed a path outside its rootdir
  names those files against the argument rather than the rootdir, so two
  files under two arguments can share one name; such a session writes no
  record, and its files read `new?`.

Everything else the mechanism can get wrong is strict: no recorder loaded
(`tox`, `nox`, `env -i`, a container, a row that sets `PYTHONPATH` or
`PYTEST_ADDOPTS` itself, a wrapper that builds its own environment, a
runner that is not pytest, pytest too old to load it) leaves no keyed
record, and the word is `new?`.

## Scope

### In

1. **The recorder**, `skills/verify/scripts/pytest_record/specseal_pytest_record.py`,
   a pytest plugin in a directory of its own so that `PYTHONPATH` exposes
   nothing else of this plugin's to the row's interpreter. It runs in the
   row's interpreter, which may be older than this plugin's floor, so it is
   written for Python 3.8 and pytest 6.1 by reading (`config.rootpath`,
   `config.invocation_params.dir`, `report.location`, `report.fspath`;
   `plan.md` §*Technical context* lists the oldest version each name
   appeared in), with no syntax newer than 3.8, no `zip(..., strict=)`, no
   `datetime.UTC`, and every `open` naming `encoding="utf-8"`.
   - **At import** it takes `SPECSEAL_RECORD_KEY` out of `os.environ`
     (`pop`) into a module variable and reads `SPECSEAL_RECORD_DIR`. Taking
     it out is what keeps a child pytest — one a test spawns, an xdist
     worker — from recording: it inherits an environment with no key.
   - **At `pytest_configure`** the first session configured in the process
     claims the key and the module variable is cleared, so a second session
     in the same process (an in-process `pytest.main` a test calls) finds
     none. With no key or no directory the recorder registers nothing and
     changes nothing.
   - **At `pytest_sessionstart`** it opens `<dir>/<key>-<pid>.jsonl` and
     writes a `session` line: the key, the pid, `rootdir` and `invocation_dir`
     as absolute strings, and `pytest`'s version.
   - **At `pytest_runtest_logreport`** it appends a `test` line per report:
     `nodeid`, `when`, `outcome`, `wasxfail` where set, and `path`, the
     absolute path `os.path.normpath(os.path.join(rootdir, report.fspath))`,
     the module that collected the test (`report.location[0]` before phase 4,
     corrected *inferred during implementation*); a session handed a path outside its
     rootdir writes no line at all (round 1).
     **At `pytest_collectreport`**, where the report failed, a `collect` line
     with `nodeid`, `outcome: "failed"` and `path` from `report.fspath` the
     same way. Each line is flushed as written, so a crash leaves what ran.
   - **At `pytest_sessionfinish`** it appends an `end` line with
     `exitstatus`. Nothing in the gate's table depends on it; it is for the
     person reading the kept file.
   - It never prints, never changes an outcome, never raises out of a hook:
     a directory it cannot write is one `warnings.warn` and no record,
     which the gate then reads as no record (strict).
2. **The environment every measured run is handed.** `recording_env(keep, key)`
   in `broad_gate.py`: `os.environ` copied, `PYTHONPATH` with the
   recorder's directory prepended (`os.pathsep`), `PYTEST_ADDOPTS` with
   ` -p specseal_pytest_record` appended to whatever it holds,
   `SPECSEAL_RECORD_DIR` the absolute path of `<keep>/records/`, and
   `SPECSEAL_RECORD_KEY` the key. The key is `secrets.token_hex(8)`
   prefixed `head-` or `base-`, made fresh each gate run. `gate` hands the
   `HEAD` run this environment; `compare_at_base` hands the base run one
   with its own key. `--preflight` runs no row and is unchanged.
3. **The reader**, one pure function of (the records directory, a key, the
   worktree the run ran in) → a `Record`: the set of sessions found, and per
   file — the test's absolute path, `os.path.realpath` applied, made
   relative to the worktree's `realpath` and spelled posix — whether any
   test or collection of it failed (`outcome == "failed"` in any phase, or
   a `collect` line), and whether it was collected at all. A path outside
   the worktree keeps its absolute spelling. Lines that do not parse are
   skipped and counted; a file whose `session` line carries another key is
   not this run's. `realpath` is not optional: on macOS a `mkdtemp`
   directory and pytest's `rootpath` spell the same place as `/var/…` and
   `/private/var/…`.
4. **The failing files at `HEAD` come from `HEAD`'s record**, not from
   `FAILED` lines: every file with a failing test or collection in any
   session carrying the head key, in first-seen order. Where **no** session
   carries the head key, `failing_files(check.text)` is the fallback list,
   with `FAILED_RE`'s path group widened to `(.+?)` so a path holding a
   space is named (#813), and every file of it reads `NO_RECORD_AT_HEAD`;
   the base is not run, because there is nothing to compare. A runner that
   loaded no recorder beside one that did contributes no file to the list;
   its `FAILED` lines stay in the kept `suite.txt`, and rule 3 says so.
5. **The base comparison is one run of the row as written.** `compare_at_base(root, base, command, files, keep)`
   keeps its signature and its `{file: word}` return. It adds the scratch
   worktree at the base as today, runs `command` there once through the one
   `run(...)` call with `recording_env(keep, base_key)`, kept as
   `suite-at-base.txt`, reads the base's record, removes the worktree, and
   gives each file one word from this table:

   | The base's record | This file in it | Word |
   |---|---|---|
   | no session carries the base key | — | `new?`, `NO_RECORD`: no pytest at the base loaded the gate's recorder, or none the row reached did (names `suite-at-base.txt` and `records/`) |
   | one or more sessions | a failing test or a failed collection of it | `failing on base too` |
   | one or more sessions | collected, nothing of it failed | `new` |
   | one or more sessions, and the row exited 0 | in no session | `new`: the row ran to its end at the base and never collected the file, so the base cannot fail a test it did not run |
   | one or more sessions, and the row exited non-zero | in no session | `new?`, `NOT_REACHED`: the row at the base ended with that exit before any session collected the file — a part that failed before a later runner, `-x` or `--maxfail`, an interrupt, a crash, a collection error above the file — so whether the base fails it was not measured (names the exit and `suite-at-base.txt`) |

   The listing prints each file as the reader spelled it, relative to the
   worktree and posix (#818), in the order of Scope 4.
6. **The words a person reads: three keep their text, two are new, five
   retire.** `NEW`, `ON_BASE` and `NOT_MEASURED` (`new? not measured`) are
   unchanged. `NO_RECORD_AT_HEAD`, `NO_RECORD` and `NOT_REACHED` each open
   `NOT_MEASURED`, say what happened, name the kept file and say how a row
   earns the measured word (let pytest load the recorder: no `PYTHONPATH`
   or `PYTEST_ADDOPTS` of the row's own, no environment the row rebuilds,
   pass the environment through any wrapper). `NO_RUNNER`, `NOT_ENDED`,
   `COLLECTED_BEYOND`, `MULTI_RUNNER` and `COMPANY` retire. Each surviving
   or new reason is pinned whole in
   `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`.
7. **What retires from `broad_gate.py`**, and the cases over it:
   `row_prefixes`, `POSIX_CUTS`, `CMD_CUTS` and the two row-cut (NAME NOT IN TREE)
   parametrized cases and the shell-selection case over them; `JUNIT_REPORT`,
   `NOTHING_COLLECTED_EXITS`, `COLLECT_ONLY`, `OWN_LISTING`, `COLLECTED_RE`,
   `LISTED_RE`, `NODE_RE`, `ERROR_LINE_RE`, `COLOUR_RE`, `RAN_RE`,
   `report_counts`, `written_report`, `proof_refused`, the `ElementTree`
   import, and the unit tables `REPORTS` and `PROOFS` with their two cases;
   the candidate split, the group, the lone-run table and the proof pass
   inside `compare_at_base`; the kept names `suite-at-base-<k>[-<n>].txt`,
   `.xml` and `collected-at-base-<n>.txt`, and `collected_at_base` in the (NAME NOT IN TREE)
   test module. `quote` stays (`signal` reads it) with its case.
8. **Every end-to-end case over the comparison is re-read, one by one, and
   `phases/phase-2.md` lists each with its word before and after.** By the
   table of Scope 5 many words move in the *permissive* direction, and each
   such move is a claim the record makes about that layout, so the phase
   record says, per case, which row of the table gave the word: the
   two-runner rows (`TWO_RUNNERS`), the droppers (`DROPS_ITS_ARGUMENTS`: a (NAME NOT IN TREE)
   `sh -c` inherits the environment and records; `-p no:junitxml` no longer
   matters), the groups (`test_a_group_decides_only_new`,
   `test_a_file_the_base_fails_only_alone_is_not_called_failing_on_base_too`,
   `test_a_count_another_file_makes_up_does_not_earn_the_word`), the silent
   measuring runner (`test_a_measuring_runner_whose_output_the_gate_never_sees_earns_no_word`,
   `test_a_silent_measuring_runner_beside_an_empty_session_earns_no_word`), (NAME NOT IN TREE)
   and `test_a_first_runner_without_the_gates_environment_costs_the_word`
   (an `env -i` runner leaves no record; where it is the only runner the
   word is `NO_RECORD`). A case whose planted layout the table now measures
   asserts the measured word **and** the record line that earned it (the
   `records/*.jsonl` file names the file). `test_a_file_the_base_fails_only_alone_is_not_called_failing_on_base_too`
   is the one to read twice: its layout fails at the base only when run
   alone, and under one whole-row run the base's record holds the row's
   own outcome for it, which is what the owner's group rule wanted and
   could not get.
9. **What a person reads changes, and is documented and pinned in the same
   commit (§14):** `templates/config.md` rule 3, rewritten whole and short
   — how the recorder is loaded, that the row runs once at the base
   unchanged, the five-row table, the cost (one more run of the whole row,
   only on a failing suite), how a row earns the word, and the limits of
   §*The class* — with its pins moved; the **New?** bullet of
   `skills/verify/SKILL.md` §*The broad gate*, whose causes become no
   record at `HEAD`, no record at the base, and a base run that ended
   before reaching the file, and which sends the reader to `suite-at-base.txt`
   and `records/`; `compare_at_base`'s docstring and the module docstring's
   paragraph beginning *On a failing test the comparison against the base
   is reactive and mechanical*, which names the prefixes and the JUnit
   report today; the comments over every constant that stays. The sentence
   "`new?` with the reason no run measured it" stays, and is pinned.
10. **Read and not edited, with the grounds:** `README.md` (the sealer row
    and the flow line "new? → not measured at the base"), `README.ko.md`
    (the same two), `agents/sealer.md` §*Boundaries* and its report list,
    `agents/smith.md` (the paragraph beginning "When the sealer reports a
    failure"), `docs/the-broad-gate.md`. Each says `new` and
    `failing on base too` are measured at the base and `new?` means no run
    there measured the file; under this work the row at the base runs the
    failing files where it collects them, and the sentences stay true.
    `changelog/0.18.3.md` is a released record and is not edited.
11. **The records.** The ledger fragment
    `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md`
    holds the new rows and a `Corrected ·` row for every released row this
    makes false, read by this frame: `seal/releases/0.18.3.md` R1 (the
    report and its reader), R2 (the proof pass), R3 (the groups and the
    lone run), R4 (rule 3's text), R5 (the corpus words), and its
    `Corrected · D1`, `D2`, `B3`, `S5`, `B4`; `seal/releases/0.18.1.md` B2
    (`row_prefixes`); `seal/releases/0.18.2.md` D2 where 0.18.3 did not
    already correct it. `evidence-check` finds any others, and re-reads go
    through `--reverify --into`. The changelog fragment is
    `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/changelog.md`,
    begun from the shape of the 0.18.3 fragment (`git show v0.18.3:seal/specs/1791180640-…/changelog.md`),
    naming #825, #807, #813, #816 and #818 and saying what a release-note
    reader sees change. `tests/test_release_hygiene.py`'s two exemptions
    move or go (R11).

### Out, and why

| Left out | Why | Who answers |
|---|---|---|
| Loading the recorder by `PYTEST_PLUGINS` instead of `-p` in `PYTEST_ADDOPTS` | Both need `PYTHONPATH` and both are inherited by children (R1, R2). The owner's direction names `-p`; `PYTEST_PLUGINS` would trade a row that sets `PYTEST_ADDOPTS` for a row that sets `PYTEST_PLUGINS`, and only the first exists in this repository's records | decided here; `plan.md` Alternatives (NAME NOT IN TREE) |
| Recording in xdist workers, or in a pytest a test spawns | The controller receives every report (R5), and a child's record would be a second session about the same tests, with an inner run's record the inner-run class of #789 come back | decided here |
| Reading `FAILED` lines where a keyed record exists | Mixing the two lists is the inference this work removes; a runner that loaded no recorder contributes no file (Scope 4) | decided here; rule 3 names it |
| Running the base where `HEAD` left no record | Nothing to compare: the files are known only by name, and a base record could match them only by the same inference | decided here |
| A `docs/the-broad-gate.md` clause about the comparison | Rule 3's home is the template; a policy clause is `settle`'s to fold after release | the release's `settle` run |
| Fixing #813 and #818 on their own | Both disappear with the regexes on the measured path (Scope 4, 5); #813's one-character widening of `FAILED_RE` is for the fallback alone | decided here, as #825 asked the frame to |
| `( … )` and `{ …; }` groups, compound commands, `&` rows | `row_prefixes` retires, so the row's shape no longer matters to the comparison; what `cmd.exe` is handed is `handed_to_shell`'s and unchanged | as those items left them |
| A record the row's own tests forge or append to | Constructed only, needs a test written against this gate's own key or file (§*The class*) | the repository owner, if it is ever met |
| Shortening the whole-row base run (`-x`, `--lf`, the failing files appended) | Appending files is what made rows collect beyond them and runners drop arguments; `-x` makes the not-reached row fire. One unchanged run is the price of no inference | decided here |

## User scenarios & acceptance *(mandatory)*

Every gate case lives in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
and is built with `base_then_feature`, `verdict_of` and `run_gate(repo,
keep=…)`; `SUITE_ROW` collects `tests`, `FILES_ROW` collects what it is
handed. The recorder's own cases live in a new module,
`tests/test_the_recorder_writes_what_its_process_ran.py`, driving pytest as
a subprocess over a scratch project. "Seen red" means the case was run
against a9d7b0e5's `broad_gate.py` and failed there (§15); for the recorder's
cases, against the module with the hook body deleted.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The recorder records its own process | A scratch project with a passing and a failing test, pytest run with the environment of Scope 2. Then one `<key>-<pid>.jsonl` exists with a `session` line, a `test` line per phase per test with absolute paths that resolve, and an `end` line with exit 1 | executed; seen red with the logreport hook deleted |
| S2 | A child records nothing | The failing test spawns `pytest` on a second file in a subprocess (under `-s`, `-q`, `-n 2`). Then exactly one record file carries the key, its `test` lines name the outer file only, and the inner run's output is in the text | executed; seen red with the `pop` replaced by `get` (two files) |
| S3 | An in-process second session records nothing | A test calls `pytest.main([...])`. Then one record file, naming the outer file only | executed; seen red with the claim-once rule deleted |
| S4 | xdist's controller records the whole run | The project under `-n 2`, two files, one failing, one with a collection error. Then one record file, both files' lines in it, the collection error as a `collect` line | executed; measurement Q-M2 first |
| S5 | No key, no record | The environment without `SPECSEAL_RECORD_KEY`, and separately without `SPECSEAL_RECORD_DIR`. Then no file is written and the run's exit is pytest's own | executed |
| S6 | The anchor, earned | `FILES_ROW` and `SUITE_ROW`, plain and xdist. The base fails `tests/test_two.py`, so does the branch. Then exactly `failing on base too`, `suite-at-base.txt` kept once, and `records/base-*.jsonl` names the file failing | executed; seen red on the kept-file assertion (a9d7b0e5 keeps `suite-at-base-1-1.txt`), and `SUITE_ROW` seen red on the word (a9d7b0e5: `new?` beyond) |
| S7 | The branch broke it | The base passes `tests/test_two.py`, the branch fails it. Then `new` | executed; the 0.18.x cases keep their word |
| S8 | A new file | The branch adds `tests/test_two.py` failing; the base passes everything. Then `new` from the exit-0 row, and no `new?` | executed; seen red on the kept-file assertion |
| S9 | Not reached | The base's `tests/test_one.py` fails and the branch adds a failing `tests/test_two.py` that the base never collects; and separately `FILES_ROW -x` with two base failures. Then `tests/test_two.py` reads `NOT_REACHED` naming the exit | executed; seen red (a9d7b0e5: `new` from the lone run) |
| S10 | Two runners in two directories | `TWO_RUNNERS`' rows (`FILES_ROW --ignore=sub ; cd sub && FILES_ROW`, the `sh -c` form). The base fails the file under the second runner. Then that file, spelled `sub/tests/test_two.py`, reads `failing on base too`, and a same-named root file the base passes reads `new` | executed; seen red (a9d7b0e5: `MULTI_RUNNER`) |
| S11 | Droppers that pass the environment on | `sh -c '{FILES_ROW}'` (POSIX, skipped with reason on Windows) and `FILES_ROW -p no:junitxml`, failing base. Then `failing on base too` | executed; seen red (a9d7b0e5: `NO_RUNNER`) |
| S12 | A runner without the gate's environment | `env -i PATH=… {FILES_ROW}` alone: `NO_RECORD`. Beside a recording runner: that runner's files measured, the other's absent from the list and its `FAILED` lines in `suite.txt` | executed; seen red on the first (a9d7b0e5: `NO_RUNNER`, a different sentence) |
| S13 | No record at `HEAD` | A row that is not pytest but prints a `FAILED a/b::t` line, and `FILES_ROW` with `PYTHONPATH` set by the row itself. Then each named file reads `NO_RECORD_AT_HEAD`, no scratch worktree is added and no `suite-at-base.txt` exists | executed; seen red |
| S14 | The group, measured per file | Two failing files the base carries, one passing and one failing at the base, run together. Then `new` and `failing on base too`, from one `suite-at-base.txt`, no file run alone | executed; seen red (a9d7b0e5: `COMPANY` for both) |
| S15 | Fails only when alone | `test_a_file_the_base_fails_only_alone_is_not_called_failing_on_base_too`'s layouts (a sibling on `sys.path`, state set at import, a session fixture's teardown). Then the base's record carries the row's own outcome for the file and the word follows it: `new` where the row passes it | executed; the case keeps its word and loses its reason |
| S16 | The inner-run class stays closed | `INNER_OUTPUT`, `FAILING_BASE_INNER_ON_STDERR`, `PASSING_BASE_INNER_ON_STDOUT` (`-s`, `--capture=sys`, `-rN`, `-rP`, `-qq`, xdist). Then the words are the base's own and the inner run is in no record | executed; the 0.18.3 cases keep their words |
| S17 | A path holding a space (#813) | `tests/test one.py` failing on both. Then `failing on base too`, listed as `tests/test one.py` | executed; seen red |
| S18 | The listing is posix (#818) | `sub/tests/test_two.py` on Windows. Then the listed path holds `/`, and `verdict_of` needs no `\` normalisation | executed on CI's `windows-latest` leg; seen red there |
| S19 | The texts | Rule 3, the **New?** bullet, the module docstring sentence and the three reasons are pinned whole or by their deciding sentence; the retired sentences are asserted gone | executed; each pin seen red with its sentence deleted |
| S20 | The regression corpus | Every layout of `REGRESSED` run through the new gate; `REGRESSED_WORDS` re-derived from each layout's `at_base` dictionary: `on` where the base's own file fails under the runner that collects it, `new` where it passes or is absent with exit 0, `new?` only by the table. Then no `failing on base too` where the layout's `at_base` passes the file | executed — phase 4 (`plan.md`) |
| S21 | This repository's own row | `uvx ruff check . && uvx ruff format --check . && bin/test -q` with one test failing at the base and on the branch, through the gate. Then `failing on base too`, one `suite-at-base.txt`, one `records/base-*.jsonl` written under `-n auto` by the controller | executed — a phase-2 probe, not a planted case (the suite does not run `uvx`) |
| S22 | This plugin's own suite under the sealer | The outer gate's `-p` and `PYTHONPATH` reach every case that spawns the gate; the inner gate's own key is claimed by the fixture's pytest. Then the suite is green under `broad-gate` | executed — the sealer's run is the measurement |

## Data & interfaces

- `skills/verify/scripts/pytest_record/specseal_pytest_record.py`: hooks
  `pytest_configure`, `pytest_sessionstart`, `pytest_runtest_logreport`,
  `pytest_collectreport`, `pytest_sessionfinish`. Reads
  `SPECSEAL_RECORD_KEY` (taken out at import) and `SPECSEAL_RECORD_DIR`.
  Writes `<dir>/<key>-<pid>.jsonl`, UTF-8, one JSON object per line with a
  `kind` of `session`, `test`, `collect` or `end`.
- `broad_gate.py#recording_env(keep, key)` → the environment of Scope 2.
- `broad_gate.py#read_record(directory, key, worktree)` → the `Record` of
  Scope 3; pure, unit-tested on its own with a table of lines (a failing
  test, an error in setup, an xfail, a skip, a collect failure, a line of
  another key, a line that does not parse, a path outside the worktree, a
  path under a symlinked temp root).
- `broad_gate.py#compare_at_base(root, base, command, files, keep)`:
  signature and return unchanged; one `run(...)` call; kept
  `suite-at-base.txt` and `records/base-*.jsonl`.
- `broad_gate.py#failing_files(text)`: unchanged name, `FAILED_RE` widened
  to `^FAILED\s+(.+?)::`; read only where `HEAD` left no record.
- Reasons: `NOT_MEASURED` unchanged; `NO_RECORD_AT_HEAD`, `NO_RECORD`
  (plain, and formatted with nothing), `NOT_REACHED` formatted with the
  exit. The smith names the constants; each opens `NOT_MEASURED`.
- Kept files under `--keep-output`: `suite.txt`, `suite-at-base.txt`,
  `records/head-<token>-<pid>.jsonl`, `records/base-<token>-<pid>.jsonl`.

## Open questions → questions.md

`questions.md` beside this file. One row is a person's and does not block:
its default is what this frame builds. Two are measurements for phase 1 and
three are the work's.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     `<who>` takes the two values the `Planning` row of `routing.md` takes,
     `framer` or `the session`, and a mark that disagrees with that row is
     refused at the pull request rather than guessed at.
     A reframe adds `Reframed <date> by <who>, after round <N>.` UNDER this
     line when the review chain sends the work item back to its framer. -->

Framed 2026-10-06 by framer, before the build.
