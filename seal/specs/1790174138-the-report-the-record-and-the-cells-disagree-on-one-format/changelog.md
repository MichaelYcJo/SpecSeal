- **The warden's report, `round_record.py` and the record's cells agree on
  one format (issues #503, #437, #505, #382, #436, #217, #218, #174).** Three
  reviewers in one release were refused by the record generator for the shape
  of one cell, and the generator and the checkers had five quieter
  disagreements with the cells they write and read. Now the reviewer copies
  the standard rather than being told it: `agents/warden.md`'s fenced
  skeleton shows a numbered 🟡, a bare 🟢 carried closure with `confirmed`,
  and a bare ❓, says the severity goes in the `#` cell and an empty cell is
  the one shape refused, names the five markers with `✅` outside them,
  allows `###` under the two fenced sections, and asks for `&lt;!--` wherever
  a comment opener is meant. The worked carried-closure row — a bare marker,
  `confirmed` never `fixed`, no 🔴 anywhere in it — is one text in the
  warden, the review skill, the specification and the round template, pinned
  to each other, and the skeleton itself is run through `new`.
  The generator reads a report section to the next heading of its own level
  or shallower, so six fixes under six `###` entries reach the record where
  they used to arrive as *no paste-ready fix in the report*, and a table
  hidden under a `###` is refused rather than silently lost; `Target SHA`
  holds the commit `--target` resolved to rather than `HEAD~1` as typed.
  `chain_check.py` refuses a `Fix range` still saying the fixes are not yet
  written beside a `round-N`, as it already refused the two surface rows,
  under `RANGE_FROM` and no cutoff of its own; `evidence-check`'s records arm
  reads the lines after an HTML comment the record never closes, the way it
  already read an unclosed fence, so a missing `-->` is no longer a way past
  it. The printed bound reports a count walk that stopped after reaching
  two as the error the gate already returns, where it printed `one
  reopening remains` one round after `this record ends the run`
  (584-sequence differential against `stopping_floor`: 16 disagreeing, now
  0). And the `Broad gate` cell holds one entry per full-suite run, newest
  first — `seal` writes the new run in front and keeps the earlier one as
  `earlier run` — for the last round record and `broad-gate.md` alike, so a
  re-seal records a second run instead of erasing the first; a first seal is
  byte-identical to before, and the reader still takes the first SHA as the
  run. #159 is deferred to the release after, with its design sketched in
  the work item's plan.
