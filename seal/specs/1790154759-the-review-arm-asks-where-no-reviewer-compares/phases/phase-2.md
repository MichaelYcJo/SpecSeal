# 1790154759-the-review-arm-asks-where-no-reviewer-compares — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 122f0aae |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Write the policy half. In `docs/review-chain-spec.md` §*Review arm*, a row for
a change confined to `docs/` and `seal/`, contrasted with the parity arm's row,
and a short paragraph carrying the measurement (`spec.md` M1–M4) as grounds.
In `skills/implement/orchestration.md`'s wake/quiet table, the review arm's
*Wakes when* cell says it wakes whatever the change touches (A5). A case
pinning the row's sentence, seen red with the row deleted (A4). Answer
`questions.md` Q1.

## What this phase found

**Q1 took its default: the declaration row was added.** The prose under the
table explains the declaration at length, but none of it states the
decision, so a reader of the table saw three conditions and had to infer a
fourth. The row now sits between the waiver and the mark, in the order
`judge` evaluates them.

**M3 was re-read before the paragraph quoted it.** The `## Verdicts` tables of
`seal/specs/1790119502-four-shipped-work-items-wait-unfolded/rounds/round-{1,2,3}.md`
hold four findings fixed in round 1 and three in round 2, every Location in
`docs/`, one 🔴. `docs/flow.md`'s deletion is `d851bd14`, dated 2026-09-11.
M4's counts (25 and 26) are carried from `spec.md` as a lower bound, written
"at least" in the paragraph; the framer's probes were not kept, so they were
not re-taken here.

**One case pins four sentences, and each was seen red on its own.** Deleting
the `docs/` row, the grounds paragraph, the declaration row, or the wake
cell's added clause each fails
`test_the_review_arms_missing_path_line_is_written_where_it_is_met` with its
own message. Every edit was restored from a saved copy.

**No other copy of the wake cell exists.** A search of `docs/`, `skills/`,
`agents/` and both READMEs for the cell's text and for *Wakes when* found only
`skills/implement/orchestration.md`, so nothing else had to move with it.

**Executed:** 39 test modules at `122f0aae` — every one that reads
`docs/review-chain-spec.md` or `skills/implement/orchestration.md`, plus
`tests/test_one_word_one_meaning.py` and `tests/test_no_real_identifiers.py`: `1735 passed, 1 skipped`, exit 0. The module list was taken by
`grep -l` over `tests/*.py`. That is the widest run of this build; it is still
not the suite, which stays the sealer's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
