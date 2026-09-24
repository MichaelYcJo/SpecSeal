# 1790260563-the-fold-checks-run-only-as-this-repositorys-tests — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 0c18fab6 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The wrap skip, #583. `tests/test_docs_line_wrap.py#prose_lines` skips the
lines `fold_check.enforced_lines` returns, and only those. New cases were to
cover S7, seen red against today's `prose_lines`, and S8, green before and
after, since that is what pins the width of the skip. `seal/releases/0.13.1.md`'s
row was to be re-read and re-stamped.

## What this phase found

- **`enforced_lines` ignores the cutoff, on purpose.** The wrap skip is about
  what a line is, and #565 will add `Enforced by:` lines to statements below
  the cutoff. A skip that followed the cutoff would refuse exactly those
  lines at their first commit.
- **It asks the same predicate the shape check asks.** `names_targets` is
  the condition that sends a value to target resolution rather than to the
  `nothing` arm. An empty `Enforced by: ` counts as targets there, so it is
  skipped here too. That line is narrow and cannot overflow, so the skip
  hides nothing.
- **S8 has three shapes of *outside any statement*:** a line under a heading
  with no marker, a line after a heading that ended the statement, and a
  line whose marker sits in a fence. The reader reads none of them, so none
  is skipped.
- **Seen red (§15).** At `a34fd12d` the S7 case failed because line 5, the
  `Enforced by:` line, was yielded as prose. S8 passed before and after.
  Mutated at `5c6fdb71`: every statement line skipped, 2 red; `nothing`
  lines skipped too, 1; the skip off, 1; the skip one line wide, 1.
- **0.13.1's marker row re-read.** The marker arm is untouched and its cases
  are green, so the claim holds. It is noted `Re-read 2026-09-25` and
  re-stamped, and the new skip is the fragment's F7.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
