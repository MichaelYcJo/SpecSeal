# 1788220055-the-skill-was-followed-and-the-text-was-still-hard — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | docs/the-skill-was-followed-and-the-text-was-still-hard |

Answered 2026-09-01 by the repository owner, before the first edit.

## Why this way

Issue #9 is prose rules in one file, `skills/writing-style/SKILL.md`. Every
change is a rule a person applies by reading it — no gate's verdict moves, no
hook changes, and the suite does not cover this file's line wrap by deliberate
exclusion.

**The one thing that argues the other way, recorded rather than hidden**: the
file ships with the plugin and both agents follow it, so it is not the
contributor-facing prose that `1788217118-a-gate-change-is-not-judged-on-prompt-cost`
was. The owner was told that and chose the pull request directly. What makes
that defensible is that the change only ADDS routing lines, a recognition
test and a fifth audience; no existing rule is reversed, so an agent reading
the old rules is not made wrong by it.

It runs in a worktree because
`1788212517-the-last-rounds-fixes-are-reviewed-by-nobody` is mid-review in the
shared tree. The two share only `CHANGELOG.md`.
