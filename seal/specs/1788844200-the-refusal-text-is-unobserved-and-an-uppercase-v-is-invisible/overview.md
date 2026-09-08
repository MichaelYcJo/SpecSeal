# 1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible — overview

📋 implement applied
· spec:     `seal/specs/<this work item>/routing.md` · `spec.md` · `plan.md`; `CONTRIBUTING.md` §"Running the checks" and §"What a change to a gate must carry"; `docs/issues-and-milestones.md` §"A label answers *what it is about*"; `docs/release-checklist.md`'s check table; `docs/flow.md`'s 0.9.x section; `seal/ledger.md` rows G5, R1, R3; `seal/follow-up.md`; `seal/config.md` (Record language absent → English); issues #203, #204, #205, #206 in full
· evidence: `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md` S1–S4 added; `seal/ledger.md` R1, R3 and G5 corrected and re-verified
· verified: executed — the module (32 passed), the seven mutations of `refusal`, and in review round 1's fix pass the `ast.parse` re-derivation (six leaves) with thirteen mutations over it leaving two survivors, the survivor mutation, the `[vV]?` mutation, the loaded-set enumeration under both patterns, the four arrangements through both implementations, `evidence-check --strict` over the fragment and over `seal/ledger.md`, `ruff check`/`format` on the one module. Read — the three documents naming the check. Unverified — the full suite, the repository-wide lint and the typecheck, which are the orchestrator's

## Why this work exists

Three of the four tickets are the same failure: a record that states, as a
measured fact, a limit nobody measured — and each one had already stood as the
grounds for looking no further. The fourth is this plugin's own version in an
uppercase spelling passing the check that exists to refuse it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| whether an uppercase instance exists in the tree | #204 says, executed at `7349afc`, that `git grep -E 'V[0-9]+\.[0-9]+\.[0-9]+'` over the loaded set returns nothing | recorded that one exists now | `docs/flow.md` writes `an uppercase V0.9.0 is invisible` in the row describing this work item. Enumerated over all 64 loaded files: the widening admits exactly that token. It is still not an offender, for two reasons rather than the ticket's one — that file is a record of a moment, and the version is below the running one |
| where `docs/flow.md` states the rule correctly | the handoff names `docs/flow.md:51` | read it at `docs/flow.md:30` | line 51 in this tree is about how a release is sized. The sentence stating the rule — #179 *"goes red on the commit that raises the version"* — is at line 30, and it is correct there, so it was left alone as the handoff intended |
| how much of the element case is new | the ticket asks for one case asserting the offender lines, the running version and the paragraph | five elements in the new case, the sixth in the case above it | the routes piece is read by both cases, and deliberately: the case above reads it as the routes, this one reads it attached to the block that precedes it. The five counted as new are the five nothing read before (round 2 ⬜ 9). `test_the_message_has_a_route_for_every_token_the_check_refuses` is the case above; the new case's docstring names where the sixth is pinned. **Corrected in review round 1's fix pass — the count was seven and six by a reading of the source; `ast.parse` gives six leaves, of which the routes are one** |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the review orchestrator, once after the rounds settle — `skills/agent-contract/SKILL.md` §2 forbids them here |
| the early-return implementation the four arrangements were run through is reconstructed from the docstring that describes it, not the historical bytes | the review orchestrator, if the reverted branch's intermediate commits can be fetched; `git log -S` over this clone finds only the pre-round-1 shape |

## Not done

**`as_release` was left alone.** Its `lstrip("v")` does not strip an uppercase
`V`, so a future call handing it `match.group(0)` would raise. Nothing does:
`timers_in` passes the bare `match.group(1)`, and the other-product lookup is
string equality. Widening it would be a speculative change that drifts a
`seal/ledger.md` anchor for a claim nobody is making, and the phase-1 record
says so where a reader hunting the uppercase class will land.

**No case pins the two documents agreeing**, which is #206's underlying class.
Building one is new mechanism in a fix the four tickets scope to prose, so it
is `questions.md` Q1 with the orchestrator as answerer, and ledger row S4
states the gap rather than leaving it to be noticed. Review round 1 found the
row citing a third document as already agreeing when that document describes
the check this one replaced; the row now says two.

**The check's own `assert not offenders, refusal(running, offenders)` is still
unpinned, and it is pinnable.** Review round 1 wrote and ran the pin — swap the
module globals `tracked` and `timers_in`, call the check, compare the raised
`AssertionError` to `refusal(running, offenders)` — and it reads no source, so
the sentence saying it could not be pinned is gone from the docstring. Planting
the case is the review orchestrator's call: it is a unit this fix pass would
add for a finding located in prose, and the pass is scoped to correcting what
was claimed rather than to closing the survivor.

**No assertion was added for #205's arrangement**, which the ticket forbids and
which is the failure it is about.

## Fed back into the spec

None. The four tickets each carried their own *What would close it*, and
nothing here added a rule the documents did not already have.
