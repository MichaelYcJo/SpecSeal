# 1788817290-the-derivation-misreads-and-the-record-refuses-the-id — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 051ebfa |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

#227, of the three the branch carries: round-prefixed finding ids (`R2-1` …
`R2-8`) collapse toward one key, and the refusal names neither the format it
wants nor the rows it read. The handoff put a contract in force for the rest
of the release run — **finding ids are bare integers** — and required that
the refusal name it. The ticket itself offered two repairs, accepting a
prefix or refusing with the format spelled out, and left the choice open.

## What this phase found

**The corpus is what settled the choice, and it was measured before a line
was written.** Running all 131 committed `round-N.md` files through the
module's own `table_body`/`verdict_rows` path under both rules: 130 parse, 82
pass under either, 46 already refuse today, and **2 pass today only by
miscounting**. `1788420761-…/round-4.md`'s `r3 🟡 2` keys as finding **3** —
the first digit run is the `3` in `r3` — and `1788433011-…/round-3.md`'s
`🟢 round 2's finding (🟡 4)` keys as **2** where the cell names 4. So the
strict rule takes away two wrong answers and no right one, which is a
stronger argument than the ticket's own guess and is what the design rests
on.

**The ticket's diagnosis of the mechanism is wrong in a way that does not
matter.** It says the parser "appears to take the last digit run"; it takes
the FIRST (`NUMBER_RE.search`). Both produce the reported collapse, so the
repair is the same — but the phase record says so because a later reader
comparing the ticket to the code would otherwise find a contradiction and
have to re-derive it.

**The severity marker is inside the cell, which bounds the rule.** Every real
`#` cell is `<marker> <digits>`, and a rule that read the marker as *not
digits* would refuse every record ever written. `[^\w\s]` reaches 🔴 🟡 🟢 ⬜
❓ ✅ and reaches no letter, which is exactly the line between a marker and
`r3`.

**A mutation found a tolerance nothing was holding.** Dropping the emphasis
strip left all 24 cases green, so `**1**` — the obvious spelling beside the
`**fixed**` the next column already carries — was unpinned. Four spellings
pin it now.

Phase 2 needs one thing from here: `finding_number` is the single place
either table reads that column, and a case asserts there is exactly one match
site. A later phase adding a third reader is what that case exists to catch.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `NUMBER_RE`, the unanchored first-digit-run pattern | nowhere — it had two callers, both now read `FINDING_ID_RE` through `finding_number`, and a case asserts the name is gone from the module so it cannot come back as a second reader |
| the refusals `a fix row's \`#\` names no finding` and `a verdict row's \`#\` names no number` | replaced in place by one message that names the format, quotes the cell and quotes the row; nothing else read those strings |
| the refusals `the fix table has two rows for finding N` and `the record has two verdict rows numbered N` | replaced by one that quotes both offending rows; `docs/review-chain-spec.md` §*The finding id* quotes the old wording as the reported symptom, so the sentence a reader searches for still lands somewhere |
