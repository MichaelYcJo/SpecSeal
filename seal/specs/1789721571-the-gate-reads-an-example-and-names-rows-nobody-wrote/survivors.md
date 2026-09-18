# the gate reads an example and names rows nobody wrote — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing".

**A row that excused nothing in the range it was written for is removed, not
left standing.** `exempted` matches on the path and on a run of the quote's
words in the candidate's own text, with no tie to a range — so a row nothing
matched is not a dormant row, it is a standing silencer for every later range
that happens to carry that wording. Two rows written in round 2's fix pass
were in that state, naming `plan.md` and `hooks/config.py`, and round 3
measured it: the check exits 0 naming two excused survivors and those two
matched no candidate at all. Their reasoning was sound and it is kept in the
fix pass's own hand-back and in round 3's report; what is removed is the row,
because a row that anchors nothing is the one shape that cannot degrade when
the text it names changes.

A row that DID excuse a survivor stays after its range merges. It did its
work, and the quote still anchors it.

**Removing a row is itself an edit the check reads, and the effect is worth
knowing before somebody meets it.** A row's quote is text in this file, so a
range that DELETES the row counts that quote as wording the range removed —
and the place the quote named is then reported as a survivor. Measured at
`9c19955`: over `95de3cd..HEAD`, the range that removes the two rows, the
check names `hooks/config.py` and `plan.md`, which are exactly the two paths
those rows quoted. Over `origin/release/v0.12.1...HEAD` — the range the
sealer's broad gate runs, where the rows were both written and removed inside
it — the check is exit 0 with no survivor standing and no exemption needed.
So the report is an artefact of measuring a sub-range, not a defect the
removal introduced. `seal/follow-up.md` carries the same mechanism running the
other way, where WRITING a row silences its survivor through the diff as well
as through the exemption. -->

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | `Measured before the fix: sites 1, 2 and 3 printed *nothing was written*` | What this range removed is a paragraph of `overview.md` §*Fed back into the spec*, rewritten because round 2's ⬜ found the wording divergence recorded under a heading `templates/sdd-overview.md` reserves for clauses this work ADDED. The measurement itself is not withdrawn and the standing sentence is the case's own record of why it exists — the place that record belongs. Removing it would leave the case with no account of what it was written for |
| `skills/verify/scripts/broad_gate.py` | `So each of those sentences says *no ROW was written*, which is what the value supports` | The same rewritten paragraph. This is the code's own statement of the rule, in the docstring of the function that applies it, and it is still exactly what the four arms do. The memo pointing at it is what moved; the rule did not |
| `skills/verify/scripts/broad_gate.py` | `return next((line for line, _reached in refused if names_this_row(line)), None)` | The wording this range removed is `missing_row`'s own copy of that idiom, replaced by a loop because that function now needs two more things from the same walk — the refused lines below the quoted one and the refused lines below the stopping one. `refused_broad_row` needs neither: it answers one question, *which refused line is this gate's row*, and the idiom is still the right shape for it. Not a claim the range corrected, and rewriting it as a loop would be a change made to quiet a report |
| `seal/specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is/questions.md` | `There are two causes and the span was the smaller one.` | The wording this range removed is `missing_row`'s docstring counting the gate's refusals — *there are two, because there are two causes and a person can act on only one of them* — which is now four. The standing sentence is a closed work item's record of a different subject entirely: which of two causes made a measured duration wrong. It shares the phrase `there are two causes and` and nothing else, and correcting it would make a record say something that work item never decided |
