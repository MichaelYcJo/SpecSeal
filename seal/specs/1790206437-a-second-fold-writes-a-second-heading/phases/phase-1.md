# 1790206437-a-second-fold-writes-a-second-heading — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | d08c671a |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

The measured instance. Plant
`tests/test_release_hygiene.py#test_no_version_heads_two_sections_of_this_ledger`
beside the changelog case, run it red against the tree as it stands
(`0.9.3 twice, at lines [1673, 1764]`) and copy the red output into this
record; then remove `seal/ledger.md` lines 1764–1765 (the second `## 0.9.3`
heading and the blank after it) with every row byte-identical;
`evidence-check` totals equal before and after; `fold_ledger.py --check`
exit 0 with the same count.

## What this phase found

**The frame holds.** Lines 1763–1766 of `seal/ledger.md` at `9f846733` read
`''`, `## 0.9.3 — 2026-09-08`, `''`, the marker for `1788890000`, as
`plan.md` §Technical context says (executed: a Python read of lines
1755–1772). `duplicated_version_headings` reads any text and
`read_text("seal", "ledger.md")` opens the file, so the ledger case is the
changelog case with the path and the message changed, as the plan says.

**The red run, copied** (`bin/test tests/test_release_hygiene.py -q -k
test_no_version_heads_two_sections_of_this_ledger`, exit 1, before the
repair):

```
E       AssertionError: seal/ledger.md heads 0.9.3 twice, at lines [1673, 1764]. One release, one section: move the later heading's work items under the first and delete it
E       assert not [('0.9.3', [1673, 1764])]
tests/test_release_hygiene.py:1123: AssertionError
FAILED tests/test_release_hygiene.py::test_no_version_heads_two_sections_of_this_ledger
1 failed, 45 deselected in 0.08s
```

**The repair, measured.** `git diff --stat -- seal/ledger.md` reads
`1 file changed, 2 deletions(-)`, and the two deleted lines are
`## 0.9.3 — 2026-09-08` and the blank after it. `evidence-check --strict .`
before: `total: 1662 ok · 0 drifted · 0 broken · 0 external · 0 old-format`,
exit 0; after: the same line, exit 0. `fold_ledger.py --check` before and
after: `118 work items marked in seal/ledger.md`, exit 0 both times. The
hygiene module after the repair: 46 passed, exit 0. `uvx ruff check` and
`uvx ruff format --check` over the test module: exit 0 each.

**One wording choice.** The changelog case's message says *merge the later
heading's entries into the first*; the ledger's message says *move the later
heading's work items under the first*, because a ledger section holds
marked `###` work items rather than entries, and the repair a reader makes
is the one this phase made.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md` line 1764, the second `## 0.9.3 — 2026-09-08` heading, and the blank line 1765 | nowhere — `1788890000`'s marker, `###` and rows now stand under the first `0.9.3` heading, which carries the same date; no row moved |
