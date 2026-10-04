# Implementation Plan: every family no re-read can clear is named, and `--into` refuses a stale date

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

Two phases. Phase 1 adds one refusal to `reverify_into`. When `--checked` is
older than the newest reading of a coordinate a `Re-read ·` row would carry,
the row is not planned and gets no move. It is named on a `LEFT` line, and the
run exits 1. Phase 2 measures which families `--reverify` still leaves at exit
0 against `--strict` 2. It then writes the ledger home's paragraph naming each
one, and pins each with a case. Phase 1 goes first because it takes the stale
row out of the class, so the paragraph phase 2 writes can say that.

## Technical context

All coordinates were read at `edee5ca2` (this branch's base).

- `skills/evidence-check/scripts/evidence_check.py#reverify_into`. It walks
  `released_drift`'s `drifted` keys. For each key it builds `stamped` from
  `current_hash` and appends to `moves` per coordinate, then appends the row
  to `rows`. The refusal goes after the `cite is None` check and BEFORE the
  coordinate loop. That way a refused row reaches neither `stamped`/`rows`
  nor `moves`, so `record_pact_changes` (step 2) and `put(into, …)` (the plan)
  hold nothing of it.
- `#family_view`. Its nested `checked(key)` returns the newest calendar date
  in a row's `Checked` cell. Its per-coordinate `newest` and `last` are
  computed and used only for the DRIFTED detail. They are not returned.
- `#released_drift`. It builds `drifted[key][coord] = m` from two sources: the
  `wanted` loop (released rows outside every family) and `view.readings`
  (family roots).
- `#main`, the reverify branch. Step 0 holds the existing refusals: the
  freeze row, `--into` not a fragment, and `--into` unreadable. Then come
  PLAN (`PLANNED`), `recorded_then_applied` (RECORD, then APPLY), and the
  `told` reports.
- `#checked_refusal` refuses a `--checked` later than today, before any
  ledger is read. That is why an after-today newest date can never be
  reached by a `Re-read ·` row (S3's second arm).
- `#dated_cell` appends ` · <date>`. Together with `checked`'s `max`, this is
  why an in-place re-stamp is never stale (spec §*The class*).
- Tests: `tests/test_a_released_row_is_read_again_in_a_fragment.py` holds
  `three_readings`, the 144-cell narrowed grid (`--checked 2026-04-01`, newer
  than every reading), `MEMBER_INTO`, `frozen`, `digests`, and the two cases
  S5 extends. `tests/test_a_signatory_records_a_pact_change.py` holds the
  record cases.

**What breaks in six months.** The refusal compares against a date that the
grading computes. If the two ever compute "newest" differently, the refusal
either lets a stale row through (the bug returns quietly) or refuses a row
that would have cleared. The chosen approach below exists to keep one
computation of that date. The other risk is cost. A stale-date axis on the
grid multiplies subprocess runs, so Q4 measures the cost before the shape is
chosen.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Refuse at step 0**, beside the `--into` refusal: exit 2, nothing planned | Step 0 runs before the in-place re-stamp. Take a family whose newest reading N sits in a fragment the run itself re-stamps. N's hash moves to current at N's own newest date and the family clears, so no `Re-read ·` row is written. A step-0 check reads N as an unanswered newest reading and refuses a run that would have written nothing stale. Computing it correctly at step 0 means running the plan first, and then it is no longer step 0 | rejected (W9's first option) |
| **Refuse the whole run after the plan and before the record** (exit 2, plan discarded) | Kill-safe, but one stale family throws away every other family's valid row and every fragment re-stamp. A narrowed run over many families reruns everything to fix one date. Against the project's unattended goal, the run as a whole stops for one row | rejected |
| **Refuse per row inside `reverify_into`, in step 1**: the row is kept out of the plan and its moves, named `LEFT`, exit 1 | A partially written run: other rows land, and the refused family stays DRIFTED until it is re-read. This is already `reverify_into`'s contract for every `LEFT` (*Name every released row it could not write … Exit 1 where a row was left*), and the round-2 report proposed this repair | **chosen** (W9's second option) |
| Refuse per coordinate and write a partial row with the non-stale coordinates | The row's Notes say *the cited row's claim holds* (`INTO_VERIFIED`), a claim about the whole row, while some of its coordinates were not answered. It would also print `wrote` for a family still DRIFTED | rejected. A whole row is refused (spec S1) |
| Rewrite the stale date up to the newest | The date is what the person typed about their reading (`checked_refusal`'s docstring). Raising it records a reading that never happened | rejected |
| Return `newest` from `family_view` (`{root: {coord: (date, key)}}`), and lift `checked` to module level so that `released_drift`'s `wanted` loop uses the same rule for a released row outside every family | One rule and two readers, so the refusal and the grading cannot disagree | **chosen** for the date. If the build finds a smaller shape that still has ONE dating function, that is the build's call, recorded in `phases/phase-1.md` |
| A second date computation inside `reverify_into` | Two spellings of one rule. This is the drift `exit_code`'s docstring warns about | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | ⬜ 12: S1–S3 and S6. The refusal in `reverify_into` (step 1), the shared newest-date rule, the `LEFT` line with both repair arms, the `--into` sentence in `docs/the-evidence-ledger.md` and the usage clause in `evidence_check.py`. Cases A1–A7. The fragment rows for S1, and the re-reads of the released rows this phase drifts (`reverify_into`, `released_drift`, `family_view`, and any other unit it edits) into this item's fragment with `--reverify --into` | A1, A2, A4–A6 seen red at `edee5ca2`, and A3 red under a `<=` mutation, then all green. `bin/test` over `tests/test_a_released_row_is_read_again_in_a_fragment.py`, `tests/test_a_signatory_records_a_pact_change.py`, `tests/test_two_branches_re_read_one_released_row.py` and `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`. `evidence-check --strict --ledger <this fragment> .` | 4c148310 |
| 2 | ⬜ 11: S4 and S5. First the enumeration (Q1): every family × carrier (released root, folded member, fragment member, fragment root) × mode (no freeze, freeze without `--into`, freeze with `--into`) × narrowed or not, for the DRIFTED and BROKEN gradings, listing each cell where `--reverify` exits 0 and `--strict` exits non-zero. Then the bold-led paragraph that replaces the double-correction sentence, naming every family found. Cases A8–A10, each seen red by a mutation. The changelog fragment for both findings, and the fragment rows for S4 | the enumeration's table in `phases/phase-2.md` (a measurement, its probe deleted per §7). A8–A10 red under their mutations, then green. `bin/test` over the module, `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py`, `tests/test_no_real_identifiers.py`. `evidence-check --strict --ledger <this fragment> .` | |

The broad gate (full suite, lint, typecheck) is in neither phase. It is the
sealer's, once the rounds settle.

## Operational impact

- No new flag, no new exit code, no new dependency, no migration.
- One behaviour change a person meets: `--reverify --into` with a backdated
  `--checked` used to exit 0 and write a row that cleared nothing. It now
  exits 1, writes nothing for that row, and says why. The failure direction
  is *refuses more*. A wrong refusal costs one rerun with the date of a real
  reading. A wrong allow is the bug, an exit 0 over a family that is still
  owed. Prompt budget: none. Nothing asks a person anything.
- **Integration with the parallel re-read chore.** Both branches may write
  `Re-read ·` rows citing the same released row. Under the newest-date rule
  the later reading wins per coordinate, and a same-day pair is a union. If
  the chore's reading is dated later and records the pre-edit hash of a unit
  this work edits, that coordinate reads DRIFTED once both land, and
  whichever branch integrates second reads it again. That is the work's to
  meet at integration (questions.md Q5). It is not a reason to take the
  chore's rows here.
