# a mutation clears one file's bytecode and ends at a timeout — questions for the planner

<!-- seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row here blocks the build.** The two tickets and the spawn left the
judgments below open, and the tree answered each of them. They are listed so
nobody reopens them, each with where its grounds are, so a reviewer can
overturn one by opening the same place. Two rows further down are a person's;
both carry a default the build takes, and a different answer changes one
constant or one README line, not the code.

## Decided from the tree

| # | Judgment | Answer | Grounds |
|---|---|---|---|
| J1 | Which mechanism closes the class — `cache_from_source` removal (#641), an mtime bump with `PYTHONDONTWRITEBYTECODE` (#129's comment), or a per-mutant `PYTHONPYCACHEPREFIX` | Remove every `<stem>.*.pyc` beside the mutated file (and under an env-set prefix mirror) after each write and each restore, and run the child with `PYTHONDONTWRITEBYTECODE=1`. That is `arm_check.py#clear_bytecode_cache` and `run_arms`'s env, reused | spec M4 and M5; plan.md §*Alternatives* C, D, E. The spelling #641 gives is tag-blind on this very machine (M2, M3): `python3` is 3.14 and the suite's `.venv` is 3.13 |
| J2 | #129's "every directory a mutated module or its importer lives in" | The mutated file's own cache only. An importer's bytecode is valid for its unchanged source; clearing it is the recompile this item removes | spec §*Scope*, out, last bullet. CPython validates a `.pyc` per source file, so only the file whose bytes changed can be stale |
| J3 | Is a script warranted, or a wording change alone | A script. The loop's three acts per mutation collapse to one command, the restore cannot be skipped or taken from `HEAD`, the bound lives in the command, and the mechanics already exist in `arm_check.py` with ledger rows behind them | plan.md §*Alternatives* A against B; spec M7 for the import |
| J4 | Where the script lives and what it reuses | `skills/verify/scripts/mutation_check.py`, importing `clear_bytecode_cache` and `restore` from `arm_check.py`; `bin/mutation-check` and `.cmd` | plan.md §*Alternatives* F and J; `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` for the pair |
| J5 | Whether the bound ends the direct child or the process group | The group, on POSIX; the direct child on Windows, with the verdict saying so | spec M6 and S5; plan.md §*Technical context*, the bound. #313 measured the hole on `arm-check`; the new command does not inherit it |
| J6 | Whether `arm-check` gets the same bound in this item | No; #313 is open and asks for that decision on purpose. The PR body names it | spec §*Scope*, out, first bullet; plan.md §*Alternatives* G |
| J7 | A timed-out run: red, survived, or neither | Neither — `timed out`, exit 2, not a verdict | spec S5 and §*Failure direction*; `run_arms` already records it as *not measured*, with the reason in the row of `seal/releases/0.9.5.md` |
| J8 | Exit codes | 0 red, 1 survived, 2 measured nothing or refused, so `&&` chains stop at the first unwatched unit | spec §*Data & interfaces*; contract §1 reads exit codes directly. `arm-check`'s report-only exit is a module-wide decision and does not transfer to one mutation |
| J9 | Whether a replacement that lands twice is applied to the first | No, refused before any write; so is one that lands nowhere | spec S3; contract §9, an edit must be able to fail |
| J10 | Whether `-p no:xdist` is prescribed for a handful of cases | Measured first, then the wording follows the figure | #641 says measure before prescribing; Q1 below |
| J11 | Whether the warden's definition changes | Not in this item | spec §*Scope*, out; the ticket names `agents/smith.md` |
| J12 | Where the changelog bullets go | `### Added` for the command, `### Changed` for the definition | spec §*What the changelog fragment says* |
| J13 | Where the pin for the new wording lives | A new case in the new module, beside `tests/test_the_handoff_before_round_one.py`'s existing case, which is not edited | spec S9; editing the existing case would drift `seal/releases/0.6.0.md` L5's second anchor for no gain |

## Rows still open

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | For a mutated run of a handful of cases, is `-p no:xdist` faster than `bin/test`'s default `-n auto`? #641 names the saving as unmeasured and says to measure before prescribing. The tree cannot answer it: it is a timing on this machine, and the framer runs no part of the suite | a measurement | Faster: `agents/smith.md`'s command example carries `-p no:xdist` and the SKILL section says why. Not faster or within noise: the example carries nothing and the phase record says what was measured | The build takes it in phase 1, step 6, three runs each way on one module, and phase 3 writes the sentence accordingly | ✅ measured 2026-10-01, `phases/phase-1.md` §*Q1, measured*: faster on a handful of fast cases (0.18 s against 0.80 s mean) and within noise on a handful taking 1.6 s, so the example carries `-p no:xdist` |
| Q2 | Should `mutation-check` be listed in `README.md`'s cheat sheet (and so in `README.ko.md`, which moves with it)? `arm-check` is not listed there today, so the tree has no precedent either way, and the cheat sheet is the owner's choice of what a person is told to type | a person — the repository owner | Listed: both READMEs gain a row, and `arm-check` probably should join it in the same edit. Not listed: the command is reachable from `agents/smith.md` and `skills/verify/SKILL.md`, which is where its reader is | Not listed. The code built is the same either way | ✅ answered 2026-10-01 by the repository owner: delegated to `smith`, which decides from the tree and records the choice and its grounds in that phase's `phases/phase-N.md`; the warden reviews it. Decided in phase 3: not listed; grounds in `phases/phase-3.md` §*Q2, decided* |
| Q3 | The command's name, the exact verdict spellings and the flag names (`--replace`, `--tests`, `--timeout`, `--cwd`) | the work | Any shape that gives one mutation per call, one literal replacement that must land exactly once, the cases' command, and a bound with `0` removing it | spec §*Data & interfaces*'s suggested shape. The phase record says what was chosen | ✅ chosen in phase 1, `phases/phase-1.md` §*Q3, the shape chosen*: the suggested shape, with four refusals beyond the count rule |
| Q4 | The default bound. `arm-check` waits 900 s per operator; the slowest ordinary mutated command in the logs is 158 s (spec M8) and the hang cost 32 m. A smith who meets the bound on a legitimately long run re-runs with `--timeout`, once | a person — the repository owner, since it is a value a person waits on | 300 s (the default taken): about twice the slowest measured legitimate run and a sixth of the hang. 900 s: one number across both loops, and a hang still costs 15 m. Another value: one constant | 300 s, overridable per call and `0` to remove | ✅ answered 2026-10-01 by the repository owner: delegated to `smith`, which decides from phase 4's timing of the 10-mutation loop (the default, 300 s, stands until then; the orchestrator recommended it) and records the choice and its grounds in that phase's `phases/phase-N.md`; the warden reviews it |
| Q5 | The per-mutation wall clock, both ways, on one module (#641's "How to verify") — is it under half the clear-all figure? The tree cannot answer it: no loop exists yet to time | a measurement | Under half: the ticket's target is met and the ledger row says by how much, with date and machine. Not under half: the row says so and the hand-back names what the remaining time is spent on | The build takes it in phase 4; the frame promises no figure | ⬜ |
