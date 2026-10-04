# 1791076831-a-here-document-body-is-data-to-the-commit-gate — review round 3

| Field | Value |
|---|---|
| Target SHA | 12f68c74b9a8970084baa9ea91ca8a2c1eddd898 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #760 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (`hooks/cmdline.py:417`), 🟡 2 (`hooks/tokens.py:431`) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 of work item `1791076831-a-here-document-body-is-data-to-the-commit-gate` (#739, PR #760). It is the verifying round for round 2's fix, `903e5603..82e0680d`, and it also reads one post-review commit after the close, which declares gh's `2.100.0` for the release-hygiene version pin. Round 2's fix was the one reopening, so this record ends the run whatever it finds. A finding left open takes the filing ladder with a `Who answers it`.

Round 2's 🔴 1 was closed by the owner's structural rule: when any heredoc on a line has an unquoted delimiter, no body on that line is data. `heredoc_data` now tests `all(r.quoted for r in records)`, and the substring test is gone. The two `zip` calls in `hooks/tokens.py` lost `strict=True` for the interpreter floor.

Judge three things: whether the structural rule closes the class round 2 named, whether every policy sentence now states it, and whether a line whose bodies are all quoted still gets its data verdicts. Do it by reading the rule against the reader's records and by calling `heredoc_data` and the gate's decision functions on constructed command strings. Ask what the gate decides; do not run a shell that executes what a line would write.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | Round 2's structural rule trusts the reader's per-body `quoted` answer. `_quoted_delimiter` can answer `quoted` where the shell does not: a backslash-newline inside the delimiter word is removed by the shell's line continuation before the word is read, so the delimiter the shell sees differs from the one the reader judged. The structural rule then calls a body data that the shell expands, so a line the base stops passes silently | `hooks/cmdline.py:417` (`_quoted_delimiter`), relied on at `hooks/tokens.py:477` (`heredoc_data`) | open | executed: `main()` decisions on constructed strings, in a repository declaring no work item, read silent at the target and at `903e5603` and stop at `e141980a`. No shell ran them. Read: the bash and zsh manuals' line-continuation rule. A one-line fail-closed change to `_quoted_delimiter` turned four proposed cases red at the target and green with the change (169 passed over three modules), and it was reverted in the scratch clone |
| 🟡 2 | R2f's list of what can run a file a line has written is incomplete. A file written over a program the line later runs from `PATH`, and `gh` running a program its configuration names, both read silent | `hooks/tokens.py:431` (`_runs_what_it_reaches`) | open | executed as gate decisions only. No writable `PATH` executable on the reviewing machine carries a name from the data-line program set, so the first mechanism is theoretical there. A candidate fix kept #739's own `gh` case as data and flipped these shapes (167 passed, ruff clean), and it was reverted |
| ⬜ 3 | `spec.md`'s R2a does not state the structural rule (every delimiter on the line is quoted) | `seal/specs/1791076831-a-here-document-body-is-data-to-the-commit-gate/spec.md:46` | open | read; a correction to the record |
| ⬜ 4 | `heredoc_data`'s docstring states R2a without the every-delimiter clause, and `docs/commit-review-gate-spec.md:194`'s "and so is every other delimiter" attaches ambiguously | `hooks/tokens.py:454` | open | read |
| 🟢 | Round 2's 🔴 1 is closed for its own instance | `hooks/tokens.py:477` | confirmed | executed: the module's cases pass at the target |
| 🟢 | Round 1's 🟡 1 stays closed: `--output` and a `printf` option keep the line read | `hooks/tokens.py:396` | confirmed | executed |
| 🟢 | The axes round 2 did not reach keep the line read: parameter expansion with side effects, arithmetic expansion, process substitution, an alias, `source`, and a backslash-newline on the command line itself | `hooks/tokens.py:477` | confirmed | executed as gate decisions |
| 🟢 | A line whose bodies are all quoted keeps its data verdicts | `hooks/tokens.py:477` | confirmed | executed: 8 lines through `heredoc_data`, 4 through `main()` |
| 🟢 | `12f68c74`, the declaration of gh's version, holds | `tests/test_release_hygiene.py` | confirmed | executed: the module passes |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `test_a_heredoc_body_nothing_runs_is_data`, `test_release_hygiene` and `test_a_script_says_which_interpreter_it_needs` at the target | 188 passed |
| `main()` and `heredoc_data` decisions on constructed strings at the target, `903e5603` and `e141980a` | as in the verdicts; no shell executed any string |
| ruff check and format on the touched files | clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/tokens.py:396` (`_plain_on_a_data_line`), with `hooks/tokens.py:432` (`_writes_a_file`) | round 1's 🟡 1 — fixed |
| round-2 | `hooks/tokens.py:475` (`heredoc_data`) | round 2's 🔴 1 — fixed |
| round-2 | `hooks/tokens.py:396` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🔴 1, 🟡 2, ⬜ 3, ⬜ 4 | this run's reopening is spent, so the filing ladder | the repository owner, who took the fix on the branch after the rounds |
