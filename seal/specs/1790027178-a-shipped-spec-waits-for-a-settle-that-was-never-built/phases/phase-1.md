# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `cc3c4f3b` |
| Ran by | `specseal:smith` on Opus 5 (1M context) — the agent definition names no `model`, and the spawning session passed no override, so the segment inherited the session's model |

## What this phase was asked

**The two readers stop reading released work items.**
`unverified_check.py --baseline` no longer reports a removed released work
item's `overview.md` as this branch's deletion, and still reports one a branch
actually deleted. `gather_changelog.py --check` judges by the `CHANGELOG.md`
markers rather than by a fragment glob that goes empty, and says what it read.

Verified by A1 and A2, each case shown red against the shipped code before it
was committed (§15).

The phase also carried Q3, the one-command measurement: run the shipped
`gather_changelog.py --check` against a scratch root with a fragment removed
and its marker absent, and write the answer into the row.

## What this phase found

**Q3 is answered, executed, and it matches what `spec.md` §*The two readers*
read.** A scratch root holding a `CHANGELOG.md` with one entry and no marker,
and a `seal/specs/<id>/` directory with no `changelog.md` in it, was handed to
the shipped script:

```
$ python3 .github/scripts/gather_changelog.py --check --root <scratch>
0 changelog fragments, all gathered
exit=0
```

It passes having examined nothing. No divergence from the spec, so nothing
goes to `overview.md` for this.

**The discriminator a removal needs is not in the removal.** A folded
directory and a deleted one are the same evidence to `unverified_check.py`:
present at the fork point, absent here. What tells them apart is whether a
policy document absorbed the work item, so the fold's own record is what the
arm has to read — and Q4's default is already that record. The reader is
`folded_items()`, which scans `docs/**/*.md` for `<!-- specs/<id> -->` on a
line of its own. Two properties are load-bearing and both have a case:

- **Line-anchored**, for the reason `fold_ledger.py#is_marked` already pays
  for. Every document describing the convention quotes the marker's shape
  inline, and a substring test would read that prose as a fold and excuse a
  removal nothing absorbed.
- **`docs/` and nothing else.** Widening the scan to the whole tree would let
  a marker in a round record, a changelog fragment, or the removed
  directory's own files at the base excuse the removal.

**The second reader's repair is a count, not a new population.** What was
wrong was never `ungathered()`; it was that an empty glob and *everything
reached the file* print the same sentence. So `--check` now prints the marker
count beside the fragment count — the shape `fold_ledger.py --check` has had
since it shipped — and refuses a corpus carrying neither, which is the state
a fold with nothing behind it produces.

**What phase 2 inherits from this.** `folded_items()` is where the fold-record
convention lives, and `settle.py` is its second reader rather than a second
spelling of it: `chain_check.py` already loads `unverified_check.py` by path
for the same reason, so the precedent for a cross-skill load is in the tree.
A `settle` that re-spelled the scan would be a second convention nobody keeps
in step, which is the defect `marker()` exists in two files to avoid and the
one the ledger's own header warns about.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `gather_changelog.py --check`'s unconditional success on an empty fragment glob | the marker count in the same line, and the refusal beneath it — both in `.github/scripts/gather_changelog.py#main` |
| nothing else | none |
