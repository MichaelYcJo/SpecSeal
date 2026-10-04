# 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data — review round 2

| Field | Value |
|---|---|
| Target SHA | d6096dec8fe5bd3a40fc62be0785444b5435a1ba |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #769 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item `1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data` (#739 and #763, PR #769). This is the verifying round for round 1's fixes, `dd555038..bcf841ee`.

For each fix, open it and judge whether its round-1 verdict is closed:
- 🟡1: the comment in `main` now states each reader's direction, and #773 holds the waiver behaviour.
- ⬜2: the agreement test gained a program arm. Its oracle is the set of markers the shell made, which must equal the suffix markers in the LEAD directory that the reduced text names.
- ⬜3: the test renamed to three measured shapes.
- ⬜4: contract §9 now names every slot of the grammar, and its pin is extended.

The new units are a finding surface: `PROGRAM_HEADS`, `SUFFIXES`, `program_corpus`, `suffix_markers`, and the renamed test. In particular, check whether the program-arm oracle could pass while the shell ran a body line. Use harmless markers only.

Name findings by mechanism and coordinate. Write no literal command string that passes either gate silently.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Contract section 9 and the policy say one space between every two tokens and then `<<` and a quoted delimiter, so a session can write a space the reader refuses; the contract also admits an empty quoted word | `skills/agent-contract/SKILL.md:241-245` | open | Executed: the reader returns None for the spaced operator and for an empty quoted word, and reduces the in-shape control. Fails closed, one stop each. The same wording is at `docs/commit-review-gate-spec.md:182-187` |
| ⬜ 2 | `program_corpus` docstring says it measures one body of all the near lines; clause A bans two of them, so that body is never admitted | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:213-215` | open | Executed: 0 of 192 rows hold it; with the banned near lines left out it is admitted (12 rows) and green in both shells, both modes |
| ⬜ 3 | Correction: the changelog fragment's grammar sentence drops the cd's word, the no-leading-dash rule and the heredoc operator, and leaves one line unwrapped | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/changelog.md:9-13` | open | Read against `hooks/one_heredoc.py:49-59`. Paperwork, outside Needs a fix |
| ⬜ 4 | Correction: the S8 row still names the measured-shapes case by its pre-rename name | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/spec.md:182` | open | Read; the case is now `test_three_measured_shapes_are_refused_under_the_press`. Paperwork, outside Needs a fix |
| 🟢 | round 1's fix-or-justify finding 1 is closed — the comment in `main` states the direction for `is_plain` and for the consent reads, and names #773 | `hooks/commit-review-gate.py:1268-1273` | confirmed | Read: the callers it names are at lines 1103, 1353 and 1397; #773 is open and holds the behaviour |
| 🟢 | round 1's finding 2 is closed — the agreement module runs the program arm, and its oracle cannot pass while the shell runs a body line | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:201-271` | confirmed | Executed: a shell made to run a body line was caught on 12 of 12 eligible rows; reader mutations went red (12 and 96 of 192); the module passed |
| 🟢 | round 1's finding 3 is closed — the case, its header and the ledger anchor say three measured shapes | `tests/test_an_automation_run_meets_no_commit_prompt.py:170-197` | confirmed | Executed: the module passed; this work item's ledger fragment 38 ok, 0 drifted |
| 🟢 | round 1's finding 4 is closed — contract section 9 names every slot, and its pin covers each one | `skills/agent-contract/SKILL.md:241-253` | confirmed | Executed: the extended pin is red on the section at `dd555038` and green at the target |
| ❓ | The program arm's agreement on bash 5.x | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:251-271` | ❓ out of verified scope | Only the macOS bash 3.2 ran here. Answered by the CI ubuntu leg at the pull request |

## Paste-ready fixes

```markdown
word, `tee` or `tee -a` and one word, or `python3 -` followed by any number of
words; then `<<` and, with no space between them, a delimiter of letters,
digits and underscores in single quotes. A word is either letters, digits,
`_`, `.`, `/` and `-` that do not start with `-`, or one single-quoted word
holding no quote and no newline and not empty.
```
```markdown
one word and `&&`; then the consumer; then `<<` and, with no space between
them, a delimiter of letters, digits and underscores in single quotes. The
consumer is `cat` with `>` or `>>` and one word, `tee` or `tee -a` and one
word, or `python3 -` and any number of words, where a word is a path of
letters, digits, `_`, `.`, `/` and `-` not starting with `-`, or one
single-quoted word that is not empty and holds no quote or newline. The body
```
```python
            "letters, digits and underscores in single quotes",
            "`<<` and, with no space between them, a delimiter",
            "holding no quote and no newline and not empty",
```
```python
        bodies_ = [[line, f": > m{i}"] for i, line in enumerate(near)]
        # Clause A refuses a body holding a carriage return or a backslash
        # before a newline, so the body of all of them keeps the rest.
        kept = [line for line in near if not any(b in line + "\n" for b in BANNED)]
        bodies_.append([x for i, line in enumerate(kept) for x in (line, f": > n{i}")])
```

## Executed probes

| What was run | Result |
|---|---|
| Six narrow modules at `d6096dec` in a scratch clone through the repository's own runner: the three one-heredoc-shape modules, the edit-tool module, the automation module and the no-shape-reads-silent module | 484 passed in 57s, none skipped, so the program arm ran in both shells |
| Probe P1: the program corpus counted | 192 rows; 16 admitted near lines per delimiter; combined body admitted in 0 rows |
| Probe P2: bash run directly, with the trailing-blank near line turned into an exact terminator in what the shell received, and the reader's expectation for the real command | 12 of 12 eligible rows caught; the shell made the body's marker beside the suffix's |
| Probe P3: reader mutated to strip trailing blanks before the comparison, zsh through `eval` | 12 of 192 disagree, red |
| Probe P4: reader mutated to keep one suffix line, bash through `eval` | 96 of 192 disagree, red |
| Probe P5: the reader on a spaced heredoc operator, on an empty quoted word, and on the in-shape control, all with a harmless body | None, None, reduced |
| Contract pin at `dd555038`'s section 9 | Red on the first slot phrase |
| The ⬜ 1 fix: pin extended with two phrases, then the proposed paragraph | Red on the current section; green with the proposed paragraph (module 11 passed) |
| The ⬜ 2 fix applied to `program_corpus` | 204 rows, 12 of them combined; the program arm green in bash and zsh, both modes |
| `evidence-check` over the clone's tree, lenient | This work item's fragment: 38 ok, 0 drifted. 10 drifted rows sit in three other work items' fragments (1791076830, 1791076832, 1791076833), on files this branch does not touch, so they are the base's state. Under `--strict` they make the tree NOT SEALED |
| Broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/commit-review-gate.py:1268-1270` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:24-26` | round 1's ⬜ 2 — fixed |
| round-1 | `tests/test_an_automation_run_meets_no_commit_prompt.py:170` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:241-245` | round 1's ⬜ 4 — fixed |
| round-1 | `hooks/one_heredoc.py:45-106` | round 1's 🟢 — confirmed |
| round-1 | `hooks/commit-review-gate.py:1271-1288` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_one_heredoc_shape_agrees_with_the_shell.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/one_heredoc.py:91-95` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_no_shape_the_base_stops_reads_silent.py` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
