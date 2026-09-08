# Implementation Plan: every published reading carries three wrong rows

## Summary

Three independent defects in one module, taken in the order that puts the
smallest first and the one with a design decision last.

`#193` arrived with a verified patch and a case seen red, so it went first and
cost one conjunct plus the second shape its own comment names. `#202` is one
line of meaning — which row of a split message wins — and the work was the
fixture that can tell the two behaviours apart, because no case written before
it could. `#200` is the one that needed a decision, and it is the only place
this plan chose between shapes the ticket left open.

## Technical context

**A streamed assistant message reaches the transcript as several rows sharing
one `message.id`.** Both readers in the file dedup on that id and both kept
the first row. For `token_totals` that is the defect: `output_tokens` grows
across the rows. For `load` it is not, because the fields it reads —
`input_tokens` and `cache_read_input_tokens` — are fixed when the request is
made and repeat unchanged; measured identical first-row and last-row over
13,425 messages.

**`family` is handed a command whose whitespace `load` has already
flattened.** A heredoc that writes a document therefore arrives as one line
with the whole document in it, which is how a `cat > …` was charged to `test`.

## The decision #200 left open

The ticket named three shapes and decided none.

| Shape | Verdict |
|---|---|
| Read the runner from `seal/config.md` | Rejected. It is the most faithful and it is the only one that cannot work for a repository that has not filled the row in — which is every installed repository on the day it installs. It also puts a `PreToolUse` reader's parser inside a script that takes a transcript path for an argument, where the repository the transcript belongs to and the repository the command runs in need not be the same |
| Widen the pattern | **Taken, for the shapes that mean the same thing in any repository**: a script named `test` invoked by path, and the runners a language's own convention names. The objection the ticket raises against it — *leaves the next repository with the same defect and no sign of it* — is answered by the row below rather than accepted |
| A family for the project's own scripts | Rejected. It does not say what the command does, which is the ticket's own objection to it, and `bin/evidence-check` would be no better described by `project` than by `other` |
| **Print what the table could not name** | Added, and it is what makes the widening honest. When `other` leads by seconds the report says the largest family names nothing and prints the slowest command charged there — the exact string a family would have to learn. A repository whose runner nobody here can guess gets a sign instead of a silently empty `test` row |

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `token_totals` keeps the LAST row per id | Right under an ordering the transcript format does not promise. Measured: last and max agree on all 13,425 messages, 0 rows out of order — so the case that separates them had to be built rather than found | Rejected; the maximum costs one dict instead of a set |
| Repair `load`'s per-turn `output` rather than remove it | Nothing reads it: `token_thirds` takes index 1, `analyse` takes `len(turns)`, no other index appears in the file. Repairing it leaves a correct number nobody consumes; leaving it leaves the first partial count waiting for its first reader, which is how #202 was written in the first place | Removed, with the shape a future consumer should take written where it was |
| Cut at any `<<` for the heredoc question | `echo 'a << b' && pytest` loses a real run. That is the same direction as the defect being fixed, on a shape that occurs in real command lines | Rejected; the delimiter must be quoted or upper-case |
| Re-derive the published readings in this work item | The transcripts still exist and a re-run is cheap, but what a corrected reading says about #51's bands is the question #145 and #149 are scheduled to ask | Out of scope, stated in `spec.md` |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #193 — the `growth[0] > 0` conjunct and the signed input filter, with three cases | `pytest tests/test_session_cost.py -q`, two mutations | 1b33418 |
| 2 | #202 — the maximum per field per message id, `load`'s tuple narrowed to input counts, four cases | the same module, four mutations | 0253001 |
| 3 | #200 — the widened family, the heredoc cut, the `unnamed` line, three cases | the same module, seven mutations | 74baaf2 |
| 4 | The records: ledger fragment, changelog fragment, questions, phases, overview, and the three boxes in `docs/flow.md` | `evidence_check.py --reverify` then `--strict`, the suite unchanged | this commit |

## Operational impact

**Every number the meter prints changes.** `output` rises — 1.7× over the
corpus measured here — and the `by family` table moves in both directions:
runs the pattern could not name arrive in `test`, and words matched inside a
document leave it. A reading taken before this release and one taken after are
not comparable, and nothing in either says so. That is the cost of the fix and
it is why `docs/flow.md`'s §0.9.5 items sit after this one.
