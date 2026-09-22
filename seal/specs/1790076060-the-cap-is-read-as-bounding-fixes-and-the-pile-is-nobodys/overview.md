# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — overview

📋 implement applied
· spec:     `seal/specs/1790076060-…/{routing,spec,plan,questions}.md`; `docs/review-chain-spec.md` §*The review run has a bound, and an end*, §*The last round verifies*, §*The reopening — one, and then the run is capped*, §*What the record carries*; `docs/issues-and-milestones.md` §*A label answers what it is about*, §*An issue is its body and its comments together*; `skills/code-review/orchestration.md`; `CLAUDE.md` fragment and coordinate rules; `skills/agent-contract/SKILL.md` §§2, 5, 9, 12, 15
· evidence: `seal/ledger/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys.md`
· verified: see `## Not verified` and each `phases/phase-N.md`

## Why this work exists

The review chain's cap was read as bounding fixes rather than rounds, so a
one-line verified repair was filed instead of made; and filing a finding ran at
100% while acting on one ran at 48% — 89 issues carried `from-review` on
2026-09-22 and 43 of them were closed. This work repairs both sentences where
each rule is owned, makes every other carrier a link, and pins the arrangement.

## The cost this work ships, stated rather than discovered

The filing ladder (#493, `questions.md` Q1) makes a new issue the third rung
rather than the default. **What it costs: a real defect that can name nobody
who will act on it stops being visible in the tracker.** It lives in the
round record and in the pull request body, which is durable until `settle`
retires the work item's directory at a later release — after which the pull
request body is what carries it.

That is the same trade `seal/follow-up.md` already made for its own file, on
the grounds that an unowned row is not a plan. It ships on Q1's default
because the run is `automation`, the ticket was raised by the repository
owner, and its body argues for it. **The repository owner is who may overturn
it**, and `questions.md` Q1 is the row where that is done.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The no-mechanism rule was declared untouched, and the fix pass touched it | `spec.md` §Grounding lists `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed* as **Unchanged**, and §Out says *Rule 1 of #493's two — a fix pass may not add mechanism* is not touched | The fix pass changed that section's **destination sentence**, and the same sentence in `agents/smith.md` and `skills/implement/SKILL.md` | The rule itself is untouched: *A fix pass may not add mechanism* still stands and still owns its own section, and `tests/test_the_rules_have_one_owner.py` rule 2 pins it with both links. What changed is where a finding it refuses GOES — *is an issue* became *takes the filing ladder* — which is the filing rule, not the no-mechanism rule. Round 1's enumeration found those three sites in the same class as the capped exit, and leaving them would have shipped the contradiction the 🔴 was about, one rule over. Executed: `git diff 6d410023..4ddfde2e` over that file touches none of the section, so the build honoured the declaration and the fix pass is what crossed it |
| Where the homes table lives | `plan.md`'s Technical context puts the leftovers table under §*The review run has a bound, and an end* | Treated as inside the `###` subsection *The last round verifies, and what it verifies is a diff* | True of the `##` section and imprecise about the `###` one. Two ledger rows are anchored on that subsection (`seal/ledger.md` R-rows at lines 2171 and 2196), so the rewrite drifts them; phase 3 read that before editing rather than after |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the `sealer`, spawned by the orchestrator after the review rounds settle. `agent-contract` §2 keeps the broad gate off this segment; what ran here is each phase's own modules |
| Whether `chain_check.py`'s `CAPPED_EXIT` constant — the refusal message that says *every finding still open becomes an issue* — should be reworded to the ladder. Under the ladder a finding at that exit may take rung 2 or rung 4 instead, so the message is now imprecise where it was exact. **One of a pair — the row below is the same question for the depth exit**, and this branch owes both the same act | the repository owner, through the review chain. The message is a line a person reads and acts on, so rewording it is a gate change this work item is scoped out of; `survivor-check` cannot report it, because the range removes that wording nowhere |
| Whether the depth exit's runtime message — `DEPTH_EXIT` in `round_record.py`, printed when `close` refuses a depth-2 unit, and the same sentence at `chain_check.py:2648` and `:3355` — should be reworded to the ladder. It says a unit a fix pass may not add *is deferred with a named answerer, or becomes an issue*; under the ladder such a unit may take rung 4 instead, so the message is imprecise in exactly the way `CAPPED_EXIT` is. The prose carriers of the same rule were rewritten in this run's fix pass; the message was not, because rewording one is a gate change `spec.md` §Out refuses | the repository owner, through the review chain |

## Not done

**No checker arm, no parsed field, no verdict word, no template column.** The
moratorium in §*What the record carries* and `spec.md`'s Out list both refuse
them, and the filing test reads the `Who answers it` column the reviewer's
`## Deferred` table already carries.

**The lookup — deriving *does this branch own the unit* from `New units`
automatically — is not built.** It is mechanism on the chain gate, it carries
`CONTRIBUTING.md` §*What a change to a gate must carry*, and #492 scopes it
out by name. It stays against #330.

**A `# RIDER:` at the coordinate was not made a rung of the ladder.** The
grounds are in `plan.md`'s Alternatives table and they are *not chosen, not
closed*: a rider stays available to whoever fixes the file.

## Fed back into the spec

**The filing rule reaches the no-mechanism rule's destination sentence, and
`spec.md` did not say so.** Marked *inferred during implementation*, so a
planner may overturn it. §Grounding calls
`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it,
and that unit ships unreviewed* **Unchanged** and §Out scopes out *rule 1 of
#493's two*; both are true of the rule and neither is true of the sentence
that says where a finding the rule refuses goes. Round 1's enumeration put
that sentence in the capped exit's class — it told a reader an open finding
becomes an issue, with no condition — so the fix pass rewrote it in the owner
and in its two carriers, `agents/smith.md` and `skills/implement/SKILL.md`.

What the next frame should take from it: **a rule's own statement and its
destination sentence are separate surfaces**, and a scope line naming a rule
does not settle what happens to its refused work. `spec.md` Scope In 5 asked
for every carrier of the filing sentence and §Out asked for the no-mechanism
rule to be left alone; the destination sentence is in both, and nothing in the
frame said which line won. It was settled the way judgment precedence settles
it — the contradiction the 🔴 reported was the thing being fixed, and shipping
it one rule over would have been the same defect with a different coordinate.

**Nothing else was fed back.** The `New units` paragraph, the rung-3 test and
the dated measurement all answer findings against sentences this work item
wrote, not against clauses `spec.md` got wrong.
