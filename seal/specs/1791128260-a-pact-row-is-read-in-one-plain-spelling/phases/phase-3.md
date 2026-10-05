# 1791128260-a-pact-row-is-read-in-one-plain-spelling — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 829cc442 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The vendored copy. `PACT_WORD` and the predicate in `evidence_check.py`
replace `NOTIFY_ROW_SHAPE`, sharing the plugin's pattern and predicate (S10
holds them equal). The vendored branch of `record_pact_changes` reads
`gfm_lines` and is blind where the file will not read, where some line naming
a pact with a `|` is neither a plain `| Pact | … |` nor a plain
`| Pact notify | … |` row, or where a plain row of each carries a value
(`spec.md` Scope 2). Every base vendored case keeps its verdict. S9 and S10.
Sibling E (PR #786) edits `record_pact_changes`' docstring and its plugin
path, so this phase keeps to the vendored branch.

## What this phase found

**The decision is a unit of its own, `notify_may_be_always(said)`.** The
vendored branch of `record_pact_changes` now calls it in one line where it
built a set from `NOTIFY_ROW_SHAPE`. That keeps the branch's diff to three
lines beside sibling E's edits of the same function, and it lets S9 run the
whole S2 corpus through the vendored decision in-process: 1,751 texts in one
case, where running each through a subprocess and a scratch repository would
cost minutes. Twenty-five of them run end to end as well.

**"Judges each line by the line's own shape" needed one more condition.**
`CONFIG_ROW_RE` takes `\s` as Python reads it, so a `| Pact | <U+2028>URL |`
line matches it as a plain `Pact` row, while the plugin's reader sees one GFM
line the walk never took and refuses it. The copy reads a line by its row
shape only where `line.splitlines() == [line]`, as the reader reads a walked
row only where the GFM line is one piece. The first `mutation-check` of that
guard survived (V5 below): every case then planted had a `Pact` value beside
it, where the guard changes nothing. `829cc442` adds the case that holds it,
a cut `Pact` row with no notify row anywhere, at each of the eight
characters, seen red by that break.

**Where the copy and the plugin still differ, nothing can mean `always`.**
With no walk, a plain row anywhere counts as plain: a plain `Pact` row below
the table with no notify row re-stamps here and is refused by the plugin. No
line names a notify value, so no row citing no clause can be owed, and the
docstring says so.

**Every base vendored case keeps its verdict.** The eleven vendored cases on
the base (five that leave, four that re-stamp, two that will not read) pass
unchanged at `5efdea16`, against both the base's `evidence_check.py` and
this one. The census row moved from `record_pact_changes` to
`notify_may_be_always`, still one call.

**`NOTIFY_ROW_SHAPE` leaves the file**, so the released anchor 0.18.1 C1
cites goes BROKEN. Phase 4 writes the `Corrected ·` row.

**Seen red (§15).** Against `94d7b2e0`'s `evidence_check.py`, 23 of the 25
new end-to-end S9 cases fail on exit 0 and a re-stamp. The two that pass
there, a plain notify row below the table and one in a closed fence, are
lines the old shape already found; the in-process S9 and S10 cases fail on
the missing names. Each new unit was then broken with `mutation-check`, and
all ten breaks went red after `829cc442`:

| Break | Cases run | Red |
|---|---|---|
| V1 the copy's `PACT_WORD` without its look-behind | S10 | 1 |
| V2 the copy's decoded line not searched | S10 | 1 |
| V3 the copy's pipe condition off | S10 | 1 |
| V4 a plain row of each never blind | vendored | 6 |
| V5 a cut line read by its row shape | S9 | 8 (survived before `829cc442`) |
| V6 an empty value counted | vendored | 1 |
| V7 a shaped item that names a pact not read | S9 | 1 |
| V8 a file that will not read not blind | vendored | 2 |
| V9 the plain notify item not plain | vendored | 2 |
| V10 a line off the row shape not read | S9 end to end | 9 |

The four pact modules and the census passed at `829cc442`, 2,152 cases.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `evidence_check.py#NOTIFY_ROW_SHAPE` | `evidence_check.py#PACT_WORD` and `#names_a_pact`, the plugin's copies; a `Corrected ·` row in `seal/ledger/1791128260-a-pact-row-is-read-in-one-plain-spelling.md` re-points 0.18.1 C1 (phase 4) |
| The census row `(evidence_check.py, record_pact_changes)` | `(evidence_check.py, notify_may_be_always)` in the same table |
