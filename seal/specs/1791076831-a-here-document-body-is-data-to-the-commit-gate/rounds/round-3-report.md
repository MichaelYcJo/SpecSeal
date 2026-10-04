# Round 3 — a here-document body is data to the commit gate (#739)

This is the verifying round for round 2's fix, `903e5603..82e0680d`, and the post-close commit `12f68c74`, at target `12f68c74`.

**How this report was written.** A safety classifier stopped the reviewing agent (`specseal:warden on claude-opus-5-5`) while it wrote a report that spelled out command strings which pass the gate. It deleted that partial file and handed back verdicts by coordinate and mechanism. This file is the orchestrator's transcription of the hand-back. On purpose, it records no command string that passes the gate. Each finding is stated by the unit it sits in and the shell rule the unit disagrees with.

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

## Executed probes

| What was run | Result |
|---|---|
| `test_a_heredoc_body_nothing_runs_is_data`, `test_release_hygiene` and `test_a_script_says_which_interpreter_it_needs` at the target | 188 passed |
| `main()` and `heredoc_data` decisions on constructed strings at the target, `903e5603` and `e141980a` | as in the verdicts; no shell executed any string |
| ruff check and format on the touched files | clean |

## Not reached

| Axis | Who answers it |
|---|---|
| whether each `gh` subcommand in `GH_REMOTE` really runs no local git at runtime | the repository owner, or someone with network access and a scratch repository · NAME NOT IN TREE: #763's fix replaced `GH_REMOTE` with `GH_NOTHING_LOCAL` |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🔴 1, 🟡 2, ⬜ 3, ⬜ 4 | this run's reopening is spent, so the filing ladder | the repository owner, who took the fix on the branch after the rounds |

Needs a fix: yes — 🔴 1 (`hooks/cmdline.py:417`), 🟡 2 (`hooks/tokens.py:431`)

Loses a record or crashes: no
