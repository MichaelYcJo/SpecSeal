# 1790297086-the-broad-gate-says-what-ci-says — round 3 report

Round 3 is the verifying round after the run's one reopening, over round 2's
fix range `bafaede2..174ad801` (7 commits) at target `bf43c025`. The run is
capped: this record ends it whatever it finds, so what it opens is written as
a `deferred <home>` candidate and not as a fix to commission.

The work was done in a `git clone --no-local` at `bf43c025` under the
session's scratchpad (`item-d/round-3/clone`); nothing was written in the
worktree except this file.

## Summary

- Round 2's finding 1 (fix or justify) is closed. `as_cmd_expands` resolves
  `%CD%` and `%__CD__%`, in any case, to the directory the row runs in, and
  leaves `$NAME`, `%%` and an unset `%NAME%` as written. Executed below, both
  directions.
- Round 2's notes 2 and 3 are closed, read.
- M1 is closed. The real-platform case now fails, not skips, where
  `os.name == "nt"` and the shell is not `cmd.exe`, executed by forcing that
  branch. The windows leg is green at this tip, so the case ran there and
  `where/q cmd` exited 0 under `cmd.exe`.
- The fix pass's extra correction to `seal/releases/0.12.2.md` R2 and its new
  `survivors.md` row are both true, read and executed.
- Two new notes, both inside `as_cmd_expands`, neither a defect a release
  would ship: one mutation of the new unit survives the module (⬜ 1), and the
  docstring claims more of `cmd.exe`'s expansion than the regex models (⬜ 2).

## Round 2's finding 1 — `%CD%` is resolved, and only `%NAME%` is expanded

Claimed by the fix pass (f68c61fe): `%CD%` and `%__CD__%` name the directory
the row runs in, a name in the environment takes its value, anything else is
left as written, and `$NAME` and `%%` mean nothing.

Found, executed through `as_cmd_expands` and `handed_to_shell(windows=True)`
with `CD`, `__CD__` and `NOPE` unset (`broad_gate.py:1271`):

| Input | `as_cmd_expands` | `handed_to_shell` row → handed |
|---|---|---|
| `%NOPE%` (unset) | `%NOPE%` | `%NOPE%/bin/test` → as written |
| `%cd%`, `%Cd%` | the row's directory | `%cd%/bin/test` → `%cd%\bin\test` |
| `%__cd__%` | the row's directory plus a separator | `%__CD__%bin/test` → `%__CD__%bin\test` |
| `a%CD%b` (in the middle of a name) | `a` + directory + `b` | `a%CD%/bin/test` → as written |
| `%CD%bin` | directory + `bin` (not a directory) | `%CD%bin/test` → as written |
| `%F%`, `F` naming a file | the file's path | `%F%/x` → as written |
| `%T%`, `T` naming the tree | the tree | `%T%/bin/test` → `%T%\bin\test` |
| `%%` | `%%` | — |
| `%%CD%%` | `%` + directory + `%` | — |
| `CD` set in the environment to a missing path | the environment's value | `%CD%/bin/test` → as written |

Every row matches `cmd.exe`'s documented reading. The last row is the
documented override: `set /?` says a defined variable named `CD` replaces the
computed one, and the helper asks the environment first. That order is right
and unpinned, which is ⬜ 1.

Mutations of the helper, each applied alone from saved bytes and restored, the
module `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` run each time:
the `CD` branch removed, `CD` made case-sensitive, the `__CD__` branch
removed, the environment read removed, `ntpath.expandvars` put back — each
`1 failed, 56 passed` under `-x`. That confirms the fix pass's five. A sixth,
the environment asked after `CD` instead of before, stays green at
`96 passed, 1 skipped`.

The template (`templates/config.md` §*Broad gate*), the changelog fragment
and the case's docstring now say `%CD%` is the directory the row runs in, and
the template case pins that clause. Read.

## Round 2's note 2 — `gate`'s comment names both readers of `base.given`

`broad_gate.py:2211` now names `moved_line` and `skipped_at_main`. Read:
`moved_line` reads `base.given` at `:444` and hands it to `git rev-list` at
`:466`; `skipped_at_main` takes it at `:2265`. The refusal at `:2223` also
quotes `base.given`, in a message. That is the read `seal/releases/0.12.2.md`
R2's notes already call the one that "quotes the spelling rather than
consuming it", so the comment's count of two is consistent with the ledger's
line between quoting and consuming.

## Round 2's note 3 — the survivors row places R2

