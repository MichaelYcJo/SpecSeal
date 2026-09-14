# 1789347354-a-wrapped-terminal-line-is-not-one-value — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | fix/309-339-340-a-wrapped-terminal-line-is-not-one-value |

Answered 2026-09-14 by the owner, before the first edit.

## Why this way

#309, #339 and #340 travel as one work item: the first two are the generator's
own reading of a wrapped field and the guard that was supposed to protect it,
and the third is the protocol that defines a conforming tool and never learned
the same thing. Splitting them would fix a parser whose specification still
says the other thing. The work changes what a checker accepts, so it sits on
`skills/implement/SKILL.md` §3's top rung and the framer draws the frame. The
owner answered all three axes in one batch at the cut of 0.11.4, for every
work item this release carries.
