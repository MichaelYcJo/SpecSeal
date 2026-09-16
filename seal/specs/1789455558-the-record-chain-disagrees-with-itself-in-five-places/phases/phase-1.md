# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — phase 1

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `14b617c` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

#404, and it goes first because phase 2 reads the map this phase builds.
`close`'s forward map takes the **first** row at a coordinate — `setdefault`
in place of the plain assignment — so it and `inherited_rows` resolve a
repeated `Location` the same way. The class to enumerate is every place
`close` keys a map by a verdict cell. Q4's corpus count is re-measured here
rather than inherited from the issue, because an aggregate in prose is not a
coordinate.

Verified by `bin/test tests/test_the_fixes_close_the_record.py`, with the
plain assignment restored as the red-first mutation, and by the corpus count
re-run — a non-zero count is what forecloses the refusal alternative.

## What this phase found

**Q4, measured 2026-09-15 at `c36e0fe0`, through the module's own readers.**
366 `round-N.md` files stand under `seal/specs/*/rounds/`; 247 parse under
`verdict_rows`, the keying reader `close` itself uses. Of those, **71 repeat a
`Location` in their verdict table, over 105 coordinates**. So refusing a
repeat is foreclosed: it would refuse 71 records this repository has already
written, and first-wins is the only option left.

**The defect is still latent, and the second figure is what says so.** Of
those 105 repeated coordinates, **0 pair a numbered row with an unnumbered
one** — the pairing the map and the section can actually disagree about. The
issue reported 0 of 74 on a smaller corpus; the corpus has grown by half and
the figure has not moved. What makes the repair worth a phase rather than a
note is unchanged: `agents/warden.md` asks a reviewer for exactly the shape
that produces the pairing.

**The class has one member, and reading it is what says so.** `close` keys
three maps off the record: `rows` (from `verdict_rows`) and `fixes` (from
`fix_table`) are both keyed by finding number, and `finding_number` refuses a
duplicate id in either table before the map is built — so neither can carry a
repeat at all. `now` is the only map in the subcommand keyed by a cell whose
repetition is legal, and it was the only last-wins one.

**A2 needs the numbered row in the middle.** A repeat whose numbered row sits
first agrees on both sides by accident, whichever rule each side follows, so
the case that pins the agreement builds three rows at one coordinate with
`🔴 1` between an unnumbered confirmation and an unnumbered correction. An
unnumbered row is constrained in two ways the fixture has to respect:
`OWED_MARKERS` refuses 🔴 and 🟡 without an id, and `says_open` refuses any
unnumbered row whose Verdict cell reads `open`. 🟢 with `verified` and ⬜ with
`withdrawn` are what is left.

**Both red-first mutations were run and both went red in the predicted
direction**, which is the second thing worth carrying forward: the two cases
fail on different halves. A1 fails on the value (`round 1's 🟢 — verified`
where `round 1's 🔴 1 — fixed` was owed) and A2 fails on the agreement
(`round 1's ⬜ ` against `round 1's 🟢 `), so a future change that repairs one
side alone still turns one of them red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the assignment it replaces said nothing the `setdefault` does not | none |
