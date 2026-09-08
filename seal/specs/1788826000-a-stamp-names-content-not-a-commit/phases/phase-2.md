# 1788826000-a-stamp-names-content-not-a-commit — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `03594e0` |
| Ran by | `smith on unknown — the spawn prompt named the agent and not the model` |

## What this phase was asked

Build the machinery: rider block detection, the region hash, anchor
resolution, and the commands that check and re-stamp. Move no stamp yet.

## What this phase found

**The comment-head requirement is what makes the corpus definable at all.** A
rider block opens only at a line that both carries the marker *and is a
comment* — `#` at the head after stripping, or an HTML comment. Without it the
marker's own name pulls in every file that describes the convention: this
repository has the string in `seal/follow-up.md` prose, in `CLAUDE.md`, in
`docs/`, inside string literals in three test files, and in the checker's own
docstring. With it, the scan can be widened to `.github` and `tests` — which
is what closes the second instance phase 1 found — without a blocklist that
grows. Executed: the widened scan finds exactly 20 riders and no prose mention.

**`--migrate` had to consult git, and the check had to not.** The date and the
hash are true together or not at all: a date says when a person read the claim
and a hash says what they read, so re-anchoring today's content under a date
earned months ago would assert a reading nobody did. `evidence_check.py` had
already met this and answered it — its `--migrate` is the one place in that
file that calls git, on the grounds that a one-shot writer may consult the old
stamp's commit before trusting what it recorded. The same split is taken here:
`content_at` exists on the migration path alone, and the CHECK makes no git
call, which is what actually removes the class rather than repairing the
instance.

**Refusing resurrection is a departure from the ledger, and it is deliberate.**
`resolve_unit` carries out an uncertainty flag for a place that survived only
because the declaration rule put a keyword-blocked candidate back. The ledger
tolerates it because its rows were bulk-migrated off line numbers; a rider is
hand-written by somebody standing at the coordinate, who can pick a better
anchor. Refused here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
