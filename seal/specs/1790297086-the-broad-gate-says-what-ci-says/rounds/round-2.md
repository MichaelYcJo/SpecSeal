# 1790297086-the-broad-gate-says-what-ci-says — review round 2

| Field | Value |
|---|---|
| Target SHA | 5b236208e07deb6b0007e8c175e581d437096926 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 607 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (`%CD%/bin/test` is still handed over as written, and the template, the changelog fragment and the case's docstring say otherwise) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item 1790297086 is the verifying round over round 1's fixes (4ac0b271..063cf18c) at 5b236208. For each round-1 verdict closed as fixed or answered, it asks whether it is actually closed. It reads the units the fixes created (the %VAR% expansion, the escaped-quote comment rule) as a finding surface in both directions. It also reads PR #607's CI at the new tip, including the windows leg for round 1's red 2 and for M1.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Round 1's 🟡 3 is not closed for the row it named: `%CD%/bin/test` is still handed over as written, because `CD` is computed by `cmd.exe` and is in no environment `ntpath.expandvars` reads; the template, the changelog fragment and the new case's docstring say it is rewritten. The same reader also expands `$NAME`, honours `'…'` and collapses `%%`, which `cmd.exe` does not | `skills/verify/scripts/broad_gate.py:1313` | open | executed on macOS with `CD` unset (absent on Windows too: read); the fenced helper tried in the clone, module 97 passed, 1 skipped, then reverted |
| ⬜ 2 | `gate`'s comment says `skipped_at_main` is the one reader of `base.given` below the resolution; `moved_line`, called at `:2221`, also reads it and hands it to `git rev-list` | `skills/verify/scripts/broad_gate.py:2187` | open | read; behaviour correct, the count in the sentence is not |
| ⬜ 3 | `survivors.md`'s 0.12.2 row says R2 is "on the line above" G3; R2 is row 9, G2 is above G3 | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md:10` | open | read; a correction to the run's paperwork, outside `Needs a fix` |
| 🟢 | round 1's blocking finding 1 is closed — the three survivors are excused, each with true grounds | `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md` | verified | executed: `survivor_check.py` over the PR range, exit 0 with exemptions and exit 1 without; CI did not reach the step at `5b236208` |
| 🟢 | round 1's blocking finding 2 is closed — the skip-line pin interpolates `gate.WORKFLOW` | `tests/test_the_gate_names_every_step_ci_runs.py:889` | verified | read; CI at `8f5ae44f` failed on exactly this line with backslashes; the Windows leg at `5b236208` — see the row below |
| 🟢 | round 1's ⬜ 4 — the comment names `skipped_at_main` and why it reads the spelling | `skills/verify/scripts/broad_gate.py:2187` | verified | read; the count it now makes is this round's ⬜ 2 |
| 🟢 | round 1's ⬜ 5 — R2 corrected in place with a dated note | `seal/releases/0.12.2.md:9` | verified | read against `gate`; `args.base` read once at `:2191`; evidence-check exit 0 |
| 🟢 | round 1's ⬜ 6 — the skip's bound is stated in the docstring and the template, and matches the code | `skills/verify/scripts/broad_gate.py:1864` | verified | read; pinned by the new template/docstring case |
| 🟢 | round 1's ⬜ 7 — `\"` inside `"…"` does not close it; no escape inside `'…'` | `tests/conftest.py:75` | verified | executed over ten lines in both directions; reverting the rule turns 2 cases red |
| 🟢 | round 1's ⬜ 8 — the sealer is told to quote the skip line | `agents/sealer.md:88` | verified | read; pinned |
| 🟢 | round 1's ⬜ 9 — every leading `@` is dropped from the part | `skills/verify/scripts/broad_gate.py:1453` | verified | executed; reverting to one `@` turns 1 case red |
| 🟢 | the fix pass's 21 re-read ledger rows, 9 sampled | `seal/releases/0.12.2.md` | verified | read against their units; `evidence_check.py --strict` exit 0 |
| 🟢 | the Windows leg at `5b236208` passes the skip-line case round 1's blocking finding 2 was about | `tests/test_the_gate_names_every_step_ci_runs.py:965` | verified | read: CI run 36086691559, `pytest (windows-latest, 3.12)` success, `4732 passed, 45 skipped`, no failure |
| ❓ | M1: whether the Windows leg RUNS `test_a_switch_against_a_program_runs_on_the_real_platform` or skips it | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:538` | ❓ out of verified scope | CI runs `pytest -q`, which names failures and never names skips, so neither tip's log can tell a pass from a skip (45 skipped on Windows at both tips, against 10 on macOS and 13 on ubuntu; the case did not fail at either). Answered by the orchestrator: one `-rs` run of that case on a Windows runner, or a line in the case that fails if it skips while `os.name == "nt"` |

## Paste-ready fixes

```python
# skills/verify/scripts/broad_gate.py — above handed_to_shell
CMD_VARIABLE = re.compile(r"%([^%]+)%")


def as_cmd_expands(part, here):
    """`part` with each `%NAME%` replaced the way `cmd /c` replaces it before
    it reads a command name (#596).

    A name defined in this process's environment takes its value, which is
    the environment `run` hands the shell. `CD` and `__CD__` are in no
    environment: `cmd.exe` computes them, and both name the directory the
    row runs in, which is `here`. Any other name is left as written, as
    `cmd /c` leaves an undefined one, and so is `%%`. Nothing else is
    expanded: `$NAME` and `'…'` mean nothing to `cmd.exe`, which is why this
    is not `ntpath.expandvars`.
    """

    def value(match):
        name = match.group(1)
        if name in os.environ:
            return os.environ[name]
        if name.upper() == "CD":
            return os.path.abspath(here)
        if name.upper() == "__CD__":
            return os.path.join(os.path.abspath(here), "")
        return match.group(0)

    return CMD_VARIABLE.sub(value, part)
```
```python
# skills/verify/scripts/broad_gate.py, handed_to_shell — the call
    return command_names_backslashed(
        command,
        lambda part: os.path.isdir(os.path.join(here, as_cmd_expands(part, here))),
    )
```
```python
# tests/test_the_gate_hands_cmd_a_path_it_can_run.py — in
# test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points
    monkeypatch.delenv("CD", raising=False)
    monkeypatch.delenv("__CD__", raising=False)
    # ... and add to the rows:
        # `CD` is computed by cmd.exe and is in no environment (round 2, 🟡 1).
        ("%CD%/bin/test -q", r"%CD%\bin\test -q"),
        ("%cd%/bin/test -q", r"%cd%\bin\test -q"),
        ("%__CD__%bin/test", r"%__CD__%bin\test"),
```
```text
templates/config.md:209-211 — replace "A `%VAR%` in that part is expanded
from the gate's own environment first, as `cmd.exe` expands it before it
reads the name, so `%CD%/bin/test` is still rewritten." with:

A `%VAR%` in that part is expanded first, as `cmd.exe` expands it before it
reads the name: from the gate's own environment, and `%CD%` as the directory
the row runs in, so `%CD%/bin/test` is still rewritten.

The existing needle ("A `%VAR%` in that part is expanded ...") then needs
its tail re-cut to "A `%VAR%` in that part is expanded first, as `cmd.exe`
expands it before it reads the name", and a second needle "`%CD%` as the
directory the row runs in" pins the new clause.
```
```python
# skills/verify/scripts/broad_gate.py, gate — the comment above resolve_base
    # construction*). Every check below asks `base.commit`, which is the
    # commit CI will compare against. Two readers take `base.given`, the
    # caller's spelling, and neither is a check: `moved_line`, which exists
    # to say how that spelling differs from what it resolved to, and
    # `skipped_at_main`, because the workflow's guard compares a branch NAME
    # (`github.base_ref`) and a resolved commit carries no name (#473).
```
```text
survivors.md, the seal/releases/0.12.2.md row — replace "R2 on the line
above carries the **Corrected** note that replaced its own" with "R2, row 9
of the same file, carries the **Corrected** note that replaced its own".
```

## Executed probes

| What was run | Result |
|---|---|
| `handed_to_shell`, `windows=True`, a root holding `bin/`, `%bin/`, `%%bin/`, `$X/`, `it's/` and a file, `CD` unset, over 13 rows | `%CD%/…` and `%cd%/…` as written; `%TREE%/bin/test` rewritten; `%NOPE%/…` and a variable naming a file as written; a variable set to empty and a relative one (`bin`) rewritten; `%%bin/x` rewritten via `%bin`; `$X/x` as written (X names a file); `@%TREE%/…` and `"%TREE%/…"` rewritten |
| `ntpath.expandvars` over `%%bin`, `%NOPE%`, an empty variable, `$X`, `${X}`, `'%TREE%'`, `%cd%` | `%bin`; as written; empty; expanded; expanded; as written; as written |
| `code_line` over ten lines (`\"` inside and outside `"…"`, `\\"`, `\\\"`, `'a\'`, `"C:\"`, a whole-line comment, an unterminated string) | as listed under round 1's ⬜ 7 |
| Three mutations, each reverted from saved bytes: the expansion removed, one `@` dropped instead of all, the `\"` rule removed | 1 failed; 1 failed; 2 failed |
| The fenced 🟡 1 helper patched in, with a probe of 8 rows plus `%CD%` with no root after `chdir`, then reverted | all as `cmd.exe` reads them; module 97 passed, 1 skipped; tree clean after |
| `survivor_check.py --range origin/release/v0.15.4...HEAD`, with and without every `survivors.md` | exit 0, three `exempt`; exit 1, the same three places |
| `survivor_check.py --range 4ac0b271...HEAD`, with and without | exit 0, four `exempt` from rows 4–6; exit 1, four places |
| `evidence_check.py --strict .` | exit 0 |
| `bin/test` over the three modules the fix touched | 153 passed, 1 skipped (M1, macOS) |
| CI `release` job at `5b236208` (read) | failure at *a declared review chain has the round record it claimed*: `Pass` checked beside `Fixes checked by: nobody`. This round's record answers it. The survivor, correction and four later steps were skipped |
| CI tests at `5b236208` (read) | lint, ledger, ubuntu and macOS pytest pass; Windows success, `4732 passed, 45 skipped` (six more passed than the `4726` that ran at `8f5ae44f`, the six new cases, and the skip count unchanged) |
| CI tests at `8f5ae44f` (read) | Windows `1 failed, 4725 passed, 45 skipped`, the failure being round 1's 🔴 2 with `.github\workflows\hygiene.yml` in the printed line; macOS `4761 passed, 10 skipped`; ubuntu `4758 passed, 13 skipped` |
| The broad gate (full suite, lint, typecheck through `broad-gate`) | not yet — the sealer's, after this round; nothing here ran it |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
