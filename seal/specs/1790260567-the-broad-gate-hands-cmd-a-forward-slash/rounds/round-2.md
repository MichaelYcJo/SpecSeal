# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — review round 2

| Field | Value |
|---|---|
| Target SHA | 9f493c5611a49821e8cfa764675e96466090c638 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 595 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `1cbae560b5972f0ae9c242f0d74227d798c8e17f..473892da98077b332171e1004ef65ef296235b98`, 3 commits |
| Contract changes | none |
| New units | test_a_switch_against_another_program_is_rewritten_the_documented_bound_not_the_goal (depth 1) |
| Needs a fix | yes — 🟡 1 (a switch written against a program other than a built-in is still rewritten into a path, and the documents name only the built-ins) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790260567 is the verifying round: the diff of round 1's fixes, 29678169..371206af, at 9f493c56, with the release merge 974c64a0 and its repair 9f493c56. Its job is whether round 1's verdicts are closed, whether CMD_BUILTINS, NOT_A_GH_TOKEN and the new gh case are correct, and whether the merge kept every note.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `/` written straight after any program other than a built-in (`xcopy/e/i`, `findstr/s`, `timeout/t`) is still rewritten into a path, so a row that runs today stops running; `spec.md:157` and the template name the built-ins as the only switch left as written | `skills/verify/scripts/broad_gate.py:1298` | **fixed** `1b6dcf5b` | fixed at 1b6dcf5b — ee085b9b, 473892da; executed: `handed_to_shell` with `windows=True` gives `xcopy\e\i`, `findstr\s`, `timeout\t`, `ipconfig\all`; what `cmd.exe` does with them is read from the module's own premise, and the `windows-latest` leg answers it |
| ⬜ 2 | Correction: the merge at 974c64a0 took the `\|` out of one note in each of two rows, and 9f493c56 repaired the cells but not the character, so each note now says something false about the template | `seal/releases/0.12.0.md:109` | answered | a record correction, corrected at 1cbae560; executed: word-level comparison of all 98 side-edited rows against both parents; also `seal/releases/0.5.0.md:107` |
| ⬜ 3 | Correction: PR #595's body says the conftest removes the token variables, says a name after a redirection is rewritten, and carries no A7 answer | PR #595 body | answered | the PR body is the orchestrator's, rewritten before the pull request goes ready; read via `gh pr view`; the orchestrator owns the body before ready |
| 🟢 | round 1's blocking finding 1 is closed — the suite's `gh` finds a placeholder before `hosts.yml` or the keyring | `tests/conftest.py:341` | confirmed | executed: both cases red with the block cut out, green with it in; the keyring half is read, since this machine keeps no keyring login |
| 🟢 | round 1's finding 2 is closed for `cmd.exe`'s own commands — the five cases pin a built-in's switch as written | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:114` | confirmed | executed: all five went red with `CMD_BUILTINS` emptied; the rest of the class is 🟡 1 |
| 🟢 | round 1's finding 3 is closed — the template states the rule and names examples, and a case refuses the old count | `templates/config.md:201` | confirmed | read; the case passed |
| 🟢 | round 1's finding 4 is closed — both re-stamped rows carry their first reading's date in a note | `seal/releases/0.10.0.md:62` | confirmed | read from `c88b007f`'s diff; also `seal/releases/0.12.2.md:14` |
| 🟢 | round 1's finding 5 is closed in `spec.md` and `plan.md` | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:157` | confirmed | read; the pull request body's half is ⬜ 3 |
| 🟢 | The merge kept both sides' notes, every row re-stamped at the merge carries a note, and no correction marker was dropped | `seal/releases/0.5.0.md:107` | verified | executed: the row comparison, `correction-check` over each side, `evidence-check` 2220 ok; the two characters are ⬜ 2 |
| 🟢 | `NOT_A_GH_TOKEN` breaks no test the other chains added | `tests/conftest.py:335` | verified | executed: the three modules that reach `gh` passed; read: no shipped code branches on a token variable |
| ❓ | Whether `cmd.exe` ends a command name at `=`, `,` or `;` (carried from round 1) | `skills/verify/scripts/broad_gate.py:1434` | ❓ out of verified scope | no `cmd.exe` here; the `windows-latest` leg or a person on Windows answers it |
| ❓ | Whether `cmd.exe` resolves `bin\probe` to `bin\probe.cmd` (Q1, A4; carried from round 1) | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | ❓ out of verified scope | the `windows-latest` leg answers it at the pull request; it was pending when this round looked |

## Paste-ready fixes

