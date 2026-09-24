# 1790260566-a-row-inside-a-fence-reads-as-live — survivors

What `survivor-check` reported over this branch's range, and why each place
is correct where it stands. Read 2026-09-25 at `e78ccea9`.

| Path | Quote | Grounds |
|---|---|---|
| skills/verify/scripts/unverified_check.py | also breaks on U+2028, U+0085 and form feed, so a cell holding one of those followed by | The removed text is `fold_ledger.py`'s copy of the open-rows rule (#487). This docstring is the one rule that copy now loads, so the sentence stands where the rule is |
| skills/verify/scripts/unverified_check.py | A table is a run of lines starting with | The same removed copy (#487); the rule's docstring is its one home |
| skills/verify/scripts/unverified_check.py | its first line is the header when the second is a separator, and neither is a body row | The same removed copy (#487); the rule's docstring is its one home |
| skills/verify/scripts/unverified_check.py | Table body rows of an evidence-todo file that are still open | The same removed copy (#487); this is the loaded function's own summary line |
| skills/settle/scripts/settle.py | Table body rows of an evidence-todo file that are still open | `settle.py#open_rows` delegates to the same one rule and keeps its summary line; the removed copy said the same thing about the same rule |
| .github/scripts/fold_ledger.py | Byte for byte means three things | A different function's docstring (`demote`) about why a fold splits on a newline alone; it shares two phrases with the removed open-rows copy and is true as it stands |
| .github/scripts/fold_ledger.py | as demote splits them | The same: the split rule for the release file's heading walk, unrelated to the removed copy, and true |
| tests/test_the_ledger_fragments_fold_at_release.py | read the cell's tail after U+2028 as a line of its own | The case this removed ledger row cited; its docstring records round 1's measurement, which is still what the case pins, and the claim now stands as P3-1 of this work item's fragment |
| seal/releases/0.4.0.md | Every `seal/specs/*/evidence-todo.md` in the tree is read, and one open row refuses the fold | A released row about the fold's refusal, which still holds; it shares two phrases with the neighbouring row this branch REMOVED |
| tests/test_unverified_rows_close.py | CommonMark 4.2: one to six hashes, then a space, a tab or the | The oracle's comment, which states the same CommonMark rule the reader's comment restated with the three-space bound added; the oracle's bound is written on the line above it |
| skills/verify/scripts/broad_gate.py | row written INSIDE a code fence | The broad gate's own fenced-row reader, #429's; it shares two phrases with the `#444` follow-up row this branch removed because #444 is fixed |
| tests/test_the_seal_is_taken_once_by_the_sealer.py | over a glob this file joins | A comment about an unrelated test module; it shares the phrase "py over a" with the removed `#444` follow-up row |
| docs/the-broad-gate.md | A fenced example in a config file is not a config row | #429's standing statement for the config reader, which is correct; the removed `#444` row named that work item as the precedent |
| seal/releases/0.12.1.md | 1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote | A released section's marker and heading for #429's work item; the removed `#444` row cited that id |
| seal/follow-up.md | What needs a person is which side moves | Another follow-up row, about the drift report; it shares a phrase with the records-arm row this branch removed because phase 4 answered it |
| seal/follow-up.md | drift report names a coordinate once | The same row as above; it shares a date and a phrase with the removed records-arm row |
| seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/spec.md | States that a fence is a quotation and an HTML comment is an aside, with no qualification | The frame's grounding row, which records what the skill said when the frame was drawn; phase 4 narrowed the skill, and the frame is the record of the question, not of the answer |
