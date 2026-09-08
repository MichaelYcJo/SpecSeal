# 1788817289-local-mode-from-first-setup-to-the-gate — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `02ef9d7`, `589cf25` |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Make `round_record.py#where` resolve a work item that sits under the common
git directory instead of refusing it, resolving the root the way the rest of
the plugin does rather than deriving it from the item path. Every case seen
red first.

## What this phase found

**The refusal is git declining a question, not git failing to recognise a
path.** `git -C <path inside .git> rev-parse --show-toplevel` exits 128 with
`fatal: this operation must be run in a work tree`. No amount of normalising
the argument gets an answer out of it, so the fix had to ask a different
question. `--git-common-dir` and `worktree list --porcelain` both answer from
that same path — measured in a main tree and in a linked worktree — and
`worktree list` prints the main worktree first.

**Nothing may take `dirname` of the common git directory.** It is the
repository root only for a plain `.git`, and `--separate-git-dir` puts it
anywhere. That was the tempting one-line fix and it holds on the author's
machine and not on the one that reports the bug.

**The item cannot say which tree a run is about, because one local root
serves every worktree of the clone.** A round record names a HEAD and a
branch, so the caller's tree is the answer; the main tree is the fallback for
a caller outside the clone. Phase 3 hit the same question from the other side
and answered it the same way.

**The shared-mode fast path is behaviour, not an optimisation** — found by
mutation, not by reading. Dropping `reader.repo_root(item)` left all six cases
green and silently moved a shared item inside a linked worktree to the MAIN
tree, because the fallback takes git's first entry. A shared root lives in one
tree, so the item names its own worktree; the case that pins it exists because
the mutation survived.

**The class was enumerated, and it has one other member that is not this
defect.** `skills/verify/scripts/unverified_check.py:573` derives a root the
same way, and only under `--baseline`. A local-mode root has nothing committed
for a baseline to compare against, so its refusal there is correct rather than
the same bug; it is named in the handover rather than changed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the joint refusal `--item … is not a directory inside a git repository` | split in two at `round_record.py#where`, each half naming which of the two things failed; `tests/test_local_mode_reaches_the_review_chain.py` pins both |
