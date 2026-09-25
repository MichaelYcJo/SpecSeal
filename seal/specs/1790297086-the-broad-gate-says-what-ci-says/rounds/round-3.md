# 1790297086-the-broad-gate-says-what-ci-says — review round 3

| Field | Value |
|---|---|
| Target SHA | bf43c02558e6f18320bbff135601428e665013a7 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 607 |
| Broad gate | 5c5f97da against e04b9c9c; earlier run: 5c08b8bd against 7b557144 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790297086 is the verifying round after the run's one reopening. It reads round 2's fixes (bafaede2..174ad801) at bf43c025 and ends the run whatever it finds. It asks whether as_cmd_expands closes the %CD% finding in both directions, whether the comment and survivors corrections are true, whether M1's case now runs rather than skips on the windows leg, and whether PR #607's CI is green at that tip.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | an environment `CD` wins over the computed one, as `cmd.exe` does, and no case pins that order: with the two branches swapped the module stays green | `skills/verify/scripts/broad_gate.py:1286` | deferred #616 | executed: the swap left `96 passed, 1 skipped`; the orchestrator files the issue and is its answerer. The unit is one the run's own fixes created, so it is the branch's if the orchestrator reads the cap that way |
| ⬜ 2 | `as_cmd_expands`'s docstring says it replaces names "the way `cmd /c` replaces it", but the regex leaves `%NAME:~n,m%` and `%NAME:a=b%` as written, and (read, not executed) may resume its scan at a different `%` than `cmd.exe` after an undefined name | `skills/verify/scripts/broad_gate.py:1271` | deferred #616 | executed on macOS: `%CD:~0,2%` and `%T:repo=bin%` come back as written; the resume point is unverified and needs a Windows run. The miss only leaves a row as written. The orchestrator files the issue and is its answerer |
| 🟢 | round 2's finding 1 is closed — `%CD%` and `%__CD__%` name the row's directory in any case; `$NAME`, `%%` and an unset `%NAME%` stay as written | `skills/verify/scripts/broad_gate.py:1271` | verified | executed: fourteen inputs through the helper and `handed_to_shell`, and five mutations, each `1 failed` |
| 🟢 | round 2's note 2 is closed — `gate`'s comment names `moved_line` and `skipped_at_main` | `skills/verify/scripts/broad_gate.py:2211` | verified | read: `:444`, `:466`, `:2265`; the refusal at `:2223` quotes the spelling, the read R2's notes already set apart |
| 🟢 | round 2's note 3 is closed — the survivors row places R2 at row 9 | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md:10` | verified | read: line 9 of `seal/releases/0.12.2.md` is R2 |
| 🟢 | M1 in the code — the real-platform case fails, not skips, on Windows where the shell is not `cmd.exe` | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:568` | verified | executed with the branch forced: `AssertionError` under `nt`, skip under `posix`; read: the windows leg at `bf43c025` green, `4732 passed, 45 skipped`, so the case ran and passed there |
| 🟢 | the fix pass's correction to `seal/releases/0.12.2.md` R2 is true | `seal/releases/0.12.2.md:9` | verified | read: two consumers of `base.given`; `moved_line` since 4edc99bb, 2026-09-21; executed: `evidence_check.py --strict .` exit 0 |
| 🟢 | the new `survivors.md` row excuses a sentence that holds | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md:11` | verified | read: `run` passes `windows` and `comspec` at `broad_gate.py:1220`; executed: survivor check over the fix range, exit 1 without and 0 with the exemptions |

## Paste-ready fixes

```python
# tests/test_the_gate_hands_cmd_a_path_it_can_run.py — at the end of
# test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points
    # cmd.exe lets a defined `CD` override the one it computes (`set /?`),
    # so the environment is asked first (round 3, note 1).
    monkeypatch.setenv("CD", os.path.join(tree, "nowhere"))
    got = gate.handed_to_shell("%CD%/bin/test -q", windows=True, comspec=CMD, root=tree)
    assert got == "%CD%/bin/test -q", got
```
```text
skills/verify/scripts/broad_gate.py, as_cmd_expands's docstring (round 3,
note 2) — after "Any other name is left as written, as `cmd /c` leaves an
undefined one, and so is `%%`." add:

A substring or substitution (`%NAME:~0,2%`, `%NAME:a=b%`) is not modelled
and is left as written too, so a name that starts with one keeps its `/`.
```

## Executed probes

