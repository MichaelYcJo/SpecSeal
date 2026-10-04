# 1791119073-a-pact-row-outside-the-config-table-is-refused — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | bcc2c6e3 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The vendored copy. `record_pact_changes`'s vendored branch matches its shape
over the reader's cut and `gfm_lines` together. S12, with its mutation, and
S13, red at the base. The comment above `NOTIFY_ROW_SHAPE` names the twin in
`hooks/config.py`. Keep the edit to the vendored arm: sibling E edits the
plugin path of the same function.

## What this phase found

**One line, in the vendored arm only.** The branch now matches
`NOTIFY_ROW_SHAPE` over `said.splitlines() + gfm_lines(said)`. The function
still makes one `.splitlines(` call, so its census row is unchanged, and the
plugin path E edits is untouched. `gfm_lines` is this file's own copy, so a
copy in a user's `tools/` still has it.

**A union is safe because the branch only widens.** A line seen on either cut
can only add a name to `named`, and the copy is blind only where both names
are there. So a row the reader's cut found before is still found, and one
only GFM's cut shows now joins it. Nothing the copy left before is
re-stamped now.

**The cases.** `test_a_vendored_copy_leaves_where_the_plugin_refuses_a_stray_notify`
runs S12 (a `| Pact notify | always |` under a blank line) and S13 (that row
cut at each of the eight characters only `str.splitlines` ends a line at).

**Seen red.** S13 failed for all eight characters against the unchanged
branch, which re-stamped at exit 0. S12 already passed there, as the frame
said, and three `mutation-check` breaks of the new line went red: M14
narrows the match to the table's own block (S12 red), M15 drops GFM's cut
(S13 red), and M16 drops the reader's cut (round 2 of PR #756's
line-separator case red). At `bcc2c6e3` the writer module, the census module
and the reader module pass, 339 cases.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
