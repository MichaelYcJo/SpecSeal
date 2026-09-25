# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 0de23540 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#592, the first of three phases built in order. `paired_across_paths` orders
each key's departures by affinity to the arrival's path, then by gone at `b`,
then by path order, and `corrected` passes it the paths present at `b`. The
docstring says why. `docs/review-chain-spec.md`'s second statement gains the
clause that the `corrected` coordinate names the correction, not the move.
Verified by spec S1 (red at the base), S2 (the moved file sorts first) and S3
(a one-sentence move); M6 and M7 green unedited; the whole module green; and
`RELEASE_RANGES` unchanged, or each moved coordinate explained (questions
Q1). Every new case seen red before the fix, and the red recorded here. The
38 lines left in `docs/review-chain-spec.md` are shared by the three phases
(Q3).

## What this phase found

- **S1 alone cannot tell affinity from gone-at-`b`.** In S1 the moved file
  is gone at the tip, so a rule of gone-at-`b` alone passes it. That rule is
  the rejected alternative, and it fails on a split whose two files both
  remain. So a fourth case was added, not named in `spec.md`: a section
  split off `docs/m.md` into `docs/z.md`, both files kept
  (`test_a_split_pairs_with_its_own_origin_while_both_files_remain`). It is
  the case that goes red when affinity leaves the order.
- **Red at `2e0e2fa7`, executed.** S1 and the split both named
  `docs/m.md` line 3 as the correction, and S3 named `docs/m.md` line 1.
  Each reported the same two places at 1.67, before and after. S2 was green
  there, as the spec says it would be. S2 goes red only when the order is
  reduced to reversed path order, which is the fix #592 would get if it were
  treated as an ordering problem.
- **The pairing is counted per path, not per sentence pair.** The first
  version sorted every departure-arrival pair of a key. A ledger fold moves
  hundreds of rows whose date or empty cells share one key, so that version
  cost departures times arrivals per key. The version committed sorts path
  pairs and pops sentences from them in order. The result is the same:
  within one rank, departures and arrivals are still taken in the order the
  lists hold them.
- **Mutations, one at a time, the file restored from a copy after each.**
  Five mutations were run over the eight move cases. Affinity taken out of
  the order: the split was red. Gone-at-`b` taken out, or `corrected` not
  passing the paths at `b`: S3 was red. The order reduced to reversed path
  order: S2 was red. The one-for-one pop replaced by pairing whole paths:
  M6, M7 and all four new cases were red.
- **Q1 at this phase: unchanged.** `RELEASE_RANGES` passed unedited in the
  whole-module run at `0de23540`, so the four ranges name the same
  coordinates as before.
- **Q3 at this phase: 2 lines.** The clause took two lines of
  `docs/review-chain-spec.md`, which now has 964 lines. `bin/fold-check`
  exits 0.
- **A memo was owed and missing.**
  `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
  was red because this work item had a spec and no `overview.md`. That is
  red at the framer's commits too. This phase opens the memo.
- **The narrow run.** 21 modules read `docs/review-chain-spec.md` or
  `survivor_check.py`. Run together at `0de23540`: 1269 passed, 1 skipped,
  and 1 failed, the memo case above. `ruff check` and
  `ruff format --check` are clean on both Python files.
- **CONTRIBUTING's four items.** Red test: above. Failure direction: none
  on the verdict. The key, and so its n-grams, is the same for every
  departure it could pair with, so only the printed `corrected` coordinate
  moves. Prompt budget: 0, because the sweep asks nobody anything. Platform:
  pure text over git blobs, and paths come from git with `/`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `paired_across_paths`' pairing by path order alone | none — replaced by the ordered pairing; the `corrected` coordinate it produced for a correction beside a move was the defect |
