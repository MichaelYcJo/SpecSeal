# Implementation Plan: arm-check reads a run that measured nothing as a kill

<!-- seal/specs/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-10-01 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

Two fixes in `skills/verify/scripts/arm_check.py`, one file of cases, and
the records. First, `run_arms` runs `--tests` once against the module as it
is before writing any mutation, and a run that is not green — a non-zero
exit, a timeout, a spawn failure — raises `NoBaseline`, which `main` prints
as `no baseline: …` with the command's output and exits 2. Second,
`clear_bytecode_cache` takes the cases' working directory and joins a
relative `PYTHONPYCACHEPREFIX` to it, so the mirror it clears is the mirror
the cases read. Every sentence that describes the run changes in the same
commit as the behaviour, and every new case is seen red against `a340221b`.

## Technical context

**The loop** — `arm_check.py#run_arms` (`:824-950`). The module is read and
hashed (`:861-863`), arms enumerated (`:865`), `env` built with
`PYTHONDONTWRITEBYTECODE=1` (`:872-873`). The loop writes a mutation
(`:887-888`), clears the cache (`:889`), runs `tests` (`:891-898`) and
records `run.returncode != 0` (`:899`); `TimeoutExpired` and `OSError` go
to `not_applicable` (`:900-915`); the `finally` restores and clears
(`:916-918`). The baseline goes between `:873` and the `try` at `:877`:
clear, run, judge, raise. Nothing has been written at that point, so no
restore is owed on the raise.

**The exit** — `arm_check.py#main` (`:1067-1141`). The one refusal today is
the `--timeout` guard (`:1098-1111`), exit 2 through `parser.error`. The
`run_arms` call is at `:1127-1134`; `NoBaseline` is caught around it, the
verdict line and the output printed through `echo`, and 2 returned. The
report-only comment (`:1137-1141`) stays true and should say so: exit 0 is
for a **measured** run.

**The cache** — `arm_check.py#clear_bytecode_cache` (`:758-799`). The
prefix is read at `:784-786`, the mirror built at `:788-790` as
`os.path.join(prefix, tail.lstrip(os.sep).lstrip("/"))`. The fix: when
`prefix` is relative, `prefix = os.path.join(cwd or os.getcwd(), prefix)`
before the join (spec M1 is why `cwd`). Three call sites in `run_arms`
(`:889`, `:917`, and the new baseline's) pass `cwd=cwd`.

**The cases** — `tests/test_arm_check.py`. The fixture `two_arms`
(`:689-695`) returns the module and `[sys.executable, probe, module]`; every
new case uses that shape, because the CI grammar legs install pytest alone.
`SEES_CACHE` (`:1085-1097`) is the probe that logs whether a cache exists at
run time; S9 wants a variant that looks under the prefix mirror. The five
cases spec M5 names are at `:1098-1148` (cache observation, `len(seen) == 4`),
`:1150-1187` (restore, `len(ran) == 1`), `:1274-1304` (never returns),
`:1306-1348` (spawn failure, third of four calls), `:1351-1416`
(`NO_VERDICT_COMMANDS` and the report case), `:1489-1543` (second call times
out). The report-only pin is `:1024-1047` and is not touched. The help pin
is `:1419-1452`: its two phrases are matched on a whitespace-folded,
lower-cased `--help`, so the help may gain words and may not lose those.

**The texts** — `skills/verify/SKILL.md`, the `arm-check` section's last
paragraph (*Two things it does not claim …*); `bin/arm-check` lines 12–15;
`run_arms`'s docstring; the `--timeout` help at `arm_check.py:1090-1094`.

**Constraints the tree states.** `arm_check.py` loads on 3.9 (its own
comment at `_node_arms`; `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR`
sweeps for `strict=` and `.UTC`), so no `zip(strict=)`, no `.UTC`, no
`match`; `tests/test_release_hygiene.py` refuses a three-part version token
in a loaded file. Ruff is the repository's lint (`seal/config.md` row
*Broad gate*), run narrowly on the touched `.py` files at each phase, never
the whole gate.

