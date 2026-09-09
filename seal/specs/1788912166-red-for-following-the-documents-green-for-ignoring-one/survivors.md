<!-- Judged survivors of round 1's fix range, one row each, per-survivor rather
than a whole-range declaration. This branch deleted no shipped section, so the
#297 escape is not what this is; every row below is a place a reviewer can open,
and every quote is the anchor, so the exemption stops holding as soon as that
text changes.

Seven of the eight are ONE class, and naming it once is cheaper than eight
grounds cells that repeat it. The fix pass reworded a changelog sentence that
carried BOTH of the exemption anchors at once — *"**The range is the anchor**,
exactly as the quote is for a per-survivor row, so the row stops holding the
moment the check runs over a different range"* — because the range half became
false (round 1's 🔴 1) and the quote half did not. So the phrases the range
scores against are `the quote is`, `is the anchor` and `stops holding the
moment`, all of which belong to the half that is still true and still stated
everywhere it was. The report is correct as a report and there is no defect
under it.

The last three are the same shape one layer over. Four places say
`round_record.py new` writes the `Broad gate` row on every record it generates,
so above the cutoff an absent row cannot arise honestly — the arm's own
docstring, the phase record, a case docstring, and the ledger's G2 row. G2's
wording moved because the arm went from three states to four; the fact all four
state did not move at all. -->

| Path | Quote | Grounds |
|---|---|---|
| `skills/code-review/orchestration.md` | The quote is the anchor, so an exemption stops holding the moment the text changes | About the per-survivor row's QUOTE anchor, which this fix pass did not touch. What changed is the RANGE anchor, one paragraph below, and this sentence is still exactly true |
| `CHANGELOG.md` | the quote is the anchor, so the exemption stops holding the moment that text changes | The shipped release note for #297's per-survivor rows. The quote anchor is unchanged, and a released section is not edited to match a later branch's wording |
| `seal/specs/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks/changelog.md` | the quote is the anchor, so the exemption stops holding the moment that text changes | #297's own changelog fragment, same sentence and same reason. It ships the quote anchor, which holds |
| `seal/specs/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks/plan.md` | The quote is the anchor, so the exemption stops applying the moment the text changes | #297's plan, stating the quote anchor. A plan records what was decided and the decision is unchanged |
| `skills/code-review/scripts/survivor_check.py` | quote is the anchor, so the exemption stops applying the moment the text changes | The module docstring's own sentence about the quote anchor, ten lines above the range-anchor paragraph this fix pass rewrote. Correcting it would make it false |
| `skills/code-review/scripts/survivor_check.py` | Run the check over a different range and the row does not hold | `read_exemptions`, and this is the CORRECTION rather than a survivor of it. Striking the false bound through in `phases/phase-3.md` counts as removing it, so the range then scores the true version of the same clause — which opens *but* and names the second anchor — against the struck one. There is nowhere for this to be corrected to |
| `seal/ledger/1788912166-red-for-following-the-documents-green-for-ignoring-one.md` | a spec that no longer resolves silences nothing and is printed rather than refusing the run | G6, and the claim is untouched: resolution and the loud direction are exactly what the fix pass kept. It matched because the changelog sentence stating the same fact was reworded around it |
| `seal/specs/1788912166-red-for-following-the-documents-green-for-ignoring-one/phases/phase-2.md` | it is the one decision in this phase a reviewer should weigh rather than check | A phase record saying what the phase asked a reviewer to weigh. Round 1 weighed it and found its grounds false, which the same record now says two paragraphs down — the sentence is the record's own past state and correcting it would erase the thing that worked |
| `tests/test_chain_check_at_the_pull_request.py` | above the cutoff an absent row cannot arise honestly | The absent-row case's docstring and the ledger's G2 row state one fact, and the fact is unchanged. G2's wording moved because the arm went from three states to four, not because this sentence stopped being true |
| `skills/code-review/scripts/chain_check.py` | writes this row on every record it generates, so above the cutoff an absent row cannot arise honestly | The arm's own docstring, stating the same unchanged fact. It is the SOURCE the ledger row cites, so correcting it to differ from the row would invert which of the two is authoritative |
| `seal/specs/1788912166-red-for-following-the-documents-green-for-ignoring-one/phases/phase-2.md` | writes this row on every record it generates, so above the cutoff an absent row cannot arise honestly | The phase record's reasoning for the absent-row judgment. The judgment stands and this half of its reasoning was always true — what round 1 overturned is the OTHER half, and the same record now says so two paragraphs down |
