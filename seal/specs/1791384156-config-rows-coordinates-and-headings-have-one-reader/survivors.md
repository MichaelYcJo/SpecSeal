# Survivors — config rows, the ledger coordinate and a markdown heading have one reader

`survivor-check --range origin/release/v0.21.0...HEAD` named four places that
still carry wording this item's range removed. Each was read at the fix
pass's head. Two are released ledger rows, frozen by `Ledger frozen from`,
whose families this item's fragment answers; one is a sentence about
`routing.md` that is still true where it stands; one is another work item's
frame quoting that sentence, a record of its own time.

At the build's head the sweep named 33 places (round 1, 🔴 2). Twenty-nine
of them were patterns of their own — a redirection, an HTML tag, a pact
name, a slug — sharing only character classes with a removed pattern:
twenty-seven with `settle.py`'s copy of the coordinate grammar, and two
with `rider_check.py`'s stamp pattern, whose `@[0-9a-f]{6,12}` the oracle
also holds (round 2, ⬜ 3). Round 1's fix pass froze that copy as S7's
oracle in `tests/test_settle_reads_before_it_removes.py#SETTLE_COPY_AT_0_20_0`,
so the copy's text stands in the tree again and the sweep no longer reads it
as removed. Those 29 were read too, and none was a sentence this work
corrected.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.9.1.md` | **A gate is not a writer.** `hooks/config.py#declared_mode` folds a file that will not open into *declared nothing*, which is right for `seal mode` | the notes cell of a released ledger row, frozen by `Ledger frozen from`; this item's fragment carries its `Corrected · S7–S10` row, which supersedes the row's family and states that the reader now answers `refused` |
| `seal/releases/0.15.0.md` | `heading_level` keeps the reader's own test for a heading — `startswith("#")` — and adds only the depth, so a `#120` at column 0 still ends a section | the notes cell of a released ledger row, frozen by `Ledger frozen from`, recording what was true on its date; the row's claim, that a section ends at a heading of its own level or shallower, still holds and is re-read in this item's fragment (`Re-read · A1`), and the fragment's K19 row states the rule that replaced `startswith("#")` |
| `hooks/routing.py` | A file that cannot be read is not an answer somebody gave, so the gate goes back to asking. | true as it stands: a `routing.md` that cannot be read is no declaration and the commit gate asks; the removed sentence was `hooks/config.py`'s, whose reader now refuses an unreadable `config.md` instead of reading it as nothing |
| `seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/spec.md` | A file that cannot be read is not an answer somebody gave", and `1790635413` pinned R2 the same way. | another work item's frame quoting `hooks/routing.py`'s docstring, which still says this; a record of its own time |
