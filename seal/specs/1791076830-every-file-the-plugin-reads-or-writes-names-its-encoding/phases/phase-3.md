# 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 29020e69 |
| Ran by | unknown — the spawn prompt did not name the agent and model, and the orchestrator that chose them is the one to fill this row |

## What this phase was asked

The records: the changelog fragment, the ledger fragment's new rows, and a
`Re-read ·` row for each released row the phase 1 and 2 edits drifted (M3),
each drifted row read before it is dated. `bin/evidence-check .` naming no
drift left unanswered and no broken anchor, and the text-hygiene modules over
the touched records, narrowly.

## What this phase found

**M3: 96 drifted coordinates on 74 released rows, none broken.** `bin/evidence-check .` at
`2c523396` named 94 distinct anchors in 25 release files: 92 code units, one
`.github/scripts/` or hook unit from phase 1 or a test unit from phase 2 each,
and two `CONTRIBUTING.md` heading paths moved by the House rules bullet. No
released row in `seal/ledger.md` drifted. The framer's upper bound, 136
anchors on the product files alone, was never approached because most units
those files hold were not edited.

**How each was read before it was dated.** Two readings, both executed. A
script parsed each code unit at `1ecb019f` and at HEAD, removed every
`encoding`, `text` and `errors` keyword from both, and compared the dumps:
92 of 92 equal, so no unit changed in anything but the encoding it reads or
writes. Then every claim cell citing a drifted anchor was printed and read
(77 rows matched by anchor text, 74 of them the rows the tool re-read): each
claims behaviour of its unit (a verdict, a reader's output, a refusal, a
document's rule), and none is about the bytes a file is read or written in.
The six `CONTRIBUTING.md` rows are about the fragment rule, the ledger
conflict rule and the fold's `--check`, and the edit added a bullet without
touching those. `bin/evidence-check --reverify --checked 2026-10-04 --into
<fragment> .` wrote 74 `Re-read ·` rows and left no released file edited.

**Five new rows, E1–E5**, for what this work claims: the walk and its
classification table, the entry-point half, the ASCII-console refusal, D7's
handlers, and the House rules bullet. Written with placeholder hashes and
stamped by the same `--reverify` run.

**E5 needed a pin that did not exist.** The House rules sentence is text a
contributor reads and acts on, and nothing held it, so
`test_the_rule_is_where_a_contributor_reads_it` was added: it asserts four
phrases, each changed once through `bin/mutation-check` and each red. A fifth
mutation, `enforces both` to `enforces it`, survived, because the case
asserts no word of that clause.

**The record checker reads phase records too.** `evidence-check`'s records
half refused the name of the constant phase 2 removed, which
`phases/phase-2.md`'s removals table quotes and the tree no longer has. The line now carries
` · NAME NOT IN TREE`, the checker's own exemption.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
