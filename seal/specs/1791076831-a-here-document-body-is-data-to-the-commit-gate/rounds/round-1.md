# 1791076831-a-here-document-body-is-data-to-the-commit-gate — review round 1

| Field | Value |
|---|---|
| Target SHA | f75ef84b18c31dbfc708b17b2f123ee5fe8df05f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #760 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `0844c21f148f2337725eda6796fd32499dd83e63..dafafb01d6dbddac9a2a7862675e8631dc0583a7`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (`hooks/tokens.py:396`, with `:432`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item `1791076831-a-here-document-body-is-data-to-the-commit-gate` (#739, PR #760), target `f75ef84b` against `release/v0.18.1` at `e141980a`. This is a gate change, so the risk to weigh is a hole, not a false positive: a shape the new rule makes silent that can carry an executed commit, or that runs a file the line wrote while a commit's hooks fire.

Spec compliance first. Check rules R1–R3 and R2a–f as built, which are stricter than the frame in three places that `overview.md` names: every `git` and every local-git `gh` counts as a runner, a pipeline stage that writes a file counts, and the opener's word must match the delimiter. Then check the one corpus row that moved (Q1, confirmed by the owner), Q2's strict `python3 -`, and that `cmdline_base.py` and the two old views are unchanged. Quality second.

Attack the enumeration (1,147,608 shapes, 40,608 silent, 0 bodies executed under bash 3.2 and zsh 5.9) by construction, not by re-running it: name a grammar axis it did not vary. The orchestrator verified the 3 changed test modules (177 passed) and ruff on the 6 changed Python files at the target, and re-read 0.15.1's L1 into this fragment. #752 had drifted it at the base.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_plain_on_a_data_line` drops two of `is_plain`'s per-word guards — `--output` (writes a file R2f/`_writes_a_file` then misses) and a `printf` leading-`-` option — so a data line can hold `git diff --output=<path>` writing a file a later `git commit` runs as a hook, against R2f's "nothing on the line can run that file" and the Grounding claim that R2c reuses `is_plain`'s construction | `hooks/tokens.py:396` (`_plain_on_a_data_line`), with `hooks/tokens.py:432` (`_writes_a_file`) | **fixed** `ae22b8cc` | fixed at ae22b8cc; Verified in the clone: at the target `heredoc_data("cat <<'EOF' \| git diff --no-index --output=h - /dev/null\n…\nEOF")` is `[True]`; `is_plain` rejects both shapes (`--output`, `printf -`). Not driven to an executed commit because `git diff --output` emits diff text, not the verbatim body |

## Paste-ready fixes

```python
# hooks/tokens.py, in _plain_on_a_data_line, immediately after the docstring
# and before `if program == "git":`
    program, args = command.program, command.args
    # Two of `is_plain`'s clauses, carried here so this stays its construction
    # (spec §Grounding): an `--output` option writes a file no redirection
    # names (`git diff --no-index --output=<f> -` puts its output there), and
    # `printf -v` assigns a variable, `PATH` included.
    if any(word.startswith("--output") for word in args):
        return False
    if program == "printf" and args and args[0].startswith("-"):
        return False
    if program == "git":
```
```python
        # R2c carries is_plain's file-writing guards: `git --output` writes a
        # file no redirection names, and `printf -v` assigns a variable.
        ("cat <<'EOF' | git diff --no-index --output=h - /dev/null\nbody\nEOF", [False]),
        ("printf -v PATH %s .; cat <<'EOF'\nbody\nEOF", [False]),
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the 3 changed modules (`test_a_heredoc_body_nothing_runs_is_data`, `test_no_shape_the_base_stops_reads_silent`, `test_an_automation_run_meets_no_commit_prompt`), narrow, at the target | 172 passed |
| `bin/test` on `test_edits_go_through_the_edit_tool`, `test_one_word_one_meaning`, narrow | 29 passed |
| Parser probe `heredoc_data`/`commit_invocations`/`is_plain` over constructed strings (`git diff --output`, `printf -v`, CRLF, `\|& tee`, `git commit -F -`, `<<- 'EOF'`): no shell, no body executed | `git diff --output` and `printf -v PATH` both returned data=True at the target (the finding); flip to data=False with the paste-ready fix |
| `git diff --no-index --output=<f> -` fed a body, in a temp dir | exit 1, wrote `<f>` with the stdin as diff deletion lines — confirms `--output` writes a file that no redirection names |
| Broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