**What breaks in six months, and the trade.** A `--tests` whose suite is
flaky at the baseline refuses a run that would have measured; the cost is
one re-run with the cause printed. A suite that approaches the bound now
meets it once more per invocation, in the baseline, before anything is
written — which is the right place to meet it and why S4 pins that the
bound is there. And three files are edited on this branch and on #641's at
once (spec M7); whichever squashes second resolves three small hunks, one of
them inside a ledger row that both re-stamp, hunk by hunk.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. One baseline run per `run_arms` call before any write; `NoBaseline` raised with the cause and the output; `main` prints `no baseline: …` and exits 2; `clear_bytecode_cache(path, cwd=None)` joins a relative prefix to `cwd`** | A flaky suite refuses a run it would have measured: one re-run, cause printed. The baseline adds one run per invocation. A hang now lands in the baseline, under the same bound, before anything is written (S4 pins the bound). Three files conflict with #641 at the merge (M7) | **Chosen** |
| B. Read pytest's exit codes: treat 4 and 5 as *measured nothing*, keep reading 1 as a kill | `--tests` is any command, not pytest; and exit 1 from a case that already fails is byte-identical to exit 1 from a kill. #641's round 1 rejected the same list for the same reason: *the fix is not a list of pytest codes, it is a baseline* | Rejected |
| C. A baseline before every arm, not once per call | The module is unchanged between arms, so run 2 through run 32 measure what run 1 measured. On `hooks/review-history-guard.py` that is 32 more runs of `tests/test_chain_hooks.py` under a 900 s bound each | Rejected: one run answers the question |
| D. Run the baseline, and on a non-green result continue, filing every arm under *no verdict* with the baseline's reason | The whole run is spent — 61 commands on the real module — to print a report that measured nothing. The `--timeout` guard already refuses at parse time for exactly this reason: *there is no reading of a negative bound that is worth running* | Rejected |
| E. `run_arms` returns a third value instead of raising | Every existing caller unpacks two values; a third a caller ignores is a run that measured nothing read as one that did — the defect one level up. Raising cannot be ignored | Rejected |
| F. Exit 0 on `no baseline`, keeping *report-only, exit 0 either way* literally true | A `&&` chain and a script reading `$?` both read 0 as *ran fine*. The command already exits 2 for a run it refused before measuring (`--timeout -1`), so 2 is the existing meaning, and the survivor sentence is about a survivor | Rejected |
| G. A different verdict word for `arm-check` than `mutation-check`'s `no baseline` | Two commands in one SKILL file saying the same fact in two words is a second convention for one thing, which `tests/test_one_word_one_meaning.py` exists to refuse. The fact is the same: the cases are not green against the unmutated file, so nothing was written | Rejected |
| H. Split the baseline's outcomes into `no baseline` (non-zero exit) and `timed out` / `could not start` (as `mutation-check` does) | `arm-check` has no run-level verdict vocabulary: a timeout and a spawn failure are per-pair *reasons* in the report, not verdicts. One refusal with the cause named in the reason is the shape the rest of its output already has | Rejected for `arm-check`; the cause is still named, which is what the split bought |
| I. `clear_bytecode_cache` does `os.chdir(cwd)` around the join | Process-global state in a function `mutation_check.py` imports by path; a raise between the two `chdir`s leaves the caller somewhere else | Rejected |
| J. Document that a relative prefix is unsupported | The stale `.pyc` still sits where the cases read it, and the function's whole reason to exist (the 0.9.5 row) is that no hash catches that | Rejected |
| K. Pass `cwd` through a module global set by `run_arms` | Hidden coupling; `mutation_check.py` binds the function and never sets the global, so its mirror would silently differ from `arm-check`'s | Rejected: a parameter is visible at the call site |
| L. Skip the baseline when the module has no arms | Saves one run on a module nobody runs the command against, and costs a second rule to state in the SKILL section and the help. *Runs once per `--tests` call* is one sentence | Rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.
Rows kept for the ledger fragment are written at the phase boundary that
produced them, and ride that phase's closing commit.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The baseline.** `NoBaseline`; the run in `run_arms` before any write, under `timeout`, after a cache clear; `main` prints `no baseline: <cause> … Nothing was written and no arm was measured.` then the output, exit 2. New cases S1–S3 (parametrised exit 5 / 4 / 1 plus an import-shaped failure), S4 (the bound), S5 (cannot spawn), S6 (five calls, the first before any write), each seen red against `a340221b`'s script, the hand-back saying how. The five shifted cases (spec M5) rewritten keeping every assertion. The texts of spec §Scope 3 made true in the same commit: `run_arms` docstring, `--timeout` help (S8's help case extended), `bin/arm-check` header, the SKILL section's closing paragraph. S7 untouched and green | `tests/test_arm_check.py -q -p no:xdist` (narrow); `uvx ruff check` and `uvx ruff format --check` on the touched `.py` files | |
| 2 | **The prefix.** `clear_bytecode_cache(path, cwd=None)` joining a relative prefix to `cwd`; `run_arms` passing `cwd=cwd` at all three sites; the docstring saying which directory a relative prefix is read against and citing `cache_from_source`. S9 parametrised over a relative and an absolute prefix, the relative parameter seen red against `a340221b`. The absolute parameter is green today and stays | `tests/test_arm_check.py -q -p no:xdist` (narrow), with `PYTHONPYCACHEPREFIX` set only inside the case's child environment; `tests/test_a_script_says_which_interpreter_it_needs.py` and `tests/test_release_hygiene.py` (S10's syntax half) | |
| 3 | **The records.** The ledger fragment with at least three rows — the baseline (R1), the baseline's bound (R2), the prefix (R3) — each `executed`, dated, naming how red was seen; the changelog fragment under `### Fixed`; the three release rows spec M6 names re-read against the edit, their claims corrected in place where the edit made one false, re-stamped with a dated note; `bin/evidence-check` green on `seal/releases/*.md`, `seal/ledger.md` and the fragment; `overview.md` closed with S11 in `## Not verified` naming its answerer | `bin/evidence-check`; `tests/test_arm_check.py` once more after the records (nothing in them changes code, so this is the narrow run at the boundary and not a broad one) | |