| What was run | Result |
|---|---|
| `as_cmd_expands` over `%NOPE%`, `%cd%`, `%Cd%`, `a%CD%b`, `%CD%bin`, `%F%` (a file), `%%`, `%%CD%%`, `%NOPE%CD%`, `%CD:~0,2%`, `%T:repo=bin%`, `%__cd__%`, with `CD`, `__CD__`, `NOPE` unset | as written; directory; directory; `a`+directory+`b`; directory+`bin`; the file's path; `%%`; `%`+directory+`%`; as written; as written; as written; directory plus separator |
| `handed_to_shell(windows=True)` over eight rows, then `%CD%/bin/test` with `CD` set to a missing path | `%cd%`, `%T%` and `%__CD__%bin` rewritten; `%NOPE%`, `a%CD%`, `%F%`, `%CD%bin`, `%CD:~0,2%` as written; with `CD` set, as written (environment first) |
| Six mutations of `as_cmd_expands`, each alone from saved bytes, the module run each time | five `1 failed, 56 passed` (`-x`); the order swap `96 passed, 1 skipped`; restored `96 passed, 1 skipped`, tree clean |
| The real-platform case with `runs_under_cmd_exe` forced false, `os.name` as `nt` then `posix` | `AssertionError` naming M1; skip |
| `survivor_check.py` over `bafaede2...174ad801`, without and with `survivors.md` | exit 1, one place (`broad_gate.py:1214`); exit 0, one `exempt` |
| `survivor_check.py` over `origin/release/v0.15.4...HEAD` with `survivors.md` | exit 0, three `exempt` |
| `evidence_check.py --strict .` | exit 0 |
| CI `release` at `bf43c025` (read) | failure at *a declared review chain has the round record it claimed*: `Pass` checked beside `Fixes checked by: nobody`, the state round 2's record is in until this round's record names it. Not a finding |
| CI lint, ledger, ubuntu at `bf43c025` (read) | lint and ledger pass; ubuntu `4764 passed, 13 skipped` |
| CI windows and macOS at `bf43c025` (read, run 36088528007) | windows `4732 passed, 45 skipped`, no failure, the same counts as at `5b236208` (the fix range added rows and an assert, no case); macOS `4767 passed, 10 skipped` |
| The broad gate (full suite, lint, typecheck through `broad-gate`) | not yet. Nothing in this round ran it. It is the sealer's, and with nothing here needing a fix, the sealer's spawn is what comes due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/releases/0.15.3.md:60` | round 1's 🔴 1 — fixed |
| round-1 | `tests/test_the_gate_names_every_step_ci_runs.py:885` | round 1's 🔴 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1306` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2175` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/releases/0.12.2.md` | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:1841` | round 1's ⬜ 6 — answered |
| round-1 | `tests/conftest.py:48` | round 1's ⬜ 7 — fixed |
| round-1 | `agents/sealer.md:71` | round 1's ⬜ 8 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1491` | round 1's ⬜ 9 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1220` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.12.2.md:39` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_gate_names_every_step_ci_runs.py` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | round 1's ❓ — out of verified scope |
| round-2 | `skills/verify/scripts/broad_gate.py:1313` | round 2's 🟡 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2187` | round 2's ⬜ 2 — fixed |
| round-2 | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md:10` | round 2's ⬜ 3 — answered |
| round-2 | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md` | round 2's 🟢 — verified |
| round-2 | `tests/test_the_gate_names_every_step_ci_runs.py:889` | round 2's 🟢 — verified |
| round-2 | `seal/releases/0.12.2.md:9` | round 2's 🟢 — verified |
| round-2 | `skills/verify/scripts/broad_gate.py:1864` | round 2's 🟢 — verified |
| round-2 | `tests/conftest.py:75` | round 2's 🟢 — verified |
| round-2 | `agents/sealer.md:88` | round 2's 🟢 — verified |
| round-2 | `skills/verify/scripts/broad_gate.py:1453` | round 2's 🟢 — verified |
| round-2 | `tests/test_the_gate_names_every_step_ci_runs.py:965` | round 2's 🟢 — verified |
| round-2 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:538` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — no case pins that an environment `CD` wins over the computed one | a new issue, filed by the orchestrator (no open issue holds `cmd.exe` expansion; #596 closes with this pull request) | the orchestrator files it; whoever next edits `as_cmd_expands` plants the row |
| ⬜ 2 — `as_cmd_expands` models `%NAME%` alone, and says it models `cmd /c` | the same new issue | the orchestrator files it; a Windows run answers the resume point |
