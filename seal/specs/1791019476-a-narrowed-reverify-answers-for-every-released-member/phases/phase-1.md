# 1791019476-a-narrowed-reverify-answers-for-every-released-member — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 72a9c90a |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build 🟡 16 in the order `plan.md` gives for phase 1. First, in
`tests/test_a_released_row_is_read_again_in_a_fragment.py`, plant the
enumeration over spec §*The class, enumerated*, asserting S4's invariant per
cell, with the control cell for a superseded family. Then plant round 3's
two cases as S1 and S2, and see all of them red against `2b1dcb1f`'s filter.
Then the fix: `released_drift`'s family filter tests `view.families[top]`
against every ledger the run read, its first loop stays released-only, its
docstring is rewritten, `main`'s freeze branch hands `reverify_into` the
whole narrowed list, and the no-freeze comment is rewritten. Then the home's
**Without the row** sentence (S7) and the changelog's first `### Fixed`
entry. Answer M1, M2 and W1 here. Q1(b) is decided as the frame chose.

## What this phase found

**The frame held, with one sentence that is literally false and harmless.**
Spec D3 says "every family's root is released". It is not: a `Corrected ·`
row in a fragment roots a family of its own (`family_view`'s `root_of` stops
at any verb but `Re-read`), and so does a citing row whose citation does not
resolve. Neither family can hold a released member, because a citation into
a fragment is refused and joins nothing, and `released_drift`'s second loop
grades released members only. So such a family owes nothing narrowed or
unnarrowed, before the fix and after it, and D3's conclusion stands. Read,
not executed.

**The red cells at `2b1dcb1f`, executed.** The new cases ran against the
checker as `2b1dcb1f` held it, before any edit to it: 18 of 77 failed.

- The two report cases, S1 and S2, failed with `0 citing rows written` and
  with exit 0 and no `LEFT` line.
- 16 of the 72 enumeration cells failed, each because `--reverify` exited 0
  and `--strict` with the same narrowing exited 2:
  - narrowed to M's file: all 12 cells, M in a release or a fragment, N in a
    release or a fragment, every mode;
  - narrowed to N's file with N folded into a release, under the freeze, with
    or without `--into`: 4 cells. Without the freeze the in-place re-stamp
    reaches N, so those 2 cells were green.
- Every cell narrowed to R's file, R's and M's files, an unrelated fragment
  or nothing was green, and so was the superseded control in all three
  modes. That is S5's half: those columns do not change.

**M1, answered by measurement: the fragment cell is red.** The 6 cells with
M in a fragment, narrowed to M's file, failed at `2b1dcb1f`. A second
measurement says D1's fragment half is what closes them: with the fix in
place and membership cut back to released files alone (`read_here = wanted`,
round 3's paste-ready shape), exactly those 6 cells go red again.

**M2, answered by measurement: no cut.** The 77 new cases took 5.5 s under
`bin/test`'s parallel run, and the whole module of 123 took 3.3 s. All 72
cells stay.

**W1, met by no cell.** In every cell where the no-freeze `LEFT` line fires,
the newest reading N sits in a file the narrowing left out, so "sits in a
file this run did not write" is true there. The enumeration holds no row
without a date cell, which is W1's only candidate. The wording is unchanged.

**One way round 3's paste-ready text would have gone wrong, not taken.** It
kept passing `released` to `reverify_into` in the freeze branch. With that
argument left as it was, the 4 freeze cells with M in a fragment stay red
even with the widened filter; a mutation of that argument alone shows it.

**Mutations, executed with `bin/mutation-check`, each red:**

| Unit | Break | Cases red |
|---|---|---|
| the family filter | back to `if top[0] not in read_here` | 18 |
| membership over every ledger read | `read_here = wanted` | 6, the fragment-M cells |
| the freeze branch's argument | pass the released files alone | 4, the freeze fragment-M cells |
| the control's premise | grade superseded families in `family_view` | 2 of the 3 control cells |

**The narrow run at the phase boundary, executed.** `bin/test` over the 40
modules that read a file this phase edited (`grep -l` over `tests/` for
`evidence_check.py`, `the-evidence-ledger`, the test module's name and the
changelog fragment): 2,285 passed, 7 skipped, 2 failed.

- `test_chain_hooks_hardening.py`'s overview case failed because this work
  item had no `overview.md` yet. It is written in `72a9c90a`, and the
  module then passed.
- `test_a_record_states_what_the_tree_has.py`'s own-records case fails on
  the base as well: four lines in `1790993137`'s records name
  `SELF_ANCHOR_RE`, which #736 removed. The integration branch's `bb2f3400`
  marks them, and this branch takes that when `origin/release/v0.18.0` is
  merged in. Not this work's to fix.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `main`'s `released` list in the freeze branch, which only `reverify_into` read | none: `reverify_into` now takes the whole narrowed list |
| the home's sentence saying a narrowed `--reverify` names "each released row it read whose family's newest reading sits in a file it did not write" | `docs/the-evidence-ledger.md`, the same paragraph, rewritten to name each family by its root row |
