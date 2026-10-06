# 1791240748-reverify-computes-once-and-judges-in-one-place — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 30bf8be4 |
| Ran by | unknown — the spawn prompt named neither the agent nor the model, and this record does not source the value from the segment itself |

## What this phase was asked

`reverify` rewritten (spec D1, D4, D5). First S2, S3a in place, S3b, S3c,
S4, S5, S6, S7, S8, S9 planted and seen red at the base or under their
mutations; the walk-order cases removed or rewritten as the spec's table
says; the `left`-word assertions rewritten (S11). Then the recomputation,
one write, MOVES from the final plan, the `left` lines from the judge, D4's
reader of every ledger coordinate in files left out; `cited_first`, the walk
loop, `first_old`, `still`, `walked_move`, `owed_moves`, `walked_outcome`,
`left_because`, the `unplaced` copy and `citations_left` removed. `reverify`'s
docstring and the usage text rewritten. D6's probe 2 for `--reverify`, every
difference classified. Questions Q1 decided by the work.

## What this phase found

**Q1, decided: each round judges against the round before, and a pass that
reaches its bound leaves only the cycle.** Every coordinate naming a ledger
the run writes is judged against the previous round's planned text, never a
plan edited file by file, so S4 holds by construction. The bound is the
number of such coordinates still judged, plus two: an acyclic chain of
them settles within its length plus one round. A repeated-state check was
not taken, because the row S6 describes never repeats a state: its hash is
part of the line it hashes, so every round's text is new. At the bound the
coordinates still moving are not all left. `on_a_cycle` reads each one's
verdict region and keeps those whose naming leads back to their own row; a
coordinate downstream of a cycle is recomputed once the cycle is left and
settles (`test_a_row_naming_one_that_never_settles_is_restamped`). Of those
left, one that reads OK against the final text is named nowhere
(`test_of_two_rows_quoting_each_other_only_the_one_still_moved_is_named`).
Within a round a verdict is reused where the file its coordinate names did
not change, except a BROKEN one, whose scan reads other files: a moved
section the run itself edits stops reconstructing the row's hash
(`test_a_re_point_is_judged_against_the_section_the_run_writes`).

**The frame holds; four of its facts were measured otherwise.**

- S6's base is not *silent, exit 0*. Over every ledger the base re-stamped
  the row once to a hash that drifted at once, and the family reader then
  named it `still DRIFTED … does not hold the code` and exited 1. The case is
  red at the base all the same: the hash it wrote, and no line saying the
  row does not settle.
- D7's list of released rows to correct names code units only. Six released
  rows also cite test functions this phase removed or renamed:
  `test_a_restamp_a_later_walk_leaves_is_a_move_and_then_broken`,
  `test_every_walk_sequence_hands_over_what_the_file_holds`,
  `test_every_walk_sequence_prints_what_the_file_holds`,
  `test_the_walk_order_survives_a_self_citation_and_a_cycle`, and
  `test_one_unfrozen_run_restamps_a_citation_no_order_places`, which the spec
  retitles (now `test_one_unfrozen_run_settles_a_self_citing_file_in_one_run`).
  `--strict` names each BROKEN; phase 4 writes their `Corrected ·` rows.
- `seal/releases/0.18.0.md:24` is already superseded by
  `seal/releases/0.18.1.md:417`, so its coordinates are not checked again,
  and a second `Corrected ·` row citing it would make the pair read DRIFTED as
  a double correction. Phase 4 corrects `0.18.1.md:417` alone.
- The held-coordinate branch's `OK` test was dead: `judge` gives every `OK`
  coordinate its hash, so an `OK` one never reaches the branch for a
  coordinate with no hash. Removed.

**What a person now reads, as the spec says (D2).** Every `left` line is the
check's sentence followed by ` — left`. Where the check's own sentence ends
`— re-verify`, the line reads `… — re-verify — left`; the spec's rule was
followed literally. A coordinate escaping every checkout now reads `not in
this repo; pass --map/--default-repo — left` or `file not found — left`,
where it read `not in any known checkout — pass --map/--default-repo; left`.

