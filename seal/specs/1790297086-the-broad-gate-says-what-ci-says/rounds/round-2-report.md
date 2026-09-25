# 1790297086-the-broad-gate-says-what-ci-says — round 2 report (verifying)

Target: `5b236208`. Surface: the fix range `4ac0b271..063cf18c` (9 commits) and the three units round 1's `New units` row names. Nothing outside that diff was opened as a finding surface, with one exception named under ⬜ 2: the gate comment the fix rewrote makes a count, and I opened the function the count leaves out.

## Summary

Eight of round 1's nine findings are closed on my own grounds. Round 1's 🟡 3 is not closed for the one row it named. `%CD%/bin/test` is still handed to `cmd.exe` as written. The fix expands the part with `ntpath.expandvars`, which reads the process environment, and `CD` is a variable `cmd.exe` computes for itself: no process environment holds it. The template, the changelog fragment and the new case's docstring all say `%CD%/bin/test` is still rewritten. That sentence is false, and the case that should hold it uses an ordinary variable instead of `CD`.

The same cause has a second, much smaller effect. `ntpath.expandvars` also expands `$NAME` and `${NAME}`, skips text inside `'…'`, and turns `%%` into `%`. `cmd.exe` does none of these. One helper that expands the way `cmd /c` does closes both effects, and it is fenced below. I tried it in the clone: 97 passed, 1 skipped in the module, with every `%CD%` row rewritten.

Everything else holds. The `\"` rule in `code_line` is correct in both directions. Each fixed case goes red when its fix is reverted. The six survivor rows are needed and their grounds are true, with one wrong line reference. The sampled ledger rows hold against their units. CI's `release` job is red at the one step this round exists to answer, and every pytest leg, Windows included, is green at `5b236208`.

## Findings from execution

### 🟡 1 — `%CD%/bin/test` is still handed over as written, and three documents say it is rewritten

`skills/verify/scripts/broad_gate.py:1313` asks `os.path.isdir(os.path.join(here, ntpath.expandvars(part)))`. `ntpath.expandvars` looks each name up in `os.environ`. `%CD%` is a dynamic variable. `cmd.exe` computes it when it reads the line, and it is not in the environment block, so neither `os.environ` on Windows nor a child process sees it. `%__CD__%` and the date/time variables work the same way. The part therefore stays `%CD%`, a directory with that name never exists, and the name is handed over as written.

Executed on macOS with `CD` absent from the environment. On Windows the variable is absent too, but that half is read, not executed. The probe's rows, with `root` holding `bin/`:

- `%CD%/bin/test -q` → `%CD%/bin/test -q`. Not rewritten.
- `%cd%/bin/test -q` → as written.
- `%TREE%/bin/test -q`, with `TREE` set to the root → `%TREE%\bin\test -q`. This is the shape the new case pins.

Why it matters: round 1 raised 🟡 3 because 0.15.3 rewrote `%CD%/bin/test` and this branch stopped rewriting it, so that row regresses when the release ships. The fix does not restore that row. It also added three sentences that say it does:

- `templates/config.md:211` — "so `%CD%/bin/test` is still rewritten". A person writing the row reads this.
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/changelog.md:10` — the same claim. It reaches the release notes.
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:218`, in the new case's docstring — "without the expansion that row stopped running". The case never runs that row.

The class, enumerated by what `ntpath.expandvars` does that `cmd /c` does not do (§12):

- **A name `cmd.exe` computes** (`%CD%`, `%__CD__%`). Nothing expands it. This is the named regression.
- **`$NAME` and `${NAME}`.** Both are expanded, and `cmd.exe` does not read them. Executed: with a `$X` directory in the root and `X` naming a file, `$X/x` is handed over as written. Before the fix it was rewritten, and `cmd.exe` looks for the `$X` directory. This needs a literal `$`-named directory, so it is rare.
- **`'…'`.** Text inside single quotes is not expanded, and `cmd.exe` has no single-quote quoting. Rare for the same reason.
- **`%%`.** It becomes `%` (executed: `%%bin` → `%bin`). `cmd /c` leaves `%%` alone on its command line. Rare.

The fenced helper expands only `%NAME%` and resolves `%CD%` and `%__CD__%` to the directory the row runs in. It leaves every other name as written, which is what `cmd /c` does with an undefined name. It was tried in the clone and then reverted. With it, `%CD%`, `%cd%`, `%__CD__%bin`, `%TREE%` and `$X` come out as `cmd.exe` reads them. `%NOPE%`, a variable naming a file, and `xcopy/e/i` stay as written, and the existing module is 97 passed, 1 skipped.

