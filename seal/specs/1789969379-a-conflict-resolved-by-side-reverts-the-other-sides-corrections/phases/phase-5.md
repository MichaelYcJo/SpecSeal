# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 7d404216 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

The documents: `CLAUDE.md`, `CONTRIBUTING.md`,
`skills/evidence-check/SKILL.md`, the changelog fragment and the
`seal/ledger/` fragment. A8, red when either document stops saying it, and
the ledger fragment's anchors resolving under `evidence-check --strict`.

## What this phase found

**A8's case matches sentences, not lines, and that is not a detail.** Both
documents wrap at 88 columns — `tests/test_docs_line_wrap.py` enforces it —
so every sentence worth pinning is split across two lines and a raw substring
test finds none of them. The first run of A8 went red for exactly that
reason, on a document that said the thing. Collapsing the whitespace before
matching is what makes the needle a sentence.

**What the needles are is the same judgment the check itself rests on.** They
are the instruction and the argument behind it — *resolve it hunk by hunk and
read both sides*, `--ours`, `--theirs`, *resolved in opposite directions*,
*byte-identical to a row nobody touched* — rather than whole paragraphs.
Pinning the prose word for word would go red on a rewording that still says
it, which is the failure this work item's own marker matching exists to
avoid. The case is the rule applied to itself.

**The skill's section says when the command runs, and one case exists to keep
it saying so.** A check whose moment nobody states gets run at the wrong one,
and this one has exactly one moment: the merges it reads stop existing at the
squash. Driving that case red needed every occurrence of `squash` removed
from the skill, because the word appears more than once — which is the right
shape, since a single mention is not a statement anybody meets.

**The ledger fragment's anchors were written with `00000000` and filled by
`evidence-check --reverify`.** All fourteen resolve, and `seal/ledger.md` was
not touched: `git diff --stat` on it is empty after the reverify run. That
matters for this work item more than for most — its whole subject is a
correction silently lost from that file, and a branch that re-stamped rows it
had not read would be the thing it is about.

**Nothing on this branch re-read a row of the shared file**, so no `Re-read`
marker is owed there. The eight new rows are claims about code this branch
wrote, and they live in the fragment where the convention puts them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — both documents gain paragraphs and neither loses one | none |
