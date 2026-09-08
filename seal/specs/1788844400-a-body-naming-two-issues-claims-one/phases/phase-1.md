# 1788844400-a-body-naming-two-issues-claims-one — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 9a3f9d1 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Build the narrow version of #167: a check on a pull request body that reports
rather than fails, flagging a closing keyword followed by a number and then
another `#N` in the same sentence carrying no keyword of its own, and
reporting every number the body claims and every one it merely mentions as two
lists. Settle what a sentence is and write the choice down. Find where the
hygiene workflow already reads a body and reuse it. Follow the shape of
`gather_changelog.py` and `fold_ledger.py` rather than inventing one.

## What this phase found

**The hygiene workflow reads no pull request body.** The ticket and the
handoff both say to reuse where the body is already read; opened and measured,
`.github/workflows/hygiene.yml` reads `github.base_ref`, the git history and
files in the tree, and `github.event.pull_request.body` appears nowhere in the
repository. So this is a first read, not a reuse. What is reused instead is
the **job**: the step joins the workflow that already runs on every pull
request, so it needs no new workflow, no new trigger and no new token scope.

**Length-preserving masking is what the sibling does not do, and it earns its
place twice.** `close_issues_on_release.py` blanks a fence or a code span to a
single space, which is correct for a `findall` and wrong here: a fence
collapsing to one space would splice the line above it onto the line below,
and this module segments by line structure. The second payment was not
planned — because offsets survive the mask, the warning can quote the sentence
from the **original** body rather than from the blanked copy. The first
acceptance run showed why that matters: the masked quote read *"they stay open
until the release reaches , where closes them"*, which is not a sentence the
author would recognise as theirs.

**Only a number AFTER the claim is a candidate.** `Part of #11, and this
closes #22` is not somebody losing a claim, and warning about it would spend
the false-positive budget on the shape nobody writes.

**The nearest preceding claim is the one named**, not the first in the
sentence: with two keywords ahead of it, naming the first sends the author to
the wrong keyword.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