Does it lose a record or crash? No. The row is handed over as written, which is how `cmd.exe` got it before #448.

## Findings from reading

### ⬜ 2 — `gate`'s comment counts one reader of `base.given` below the resolution, and there are two

The fix for round 1's ⬜ 4 rewrote the comment at `skills/verify/scripts/broad_gate.py:2183-2190`. It now says everything below asks `base.commit` "with one exception: `skipped_at_main`". But `moved_line(root, base)` is called below it at `:2221`. It reads `base.given` in three messages, and at `:465-467` it hands `base.given` to `git rev-list --count --left-right`. The comment now makes a count, and the count is one short.

The behaviour is correct, because `moved_line` exists to describe the spelling the caller gave. That is also why the ledger's R2 correction still holds. R2 speaks of consumers, meaning the checks the gate runs and what decides which of them run. The #468 re-read note on the same row already read `moved_line` that way. Only the comment's "one exception" is wrong.

### ⬜ 3 — a survivor row's grounds point at the wrong line (correction)

`seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md`, the `seal/releases/0.12.2.md` row, says "R2 on the line above carries the **Corrected** note". R2 is row 9 of that file. The row above G3 (line 38) is G2. The grounds are otherwise true. This is the run's paperwork, so it is a correction and stays out of `Needs a fix`.

## Round 1's findings, answered

- **🔴 1 (survivors).** Verified. At `5b236208`, `survivor_check.py --range origin/release/v0.15.4...HEAD` with every `survivors.md` passed as `--exempt` exits 0 with three rows `exempt`. Without the exemptions it exits 1 on the same three places. Over the fix range alone (`4ac0b271...HEAD`) rows 4–6 excuse four places, and they do nothing over the PR range. That is expected, because the note they cover was added and removed inside the branch. CI did not reach the step at `5b236208` (see the probes), so this answer is local.
- **🔴 2 (the skip line on `windows-latest`).** Verified by reading and by CI. At `8f5ae44f` the Windows leg failed exactly as round 1 predicted: `1 failed, 4725 passed, 45 skipped`, and the printed line reads `.github\workflows\hygiene.yml`. The pin now interpolates `gate.WORKFLOW`, which is `os.path.join(".github", "workflows", "hygiene.yml")`. At `5b236208` the Windows leg passes: `4732 passed, 45 skipped`, no failure.
- **🟡 3.** Not closed. It is this round's 🟡 1.
- **⬜ 4.** The comment names `skipped_at_main` and gives the reason. Verified as far as it goes, and the count it now makes is this round's ⬜ 2.
- **⬜ 5.** Verified. R2 (`seal/releases/0.12.2.md:9`) carries a dated **Corrected** note naming `skipped_at_main` and its reason. `args.base` is read once, at `:2191`, and the other three matches are comments. Every check the gate runs is handed `base.commit` (`:2243-2262`).
- **⬜ 6.** Verified. The docstring of `skipped_at_main` (`:1864-1867`) and `templates/config.md:169-174` both state the bound. The code keys on `given` with one `origin/` removed and equal to `main`, and on the step being present (`:1869-1877`), which matches the stated bound.
- **⬜ 7.** Verified by execution, in both directions. Inside `"…"`, `\"` does not close the string: `"a \" # b"` is kept whole, `"a \"" # b` is cut at the comment, `"a \\" # b` is cut, and `"a \\\" # b"` is kept. Inside `'…'` there is no escape: `'a\' # b` is cut, as the shell does. Outside a quote, `echo \" # b` is kept, which reads a comment as code, the direction the docstring accepts. A backslash only ever keeps a string open, so the new rule cannot drop code that the old rule kept.
- **⬜ 8.** Verified. `agents/sealer.md:88-94` tells the sealer to quote the line, and `test_the_sealer_is_told_to_quote_the_skip_line` pins it.
- **⬜ 9.** Verified by execution. `@@bin/test` → `@@bin\test`, and `"@bin/test"` and `^@bin/x` stay as written, as `cmd.exe` reads a quoted or escaped `@`.

## New units, judged as code

- `test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points`. It is correct for what it runs, and it went red with the expansion reverted (1 failed). It does not run `%CD%`, the row its docstring names, which is part of 🟡 1.
- `test_the_template_and_the_docstring_state_the_skips_bound`. Correct. The section split ends at `## The fold's values`, the next heading.
- `test_the_sealer_is_told_to_quote_the_skip_line`. Correct.
- The `\"` cases in `tests/test_a_workflow_is_read_the_one_way.py` and the `@@bin/test` case went red with their fixes reverted: 2 failed and 1 failed.

