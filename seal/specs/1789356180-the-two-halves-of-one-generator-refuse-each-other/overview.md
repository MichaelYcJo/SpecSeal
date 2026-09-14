# the two halves of one generator refuse each other — overview

<!-- seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/overview.md
— the closing memo. Only what the diff cannot show. -->

Six tickets, every one a place where `round_record.py new` writes a round
record that `round_record.py close` then refuses, with a person hand-editing a
generated file in between. Four phases, cut by the column of `rounds/round-N.md`
each disagreement is about; the record now says what the reviewer wrote, the
fix pass keeps what the reviewer said, and the two subcommands agree.

## Where spec and implementation diverged

| The spec said | What was built | Which won, and why |
|---|---|---|
| `spec.md` §6: **1,992** verdict rows, **54** with no digit, **103** carrying an empty code span; the frame labelled these `read` and told this build to re-derive anything it relied on | Executed over the 207 committed records that parse: **1,989**, **51**, and **210** | The measurement. The counts are right and **round 1's 🟡 2 found the READING of the 51 wrong**: 44 of them are a severity marker and a single letter, a finding id in the wrong alphabet, and only 7 are the shape the rule admits. The corrected grounds are in `docs/review-chain-spec.md`, `skills/code-review/SKILL.md`, `templates/sdd-round.md`, `agents/warden.md`, `round_record.py` and the ledger fragment. Every number in the fragment and the changelog is the executed one |
| `spec.md`'s table puts `❓ out of verified scope` in the **Verdict** column's change and the id-less row in the **`#`** column's, which reads as two phases | Both shipped in phase 1 | The spec's own split, arriving one phase earlier. #84's finding 15 carries the id `15`, so the `#`-cell mechanism never reaches it — the scope marker had to be closed from the Verdict column, and phase 1 is where it was met |
| `plan.md` leaves open "whether a row with no id needs a spelling of its own in the `#` cell or whether an empty cell is enough" | A cell with no digit **and** no severity that owes an answer, and never an empty one | The corpus, twice. No sentinel of its own, because a reviewer who forgets an id writes an empty cell as readily as a word — but the `#` cell alone cannot say whether anything is owed, which round 1's 🔴 1 measured as a record written with `Pass` ticked beside an open finding. The severity marker already carries that meaning and is read alongside |
| Q2 reads as a document correction: `docs/review-chain-spec.md` is corrected and one case rewritten | One code change beside it — `fix_table` now refuses a suffixed verdict cell by naming the two-cell shape | Four of phase 2's five cases were green before any edit. The live defect was not the accepted spelling, it was the message a reader met when they followed the owner instead: three words listed, one of which their cell had begun with, and nothing saying so |
| The standing `# RIDER:` at `fix_table`: widening `chain.SEPARATORS` would strip the backticks off a home deliberately written as a code span | Measured false at that site. `chain.EMPHASIS` is ``[*_`]+`` and runs over the verdict cell one line earlier, so such a home already arrives stripped | The measurement, for the fact; the rider, for the conclusion. Its other two callers are a real cost and nothing here measured them, so the constant is still left alone — and the case pins the constant and the cut site rather than the consequence that turned out not to exist |
| `plan.md` §Alternatives rejects one commit carrying two rules | Phases 3 and 4 were committed together by mistake | The plan. The commit was reset, phase 4 reverted, phase 3 verified standing alone and committed, and phase 4's case seen red **again** on that tree before being re-applied |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Contract §2 makes this one act with one owner and `agents/sealer.md` is that owner; narrow runs covered every module this branch touches and the ones that read them | the orchestrator, through the sealer spawn |
| Whether the two other callers of `chain.SEPARATORS` — `chain_check`'s own readers — would lose anything if a backtick were added to it. Not needed for this work, which leaves the constant alone, and it is what the replaced rider's conclusion rests on | whoever next proposes widening `chain.SEPARATORS` |
| Whether any of the 11 recoverable rows whose grounds were reduced to a home lost prose a reader still needs badly enough to justify rewriting a past record. Q6 answers the migration question `no` on the grounds that a round record asserts a past state; this is the narrower judgment left standing | the repository owner, if #344 is ever built |

## Fed back into the spec

| Clause | Where |
|---|---|
| A verdict row that commissions nothing — what it is, which three kinds of row are that shape, that a 🔴 or 🟡 with no number is refused, and which way the rule still fails | `docs/review-chain-spec.md` §*A verdict row that commissions nothing*, new. *Inferred during implementation*: the discriminator is this build's, and its second half — the severity — is round 1's |
| `❓ out of verified scope` is a closing verdict in neither `FIX_WORDS` nor `HOME_WORDS`, and a severity marker leads a verdict cell without being part of it | the same section. *Inferred during implementation*: the marker rule was measured over the whole corpus before it was taken |
| The correcting SHA is two cells, a repair made outside the tree takes the same shape, and `already deferred` is grounds | `docs/review-chain-spec.md` §*The last round verifies*, corrected |
| `close` writes both of `landing_values`' answers, and nothing reads the reason | `docs/review-chain-spec.md` §*`Fixes checked by` has to name a checker the repository can confirm* |
