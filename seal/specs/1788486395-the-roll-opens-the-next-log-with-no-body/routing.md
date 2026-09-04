# 1788486395-the-roll-opens-the-next-log-with-no-body — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/136-the-roll-opens-the-next-log-with-no-body |

Answered 2026-09-04 by the repository owner, before the first edit.

## Why this way

The change alters what a release-time script writes and what a skill instructs
every future session to do, which is the rung where a spec and a plan come
first. It has a deadline rather than a preference: the push that takes 0.8.0
to `main` is the same push that runs `roll_flow_measurement_issue.py`, so
anything not landed by then applies a release late.

The one question it had was answered in the same batch as these rows. A
repository declares its durable measurement log with a **second label**, not a
config row and not a milestone-name convention — the lookup stays one
`gh issue list --label` call, it reuses the mechanism `flow-measurement`
already uses for the rolling log, and its invariant can be written in the same
shape.
