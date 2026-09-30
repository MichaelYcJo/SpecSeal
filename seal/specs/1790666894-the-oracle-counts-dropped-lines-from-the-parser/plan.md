# Implementation Plan: the oracle counts a paragraph's dropped lines from the parser (#677)

<!-- seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

The oracle stops reading container markers. Phase 1 takes the dropped-line
count from markdown-it-py's own `paragraph` and `lheading` rules, deletes the
hand-written helper, plants the round 3 report's shapes, and keeps every
record the deletion touches true in the same commit. Phase 2 plants the rest
of the class and the case over every character the strip drops, so the claim
that the class is closed is something a row can fail on.

## Technical context

Read at `cd56113c`, the branch's base, unless marked.

- `tests/commonmark_oracle.py#_recording_html_inline` and `#parser`: the
  wrapping pattern this reuses, and the place the two new `ruler.at` calls go.
- `tests/commonmark_oracle.py#_inline_html_lines`: the `while` loop that the
  parser-side count replaces, and the docstring's last paragraph.
- `tests/commonmark_oracle.py#_hidden_commonmark`: the one caller that passes
  `lines`.
- `tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_oracle_names_each_kind_it_hides`
  (the 13 marker rows that stay), `#FOUND`, `#test_where_the_walk_claims_to_be_exact_it_is`,
  `#test_the_walk_is_exact_somewhere` (its claim floor) and
  `#test_the_oracle_imports_the_parser_and_nothing_of_this_repositorys`.
- markdown-it-py 4.2.0, read in a uv cache copy of the pinned version:
  `rules_block/paragraph.py` and `lheading.py` (both end
  `state.getLines(startLine, nextLine, state.blkIndent, False).strip()`, and
  `lheading`'s inline `map` is `[startLine, nextLine]`, the underline
  excluded); `StateBlock.getLines` in `rules_block/state_block.py`;
  `parser_block.py`'s rule table (both rules with an empty `alt`); and
  `Ruler.at` in `ruler.py`, which replaces a rule's function and resets its
  `alt`.
- The round 3 report's paste-ready fix, `rounds/round-3-report.md` of H,
  §*Paste-ready fixes*. It is the starting point for the oracle half of
  phase 1. This plan changes three things in it: `lines` leaves
  `_inline_html_lines`' signature, the module docstring gets its sentence, and
  the report's rows go in a case of their own instead of the existing table.

**What breaks in six months.**

- **The parser moves.** A markdown-it-py that renames `rules_block.paragraph`
  or changes a block rule's signature fails at import or at `ruler.at`, which
  raises `KeyError` on an unknown name. That is loud, which is the direction
  to fail in. The quiet case is a version that pushes a paragraph's `inline`
  token some other way: the wrapper then records nothing, `meta` has no
  `dropped`, and the count reads 0. S1 to S4 are what catch that, because
  every one of them has a dropped line. The pin is what keeps it from
  happening unannounced.
- **A new block rule that joins several lines into one `inline` token**, from
  a plugin enabled later. It would need the same wrapper. The table in
  `spec.md` §*Why these two rules and no others* is the enumeration to redo.
- **Python's whitespace set grows.** S4 computes it, so a new character is
  tested without a row being added.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Keep the hand count and add a column count for `>` (the obvious fourth patch) | `10. >` followed by `    > b`: the `>` four columns in is a real marker there, so the count needs the item's content indent. Round 3 executed the parser's inline content as `'a\nb'` on that shape. The helper would have to rebuild the container stack, which is what three rounds did one marker at a time | rejected: S3m pins this shape, so a return to column counting goes red |
| Import a container rule from `hooks/` | `test_the_oracle_imports_the_parser_and_nothing_of_this_repositorys` forbids it, and the oracle would then agree with the walk by construction, which is the failure F's round 3 named | rejected |
| Count the dropped lines by comparing `inline.content` with each source line | The source lines still carry the markers, so the comparison has to strip them, which is the hand count again | rejected |
| Wrap only `paragraph` | A setext heading's text is joined and stripped the same way. The report executed the fix with `lheading` unwrapped: S2a alone fails | rejected: both rules |
| Refuse a multi-line `inline` token that carries no `dropped` key, instead of reading 0 | Stricter against the quiet case above, but it is one more rule about tokens written into the oracle, and S1 to S4 already turn red when the count reads 0 (the report's 16) | rejected: read 0, and let the rows be the guard |
| Keep `_inline_html_lines(inline, lines)` as the report's draft does | A parameter nothing reads tells the next reader the lines are read. That reading is what grew the helper | rejected: the parameter goes |
| Plant the report's four rows in `test_the_oracle_names_each_kind_it_hides`, as its draft does | That case's docstring says it shows what each of the four kinds is, one case each. It already holds 13 rows that are about the count, and S1 to S3 add 24 more. A case of its own gives the class one place, and its docstring can say why a row is there | rejected: a new case. The 13 existing rows stay, because moving them drifts two ledger rows and changes nothing that is checked |
| Narrow R1-1 to its two live anchors instead of removing it | The row would keep a claim about the helper's marker reading on code that no longer reads markers. H narrowed F's rows only where the claim still held | rejected: REMOVED |
| Leave S5 out of `FOUND` and rely on the oracle rows | The false red lives in the property, and `FOUND` is where the property meets a shape its seeded corpus does not reach. One document, so the claim floor moves by a handful of lines at most | rejected: S5 goes in. If the floor fails, it comes out and the phase record says so (Q3) |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The oracle takes the count from the parser (🟡 1 of H's round 3).** In `tests/commonmark_oracle.py`: `_recording_lines`, the two `ruler.at` lines in `parser`, the helper deleted, `_inline_html_lines(inline)` starting at `map[0]` plus `meta["dropped"]`, its docstring's last paragraph and the module docstring's sentence. In the test module: a new case holding S1 and S2, and S5 in `FOUND`. Records in the same commit: H's R1-1 REMOVED, H's P1-1 corrected and re-stamped, F's P1-2 re-read and re-stamped, a new row in this work item's fragment, and the marker on every line of H's records the records arm names | S1 and S5 red with the oracle from `cd56113c`; S2 red with `lheading` unwrapped; the whole new case red with the count forced to 0. Then `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q`, exit 0. `bin/evidence-check --ledger` on the three fragments, exit 0, and the records arm on the tree, exit 0 | cbfe84f8 |
| 2 | **The class, enumerated (§12).** S3's sixteen rows in phase 1's case, and S4's case over every character the strip drops, each character in the two shapes. `changelog.md`. The fragment's new row gains the S3 and S4 anchors, and whatever this phase drifted is re-read | Every S3 row and every S4 shape red with the count forced to 0; which S3 rows are also red with the oracle from `cd56113c` recorded in the phase record (Q2). Then the module again, exit 0, and `bin/evidence-check --ledger` on the three fragments, exit 0 | 128dda72 |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
**Re-read the column after any rebase**, or it names commits that resolve in
one clone and nowhere else.

**Why phase 1 carries the records.** Deleting the helper breaks R1-1's anchor
and makes H's records refuse in the records arm at that commit. A phase whose
commit leaves two checkers red does not stand on its own, so the records land
with the deletion. Phase 2 only adds rows, and its records are re-stamps.

## Operational impact

None to deploy. No migration, no environment variable, no new dependency: the
two new imports come from the markdown-it-py 4.2.0 the suite already pins,
and nothing a plugin user installs or runs changes. The one reader of the
change is a contributor whose property run used to report a false
disagreement on the shapes of S1, and now does not.
