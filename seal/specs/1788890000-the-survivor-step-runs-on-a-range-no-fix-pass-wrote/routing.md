# 1788890000-the-survivor-step-runs-on-a-range-no-fix-pass-wrote — routing

| Axis | Answer |
|---|---|
| Review | straight to the PR |
| Destination | open the pull request |
| Implementation | the session |
| Branch | fix/the-survivor-step-runs-on-a-range-no-fix-pass-wrote |

Answered 2026-09-08 by the repository owner, before the first edit, in the one
batch that answers every work item of 0.9.3. This item was not in that batch —
it did not exist — and it inherits the batch's answers because it is a repair
to one of the five, found by the release pull request the batch's own
destination answer opened.

## Why this way

The survivor check #180 shipped runs in `hygiene.yml` on every pull request,
and the release pull request into `main` carries a range no fix pass ever
writes: the union of five work items. It reported 72 places and failed the
release. The check is right and its wiring was not bounded to the range it was
calibrated over.

The session implements rather than `smith` because the change is one guard in
one step plus the case that pins it, and the whole of the finding is already
established — spawning a segment to transcribe it would buy the discovery a
second time.
