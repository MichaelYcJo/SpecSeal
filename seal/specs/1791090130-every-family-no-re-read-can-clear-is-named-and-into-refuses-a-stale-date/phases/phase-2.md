# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 3793c934 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

⬜ 11 of #743's round 2: S4 and S5. Settle Q1 first by measurement. That
means every family × carrier × mode × narrowing, for the DRIFTED and BROKEN
gradings, plus the four candidates Q1 names. Then replace the
double-correction sentence of `docs/the-evidence-ledger.md` §*A released row
is read again in the branch's fragment* with a bold-led paragraph naming
every family found. Each family gets a case (A8–A10 and any further one),
each seen red under a mutation. Then the changelog fragment for both
findings, and the fragment rows for S4.

## What this phase found

**The enumeration (Q1), executed at `630c20cb`'s checker.** One probe built
each configuration in a fresh tree. It ran `--reverify` and then `--strict`
with the same narrowing, once with no `--ledger` and once with `--ledger` on
each file the tree holds. It did that in the three modes (no freeze, freeze
without `--into`, freeze with `--into --checked 2026-04-01`) and over both
placements where a member can be folded or sit in a fragment. A cell is *in
the class* where `--reverify` exits 0 and that `--strict` exits non-zero.
354 cells were run, 336 of them distinct. The BROKEN configurations ran in
two passes: once with the unit renamed, which `--reverify` follows to its new
name, and once with it deleted. The only-a-re-read tree deletes its unit in
both passes, so its 18 cells ran twice. The
probe files were deleted after the run (contract §7).

| Configuration | Cells | In the class | Where |
|---|---|---|---|
| a released row corrected by two `Corrected ·` rows (both in fragments, both folded, one of each) | 48 | 36 | every mode, every narrowing but R's file alone, where `--strict` exits 0 too |
| a BROKEN unit, deleted: a released row outside every family | 12 | 4 | without the freeze; under it the row is named, exit 1 |
| a BROKEN unit, deleted: a fragment row outside every family | 12 | 12 | every mode |
| a BROKEN unit, deleted: the root and a re-read both carry it | 18 | 6 | without the freeze; under it exit 1 |
| a BROKEN unit, deleted: only a re-read carries it | 18 | 8 | the re-read in a fragment, every mode; folded, without the freeze only |
| a family rooted in a fragment, its anchored statement gone | 18 | 6 | the `Corrected ·` row in a fragment, every mode; folded, it is a released root and exits 1 |
| a family rooted in a fragment, its unit gone (BROKEN) | 18 | 8 | as the BROKEN rows: fragment every mode, folded without the freeze |
| a family rooted in a fragment, its unit drifted | 18 | 0 | the in-place re-stamp clears it |
| a citation whose released line changed (R's Notes edited) | 18 | 4 | the citing row folded, under the freeze |
| the unit renamed, a released row or a fragment row outside every family | 24 | 0 | `--reverify` re-anchors the row to the new name |
| the unit renamed under R and a fragment re-read | 18 | 1 | no freeze, no `--ledger`: the run re-stamps R in place, which moves the line M cites |
| a `Re-read ·` row with no marker in its Notes | 18 | 12 | every mode, narrowed to the row's file or not |
| a `Re-read ·` row whose citation names a fragment row | 18 | 12 | every mode, narrowed to the row's file or not |
| a coordinate every reading dates with no calendar date | 18 | 0 | — |
| a superseded root, narrowed to each file | 60 | 0 | — |

**Q1's answer: five things, where the frame read three.** The frame's three
hold as `spec.md` §*The class* read them. Three more appear. A citing row
refused `MALFORMED` exits 0. A citation whose released line changed exits 0
under the freeze. And without the freeze a run can create that citation
drift itself. `released_drift`'s BROKEN list is the only place `--reverify`
answers a BROKEN coordinate, and only for a released carrier under the
freeze, so a BROKEN unit is one family whatever row holds it. The paragraph
names it that way rather than as *a BROKEN anchor in a family*. The spec's
*Out* table kept row-shape refusals out *unless phase 2's enumeration shows
one of them inside a family exiting 0*. The marker refusal is inside a
family, and it is named.

**The unfrozen re-stamp moves a line a citation reads.** Without the freeze,
take a released row R and a fragment `Re-read ·` M of it, both recording a
unit at its old hash. One `--reverify` over every ledger re-stamps both. R's
own line changes, M's citation of R was read before that, and `--strict`
then reads M's citation DRIFTED, *the released file changed under the row it
cites*. A second run re-stamps it. M folded, or either file narrowed alone,
does not show it. This is a defect in the unfrozen writer, and this
repository runs frozen. The spec keeps exit changes out of this work, so the
paragraph names it and a case pins *exit 0, then clean on the second run*.
The orchestrator owns whether it becomes an issue (`overview.md`, Not done).

**Q4's shape repeats here.** Each family is one parametrized case over the
modes and the narrowing, between 2 and 24 cells. The existing
`test_a_released_row_corrected_by_two_rows_names_both` and
`test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read` were left as
they stood. The spec offered *extend or a sibling*, and the siblings carry
the axes without rewriting what those two pin.

**The headline was reworded after the cases landed.** It said *Five things
no re-read clears*, which the unfrozen citation drift contradicts: a second
run clears that one. It now names the exits, and its pin, the changelog and
F3 followed in `3793c934`.

**`survivor-check --range e1e54c71..HEAD`** reported one place, this item's
own `spec.md` quoting the replaced sentence as the one the work changes. It
is recorded in `survivors.md`, and the check exits 0 with it.

**Mutations, each red:** the double-correction notice (`if len(keys) < 2`)
for A8 (18 cells), `released_drift`'s released BROKEN append for A9 (4 of
24, the released-row carrier under the freeze), the fragment-root guard for
A10 (6 of 12, the fragment placement), the marker refusal and, separately,
the fragment-citation refusal for the `MALFORMED` case (6 of 12 each), and
`cited_row`'s hash compare for both citation cases (5). Each of the seven
pinned sentences went red with its words deleted.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence *A row corrected by two rows is not a re-read's to clear: …* closing the *Without the row* paragraph | its first bullet, in the bold-led paragraph that follows it in the same section |
