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

<!-- CORRECTED in round 1's fix pass. Every word above is true of what
`--migrate` wrote and false of what this phase left in the tree. A later
`--reverify` in the same phase rewrote all twelve to 2026-09-08, because its
skip condition required the hash AND the date to match and only the hash had
not moved. The reviewer found twenty stamps reading 2026-09-08 against a
record claiming twelve preserved dates (round 1, findings 1 and 2).

The writer is fixed and the twelve are restored, each proved again the way
this phase describes: the region its current anchor names, hashed at the
commit the pre-migration stamp claimed and at HEAD, and only an identical
pair licenses the date. Proved in this repository rather than in a clone, so
`4581fe1` is present and the twelfth needs no separate argument.

The four riders whose anchors were written BY HAND keep 2026-09-08 and are
not among the twelve. Nobody could prove those dates, because the anchor did
not exist until somebody read the rider to choose one -- and reading the
claim to choose an anchor is a reading. `templates/evidence-check.yml` is
provable at 2026-08-31 now that it has an anchor, and is deliberately left
alone for that reason. -->

**Seven were refused, for three distinct reasons, and the refusals were
right.**

- **Four have no enclosing unit**, so what they are *about* is a judgment a
  tool must not make. `agents/smith.md` anchors `"## Phases"` and
  `skills/implement/SKILL.md` anchors `"### 1. Read the spec before the code"`
  — the heading each document owns. `hooks/root-migrate.py` anchors
  `PREFIXES`, which *is* its claim to be a reader of the old tree.
  `templates/evidence-check.yml` anchors the header line it quotes.

<!-- CORRECTED in round 1's fix pass (finding 5). The two markdown riders
anchored the PARAGRAPH above them, quoted as a sentence, and a sentence
anchor breaks on any rewording: one word changed in each gave BROKEN — *the
anchor resolves to nothing in this file* — at exit 2, where `CLAUDE.md`'s
rule is that an anchor degrades to DRIFTED and never to BROKEN.
`skills/implement/SKILL.md`'s rider asks a reader to reword the very sentence
it anchored, so doing what it says reported that its subject had vanished.
Both now name their heading, and rewording either sentence drifts —
executed, on a copy of each file.

`templates/evidence-check.yml` keeps its quoted line, argued rather than
fixed. A YAML file has no heading structure — `text_regions`'s heading rule
is markdown-only — and the alternative the round proposed, `"name:
evidence-check"`, resolves to that single line, which the rider makes no
claim about. Measured: the quoted line owns lines 1-18 and hashes the header
the rider IS about, while `name:` owns line 20 alone. Trading a loud wrong
verdict for a silent rider is the wrong direction for a design whose stated
losses are all losses of an alarm rather than inventions of one. -->
- **Two had moved since they were stamped** — `round_record.py`'s `load` and
  `swallowed` — so their dates could not be proved, and both were re-read and
  set to today. `load`'s docstring now states the same conclusion the rider
  does, which is what re-reading it established.
- **One names a commit that predates its own file.**
  `.github/scripts/fold_ledger.py` was stamped `881fb0f`, which git resolves
  and which is an ancestor of HEAD -- `fold_ledger.py` was simply not in that
  tree. Not the squash orphaning a stamp, which this migration never observed
  in the act; a stamp that was wrong when it was written.

<!-- CORRECTED in round 1's fix pass (finding 6). This bullet read *"One
names a commit git can no longer resolve at all ... the defect caught in the
act by the migration built to remove it"*, and it was the branch's only claim
to have observed the ticket's own failure happening. `git cat-file -t`
resolves the commit, `git merge-base --is-ancestor` says it is an ancestor,
and `git show <sha>:./.github/scripts/fold_ledger.py` says the path exists on
disk but not in that commit. `content_at` returned None for every non-zero
git exit, so one sentence was printed for three different causes; it now
names which one it hit. Re-enumerated: `hooks/root-migrate.py` at `4f78074`
is the same shape, and was refused one step earlier for having no enclosing
unit. -->

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
already drifted the row -- but only once `--reverify` stops rewriting a stamp
whose region hash has not moved. Until round 1's fix pass it did, so a
date-only re-stamp drifted the ledger row of a unit nobody had edited and the
two checkers disagreed in a standing way: measured, one changed date digit
gave `rider_check` `20 ok` exit 0 and `evidence_check`
`DRIFTED hooks/dispatch.py#run_gate` exit 1 (round 1, finding 3). The
sentence above is true of the tree as it now stands and was false when this
phase wrote it. All six were read before re-stamping, and the scoped
write form was used, per `seal/ledger.md`'s own discipline against a blanket
run re-stamping rows on behalf of a session that never opened them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| every `Verified <date> at <sha>` stamp in the tree | replaced in place by `Verified <date> against <anchor>@<hash>`; the old form is refused by `test_no_rider_stamp_names_a_commit` |
| the commit `881fb0f` as a referent | nowhere — it no longer resolves, which is the ticket. The claim it carried survives in `fold_ledger.py#demote`'s rider, re-verified against today's content |
