# Feature Specification: a mutation clears one file's bytecode and ends at a timeout

<!-- seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Milestone `release: 0.17.0`, item A: #641, with #129 as its correctness twin.
This branch is cut from `release/v0.17.0` at `cd24f516`. The owner put all six
0.17.0 items in scope on 2026-10-01 and pressed `automation`.

**The class.** `agents/smith.md` §Phases step 4 tells the implementer to
mutation-test every unit it added and to "clear `tests/__pycache__` between
mutations". That sentence does two things wrong at once, and they are one
defect read from two sides.

- **It clears the wrong thing.** CPython reads a cached `.pyc` instead of the
  source whenever the source's size and its mtime in whole seconds match what
  the cache recorded. A same-length mutation written and restored inside one
  second is exactly that match, which is how `WINDOW = 15` → `25` read green
  (#89) and how a false red arrived in #370. The cache that matters is the
  one beside the **mutated file**, wherever that file lives; `tests/` holds
  the importers, whose bytecode is valid and unchanged. So the instruction
  misses the case #129 met (`.github/scripts/__pycache__`) and the case #326
  met (`skills/verify/scripts/__pycache__`), and any third location would
  reproduce it under a new name.
- **It clears far too much.** `rm -rf tests/__pycache__` forces pytest to
  recompile all 142 test modules on every mutated run. The flow logs put that
  at about 5.8 of 10.1 command minutes on one segment (#197) and 1.6 of 3.9
  on another (#348), and no document named it as a cost.

A third thing the sentence does not do: bound the run. Nothing in the loop
ends a mutated run that hangs, and one did, for 32 minutes (#577).

The class closes when the loop's housekeeping is derived from the mutated
file rather than enumerated by directory, every run of it is bounded, and the
smith performs that loop through one command whose restore cannot be skipped
or taken from `HEAD`. Rewording the sentence to name a second directory closes
the instance #129 found and leaves the class.

**What the tree already holds.** `skills/verify/scripts/arm_check.py` is a
mutation loop with exactly these mechanics (read, at `cd24f516`):
`clear_bytecode_cache` removes every `<stem>.*.pyc` under the mutated file's
own `__pycache__` and under an env-set `PYTHONPYCACHEPREFIX` mirror;
`run_arms` runs the command with `PYTHONDONTWRITEBYTECODE=1`, restores the
module from bytes it held and compares a sha256, and bounds the wait at 900 s
per operator, reporting a timed-out pair as *not measured* rather than as a
verdict. Four cases in `tests/test_arm_check.py` pin those halves and eight
rows of `seal/releases/0.9.5.md` record them. What `arm-check` cannot do is
the smith's loop: it mutates a module's **arms** under two fixed operators,
and the smith's mutation is whatever breaks the unit it just added — a
constant, a deleted sentence in a markdown file, a flipped comparison. So
the mechanism exists and the smith has no way to type it.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #641 (the ticket) and the milestone description | The order and the grounds: "Clear only the mutated file's bytecode, and put a timeout on every mutated run." The two things that must not break: the same-length mutation still reads red; restore from kept bytes, never from `HEAD` |
| #129 (the twin) and its one comment | The class is *any* location, and the ticket's own proposed general form ("every directory a mutated module or its importer lives in") is wider than the defect: only the mutated file's cache can be stale. The comment's size-and-mtime account of pyc validation is right and is the ground for deriving the cache from the file |
| `CLAUDE.md` §*The goal a design is chosen against* | A loop that stops to ask nobody and ends on its own bound is the design; the prompt budget is zero |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* and §*An anchor degrades to DRIFTED* | New rows go to `seal/ledger/1790815610-….md`. The four released rows anchored on `agents/smith.md#"## Phases"` drift when step 4 changes; each is re-read against the edit and re-stamped with a dated note, not re-pointed |
| `docs/the-agent-set.md` §*One contract every agent receives, and one definition each* | A rule the smith acts on lives in `agents/smith.md`, which it receives at startup. `skills/verify/SKILL.md` is preloaded by no agent (read: all four `skills:` lists), so the command has to be named in the definition itself |
| `docs/the-broad-gate.md` §*A check that cannot fail is not a check* | `arm-check`'s clause. The new command is the same rule asked of one unit at a time rather than of a module's arms, and it is report-shaped the same way: a verdict, never a gate |
| `skills/agent-contract/SKILL.md` §9, §12, §14, §15 | §9: an edit must be able to fail, so a replacement that matches zero or two places is refused before anything is written. §12: the class above, closed by derivation rather than by a list. §14: a sentence the smith reads changes, so a case pins the new text and the absence of the old. §15: every new case is seen red first, and this file says where |
| `skills/code-review/SKILL.md` §*A fixture chain is `&&`* ("give any call that could run long a timeout you chose rather than one you assumed") | The repository already states the bound as a rule for reviewers; this work gives the smith's loop one |
| `skills/verify/SKILL.md` §*`arm-check` asks condition 2 of a whole module* | The timeout paragraph: `subprocess.run`'s bound kills the direct child only, and `bin/test` puts pytest one process further down. The new command must not inherit that hole, because the documented `--tests` form is the wrapper |
| `tests/test_the_handoff_before_round_one.py#test_the_smiths_definition_mandates_mutating_every_unit_it_added` | The two sentences that must survive the rewording, verbatim: "Mutation-test every unit you added, one at a time, before you hand over." and "watch one go red" |
| `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` | A shipped script named by a shipped document has a `bin/` wrapper pair (`<name>` and `<name>.cmd`, underscores to hyphens), and every shipped document naming it carries the command or the repo-relative path |
| `tests/test_a_moved_rule_leaves_its_definition.py` (`WINDOW = 15`) | The new wording in `agents/smith.md` may cite the contract and may not carry fifteen consecutive words of any of its sections |
| `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` and `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | A new script under `skills/` carries no `zip(` with `strict=`, no `.UTC`, and no three-part version token |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The command exits by verdict and gates nothing, so it is not a gate. The failure direction is still stated below, because a loop that reports *red* for the wrong reason is the counterfeit this repository's own history is full of |

## What was measured before the frame, and by whom

| # | Fact | Label |
|---|---|---|
| M1 | `grep -l "tests/__pycache__" tests/*.py` returns nothing (exit 1). Outside `seal/` and `CHANGELOG.md`, the string occurs in one shipped file, `agents/smith.md:267` | executed by the framer, 2026-10-01 at `69bf9f30` |
| M2 | `python3 --version` on this machine is 3.14.4. The main clone's `.venv/pyvenv.cfg` says 3.13.9. This worktree has no `.venv`, so its first `bin/test` builds one with `uv venv --python ">=3.12"` | executed (the two reads) and read (`run_tests.py#build`) by the framer |
| M3 | Two interpreter tags coexist beside one source in the main clone today: `tests/__pycache__` holds 131 `cpython-313-pytest-9.1.1.pyc` and 1 `cpython-313.pyc`; `hooks/__pycache__` 21 of `cpython-313` and 6 of `cpython-314`; `skills/verify/scripts/__pycache__` 6 and 3; `.github/scripts/__pycache__` 13 and 3 | executed by the framer (a directory listing) |
| M4 | `importlib.util.cache_from_source(path)` names the cache for the interpreter that calls it. Called from `python3` here it names `cpython-314.pyc`; the suite's `.venv` reads `cpython-313.pyc`. So #641's option 1 as literally written removes a file the test child never reads, on the owner's own machine. `arm_check.py#clear_bytecode_cache`'s `<stem>.*.pyc` glob removes every tag | read (the function and Python's documented tag rule); the version split is M2 and M3, executed |
| M5 | `arm_check.py#run_arms` writes the mutation, calls `clear_bytecode_cache`, runs with `env["PYTHONDONTWRITEBYTECODE"] = "1"` and `timeout=900.0`, and in `finally` calls `restore` (sha256-compared) and `clear_bytecode_cache` again. A `TimeoutExpired` is recorded as *not measured*. Pinned by `tests/test_arm_check.py#test_no_arm_runs_while_cached_bytecode_for_the_module_exists`, `#test_the_run_leaves_no_bytecode_cache_behind`, `#test_no_verdict_is_taken_after_a_restore_that_did_not_land`, `#test_a_command_that_never_returns_is_recorded_as_unmeasured` | read by the framer |
| M6 | `subprocess.run(..., timeout=)` kills the direct child and nothing below it. With `--tests "bin/test …"` pytest is a grandchild (`bin/test` execs `run_tests.py`, which `subprocess.run`s pytest), so a timed-out run leaves the suite running. Measured by #313's reviewer with a sleeping grandchild against a 1 s bound | read from #313 (open); not re-run by the framer |
| M7 | No script under `skills/*/scripts/` imports a sibling script; every import there is standard library. A script run by its path has its own directory first on `sys.path`, which is how `bin/arm-check` reaches `arm_check.py` | executed (the grep) and read (`bin/arm-check`) by the framer |
| M8 | The flow-log figures #641 cites, as the logs state them: #197, five of eight slowest commands were `rm -rf tests/__pycache__ && ./bin/test …` at 121, 96, 50, 41 and 41 s, about 5.8 of 10.1 command minutes over 32 mutations; #348, 1.6 of 3.9 min; #577 item E, 108 m segment with "32 m lost to one hung mutated pytest that it killed (its own process; the harness flagged the kill)"; #601 item D, 13, 14 and 11 mutation probes per phase. The slowest ordinary mutated command in #577's tables is 158 s. **How the harness's own command bound did not end the 32 m hang is not in the log** | read by the framer from the issues; the mechanism of the hang is unverified and nobody's finding |
| M9 | Rows anchored on `agents/smith.md#"## Phases"@df6ee11b` (the framer read hash `cede28c2`; **Corrected 2026-10-01** by the build after phase 3's edit moved the section and the rows were re-read and re-stamped to this hash, so the stamp says what the rows now hold): `seal/releases/0.6.0.md` L5, `0.8.1.md` R8, `0.12.0.md` (the design gate's second copy), `0.15.1.md` N1. A `# RIDER:` at `agents/smith.md:81-116` is stamped `Verified 2026-09-25 against "## Phases"@035903e4`. L5 also anchors `tests/test_the_handoff_before_round_one.py#test_the_smiths_definition_mandates_mutating_every_unit_it_added@6a971c8f` | executed (the grep) by the framer |
| M10 | #641 has no comments. #129 has one, by a third party, proposing `PYTHONDONTWRITEBYTECODE=1` plus a strictly increasing whole-second mtime on every write, and naming a per-mutant `PYTHONPYCACHEPREFIX` as untested | executed by the framer |
| M11 | `timeout` on this machine is Homebrew coreutils at `/opt/homebrew/bin/timeout`, not an OS-provided utility, and GNU `timeout` is absent from a stock macOS. `agents/smith.md` cannot lean on it | executed (`command -v`) and read |
| M12 | `README.md`'s cheat sheet lists ten commands a person runs by hand; `arm-check` is not among them | executed (the grep) |

## Scope

**In.**

1. **A command, `mutation-check`, one mutation per call.** A new script
   `skills/verify/scripts/mutation_check.py` with the wrapper pair
   `bin/mutation-check` and `bin/mutation-check.cmd`, in `bin/arm-check`'s
   shape. It takes a file, one literal replacement, the command the cases run
   as, and a bound; it holds the file's bytes and their hash, refuses a
   replacement that lands anywhere but exactly once, writes the mutation,
   removes that file's cached bytecode for every tag, runs the command with
   `PYTHONDONTWRITEBYTECODE=1` under the bound, restores from the held bytes
   and compares the hash, removes the bytecode again, and prints one verdict
   line. It imports `clear_bytecode_cache` and `restore` from `arm_check.py`
   rather than carrying a second copy (M7 says how the import resolves).
2. **The bound ends what the run started.** On POSIX the command runs in its
   own session (`start_new_session=True`) and a timed-out run's whole process
   group is ended, so a wrapper's pytest does not outlive the verdict (M6).
   On Windows the direct child is ended and the verdict says that anything it
   started was not. `KeyboardInterrupt` restores the file and ends the group
   the same way.
3. **`agents/smith.md` §Phases step 4** keeps its two pinned sentences,
   names the command with its shape, and no longer names `tests/__pycache__`
   or any directory. §Boundaries' "Commit before you mutate, and restore from
   your own copy" bullet says the command holds that copy and compares the
   hash. `skills/verify/SKILL.md` gains a `####` section beside `arm-check`'s
   with the command, its verdicts, its bound and what the bound ends.
4. **Cases, each seen red first**, in one new module
   `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`:
   the scenarios below.
5. **Two measurements the ticket asks for**, taken by the build and recorded
   with date, machine and module in this item's ledger fragment: the
   per-mutation wall clock of a 10-mutation loop on one module both ways
   (`rm -rf tests/__pycache__ && bin/test …` against `mutation-check`), and
   the cost of `-n auto` against `-p no:xdist` for a handful of cases. The
   smith's wording recommends `-p no:xdist` only if the second measurement
   says so (`questions.md` Q1).
6. **The ledger**: the four `## Phases` rows and the rider re-read and
   re-stamped (M9); this item's rows in `seal/ledger/1790815610-….md`.
7. **The changelog fragment**, `seal/specs/1790815610-…/changelog.md`.

**Out, each with its grounds.**

- **`arm-check` adopting the process-group bound.** That is #313, open, which
  names the Ctrl-C consequence and the Windows divergence as decisions to
  take on purpose. The new command takes them for itself (In-2) and `run_arms`
  is not edited; the PR body names #313 so the owner can fold the two. A
  second implementation of the bound beside `run_arms` is the cost, stated.
- **A sidecar copy of the original on disk.** #312: the only copy of the
  original is in the process's memory, and a `SIGKILL` loses it. The smith's
  own rule, *commit before you mutate*, is what bounds that loss, and the
  script's docstring says so. Not built here for the reasons #312 records.
- **A process-group kill on Windows.** #313's option 3 needs a machine or a
  CI leg that runs it, and `bin/arm-check.cmd` has been run by nobody. The
  Windows path ends the direct child and says so (In-2); the strategy is
  chosen by a function that takes the platform as an argument, so the choice
  is pinned from any machine (§13).
- **`agents/warden.md`.** The warden reproduces findings by mutation too, and
  #577's warden rounds typed the same `rm -rf tests/__pycache__` command, but
  the ticket names the smith's definition and no instruction in the warden's
  says how to mutate. The command is in the tree and the smith's hand-back
  names it; whether the warden's definition should point at it is a
  definition change with its own pin, outside item A.
- **A README cheat-sheet entry.** `arm-check` is not there either (M12), and
  both READMEs move together. The owner's call (`questions.md` Q2), default
  not added.
- **Bringing `agents/smith.md` under `tests/test_docs_line_wrap.py`.** An open
  row of `seal/follow-up.md` for the owner. The new paragraph is written
  wrapped so it adds nothing to that sweep.
- **Clearing the importer's cache.** #129's proposed general form includes
  the directory the importer lives in. A test module's bytecode is valid for
  its unchanged source and is never stale; clearing it buys the recompile this
  item removes. Not done, and `questions.md` J2 records why.

## User scenarios & acceptance *(mandatory)*

Each case is written and seen red **before** the change that turns it green.
The base is `cd24f516`. Every fixture lives under `tmp_path`; nothing is
planted in the repository's own `__pycache__` directories.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the mutated file's bytecode is gone for every tag at the moment the cases run, and none is written | Given a module under `tmp_path` with a planted `__pycache__/<stem>.<running tag>.pyc` made by a real import **and** a hand-written `<stem>.cpython-399.pyc`, when `mutation-check` runs with a `--tests` probe that records whether any `<stem>.*.pyc` exists and whether `PYTHONDONTWRITEBYTECODE` is set, then the probe saw none and saw the variable, and after the run no `<stem>.*.pyc` exists | executed: a new case. **Red at the base** (no command). After the build, **red** with the glob replaced by `os.remove(importlib.util.cache_from_source(path))` alone — the foreign tag survives — which is M4's finding pinned. Timing-dependent reproduction is not attempted; the mechanism is pinned, as `tests/test_arm_check.py#test_no_arm_runs_while_cached_bytecode_for_the_module_exists` does and says why |
| S2 · the same-length mutation reads red | Given `VALUE = 15` in a module and a `--tests` probe asserting `VALUE == 15` by importing it, when `--replace "VALUE = 15" "VALUE = 25"` runs immediately after the probe has imported the unmutated module once (so a cache exists), then the verdict is red | executed: a new case. **Red at the base**. This is the ticket's "What must not break", and it holds by S1's mechanism; the case is the smith's own loop in miniature |
| S3 · a replacement that cannot land exactly once is refused before anything is written | Given `OLD` absent, and given `OLD` present twice, when the command runs, then it exits 2, names the count, and the file and its directory are byte-for-byte untouched. Given `OLD` present once, the `--tests` probe sees `NEW` in the file | executed: a new case, three branches. **Red at the base** |
| S4 · the file is restored from held bytes and the restore is proved | Given a `--tests` command that rewrites the file (so the restore has something to undo), and separately `restore` made to raise, when the command runs, then the file is byte-identical afterwards in the first, and in the second the run stops with `was not restored` in its output and exit 2 | executed: a new case, two branches. **Red at the base** |
| S5 · a run that never returns ends at the bound, with a named verdict and nothing it started left alive | Given `--tests` naming a wrapper script that spawns a child sleeping 30 s, and `--timeout 1`, when the command runs, then it returns within a few seconds with `timed out` and the bound in its output, exit 2, the file byte-identical, no `<stem>.*.pyc` left, and the grandchild's pid no longer alive (polled) | executed: a new case, `skipif os.name == "nt"`. **Red at the base**, and **red after the build** with `start_new_session` and the group kill removed: the grandchild is still alive — #313's measurement, re-taken here on the new command |
| S6 · the Windows half ends the direct child and says what it did not end | Given the strategy chooser asked with `os.name` as `nt`, then it returns the direct-child strategy and the timed-out verdict text names that anything the command started was not ended | executed on any machine: a new case driving the chooser with the platform passed in (§13). **Red at the base** |
| S7 · the verdict and the exit code say which of three things happened | Given `--tests` that fails against the mutant, then the output opens with `red` and the exit code is 0. Given one that passes, `SURVIVED` and 1. Given one that cannot be spawned, `could not start` with the error and 2 | executed: a new case, three branches. **Red at the base** |
| S8 · a file that is not Python is mutated the same way | Given a markdown file and `--replace` deleting one sentence (`NEW` empty), with a `--tests` probe that reads the file, then the probe saw the sentence gone, the file is restored, and the bytecode step removed nothing and reported nothing | executed: a new case. **Red at the base** |
| S9 · the smith's definition names the command and no longer names a directory to clear | Given `agents/smith.md`, then the flattened text carries `mutation-check` with `--replace` and `--tests` in one command, carries both sentences the existing case pins, and does not carry `tests/__pycache__` | executed: a new case. **Red at the base**: the command absent and the directory present. The existing `#test_the_smiths_definition_mandates_mutating_every_unit_it_added` is unchanged and stays green |
| S10 · the command is reachable from every shipped document that names its script | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`, unchanged | executed. **Red** the moment `mutation_check.py` exists without its wrapper pair, or `skills/verify/SKILL.md` names the file without the command — write the pair and the section before that module is run green |
| S11 · the per-mutation wall clock, both ways | Given one module of this repository and ten mutations of one unit in it, run once through `rm -rf tests/__pycache__ && bin/test <module> -q -k <cases>` with the mutation applied by hand and once through `mutation-check … --tests "bin/test <module> -q -k <cases>"`, then the per-mutation figures are recorded with the date, machine and module. The ticket's target is under half the clear-all figure; the frame promises no figure | executed by the build, phase 4; recorded in the ledger fragment, not a case |

**Constraints the build meets, verified rather than cased.**

| # | Constraint | Verified how |
|---|---|---|
| C1 | `mutation_check.py` follows `arm_check.py`'s own interpreter conventions (`from __future__ import annotations`, nothing 3.10+ in syntax, no `zip(` with `strict=`, no `.UTC`, no three-part version token) and is ruff-clean | executed: `tests/test_a_script_says_which_interpreter_it_needs.py`, `tests/test_release_hygiene.py`, `uvx ruff check` and `uvx ruff format --check` on the touched `.py` files |
| C2 | `arm_check.py` is not edited, and `tests/test_arm_check.py` stays green | executed: `bin/test tests/test_arm_check.py -q` |
| C3 | The definition edit keeps every existing pin green: `tests/test_the_handoff_before_round_one.py`, `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_one_word_one_meaning.py`, `tests/test_every_agent_reads_the_contract.py`, `tests/test_a_phase_hands_the_next_one_a_record.py`, `tests/test_a_corrected_sentence_survives_elsewhere.py` | executed, narrow runs |
| C4 | The four `## Phases` rows (M9) are re-read against the step-4 edit and re-stamped with a dated note; the rider at `agents/smith.md:81-116` is read and re-stamped with `rider_check.py --reverify --only agents/smith.md`; `evidence-check` reports no drift on `seal/releases/*.md`, `seal/ledger.md` and the fragment afterwards | executed: `evidence-check` and `.github/scripts/rider_check.py` |
| C5 | No case leaves anything: every fixture under `tmp_path`, every spawned process reaped or proven dead, `git status --porcelain` empty after the module runs | executed by the build and said in the hand-back |
| C6 | `payload-meter`'s figure for `smith` before and after the wording change, reported in the hand-back as a delta; no cap is set | executed: `payload-meter` |

## Data & interfaces

**The command.** Suggested shape; `questions.md` Q3 leaves the name and the
exact verdict spelling to the work.

```
mutation-check <path> --replace OLD NEW --tests "<command>" [--timeout S] [--cwd DIR]
```

- `<path>`: the file to mutate, any text file. Python or not, the restore and
  the hash compare are the same; the bytecode step is a no-op for a file with
  no `__pycache__` beside it.
- `--replace OLD NEW`: literal text, no regex. `OLD` must occur exactly once
  or the run is refused before any write (S3). `NEW` may be empty.
- `--tests "<command>"`: split with `shlex`, as `arm-check`'s `--tests` is.
  Run with `cwd` as given, the inherited environment plus
  `PYTHONDONTWRITEBYTECODE=1`, output captured and shown after the verdict.
- `--timeout S`: seconds the command is waited for, default 300; `0` removes
  the bound, as `arm-check` spells it (`questions.md` Q4 holds the number).
- Output: one verdict line first — `red`, `SURVIVED`, `timed out after S s`,
  `could not start`, or `refused` — with the elapsed time, then the command's
  own output. Exit 0 for red, 1 for survived, 2 for everything that measured
  nothing; so a run of `mutation-check … && mutation-check …` stops at the
  first unit nothing watches. One file holds the whole loop:
  `clear_bytecode_cache` and `restore` are imported from `arm_check`.
- Nothing is read from or written to git. The restore source is the bytes
  read before the write, held in memory for the length of one run.

**`agents/smith.md`**, step 4, suggested text (the work finalises the words;
the two sentences in bold are pinned verbatim and stay):

> **Mutation-test every unit you added, one at a time, before you hand
> over.** Break one unit, run the cases that cover it, and **watch one go
> red**. A unit that stays green while broken has nothing behind it, whatever
> the suite total says. One command does the loop's housekeeping:
>
> ```
> mutation-check <file> --replace "<old>" "<new>" --tests "bin/test tests/<module>.py -q -k <cases>"
> ```
>
> It writes the break, removes that one file's cached bytecode for every
> interpreter tag, runs the cases under a bound (300 s unless `--timeout`
> says otherwise), restores the file from the bytes it held and compares the
> hash, and prints red, survived or timed out. A timed-out run is a result
> to report, not a kill to find later. Clearing a whole `__pycache__` is
> neither needed nor enough: the stale `.pyc` that read a same-length
> mutation wrong sat beside the module, wherever the module was.

§Boundaries, the existing bullet gains one sentence: `mutation-check` holds
that copy and compares the hash after the restore, which is why the loop runs
through it.

**`skills/verify/SKILL.md`**: a `####` section after `arm-check`'s and before
`### 3. Bound to the tree`, carrying the command, the three verdicts and
their exit codes, the bound and what it ends on each platform, and a pointer
at `arm-check` for a module's arms. The `arm-check` section's `--timeout`
paragraph is not edited; `seal/releases/0.15.1.md` N2 anchors that heading.

**Ledger coordinates**: `plan.md` §*Ledger*.

## Failure direction and prompt budget

The loop reports **red for the wrong reason** in two ways, and both are the
counterfeit this repository's own rows describe. A cached `.pyc` for a
previous mutation makes the interpreter run the wrong code (S1 is the
mechanism, S2 the symptom). A restore that did not land makes every later
verdict a verdict about a mutant (S4). Both are refused loudly rather than
reported as verdicts.

It reports **SURVIVED for the wrong reason** when the `--tests` command runs
cases that never import the unit — a coverage question the command cannot
answer, and `agents/smith.md`'s "run the cases that cover it" is where it
stays.

A timed-out run is **not a verdict** (S5). Reporting it as red or as survived
would be a measurement nobody took.

No person is asked anything by the build or by the command. Prompt budget:
zero.

## What the changelog fragment says

Under `### Added`, one bullet, written for a plugin user:

- **`mutation-check`: one command runs one mutation of one unit.** It writes
  the break, removes only that file's cached bytecode — every interpreter
  tag, wherever the file lives — runs the cases you name under a bound
  (300 s by default), restores the file from the bytes it held and compares
  the hash, and prints red, survived or timed out. On POSIX a timed-out run's
  whole process group is ended, so a wrapper's pytest does not outlive the
  verdict (#641, #129).

Under `### Changed`, one bullet:

- **`agents/smith.md` no longer says to clear `tests/__pycache__` between
  mutations.** That clear recompiled every test module on every mutated run
  and missed the cache beside a module imported from anywhere else. The smith
  types `mutation-check` per mutation instead (#641, #129).

## Open questions → questions.md

Nothing here waits on a person. `questions.md` lists the judgments the
tickets left open and how the tree answered each, then the rows still open,
two of them a person's and neither blocking.

Framed 2026-10-01 by framer, before the build.
