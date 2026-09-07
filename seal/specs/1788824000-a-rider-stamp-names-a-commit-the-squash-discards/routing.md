# 1788824000-a-rider-stamp-names-a-commit-the-squash-discards — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | fix/239-a-rider-stamp-names-a-commit-the-squash-discards |

Answered 2026-09-08 by the orchestrating session, before the first edit.

## Why this way

This is the one item of the 0.9.1 run whose review answer differs from the
batch, and the difference is stated rather than assumed.

`release/v0.9.1` is red: `test_every_rider_stamp_names_a_commit_this_branch_can_reach`
refuses a stamp naming `cedc58e`, a commit #226's squash discarded. Every pull
request into the release branch fails on it until it is repaired, so the repair
blocks the rest of the release rather than queueing behind it.

The change is one line, and the test that failed is the review: it asserts
exactly the property the new stamp has to have, it was seen red, and it goes
green only if the stamp resolves. A review round reads the same one line and
the same one assertion.

What a round WOULD be for — whether a stamp should name a commit at all, when
this repository's own merge rules rewrite commits at every boundary — is not
answerable in a one-line repair and is filed as **#239** with three candidate
directions. That is where the judgment belongs, and it is 0.9.2's.
