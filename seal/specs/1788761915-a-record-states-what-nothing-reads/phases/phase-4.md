# 1788761915-a-record-states-what-nothing-reads — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `1b1a1c8` |
| Ran by | unknown — the spawning session named no model in the prompt, and the row is the orchestrator's to fill |

## What this phase was asked

The stamp arm: a record naming `path#unit@hash` is resolved the way a ledger
anchor is. Verified by a case over a fixture whose unit was edited, and the
tree's one real stamp green.

## What this phase found

**"Resolved the way a ledger anchor is" is a refactor, not a second reader.**
`check_ledger`'s anchor loop is 160 lines of graded resolution — the
resurrection rule, the repo-wide rename scan, the minor-anchor widening — and
a records arm with its own copy would be two rules the first time either is
edited. The loop is now `check_text`, and `check_ledger` is that call plus
`old_format_rows`. The records arm calls `check_text` on one line at a time.

**Two things must not carry across, and both were found by writing a case.**
`old_format_rows` refuses `path:line` and tells the author to run the
migrator, which is right for a ledger row and wrong for a record: a verdict
table's `Location` column is `path:line` by design, prescribed by
`templates/sdd-round.md`. The alternative design — `check_ledger` over the
whole record file — was run as a mutation and turns five cases red, that one
included.

The second is the grading. **Drift in a record is exit 1 the way drift in a
ledger is; a name or an anchor that does not resolve is exit 2.** A live work
item's branch is editing the very units its records stamp, so failing on
drift is red by construction — the state `.github/workflows/test.yml`'s
`ledger` job already refuses in its own comment, and a check that is always
red gets ignored.

**The line, not the file, and that is why the arm reads line by line.** The
identifier arm names `file:line:name`; a stamp refusal naming only the file
would send a reader through a record hunting for which of its anchors moved.
A fresh `seen` per line follows from that — two lines stamping one unit are
two claims — and the repo-wide scan cache is shared across them so the scan a
broken anchor triggers is paid once.

**The acceptance row's *the tree's one real stamp stays green* is not what
the tree holds, and the boundary is what makes it not matter.** Measured over
this tree: `skills/code-review/scripts/chain_check.py#main@fd1525ae` in <!-- NAME NOT IN TREE: a stamp quoted as another record's, measured at a moment -->
`1788326734`'s `overview.md` reads DRIFTED, the `"## Comparison axes"` stamp
in `1788272986`'s `round-2.md` reads DRIFTED, and the fixture stamp in
`1788597030`'s `round-1.md` reads BROKEN. All three sit in work items that
have shipped, so the arm never opens them. There are no stamps at all in the
two unreleased work items — `0 stamps read` — which means the arm's proof on
this tree is its cases and its mutations rather than a live occurrence.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `check_ledger`'s anchor loop | `check_text`, which `check_ledger` now calls — and `tests/test_a_row_points_by_content.py`'s resurrection-flag guard, whose consumer list moved with it |
