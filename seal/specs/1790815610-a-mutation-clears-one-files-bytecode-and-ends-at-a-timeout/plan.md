# Implementation Plan: a mutation clears one file's bytecode and ends at a timeout

<!-- seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-10-01 by the repository owner, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. -->

## Summary

The smith's mutation loop becomes one command per mutation, `mutation-check`,
built on the two functions `arm_check.py` already has for exactly this —
`clear_bytecode_cache` and `restore` — plus a bound that ends everything the
mutated run started. The command derives the cache to remove from the file
it mutated, so no directory is enumerated and #129's class closes with #641's
instance; it recompiles one module instead of 142; and a run that hangs is a
`timed out` verdict a few seconds after the bound rather than 32 minutes
found later. `agents/smith.md` names the command and stops naming
`tests/__pycache__`. Four phases, each a slice the next stands on.

## Technical context

**What the build starts from, by coordinate.**

- `skills/verify/scripts/arm_check.py#clear_bytecode_cache` (lines 758–798
  at `cd24f516`): removes `<stem>.*.pyc` under the file's `__pycache__` and
  under an env-set `PYTHONPYCACHEPREFIX` mirror; returns what it removed.
  `#restore` (801–820): writes the held bytes and raises `RuntimeError`
  naming `was not restored` when the sha256 differs. `#run_arms` (823–949):
  the loop shape to copy — write, clear, run with
  `PYTHONDONTWRITEBYTECODE=1`, `finally: restore; clear`. Its
  `subprocess.run(..., timeout=)` is the half NOT to copy (spec M6).
- `bin/arm-check` and `bin/arm-check.cmd`: the wrapper pair's shape. The POSIX
  half resolves the script relative to itself and `exec`s `python3`; the
  `.cmd` half prefers `py -3` and falls back to `python`. Name the new pair
  `mutation-check` / `mutation-check.cmd`, because
  `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py#command_name`
  derives the command from the filename with underscores to hyphens.
- `agents/smith.md:263-267` (step 4's mutation paragraph) and `:377-382`
  (the Boundaries bullet). The `# RIDER:` at `:81-116` is stamped against
  `"## Phases"` and will fire on the step-4 edit; read it, then re-stamp.
- `skills/verify/SKILL.md:59-125`, the `arm-check` section, for the register
  and for the paragraph that already states the grandchild hole.
- `tests/test_arm_check.py:1049-1208`, the four cache and bound cases, for
  the fixture style: a planted cache made by a real `importlib` load, a
  `SEES_CACHE` probe written to `tmp_path` and named in `--tests`, a verdict
  asserted on what the subprocess *saw* rather than on timing.
- `tests/test_the_handoff_before_round_one.py:156-204`: the pinned sentences
  and the reason the whole clause is asserted rather than its words.

**How the sibling import resolves.** `bin/mutation-check` runs
`python3 <abs path>/mutation_check.py`, and Python puts the script's directory
first on `sys.path`, so `from arm_check import clear_bytecode_cache, restore`
resolves with no path juggling. The test module loads the script the way
`tests/test_arm_check.py` loads `arm_check.py` (an `importlib` spec from the
path) and must put `skills/verify/scripts` on `sys.path` first, or load
`arm_check` under its bare name before the script — say which in the module
docstring. No sibling import exists today (spec M7); this is the first, and
the alternative is a second copy of two ledgered functions.

**The bound, on each platform.** POSIX: `subprocess.Popen(cmd,
start_new_session=True, stdout=PIPE, stderr=STDOUT, env=env, cwd=cwd)`,
`communicate(timeout=bound)`; on `TimeoutExpired`, `os.killpg(proc.pid,
SIGKILL)`, `communicate()` to reap, verdict `timed out after S s`. On
`KeyboardInterrupt` the same kill, then the `finally` restore. Windows:
`proc.kill()` on expiry, and the verdict names that anything the command
started was not ended. The choice is a function that takes `os.name` as an
argument and returns the strategy, so S6 drives it from any machine. The
Ctrl-C consequence #313 records — the child leaves the terminal's group, so
Ctrl-C reaches only the parent — is why the parent kills the group on
`KeyboardInterrupt` and why the docstring says so.

**Constraints the edit is written against** (spec C1–C6): the script loads
on `arm_check.py`'s own claimed interpreters (its `_node_arms` comment says
3.9), so `from __future__ import annotations`, no match statements, no
`zip(..., strict=)`, no `.UTC`; no three-part version token under `skills/`;
`ruff.toml`'s selection (B, SIM, UP, RUF) clean. The definition edit carries
no fifteen consecutive words of any contract section.

