# 1788904490-every-published-reading-carries-three-wrong-rows — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | fix/200-202-193-every-published-reading-carries-three-wrong-rows |

Answered 2026-09-09 by the repository owner, before the first edit, as one
instruction covering the whole of 0.9.4: run the section end to end from the
issues and `docs/flow.md`.

## Why this way

The three issues are one file and one theme — every per-segment reading this
repository has published carries all three defects — so they are one branch,
the shape `[#209 · #210]` and `[#256 · #257]` already used for defects sharing
a file.

Straight to the PR because the owner asked for the release to be carried to
its end in this run, and the session implements rather than a `smith` because
it already holds the 0.9.3 release context the section is measured against.
The trade is stated rather than hidden: no second reader looks at this branch.
