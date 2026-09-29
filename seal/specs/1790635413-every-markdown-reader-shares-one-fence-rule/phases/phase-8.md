# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 8

| Field | Value |
|---|---|
| Phase | 8 |
| Commit | 7c47eec8 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 8, added after round 1 at the owner's request: fix #658 in
this branch rather than file it. The readers with no fence state at all —
`hooks/routing.py#table_rows`, the `--exempt` reader in `survivor_check.py`,
and the fence toggles in `tests/test_docs_line_wrap.py` and
`tests/test_handoff_outlives_the_merge.py` — each skip fenced lines, with the
hook keeping phase 6's copy-and-parity-test shape. Each reader gets a fenced
row that reads as live seen red at `08d4aec3`, `bin/test` over its modules and
the parity test, one killed mutant per changed unit, ledger fragment rows, a
changelog entry naming #658, and any drifted row re-read in place.
`hooks/routing.py` is this phase's; D (#28) edits `hooks/cmdline.py`,
`hooks/dispatch.py` and the commit gate in parallel.

## What this phase found

- **Half of this phase was reverted after round 3, at the owner's
  decision.** `hooks/routing.py` is byte for byte `release/v0.16.0`'s again:
  its fence copy, round 2's comment walk, their cases in
  `tests/test_routing_is_recorded.py`, the routing parity shapes and ledger
  rows are gone, and `table_rows` keeps no fence state, as it did before.
  The reason is round 3's 🟡 1 and ⬜ 3: the routing walk had taken on the
  config reader's comment-before-fence order, and that order reopened a
  finding every round. #658 stays open for the routing half, and a new work
  item redoes it. What stays is the exemption half and the two test walks:
  `survivor_check.py#read_exemptions` (with round 2's 🟡 3 fix, which reads
  it through `readable`), `tests/test_docs_line_wrap.py#fenced_numbers` and
  `tests/test_handoff_outlives_the_merge.py#fenced_block_lines`. The first
  two bullets below describe reverted code.
- **`routing.py` keeps a copy, not an import.** Importing `hooks/config.py`'s
  held copy would have been one copy fewer. It would also have added an
  import edge to the commit gate's hook while D changes what a hook's load
  failure does, and the plan names the copy. `fenced` is held to the shared
  rule over the same nineteen shapes as `config.py`'s copy.
- **The routing defect was sharper than #658 put it.** `parse` keeps the
  LAST row of each label, so a fenced example BELOW the real table did not
  merely add a row. It answered for the declaration: the case reads a
  declared review chain as *straight to the PR* with another branch.
- **The exemption reader hides a fence nobody closed, where the ledger
  readers read it.** An exemption excuses a survivor, which is the silent
  direction, so reading less is the loud one. `blank_fences` is the rule, and
  a file whose only rows are fenced is refused as holding none.
- **The strict shared opener turned the real-tree line-wrap case red.**
  `skills/implement/orchestration.md` fences a 155-column command five spaces
  deep under a list item. The shared rule has no block model and reads that
  line as prose. Both test walks therefore ask the shared delimiters with a
  line's indentation stripped first, which is the wider opener
  `round_record.py#fenced_after` keeps for the same reason, and
  `fence_opener`'s docstring now lists them there.
- **No committed file reads differently.** A probe compared `08d4aec3`'s
  readers with this phase's over the 25 `routing.md` and 15 `survivors.md`
  files in the tree: 0 differ. The probe was deleted.
- **Red at `08d4aec3`:** the routing and exemption cases on the assertion
  itself, the line-wrap case on the nested fence, and the routing parity case
  on all 19 shapes as a missing function. The handoff helper is new, so at
  `08d4aec3` its case is a missing name. Its meaningful red was shown by
  putting the old toggle in the helper.
- **`fence_opener`'s docstring** no longer lists these readers as a class
  with no fence state. Only `test_release_hygiene.py#overwide_rows` is left
  there, and it is A's (#585).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The fence toggles in `tests/test_docs_line_wrap.py#prose_lines` and `test_every_migration_command_creates_its_destination` | `#fenced_numbers` and `#fenced_block_lines`, over the shared delimiters |
| `hooks/routing.py#table_rows`, the `--exempt` reader and the two tests in `fence_opener`'s bullet of readers with no fence state | the same docstring's lists: the hook copy, the readers that ask the rule, and the wider opener. After the revert, `table_rows` is named in that docstring again, as a reader with no fence state that a new work item takes up |
