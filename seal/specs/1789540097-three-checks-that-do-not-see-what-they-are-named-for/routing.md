# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | test/413-418-422-three-checks-that-do-not-see-what-they-are-named-for |

Answered 2026-09-16 by MichaelYcJo, before the first edit.

## Why this way

Three checks this release itself wrote pass while blind to the axis each is
named for, and each was deferred by a capped run rather than judged unworthy.
They are one work item because they are one shape and because the release's
own subject is that shape. A check that starts refusing what it did not refuse
is a gate's verdict changing, which is the ladder's top rung, so the frame is
drawn by a party that does not then build to it.

`#415` is deliberately not here. It is `hooks/config.py` rather than a test
module, and it is a different thing — configuration disappearing without a
message, not a check failing to look. One changelog entry covering both would
teach a reader they are the same.