**D6 probe 2 for `--reverify`, executed.** The scratchpad plugin ran every
call of the script the seventeen modules make through the base script and
this branch in the same tree. 1,284 calls (708 `--strict`, 18 `--migrate`,
558 `--reverify`), 1,417 cases passing. `--strict` and `--migrate`: 0
differences. `--reverify`: 112, each classified.

| Class | Calls | What differs |
|---|---|---|
| D2, a `left` line's words | 71 | the line carries the check's sentence; one of them also prints its lines in another order |
| D1/D5, a walk-order artefact | 28 | 27 print the same lines in file order rather than walk order; 1 writes a pact-change record's two rows in that order |
| #806 (S2, S4) | 7 | B's coordinate of Q's line is re-stamped in the same run: exit 0 where the base exited 1, in S2 and in six of S4's orderings |
| #809, cell C8 (S3a) | 3 | `--into` writes the `Re-read ·` row; in place the row is re-stamped; both records hold the move, not BROKEN |
| S6 | 1 | the self-quoting coordinate keeps its hash and is named `does not settle` |
| S8 | 1 | X1 keeps its recorded hash and its row is not dated; the base wrote an intermediate hash and dated it |
| D4 (S9) | 1 | the narrowed run names B's non-citation coordinate and exits 1 |
| unexplained | 0 | |

**Mutations, executed** (`bin/mutation-check`, one at a time, file restored
and hash-compared each time):

| Mutation | Cases | Verdict |
|---|---|---|
| judge ledger coordinates against the disk | S2, S4, S5, #772's | red, 5 |
| apply the plan after the first recomputation | S5 | red |
| record the first recomputation's hash | S7 | red, 4 of 6 trees |
| `on_a_cycle` finds no cycle | S6's downstream case | red |
| a pass leaves nothing at its bound | S6 | timed out at 60 s, no verdict: without it the passes never end |
| a coordinate left on a cycle and OK at the end is named | the two-row cycle | red (survived until that case was planted) |
| held coordinates ride no dated row | #785's rider case | red |
| a verdict is reused though its file moved | S2, S5, S7 | red, 2 |
| a BROKEN verdict is reused across rounds | the re-point case | red (survived until that case was planted) |
| D4: a coordinate never read OK before the run | S9 | red |
| `judge` gives a DRIFTED coordinate no hash | S3a, C8 | red, 7 |
| `judge` re-points a claim row | `test_a_claim_row_is_never_re_pointed` | red (survived until that case was planted) |
| a pure move dates its row | the row-points module | red, 3 |
| a left-whole row's move is not the run's leaving | #792's left-whole case | red |
| a held move rides an undated row into MOVES | #785's record case | red |
| a citation's re-stamp is a pact change | #772's record case | red |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `cited_first`, the walk loop, `first_old`, `still`, `walked_move`, `owed_moves`, `walked_outcome` | `reverify`'s recomputation, `plan_ledger` and `on_a_cycle`; released rows citing them take `Corrected ·` rows in phase 4 |
| `left_because` | `judge`'s detail; `seal/releases/0.18.3.md:6` takes a `Corrected ·` row |
| `citations_left` | `moved_and_left_out`, which reads every ledger coordinate; `seal/releases/0.18.2.md:86` takes a `Corrected ·` row |
| the held-coordinate loop's own reading of a place (`unplaced`) | `judge`'s verdict, read by `plan_ledger` |
| `test_the_walk_order_survives_a_self_citation_and_a_cycle` | its tree is `six_files`, read by S4 and S5 |
| `test_every_walk_sequence_hands_over_what_the_file_holds`, `test_every_walk_sequence_prints_what_the_file_holds` | S7, over the trees the module builds |
| `test_a_restamp_a_later_walk_leaves_is_a_move_and_then_broken` | S8, `test_a_coordinate_whose_statement_the_run_removes_is_left_at_its_hash` |
