# 1788632199-the-repository-ships-no-way-to-run-its-own-suite — review round 2

| Field | Value |
|---|---|
| Target SHA | 57d7afa |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 176 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | RECORD (depth 1); test_the_section_names_the_words_the_writer_can_put_in_a_reach (depth 1); test_a_refused_environment_is_hidden_too (depth 1); test_a_directory_no_builder_can_finish_is_hidden_too (depth 1) |
| Needs a fix | yes |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round, against `57d7afa`, targeting the diff of round 1's
fixes — `61feecb..542a8b9`, three commits. It was told to stop when it found
nothing that leaves the root and nothing that crashes.

Four probes were handed over as re-checks: the work item's own module, the
`grep` showing the warden names no repository-specific command, the unscoped
ledger read, and ruff. Six claims of the fix pass were named as claims under §5,
each with the instruction to judge rather than repeat: whether the class was
enumerated at all three agent definitions and the `agents/scribe.md` exclusion
holds, whether finding 5's widening from two copies to three lost anything,
whether `ensure` is the right home for a floor check the finding located at
`#has_pytest`, **whether there is a fourth path `hide_from_git` still misses**,
which two mutations to re-run, and whether `Contract changes` names the whole of
what changed shape.

The runner handed over was the work item's own product, and the note that the
fix under review is the reason the reviewer's own definition told it how to run
a test.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The reviewing segment was left out of the class: `agents/warden.md` still said to build its own `uv` venv and named no runner | `agents/warden.md` | answered | **[executed]** mutation 6 — `warden.md` naming `bin/test` — goes red on `test_no_agent_definition_names_this_repositorys_own_command`, and `grep -c "bin/test"` is 0 in all three definitions, wider than the case's two. **[read]** the new bullet carries the generic shape, the narrow-form sentence and the link rather than a restatement, and the `uv` line survives as the branch for a repository that ships none. **[read]** `agents/scribe.md` whole: the exclusion holds |
| 🟡 2 | A failed build, and an adopted `.venv`, both leave a virtualenv with no ignore in `git status` | `.github/scripts/run_tests.py#ensure` | answered | **[executed]** mutations 3, 4 and 5 each red on their own case. All three named paths are closed and each is pinned. The enumeration is not complete — finding 10 |
| 🟡 3 | `FLOOR` is enforced when the runner builds and ignored when it adopts | `.github/scripts/run_tests.py#has_pytest` | answered | **[executed]** mutations 1 and 2 each red on their own case. **[read]** the placement in `#ensure` rather than `#has_pytest` is right, for the reason above |
| ⬜ 4 | `bin/test.cmd` drops the second half of the sentence its POSIX twin prints | `bin/test.cmd` | answered | **[read]** both files carry both sentences. **[executed]** `test_both_wrappers_say_the_same_thing_when_the_runner_is_missing` passes and carries no `skipif`, so unlike its neighbour it runs on the platform the `.cmd` twin is for |
| ⬜ 5 | A second, untraced `3.12` stands in the same section, and the `FLOOR` comment asserts a CI fact nothing pins | `CONTRIBUTING.md#"## Running the checks"` | answered | **[executed]** `test_the_section_states_the_floor_once` passes. **[read]** the surviving copy is the sentence naming `FLOOR`, and the two that went now refer back. Nothing that needed the number lost it; the CI half is read out of the workflow by a case rather than asserted in a comment. The widening from two to three was the right call |
| ⬜ 6 | Question 7 is confirmed rather than hypothetical | `seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/questions.md` | answered | **[read]** the addition states it as confirmed, carries both executed measurements with their labels, and says why no guard was built. The decision stays the owner's |
| ⬜ 7 | The record states the ignore claim without the path where it fails | `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md` | answered | **[read]** both now name all three paths in the same words. The claim they now make is what finding 10 falsifies, so the row closes and the wording reopens one path over |
| ⬜ 8 | R6 earns its row | `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md` | answered | **[read]** unchanged by the fix diff. **[executed]** the fragment reads 39 ok · 0 drifted · 0 broken |
| ⬜ 9 | The ledger is where the handover says it is | `seal/ledger.md` | answered | **[executed]** unscoped `evidence_check.py .` in a clone at `57d7afa`, exit read directly: exit 1 · 637 ok · 1 drifted · 0 broken. The single drift is `templates/config.md#"# Repository config"`, pre-existing |
| 🟡 10 | The floor refusal returns one line above the ignore, so the one adopted `.venv` the runner refuses is the one it leaves in `git status` — a fourth path, opened by this fix pass, and R2 and the changelog both claim there are three | `.github/scripts/run_tests.py#ensure` | **fixed** `e59cc9b` | fixed at e59cc9b — `` — the move, but not the one-line version the report described. Measuring first found a **second** unhidden state nobody had named: `build` returns its no-tool sentence from the `else` above its own `try`, so a `.venv` an earlier run left is never reached on a machine where `uv` is gone and `python3` is 3.9, and a call placed above the floor question does not reach it either. So the guarantee moved off a list of paths and onto `ensure`'s `finally`. The docstring deliberately carries no count — a first draft said *the four that refuse*, which was both a count and wrong; **[executed]** in a clone at `57d7afa`, in a real `git init` repository: a `.venv` with `version = 3.11.9`, an interpreter and a `pytest` script → `ensure` returns `None`, no `.gitignore` is written, `git status --porcelain` reads `?? .venv/`. The control at `version = 3.12.7` comes back hidden with empty status. **[executed]** `python3.12 -m venv` writes no `.gitignore`; **[read]** CPython added that write at 3.13, so every version this refuses is older than the one that would have covered for it. §12: the class is *every path on which a directory can exist without an ignore*, and the fix enumerated three of four while adding the fourth |
| ⬜ 11 | `Contract changes`' reach names `pytest`, which is no call site — while its enumeration is complete, `ensure`'s refusal being no new return value for `main`, which already branches on `None` | `seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/rounds/round-1.md` | answered | `pytest` is the generator's own word, not a call site: `round_record.py:753` defines `PYTEST = "pytest"` and `call_sites` appends it for any caller under `tests/`. Re-running `call_sites` at `57d7afa` returns `['build', 'ensure', 'pytest']` — round 1's cell verbatim. Editing the record would write a value the generator never produces and the next `close` would put back. What was missing is `docs/review-chain-spec.md` §*The fix surface*, which defined the reach and named none of the five values a writer can put there; two paragraphs and a case reading the three constants out of the generator, at `8ef8724` |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree, `git checkout 57d7afa` | clean tree, HEAD `57d7afa` |
| `./bin/test tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` in that clone, cold | 47 passed in 0.56 s, 2.1 s wall including the uv build; `git status --porcelain` empty afterwards — the runner hid its own `.venv` |
| Round 1's six-mutation pass, repointed at the clone, each substitution asserted before it ran | six of six RED; restored run exit 0 · 47 passed |
| A `test_tmp_*` probe in a real `git init` repository: adopted `.venv`, `version = 3.11.9`, interpreter and `pytest` script, no ignore | `ensure` → `None` with the refusal sentence; `.gitignore` not written; `git status --porcelain` → `?? .venv/`. Finding 10 |
| The same directory, control at `version = 3.12.7` | `.gitignore` written; `git status --porcelain` empty |
| `python3.12 -m venv --without-pip`, contents and `pyvenv.cfg` listed | no `.gitignore`; `version = 3.12.7`. `python3.9` and `python3.11` are not on this machine's PATH, so the below-floor builder's silence is read from CPython's history rather than executed |
| `evidence_check.py .` unscoped in the clone, exit read directly | exit 1 · 637 ok · 1 drifted · 0 broken |
| `uvx ruff check` over the runner and the test module | All checks passed |
| `grep -c "bin/test"` over all three agent definitions | 0, 0, 0 |
| Cleanup: both `test_tmp_*` scripts and the clone deleted; `git status` on the worktree | empty, HEAD still `57d7afa` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `agents/warden.md:36` | round 1's 🟡 1 — fixed |
| round-1 | `.github/scripts/run_tests.py#ensure` | round 1's 🟡 2 — fixed |
| round-1 | `.github/scripts/run_tests.py#has_pytest` | round 1's 🟡 3 — fixed |
| round-1 | `bin/test.cmd` | round 1's ⬜ 4 — fixed |
| round-1 | `CONTRIBUTING.md#"## Running the checks"` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/questions.md` | round 1's ⬜ 6 — answered |
| round-1 | `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md` | round 1's ⬜ 7 — answered |
| round-1 | `seal/ledger.md` | round 1's ⬜ 9 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a deliberate invocation of the runner out of a plugin cache needs a guard of its own | already deferred by round 1 — question 7, now recorded as confirmed | the repository owner |
| `bin/test.cmd` executed on Windows | already deferred by round 1 — `overview.md` §Not verified, alongside the five sibling pairs | the repository owner |
| A genuinely cold first call — empty `uv` wheel cache, no 3.12-or-newer interpreter | already deferred by round 1 — `overview.md` §Not verified | the first contributor on a fresh machine |
| A below-floor interpreter's `venv` built for real, rather than a hand-written `pyvenv.cfg` | this machine has neither `python3.9` nor `python3.11`; the state finding 10 needs was constructed instead | the orchestrator, if it wants the executed form |
| The full suite, repository-wide lint and typecheck | contract §2 forbids all three to me; four macOS-only #160 failures stand at this branch's base, so the gate is read against four rather than zero | the orchestrator, at the broad gate — now due |
