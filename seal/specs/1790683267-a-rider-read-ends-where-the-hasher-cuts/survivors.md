# Survivors — a rider read ends where the hasher cuts

`survivor-check --range origin/release/v0.16.0...HEAD`, run by phase 1 at
`28e9bdb`, reported two places sharing phrases with the `comment_blocks`
docstring paragraph and code comment this range removed along with the
reader's step-over. Both were read against `rider_check.py` as it stands after
the fix. Both describe an earlier round's finding as history, and what each
says of the reader is still true of what it does.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_every_reader_ends_a_line_where_gfm_does.py` | `region_lines` cuts blocks out of GFM lines, so it never cut that one | the docstring of `test_a_rider_marker_after_a_break_gfm_does_not_honour_is_no_rider`, which records F's round 3, 🟡 3 as found. Its last sentence, "The reader steps over it", is what the reader still does: a marker piece mid-line on a GFM line that opens no comment is in no block `comment_blocks` returns, so `riders_in` reads no rider there, and the case is green. The case is an existing one, and S8 of this item's spec keeps existing cases unedited apart from S10's index |
| `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md` | a mid-line marker piece is stepped over only where `comment_blocks` over the GFM lines does not cut its line | P5-1's dated `Re-read 2026-09-29 in round 2's fix pass of work item 1790655302` note, which records the step-over as it stood then. The same row now carries this item's `Corrected 2026-09-29 by work item 1790683267 (#682)` note in its claim, saying the step-over is gone, and its `Re-read` note after this one; a dated note keeps the state it records |
