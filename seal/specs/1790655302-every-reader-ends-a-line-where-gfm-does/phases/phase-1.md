# 1790655302-every-reader-ends-a-line-where-gfm-does — phase 1

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | eb6cfa61 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 1 of milestone 49's item G, the rest of #664, from
branch `fix/664-every-reader-ends-a-line-where-gfm-does` cut at `2e392d46`.
The splitter moves into the shared reader: `unverified_check.py` gains
`GFM_LINE_RE` and `gfm_lines`, and `readable` and `folded_items` read it. In
the same commit every `round_record.py` pair and `fold_check.py`'s marker
readers split with it, because coupled readers move together and
`round_record#swallowed` zips with `strict=True`. `fold_check.py#gfm_lines`
is retired. `reader_blanking_passes` learns the splitter by name, S17
replaces the old copy check, and the docstrings that describe a split are
corrected. Work item F's files (#672) stay untouched. Verified by S1–S4, S17
and S18 red at base, the readers' modules, and S20 for `unverified-check`,
`fold-check` and `chain-check`.

## What this phase found

- **The frame holds.** Re-enumerating every `.splitlines(` in shipped code
  by `ast` at `b1ae8b65` reproduces spec §*The class, enumerated* call for
  call, with one count off: `hooks/config.py` makes two calls, not three.
  `#unfenced` names `text.splitlines()` in its docstring only. It is F's
  file either way, and `overview.md` records it as a divergence.
- **The frame's own spec was a refused record.** At `b1ae8b65`
  `evidence-check .` read four work items and exited 0. Once this phase had
  written the item's records, it read five and exited 2: spec.md's *Out*
  table names `hooks/blocks.py#walk_text` · NAME NOT IN TREE, which exists
  on F's branch and not here. The line now carries `· NAME NOT IN TREE`, the convention the
  records reader asks for, and nothing else in it changed.
- **S20 on this tree is a one-file question.** Over every tracked file at
  `2e392d46`, `gfm_lines(text) == text.splitlines()` fails in exactly one,
  `seal/specs/1790635414-…/rounds/round-1-report.md` (spec M1, executed
  again here). So a moved reader's output can change only where it reads
  that report. `fold-check` and `chain-check` printed the same bytes before
  and after. `unverified-check` printed one more overview and one more open
  row, which is this item's own `overview.md` and not a moved reading.
- **Every new case was red at base on its real assertion.** Taken on a
  `git archive` of `2e392d46` in the scratch directory, with this branch's
  test files copied in: the record case on the quoted line arriving as two
  lines, the fix-row case on grounds cut at the separator, the marker cases
  on `{'1700000000-a'} == set()` for each of the eight, the agreement case
  on `markers` counting 1. The splitter cases were red on the missing
  function, which is the absence they pin.
- **`readable` reverted alone is caught three ways.** The record case goes
  red because `swallowed`'s `strict=True` zip raises, the fix-row case goes
  red on the cut row, and the tie in `tests/test_chain_hooks.py` refuses the
  attribute call. The pin now refuses every attribute call rather than
  allowing `splitlines`, so going back to it is not silent.
- **Two arm cases need bytecode.** `tests/test_arm_check.py`'s two
  bytecode-cache cases fail under `PYTHONDONTWRITEBYTECODE=1` because they
  need a real `.pyc` to exist. They pass without it. The variable is for
  mutation runs only.
- **The first module run found this item's missing overview.**
  `test_every_spec_directory_that_reached_the_ladder_has_an_overview` is
  what opened `overview.md` at the first divergence.
- **Ledger.** 44 rows drifted, in `seal/releases/0.8.1` to `0.15.3` and in
  item C's fragment, each re-read against the edit and re-stamped with a
  dated note. None of their claims was about where a line ends except C's
  H2, whose anchors `fold_check.py#gfm_lines` and the copy check this phase
  removed. H2 is removed there and rewritten as G3 in this item's fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/settle/scripts/fold_check.py#gfm_lines` and `#GFM_LINE_RE` | `skills/verify/scripts/unverified_check.py#gfm_lines`, which `fold_check.py` loads |
| `tests/test_a_document_has_room_for_the_next_fold.py#test_the_copy_of_the_line_rule_is_the_checkers` · NAME NOT IN TREE | `tests/test_every_reader_ends_a_line_where_gfm_does.py#test_every_copy_of_the_splitter_is_the_readers` (S17) |
| H2 of `seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md` | G3 of `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md` |
