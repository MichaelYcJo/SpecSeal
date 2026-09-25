# 1790297086-the-broad-gate-says-what-ci-says — review round 1

| Field | Value |
|---|---|
| Target SHA | 8f5ae44f125e214721e7957fcf876da97eb86904 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 607 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `4ac0b271df272d55a317a632cadf0138b4e2a877..063cf18cc7a5ec185993a0d95602859f5837651f`, 9 commits |
| Contract changes | none |
| New units | test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points (depth 1); test_the_template_and_the_docstring_state_the_skips_bound (depth 1); test_the_sealer_is_told_to_quote_the_skip_line (depth 1) |
| Needs a fix | yes — 🔴 1 (the survivor step is red at CI), 🔴 2 (C1's pinned line on `windows-latest`), 🟡 3 (a `%VAR%`-rooted command name regressed) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item 1790297086 reviews the build at 8f5ae44f against spec.md and plan.md (frame 6e93c352, approved cf5428b1). It covers the cmd.exe directory rule (#596), the gate leaving out the two arms CI skips at main (#473), the one workflow reader in tests/conftest.py (#482, #462, #463) and the release-word case (#499). The classes are every command-name shape cmd.exe runs, every spelling of a main base, every comment and quote shape in workflow text, and every line the gate prints that CI must agree with. The review also read the PR's own CI.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | CI's `release` job is red at the target: the survivor step reports three removed sentences still standing, and no `survivors.md` row covers them | `seal/releases/0.15.3.md:60` | **fixed** `bd5311a5f99fbd6639f6d2021b2fbea3f0bafcd7` | fixed at bd5311a5f99fbd6639f6d2021b2fbea3f0bafcd7; executed: CI run 36084469701 at `8f5ae44f` failed that step; `survivor_check.py --range 7b557144...HEAD` exit 1 with the same three; with the fenced rows it exits 0 |
| 🔴 2 | C1 pins the skip line with `/`, but the gate builds the path with `os.path.join`, so the exact-line assertion should fail on `windows-latest` | `tests/test_the_gate_names_every_step_ci_runs.py:885` | **fixed** `4cce232190f776aa0064bd3b80cc0656fd2c4315` | fixed at 4cce232190f776aa0064bd3b80cc0656fd2c4315; read, plus executed `ntpath.join` giving `.github\workflows\hygiene.yml`; the Windows leg was in progress at the target and answers it |
| 🟡 3 | A command name rooted in `%VAR%` (`%CD%/bin/test`) was rewritten in 0.15.3 and is now handed over as written; no bound names it | `skills/verify/scripts/broad_gate.py:1306` | **fixed** `833c21def974abaae228ca6b7ef15d46e11222d5` | fixed at 833c21def974abaae228ca6b7ef15d46e11222d5; executed against `7b557144` and `8f5ae44f` in a root holding `bin/`; the fenced predicate tried and gives `%TREE%\bin\test` |
| ⬜ 4 | `gate`'s comment says everything below takes `base.commit`, and the new guard takes `base.given` | `skills/verify/scripts/broad_gate.py:2175` | **fixed** `68514b07d792380ab0bae9d3d8b06f6d55e13fbd` | fixed at 68514b07d792380ab0bae9d3d8b06f6d55e13fbd; read |
| ⬜ 5 | R2's claim (*every consumer takes the resolved COMMIT*) got a Re-read note, not a correction, though the guard now consumes the given spelling | `seal/releases/0.12.2.md` | answered | corrected at f109847797c6e5c783cb838bc0cdfacf2d786948: `seal/releases/0.12.2.md` R2 names the one consumer that reads the given spelling, with a Corrected note, then `--reverify`; read; a correction to the run's paperwork |
| ⬜ 6 | The skip is keyed on a spelling (`refs/heads/main`, `upstream/main` run both arms) and on the step's name rather than its guard | `skills/verify/scripts/broad_gate.py:1841` | answered | b9b1e91a7b8493686a6f99142daf3906b0038e96 states the bound in `skipped_at_main`'s docstring and in `templates/config.md`; no code; executed over eight spellings; no live instance: the sealer passes the plain name and the shipped template has no `release` job |
| ⬜ 7 | The comment rule tracks quotes per line and ignores `\"`, so it can drop code, which its docstring says it never does | `tests/conftest.py:48` | **fixed** `2d18a4b979ed0382ebb294e5fc43d74247f8b329` | fixed at 2d18a4b979ed0382ebb294e5fc43d74247f8b329; executed over six lines and a spanning string; no workflow line has either shape |
| ⬜ 8 | `agents/sealer.md` names the stderr lines to relay and not the skip line, the only trace that two arms did not run | `agents/sealer.md:71` | **fixed** `4437562b079263d0720abb80e3fe6f4b2bdcb676` | fixed at 4437562b079263d0720abb80e3fe6f4b2bdcb676; read |
| ⬜ 9 | The directory part drops one `@`, and the built-in check drops all of them | `skills/verify/scripts/broad_gate.py:1491` | **fixed** `833c21def974abaae228ca6b7ef15d46e11222d5` | fixed at 833c21def974abaae228ca6b7ef15d46e11222d5; executed: `@@bin/test` handed over as written |
| 🟢 | #596's predicate is asked where the row runs, `compare_at_base` included | `skills/verify/scripts/broad_gate.py:1220` | confirmed | read: `run` passes `root`, `compare_at_base` passes `scratch`; every caller of both changed functions enumerated by grep |
| 🟢 | The 0.15.3 A2 correction: claim amended, dead anchor dropped, dated Corrected note | `seal/releases/0.15.3.md:60` | confirmed | read; `evidence_check.py --strict` 2269 ok · 0 drifted · 0 broken (executed) |
| 🟢 | The 0.12.2 G4 correction: the note is true and the claim still holds | `seal/releases/0.12.2.md:39` | confirmed | read: the G4 case runs `run_gate` with the default `base="base"` |
| 🟢 | C3 is total and goes red when a guard moves | `tests/test_the_gate_names_every_step_ci_runs.py` | confirmed | executed: the regex matches the real guard, not a mutated one, and not an echo that falls through |
| ❓ | M1: whether `cmd.exe` runs `where/q cmd` as a program plus its switch | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | ❓ out of verified scope | macOS here; the `windows-latest` leg at the pull request answers it, and the orchestrator reads that leg |

## Paste-ready fixes

```markdown
# 1790297086-the-broad-gate-says-what-ci-says — survivors

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md` | telling a program from a directory is #596 | The spec of the work item that shipped #448 in 0.15.3, recording what its round 2 decided and deferred to #596. It is a past state, and this work item is what closed #596; the design record keeps what was true when it was written |
| `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md` | A switch written with a blank before it (`xcopy /e`) is left as written, and the template says so | Same record, same grounds. The sentence is still true of the scan: a blank before a switch is never rewritten |
| `seal/releases/0.15.3.md` | and #596 holds the behaviour fix | Round 2's dated **Corrected** note on row A2, kept as the history of the claim. The **Corrected 2026-09-25 by work item 1790297086 (#596)** note after it on the same row says that it stopped being true and what replaced it |
```
```python
# tests/test_the_gate_names_every_step_ci_runs.py — the path as the gate
# builds it, so the pin holds on every leg of the matrix.
SKIPPED_LINE = (
    f"broad-gate: the base is `main`, and {gate.WORKFLOW} skips "
    "the steps the `survivors` and `corrections` arms mirror on a pull request "
    "into `main`, so this run does not run them either"
)
```
```python
# skills/verify/scripts/broad_gate.py, handed_to_shell — cmd.exe expands
# %VAR% before it reads the name, so the part is expanded the same way before
# it is asked. `ntpath` reads %VAR% on every platform, so a case drives it.
    here = os.curdir if root is None else root
    return command_names_backslashed(
        command,
        lambda part: os.path.isdir(os.path.join(here, ntpath.expandvars(part))),
    )
```
```python
# tests/test_the_gate_hands_cmd_a_path_it_can_run.py
def test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points(
    tree, monkeypatch
):
    """#596. `cmd.exe` expands `%VAR%` before it reads a command name, so the
    part is expanded before it is asked whether it is a directory."""
    gate = gate_module()
    monkeypatch.setenv("SPECSEAL_PROBE_TREE", tree)
    monkeypatch.delenv("SPECSEAL_PROBE_NOWHERE", raising=False)
    for row, expected in (
        ("%SPECSEAL_PROBE_TREE%/bin/test -q", r"%SPECSEAL_PROBE_TREE%\bin\test -q"),
        ("%SPECSEAL_PROBE_NOWHERE%/bin/x", "%SPECSEAL_PROBE_NOWHERE%/bin/x"),
    ):
        got = gate.handed_to_shell(row, windows=True, comspec=CMD, root=tree)
        assert got == expected, got
        only_slashes_turned(row, got)
```
```text
templates/config.md §Broad gate, after "…names a directory that exists where
the row runs;" — add:

A `%VAR%` in that part is expanded from the gate's own environment first, as
`cmd.exe` expands it before it reads the name.

and the matching needle in test_the_template_says_which_positions_are_rewritten:

    "A `%VAR%` in that part is expanded from the gate's own environment first",
```

## Executed probes

| What was run | Result |
|---|---|
| `handed_to_shell` at `7b557144` and `8f5ae44f`, `windows=True`, a root holding `bin/` and `tools/`, over nine rows (`%CD%/…`, `%VIRTUAL_ENV%/…`, `"@bin/test"`, `@@bin/test`, `""/x`, `^@bin/x`, `bin/test`, `.venv/…`, `C:/tools/x`) | `%CD%` and `%VIRTUAL_ENV%` rewritten before and not after; `@@bin/test`, `"@bin/test"` and `^@bin/x` no longer rewritten; `""/x` and `bin/test` unchanged; `.venv/…` not rewritten where absent (the named bound) |
| `skipped_at_main` over the real workflow with eight spellings | `main` and `origin/main` skip both arms; `refs/heads/main`, `refs/remotes/origin/main`, `upstream/main`, `MAIN`, ` main` and `origin/main/` skip none |
| `code_line` over six lines, and `code_lines` over a quoted string spanning lines of a `run: \|` block | the `\"` line cut at the `#` inside the string; the spanning string's `#` line dropped; URL, apostrophe, `''` and tab lines as the docstring says |
| `workflow_steps` against `job_steps` on the real `hygiene.yml` | 13 and 13, same order |
| C3's regex over the real survivors step, the same step with its guard mutated, and a guard whose `exit 0` follows `fi` | match, no match, no match |
| `ntpath.join(".github", "workflows", "hygiene.yml")` | `.github\workflows\hygiene.yml` |
| `survivor_check.py --range 7b557144...HEAD` in the clone, without and with 🔴 1's rows | exit 1, three places; exit 0, three `exempt` |
| `correction_check.py --range 7b557144...HEAD` | exit 0, no merge commit in the range |
| `evidence_check.py --strict .` | exit 0, 2269 ok · 0 drifted · 0 broken |
| 🟡 3's predicate over five rows with `TREE` naming a directory holding `bin/` | `%TREE%\bin\test`; `%NOPE%/bin/x` as written; `xcopy/e/i` as written |
| `bin/test tests/test_a_workflow_is_read_the_one_way.py tests/test_the_gate_names_every_step_ci_runs.py -k …` (the new reader, #473 and #499 cases) | 30 passed on macOS |
| The probe module, run once through `bin/test` and then deleted | 3 passed (it printed, it asserted nothing) |
| The broad gate (full suite, lint, typecheck through `broad-gate`) | not yet — the sealer's, once the rounds settle; nothing here ran it |
| CI at `8f5ae44f` (read, not run here) | `release` failure at the survivor step; lint, ledger, ubuntu and macOS pytest success; `windows-latest` still in progress |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
