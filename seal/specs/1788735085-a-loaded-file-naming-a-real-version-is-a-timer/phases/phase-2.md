# 1788735085-a-loaded-file-naming-a-real-version-is-a-timer — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `86a6e20` |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Stop `docs/issues-and-milestones.md` naming a real version at line 28, and put
the reason where the next author writing one will read it. The paragraph at
lines 59-64 already carries that reason, so the new line points at it rather
than restating it. Verified by phase 1's case, now green.

## What this phase found

**Pointing at the paragraph is worth more than rewording around the number.**
The sentence is an example of what a milestone answers, so the number could
have been removed altogether — "what is in this release" reads fine. It kept
an illustrative number instead, because a reader who sees a version in this
file needs to meet the rule about versions in this file, and a sentence with
no number gives that rule nowhere to attach. The line now names `1.2.3` and
says the number is illustrative for the reason the paragraph below gives.

**The edit lands in the section above the one that drifted.** The changed
lines are 25-30, inside `## A milestone answers *when*, and takes three
shapes`. The ledger anchor that drifted on this document is
`## A label answers *what it is about*, and survives the move`, spanning
39-87 — drifted by **phase 1's** rename of the test inside that paragraph, not
by this phase's edit. Worth writing down because the two look the same in a
`git status` and the wrong one would have been re-verified against the wrong
claim.

**`docs/flow.md`'s entry for the ticket became false in the present tense.**
It said the document *names* `0.9.0`; after this phase it does not. Moved to
the past tense in the same commit. `docs/flow.md` is itself a record of a
moment and exempt from the check, so nothing forced this — only that a
checklist describing a defect that no longer exists reads as a defect that
still does.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the last real version in the scanned set at or above the running one | nowhere — it was the defect; `docs/issues-and-milestones.md` now names an illustrative value, and the enumeration re-run after every phase confirms nothing replaced it |
