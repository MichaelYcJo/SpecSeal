# 1788826000-a-stamp-names-content-not-a-commit — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | none of its own — delivered inside `03594e0` (the widened roots) and `4bf8dcb` (the twentieth rider) |
| Ran by | `smith on unknown — the spawn prompt named the agent and not the model` |

## What this phase was asked

Bring the three riders nothing guarded under the check, and give the one with
a non-canonical staleness line a canonical stamp.

## What this phase found

**It could not be a phase of its own, and the reason is worth recording.** The
widening is one constant — `RIDER_ROOTS` gaining `.github` and `tests` — and
it is only safe because of the comment-head requirement phase 2 built. Landing
the constant without that requirement turns every file that *describes* the
convention into a corpus member, so the two cannot be separated into
independently runnable slices. The constant therefore shipped with the
machinery, and the twentieth rider's stamp shipped with the rest of the
corpus.

`plan.md` numbered this as a slice because the ticket lists it as a separate
obligation. That was a planning error rather than a discovery: the obligation
is real and was met, but it is not a vertical slice, because there is no point
at which it runs on its own.

**What the widening actually cost was nothing, which is the finding.** The
scan over six roots reports exactly 20 riders and no prose mention, so the
line the roots draw — what this repository executes or ships, versus what
describes the convention — held on the first attempt. The previous version of
this list drew it as *code*, which is why `agents/smith.md` and
`skills/implement/SKILL.md` were inside it while `.github` and `tests` were
not; the two markdown files carry real riders and the omission had no
principle behind it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `RIDER_ROOTS` as a list the test file owns | `.github/scripts/rider_check.py#RIDER_ROOTS`; the test imports it, so the checker and the case cannot disagree about what the corpus is |
