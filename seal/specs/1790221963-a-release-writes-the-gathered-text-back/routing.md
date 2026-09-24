# 1790221963-a-release-writes-the-gathered-text-back — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/557-a-release-writes-the-gathered-text-back |

Answered 2026-09-24 by the repository owner, before the first edit.

## Why this way

The owner pressed the `automation` preset once for every work item of the
`release: 0.15.1` milestone, and on 2026-09-24 put MichaelYcJo/SpecSeal#555
and #557 into that milestone (\"0.15.1에 넣음\"), which makes this one of its
work items; the preset is read as covering it. Both are the survivor sweep's
release held count that step A (#550) added and could not fix itself because
its run was capped: #557 a release that renames `## Unreleased` or rewords an
entry writes the gathered fragments' text and silences a survivor, #555 the
`lost` guard no case pins. The fix and the case for #557 are already written
and executed in its body.
