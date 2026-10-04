# 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data — review round 3

| Field | Value |
|---|---|
| Target SHA | d7e6a15c58eac91d212761201403d91b76f5bf4d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #769 |
| Broad gate | bcd92935 against 78d795fa |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item `1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data` (#739 and #763, PR #769). This is the verifying round for round 2's fixes, `d5b8a20c..70d48683`, which include the release-branch merge `7671e90f`. Round 1 met the floor, and round 2's fixes were the run's one reopening, so this record ends the run whatever it finds. A finding left open takes the filing ladder, with a `Who answers it`.

Judge whether each round-2 verdict is closed:
- ⬜1: contract §9 and the policy paragraph now say there is no space between `<<` and the delimiter, and that the single-quoted word is not empty. The pin is extended.
- ⬜2: `program_corpus`'s all-near-lines body drops the two lines clause A refuses. It is now accepted and measured in both shells.
- ⬜3 and ⬜4: record corrections.

Check in particular that the contract text, followed literally, now produces a string the reader accepts.

Name findings by mechanism. Write no literal command string that passes either gate silently.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 1 is closed — contract section 9 and the policy say `<<` meets the delimiter with no space and the quoted word is not empty | `skills/agent-contract/SKILL.md:246-249` | confirmed | Executed: 18 strings built slot by slot from the section's text all reduced; the spaced operator, the empty quoted word, a leading-dash word and a doubled space each return None; the four new pin phrases are absent at d5b8a20c and present at the target; the pin module passed. Same wording at `docs/commit-review-gate-spec.md:183-188` |
| 🟢 | round 2's finding 2 is closed — the combined body of every near line clause A admits is in `program_corpus` and measured | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:221-222` | confirmed | Executed: old corpus 192 rows with 0 combined, new corpus 204 rows with 12 combined, which the assertion at lines 248-249 requires; 16 of 18 near lines kept per delimiter; `BANNED` equals the reader's `_BANNED`; program arm green in bash 3.2 and zsh 5.9, both modes, no skips |
| 🟢 | round 2's correction 3 is closed — the changelog fragment states the first line as the reader reads it | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/changelog.md:9-16` | confirmed | Read against `hooks/one_heredoc.py:49-58`; evidence-check's records pass refused no name. Paperwork, outside Needs a fix |
| 🟢 | round 2's correction 4 is closed — the S8 row names the renamed case | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/spec.md:182` | confirmed | Read; the case is defined at `tests/test_an_automation_run_meets_no_commit_prompt.py:188`. Paperwork, outside Needs a fix |
| 🟢 | the release merge changes nothing an earlier verdict rested on, and the E9 and C1 re-reads resolve | `7671e90f` | confirmed | Executed: the merge's diff names four files under other work items' records and the wave-one ledger fragment; this work item's fragment 38 ok and 0 drifted; whole tree 4839 ok and 0 drifted |
| carried | round 1's fix-or-justify finding 1 and finding 3 stay closed — the comment in `main` and the renamed automation case | `hooks/commit-review-gate.py:1268-1273` | confirmed | Carried from round 2: no hook and not that test module changed after d6096dec, per the diff over hooks and tests |
| 🟢 | round 1's findings 2 and 4 stay closed after round 2's fixes touched their surfaces | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:201-277` | confirmed | Executed: the agreement module and the pin module passed at the target |
| ❓ | The program arm's agreement on bash 5.x | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:255-277` | ❓ out of verified scope | Only macOS bash 3.2 ran here. Answered by the CI ubuntu leg at the pull request |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| Four narrow modules at the target through the repository's own runner: the edit-tool module, the one-heredoc-shape agreement, read-exactly and is-data modules | 416 passed in 78s, none skipped, so both arms ran in bash 3.2 and zsh 5.9 |
| Probe: nine first lines built slot by slot from contract section 9, each with a harmless body, with and without a trailing newline | 18 of 18 reduced |
| Probe: the spaced operator, an empty quoted word, a leading-dash word, two spaces between tokens, the terminator written with its quotes, and a sink followed by blank lines | None, None, None, None, None, reduced |
| Probe: the combined-body count under round 2's old corpus and the target's | old 192 rows, 0 combined; target 204 rows, 12 combined; 12 required |
| Probe: the new pin phrases in the contract and the policy at `d5b8a20c` and at the target | absent in both files at `d5b8a20c`, present in both at the target |
| `evidence-check` over the clone, lenient | this work item's fragment 38 ok, 0 drifted; whole tree 4839 ok, 0 drifted; records pass 753 names read, 0 refused |
| Broad gate (full suite, repository lint, typecheck) | not yet — not run by anyone on this branch; the sealer's, and it comes due now |

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
| round-2 | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:213-215` | round 2's ⬜ 2 — fixed |
| round-2 | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/changelog.md:9-13` | round 2's ⬜ 3 — answered |
| round-2 | `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/spec.md:182` | round 2's ⬜ 4 — answered |
| round-2 | `hooks/commit-review-gate.py:1268-1273` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:201-271` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_an_automation_run_meets_no_commit_prompt.py:170-197` | round 2's 🟢 — confirmed |
| round-2 | `skills/agent-contract/SKILL.md:241-253` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_one_heredoc_shape_agrees_with_the_shell.py:251-271` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
