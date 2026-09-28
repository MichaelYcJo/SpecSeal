# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 3f422fa7 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 4: `correction_check.py#rows` skips rows inside a fenced
block that closes. It loads the reader by path and exits 2 with a sentence
where it is missing. §*What it reads* in the module docstring says which
rows. Verified by S10 and S11 in
`tests/test_a_merge_cannot_silently_drop_a_correction.py`, and S18's row for
this script.

## What this phase found

- **The loader runs at import.** `correction_check.py` does everything else
  after `parse_range`, which asks git first, and S18's copy is run in a
  directory that is no repository. A lazy load would never be reached there:
  against the old script the case exits 2 from the range refusal and names
  no path. Loading at import is `round_record.py`'s shape, and it means any
  invocation reaches the sentence.
- **`marker_counts` reads through `rows` as well**, so the base-parent
  comparison that decides whether a parent honoured a deletion uses the same
  rows. No separate edit was needed and none was made.
- **S11 carries the comment half of the direction too.** A row inside an
  HTML comment is read by the checker (`evidence_check.py#quoted_lines`'s
  docstring), and S11 asserts its loss is still reported.
- **`tests/test_a_script_copied_alone_exits_2.py`'s docstring lists the
  scripts it holds.** It gained `correction_check.py` and a paragraph saying
  why #584 added it, so the list is not one short. Phase 5 adds
  `payload_meter.py`'s second loader to the same paragraph.
- **The `fence_opener` docstring** moves `correction_check.py#rows` from the
  readers that keep their own rule to the readers that ask it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/evidence-check/scripts/correction_check.py#rows` in `fence_opener`'s list of readers that keep their own rule | the same docstring's list of readers that ask it |
