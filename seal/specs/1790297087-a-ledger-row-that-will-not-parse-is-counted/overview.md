# 1790297087-a-ledger-row-that-will-not-parse-is-counted — overview

📋 implement applied
· spec:     this work item's `spec.md`, `plan.md`, `questions.md`; `docs/the-evidence-ledger.md` as `spec.md` §*Grounding* cites it; `skills/evidence-check/SKILL.md` §*A coordinate names content, never a position*, §*Verdicts and what to do*, §*Re-verifying is recomputing the hash*, §*Known limits*; `templates/ledger.md` §*Coordinates*; `CLAUDE.md` §*a change writes fragments, never the shared file*; `seal/follow-up.md`'s #299 row; #299, #322
· evidence: filled in as each phase closes
· verified: filled in as each phase closes

## Why this work exists

A ledger row whose coordinate the checker could not parse was counted nowhere, so a typo in a hash or an unescaped quote took a claim out of the ledger while the build read clean; five such rows were standing in this repository.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The rider-stamp row in `seal/ledger.md` | `spec.md` §*In* item 6: *A claim that still holds gets its coordinate corrected … A claim that no longer holds is corrected or taken out* | Taken out, and the current claim written as a new row in this work item's fragment | The quoted line `STAMP = re.compile(…)` is no longer in `tests/test_a_rider_reaches_its_file.py` (it is `OLD_STAMP`, kept only to name the pre-#239 form), and the claim *the SHA is an ancestor of HEAD* has been false since #239. `CLAUDE.md`: *A row whose anchor a change removes is REMOVED, not re-pointed … Write the new claim as a new row in the work item's own fragment* |
| Two more coordinates that never parsed | `spec.md` §*The live instances* lists five, all in a `Code grounds` cell | Two more repaired in the same phase: the `test_what_the_reader_understands.py` fixture coordinate in `seal/ledger.md`'s eval row and the `CLOSED_WORDS` coordinate in its separator row, both in a Notes cell | Both are quoted locators with bare `"` inside, and `check_text` reads every anchor in a row, Notes included, so each was a claim meant to be checked and never was. The arm this work builds reads only the `Code grounds` cell, so it would not have named them; they were found by scanning every cell of every row (§12) |
| The `CLOSED_WORDS` coordinate | `plan.md` phase 1: *`\"` for the four quoted locators* | Cited by the constant's name, `chain_check.py#CLOSED_WORDS` | The one-line `CLOSED_WORDS = {…}` it quoted is no longer in the file: the set spans several lines and holds two more words. Escaping would have produced a coordinate that parses and resolves to nothing. It is a Notes coordinate and not one of the four `plan.md` counts |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite | the sealer, once, after the review rounds settle |

## Not done

Nothing yet.

## Fed back into the spec

None yet.
