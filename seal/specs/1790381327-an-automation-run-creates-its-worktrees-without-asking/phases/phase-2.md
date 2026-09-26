# 1790381327-an-automation-run-creates-its-worktrees-without-asking — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | e7a7d643 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Row 0 of `guard_worktree_creation` reads record-or-answer on both entry
points, with the record's existing effect. `main` and `judge_creation` carry
the payload's `transcript_path`. The unreachable `ask` tail and its rider are
removed, so `consented` takes `allow` or `silent` only.
`docs/worktree-guard-spec.md` §B row 1 and §*Creation consent* (the fourth
column, the budget) updated with `Enforced by:` lines. Verified by S1, S2, S3
and S9 through `wg.main()`, each seen red against the phase-1 tree, and S5 as
the guard's test files passing with no edit outside the cases this phase
rewrites. Q4, if the build meets it, answered here.

## What this phase found

**The code landed in `a9f173ec`, the docs in `e7a7d643`.** Row 0 calls
`worktree_consent.consent`, which returns `record`, `answer` or nothing. The
`allow` reason says which of the two it read, in both languages, because they
are two different facts a person may want to check.

**S9 and S8 cannot be red against the phase-1 tree**, and the plan asked for
S9 to be. Both pin behaviour that must not move: the phase-1 tree already
denies the switch and already ignores a malformed transcript, because it reads
no transcript at all. Each was seen red by a mutation instead. S9 went red
when the switch ladder was made to exit on consent. S8 went red when the
parser's `ValueError` was let through. The first S8 mutation stayed green: the
malformed lines in the cases carried neither word the prefilter looks for, so
they never reached the parser. The cases now use a line cut off mid-write
that carries both words.

**Seen red against the phase-1 tree** (`cf9e4c82`'s `hooks/worktree-guard.py`):
6 of the 8 new cases fail, namely S1, S2, the placement case, S3, the
payload-path case and the reason pin. The other two are S9 and S8 above.
Mutations on the new tree:

| Mutation | Red cases |
|---|---|
| row 0 reads the record alone | S1, S2, placement, S3, payload path |
| `judge_creation` does not pass `transcript_path` down | payload path |
| the answer's `allow` reason is the record's | the reason pin |
| the switch ladder exits on consent | S9 |
| a malformed line raises | S8, both the reader case and the guard case |

**The plan's one-`Enforced by:`-line-per-clause does not fit the fold shape.**
`docs/worktree-guard-spec.md` §*Creation consent* sits under one fold marker,
and `tests/test_a_folded_statement_names_what_enforces_it.py` holds a marked
statement to exactly one `Enforced by:` line, running to the next heading. A
second line turned it red. The new cases were added to the statement's
existing line instead, and the fold shape won over the plan's wording.

**The folded statement's own rule sentence had to change.** It read *the first
worktree creation in a session is the question*, which is no longer true for
a session whose person pressed `automation`. The bold opener and the
*what changes is one invariant* sentence now say so.

**Two stale sentences, twins of §B row 1.** `only_creates_a_worktree`'s
docstring and §*Creation consent*'s *Why the allow is bounded* both said a
compound gets an `ask`. The code has answered `silent` since #257. Both were
corrected in this phase. Editing that docstring drifts
`seal/releases/0.9.1.md`'s two `only_creates_a_worktree` rows, and phase 4
re-reads them.

**Q4 was not met, and the build cannot meet it from here.** Whether a
subagent's `PreToolUse` payload carries the parent's `transcript_path` or its
own `subagents/…` path is visible only to a hook. The guard that runs in this
session is the installed 0.15.4 copy, not this branch's, and nothing in the
repository logs a payload. Either answer lands on rule 1's second form:
`test_a_subagents_own_path_falls_back_to_the_parents_transcript` covers the
case where the path names the subagent's own file.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the `ask` tail of row 0 (*this command does more than create a worktree, so the confirmation covers the rest of the command line*) and its `# RIDER:` | none — no production caller reached it since #257, and the rider asked for this decision |
| `consented`'s `ask` default | `silent`, the value the Bash compound arm already passed |
