# 1790655302-every-reader-ends-a-line-where-gfm-does — phase 2

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | cbbac755 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 2: the changelog readers.
`gather_changelog.py#live_markers`, `#leaves_open`, `#section_lines`,
`#insert` and `#main` read the shared reader's `gfm_lines`, and `#insert`
takes a section's index on the same line list it indexes.
`survivor_check.py#gathered_fragments`, `#segments` and
`#removed_ledger_rows` move with them, since the sweep and the gatherer read
one marker. `#live_markers`' docstring names the shared rule. Verified by
S5–S8 red at base, the gatherer's and the sweep's modules, and S20 for
`gather_changelog.py --check` and `survivor-check`.

## What this phase found

- **The spec's S5 and S8 needed a second look to be red.** S5 as written
  is red at base, but the index it exercises is the same number on every
  file `main` can read: `open()` translates a lone CR, and with no CR
  counting LF and counting `gfm_lines` agree. The mutant that puts the LF
  count back stayed green until `test_the_sections_index_is_counted_on_the_list_it_indexes`
  handed `insert` a lone CR directly. S8 as the spec words it (a row with a
  U+2028 in its notes, unchanged at both ends) is not red at base, because
  both halves of a row cut the same way at both ends compare equal. The
  case that is red is a row with no id whose still-resolving anchor stands
  after the separator, corrected in place: cut, the row lost that anchor,
  and the correction read as a removal. The anchor stands after the
  separator at both ends, so each end's split is caught by its own mutant.
- **The spec's S6 is red on both sides at base**, not only the sweep's.
  The case asserts the sweep first so the red it shows is the one the spec
  named.
- **`segments` needed the reader loaded once.** It runs once per corpus
  file, 504 on this tree, and `survivor_check.py#reader` executed the module
  on every call. It now caches by path, so a `READER` that moves is still
  refused, and a case holds both halves.
- **Four more readers than S5–S8 name.** `leaves_open`, `section_lines`,
  the fresh-section arm of `insert` and the dry-run print each got a case,
  each red at base, because a moved call no case notices is a move nobody
  can check. `main`'s heading line is the one equivalent mutant left: it
  is `section`'s own `## <version> — <date>`.
- **S20.** `gather_changelog.py --check` printed the same bytes before and
  after. `survivor-check --range 2e392d46..b1ae8b65` printed the same bytes
  too.
- **Ledger.** 11 rows drifted and each claim held; each is re-read with a
  dated note. G5 and G6 are this phase's rows.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
