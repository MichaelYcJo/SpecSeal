# 1788873610-every-copy-out-of-raw-meets-the-hider-question — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 0b99eb9 |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Close the second of the ticket's three `Done when` lines: *a comment that
opens inside a copied block and closes outside it is refused by a message
naming the comment rather than a fence that closes*. The spawn prompt carried
the executed evidence — a fenced block holding `&lt;!-- a note`, the block
closed, and the `-->` on the next line, refused at `c8d2907` as *a fenced
block in the report is never closed* while every fence in that report closes
— and named `round_record.py#swallowed` as the coordinate.

It was also told that new cases must reach the shape the old ones could not:
both existing cases use a comment that never closes at all, so they pin the
question order without ever reaching the balanced straddle.

## What this phase found

**The refusal is one boolean away from correct, and the boolean is which
TEXT the fence question is asked of.** A comment crossing a block's closing
fence leaves the fence open in `strip_comments(text)` and closed in `text` as
written. A fence nobody closed is open in both. So one extra `blank_fences`
call over the raw lines separates the two, and there is no need to find the
comment or the block: the pair of answers names the shape.

**The order of the two questions was written out once per text, and that was
already two copies with a third due.** `swallowed` carried a pair of raises
and `build` carried the same pair for the round paragraph, each with its own
paragraph explaining why the comment comes first — and the reason is a
property of `readable`'s pass order, not of either text. Phase 2 needed the
same questions asked of a record, which would have been a third copy. So the
pair moved into `open_hider`, the order with it, and each text now
contributes its three sentences and nothing else. What stayed in `swallowed`
is the positional half of its rule, which really is about the report:
`REPORT_TABLES` and `TERMINAL_LINES`.

**The third answer made an existing assertion too loose, and the next phase
would not have caught it.** Two committed cases pin the question order by
asserting the refusal says `HTML comment`. The straddle sentence says that
too, so after `open_hider` grew its third answer, asking the fence question
first turned those two cases GREEN with the wrong message — a comment that
never closes reported as one that *closes outside the block*. Found by
running the order mutation rather than by reading, which is the method this
release is named for. Both cases gained an assertion on `never closed`, which
is what separates the two answers, and the mutation is red again.

**What the coordinate in the message costs and buys.** `opens_at` walks
prefixes and asks the reader's own pass of each, which is quadratic in the
line count. The alternative is a second reading of where `&lt;!--` and a fence
marker sit — and a second reading of exactly that is the check/copy asymmetry
this module has been bitten by three times. The walk cannot drift from the
pass it calls, and a record is a few hundred lines.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the pair of never-closed raises in `swallowed` | `open_hider` and `hiders_close`, called from the same place in `swallowed`. `seal/ledger.md` F1, F3, F4 and F5 were re-read against the change and their claims are about the positional loops, which did not move |
| the pair of never-closed raises in `build`, and the paragraph explaining the order | `open_hider`'s docstring, which is now the one place the order and its reason live. `build` keeps a shortened comment saying which text is asked and pointing there |
| nothing else | `none` |
