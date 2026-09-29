# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 3c0787ff |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 3: `rider_check.py#comment_blocks` — in a `.md` file, a line
inside a fence span opens no rider and changes no comment state. It loads
`unverified_check.py` with `load_checker`'s missing-file shape, and the
docstring's paragraph on what opens a block says so. Verified by S8 and S9
in `tests/test_a_rider_reaches_its_file.py`, and the tree's own
`rider_check.py` run unchanged except for the rider phase 1 retired.

## What this phase found

- **Reverted after round 3, at the owner's decision.** `.github/scripts/
  rider_check.py` is byte for byte `release/v0.16.0`'s again, with this
  phase's fence walk, round 1's and round 2's fixes to it, their cases in
  `tests/test_a_rider_reaches_its_file.py`, and their ledger rows gone. A
  rider inside a fenced example is read as a rider once more, which is the
  behaviour the release ships. The reason: the fence walk had to know which
  comment delimiters were real, and each round found a shape it read wrong
  (round 1 🟡 4, round 2 🟡 1, round 3 🟡 2), the last one closable only by
  reversing an assertion round 2's fixes pinned. A new work item redoes it
  from a clean frame. The bullets below record what the phase found when it
  was built; they describe no code in the tree.
- **`fence_spans` has no comment state, and the rider walk does.** The two
  models disagree only where a fence delimiter stands inside an HTML comment.
  The build settles it one way and pins it: a rider block that is already
  open runs to its own `-->`, whatever fence lines it holds, because inside
  a comment nothing is markdown. A lone ```` ``` ```` inside a comment can
  still open a span that `fence_spans` runs to the end, which hides every
  later rider in the file. That loses an alarm rather than inventing one,
  the direction the module's docstring requires, and no file in the tree has
  the shape.
- **The reader is loaded lazily.** `fenced_lines` loads
  `unverified_check.py` the first time a markdown file carrying the marker
  is read, so the missing-file sentence names the path at the moment it is
  needed. `load_reader` has `load_checker`'s shape: a sentence on stderr and
  `SystemExit(2)`. A third case pins that sentence (§14).
- **The re-measure the spec asked for.** `rider_check.py` over this tree
  reads 21 riders at `7ec376df` and 21 at `3c0787ff`, exit 0 both times, so
  no shipped markdown file carries a rider inside a fence. The 22 → 21 step
  is phase 1's retired rider.
- **S8's fixture could not keep a `path:line` in its ledger row.** The first
  draft of R1 quoted the refusal's `skills/x/SKILL.md:6`, and
  `evidence-check --strict` read it as an old-format coordinate. The row
  says what the refusal was instead.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
