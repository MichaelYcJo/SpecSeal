# 1790154761-folded-statements-pile-into-one-spec — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e491b63e |
| Ran by | unknown — the spawn prompt named no value, and a segment does not source this row from its own idea of what it is |

## What this phase was asked

Write `tests/test_both_editions_carry_the_same_folds.py` and see it red at the
base first (the spec's figure: 10 ids against 0). Then translate the missing
§*What the repository decides for itself, and how it is read* into
`docs/one-root-by-lifetime.ko.md` with its markers, place the other five
markers at their matching headings, and widen `CONTRIBUTING.md`'s README rule
to every `.ko.md` edition.

## What this phase found

- **The base went red on the heading levels, not on the ids.** The English
  edition has one more heading, so the level sequences differ (23 positions
  against 22, preamble included) and the check stops there. It compares ids
  per position only once the outlines agree. The spec's "10 ids against 0"
  appeared at the second step: with the Korean heading added and no markers
  yet, the test named the missing ids position by position. Both reds were
  executed before any marker was written.
- **Where the markers went (Q5, the work's).** Each marker sits above the
  Korean paragraph that carries the same statement. For the five on shared
  sections it is directly under the heading, as in the English edition. The
  two stacked markers under §*Shared or local* stay stacked.
- **A code span must not wrap across lines in these documents.** The first
  draft split `` `Commit and pull request language` `` over two lines. A
  backtick run with no partner on its own line is the case `live_lines` reads
  both ways, so it could park the lines after it. The span was rewrapped onto
  one line before any check ran. Nothing measured a failure; the rewrap
  avoids the ambiguous case.
- **`CONTRIBUTING.md`'s rule sentence is pinned in the new module**
  (`test_the_contribution_guide_owns_the_rule_and_names_this_check`), shown
  red with the file restored to `HEAD`. The phrase `both READMEs move
  together` elsewhere is a hygiene workflow step name, and this phase did not
  touch it.
- Mutations executed, one at a time, each restored from a copy kept outside
  the tree: a Korean marker moved to another section, the per-position
  comparison disabled, the level comparison disabled, and the heading pattern
  without its space. Each turned at least one case red.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
