# Round 3 — the corrections, applied by the orchestrator in the closing commit

The run is capped: rounds 1 and 2 both closed on fixes, so no round follows
this one. Neither correction below is a code change, and neither was
commissioned as a fix pass. They were applied because what they correct is a
sentence that measurement had just shown to be false, and shipping a false
claim in a ledger row is the one thing a ledger cannot do.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `8a31d08`. The docstring at `tests/test_version_check.py` and row S1·S2·S3 of `seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md` both said the two cases hold together against a careless golden-string update. The round measured that they do not: with the golden brought along in the same edit, an added overclaim, `unmeasured, yet it is picked up`, the restart named first, and the `measured` and `skill bodies` labels dropped all pass at `18 passed`. Both sentences now say what the pair actually holds — the scope qualifier, and nothing else — and name the message as an instruction to a person rather than a check. The row's hash over the edited case was re-anchored with `evidence-check --reverify` in the same commit |
| 2 | fixed | `8a31d08`, by `round_record.py new` itself, which set `round-2.md`'s `Fixes checked by` to `round-3` when this record was written |

## What was deliberately not done

The residual finding 1 names is real and is not closed here: an author who
rewords the notice and updates the golden string in the same edit passes both
cases, and five of the seven properties the deleted predicates held are then
checked by nothing. That is a design question about what an exact pin can
carry, not a defect in this branch's text, and the run is capped. It is filed
as an issue against 0.9.2.
