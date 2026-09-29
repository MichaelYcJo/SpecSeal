# Survivors — the walk leaves every inline HTML construct uncertain

The sealer's sweep (`survivor-check --range 86256492...HEAD`, at `a0e84a56`)
reported two places sharing phrases with `hooks/blocks.py` sentences this range
rewrote from "an inline comment" to every kind of inline raw HTML. Both were
read against the code as it stands after the merge of `release/v0.16.0`, and
both describe the comment shape as history, which is still true.

| Path | Quote | Grounds |
|---|---|---|
| `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md` | the line opened an inline comment before it and left it open | R1-1's dated `Corrected 2026-09-29 in round 2's fix pass` note, which records the defect #667's round 2 fixed, for the comment it was found on. The row's own claim was corrected in phase 2 of this work item to "leaves inline raw HTML of any kind open", and its `Corrected … in phase 2 of work item 1790659274` note follows in the same cell; a dated note keeps the state it records |
| `tests/test_the_hooks_hide_what_a_renderer_hides.py` | a piece that starts inside an inline comment its line opened | the comment over `FOUND`'s round 2 document, which is a comment shape (`"x " + OPEN + " a" + …`) and is described exactly; the next comment in `FOUND`, `# #673: the same piece inside every other kind of inline raw HTML`, introduces the documents for the other kinds |
