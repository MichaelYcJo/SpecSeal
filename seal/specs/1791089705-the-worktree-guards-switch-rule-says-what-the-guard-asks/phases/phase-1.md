# 1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | f5dc2aa2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build #750 to the approved frame (`401b9fc7`, approved at `dc0553fb`), with
D1–D7 as the frame decided them and M1 and W1 left to the build. First fetch
and merge `origin/release/v0.18.1` (head `edee5ca2`, where #756, #757 and
#758 had squashed) into the branch, never rebasing, and confirm the frame's
coordinates still hold after the merge. Then make commit A (the sentence, the
docstring, the pin and three `KINDS` rows) and commit B (the rule case's
`frozen` clause) as the plan cuts them, and write the records. Every check
is seen red first, each new `KINDS` row against the mutant `spec.md` A3
names. Leave the glued-option shape alone (filed as #764). Do not push. Run
`bin/survivor-check` over the build range and `bin/evidence-check --strict .`
before handing back, and re-read no ledger row outside this item's own
drift: the 10 rows the wave-one squashes drifted belong to a parallel chore.

## What this phase found

**The frame holds after the merge.** The merge brought `encoding="utf-8"`
into three `open` calls of `hooks/worktree-guard.py` (`dead_session_ids`,
`fresh_leases`, `already_asked`) and into `write_text` calls of
`tests/test_guard_resolves_the_tree_it_judges.py`, all from #757. None of
them is in `switch_kind`, `wider_only_kinds`, the three test units C1–C3
edit, or `docs/worktree-guard-spec.md`. Every line number the frame names
still holds (`switch_kind` at 290, `wider_only_kinds` at 320, the rule case
at 1204, the pin's host at 1251, `KINDS` at 1315), and the round-3 fences
applied without change.

**Each check was seen red, one at a time.**

- The pin failed against the sentence as it stood, and passed after S1–S3.
- The three new `KINDS` rows passed against `switch_kind` before any edit.
  Each turned red alone through `bin/mutation-check` against its own mutant:
  `-B` dropped from the `checkout` tuple, the `checkout` branch's `--`
  return deleted, and `switch` reading only the words before `--`.
- The rule case survived the mutant `kind and kind not in frozen` → `kind`
  before C3, which is round 3's ⬜ 10 measured again. After C3 the same
  mutant turned it red, with 1,180 generated shapes outside the rule.

**The A7 range in `spec.md` would read the merge.** `spec.md` A7 names
`e141980a...HEAD`. After the merge that range also carries #756–#758, so
`survivor-check` would weigh sentences this item did not remove. The build
ran the range from the merged release head instead
(`origin/release/v0.18.1...HEAD`, base `edee5ca2`) and the build range
`807fe9e7..f5dc2aa2`. Both report three removed sentences and no survivor,
which answers M1.

**`spec.md` held one stamp the records arm refused.** Once the ledger
fragment existed, `evidence-check` started reading this work item's records.
It refused `spec.md`'s quotation of K7's coordinate, which shortened the
heading to `"### Which tree…"`, as `BROKEN` (locator not found). The build
wrote the heading out in full and kept the hash the released row cites. The
stamp now reads `DRIFTED`, which a live work item's records are allowed to
be. No other word of the frame changed.

**`--reverify --into`, narrowed to the two release files, wrote five rows.**
Narrowing it to `seal/releases/0.16.0.md` and `seal/releases/0.18.0.md`
still answers for every family those files hold a member of. So it also wrote
`Re-read · C4` (`tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT`)
and `Re-read · S8` (`templates/config.md`). Both are wave-one drift, so the
build removed them from the fragment unread. The three it kept are M2, K5
and K7, and each was read against the changed text before it was dated.
`Re-read · M2` in `seal/releases/0.18.0.md` belongs to M2's family, so the
one row citing the 0.16.0 root answers it.

**W1, the docstring.** `switch_kind`'s docstring now states the checkout's
order as `classify` has it: `-b` or `-B` counts with or without a name, then
a `--` anywhere means no switch, then `-` or a word other than `.` counts. It
also says that a `switch` counts wherever it names a word or `-`, with or
without `--`. It names `docs/worktree-guard-spec.md` §*Which tree* as the
place that states the same words.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the old word list in §*Which tree* ("a `switch` or a `checkout` naming a word or `-` (other than `checkout`'s `.` and anything after `--`), a `checkout -b`") | none. It was wrong, and the corrected sentence replaces it in the same place |
| "every `checkout` with a name in it counts" in `switch_kind`'s docstring | none. It was wrong for a name before `--`, and the corrected docstring replaces it |
