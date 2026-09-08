# 1788844400-a-body-naming-two-issues-claims-one — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/167-a-body-naming-two-issues-claims-one |

Answered 2026-09-08 by the repository owner, before the first edit, in the one
batch that answers every work item of 0.9.2.

## Why this way

A closing keyword claims the one number that follows it, and a body writing
`Closes #153 and #150` loses the second silently. Nothing malfunctioned and the
rule is already written down — in the one file whose author needs it least at
the moment the prose is written. So the repair is a check that reports, not
another sentence.

Through the review chain because the change is a new check on a surface a
release depends on, and a check that reports the wrong split is worse than no
check.