```markdown
templates/config.md, §Broad gate — replace "switch (`rd/s/q build`). Any other" with:

switch (`rd/s/q build`). A `/` written straight after any other program's
name is rewritten, because the scan cannot tell a program from a directory:
`xcopy/e` is handed over as `xcopy\e`, which `cmd.exe` cannot find. Write a
blank before the switch (`xcopy /e`), which `cmd.exe` reads the same way and
the scan leaves as written. Any other
```
```markdown
seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md,
Failure directions, first bullet — replace from "The rewrite only ever turns"
to "a row that ran before (round 1's 🟡 2)." with:

  The rewrite only ever turns `/` into `\` inside a command word. Where the
  word before the `/` is a directory, as in `bin/test`, that is the only
  change. Where it is a program, the `/` was that program's switch:
  `cmd.exe`'s own commands (`rd/s/q`, `dir/b`) are left as written, and any
  other program (`xcopy/e`) is rewritten and **denied** — a row that ran
  before now fails to find `xcopy\e`. The template says so and names the
  blank that avoids it. **Corrected 2026-09-25** in round 1's fix pass for
  the built-ins (round 1's 🟡 2), and in round 2's for every other program
  (round 2's 🟡 1).
```
```python
# skills/verify/scripts/broad_gate.py, command_names_backslashed's docstring,
# appended after the "Not rewritten, and named rather than claimed" paragraph:

    **Rewritten, and named rather than claimed:** a switch written straight
    against a program that is not one of `CMD_BUILTINS` (`xcopy/e`). The
    scan cannot tell a program's name from a directory's by its spelling,
    so `xcopy/e` is handed over as `xcopy\\e` and does not run. This one is
    worse than the row as written, and `templates/config.md` §*Broad gate*
    says so and names the blank that avoids it (`xcopy /e`).
```
```python
# tests/test_the_gate_hands_cmd_a_path_it_can_run.py, added to the
# parametrisation of test_only_the_command_names_have_their_slash_turned,
# after the built-in cases:
        # Any other program's switch is rewritten: the gap the template
        # names, pinned so it stays the one it states.
        ("xcopy/e/i a b && bin/test", r"xcopy\e\i a b && bin\test"),
        ("xcopy /e /i a b && bin/test", r"xcopy /e /i a b && bin\test"),

# and to the needles of test_the_template_says_which_positions_are_rewritten:
        "A `/` written straight after any other program's name is rewritten",
        "Write a blank before the switch (`xcopy /e`)",
```
```markdown
seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/changelog.md,
first bullet — after "is that command's switch and is left as written." add:

  A switch written straight against any other program, as in `xcopy/e`, is
  rewritten and stops running; write a blank before it (`xcopy /e`).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_suite_runs_with_gh_logged_out.py`, `tests/test_the_record_is_generated.py`, `tests/test_release_hygiene.py` and `tests/test_the_closer_carries_on_past_a_refusal.py`, in the clone at 9f493c56 | exit 0, 245 passed |
| The two cases in `tests/test_the_suite_runs_with_gh_logged_out.py` with the conftest's `gh` block cut out of the clone (`gh` 2.100.0, login in `hosts.yml`) | exit 1, 2 failed: the structural case listed all four variables; the behavioural case found a login (exit 0, 40 characters, not printed); the clone was restored |
| `handed_to_shell` with `CMD_BUILTINS` emptied, over the five new rows | each built-in's switch was rewritten, so each case would go red |
| `handed_to_shell` with `windows=True` over 16 rows: built-ins, external programs with a switch, `^`/`"`-opened names, a directory named like a built-in | built-ins left as written; `xcopy\e\i`, `findstr\s`, `timeout\t`, `ipconfig\all`, `^rd\s\q`, `"rd"\s\q` rewritten; `path/to/tool` left |
| `evidence-check` in the clone at 9f493c56 | exit 0; 2220 ok, 0 drifted, 0 broken |
| `correction-check --range e1f1d4ec..9f493c56` and `--range 8dcd0d90..9f493c56` | exit 0 and exit 0; no correction marker dropped |
| A word-level comparison of every ledger row either side edited (98), against the merge base, both parents and 9f493c56 | two characters lost (⬜ 2); every other note word kept; one hash new to both parents, with the merge note |
| The full suite, lint and typecheck (the broad gate) | not yet — nobody has run it on this branch, and it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/conftest.py:324` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1375` | round 1's 🟡 2 — fixed |
| round-1 | `templates/config.md:201` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/releases/0.10.0.md:62` | round 1's ⬜ 4 — answered |
| round-1 | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:150` | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:1204` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1236` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1922` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.10.0.md` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