**The order inside phase 1, because §15 decides it.** Commit at each step.

1. Write S1–S6 against the script as it stands and run the module: S1–S3
   red on `killed` beside both arms and exit 0; S4 red on two refused arms
   and no exception; S5 red on two arms in the no-verdict list; S6 red on
   four calls.
2. Add `NoBaseline`, the baseline run, and `main`'s arm. S1–S6 green; the
   five shifted cases now red on their counts — that is the expected shift,
   not a regression.
3. Rewrite the five shifted cases (spec §Scope 5). The module green.
4. Delete the baseline's `timeout=timeout` and watch S4 go red; restore it.
   Move the baseline after the first write and watch S6 go red; restore it.
   Say both in the hand-back.
5. The texts, with the help case extended. The module green. One commit
   with the behaviour, or the behaviour's commit amended before it is
   handed on — §14 is *the same commit*.

**Phase 2 is independent of phase 1 in code and ordered after it in the
plan**, because its `run_arms` edit (three `cwd=cwd` arguments) lands on the
loop phase 1 just changed, and because the S9 probe follows `SEES_CACHE`'s
shape, which phase 1's rewrite of the cache-observation case already
touched. Doing them in this order keeps each diff about one thing.

## Ledger

New rows go in
`seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md`,
no header. Anchors are `path#unit@hash`; the builder takes the hashes with
`evidence-check` after the edit and does not type them.

| Row | Claim | Anchors (the units) |
|---|---|---|
| R1 | A `--tests` that is not green against the unmutated module refuses the run as `no baseline`, exit 2, before anything is written; a non-zero exit, a timeout at the bound and a spawn failure are the three ways, each named in the reason | `arm_check.py#NoBaseline`, `#run_arms`, `#main`; the S1–S3 and S5 cases |
| R2 | The baseline's run is bounded by `--timeout` exactly as an operator's is, and a baseline that hangs is `no baseline` within the bound | `#run_arms`; the S4 case |
| R3 | A relative `PYTHONPYCACHEPREFIX` is resolved against the cases' working directory, so the mirror cleared is the mirror the cases read; an absolute prefix is unchanged | `#clear_bytecode_cache`; the S9 case |

Rows that drift and are re-read in place, never re-pointed: `seal/releases/0.9.5.md`
the `clear_bytecode_cache` row (its anchor and its test anchor both move;
its claim *clearing the cache around every mutation* gains the baseline and
the directory) and the `run_arms` row (its anchor and two test anchors move;
its narrative about *the third of four calls* is now the fourth of five, so
the note says so); `seal/releases/0.15.1.md` N2 (the SKILL heading's hash
moves if the heading is touched — it should not be; `run_arms`'s does; the
claim about the bound holds and gains that the bound covers the baseline).
`CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not
re-pointed* does not apply: no anchor is removed.

## Operational impact

- **No new dependency, no new environment variable, no CLI flag change.**
  Exit 2 gains a second meaning beside the usage error it already carried:
  a run refused before measuring. Exit 0 is unchanged for every measured
  run.
- **One more run of `--tests` per invocation**, bounded by `--timeout`. On
  `hooks/review-history-guard.py` against `tests/test_chain_hooks.py` that is
  one suite run added to 61; the figure for the ledger row is
  `questions.md` Q3's measurement.
- **`mutation_check.py` (#641's branch, PR #698, unmerged) binds
  `clear_bytecode_cache` and `restore` from `arm_check.py` by path.** The
  new keyword parameter defaults to today's behaviour, so its three
  `clear_bytecode_cache(path)` calls keep working unchanged when both
  branches are on `release/v0.17.0` (S11, verifiable only there). Its own
  instance of the relative-prefix defect — #641's ⬜ 7, recorded in its
  `overview.md` §*Not verified* — closes only when those three calls pass
  `cwd=cwd`, a one-line change that belongs to whichever branch lands second
  (`questions.md` Q1).
- **Three files are edited on both branches** (spec M7): the two cache cases
  in `tests/test_arm_check.py` (#641 adds a `monkeypatch` line in each; this
  item changes one of them for the baseline count), the SKILL section's
  closing paragraph (#641 inserts its `mutation-check` section immediately
  after it), and the `clear_bytecode_cache` row of `seal/releases/0.9.5.md`
  (both re-stamp it). Resolve hunk by hunk, both sides read, and run
  `evidence-check` after the resolution (`CLAUDE.md` §*When a ledger file
  conflicts*). Never `--ours` or `--theirs`.
- **CI**: the two `arm-check-grammar` legs run the touched module on 3.13
  and 3.14 with pytest alone, so every new case has to pass there; S10 is
  the pull request's to show.
