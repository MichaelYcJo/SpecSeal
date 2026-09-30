# 1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule — phase 5

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 848d9531 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 5, the rider check on the walk: in a `.md` file, a
marker line the walk places inside a fence that closes opens no rider and
changes no `in_html` state; `#region_lines` follows through `comment_blocks`;
other file types unchanged. K1 to K7, each marked red failing against
`3911a8cf`'s `rider_check.py`; K8's measurement over `RIDER_ROOTS`. The spawn
named work item B (#663) as landing in the shared reader meanwhile, to be
merged hunk by hunk.

## What this phase found

- **B landed before this phase, and one hunk conflicted** (`72d03c43`):
  `unverified_check.py#fence_opener`'s docstring, which both branches
  rewrote. The release side's structure was kept, two lists of readers, and
  its two bullets naming the hook readers were rewritten: the delimiter copy
  is `hooks/blocks.py#FENCE`, read through the walk by `hooks/config.py` and
  `hooks/routing.py`, and after this phase by the rider check through
  `quoted_lines`. Nothing #663 reverted is named (Q6).
- **`rider_check.py#quoted_lines` is the one new unit**, and it loads
  `hooks/blocks.py` by path in `load_checker`'s shape, lazily, at the first
  markdown file that carries the marker. `comment_blocks` asks it only for a
  `.md` file that holds the marker, and steps over a quoted marker line
  without touching `in_html`. Both halves of that sentence went red under
  their own mutation, the second only after a case was written for it
  (`test_a_quoted_marker_line_leaves_the_comment_state_alone`: a rider that
  never closes, a fence below it quoting a rider, then a bare marker line the
  open comment still makes a rider), and the first only after the `.py` case
  gained two backtick lines around a top-level rider.
- **K4 is kept as `1790635413` pinned it, not as its round 3 proposed.** The
  fence under the lone backtick never closes, so it is no fence, and the
  rider below is read; the frame's D4. The mutation that runs an unclosed
  construct to the end turned K4 and the unclosed-fence case red.
- **Seen red against `3911a8cf`** with that commit's `rider_check.py` in
  place: K2, K3, K5, K7 and the whole-check case failed; K1, K4 and K6
  passed, as the frame marks them.
- **Every pin was seen red too**, since a pin passes at the base by design.
  Each was run under a mutation that brings back the reading it pins
  against: a mid-line opener opening a comment block (C1, C4, C13, R7, K2,
  K3), an unclosed construct running to the end (R3, K4), an unclosed comment
  switching off every fence below it, round 3's own finding (C3, R6, R6b,
  R8), an unclosed comment hiding everything below (C9a, C9b), the fence
  rule alone, fence first, in routing (R3, R4) and in the rider check (K1,
  K4), and a config reader that hides nothing (C12, C14).
- **K8, measured (Q3's rider third, answered (a)).** Every file under
  `RIDER_ROOTS`, 241 files of which 46 are markdown: `comment_blocks` gives
  the same 20 blocks with `3911a8cf`'s script and with HEAD's, and the check
  exits 0 on this tree with either, `20 ok · 0 drifted · 0 broken`.
- **The ledger pass for the whole work item ran here**, once, after the
  three readers had drifted theirs: 31 rows in 13 ledger files re-read with a
  dated note, two corrected in place (`seal/releases/0.15.3.md`'s P1-2, which
  named `fence_map` as the delimiter copy, and `seal/releases/0.12.1.md`'s
  R7, whose note said `fenced_row` takes the complement of what the reader
  shows), and every file re-stamped; `evidence-check .` then read 2802 rows,
  0 drifted, 0 broken, exit 0. Two names the frame cites that no longer
  exist were settled the checker's way: `QUOTED_DELIMITERS` is C1's name in
  the mode-question module again, and `plan.md`'s rejected-alternatives row
  marks `hidden_by_the_shared_rule` NAME NOT IN TREE.
- **Gate lines, drafted for `CONTRIBUTING.md` §*What a change to a gate must
  carry*.** Seen red: above. Failure direction: the check stops failing on a
  rider quoted in a fenced example (K5, K7), and reads every rider it read
  before (K1, K4, and 0 of 241 files differ); the one alarm this checker's
  own docstring says it must never invent is the one removed. Prompt budget:
  none, a CI check asks nobody. Platform: string processing only; CI's three
  legs are the pull request's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `unverified_check.py#fence_opener`'s bullet saying the routing reader and the rider check keep no fence state | the same docstring's bullet on `hooks/blocks.py#FENCE`, which names both as readers of the walk |
