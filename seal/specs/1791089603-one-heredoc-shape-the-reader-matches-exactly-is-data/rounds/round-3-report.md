# Round 3 report — 1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data

Target SHA: `d7e6a15c58eac91d212761201403d91b76f5bf4d`. Base: `release/v0.18.1` at
`78d795fa`. Scope: round 2's fix range `d5b8a20c..70d48683`, including the
release-branch merge `7671e90f`. This is the verifying round of the one
reopening, and the run's last.

Every probe ran in a `git clone --no-local` of the worktree at the target,
under this session's scratchpad, and nothing was written in the worktree but
this file. No command string that commits was built or run: every probe body is
harmless text, and the gate's own decisions were judged through the agreement
modules, which use `: > NAME` markers.

## Summary

All four round-2 verdicts are closed. Contract section 9 and the policy
paragraph, followed slot by slot, now produce first lines the reader admits,
and both readings round 2 found the text allowed (a space after `<<`, an empty
quoted word) are now excluded in words and pinned. `program_corpus` now
carries its combined body, and the program arm measures it in bash and zsh.
The release merge changed no code and no document an earlier verdict rested
on. Nothing this round opened needs a fix.

## Round 2's findings

**Finding 1 (contract and policy wording) is closed.** The contract at
`skills/agent-contract/SKILL.md:246-249` and the policy at
`docs/commit-review-gate-spec.md:183-188` now say that `<<` and the delimiter
have no space between them, and that the single-quoted word is not empty. That
is what `hooks/one_heredoc.py:51` and `hooks/one_heredoc.py:58` require.

Executed: I built nine first lines from section 9's text alone, one per slot
the paragraph names. They cover each of the four sinks, `python3 -` with and
without words, `cd` with a plain and with a quoted word, and a delimiter with
digits and an underscore. Each was given a harmless two-line body and a
terminator, once with a trailing newline and once without. `reduce` admitted
all 18. The readings the text now excludes all come back `None`: a space after
`<<`, an empty quoted word, a word starting with `-`, and two spaces between
tokens.

The pin `test_the_rule_names_the_one_heredoc_shape_it_does_not_read` grew by
two phrases for the contract and two for the policy. All four phrases are
absent from both files at `d5b8a20c` and present at the target, so the
extended pin would have been red on the old text. It is green at the target.

**Finding 2 (the combined body) is closed.** `program_corpus` at
`tests/test_one_heredoc_shape_agrees_with_the_shell.py:221-222` now leaves out
of the combined body the near lines clause A refuses. A new assertion at lines
248-249 requires the combined body in every delimiter, head and suffix
combination.

Executed: the old corpus yields 192 rows and 0 combined rows. The new corpus
yields 204 rows and 12 combined rows, which is 2 delimiters times 3 heads times
2 suffixes, so the new assertion is red on the old code and green on the new
one. Per delimiter, exactly the carriage-return and trailing-backslash near
lines are dropped (16 of 18 kept). The test's `BANNED` is the same tuple as
the reader's `_BANNED`. `test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body`
ran in bash 3.2 and zsh 5.9, directly and through `eval`, with no skips, so
the combined body is now measured in both shells.

**Corrections 3 and 4 are closed.** The changelog fragment now states the
first line as `hooks/one_heredoc.py:49-58` reads it: `cd` with one path, no
space after `<<`, no leading `-`, and a non-empty quoted word. `spec.md`'s S8
row names `test_three_measured_shapes_are_refused_under_the_press`, which is
defined at `tests/test_an_automation_run_meets_no_commit_prompt.py:188`.
`evidence-check`'s records pass read 753 names in the unreleased work items
and refused none.

## The release merge and the ledger re-reads

`7671e90f` brought four files: three under another work item's `seal/specs/`
directory and the wave-one ledger fragment. No hook, test, policy document or
skill changed in the merge, so nothing an earlier verdict rested on moved.
`70d48683` re-pinned this work item's E9 and C1 rows to the policy heading's
new content hash. Executed: this work item's ledger fragment reads 38 ok and 0
drifted. The whole tree reads 4839 ok and 0 drifted, so the ten drifted rows
round 2 saw in the base are gone after the merge.

## Round 1's findings

Neither `hooks/commit-review-gate.py` nor
`tests/test_an_automation_run_meets_no_commit_prompt.py` changed after round
2's target `d6096dec`. Round 1's fix-or-justify finding 1 (the comment in
`main`) and finding 3 (the renamed case) therefore stand where round 2
confirmed them; I carried those two rather than re-deriving them. Round 1's
findings 2 and 4 sit on the surfaces round 2's fixes touched, so I re-checked
them, and both modules are green at the target.

## Asked in particular — does the contract, followed literally, give a string the reader accepts

Yes, for every slot the paragraph names (executed, above). I considered two
readings that remain and opened neither.

- **The terminator written with its quotes.** "The first line exactly equal
  to the delimiter" could be read as a line holding the quoted delimiter. The
  reader then finds no terminator and returns `None`. Bash does not end the
  body on that line either, so the reader and the shell agree, and the gate
  reads such a command as shell, as before. That is a stop, never a silent
  pass.
- **"No second `<<`" without "outside the body".** The contract at
  `skills/agent-contract/SKILL.md:251-252` omits the qualifier the policy
  carries at `docs/commit-review-gate-spec.md:191`. That is stricter than the
  reader, so a session following it literally writes nothing the reader
  refuses. It only under-promises for a body that quotes `<<`, and such a
  session falls back to the `Edit` tool, which section 9's first reason
  already asks for.

Neither would ship a defect, and both are worded the way rounds 1 and 2 left
them, outside this round's fix range.

## Regression tests to plant

None. The two cases round 2's fixes needed are in the tree, and each was shown
red against the code before its fix (above).

## Facts for the evidence ledger

None new. The fragment's 38 rows resolve at the target.

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

Needs a fix: no
Loses a record or crashes: no

The rounds have settled with nothing open but a ❓ the CI leg answers, so the
broad gate comes due: what comes due is the sealer's spawn.

## Proof block

Files opened this round:

- `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/rounds/round-2.md`
- `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/rounds/round-2-report.md`
- `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/changelog.md`
- `seal/specs/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data/spec.md` (the S8 row, through the diff)
- `seal/ledger/1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data.md` (through the diff)
- `hooks/one_heredoc.py`
- `skills/agent-contract/SKILL.md:225-275`
- `docs/commit-review-gate-spec.md:165-215`
- `tests/test_one_heredoc_shape_agrees_with_the_shell.py:1-80` and `:150-290`
- `tests/test_edits_go_through_the_edit_tool.py` (the hunk at 285-305, through the diff)
- `skills/code-review/scripts/chain_check.py:468-474` and `:1762-1777`
- `docs/round-record-spec.md` (the `Contract changes` lines, through a search)
