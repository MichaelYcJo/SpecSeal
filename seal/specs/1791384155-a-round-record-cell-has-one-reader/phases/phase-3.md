# 1791384155-a-round-record-cell-has-one-reader — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | ae628547 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

J3 of `spec.md`: `depth_two` reads through `path_forms`; the wide `Location`
reader and its five patterns leave; `depth_two`'s docstring and
`docs/round-record-spec.md` §*The depth in `New units`* by replacement; the
docstring in `tests/test_a_fix_of_a_fix_is_counted.py` that named the wide
reader. Verified by S5's bare-name case red against the depth walk as it
stood, S6, and the two modules green.

## What this phase found

- `landings` still called the wide reader with `paths_only=True`, which
  only forwarded to `path_forms`. It calls `path_forms` directly now, so no
  flag survives the reader it chose between.
- The existing depth-2 case was parametrized over ten shapes; four of them
  carry no path (`` `helper` ``, `` `helper()` ``, `helper`, and a `#helper`
  standing apart from its path) and are depth 1 now. They moved to a case of
  their own, which is S5's bare-name case: run against an archive of
  6b20dd77 with the new test file, all four fail, because the old walk
  refused each.
- `docs/round-record-spec.md` §*The depth in `New units`* carried no sentence
  about a name with no file; the sentence that says `close` keys its refusal
  on the `Location` now says the cell is read as §*A fix of a fix* reads it.
  The document stays at 998 lines.
- `skills/evidence-check/scripts/evidence_check.py` had a comment naming one
  of the five patterns as a second reader of the same shape; it was false
  after the edit and says what is true now.
- One released row, A8 of 0.19.0, rested on the wide reader as a coordinate,
  which `evidence-check` reports broken once the unit leaves. Its claim still
  holds, so it is a `Corrected ·` row with that coordinate retired. #860's
  fragment row `Corrected · A1` named the wide reader in its claim; it was
  corrected in place, with a note saying by whom.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the wide `Location` reader in `round_record.py` and its five patterns (the unit, line, fragment, identifier and bare-identifier patterns) | `path_forms`, the one reader, for both walks |
| the depth walk's branch that resolved a path-less name against every file the range touched | nowhere: a name with no path places nothing (`spec.md` J3) |
| the four name-only shapes of the depth-2 refusal case | `test_a_finding_located_by_a_name_with_no_path_places_nothing` |