**What breaks in six months.** The smith stops typing the command and goes
back to `rm -rf tests/__pycache__`. Nothing in the tree can stop a session
typing a shell line; what S9 pins is that no document tells it to, and the
flow logs' slowest-command tables are where the regression would show, as
they are where this defect was found. The other direction: `arm_check.py`'s
two functions change shape under a later item and the import breaks at
run time rather than at lint — `tests/test_arm_check.py` and S1/S4 load both
files, so the suite goes red before a smith meets it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. One command per mutation, built on `arm_check.py`'s two functions, with a process-group bound on POSIX; the definition names the command** | A session ignores the command and types the old line (above). A second bound implementation stands beside `run_arms`'s until #313 folds them. The sibling import is the first in `skills/*/scripts/` | **Chosen** |
| B. Wording only: per-file `rm -f <dir>/__pycache__/<stem>.*.pyc`, `PYTHONDONTWRITEBYTECODE=1`, `timeout <s>` around `bin/test` | Three tool calls per mutation remain (edit, run, edit back), and the restore is an `Edit` from memory — the class #59 and the two-spaces incident in `run_arms`'s docstring belong to. GNU `timeout` is a Homebrew install here (spec M11) and absent on stock macOS. `timeout` and the harness's own bound both end the direct child only (M6). The definition grows by the whole incantation on every spawn (#292) | Rejected |
| C. `os.remove(importlib.util.cache_from_source(path))`, #641's option 1 as written | Tag-blind: removes the cache for the interpreter running the loop, and the suite's `.venv` reads another tag on this machine today (M2–M4). It would have passed every case written on a machine where the two agree | Rejected as the spelling; the glob in `clear_bytecode_cache` is the mechanism, and S1's foreign tag pins the difference |
| D. `PYTHONDONTWRITEBYTECODE=1` plus a strictly increasing whole-second mtime per write (#129's comment) | Leaves every mutated source with a future mtime after the loop, and depends on `os.utime` landing on a filesystem whose clock is at least whole seconds. The pre-run cache the realistic trigger leaves (`hooks/__pycache__` before any loop, the 0.9.5 row) is not removed by it, only out-raced. Removing the file is exact | Rejected as the primary mechanism; the env half is kept, as `run_arms` keeps it |
| E. `PYTHONPYCACHEPREFIX=<fresh dir>` per mutation | Every source import of the run, standard library included, compiles again on every mutated run: the prefix redirects the whole cache, not the module's. Correct and expensive, and the item exists to remove a recompile | Rejected on cost (read from the variable's documented semantics; not measured here) |
| F. Extend `arm-check` with a `--replace OLD NEW` mode | The report is a module-wide table and its exit code is report-only by a stated decision (`skills/verify/SKILL.md`); a single mutation's result is its exit code. Two tools in one name muddle `tests/test_one_word_one_meaning.py`'s rule by example | Rejected; the sibling imports the two functions instead |
| G. Give `arm-check` the process-group bound in the same item (#313) | Changes a shipped tool's Ctrl-C behaviour and Windows path under an item whose grounds are the smith's loop; #313 asks for that decision on purpose. The PR body names #313 and the helper now exists to fold | Out of scope |
| H. Rely on the Bash tool's own `timeout` parameter | It ends the shell, not pytest's grandchildren, and #577 shows a 32 m loss under it. A bound that lives in the command is what makes the verdict `timed out` rather than a kill found later | Rejected |
| I. A sidecar copy of the original beside the file (#312) | A new on-disk protocol with its own recovery procedure, which #312 enumerates. *Commit before you mutate* bounds the loss already | Out of scope |
| J. A new shared module for the two functions | A third shipped script, which `test_a_document_that_names_a_script_says_how_to_reach_it.py#scripts()` would then demand a wrapper or a classification for; and the functions' ledger anchors move | Rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `mutation_check.py` with the replace, the cache halves, the restore and the three verdicts, run with a plain `subprocess.run` bound for now; the wrapper pair. S1, S2, S3, S4, S7, S8 written and seen red at the base before the script exists, then green. The xdist measurement (spec In-5, second half) taken on one module and written to `phases/phase-1.md` | Executed: `bin/test tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py -q`, `bin/test tests/test_arm_check.py tests/test_a_document_that_names_a_script_says_how_to_reach_it.py tests/test_a_script_says_which_interpreter_it_needs.py -q`, `uvx ruff check` and `uvx ruff format --check` on the touched `.py` files. S1's second red: the glob swapped for `cache_from_source`, seen red, restored | 09ba83c3 |
| 2 | The bound: the platform-chosen strategy, the POSIX session and group kill, the `KeyboardInterrupt` path, the Windows verdict text. S5 and S6 seen red at phase 1's `subprocess.run` form (the grandchild alive), then green | Executed: the new module again, and `tests/test_arm_check.py` unchanged | d1921115 |
| 3 | `agents/smith.md` step 4 and the Boundaries sentence; `skills/verify/SKILL.md`'s new section; S9 seen red at the base then green; S10 green. The four `## Phases` ledger rows re-read against the edit and re-stamped with a `Re-read 2026-10-01` note, the rider read and re-stamped, `evidence-check` clean | Executed: `bin/test tests/test_the_handoff_before_round_one.py tests/test_a_moved_rule_leaves_its_definition.py tests/test_one_word_one_meaning.py tests/test_every_agent_reads_the_contract.py tests/test_a_phase_hands_the_next_one_a_record.py tests/test_a_corrected_sentence_survives_elsewhere.py tests/test_a_document_that_names_a_script_says_how_to_reach_it.py -q`; `evidence-check` on `seal/releases/*.md` and `seal/ledger.md`; `.github/scripts/rider_check.py --reverify --only agents/smith.md`; `payload-meter` before and after (C6) | |
| 4 | The 10-mutation timing both ways on one module (S11), the ledger fragment with L1–L4, the changelog fragment, `overview.md`, the phase records | Executed: the timing table with date, machine and module in the fragment; `evidence-check` on the fragment; `survivor-check --range <base>..HEAD` for the removed `tests/__pycache__` wording | |

**The order inside phase 1, because §15 decides it.** Commit at each step.

1. Write S3, S4, S7 and S8 against a script that does not exist. Seen red:
   the loader finds no file.
2. The script's replace, write, restore and verdicts; S3, S4, S7, S8 green.
3. Write S1 and S2. Seen red: the planted caches survive and S2's probe
   runs the cached module.
4. Import `clear_bytecode_cache` and set the env; S1, S2 green. Swap the
   glob for `cache_from_source`, see S1 red on the foreign tag, restore.
5. The wrapper pair; `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`
   green.
6. The xdist measurement: `bin/test <module> -q -k <cases>` three times and
   `bin/test <module> -q -k <cases> -p no:xdist` three times, wall clock each,
   written to the phase record with the module and the machine. It decides
   one sentence of phase 3's wording (`questions.md` Q1).

**Phase 3's ledger act, spelled out.** Each of the four rows (spec M9) is
opened and its claim read against the new step 4. L5 (0.6.0) is about the
mutation rule's presence and its pinning case; the case is unchanged and
the rule is still there in its two pinned sentences, so the note says what
changed around it. R8 (0.8.1), the 0.12.0 row and N1 (0.15.1) are about
other paragraphs of `## Phases` and the note says so. Then
`evidence-check --reverify --checked 2026-10-01 --ledger <file>` per file,
never a bare `--reverify` (`CLAUDE.md` §*An anchor degrades*). The rider is
read before it is re-stamped: it is about the waiver example and nothing in
step 4.

## Ledger

**Re-read and re-stamped in place** (`CLAUDE.md` §*Repo rule — a change
writes fragments*): the four rows anchored on `agents/smith.md#"## Phases"`
and `seal/releases/0.6.0.md` L5's second anchor only if the build touches
`test_the_smiths_definition_mandates_mutating_every_unit_it_added`, which
this plan does not. `seal/releases/0.15.1.md` N2 anchors `skills/verify/SKILL.md`'s
`arm-check` heading; the new section is a sibling heading, and if the hasher's
unit for a `####` runs to the next `###` the row drifts anyway — re-read it
against the insertion, where the claim holds unchanged, and re-stamp.

No row anchors a unit this plan edits in `skills/verify/scripts/arm_check.py`
(not edited) or in `tests/test_the_handoff_before_round_one.py` (not edited).

**New rows**, in `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md`,
each executed and dated by the build:

| # | Claim | Anchors |
|---|---|---|
| L1 | One mutated run removes exactly the mutated file's cached bytecode, for every interpreter tag and wherever the file lives, before the cases run and after the restore, and writes none | `mutation_check.py`'s loop unit, pinned by S1 and S2 |
| L2 | A mutated run that does not return by the bound is a `timed out` verdict, not red or survived; the file is restored; on POSIX nothing the run started survives it, and on Windows the verdict says the direct child alone was ended | the bound's unit and the strategy chooser, pinned by S5 and S6 |
| L3 | A replacement lands exactly once or nothing is written; the restore is from held bytes and hash-compared | the replace unit and the import of `restore`, pinned by S3 and S4 |
| L4 | `agents/smith.md` names `mutation-check` for the loop and names no directory to clear; the two mandating sentences are unchanged | `agents/smith.md#"## Phases"`, pinned by S9 beside the existing case |
| L5 | The per-mutation wall clock of a 10-mutation loop on one module, both ways, with date, machine and module; and the `-n auto` against `-p no:xdist` figures for a handful of cases | the measurement rows carry no anchor; they are the figure, its instrument and its moment |

## Operational impact

A plugin user gains one command on PATH, `mutation-check`, with a `.cmd`
twin. No new dependency: standard library only, and the suite installs
nothing new. No environment variable is read beyond `PYTHONPYCACHEPREFIX`,
which `clear_bytecode_cache` already honours. The process model of a mutated
run changes on POSIX — its own session — which is what makes the bound end
the whole run and what makes Ctrl-C reach it only through the parent's
`KeyboardInterrupt` handler. `arm-check` is unchanged.
