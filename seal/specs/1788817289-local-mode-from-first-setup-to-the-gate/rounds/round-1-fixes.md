# Round 1 — fix pass

Fix commits `1a54687..ca59969`, on
`fix/225-151-local-mode-from-first-setup-to-the-gate` at base `9d2f440`.

Every paste-ready fix in the report was re-run here rather than accepted on
reasoning, and each was seen red first — the ten-call probe for 1, the three
unreadable shapes for 2, the two-worktree clone for 3, and a real
`--separate-git-dir` repository for 4. The reds are in the round record's
probe table.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | 1a54687 |
| 2 | fixed | 1a54687 |
| 3 | fixed | 1a54687 |
| 4 | fixed | 1a54687 |
| 5 | fixed | a3bea92 |
| 6 | fixed | 1a54687 |
| 7 | fixed | a3bea92 |
| 8 | fixed | a3bea92 |

## What each one did

**1** — both prompts are spent once and the session is silent after them.
Measured before: 1 deny, 9 asks over ten ordinary Bash calls. After: 1 deny,
1 ask, 18 silent over twenty. The `ask` had no early return to bound it,
because unlike its sibling this gate fires on every command rather than on a
commit.

**2** — `unreadable()` tells *no answer* apart from *an answer this could not
open*, in the gate only. `hooks/config.py` keeps its four spellings for the
writer, which goes on to write the row either way.

**3** — `marker_dir()` keys the two markers to the root: per work tree for a
shared root, per clone for a local one. The shared half is pinned separately,
because it must not move with the other.

**4** — `repo_of` prefers the caller's tree whenever it shares the item's
clone, compared by common git directory rather than by the paths
`git worktree list` prints; a first entry that is not a work tree is refused
rather than named.

**5** — stated rather than removed. The budget section now carries the
measured per-call cost: one `git rev-parse --show-toplevel` where the sibling
makes none, two in a repository with a root and no row, and still two after
the budget is spent. Removing it means resolving the root once for all three
gates instead of once each, which is a change to three gates and is named as
not this branch's.

**6** — the inert parameter is gone, and the invariant it looked like it was
guarding moved into `git_dir_of`, which now resolves git's answer against the
root. This was not cosmetic by the end: fix 3 introduced `--git-common-dir`,
which answers `.git` from a main work tree, so the resolution became
load-bearing in the same pass that would have dropped it.

**7** — `templates/config.md`'s opening carves out `Mode` for the second
reason as well as the first.

**8** — the changelog fragment names who meets the gate on upgrade: every
repository that opted in before this release, because nothing back-fills the
row.

## Re-enumeration

Four classes swept, from the two causes the report named.

| Class | Members found | Disposition |
|---|---|---|
| A per-command gate with no early return | `mode-gate.py` alone — `commit-review-gate.py` and `worktree-guard.py` both filter by command | fixed above |
| A gate whose unreadable-file fallback lands on its most blocking decision | `mode-gate.py` alone. `routing.py#declarations` folds an undecodable declaration into *no declaration*, and that lands on `ask`, which its own comment argues for | fixed above |
| A marker keyed per work tree for a subject that is per clone | `mode-gate.py` alone. `implementer.py`, `session-lease.py` and `worktree-guard.py` are each about one tree; `optin.py`'s scratch marker is already per clone, deliberately | fixed above |
| `git worktree list --porcelain` read as a root oracle | two: `round_record.py#repo_of`, and `seal.py#other_worktrees` | the first fixed; the second carries a rider at ca59969 |

`seal.py#other_worktrees` returns the git directory as another worktree in a
`--separate-git-dir` repository — measured, and `git -C` on it answers *this
operation must be run in a work tree*. Its caller only prints a note, it
predates this branch, and no finding named it, so it is a rider at the line
rather than a fix in a fix pass.

## Ledger

The S7–S10 row stated the budget the code did not have, so its claim is
rewritten and re-verified with the units this pass added; S1–S4 gains the
`--separate-git-dir` case and the two units that answer it. Sixteen rows
re-verified in the fragment, which is now clean.

One row in `seal/ledger.md` drifted because this pass rewrote the prose above
`templates/config.md`'s table. It was re-read rather than re-stamped: the row
pins the table's shape, and the table is untouched. The nine other drifted
rows there are the ones already deferred to the repository owner, and a
blanket `--reverify` would have closed that deferral without anyone reading a
line.

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — `agent-contract` §2 keeps them out of a fix pass |
| four cases in `tests/test_the_records_can_be_carried_out_and_in.py` fail here, and fail identically at the branch base `86e140f` — #111's, not this pass's | the orchestrator, at the broad gate after `release/v0.9.1` is merged in |
