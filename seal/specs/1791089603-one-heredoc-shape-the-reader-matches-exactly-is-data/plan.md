# Implementation Plan: one heredoc shape the reader matches exactly is data (#739, #763)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

Replace PR #760's rule, which trusted the shared splitter's body boundaries,
with a fresh reader for one heredoc shape that it can match byte for byte
(`spec.md` §*The shape*). Where the reader matches, the commit gate reads the
command with the body taken out. Everywhere else it reads exactly as the base
at `e141980a` does.

## Technical context

- **Hook point.** `hooks/commit-review-gate.py#main` calls `commit_invocations(command, cwd)` and then, for the unparsed fallback, tests the substrings `git` and `commit` in `command`. Both take the reduced text where the reader matches. `commit_invocations` is unchanged and so is its recursion (`_reads_a_commit`). `main` also reads `tokens.is_plain(command)`, and `is_git_commit` calls `commit_invocations(command)`. `is_plain` keeps the full command. Whether `is_git_commit` still has a caller is for the work to check; at the base, `grep` finds none in `hooks/` or `tests/`.
- **Why the reduced text and not "skip body k".** #760 skipped the k-th body of `heredoc_bodies(drop_comments(command))`. That index belongs to the shared splitter, and a disagreement about where a body ends moves which text is body. The reduced text has no heredoc in it at all, so nothing below the new reader is asked where a body is.
- **Module.** `hooks/one_heredoc.py`, standard library `re` only. Hooks import siblings by plain name (`import tokens` in the gate), so no registry needs an entry. `tests/test_the_root_migrates_itself.py` walks every `hooks/*.py` for an old ledger path, and a new module passes it by holding none.
- **The agreement test (S6).** Real shells on harmless strings. bash here is 3.2.57 (`/bin/bash`) and zsh is 5.9. No bash 5.x is installed locally. `.github/workflows/test.yml` runs ubuntu, macos and windows legs, so bash 5.x comes from the ubuntu leg. Each shell is located with `shutil.which` and skipped by name where absent.
- **Windows.** The moved row's LEAD path goes through `shlex.quote`. On the Windows leg that is a single-quoted path with backslashes, which is why `WORD` admits one single-quoted word. A backslash is banned only where a newline follows it.
- **What breaks in six months.** Someone widens the grammar, for example with a LEAD assignment, a parameter as the target, or a program after a sink, to cover a habit. Each widening reopens one row of `spec.md`'s disagreement table. The guard is that the policy paragraph names the grammar and its `Enforced by:` line names the agreement test and the edge cases, so a widening that skips them goes red.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Keep #760 and fix each finding (#763, the post-review check) | Each pass found one more place where the splitter and the shell disagree: CR, a cut `#` tail, a backslash-newline, a split `$(`, and runners from `PATH`. The class is open-ended because the splitter was never written to be exact | rejected by the owner, 2026-10-04 |
| B. One shape, read fresh, with the reduced text handed to the base (chosen) | A habit falls outside the grammar and stops as at the base. That cost is a stop, never a silent commit | **chosen** |
| C. B, but carrying #760's `Heredoc` record fields | The fields come out of `_heredoc_split`'s pass, so the decision would rest on the splitter again | rejected |
| D. B with a richer LEAD (assignments, `$(…)`) to cover refusals 2 and 3 as recorded | Proving the opener is at top level after a substitution or a quote needs a quote-aware reader of line 1. That is the shared splitter's job, and its failure | rejected (Q2) |
| E. B with programs allowed after a sink, for example the PR-body-then-`gh` habit | `gh` runs `git` and `ssh -G` from `PATH`, and `ssh -G` runs `Match exec` from a config file a sink could have written. A list of what each later program reads is the list that rotted in #760 | rejected (Q2) |
| F. B with a `gh … --body-file -` consumer (no file written) | It adds no coverage over a lone sink call: with any later program it has the round-trip problem E has, and without one it is two calls, as the sink is | rejected; recorded in `questions.md` |
| G. B, but admit the opener on any line, with earlier lines read the base's way | An earlier line can leave a quote or a heredoc open. Showing it closed needs the splitter | rejected |
| H. Allow a backslash-newline inside the body, where a quoted body keeps it literal | The ban costs a Python body with a line continuation one stop. Lifting it needs a measurement in three shells that this frame does not have | rejected for now; a later loosening with S6 extended |

## Phases

Vertical slices. Each ends with its narrow modules green and every new case
seen red first (contract §15).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The reader, `hooks/one_heredoc.py`: clauses A–F as a grammar over line 1, a raw line split, the `<<` count and the reduced text. Unit cases for every slot and every failing clause (S4's reader half). The agreement test over the generated corpus in bash and zsh, directly and through `eval` (S6) | the new unit module and the agreement module, narrow; red shown by deleting each ban in turn (CR, backslash-newline, the `<<` count, the empty-rest-after-a-sink clause) and seeing a case or the agreement oracle fail | b21cb44a |
| 2 | The gate: `main` (and `is_git_commit` if it has a caller) reads the reduced text for commits. The moved row (Q1) in both modules. Gate cases S1–S5, S7, S8, with #760's must-stop lists and the findings table rebuilt as fixtures | the new gate module, `tests/test_no_shape_the_base_stops_reads_silent.py`, `tests/test_an_automation_run_meets_no_commit_prompt.py`, `tests/test_the_commit_gate_decides_at_the_commit.py` and S9's list, narrow; S1 and S2 red at `e141980a` | 9c48f115 |
| 3 | The words: the two policy paragraphs and contract §9 rewritten, with `Enforced by:` lines; the changelog fragment; the ledger fragment with the re-reads | S10's modules, narrow; `evidence-check` on the fragment | |

The broad gate (full suite, repository-wide lint, typecheck) is the sealer's,
once, after the review rounds settle. No phase runs it.

## Operational impact

None for a deployer: no migration, no new environment variable, no new
dependency. What a session sees changes only for commands of the one shape,
which go from a stop to silent. Every other command keeps its decision.