`survivors.md` now says R2 is "row 9 of the same file". Line 9 of
`seal/releases/0.12.2.md` is R2 and G3 is line 38. Read.

## M1 — a skip on Windows is now a failure

Claimed (0861f892): where `runs_under_cmd_exe` says no and `os.name == "nt"`,
the case asserts and fails; elsewhere it still skips.

Executed with `runs_under_cmd_exe` forced false: with the module's `os.name`
set to `nt`, the case raises `AssertionError: this is Windows and the shell
the gate hands the row to is not cmd.exe, so the case cannot answer M1`; with
`posix`, it skips. Read: nothing else in the case can skip it, so a pass on
`windows-latest` means it ran.

The windows leg at `bf43c025` (run 36088528007) is green at `4732 passed,
45 skipped` with no failure. At this tip the case can no longer skip on
Windows. It did not fail, so it ran and passed. That also answers M1 itself:
on `windows-latest`, `where/q cmd` is handed over as written and exits 0 under
`cmd.exe`, so phase 1 stands. The skip count equals the one at `5b236208`,
and the fix range added no case, so the case was most likely running there
too. That last point is inferred from the counts and was not executed.

## The fix pass's correction to `seal/releases/0.12.2.md` R2

The fix pass rewrote R2's claim to "every check … takes the resolved COMMIT,
and two readers that are not checks take the given spelling", naming
`moved_line` and `skipped_at_main`. It added a **Corrected** note saying round
1's correction had named one reader where there are two, "as it did when this
row was written". It also re-read the `gate@5fdd69eb` anchor, twice in the
same row.

Checked:
- **Readers.** `moved_line` and `skipped_at_main` are the two consumers of
  `base.given` in `gate`. `args.base` is read once, at `:2220`. Read.
- **Dates.** `moved_line` arrived in 4edc99bb, dated 2026-09-21, the row's
  own date, so "as it did when this row was written" holds. Read.
- **Ledger.** `evidence_check.py --strict .` exits 0. Executed.

## The new `survivors.md` row

The row excuses `run`'s docstring sentence at `broad_gate.py:1214`, "so a
case can drive the `cmd.exe` branch from any machine the way `quote` is
driven". It shares two phrases with the comment that was removed from
`handed_to_shell`. Its grounds say that sentence is about `run` passing
`windows` and `comspec` through. That holds: `run` hands both to
`handed_to_shell` at `:1220`. Read.

Executed: `survivor_check.py --range bafaede2...174ad801` exits 1 with that
one place and exits 0 with `--exempt survivors.md`, one `exempt`. Over
`origin/release/v0.15.4...HEAD` it exits 0 with the exemptions, three `exempt`.

## New notes

### ⬜ 1 — nothing pins that an environment `CD` wins over the computed one

`skills/verify/scripts/broad_gate.py:1286`. The helper asks `os.environ`
before it treats `CD` or `__CD__` as computed, which is what `cmd.exe` does
(`set /?`: a defined variable of that name overrides the dynamic one). If the
two branches are swapped, `%CD%` always names the row's directory even where
the environment defines `CD`, and the module stays green (`96 passed,
1 skipped`). The behaviour is right today. The next edit to the helper can
reverse the order and nothing will say so.

### ⬜ 2 — the docstring says "the way `cmd /c` replaces it", and the regex models `%NAME%` alone

`skills/verify/scripts/broad_gate.py:1271`. `cmd.exe` also expands
`%NAME:~n,m%` (a substring) and `%NAME:a=b%` (a substitution) for a defined
name. Executed: `CMD_VARIABLE` reads `CD:~0,2` and `T:repo=bin` as names,
finds neither, and leaves both as written. So a row that starts
`%CD:~0,2%/…` keeps its `/`. The docstring's "Any other name is left as
written, as `cmd /c` leaves an undefined one" is true only of undefined names.

There is a second gap, which is read and not executed. For an undefined name
on the command line, `cmd.exe` probably resumes its scan at the closing `%`,
while `re.sub` resumes after it, so `%NOPE%CD%` could be read differently.
This is from memory of the parser. No Windows run here tested it, and a
Windows run is what would answer it.

The miss goes one way only: a name is left as written and never rewritten
wrongly, which was the behaviour for every such row before #596. No row in
this repository or the template takes either form. The fix is a sentence in
the docstring or a wider pattern. Whoever takes the new issue decides which.

## Regression tests to plant

