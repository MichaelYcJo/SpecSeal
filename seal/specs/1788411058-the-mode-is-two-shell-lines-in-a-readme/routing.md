# 1788411058-the-mode-is-two-shell-lines-in-a-readme — routing

<!-- seal/specs/1788411058-the-mode-is-two-shell-lines-in-a-readme/routing.md
— the answer given before the first edit, in the batch the `implement` skill
collects (§1). Committed, because the check happens at the pull request and CI
sees only what is in the tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/the-mode-is-two-shell-lines-in-a-readme |

Answered 2026-09-03 by the repository owner, before the first edit. The same
three answers every 0.5.0 work item has carried; the owner's standing
instruction for this flow is to proceed at them rather than ask again.

## Why this way

Issue #104, added to 0.5.0 after the other four merged. It belongs in this
release rather than the next because 0.5.0 is the release that introduces the
two modes, and it is also the release where every repository coming from the
0.3.x layout lands in shared mode without being asked. A switch that exists
only as two shell lines in a README leaves those repositories a whole release
cycle with nothing to run.

It moves committed files and runs `git rm -r --cached`, so it goes through
the chain. The pull request lands on `release/v0.5.0`, and the release
preparation follows it.
