# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | docs/361-a-release-is-sized-by-a-count-and-cut-by-urgency |

Answered 2026-09-12 by the repository owner, before the first edit.

## Why this way

Issue #361. `Review` and `Destination` are the owner's answers, given as one
batch of three checkboxes with `Implementation`; all three were checked.

`Planning` reads `framer` and nobody was asked for it — `skills/implement/SKILL.md`
§3's ladder decides, and this work item is on its top rung twice over. It
rewrites a rule a person reads and acts on, and it renames the value a release
is sized against: *three or four* stops being a target and becomes a ceiling,
which is exactly the "value someone waits on or is limited by" clause that
puts a change on that rung. A `now` label whose description a reader applies
without asking is the same kind of text. So `spec.md` and `plan.md` are
written before implementing, and the framer holds the pen.

`Review` is worth one sentence because it is not forced. #359 had no choice —
it added a gate, so `CONTRIBUTING.md` §*What a change to a gate must carry*
applied. This adds no gate, and the chain is the owner's call rather than the
document's.

The branch is cut from `release/v0.11.1` at `7e17f5e`, which the repo rule's
merge table requires for this direction, and it squashes back into it. #361
sits in `release: 0.11.1`, so the completeness gate #359 shipped will refuse
the 0.11.1 release pull request until this is merged — the milestone would
otherwise claim work the release does not carry.
