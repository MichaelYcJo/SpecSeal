# 1788472135-the-run-outlives-its-last-finding — phase 3

<!-- seal/specs/1788472135-the-run-outlives-its-last-finding/phases/phase-3.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 19ce128 |

## What this phase was asked

Build phase 3 only: three refusals in
`skills/code-review/scripts/chain_check.py`, plus the row-presence check that
pairs with the first, each grandfathered by work-item id and each seen red
before the code that makes it green.

1. The floor row is read on every record. `| Loses a record or crashes |`
   absent, empty, or holding a value that is neither `no` nor `yes — <what>`.
   Absent is the only one the grandfathering reaches: present-and-malformed
   fails on any record, the split `fix_surface` already makes.
2. `New units` entries carry a depth. An entry with no depth fails; `none`
   stays an answer with or without a reason.
3. Depth 2 or above is refused, and the failure names where the work goes
   instead — deferred with a named answerer, or an issue. A refusal that does
   not name the exit is the wall phase 2 was ordered before phase 3 to avoid.
4. A record that met the floor is followed by at most one more round record.
   One later record is the verifying round and refusing it would refuse the
   round that ends a run honestly.

`FLOOR_FROM` and `DEPTH_FROM`, both `1788472135` — this work item's own id —
in the shape and with the recorded reasoning of `STRICT_FROM` and
`SURFACE_FROM`, pointed at rather than restated.

One consequence was named for the segment to design against: the two cutoffs
are this work item's own id, so **this branch's own review rounds are the
first records held to both rules**, and a shape refused with no honest
spelling would be the wall itself.

Coordinates given rather than searched for: `chain_check.py:1375`
(`fix_surface`), `:1466-1483` (the per-entry walk), `:1800` (the wiring),
`:1355` (`says_none`), `:350` (`SEPARATORS`), `:701` (`field`), `:709`
(`table_rows`), `:557` (`round_records`), `:536` (`read_record`), and
`tests/test_the_fixes_name_their_surface.py:223` and `:234` as the
grandfathering and cutoff-second cases to mirror.

Segment constraints: no changelog or ledger fragment (phase 4's), one venv
reused rather than `uvx --with pytest` per call, named test files rather than
a `grep -rl` sweep, and narrow verification only.

## What this phase found

**Two sibling test files had to gain the rows before any case here could
pass, and that is the first real evidence the rules have an honest spelling.**
`tests/test_the_fixes_name_their_surface.py` and
`tests/test_the_last_rounds_fixes_are_checked.py` both build fixture records
under work-item ids well after the cutoffs (`1799000000-a-later-work-item`),
so every one of their passing cases went red the moment the floor row became
required — 476 cases across the twelve files that run this checker, one
failing on a rule neither file pins. Both `record()` builders now write
`| Loses a record or crashes | no |`, and the one fixture that listed units
without depths now writes `` `SURFACE_FROM` (depth 1); `fix_surface` (depth 1) ``.
The work this cost is the check being applied to records nobody wrote for it,
which is what the branch's own rounds will be.

**The two grandfatherings are not one grandfathering, and the difference is
new.** `STRICT_FROM` and `SURFACE_FROM` both excuse a row that is absent,
because a merged record has no honest repair. The floor's fourth refusal is
not about a row at all: a run that went three rounds past its floor is
excused because the repair is *a round that was never spawned*, which nobody
can write now. A malformed row is still refused at any age. Both reasons are
in `docs/review-chain-spec.md`'s new subsection, because the existing
paragraph on why older records are excused does not cover the second.

**`templates/config.md`'s *What no row governs* list owed its third and
fourth entries, and they are `no` and `yes`.** Phase 2 predicted a third; the
prediction was about the depth marker, which phase 2 had already added. What
was actually missing is the floor's two answer words: they become a
vocabulary a checker matches literally the moment `FLOOR_NO` and `FLOOR_YES`
exist, and `test_the_exclusion_list_holds_every_string_a_checker_matches`
derives its expectation from the module's own constants. Seen red for exactly
those two parameters and green for `depth` and `Loses a record or crashes`,
which phases 1 and 2 had already listed. Writing the two words inline instead
of as constants would have passed the same case in silence — the derivation
only sees what a constant names.

**Mutation found two cases missing, one in each direction, and both were
invisible to the twenty-nine cases already written.**

- `DEPTH_RE` degraded to a bare `(\d+)` killed nothing. No fixture had a digit
  in a unit name, and `sha256_of` with no depth then reads as depth 256 —
  over the bound, so the loose pattern fails in the wrong direction as well as
  passing records it should refuse.
- `floor_answer`'s reason replaced by a constant killed nothing either. `yes`
  alone is caught by the equality arm before the reason is read, so the one
  cell that tells the two apart is `yes —` with a separator and nothing after
  it.

Twenty-one mutations in total, nineteen dead on the first pass and all three
survivors dead after those two cases were added. A third survivor was the
mutation's own fault rather than a gap: replacing the first `` `DEPTH_FROM` ``
in the document left three more, and a presence assertion is answered by any
of them.

**What phase 4 parses, stated exactly.** The failures, verbatim, since a
reviewer reads them and a changelog entry describes them:

```
`New units` lists `<entry>` without the depth it was added at. A fix pass may
add a unit; that unit's fix may not, and the row cannot show which of the two
this is without the depth. Write `unit (depth 1)`, entries separated by `;`

`New units` lists `<entry>` at depth 2 or above — a unit added by a fix
answering a finding INSIDE a unit an earlier round's fixes created. … It does
not go in this row: it is deferred with a named answerer, or becomes an issue

`Loses a record or crashes` is `no` and <N> round records follow this one. A
record that met the floor is followed by at most one more — the verifying
round, at the diff of the fixes that closed it. …
```

The units phase 4's ledger fragment can anchor on:
`skills/code-review/scripts/chain_check.py#floor_answer`,
`#depth_problems`, `#listed`, `#stopping_floor`, and the constants `FLOOR`,
`FLOOR_NO`, `FLOOR_YES`, `DEPTH_WORD`, `DEPTH_RE`, `DEPTH_MAX`, `FLOOR_FROM`
and `DEPTH_FROM`.

**The one check that was red on this branch for a reason that was not the
phase's is now green.**
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
failed through phases 1 and 2 while this work item's directory had no
`overview.md`. Commit `f01f394` added it, and the case passes; phases 1 and 2
both name it, so it is recorded here as closed rather than left for a third
segment to rediscover.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
