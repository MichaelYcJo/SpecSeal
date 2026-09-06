# 1788632199-the-repository-ships-no-way-to-run-its-own-suite — review round 1

| Field | Value |
|---|---|
| Target SHA | d648b2c |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 176 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | hide_from_git → build, ensure, pytest |
| New units | venv_version (depth 1); WORKFLOW (depth 1); REAL_RUN (depth 1); test_both_wrappers_say_the_same_thing_when_the_runner_is_missing (depth 1); test_an_environment_below_the_floor_is_refused (depth 1); test_an_environment_that_says_nothing_about_its_version_is_kept (depth 1); git_status (depth 1); test_a_failed_build_still_leaves_no_trace_in_git (depth 1); test_an_adopted_environment_is_hidden_too (depth 1); test_the_section_states_the_floor_once (depth 1); test_ci_runs_the_suite_at_the_floor_the_runner_holds (depth 1); test_warden_finds_the_runner_before_building_its_own (depth 1); test_no_agent_definition_names_this_repositorys_own_command (depth 1) |
| Needs a fix | yes |
| Loses a record or crashes | no |
<!-- New units: bin/test.cmd read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1, the finding round, against `d648b2c` with base `dcbf404`. Eight things
to attack, in order, the first being that this work item hands every segment a
fast way to break the rule it works under — `bin/test` runs the full suite and
contract §2 forbids that to smith and warden. Then the failure paths of
`run_tests.py`, the `.gitignore` claim, the floor's single home, the corrected
placement reason and whether question 7 stands, the Windows twin nobody has run,
the three re-stamped shared rows and the fragment's six, and whether the demoted
fallback still answers the question a newcomer arrives with.

The unscoped ledger read was named as the form to run, with the reason the
scoped form is a writer's narrowing. The runner handed over was this work item's
own product — `./bin/test tests/<file> -q` — on the grounds that reviewing the
thing by using it is part of the review.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The reviewing segment was left out of the class: `agents/smith.md` was told to find the shipped runner, `agents/warden.md` still says to build its own `uv` venv and names no runner | `agents/warden.md:36` | **fixed** `8f374c4` | fixed at 8f374c4 — `` — the warden gains *Find the runner before you build your own*, in the smith's generic shape rather than the report's paste-ready block: `agents/` is copied into every install, so a definition may not name this repository's own command. The `uv` sentence is kept as the branch for a repository that ships none. The class was enumerated at all three definitions — `agents/scribe.md` is not a member, it reads an original for facts and runs no target suite — and `test_no_agent_definition_names_this_repositorys_own_command` is parametrised over both members; **[read]** both definitions and `agents/scribe.md`; the class is two segments and the fix reached one (contract §12). This round's own prompt had to carry the incantation by hand |
| 🟡 2 | A build that fails at the install step, and a `.venv` the runner adopts, both leave a virtualenv with no ignore in `git status` | `.github/scripts/run_tests.py#ensure` | **fixed** `8f374c4` | fixed at 8f374c4 — `` — `hide_from_git` now runs on all three paths: a `try/finally` around `build`'s step loop, opening after the `else: return` so the `/nowhere/.venv` case still returns first, and a call on `ensure`'s warm path. `hide_from_git` gained `if not venv.is_dir(): return`, which is what makes the failed-build call safe when step 1 dies before a directory exists; **[executed]** in a clone at `d648b2c`: forced 3.12 fallback with a failing pip step → `IGNORE EXISTS: False`, `?? .venv/`; adopted `.venv` → `?? .venv/`. **[executed]** `python3.12 -m venv` writes no `.gitignore`. **[read]** the root `.gitignore` has no `.venv` entry |
| 🟡 3 | `FLOOR` is enforced when the runner builds and ignored when it adopts, so a below-floor `.venv` runs the suite silently | `.github/scripts/run_tests.py#has_pytest` | **fixed** `8f374c4` | fixed at 8f374c4 — `` — `venv_version` reads `pyvenv.cfg` (`uv` writes `version_info`, the standard library writes `version`), so no interpreter starts and the warm-call claim survives. `ensure` refuses below `FLOOR` with a sentence naming the version found, the floor, and what to remove. Located at `#has_pytest` and fixed in `#ensure` deliberately: `has_pytest` stays about pytest, with a docstring line saying where the floor is asked so the next reader does not add a subprocess there; **[read]** `has_pytest` checks existence only and `build:105` is the sole floor comparison; `main:170` prints the path and not the version. **[executed]** both builders record the version in `pyvenv.cfg`, so the check costs no subprocess |
| ⬜ 4 | `bin/test.cmd` drops the second half of the sentence its POSIX twin prints, on the platform with no coverage | `bin/test.cmd` | **fixed** `8f374c4` | fixed at 8f374c4 — `` — `bin/test.cmd` prints both sentences its POSIX twin prints, and the new case reads the two files and compares, so it runs on every platform unlike the `skipif(os.name == "nt")` one; **[read]** against `bin/test:29` and the five sibling pairs; `test_a_copy_without_the_runner_beside_it_says_so` is skipped on `nt` |
| ⬜ 5 | A second, untraced `3.12` stands in the same section R3 claims traces to `FLOOR`; the `FLOOR` comment also asserts a CI fact nothing pins | `CONTRIBUTING.md#"## Running the checks"` | **fixed** `8f374c4` | fixed at 8f374c4 — `` — the section stated `3.12` three times, not the two the finding named: `:23` traced to `FLOOR`, plus `:25` and `:40` untraced. Both untraced copies went, and `test_the_section_states_the_floor_once` asserts the count. The `FLOOR` comment's CI claim is now read out of `.github/workflows/test.yml` by a case rather than left asserted; **[read]** all four places stating the version; the CI matrix and ruff's target are separate facts, this one is not |
| ⬜ 6 | Question 7 is confirmed rather than refuted: from a plugin cache both of the runner's guards pass, and only the shell builtin keeps a user out | `seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/questions.md` | answered | corrected at `915b659` — question 7 was **confirmed** by round 1 rather than left hypothetical, and `questions.md` now says so with the two executed measurements. No guard was built: it would be mechanism, and it stays the owner's |
| ⬜ 7 | The record states the ignore claim without the path where it fails | `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md` | answered | corrected at `542a8b9` — the changelog fragment and R2 now say *invisible to git on every path that can leave one behind*, naming all three. R1 gained the version read, R3 four uses of `FLOOR`, R5 both carriers, and R7 is new: the floor on an adopted environment, with the `found is not None` guard written up as the tidy-up it exists against |
| ⬜ 8 | R6 earns its row | `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md` | answered | **[read]** the row is the only place the true reason and the falsified one sit together, and a false placement reason invites moving the runner rather than fixing a sentence. Its anchor resolves — the fragment reads 29 ok · 0 drifted · 0 broken |
| ⬜ 9 | The ledger is where the handover says it is | `seal/ledger.md` | answered | **[executed]** unscoped `evidence_check.py .` in the clone at `d648b2c`: exit 1, 627 ok · 1 drifted · 0 broken, the drift being `templates/config.md#"# Repository config"` and pre-existing. Re-derived rather than carried |

