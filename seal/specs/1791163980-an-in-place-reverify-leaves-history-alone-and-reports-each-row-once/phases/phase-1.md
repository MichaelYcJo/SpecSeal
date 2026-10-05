# 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 5d2282bd |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#785 (D1). First S1 (with S6 as a parameter), S2 (narrowed and not), S3, S4
and S7, each seen red at the base `a3aa139a`, and S5 seen red under the
mutation *leave every family member alone*. Then the pre-walk family judgment
in `reverify`: a code coordinate is left alone where `view.held[root][coord]`
is non-empty or where the member's family is in `view.superseded`, with the
view built over every ledger the repository carries. Then D1's sentence in
`reverify`'s docstring, the usage text, `skills/evidence-check/SKILL.md`
§*Re-verifying is recomputing the hash* and `docs/the-evidence-ledger.md`
§*A released row is read again*, each pinned and seen red with the sentence
deleted. `docs/the-pact.md` §*A signatory records a pact change* re-read, and
edited only if a sentence there became false.

## What this phase found

**The frame does not hold in one place: a row the run dates.** Spec D1 says
a left-alone coordinate keeps its hash, and *a row with other coordinates the
run does re-stamp is dated as today, once*. Built that way, the date makes the
row the family's newest reading of every coordinate on it, the left-alone one
included, and that coordinate then reads DRIFTED against the hash an outranked
reading recorded. The tree: B holds `handler`, and A, older, carries
`handler` at an outranked hash beside `other`, which drifted with no reading
holding it. The run re-stamps A's `other`, dates A `2026-04-01`, and
`--strict` reads A's `handler` as the newest reading, not holding: exit 2,
where the base's run exits 0. So a held coordinate is deferred, and it rides
its row only where the run dates that row for another move: its hash is
re-stamped with the row, and its move is handed to MOVES. Without
`--checked`, or on a row the run leaves whole, it stays. The date says the
whole row was read, so this claims no reading the `--checked` paragraph does
not already assert. The case is
`test_a_held_coordinate_on_a_row_the_run_dates_is_re_stamped_with_it`, green
at the base and red under the spec-literal build (the riders mutation below).
Recorded in `overview.md`'s divergence table.

**A held coordinate that does not resolve is left too.** `handler` can name
two places, one holding B's hash: the family holds it, and A's older hash
matches neither place. The base left A with a `left` line and handed MOVES a
BROKEN part. A reading the family holds is history whether it resolves or
not, so `reverify` checks `current_hash` for a held coordinate and leaves it
silently where that is None. Held by
`test_a_held_coordinate_with_two_places_is_left_alone`, red at the base.

**The superseded skip is for code coordinates only.** A `Re-read ·` row in a
superseded family still has its citation checked by `family_view`, so its
citation is still re-stamped. Held by
`test_a_superseded_familys_citation_is_still_re_stamped`, green at the base
and red with a citation judged as a code coordinate.

**The view shares `reverify`'s scan cache.** `family_view` and the rename
scan both key it by repository and read code, which no walk writes.

**`docs/the-pact.md` §*A signatory records a pact change* stays true.** It
records a pact change when the run moves a row's hash or leaves a coordinate
BROKEN. A left-alone coordinate does neither, so no sentence there became
false, and it is not edited.

**Seen red.** At the base, before the code: S1 dated and undated, S2 both
narrowings, S3, S4, S7 and the two-place case. S5 and the dated-row case were
green there, as they should be. The six document pins were red with the base's
three files swapped in. Every unit was then mutated once through
`bin/mutation-check`, and each went red: the superseded branch of
`left_alone` turned off (S4) and turned on for every family (S5), the
`holding` test (S1), the riders joining a dated row (the dated-row case), the
MOVES filter for deferred moves (S7), the citation guard (the superseded
citation case), the resolution guard (the two-place case), and the view
narrowed to LEDGERS (S2 narrowed).

**What phase 2 needs.** A left-alone coordinate produces no outcome at all, so
it has no `left` line and is no reason (ii). A held coordinate deferred on a
row that is not dated resolves, so it is never left either.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `reverify`'s docstring opening *Rewrite the hash of every row whose anchor resolves.* | The same docstring, now naming where a re-read is owed, and its new `left_alone` paragraph |
