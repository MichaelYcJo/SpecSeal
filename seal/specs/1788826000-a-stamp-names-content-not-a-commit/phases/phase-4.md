# 1788826000-a-stamp-names-content-not-a-commit — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `4bf8dcb` |
| Ran by | `smith on unknown — the spawn prompt named the agent and not the model` |

## What this phase was asked

Move all twenty stamps. Not the shape — the corpus, all of it, because a
migration that leaves half the corpus on the old form is the state the ticket
is about.

## What this phase found

**Twelve migrated with their original dates intact, and that is the phase's
main result rather than a detail.** Each was proved rather than assumed: the
same anchored region was hashed at the commit the old stamp named and found
identical to today's, so the date really was earned against this content and
nothing was manufactured. A blanket rewrite to today's date would have been
one command and would have destroyed twelve true facts.

**Seven were refused, for three distinct reasons, and the refusals were
right.**

- **Four have no enclosing unit**, so what they are *about* is a judgment a
  tool must not make. `agents/smith.md` and `skills/implement/SKILL.md` anchor
  the paragraph above them — measured first: both are separated from that
  paragraph by a blank line, so the paragraph's contiguous-run region excludes
  the rider and the exclusion rule is not even needed there.
  `hooks/root-migrate.py` anchors `PREFIXES`, which *is* its claim to be a
  reader of the old tree. `templates/evidence-check.yml` anchors the header
  line it quotes.
- **Two had moved since they were stamped** — `round_record.py`'s `load` and
  `swallowed` — so their dates could not be proved, and both were re-read and
  set to today. `load`'s docstring now states the same conclusion the rider
  does, which is what re-reading it established.
- **One names a commit git can no longer resolve at all.**
  `.github/scripts/fold_ledger.py` was stamped `881fb0f`, and that is the
  defect caught in the act by the migration built to remove it.

**A wrapped locator does not parse, and the first attempt at three of them was
wrong.** The quoted-anchor pattern forbids a newline, so an anchor split
across two comment lines matches nothing. All three markdown and YAML stamps
now keep the whole `Verified … against …@…` on one line, which is why two of
them run past the usual wrap width; neither file is under
`tests/test_docs_line_wrap.py#COVERED`, checked before writing.

**The twentieth had never carried a stamp in any form.**
`tests/test_the_records_can_be_carried_out_and_in.py:1415` said *"green at
3f8f846, measured 2026-09-03"*, matched no pattern, and sat outside the roots
anything scanned. It anchors the parametrized case it asks a row to be added
to, so doing what it asks will drift it — which is the signal working.

**The rider edits drifted six ledger rows, and this is a one-time cost rather
than a standing one.** A ledger hash covers comments, so rewriting a stamp
inside a unit changes that unit's hash. In steady state it adds no new drift
event: a rider is re-stamped when its unit changes, and that same change has
already drifted the row. All six were read before re-stamping, and the scoped
write form was used, per `seal/ledger.md`'s own discipline against a blanket
run re-stamping rows on behalf of a session that never opened them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| every `Verified <date> at <sha>` stamp in the tree | replaced in place by `Verified <date> against <anchor>@<hash>`; the old form is refused by `test_no_rider_stamp_names_a_commit` |
| the commit `881fb0f` as a referent | nowhere — it no longer resolves, which is the ticket. The claim it carried survives in `fold_ledger.py#demote`'s rider, re-verified against today's content |
