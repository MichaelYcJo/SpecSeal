# 1788302682-the-release-check-never-watched-bin — routing

<!-- specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). Committed,
because the check happens at the pull request and CI sees only what is in the
tree. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/the-release-check-never-watched-bin |

Answered 2026-09-02 by the repository owner, before the first edit.

## Why this way

Issue #10: the hygiene check that asks a release pull request to move the
version watches five roots, and `bin/` — the wrappers a user actually
invokes — is not one of them. All three axes were answered in one question
at the start, as the `implement` skill asks; the owner checked all three.
