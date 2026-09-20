# 1789919879-the-outside-contributor-has-no-procedure — routing

| Axis | Answer |
|---|---|
| Answered by | the `automation` preset |
| Automation | yes |
| Implementation | smith |
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Branch | docs/the-outside-contributor-has-no-procedure |

Answered 2026-09-20 by the owner, before the first edit. The preset was
pressed; the four rows above are what it expands to, recorded because a
pressed preset and four ticks by hand are otherwise the same bytes.

## Why this way

A first-time contributor opened #443 against `main`, because nothing this
repository shows a contributor says where a pull request goes. The hygiene
gate then refused it with `this PR changes what ships but leaves plugin.json
at 0.12.0` — a message that is correct for the person cutting a release and
points a contributor at the wrong file entirely. Neither half is the
contributor's mistake.

The work changes a gate's refusal text, which puts it on
`skills/implement/SKILL.md` §3's top rung, so the framer draws the frame and
the review chain runs. The owner answered every axis in one batch at the cut
and asked for the run not to stop again.
