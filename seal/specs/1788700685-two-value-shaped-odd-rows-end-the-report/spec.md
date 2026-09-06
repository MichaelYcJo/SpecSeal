# Feature Specification: one odd row does not end the report, on the axis the rule is about

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `session_cost.py#parse_time` docstring — *one odd row must not end the report* | The rule this work applies to the axis it was actually about; `count` already applies it to the value axis |
| `skills/code-review/SKILL.md` § *Verdicts that close too early* — an enumeration over an unbounded domain is a recorded limit | #170's enumeration closed the **type** axis and its ledger row states the guarantee over the whole class; the axis has to be named where the row is |
| `skills/agent-contract/SKILL.md` §12 | The class is *every arithmetic operand taken out of a transcript*, and it has two axes: what type the value is, and what a `datetime` carries |

## Scope

**In.** Two crashes reachable from a transcript, both measured at `a9a827b` and byte-identical there:
- a paired call whose `tool_use` and `tool_result` share a timestamp, so `span_s == 0.0` and `report`'s four divisions raise `ZeroDivisionError` — the span line printed, the token block lost;
- a transcript mixing a zone-aware stamp with a naive one, so `analyse`'s subtractions raise `TypeError` with stdout empty, on both the report and `--json`.

And the ledger row that states #170's guarantee, which must name the axis its enumeration ran on.

**Out.**
- Making the numbers *right* for such a transcript. A span of zero is a degenerate reading, and what this work owes is a report that survives it, not one that invents a percentage.
- The harness. Measured over 299 real transcripts: 0 calls with `start == end`, 0 transcripts with `span == 0`, and 94,514 of 94,514 timestamps zone-aware. This harness produces neither shape; the claim is what is being repaired, not a live crash.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A zero span prints what it can | Given a transcript whose only paired call shares one timestamp; when the report runs; then the span line, the token block and the family table all print, and no percentage is invented for a denominator of zero | A case over a synthetic transcript, seen red first |
| A naive stamp does not end the report | Given a transcript mixing a zone-aware stamp with a naive one; when the report runs; then it prints, and the odd row is handled the way an unparseable one already is | A case over a synthetic transcript, seen red first, asserting both the report and `--json` |
| `--json` survives both | Given either transcript; when `--json` runs; then it emits an object, not a traceback | The same two cases, second arm |
| The guarantee says what it covers | Given #170's ledger row; when it is read; then it names the axis its enumeration ran on, so a next editor cannot read *no survivor* as the whole class | The row, and the case that pins the document claim if one exists |

## Data & interfaces

No CLI change and no output-format change for a transcript this harness produces — the two paths are unreachable there, which the cases build by hand.

## Open questions → questions.md

Whether a naive stamp is normalised at `parse_time` or dropped like an unparseable one is settled in `plan.md`'s Alternatives, not here.
