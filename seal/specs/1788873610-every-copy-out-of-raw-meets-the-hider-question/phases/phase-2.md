# 1788873610-every-copy-out-of-raw-meets-the-hider-question — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 2125094 |
| Ran by | smith on `claude-opus-5[1m]` — the spawn prompt named no model. The segment's own harness line is the source; the transcript's `message.model` rows carry the bare id `claude-opus-5`, the same model without the context-window marker |

## What this phase was asked

Close the first of the ticket's three `Done when` lines: *every copy taken
out of `raw` meets the hider question, or the rule says why one does not*.
The spawn prompt named `round_record.py#inherited_rows` as the fourth copy
and carried the ticket's account of it — a verdict row carrying an
unterminated `&lt;!--` reaching a later record, whose `## Deferred` is then
present in the bytes and resolves to zero occurrences through the shared
reader, silently, with the loss re-entering every later record of the chain.

It was told to build the argument on the property rather than on the count:
`grep -n 'raw\[' round_record.py` enumerates the copies, and where a test or
a document states completeness it should state the property, so that a fifth
copy added later is caught rather than described.

## What this phase found

**The ticket's consequence for `inherited_rows` does not reproduce, and the
premise does.** Measured at `8114937`, both paths the ticket names:

| Shape | Measured |
|---|---|
| a `round-1.md` corrected in place with an opener in a `Location` cell, then round 2 generated | refused — `a verdict row has 3 cells`. The opener swallows the row's remaining pipes, because the raw reading treats a `\|` inside a comment as text, so the row comes in under its header width |
| the same with the opener in a `Grounds` cell | round 2's record written and CLEAN, every section resolving. `inherited_rows` copies the `Location` cell alone, so nothing else in the row travels |
| round 1's own record written from a report whose `Grounds` cell straddles | round 2's record clean as well: the loss does **not** re-enter the chain |

So `inherited_rows` is a fourth copy with no hider question — true — and the
silent loss the finding attributes to it is refused today, loudly, by cell
arithmetic. What IS reachable is one step earlier and worse: a report whose
`Grounds` cell opens a comment and closes it on the line below is accepted,
`new` **exits 0**, and round 1's own record has three sections resolving to
zero occurrences while standing in the bytes.

**That relocates the answer from the sources to the destination.** Every copy
lands in one artefact, so asking the question of the record answers for all
of them at once — the three the grid named, the fourth it did not, and a
fifth added later — and it closes the cell the branch had recorded as needing
*balance across the slice*, a question no report-wide guard could ask because
a copied block may legitimately carry a whole comment. Asked at the
destination it needs no knowledge of which slice took the half.

**It also reaches what no question asked of a source can.** `cell` refuses a
`|` and a newline because either breaks the row; `&lt;!--` breaks every reader
below the row, and `--ran-by` and `--broad-gate` pass through no text at all.
Both are cases now.

**A whole-text question on an input read for named sections would refuse a
file this repository already has.** That is why the fourth grid row was not
the answer even narrowed:
`seal/specs/1788826000-a-stamp-names-content-not-a-commit/rounds/round-1-fixes.md`
carries `` `&lt;!--` `` inside a code span on a table row, which blanks that
file's tail — and hides nothing `fix_table` reads, because the rows below it
stand under a different heading. Found by reading all 163 committed records
and every report and fix table beside them through both passes, which was
also what bounded the chosen design: **none of the 163 records has an open
hider**, so the guard refuses nothing this repository holds.

**The completeness argument is a case rather than a comment.**
`test_every_record_this_writes_is_read_back_before_it_is_written` walks the
module's own syntax tree for every call that opens a file in a write mode and
asserts which functions make one. It names two: `write_record`, and
`run_check`, which writes the GitHub event payload `chain_check` reads a pull
request's state from. A third name turns it red, where a grid could go one
row short and stay green. `reach_back` is covered by that case alone and by
no behavioural case, and that is honest rather than a gap: it writes
`cell(chain.CHECKED_BY, "round-N")`, a value that cannot carry a hider, so
there is nothing to construct.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the three `with open(..., "w")` blocks in `reach_back`, `new` and `close` | `write_record`, which all three now call. `seal/ledger.md` R1, R2, R9 and R3 of `1788761915-…` were re-read against the change and their claims stand |
| the `# RIDER:` at `swallowed` carrying the still-open straddle | the fix itself, in phase 2. What stands at that line now is a comment saying the rider is gone and why — `write_record` asks the balance question the function could not. `seal/ledger.md` F2's Notes carries the same, with its strike-through |
| nothing else | `none` |