## Executed probes

| What was run | Result |
|---|---|
| A `test_tmp_*` probe in a `git clone --no-local` at `d648b2c` — real `python -m venv` for step 1, pip step forced non-zero, `sys` shimmed to 3.12.11 | `IGNORE EXISTS: False`, `git status --porcelain` → `?? .venv/`. Finding 2(a) |
| Same probe: `ensure` over a `.venv` holding an interpreter and a `pytest` script and no ignore | `ensure` returned the interpreter, `IGNORE EXISTS: False`, `?? .venv/`. Finding 2(b) |
| `python3.12 -m venv` and `python3.13 -m venv`, contents listed | 3.12.11 writes no `.gitignore`; 3.13.9 writes one. The floor version is the one that does not |
| `cat pyvenv.cfg` for a uv-built and a 3.12-built environment | uv 0.10.4 → `version_info = 3.13.9`; stdlib → `version = 3.12.7`. Both readable without a subprocess |
| `command -v test` and `type test` in `sh`, `bash` and `zsh`, clone's `bin/` first on `PATH` | all three: `test is a shell builtin`. The placement's corrected reason holds |
| `ls -a` on the 0.8.1 plugin cache and its `bin/` | `.github`, `bin`, `tests` all present; `bin/` holds the five earlier pairs and no `test` yet |
| `../bin/test tests/test_the_handoff_names_the_form_it_ran.py -q` from `docs/` | 6 passed in 0.01 s; the interpreter line named the clone's `.venv` |
| `./bin/test … -k nosuchtest_zzz` | exit 5 — pytest's own code, not swallowed |
| `./bin/test` cold in a fresh clone | 3.27 s wall including the uv build; warm calls under a second |
| `evidence_check.py .` unscoped, exit read directly | exit 1 · 627 ok · 1 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a deliberate invocation of the runner out of a plugin cache needs a guard of its own | `questions.md` question 7, raised in phase 2 and confirmed rather than closed by this round | the repository owner |
| `bin/test.cmd` executed on Windows — path resolution, `py -3` preference, exit code | `overview.md` §Not verified; the five sibling pairs stand in the same state and closing it is a change to CI | the repository owner |
| A genuinely cold first call — empty `uv` wheel cache, no 3.12-or-newer interpreter | `overview.md` §Not verified | the first contributor on a fresh machine |
| The full suite, repository-wide lint and typecheck | contract §2 forbids all three to me; `plan.md` records four macOS-only #160 failures at this branch's base, so the gate is read against four rather than zero | the orchestrator, at the broad gate |
