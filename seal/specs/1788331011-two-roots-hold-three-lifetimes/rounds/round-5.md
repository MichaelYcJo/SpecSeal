# 1788331011-two-roots-hold-three-lifetimes — review round 5

<!-- seal/specs/1788331011-two-roots-hold-three-lifetimes/rounds/round-5.md — the
verifying round the run ends on, a second time: round 4 had ended it, then
PR #90's windows leg opened 🔴 M after the record. This round opened that
fix (3796b00..cbf6a4e) and nothing needing a fix, so it does not consume the
cap. Written by the review orchestrator after the report was verified and
the broad gate ran again. -->

| Field | Value |
|---|---|
| Target SHA | e29354f (the fix diff is 3796b00..cbf6a4e; e29354f is round-4's record edit only) |
| PR | #90 |
| Broad gate | e29354f vs origin/release/v0.4.0 — `pytest tests/ -n auto` 1298 passed · 1 skipped, `ruff check .` clean, `ruff format --check .` 78 files formatted, `evidence_check.py --strict .` 222 ok · 0 drifted · 0 broken, `unverified_check.py --baseline` exit 0 (13 overviews · 28 open · 15 closed · 0 unreadable). Run again because cbf6a4e edited a test file after the 4250a71 run; the delta after this run is this record and round-4's `Fixes checked by` cell — docs-only, the non-invalidating class |
| Fixes checked by | no fixes to check |
| Contract changes | none — this round wrote no fixes |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 4-M | round-4 🔴 M (the by-hand README test ran its block through cmd.exe on the windows leg) | `tests/test_the_root_migrates_itself.py#test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set` | answered — the fix is cbf6a4e's, this round reproduced its closure | executed: both parametrizations green; a stub `bash` exiting 1 on PATH → both skipped with `exited 1 -- not a shell here`; no `bash` on PATH → both skipped with `did not run (FileNotFoundError)`; every line of both READMEs' block executed under `bash -c` one by one with its exit code and index delta read (only `rmdir specs` exits 1, the README's own "one holding something else stays" case). Read: `shlex.quote` on a forward-slashed path has the same effect as `test_evidence_check.py#step`'s unconditional quoting, by a different technique |
| ❓ N | cbf6a4e has not run on the windows leg yet — the fix's skip path is executed here against a stub, not on the runner | `overview.md` Not verified, the Windows row | out of verified scope — the next push's windows leg answers | read: the last CI runs on the branch are at 3796b00 |
| 🟢 O | the test's docstring gives `git mv … && …` as the cmd.exe example, but no README block line carries `&&` | `tests/test_the_root_migrates_itself.py` (the docstring) | nit, no fix | executed: the probe asserted `&&` in no line of either block |
| 🟢 4-fix-surface | round-4's `Contract changes: none` and `New units: none` | `rounds/round-4.md` | truthful | `shell_probe` has three callers and an unchanged signature; the diff adds no top-level definition (grep) |
| 🟢 fragment | the "What CI settled" row and the re-hashed 🟢 E row | `seal/ledger/1788331011-two-roots-hold-three-lifetimes.md` | anchors resolve | `--strict .` 222 ok · 0 drifted · 0 broken |
| 🟢 overview | the ✅ Windows and case-insensitive rows claim exactly what CI executed | `overview.md` Not verified | consistent | run 33628905815 read leg by leg with `gh`; the windows failures were the two by-hand cases only |
| carried | round-4's other verdicts (🟡 3-H, 🟢 3-I, 🟢 3-J, ❓ 1-a, ❓ 2-G, 🟢 1-10, 🟢 K, 🟢 L) | — | carried, not re-judged | the fix diff touched none of their surfaces |

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_the_root_migrates_itself.py -k by_hand` | 5 passed, both parametrizations of the target among them |
| the same with a stub `bash` (exit 1) first on PATH | 3 passed · 2 skipped, `exited 1 -- not a shell here` |
| the same with a PATH holding only a `git` link | 3 passed · 2 skipped, `did not run (FileNotFoundError) -- not a shell here` |
| a probe running each README block line under `bash -c` with rc and index delta | all 8 lines act, no `&&` in any line, `rmdir specs` alone exits 1 |
| `evidence_check.py --strict .`; the fragment alone | 222 ok · 0 drifted · 0 broken; 62 ok |
| `gh` on run 33628905815: per-leg conclusions and `--log-failed` | windows failure = the two by-hand cases only; no run after 3796b00 |
| `grep shell_probe tests/`; `git diff 3796b00..cbf6a4e -- tests \| grep '^+def'` | three callers; no new definition |
| the broad gate at e29354f (orchestrator) | see the field above |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-4 | `tests/test_the_root_migrates_itself.py#by_hand_block` and the by-hand test | the one surface CI has not yet run in its fixed form (❓ N) |
| round-3 | `hooks/root-migrate.py#main` (the order of the seven checks) | 🟢 K's asymmetry lives in the order |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ N the fixed by-hand test on the windows leg | PR #90's CI at the push that carries cbf6a4e | CI |
| 🟢 O the docstring's `&&` example | this record only | nobody — recorded |
| 🟢 K, 🟢 L | round-4's record | nobody — recorded |
