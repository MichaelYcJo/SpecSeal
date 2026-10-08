# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | a2bc18ec |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 3: `"block"` for `.yml`/`.yaml` with the compact-sequence
item at the key's indent; the three repository coordinates in S7 keep their
spans; `bin/evidence-check --strict .` on the branch shows no `BROKEN` and no
`DRIFTED` that `main` does not show (Q2 measured here), its output quoted
here. Case S7 red, then green.

## What this phase found

**Q2 is 0 and 0, measured on this branch's own tree rather than against
`main`.** `main` predates the release branch this branch merged, so its
ledger is a different ledger. The measurement that isolates the rule change
is one tree read by two checkers: `bin/evidence-check --strict .` at
a2bc18ec, and `origin/release/v0.21.0`'s `evidence_check.py` (extracted with
its siblings into a scratch directory, deleted after) run with `--strict .`
from the same worktree. The two outputs are byte-identical (`diff` exit 0,
183 lines each), and both totals read:

```
7382 ok · 34 drifted · 0 broken   (summed over every ledger file)
```

Both exit 2. The 34 drifted rows are rows whose cited unit changed in the
tree, which a checker reads the same whichever rule bounds it: 25 cite
`evidence_check.py` units this branch rewrote (`resolve_unit` 7,
`file_units` 6, `judge` 4, `content_matches` 2, `py_spans` 2,
`read_citation` 2, `generic_units` 1, `minor_region` 1) and one cites
`.github/scripts/rider_check.py#region_lines`; phase 4 re-reads each and
re-stamps it. The other 8 cite `agents/warden.md#"## Report"`, which
`origin/release/v0.21.0`'s #837 changed and this branch did not touch
(`git diff origin/release/v0.21.0 -- agents/warden.md` is empty): not this
work item's, and named in the hand-back.

**The S7 coordinates are compared with the indentation rule, not pinned to
line numbers.** `spec.md` quotes 32–128, 146–164 and 46–138 from
2026-10-07; the release branch's #864 has since rewritten `test.yml`. The
case computes the indentation rule's span over the file as it stands and
asserts the block rule's equals it, so a later edit to the workflow cannot
turn the case red for a reason that is not this rule.

**A compact item joins its key only at the key's own indent.** The first cut
sliced the line at the key's indent and survived two mutations; an item
further out (the next element of the sequence the key's mapping sits in) is
a sibling, and a lone `-` opens an item too. Both are pinned.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The YAML half of the indentation loop's assumption that a line at the key's indent ends the unit | `block_span`, which reads a `- ` item at the key's own indent as the key's value |
