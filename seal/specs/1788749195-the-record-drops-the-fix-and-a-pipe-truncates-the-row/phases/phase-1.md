# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — phase 1

<!-- seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 007436a |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Escape a bare `|` inside a cell the record COPIES, in every table `new`
copies and in `close`'s fix table, so the row keeps its header's width.
Phase 1 before phase 2, and `plan.md` says why: #187 makes the fixes section
the durable home for a paste-ready fix, a paste-ready fix is where a `|`
comes from, and escaping first is what keeps the two from compounding in the
same run.

`plan.md`'s Alternatives are settled — escaping, not refusing, on
`CLAUDE.md`'s first goal — and `cell()` is explicitly not the site: it
composes what the writer writes and refuses a pipe there, where the copy path
carries what the reviewer wrote.

Also asked, and answered below: whether any record the generator has written
since it shipped carries a truncated row.

## What this phase found

**Eight rows in this repository's 125 committed records are over-wide, and
every one of them has its pipe inside a backtick code span.** Counted by
splitting each record's tables and comparing each body row's width against
its own header:

| Record | Width | Where the pipe is |
|---|---|---|
| `1788184145…/rounds/round-2.md:22` | 6 vs 5 | Grounds, inside a code span whose backtick runs are unbalanced |
| `1788433011…/rounds/round-2.md:45` | 3 vs 2 | `What was run` — the FIRST column of the probes table, `` `grep -c '^\| L'` `` |
| `1788501054…/rounds/round-3.md:88` | 7 vs 5 | Grounds, `` `Fixes checked by \| nobody \|` `` — two pipes |
| `1788501054…/rounds/round-4.md:91` | 6 vs 5 | Grounds, `` `Contract changes \| none` `` |
| `1788501054…/rounds/round-5.md:79` | 6 vs 5 | Grounds, the same span |
| `1788501054…/rounds/round-6.md:76` | 6 vs 5 | Grounds, `` `grep -c '^\| R[0-9]'` `` |
| `1788501054…/rounds/round-7.md:95` | 6 vs 5 | Grounds, `` `New units \| none` `` |
| `1788501054…/rounds/round-9.md:75` | 6 vs 5 | **Finding** — the second column, `` `Contract changes \| none` `` |

Those records belong to other work items and are not touched here; each is a
finding for the work item that wrote it.

**The measurement is what settled the shape of the repair, and it settled it
against the obvious one.** The obvious repair is to fold a row's surplus
cells into the last column, because the last column is the free-text one in
every table the record copies. Two of the eight say that is wrong. The probes
table's first column is a command, and a command has a pipe in it; folding
moves half the command into `Result`. And `round-9.md:75` has its pipe in the
Finding column, where folding shifts every later column left — the record's
verdict cell would come out holding the location, and `chain_check` reads
that cell.

So the reading is taken in two passes, `row_cells`:

1. **A `|` inside a backtick code span is text**, not a column break. That is
   the reviewer's own markup saying so, and it is the reading that leaves the
   columns where the reviewer put them. Taken only when it lands on exactly
   the header's width, because an unbalanced backtick run swallows every
   break after it — which is exactly what `round-2.md:22` does, and it is why
   the reading has to be checked rather than trusted.
2. **Otherwise the plain reading, capped at the header's width**, so a `|`
   past the last column stays in the last cell as the text it stood in.

Replayed over all eight rows: every one comes out at its header's width, and
seven of the eight recover the reviewer's own placement through pass 1. The
eighth — the unbalanced-backtick row — lands its tail in the last column,
which is the stated limit and is pinned by
`test_a_bare_pipe_before_the_last_column_keeps_its_text`.

**The cap could not be built by rejoining already-split cells.** `split_row`
strips each cell, so rejoining `a |= b` with `" | "` produces `a | = b` — the
first case written for this went red on exactly that space. The cap has to be
applied while the row is still text, which is why `split_cells` takes a
`limit` rather than `row_cells` joining afterwards.

**`split_cells` with both knobs off has to BE `reader.split_row`.** The
record is read back through that function by `chain_check`, so a cell this
composes and that one reads differently is a cell the pull-request check
reads differently from the record. `row_cells` therefore takes the reader's
own answer wherever it fits and reaches for its own spelling only for the
over-wide row, and
`test_the_plain_reading_is_the_readers_own` pins the two against each other
over the shapes they could disagree about — escapes, an empty last cell, a
missing closing pipe, a line that is not a row.

**The fix is one function reached from three sites, which is the class.**
`table_body` reads every row of every table the generator parses, so
`fix_table`'s third cell and `verdict_rows`' verdict column are fixed by the
same change as `table_of`'s copy; `close`'s two direct reads of a verdict row
out of `raw` are the two that `table_body` does not cover, and both moved.
Nine mutations, one per site and one per branch of the new units, and all
nine turn the two modules red.

**What phase 2 inherits.** A paste-ready fix reaches the record as a fenced
block, and a fence is copied whole rather than re-serialised — so nothing in
phase 2 goes through `row_cells`, and the two repairs do not meet. That is
the ordering `plan.md` asked for, and it holds for the reason it named.

**The gate argument** (`CONTRIBUTING.md` §*What a change to a gate must
carry*). This changes what `round_record.py` writes into the file
`chain_check` gates a pull request on, and it adds no refusal: the failure
direction is that the generator ALLOWS more — a row it used to copy wrongly
it now copies whole — and no input that exited 0 before exits non-zero now.
The prompt budget is zero: nothing here asks a person anything, which is the
whole of why `plan.md` refused the refusing alternative. Platform: no process
inspection, no path resolution, no encoding boundary — the change is string
handling over text already read.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `table_of`'s verbatim copy of a report row (`raw[i].strip()`) | `copied_row`, which re-serialises the same raw line through `row_cells` and `escape`. It still reads `raw` rather than the comment-stripped `lines`, so a comment a reviewer wrote inside a cell is still theirs to keep — and the comment-straddle RIDER above `swallowed` is unchanged by this phase |