## survivors.md, row by row

| Row | Quote found at | Judgement |
|---|---|---|
| 1 | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:169` | Holds. That work item's design record. It shipped in 0.15.3 and recorded a deferral this branch closes |
| 2 | same file `:167` | Holds. `templates/config.md:210` still names the blank before a switch, and the scan never rewrites across a blank |
| 3 | `seal/releases/0.15.3.md:60` | Holds. A2 carries round 2's note, and after it this work item's **Corrected** note says that note stopped being true |
| 4 | `seal/releases/0.10.0.md:68` (S7) and `:72` (S12) | Holds. Both notes are dated readings, and S7's and S12's claims do not depend on which arms run |
| 5 | `seal/releases/0.12.0.md:26` | Holds. The refusal still stands before any `run` |
| 6 | `seal/releases/0.12.2.md:38` (G3) | Holds, except that the grounds place R2 "on the line above" (⬜ 3) |

## Ledger rows sampled (the fix pass re-read 21)

Read against their units at `5b236208`:

- 0.12.2 R2
- 0.12.2 G3
- 0.10.0 S7
- 0.12.0 line 26 (`not_as_written`)
- 0.15.3 A1
- 0.15.3 A2
- 0.5.0 S8
- 0.15.1 G3 and N1

Each note describes its unit's change correctly. `gate` changed in one comment. The template changed only under `## Broad gate` (heading at `:161`, hunks at `:169` and `:204-211`). `agents/sealer.md` gained one paragraph. `handed_to_shell` gained the expansion. Each claim still holds. The Re-read notes on A1 and A2 describe the expansion correctly as code. Neither of them repeats the `%CD%` claim, so 🟡 1 does not make either row false. `evidence_check.py --strict .` exits 0.

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

## Paste-ready fixes

### 🟡 1

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

### ⬜ 2

```python
# skills/verify/scripts/broad_gate.py, gate — the comment above resolve_base
    # construction*). Every check below asks `base.commit`, which is the
    # commit CI will compare against. Two readers take `base.given`, the
    # caller's spelling, and neither is a check: `moved_line`, which exists
    # to say how that spelling differs from what it resolved to, and
    # `skipped_at_main`, because the workflow's guard compares a branch NAME
    # (`github.base_ref`) and a resolved commit carries no name (#473).
```

### ⬜ 3

```text
survivors.md, the seal/releases/0.12.2.md row — replace "R2 on the line
above carries the **Corrected** note that replaced its own" with "R2, row 9
of the same file, carries the **Corrected** note that replaced its own".
```

## Regression tests to plant

- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`: the three `CD` rows above, inside the existing case. They go red against `5b236208`: the probe showed `%CD%/bin/test -q` handed over as written.

## Facts for the evidence ledger

- The fragment's S1 row (`seal/ledger/1790297086-the-broad-gate-says-what-ci-says.md`) says the part is expanded "with `ntpath.expandvars`". Once 🟡 1 is fixed, that claim names the new helper and its `CD` rule, and the row is re-stamped against `handed_to_shell`. The helper's name is NAME NOT IN TREE until then.

Needs a fix: yes — 🟡 1 (`%CD%/bin/test` is still handed over as written, and the template, the changelog fragment and the case's docstring say otherwise)

Loses a record or crashes: no

## Proof block

Files opened this round, at `5b236208` in the clone or the worktree:

- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/rounds/round-1.md`
- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md`
- the fix-range diff of `skills/verify/scripts/broad_gate.py`, `tests/conftest.py`, `templates/config.md`, `agents/sealer.md`, the three test modules, the changelog fragment and `overview.md`
- `skills/verify/scripts/broad_gate.py`, lines 405-480, 1195-1240, 1268-1320, 1400-1500, 1507-1522, 1845-1900 and 2176-2262
- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, lines 30-55 and 530-557
- `.github/workflows/hygiene.yml`, lines 241-256
- `seal/releases/0.12.2.md` lines 9, 37 and 38; `seal/releases/0.10.0.md` lines 68 and 72; `seal/releases/0.15.3.md` lines 59 and 60; `seal/releases/0.5.0.md` line 107; `seal/releases/0.12.0.md` line 26; `seal/releases/0.15.1.md` lines 25 and 26
- `templates/config.md` headings
- `bin/test`
- CI logs of runs 36086691558, 36086691559, 36084469701 and 36084469835
