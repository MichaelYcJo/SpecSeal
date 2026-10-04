# 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data — review round 1

| Field | Value |
|---|---|
| Target SHA | 68eaf258aca00ef7c27e5081d821e5aa68bd7642 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #769 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1, the sentence in the comment in `main` that calls the consent read on the raw text safe |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item `1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data` (#739 and #763, PR #769). Target `68eaf258`, against `release/v0.18.1` at `edee5ca2`. This is the redesign of #760, which four review passes broke.

The change is a narrowing of the gate's trust. The risk to weigh is a string the new reader accepts as the shape, where the shell runs something the gate then no longer reads.

**Spec compliance first.** Check clauses A–F as built in `hooks/one_heredoc.py`, and check that the reader uses none of the shared splitter's units. Check the reduced text `main` hands to `commit_invocations`, and that `is_plain` and the consent read still see the raw text.

**Then attack the shape by construction.** For each clause, list what the shell does on every input the clause admits:
- the `cd WORD` slot;
- the consumer slot;
- the delimiter;
- the terminator line;
- what follows a python terminator.

Measure with the gate's decisions and with harmless marker strings run through the repository's own agreement test. Never run a string that would make a commit.

**Then #760's recorded classes.** Its round reports and its `post-review-check.md` state them by mechanism: split substitution, continuation in the delimiter, CR before the terminator, a comment tail on a terminator line, and gh running `ssh` and `git`. Check each is closed.

**Quality second.**

Records and your report name mechanisms and coordinates only, never a literal command string that passes either gate silently. Two reviewers were stopped by a safety classifier for writing such strings into a report.

The orchestrator has already verified the changed modules and the hygiene modules (846 passed) and ruff on the changed Python files at the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `main`'s comment claims the consent read on the raw text is safe ("can only keep the reading in"), but a waiver token inside a data body silences a suffix commit | `hooks/commit-review-gate.py:1268-1270` | open | Executed: the program shape with the token in a Python string literal and a suffix commit to an undeclared repository was silent, and deny without the token. Identical at `edee5ca2`. The behaviour is deferred; the sentence is this diff's |
| ⬜ 2 | Agreement module claims a program body cannot carry the oracle's lines, so clauses E and F (program arm) have no shell measurement | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:24-26` | open | Executed probe: program heads with markers ran in bash and zsh, both modes, with no disagreement, which shows the oracle is possible |
| ⬜ 3 | Test name and section header say four measured shapes; three remain | `tests/test_an_automation_run_meets_no_commit_prompt.py:170` | open | Read: `measured` returns three rows |
| ⬜ 4 | Contract §9's summary omits the WORDs after `python3 -` and the WORD alphabet | `skills/agent-contract/SKILL.md:241-245` | open | Read against `docs/commit-review-gate-spec.md`'s paragraph and `_PROGRAM`. Fails closed, at the cost of a stop |
| 🟢 | Clauses A–F built as `spec.md` §*The shape* states, with no import beyond `re` | `hooks/one_heredoc.py:45-106` | confirmed | Read, and the unit module passed |
| 🟢 | `main` hands the reduced text to `commit_invocations` and the `unparsed` test; `is_plain` and the consent read see the raw text | `hooks/commit-review-gate.py:1271-1288` | confirmed | Read |
| 🟢 | Every admitted sink string is cut where bash 3.2 and zsh 5.9 cut it, directly and through `eval` | `tests/test_one_heredoc_shape_agrees_with_the_shell.py` | confirmed | Executed: 400 passed across the three new modules |
| 🟢 | The program's suffix runs exactly as the reduced text says, and no body line runs | `hooks/one_heredoc.py:91-95` | confirmed | Executed probe: 4 heads, 11 near lines, 2 shells, 2 modes, no disagreement |
| 🟢 | #760's five recorded classes are each closed by a named clause | `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` | confirmed | Read per clause, and `test_what_760_found_still_stops` passed |
| 🟢 | The program class removes no stop the base had for a Python program that commits | `hooks/one_heredoc.py:91-95` | confirmed | Executed: the `os` and `subprocess` forms were silent at `edee5ca2` and at the target; a shell-fed body stayed deny at both |
| ❓ | Bash 5.x agreement (Q3) | `tests/test_one_heredoc_shape_agrees_with_the_shell.py` | ❓ out of verified scope | Only bash 3.2 exists on this machine. Answered by the CI ubuntu leg at the pull request |
| ❓ | The moved row reaches the shape on Windows (Q4) | `tests/test_no_shape_the_base_stops_reads_silent.py` | ❓ out of verified scope | No Windows host here. Answered by the CI Windows leg at the pull request |

## Paste-ready fixes

```python
    # Where the command is the one heredoc shape `hooks/one_heredoc.py`
    # matches byte for byte, every reading for a COMMIT reads it with the body
    # taken out (#739, #763): a file's text, or a Python program on stdin,
    # which `docs/commit-review-gate-spec.md` already leaves unread as a
    # program whose operands are a script. Everywhere else it is the command
    # as written, exactly as before. Nothing below is asked where a body is,
    # because the reduced text holds none. `is_plain` keeps the command as
    # written, because reading more of it can only keep the reading in. The
    # consent reads (`has_marker`, here and in `judge`) also keep it, as at
    # the base, and that runs the other way: a waiver token inside the body
    # still counts, although the body is data to the commit reading. That is
    # the base's behaviour, left to the consent reads' own work item.
```

## Executed probes

| What was run | Result |
|---|---|
| The three new modules, narrow, in a scratch clone at `68eaf258` with a `uv` venv | 400 passed in 21s (bash 3.2.57, zsh 5.9 present) |
| Probe A: program heads (no argument, quoted plus PLAIN arguments, quoted LEAD, PLAIN LEAD), each with 11 near-terminator body lines followed by a marker line, and a suffix marker. Run in bash and zsh, directly and through `eval`; harmless colon-redirect markers only | No disagreement: only the suffix marker existed, in the LEAD's directory. Reduced text equals head plus suffix in every case |
| Probe B: 13 constructed strings handed as JSON to the gate hook at the target and at `edee5ca2` (extracted with `git archive`). Session declared; commit targets opted in and undeclared. No string was run by a shell | Program with the token as a body shell word, suffix commit: silent / silent. Token in a Python string literal: silent / silent. No token: deny / deny. Sink whose body commits: silent / deny (the intended change). Near-terminator then commit, sink: silent / deny (the intended change). Quoted WORD holding `<<`: deny / deny. Sink followed by spaces: deny / deny. Python `os` and `subprocess` commits: silent / silent. Shell-fed body: deny / deny |
| Broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A waiver token in a heredoc body the gate now treats as data still waives the commit arm for a commit elsewhere on the command (🟡 1's behaviour, the same at `edee5ca2`) | Candidate for a new issue: the consent reads, which `spec.md` §*Scope* puts outside this ticket | the repository owner |
