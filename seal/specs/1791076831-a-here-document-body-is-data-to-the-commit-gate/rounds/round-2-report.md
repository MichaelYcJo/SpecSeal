# Round 2 — a here-document body is data to the commit gate (#739)

The verifying round for round 1's fixes, `0844c21f..dafafb01`, at target `fb5e93e7`.

**How this report was written.** The reviewing agent (`specseal:warden on claude-opus-5-5`) was stopped by a safety classifier partway through the round, while building probes that bypass the gate. It wrote no report. It handed back what it had executed before the stop, and this file is the orchestrator's transcription of that hand-back. The orchestrator checked the finding's coordinate against the code before writing it down: `hooks/tokens.py`'s third guard is the literal substring test `"$(" in r.text or "`" in r.text`. The axes the round was asked to attack and did not reach stay open as ❓. They are not passes.

## What the account claimed, and what the code showed

The fix pass said it carried three of `is_plain`'s guards into the data rule:
- `--output`;
- a `printf` option;
- an unquoted body holding `$(` or a backtick.

The first two hold. Both shapes, `git diff --output` and `printf -v`, now turn `heredoc_data` to `[False]`. The abbreviated `--outp=` is not a hole, because git 2.54 refuses the abbreviation and exits 129.

The third does not hold. It searches the raw text of an unquoted body. The shell removes a backslash-newline inside an unquoted here-document body before it expands substitutions. So a body whose raw text never contains `$(` still runs a command substitution: the `$` ends one line and the `(` begins the next. The first, quoted body on the line is then judged data. Under bash 3.2 and zsh 5.9 the gate returned `silent` through `main()`. The file the first body wrote ran, and a commit landed. The same holds with `tee` in place of `cat`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The third guard tests an unquoted body's raw text for `$(` or a backtick, but the shell removes a backslash-newline in such a body before expanding it. A split `$(` passes the test, the line's quoted body is called data, and the file it wrote runs, so a commit passes the gate silently. The base read every body as shell and stopped this line | `hooks/tokens.py:475` (`heredoc_data`) | open | executed by the reviewing agent before its stop, in bash 3.2 and zsh 5.9: `main()` returned silent and the commit landed. Read by the orchestrator: the guard at `hooks/tokens.py:475-477` is a substring test over `r.text` |
| 🟢 | Round 1's 🟡 1: `--output` and a `printf` option no longer leave a body data | `hooks/tokens.py:396` | confirmed | executed: both shapes give `heredoc_data` `[False]` at the target |

## Executed probes

| What was run | Result |
|---|---|
| The two round-1 shapes through `heredoc_data` at `fb5e93e7` | `[False]` each |
| `git diff --outp=` under git 2.54 | refused, exit 129 |
| A quoted sink body with an unquoted second body holding a backslash-newline-split substitution, through `main()`, under bash 3.2 and zsh 5.9, in a scratch clone with a hook that commits | the gate silent and the commit landed, in both shells, with `cat` and with `tee` |

## Not reached

| Axis | Who answers it |
|---|---|
| parameter expansion with side effects, arithmetic expansion, process substitution, an alias, `eval` or `source` reached indirectly, a file written over an executable already on `PATH` | the next verifying round; this one stopped before them |
| whether `is_plain`'s own raw-text test (`hooks/tokens.py:188`, at the base) has the same gap | the repository owner, since it is base code and outside this range |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `is_plain`'s raw-text test at the base | not filed yet | the repository owner |

Needs a fix: yes — 🔴 1 (`hooks/tokens.py:475`)

Loses a record or crashes: no
