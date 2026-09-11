# 1789053786-the-plan-is-renumbered-and-eight-tickets-take-rows — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | docs/the-plan-is-renumbered-and-eight-tickets-take-rows |

Answered 2026-09-11, before the first edit.

## Why this way

The same housekeeping `docs/flow.md` names as its own — *deleting a shipped
version's section, or moving items between releases* — and #327 is the
precedent, one release back, declared exactly this way.

**The three rows were not each chosen.** The owner answered the placement
question and left the routing axes unanswered, so each row here is what the
precedent or the ruleset already settles, and this paragraph is where that is
said rather than presented as a decision somebody made:

- **Review** follows #327: no code changes, so there is nothing for a review
  chain to enumerate that reading the diff does not.
- **Implementation** is `the session` by the criterion the `Implementation`
  row itself now carries — this is writing down, not finding out, and the diff
  is one document plus a survivors file.
- **Destination** is not a choice at all. The `release/*` ruleset takes no
  direct push, so a pull request is how any change reaches the release branch.

It exists as a work item rather than a `[no-review]` waiver for the reason
#327 had: a branch that deletes a shipped version's section leaves survivors
that `survivor-check` reports, and the range row that excuses them lives in a
work item's own `survivors.md`.
