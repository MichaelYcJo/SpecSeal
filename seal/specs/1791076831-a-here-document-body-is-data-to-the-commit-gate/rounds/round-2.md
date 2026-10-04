# 1791076831-a-here-document-body-is-data-to-the-commit-gate — review round 2

| Field | Value |
|---|---|
| Target SHA | fb5e93e75d05eb150f10ac886a8086ec249f9302 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #760 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (`hooks/tokens.py:475`) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item `1791076831-a-here-document-body-is-data-to-the-commit-gate` (#739, PR #760). This is the verifying round for round 1's fixes, over the range `0844c21f..dafafb01`. Round 1 met the floor and its fixes were the one reopening, so this record ends the run whatever it finds. A finding left open takes the filing ladder, with a `Who answers it`.

The fix pass compared every clause of `is_plain` against the data rule and carried three guards:
- `--output`, which writes a file;
- a `printf` option such as `-v`;
- a third guard that round 1 did not name: an unquoted body holding `$( … )` or a backtick, read in `heredoc_data`. This was a real hole. With `cat > f.sh <<'A'` followed by `cat <<B` holding `$(sh f.sh)`, the first body was called data, and bash 3.2 ran `f.sh`.

Open each guard. Then attack the class the third one belongs to, by construction: any other way the outer shell can execute text on the same line after a data body has written a file. That covers parameter expansion with side effects, arithmetic expansion, process substitution, an alias, and `eval` or `source` reached indirectly. Check each against R2c/R2f as built.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The third guard tests an unquoted body's raw text for `$(` or a backtick, but the shell removes a backslash-newline in such a body before expanding it. A split `$(` passes the test, the line's quoted body is called data, and the file it wrote runs, so a commit passes the gate silently. The base read every body as shell and stopped this line | `hooks/tokens.py:475` (`heredoc_data`) | open | executed by the reviewing agent before its stop, in bash 3.2 and zsh 5.9: `main()` returned silent and the commit landed. Read by the orchestrator: the guard at `hooks/tokens.py:475-477` is a substring test over `r.text` |
| 🟢 | Round 1's 🟡 1: `--output` and a `printf` option no longer leave a body data | `hooks/tokens.py:396` | confirmed | executed: both shapes give `heredoc_data` `[False]` at the target |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| The two round-1 shapes through `heredoc_data` at `fb5e93e7` | `[False]` each |
| `git diff --outp=` under git 2.54 | refused, exit 129 |
| A quoted sink body with an unquoted second body holding a backslash-newline-split substitution, through `main()`, under bash 3.2 and zsh 5.9, in a scratch clone with a hook that commits | the gate silent and the commit landed, in both shells, with `cat` and with `tee` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/tokens.py:396` (`_plain_on_a_data_line`), with `hooks/tokens.py:432` (`_writes_a_file`) | round 1's 🟡 1 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `is_plain`'s raw-text test at the base | not filed yet | the repository owner |