- ⬜ 1: `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, a row in
  `test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points` with
  `CD` set to a path that is not a directory. Fenced below.

## Facts for the evidence ledger

- The ledger fragment's S1 row (round 2's fix pass) names five mutations red.
  This round executed the same five, plus a sixth (the order) that survives.
  If ⬜ 1's row is planted, the sixth belongs beside the five.
- The fragment's M1 row
  (`test_a_switch_against_a_program_runs_on_the_real_platform@7a1f0d4a`) says
  **Unverified**, and only CI's windows leg executes it. That leg ran it green
  at `bf43c025` (run 36088528007), so the row can say **Executed** on
  `windows-latest` at that SHA. `questions.md` M1's answer cell can then read
  yes. Both of those are the orchestrator's edits, not this round's.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | an environment `CD` wins over the computed one, as `cmd.exe` does, and no case pins that order: with the two branches swapped the module stays green | `skills/verify/scripts/broad_gate.py:1286` | deferred a new issue | executed: the swap left `96 passed, 1 skipped`; the orchestrator files the issue and is its answerer. The unit is one the run's own fixes created, so it is the branch's if the orchestrator reads the cap that way |
| ⬜ 2 | `as_cmd_expands`'s docstring says it replaces names "the way `cmd /c` replaces it", but the regex leaves `%NAME:~n,m%` and `%NAME:a=b%` as written, and (read, not executed) may resume its scan at a different `%` than `cmd.exe` after an undefined name | `skills/verify/scripts/broad_gate.py:1271` | deferred a new issue | executed on macOS: `%CD:~0,2%` and `%T:repo=bin%` come back as written; the resume point is unverified and needs a Windows run. The miss only leaves a row as written. The orchestrator files the issue and is its answerer |
| 🟢 | round 2's finding 1 is closed — `%CD%` and `%__CD__%` name the row's directory in any case; `$NAME`, `%%` and an unset `%NAME%` stay as written | `skills/verify/scripts/broad_gate.py:1271` | verified | executed: fourteen inputs through the helper and `handed_to_shell`, and five mutations, each `1 failed` |
| 🟢 | round 2's note 2 is closed — `gate`'s comment names `moved_line` and `skipped_at_main` | `skills/verify/scripts/broad_gate.py:2211` | verified | read: `:444`, `:466`, `:2265`; the refusal at `:2223` quotes the spelling, the read R2's notes already set apart |
| 🟢 | round 2's note 3 is closed — the survivors row places R2 at row 9 | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md:10` | verified | read: line 9 of `seal/releases/0.12.2.md` is R2 |
| 🟢 | M1 in the code — the real-platform case fails, not skips, on Windows where the shell is not `cmd.exe` | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:568` | verified | executed with the branch forced: `AssertionError` under `nt`, skip under `posix`; read: the windows leg at `bf43c025` green, `4732 passed, 45 skipped`, so the case ran and passed there |
| 🟢 | the fix pass's correction to `seal/releases/0.12.2.md` R2 is true | `seal/releases/0.12.2.md:9` | verified | read: two consumers of `base.given`; `moved_line` since 4edc99bb, 2026-09-21; executed: `evidence_check.py --strict .` exit 0 |
| 🟢 | the new `survivors.md` row excuses a sentence that holds | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md:11` | verified | read: `run` passes `windows` and `comspec` at `broad_gate.py:1220`; executed: survivor check over the fix range, exit 1 without and 0 with the exemptions |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — no case pins that an environment `CD` wins over the computed one | a new issue, filed by the orchestrator (no open issue holds `cmd.exe` expansion; #596 closes with this pull request) | the orchestrator files it; whoever next edits `as_cmd_expands` plants the row |
| ⬜ 2 — `as_cmd_expands` models `%NAME%` alone, and says it models `cmd /c` | the same new issue | the orchestrator files it; a Windows run answers the resume point |

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

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round:
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/rounds/round-2.md`
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/rounds/round-2-report.md`
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/routing.md`
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md`
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/questions.md` (M1, M2)
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/changelog.md` (diff)
- `seal/ledger/1790297086-the-broad-gate-says-what-ci-says.md` (diff)
- `seal/releases/0.12.2.md` (R2, and row positions)
- `skills/verify/scripts/broad_gate.py` (`:425-:445`, `run`, `as_cmd_expands`, `handed_to_shell`, `gate` `:2205-:2270`)
- `templates/config.md` (diff)
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` (`gate_module`, the variable case, the real-platform case)
- `docs/round-record-spec.md` (the `open` word rule)
- `bin/test`
