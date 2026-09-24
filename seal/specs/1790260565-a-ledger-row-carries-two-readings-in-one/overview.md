# 1790260565-a-ledger-row-carries-two-readings-in-one — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show goes here, and each part is written when it happens. -->

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this work item; `docs/the-evidence-ledger.md` §*A row is a content anchor* (edit-arm and escaped-pipe paragraphs) and §*A correction a merge dropped* (halves paragraph)
· evidence: in place — S4 (`seal/releases/0.9.2.md`), G5 (`seal/releases/0.8.2.md`), the eleven-modules row (`seal/releases/0.9.3.md`)
· verified: see each phase's record under `phases/`

## Why this work exists

Three ledger rows stated two readings where the table has room for one, the
width case counted no row that sits under no header, and two clauses of the
ledger's rules had no case holding them (#568, #501, #569).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S4's claim cell | Spec: "Re-read note, or `Corrected <date>` where the re-read found the claim false" (Q3). The re-read found the claim's paraphrase of the rule false: it said *at or above the running one* is refused, while the check and the document both keep a tagged version as history since #363 | corrected in place, `Corrected 2026-09-24` note | `docs/the-evidence-ledger.md`: "one the edit made false is corrected there first, with a `Corrected <date>` note" |
| The phase-1 instrument's answer | Spec: the instrument returns "the issue's three rows exactly" | four rows before the edit, one after: `seal/releases/0.11.5.md`'s `seal` last-record row also carries a `\|` outside a code span by CommonMark's pairing | That row quotes an assertion whose text holds backticks inside a single-backtick span, so the span closes early. It carries one reading, not two, so it is not #568's class and was left alone |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and format over the finished branch | the sealer, after the review rounds settle |

## Not done

nothing

## Fed back into the spec

none
