# 1790297086-the-broad-gate-says-what-ci-says — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | f01a37ae |
| Ran by | unknown — the spawn prompt did not name the agent and model, and this segment does not source that value from its own idea of itself |

## What this phase was asked

#596. The scan takes `is_directory`, `handed_to_shell` takes `root`, and
`run` passes it on. `handed_line` is reworded. The scan's docstring and
`templates/config.md` §*Broad gate* state the directory rule and both bounds,
and they drop "Telling the two apart is #596". The cases are these:

- A1: the bound case, inverted and renamed.
- A2: the existing table, driven with its directories present.
- A3 and A4: a new table for the other side.
- A6: a real-platform case running `where/q cmd`, skipped off `cmd.exe`.
- A7: the template case's needles.
- Every `handed_to_shell` call in the module is given a root.

The spawn prompt added one trap the framer flagged:
`test_the_row_runs_on_the_real_platform` called `handed_to_shell("bin/probe")`
with no root, and it had to be given its fixture repository. The ledger work
was also named: `seal/releases/0.15.3.md` row A2 is corrected in place, and
the new claim goes in this work item's fragment.

## What this phase found

- **The trap was wider than one line.** Two more existing calls leaned on
  pytest's working directory without saying so: the kept-row case ran `run`
  with `tmp_path` as `root`, and that path had no `bin/`. Under the directory
  rule it would have gone red rather than silently reading `sh`, so it was
  loud, but it is the same class. Every call in the module now passes a
  root, and a module fixture, `tree`, holds `bin/`, `tools/` and `x/`, the
  directories the A2 table's rows name.
- **The frame's red at the frame commit is blunt through the module.** Every
  new case passes `root=`, which the frame's `handed_to_shell` does not take,
  so all of them fail with `TypeError` (83 failed, 10 passed in a scratch
  copy of `cf5428b1`). The behavioural red was shown by calling the frame's
  own function instead. The four switch rows were rewritten there
  (`xcopy\e\i`, `findstr\s`, `timeout\t`, `ipconfig\all`), and the scan took
  one argument.
- **A leading `@` is dropped before quotes and carets are removed.** The
  spec lists the three removals without an order. `cmd.exe` treats only an
  unescaped, unquoted `@` as the echo-off prefix, so `@"a b"/c` asks about
  `a b`, while `"@x"/y` and `^@x/y` keep their `@`. This is also the order
  the built-in check already used (`lstrip("@")` on the raw name).
- **One guard was removed after the first commit.** The built-in check at
  the first `/` was guarded by "no decision taken yet". A raw quoted name
  never matches a built-in, so no output can reach the guard. It was removed
  in 5fbb7edf rather than left for a mutation to survive.
- **Two mutations survived the first table.** Leaving a name's start unset
  for a quoted or `^`-opened name changed nothing while that name stood first
  in the row. Two rows with such a name after a separator now pin it, and
  both mutations go red.
- **A drive-letter name stays platform-dependent, and it is not claimed.**
  For `"C:/tools/x"` the part is `C:`. On Windows `os.path.isdir` answers it
  from the drive's current directory, and on a POSIX machine driving the
  Windows branch it is not a directory. No case pins it and no document
  claims it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_a_switch_against_another_program_is_rewritten_the_documented_bound_not_the_goal` — NAME NOT IN TREE — which pinned `xcopy/e` → `xcopy\e` as a bound | inverted as `test_a_switch_against_another_program_reaches_cmd_exe_as_written`. The 0.15.3 row A2's anchor on it was dropped as dead, and the claim is in `seal/ledger/1790297086-the-broad-gate-says-what-ci-says.md` |
| the template's sentences "A `/` written straight after any other program's name is read as part of a path and rewritten … Telling the two apart is #596" | `templates/config.md` §*Broad gate*, as the directory rule and its two bounds |
