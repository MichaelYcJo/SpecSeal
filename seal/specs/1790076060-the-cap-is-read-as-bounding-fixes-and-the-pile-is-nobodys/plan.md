# Implementation Plan: the cap bounds rounds, and a filed finding names who acts

Approved 2026-09-22 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

Two sentences are repaired and pinned, and nothing mechanical moves.

The first says that the cap bounds ROUNDS: a run the cap stopped may still
write a fix, and what decides between a fix and a home is **who owns the unit
now**. The second says a finding is filed only where somebody will act on it,
and gives the homes in order so that opening a new issue stops being the
default.

Both are written where the rule is already owned, every other carrier becomes
a link naming that owner, and `tests/test_the_rules_have_one_owner.py` holds
the arrangement — the shape the repository already uses for twelve rules.

**No gate changes.** No arm of `chain_check.py`, no subcommand of
`round_record.py`, no hook, no workflow. The states the repaired sentences
describe are states those checkers already accept, and the measured instance
is the proof: `seal/specs/1790039346-…/rounds/round-6.md` is a capped record
that closed five findings `fixed` and reads `Fixes checked by: round-7`, and
`round-7.md` is the reader that commissioned nothing. That branch shipped
green.

**Prompt budget: zero.** The work adds no question anywhere. The ownership
evidence is a row the record already carries, and the filing test is a column
the reviewer already writes.

## Technical context

| Coordinate | What is there now |
|---|---|
| `docs/review-chain-spec.md` §*The review run has a bound, and an end* (from line 32) | The cap's numbers, the floor, the verifying round, and the leftovers table that lists the homes. This section owns the cap and says nothing about whether a stopped run may write a fix |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* (from line 1230) | The second exit. Its paragraph is the sentence #492 quotes, and three of its four clauses are true only of a record that wrote no fixes |
| `docs/review-chain-spec.md` §*What the record carries* (line 1649) | The moratorium on new parsed fields |
| `skills/code-review/orchestration.md` lines 114–260 | The verifying round, the floor, and the no-mechanism rule. Carries the capped-exit sentence in full at lines 168–180 |
| `agents/warden.md` lines 125–133 | Already a link for the reopening rule, and already says a verifying round after a reopening reports `deferred #N` candidates |
| `agents/warden.md` lines 254–266, 396–400 | The `## Deferred` table the reviewer writes, with its `Who answers it` column — the filing test's evidence, already on the page |
| `agents/smith.md` lines 271, 280, 297 · `agents/sealer.md` lines 88–100, 106, 142 | The `Fixes checked by` vocabulary and the sealer's refusal. `round_record.py seal` refuses `Broad gate` on a last record whose cell reads anything but `no fixes to check` |
| `templates/sdd-round.md` lines 40, 92, 153, 164, 218–226, 340–348, 419–425 | The record's own prose for all of the above, and the `## Deferred` table |
| `docs/review-handoff-protocol.md` lines 160, 245, 253, 400–430 | The protocol's copy of the floor and the reopening |
| `skills/code-review/scripts/chain_check.py` lines 227–232, 365–372, 3360–3390 | The exit sentence in a docstring and a comment, `CLOSED_WORDS`, `HOME_WORDS`, and the reopening walk's refusal of a second fix-closing record |
| `tests/test_the_rules_have_one_owner.py` lines 106–200, 538–560 | The `RULES` table and the phrase sweep over `docs/`, `skills/`, `agents/`, `templates/` |
| `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-6.md` and `round-7.md` | The measured instance, both ends of it |

**Two traps in that last test module, and they are constraints on the prose
rather than things to change.** The phrase *at most one more round record* is
asserted at exactly one occurrence in `docs/review-chain-spec.md` and one in
each of `skills/code-review/orchestration.md` and `templates/sdd-round.md`,
with a ceiling of four across the whole tree — a new paragraph that repeats it
fails the sweep. And the four swept files may not state the exception as
*Unless th…*; the assertion is a bare substring match, so an ordinary sentence
beginning *Unless the* trips it.

