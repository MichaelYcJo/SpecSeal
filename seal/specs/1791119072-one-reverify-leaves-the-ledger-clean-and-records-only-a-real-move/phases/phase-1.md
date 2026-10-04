# 1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 1dea315c |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#774. S1 (both arms), S2 and S3, each seen red at the base. Then D1 at the
four append sites of `reverify_into`: a recorded move's old hash is the
coordinate's newest reading's hash. Then the guard in `record_pact_changes`
that drops a part whose two hashes agree. Then one sentence in
`docs/the-pact.md` §*A signatory records a pact change* saying which hash a
recorded move starts from, pinned through
`test_the_documents_say_what_the_writer_does`, and the paragraph's
`Enforced by:` line gaining the two #746 cases and S1's case (D6). Keep the
edits to `record_pact_changes` to where `parts` is built, because sibling F
(#759) edits the same function.

## What this phase found

**The frame holds.** Every coordinate the plan names was where it said at
`fc4e56d3`: the four `m.group("hash")` sites, `family_view`'s `newest`, and
`parts = list(dict.fromkeys(coords))`. P3's hashes came back exactly: S1
recorded `serialize@57f678c6 → @57f678c6` at the base in both arms, and S3
recorded `serialize@57f678c6 BROKEN`, where the newest reading holds
`7069baf7`.

**The fourth site is fixed where its hash is chosen, in `released_drift`.**
The plan names the `for at, coord, detail, key, recorded in broken` loop in
`reverify_into`. That loop's `key` is the family member `released_drift`
picked, not the family's root, and only the root keys `view.newest`. The
hash is therefore set in `released_drift`'s family arm, where `top` is in
hand, and the loop is unchanged. `released_drift`'s docstring says which
hash the BROKEN list carries now. Its only other caller, `main`'s unfrozen
arm, discards the BROKEN list.

**The minor-anchor miss the plan's alternatives table guards against cannot
happen.** `view.readings` is keyed by `coordinate_of`, which keeps the minor
anchor, so the newest reading of a coordinate always carries that coordinate
in the same spelling. The lookup (`newest_hash`) falls back to the member's
own hash only for a row outside every family, which is its own newest
reading. No divergence row was needed.

**The guard's `continue` is observable only where an owed row is LEFT.** The
first mutation plan showed removing `if not parts: continue` survived S2:
in the plugin's own arm an entry with no parts already records nothing,
because the `fresh` filter leaves it empty. The `continue` matters in the
two arms that leave a row without recording it, a copy with no `hooks/` and
a `Pact` row that will not read, where a row whose only part moved nothing
used to print `LEFT` and exit 1. `test_a_row_whose_parts_all_agree_is_not_left_either`
holds both. The `new is None` arm of `reverify_into` had no case either, so
`test_a_coordinate_left_under_a_newer_reading_names_the_newest_hash` holds it
with a minor anchor whose statement is gone.

**Every unit was mutated once through `bin/mutation-check`, and each went
red**: `newest_hash`'s family lookup, the BROKEN site in `released_drift`,
the refusal arm, the `new is None` arm, the written arm, the guard's filter,
the guard's `continue` (after the case above), and the pact sentence's pin.
The pin's first run selected no case: `-k` does not match a parametrised id
holding spaces, so it was re-run with the test function's name.

**Run at the phase boundary, executed:** `bin/test
tests/test_a_signatory_records_a_pact_change.py
tests/test_a_released_row_is_read_again_in_a_fragment.py
tests/test_a_folded_statement_names_what_enforces_it.py -q`, 478 passed at
`1dea315c`; `uvx ruff check` and `uvx ruff format --check` on the touched
`.py` files. The suite as a whole is `unverified`, answerer the sealer.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
