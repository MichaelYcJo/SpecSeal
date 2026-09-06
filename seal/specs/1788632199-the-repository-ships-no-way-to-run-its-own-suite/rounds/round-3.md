# 1788632199-the-repository-ships-no-way-to-run-its-own-suite — review round 3

| Field | Value |
|---|---|
| Target SHA | 60352fd |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 176 |
| Broad gate | 60352fd, against dcbf404 — 2337 passed, 2 skipped, 4 failed: the four macOS export cases of #160, identical at the base. `uvx ruff check .` and `format --check .` clean over 108 files |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | yes — an unwritable `.venv` makes `ensure` raise `PermissionError` out of `main` instead of returning its refusal sentence (🟡 12). No record is lost, and the sentence the reader needs still prints before the traceback. The run is capped, so it leaves as issue #177 rather than as a fix pass — `docs/review-chain-spec.md`'s stated trade, *a defect the second reopening would have found ships as an issue rather than as a round* |

- [x] Pass

## What this round was asked

Round 3, a verifying round, against `60352fd`, targeting the diff of round 2's
fixes — `2b7eea4..6f71064`. It was told the run had already been reopened once,
so the bar was the floor rather than a hunt.

Three probes were handed over as re-checks and four claims of the fix pass were
named as claims under §5, each with the instruction to judge rather than
repeat: whether `ensure` is really the only route to a virtualenv given `main`
and both wrappers; whether `docs/review-chain-spec.md` is the right home for the
reach vocabulary and whether the case reading the generator's constants rots
loudly; whether `build`'s retained `finally` is dead code, a second guarantee or
a finding; and the whole-file revert to `2b7eea4`, which the fix pass offered as
the real demonstration after disclosing that its own mutation anchor had matched
`build` first and left `ensure`'s guarantee unpinned in one pass.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The reviewing segment was left out of the class | `agents/warden.md` | answered | carried from round 2 — the fix diff does not touch `agents/` |
| 🟡 2 | A failed build, and an adopted `.venv`, both leave a virtualenv with no ignore | `.github/scripts/run_tests.py#ensure` | answered | re-derived: this diff rewrote `ensure`. **[executed]** all four git-hiding cases green, and the whole-file revert takes only the two new ones red, so round 1's two still pin what they pinned |
| 🟡 3 | `FLOOR` is enforced when the runner builds and ignored when it adopts | `.github/scripts/run_tests.py#has_pytest` | answered | re-derived. **[executed]** the floor question is unmoved inside `ensure`'s new `try`, and the refusal still returns `None` with its sentence |
| ⬜ 4 | `bin/test.cmd` drops the second half of its POSIX twin's sentence | `bin/test.cmd` | answered | carried from round 2 — untouched by the fix diff |
| ⬜ 5 | A second, untraced `3.12` stands in the same section | `CONTRIBUTING.md#"## Running the checks"` | answered | carried from round 2 — untouched by the fix diff |
| ⬜ 6 | Question 7 is confirmed rather than hypothetical | `seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/questions.md` | answered | carried from round 2 — untouched by the fix diff |
| ⬜ 7 | The record states the ignore claim without the path where it fails | `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md` | answered | re-derived: this diff rewrote R2 a second time. **[read]** R2 now claims every exit of `ensure` rather than a list, which is what I confirmed structurally. One gap stands, and it is 🟡 12's |
| ⬜ 8 | R6 earns its row | `seal/ledger/1788632199-the-repository-ships-no-way-to-run-its-own-suite.md` | answered | carried. **[executed]** the fragment reads 44 ok · 0 drifted · 0 broken |
| ⬜ 9 | The ledger is where the handover says it is | `seal/ledger.md` | answered | re-derived: this diff re-stamped one row. **[executed]** unscoped read in a clone at `60352fd`, exit read directly: exit 1 · 642 ok · 1 drifted · 0 broken, the drift pre-existing. **[read]** the re-stamped row names this change and says the stamp was scoped |
| 🟡 10 | The floor refusal returned one line above the ignore — a fourth path | `.github/scripts/run_tests.py#ensure` | answered | **closed.** **[executed]** the whole-file revert takes exactly the two new cases red and nothing else (§15). **[executed]** the reviewer's one-line fix, rebuilt, leaves the fourth case red — the pass's reason for taking the resolution and not the fix is correct rather than merely stated. **[read + executed]** `ensure` is the only route to a virtualenv. A second defect stands on the same function, opened by this fix — 🟡 12 |
| ⬜ 11 | `Contract changes`' reach names `pytest`, which is no call site | `seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/rounds/round-1.md` | answered | **closed, and the refusal was right.** **[read]** `round_record.py:752-754` and `call_sites:1044-1045`; editing the record would write a value `close` puts back. **[executed]** three mutations each take the new case red. One limit — ⬜ 13 |
| 🟡 12 | `hide_from_git`'s unguarded write turns `ensure`'s new `finally` into a traceback on a `.venv` the process cannot write, on the two exits where a sentence is the whole product | `.github/scripts/run_tests.py#hide_from_git` | deferred #177 | **[executed]** a probe on both SHAs: at `2b7eea4` the below-floor refusal over a `chmod 555` `.venv` returned `None` and only the warm success path raised; at `60352fd` both raise `PermissionError`. Pre-existing on one exit, widened onto the refusals by this fix. The run is capped, so it leaves as an issue |
| ⬜ 13 | The reach-vocabulary case pins three words rather than the set | `tests/test_the_fixes_name_their_surface.py` | deferred #177 | **[executed]** the three loud paths all measured red. **[read]** nothing in the case notices a fourth branch appearing in `call_sites`. The document is correct today, so nothing ships broken |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree at `60352fd`, venv built by `./bin/test` itself | clean tree, cold build 2.1 s wall |
| `./bin/test` over the two changed test modules, exit read directly | exit 0 · 83 passed |
| `git checkout 2b7eea4 -- .github/scripts/run_tests.py`, then the runner module | exit 1 · 2 failed, 47 passed — exactly the two new cases; round 1's two green |
| `git checkout 2b7eea4 -- docs/review-chain-spec.md`, then the surface module | exit 1 · 1 failed — the new reach-vocabulary case |
| `PYTEST_ONLY` value changed in the clone's `round_record.py`, substitution asserted | exit 1 · 1 failed — the constants are pinned by value, not only by name |
| The reviewer's one-line fix rebuilt on the target, three substitutions asserted, the four git-hiding cases | exit 1 · 1 failed, 3 passed — only `test_a_directory_no_builder_can_finish_is_hidden_too` |
| `git grep` for every call of `ensure`, `build` and `hide_from_git` over tracked `.py`, `.yml` and `bin/` | one `ensure(` at `main:258`, one `build(` at `ensure:231`. No other producer of a virtualenv |
| A `test_tmp_*` probe: adopted `.venv` at `version = 3.11.9` and one at the floor, `chmod 555`, `ensure` called on each, at both SHAs | `60352fd`: both raise `PermissionError` on `.venv/.gitignore`. `2b7eea4`: the refusal returned `None`, the success path raised. Finding 12 |
| `evidence_check.py .` unscoped in the clone, exit read directly | exit 1 · 642 ok · 1 drifted · 0 broken; the fragment 44 ok · 0 drifted |
| Every test module that reads `docs/review-chain-spec.md` — 16 files | exit 0 · 681 passed, 1 skipped in 113.89 s. The doc edit breaks no other reader |
| Cleanup: probe deleted, clone removed, `git status` on the worktree | empty, HEAD still `60352fd` |

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
| round-2 | `agents/warden.md` | round 2's 🟡 1 — answered |
| round-2 | `seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/rounds/round-1.md` | round 2's ⬜ 11 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 12 — the unguarded `.gitignore` write | **issue #177**, opened by the orchestrator after reproducing it, milestone 0.8.3. The run is capped, so a finding this round opens becomes an issue rather than a fix pass | the repository owner |
| ⬜ 13 — the reach-vocabulary case's blind spot | **issue #177**, its second half | the repository owner |
| Whether a deliberate invocation of the runner out of a plugin cache needs a guard | already deferred by round 1 — question 7, recorded as confirmed | the repository owner |
| `bin/test.cmd` executed on Windows | already deferred by round 1 — `overview.md` §Not verified, alongside the five sibling pairs | the repository owner |
| A genuinely cold first call — empty `uv` wheel cache, no 3.12-or-newer interpreter | already deferred by round 1 — `overview.md` §Not verified | the first contributor on a fresh machine |
| A below-floor interpreter's `venv` built for real | already deferred by round 2 — this machine has neither `python3.9` nor `python3.11`, so the state was constructed again | the orchestrator, if it wants the executed form |
