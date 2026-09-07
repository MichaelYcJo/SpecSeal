# 1788789330-the-update-notice-names-the-expensive-move — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | <filled at the commit that closes this phase> |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

The records this repository's conventions require, as fragments rather than
shared files: the changelog entry at
`seal/specs/1788789330-the-update-notice-names-the-expensive-move/changelog.md`
and the ledger rows at
`seal/ledger/1788789330-the-update-notice-names-the-expensive-move.md`, with
coordinates in `path#major@hash` form and no line numbers. Plus the tracker
box at `docs/flow.md:74`.

## What this phase found

**`seal/ledger/` did not exist in this worktree, so this work item is the
first of the release to write a fragment.** Nothing about that needed a
decision — the checker reads the `seal/ledger/*.md` glob and found the
directory the moment it held a file — but it is worth the line, because the
`fold_ledger.py --check` arm on a release pull request now has something to
gather for 0.9.1 where it had nothing before.

**The hashes were produced, not typed.** The fragment was written with
`@00000000` in all eight coordinates and `bin/evidence-check . --reverify`
rewrote each to what its anchor actually holds, printing the eight
substitutions. Then the plain check resolved 772 rows across the gathered file
and the fragment, 0 drifted and 0 broken. A hash a session invents is a hash
nothing checked; this is the two-step that keeps a session from writing one.

**A markdown anchor is a quoted heading and it survived the paragraph split.**
`README.md#"### Updating"` and `README.ko.md#"### 업데이트"` both resolve after
phase 3 broke one paragraph into two under those headings — which is the
property the notation is for. The row's hash moved and its anchor did not,
where a line number would have moved for every edit above it in the file.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The unticked box at `docs/flow.md:74` | ticked in place. Its text is left alone: it describes the ticket as filed, and `spec.md`'s enumeration row 18 records that decision |
