# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — questions for the planner

<!-- seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Judgments the tickets left open that the tree answered.** Listed so nobody
reopens them; each has its grounds in `spec.md` In or `plan.md` Alternatives.

- **#856's choice between (a) expanding braces and (b) a known limit.** The
  tree gives a third answer: `docs/worktree-guard-spec.md` §A stops a shape
  the guard does not recognise where the tree matters, and a word bash
  expands before git reads it is one. #856 was filed before the inventory;
  #834 part 8 is why (a) is refused (the family did not converge on
  prediction), and the Premise is why (b) is (both measured commands switch
  HEAD silently in an ACTIVE tree). Decided (c), `spec.md` In 5.
  **Confirmed by the repository owner on 2026-10-08:** (c) — an unquoted
  brace expansion in a git word is an unrecognised shape, and the guard
  stops on it.
- **How far the consolidation goes** (#868's last paragraph). The four facts
  with a measured or traced disagreement, and the copies a change to one of
  them touches (`crg.git`); the listed-for-scope copies stay (`spec.md`
  Out).
- **Whether `hooks/cmdline_base.py` is reopened.** No. The brace rule reads
  the frozen words and the judgment text inside the guard; the placement
  function reads the frozen walk's answer. Nothing below the rider changes.
- **Which placement rule is the one.** The guard's, because it is where bash
  runs the segment on both shapes that disagreed (the framer's probe,
  `spec.md` In 1) and the base's on the three pinned chains.
- **Whether `$CLAUDECODE` stays in the stub.** No; the verdict is unchanged
  in every state (`plan.md` Alternatives), and the name exists in
  `steps_around_hooks` only because the stub read it.
- **Whether `answers.given`'s match by `ps` text is in scope.** No; a named
  limit with no owned input to replace it (`spec.md` Out, measured).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | Does a hook process the harness spawns (`session-lease.py` at PostToolUse, the three git stubs' Python through a Bash child's git) see `CLAUDE_PID` in its environment? Measured in a Bash child it is exported and equals the `claude` ancestor's pid; `ps -E` on the session's own `claude` process showed no `CLAUDE_*` variable, so the hook side is unread — NAME NOT IN TREE | a measurement | **yes**: the lease records an observed pid for every session, extension hosts included, and `from_lease` matches it with no `ps` run. **no**: the lease side keeps the walk and only the git-hook side reads the variable (git inherits the Bash child's environment). Either answer builds the same code, because the walk stays under the variable (§13); the answer decides only which route S5 exercises live | **no** is assumed; phase 1 measures it where it can (a Bash child's `env`, read; a hook's environment, by a lease written after phase 4 compared with the walk's answer on a host whose process is not named `claude`, or left `unverified` with the repository owner named) | ⬜ The Bash-child half answered by phase 1 (executed: exported, and equal to the `claude` ancestor's pid); the hook half stays open, `unverified` in `overview.md` with the repository owner named, because no hook of a session can be made to print its environment without changing the installed configuration |
| M2 | How many recorded (command, cwd) pairs hold a git segment with an unquoted brace expansion, by subcommand — In 5's new stop class, tree-blind? | a measurement | a count. It goes into §A's failure-direction paragraph and the changelog; it changes no code. A count above the pairs the rule exists for (`rebase`, `stash`, `worktree`) says which listed subcommands pay the over-stop | none needed; phase 1 counts it by 1791270162 phase 1's method, with the self-check first | ✅ zero of 32,431 pairs, by any subcommand, after a self-check that found all four S11 forms and none of the three S12 forms (`phases/phase-1.md`) |
| M3 | How many recorded pairs do not split and carry `[no-review]` or `[no-parity]` as a substring — In 3's cost, the commands that waived through `has_marker`'s fallback and will meet the refusal? | a measurement | a count, for the changelog. It changes no code: the refusal names the git-native spelling either way | none needed; phase 1 counts it in the same probe | ✅ six pairs under the framed rule, four of them the guard's comment form with an apostrophe after the token; one pair under the rule phase 5 builds, the words read before the split fails (`phases/phase-1.md`, `overview.md`'s divergence row) |
| W1 | How does S10 make `git diff --name-only --cached` fail in a test: a `git` shim first on `PATH` that exits 128 for `diff` and execs the real git otherwise, or an index git cannot read? | the work | the shim is portable and names the failure; a broken index depends on the git version's message. Either way the case is red at 5623d728 | the shim; phase 5 records which | ✅ the shim, a POSIX script exiting 128 for any `diff`; the cases skip on Windows (`phases/phase-5.md`) |
| W2 | Which cases retire with the guard's `has_token` body and `_without_bodies`, and which are rewritten against `tokens.given` (released row T1's four cases in `tests/test_guard_resolves_the_tree_it_judges.py`, and the `base_marker` helper of `test_one_heredoc_shape_is_data_to_the_commit_gate.py`)? | the work | a case whose subject is the removed splitter retires; one that pins the token rule moves to the one reader. `test_s6_neither_read_honours_a_token_the_base_did_not` keeps its `base_marker`, because it asserts the new read is no wider than the base's, which still holds | phase 5 names each in `phases/phase-5.md` | ✅ none retired; T1's four cases pass unchanged through the one reader, and `test_s6_neither_read_honours_a_token_the_base_did_not` compares against both base reads together, because the one reader reads what `has_marker` read and the strict base `given` did not (`phases/phase-5.md`) |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build. This file
  holds none: #856's choice is decided from policy above, with the grounds
  where a reader can overturn them.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
