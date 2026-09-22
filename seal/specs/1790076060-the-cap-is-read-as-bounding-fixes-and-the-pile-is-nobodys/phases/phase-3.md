# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 00b7b306 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

#493's rule. `docs/review-chain-spec.md`'s leftovers table becomes an ordered
ladder, with the test read off the `Who answers it` column the reviewer's
`## Deferred` table already carries. Links in
`skills/code-review/orchestration.md`, `agents/warden.md`,
`templates/sdd-round.md` and `docs/issues-and-milestones.md`, and that last
document gains the `from-review` paragraph — what the label marks and what it
is counted for. A second `RULES` row pins it, seen red first.

## What this phase found

**The ladder needed a heading, and giving it one moved a boundary.** The
homes table had no heading of its own and sat inside §*The last round
verifies, and what it verifies is a diff*, which is a subsection about the
verifying round rather than about how a run ends. The repository's link shape
names the owner's **subsection**, so a rule with no heading cannot be linked
at all. The table, the sealer's paragraph and *The chain ends at a PR* now sit
under §*Where a leftover goes — the ladder, and why a new issue is not the
default*, and the `###` that opens it ends the verifying round's subsection
where its subject ends.

**A fifth carrier was found by reading and is not in `plan.md`'s list.**
`agents/smith.md` said a finding neither fixed nor answered *goes to*
`seal/follow-up.md`, flatly. The ladder makes that a rung with a test, so the
flat sentence became false the moment the ladder landed — the same class the
four named carriers are in, found the way §12 says to find it rather than by
waiting for the sweep. It gets the link and a sentence saying the first home
is a rung.

**`seal/follow-up.md` is the same rung as a new issue, not a cheaper one.**
`spec.md` scopes it out as a home for a finding that names nobody, and the
ladder says so by putting it on rung 3 with the same test — which is what
keeps every sentence in `agents/smith.md` and `skills/implement/SKILL.md`
about that file true rather than needing a second correction.

**One sentence in `docs/issues-and-milestones.md` was falsified and
corrected.** §*A milestone answers when* said the count is in work items
because *a run that reaches the reopening bound turns every finding still open
into an issue*. Under the ladder that is no longer what happens, and the
sizing argument does not depend on it — it depends on leftovers arriving as
several ticket numbers, which is what the sentence now says. The rewrite also
dropped a line 105 columns wide that `tests/test_docs_line_wrap.py` caught
immediately; that file is covered at 88 and the two documents the ladder's
prose reaches are too.

**The six mutations were killed one at a time**, by a probe in the shape phase
2's took: bytes kept, one needle removed whitespace-flexibly, the module run,
the file restored from the probe's own copy. Every run exited 1 and named the
case it was meant to redden — `test_the_owner_states_the_rule[14 …]` for the
owner's sentence and `test_every_link_names_the_owner[14 …]` for each of the
five links — with the module 60 green before the first mutation and 60 green
after the last restore. The probe was deleted and the tree is byte-identical
to the commit.

**What was run.** Twenty modules at the phase boundary: 1090 passed, 8
skipped, exit 0. `grep -c "from-review" docs/issues-and-milestones.md` returns
2 where it returned 0, which is scenario A8. The full suite is the sealer's
and was not run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The row *A finding neither fixed nor answered → `seal/follow-up.md`, and named in the PR body* | rung 3 of the ladder, which keeps the file as a home and adds the test it always applied to its own rows |
| The clause *a run that reaches the reopening bound turns every finding still open into an issue*, in `docs/issues-and-milestones.md` | nowhere — it was the old filing rule quoted as an aside, and the sizing argument it supported now rests on the leftovers arriving as several ticket numbers |
| The sentence's *four ticket numbers* and *four releases' worth of work* | nowhere; *several* replaces both, because the count was an illustration of the old rule's arithmetic |
