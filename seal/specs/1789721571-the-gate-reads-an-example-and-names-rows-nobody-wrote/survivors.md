# the gate reads an example and names rows nobody wrote — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

| Path | Quote | Grounds |
|---|---|---|
| `skills/verify/scripts/broad_gate.py` | `return next((line for line, _reached in refused if names_this_row(line)), None)` | The wording this range removed is `missing_row`'s own copy of that idiom, replaced by a loop because that function now needs two more things from the same walk — the refused lines below the quoted one and the refused lines below the stopping one. `refused_broad_row` needs neither: it answers one question, *which refused line is this gate's row*, and the idiom is still the right shape for it. Not a claim the range corrected, and rewriting it as a loop would be a change made to quiet a report |
| `seal/specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is/questions.md` | `There are two causes and the span was the smaller one.` | The wording this range removed is `missing_row`'s docstring counting the gate's refusals — *there are two, because there are two causes and a person can act on only one of them* — which is now four. The standing sentence is a closed work item's record of a different subject entirely: which of two causes made a measured duration wrong. It shares the phrase `there are two causes and` and nothing else, and correcting it would make a record say something that work item never decided |