**What breaks in six months.** Two things, and #492 names the first itself:
fixing a sentence does not stop the next orchestrator from misreading a
sentence, which is why #330 exists. The second is the filing ladder's second
rung — *an open issue already owns the ground* is a judgment nothing checks,
so it can decay into opening a new issue anyway and no check will notice. What
makes that visible is the count #493 took: 89 `from-review` issues, 47%
closed. Re-taking it is one query while the label is documented, which is why
documenting the label is in scope.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Owner of both rules is `skills/code-review/orchestration.md`, because filing and capping are the orchestrator's acts | The leftovers table — the list of homes a finding can take — is already in `docs/review-chain-spec.md`, and the cap is too. Moving the rule to the skill leaves the spec's table restating it, which is the eight-carrier failure `test_the_rules_have_one_owner.py` exists to prevent | **Rejected.** `docs/review-chain-spec.md` owns both; the orchestration file, the template, the two agents and the handoff protocol carry links |
| Owner of the filing rule is `docs/issues-and-milestones.md`, because it owns the tracker | It owns what a milestone and a label mean, not what a review run does with a finding. The rule would sit one document away from the cap it is triggered by, and the leftovers table would still have to restate it | **Rejected**, and it gets the link plus the `from-review` paragraph instead |
| Leave the reopening bound's terminal record free to write fixes too, so one sentence covers both exits | `chain_check.py`'s reopening walk refuses a second fix-closing record after a floor `no`. The document would name a spelling its own checker refuses, which is #341 exactly — the failure this repository has already paid for once | **Rejected.** The two exits are named apart, and the permission is the round cap's alone |
| Let a capped run's fixes go unread — `Fixes checked by: nobody — the run is capped` | `round_record.py seal` refuses to write `Broad gate` on a last record whose cell reads anything but `no fixes to check`, and `chain_check` fails a ready pull request on `nobody`. The measured instance hit this twice and answered it with a round both times | **Rejected.** Capped fixes owe one verifying round at their diff, and it commissions nothing |
| A finding nobody will act on goes to `seal/follow-up.md` | That file's own rule is *every row names a person, with no condition attached*, which is the same test the ladder applies before an issue is opened. A finding that fails the test fails it there too | **Rejected.** It is not a cheaper home and this work does not make it one |
| A finding nobody will act on becomes a `# RIDER:` at its coordinate | Genuinely attractive: `seal/follow-up.md` sends anything tied to a coordinate there, every review finding has a `Location`, and a rider arrives at whoever opens the file rather than at whoever browses the tracker. What it costs is a write into a file the branch may not own, a stamp `rider_check.py` then holds, and a second thing to keep true | **Not chosen, and not closed.** The ladder's fourth rung is the round record; a rider stays available to whoever fixes the file, and the grounds are here rather than lost |
| A finding nobody will act on is dropped | A real defect leaves no trace at all, and the round record is free — it is durable, the next round on the work item reads it, and the finding's coordinates are already in it | **Rejected** |
| Keep opening a new issue per finding, and fix the pile by triage instead | That is today, measured: filing at 100%, action at 47%, 47 open, 23 of them from a three-day window. Triage is a person's act and the first goal says a design that needs one is the more expensive | **Rejected** |
| Make the ownership test a lookup over `New units` now | It is mechanism on the chain gate and carries `CONTRIBUTING.md` §*What a change to a gate must carry*. #492 scopes it out by name and leaves it against #330 | **Rejected here**, kept there |
| Add a parsed field or a checker arm for *who answers it* | The moratorium refuses a new parsed field, and every field that ever arrived cost a checker arm, a template row, a protocol row and a cutoff. The column already exists in the reviewer's report and in the record | **Rejected.** The rule reads the column that is there |

## Phases

Vertical slices. Each ends with the pin test green and, where it added a pin,
with that pin seen red first.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #492's rule, in its owner. `docs/review-chain-spec.md`: the cap bounds rounds, a run the round cap stopped may write a fix, the ownership test in the words *who owns the unit now* with `New units` named, and *when did the defect start* named as the substitution. The reopening section's exit sentence corrected so that `no fixes to check` is stated of the record that wrote no fixes rather than of every capped record, and the two exits named apart | `bin/test -q tests/test_the_rules_have_one_owner.py tests/test_release_hygiene.py`, read of the section, and a `grep` showing *at most one more round record* still at one occurrence in this file | `4b34b1b7` |
| 2 | #492's carriers become links naming the owner: `skills/code-review/orchestration.md`, `templates/sdd-round.md`, `docs/review-handoff-protocol.md`, `agents/warden.md`, `agents/smith.md`, `agents/sealer.md`, and the restating comment in `skills/code-review/scripts/chain_check.py`. A new `RULES` row pins the rule and its links | The new row's two assertions seen red with the owner's sentence stashed, then `bin/test -q tests/test_the_rules_have_one_owner.py` | `c2527d96` |
| 3 | #493's rule. `docs/review-chain-spec.md`'s leftovers table becomes the ordered ladder, with the test read off the `Who answers it` column. Links in `skills/code-review/orchestration.md`, `agents/warden.md`, `templates/sdd-round.md` and `docs/issues-and-milestones.md`, and that document gains the `from-review` paragraph — what the label marks and what it is counted for. A second `RULES` row pins it | The new row seen red, then `bin/test -q tests/test_the_rules_have_one_owner.py`; `grep -n "from-review" docs/issues-and-milestones.md` returns a hit | `00b7b306` |
| 4 | The sweep and the fragments. `survivor-check` against the base, answered line by line — corrected where the wording should have moved, recorded in `seal/specs/<work-item-id>/survivors.md` with grounds where it stands by design (`CHANGELOG.md` and earlier work items' records are durable copies). `changelog.md` and, for any claim verified against a coordinate, `seal/ledger/<work-item-id>.md`. `evidence-check --reverify` for any row whose anchor this branch drifted | `survivor-check`, `evidence-check`, and the fragment paths present | `ccf3d921` |

Each phase closes with `seal/specs/<work-item-id>/phases/phase-N.md` from
`templates/sdd-phase.md`, and the Status cell takes the commit that closed it.

## Operational impact

No migration, no environment variable, no dependency, no compatibility break.
Nothing a deployer touches.

What changes for whoever runs a review chain: at a round-cap exit the
orchestrator has a decision where it used to have a default, and the decision
costs no question — the evidence is the `New units` rows of the run's own
records. At the reopening bound nothing changes at all.

Two conventions this repository imposes on the work, both stated in
`CLAUDE.md` and neither optional: the changelog entry is a fragment under
`seal/specs/<work-item-id>/changelog.md` and any ledger row a fragment under
`seal/ledger/<work-item-id>.md`, never the shared files; and no file loaded at
runtime may name the running version or anything above it.
