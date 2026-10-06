# Survivors — `--reverify` computes once and judges in one place

This range removed the walk (`cited_first`, its revisits and the per-walk
fold), `left_because`, `current_hash` and `citations_left`, with the
docstrings and comments that described them, and reworded the sentences
that said how the run walked. `survivor-check --range e6d5a055..1f4d6cfc`
named 50 places sharing words with what it removed, and each is one of
three kinds, each judged below.

- **A record of past work.** Another work item's spec, plan, overview,
  phase, round or verifying pass, or a released ledger row, describing the
  tree at the commit it was written for. A released row is never edited
  under the freeze; the three whose claim this range makes false take a
  `Corrected ·` row in this item's fragment (`seal/releases/0.18.2.md:86`,
  `0.18.3.md:6`, `0.18.3.md:8`).
- **A sentence this range wrote or kept on purpose.** The new docstring,
  usage text and the test docstrings that still describe what the code does.
- **A test's own data.** Parameter ids and asserted strings that are still
  the words the code prints.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.18.2.md` | walks each ledger after every ledger of its list | released row E3, the 0.18.2 claim about `cited_first`; never edited under the freeze, and corrected by a `Corrected ·` row in this item's fragment |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md` | For each of the 36 sequences, the printed lines are the fold | the 0.18.3 item's spec, a record of the scenario it framed at its own commits |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check-2.md` | Two walks find the quoted hash gone and leave X1 | the 0.18.2 item's second verifying pass, a record of the walk it measured |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check-2.md` | The move that landed runs from the pre-run hash | the same pass, describing the fold `owed_moves` made at its commit (NAME NOT IN TREE) |
| `tests/test_a_row_points_by_content.py` | Three sentences this command printed, none of them true | round 7's history of three lines the base printed; still true as history, and the case still asserts the check's verdict |
| `tests/test_a_signatory_records_a_pact_change.py` | A coordinate no one place holds is recorded as | still true: a coordinate the run leaves is recorded BROKEN |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check.md` | The file keeps the first hash, so MOVES holds that move | the 0.18.2 item's verifying pass, a record of that commit's fold |
| `skills/evidence-check/scripts/evidence_check.py` | A `left` line claims no write, so it is printed here | this range's own docstring for `reverify`, true of the rewrite |
| `seal/releases/0.18.3.md` | prints each coordinate's `left` line once the walks end | released row A3, the claim about `walked_outcome`; corrected by a `Corrected ·` row in this item's fragment |
| `seal/releases/0.18.3.md` | a held one whose reading no longer resolves to one place | released row A1, the claim about the held-coordinate loop and `left_because`; corrected by a `Corrected ·` row in this item's fragment |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | named `left` in the check's own terms and handed MOVES a BROKEN part | the 0.18.3 item's closing memo, a record of its divergence table |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md` | A held coordinate no one place holds, on a row the run dates | the 0.18.3 item's spec, and still true: such a coordinate takes the verdict any other does |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | A held coordinate rides its row where the run dates that row | the 0.18.3 item's closing memo, and still true of `plan_ledger`'s riders |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | So no earlier walk of the same key can have left | the 0.18.3 item's verifying pass, a record of the walk it read |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | a file citing itself, beside what the run leaves | a parameter id of the kept case, which still builds that tree |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | a file citing itself | the same case's parameter ids, which still name its trees |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | a file citing itself, undated | the same case's parameter id |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | "a file citing itself" | the home-pin case's id for the sentence this range rewrote, still the sentence's subject |
| `tests/test_a_row_points_by_content.py` | keeping it would leave the re-anchored row DRIFTED | a test comment on the re-point's hash, which `repointed` still follows |
| `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/spec.md` | The hashes in the row are still rewritten where their anchors | the overflow item's spec, still true: an overflowing row's hashes are re-stamped |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check.md` | The fix keeps, per coordinate, the first old hash | the 0.18.2 item's verifying pass, a record of that fix |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check.md` | and whether the last walk left it BROKEN | a line of that pass's quoted diff |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/spec.md` | A run narrowed with `--ledger` may move a released | the 0.18.2 item's spec, still true, and the narrowed-run line still names it |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | S9 in the same spec forbids a line for left then unchanged | the 0.18.3 item's closing memo, quoting a docstring of its commit |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/plan.md` | The walked-file skip in | the 0.18.3 item's plan, a record; the skip itself survives in `moved_and_left_out` |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | two places holding a claim's minor hash is a tie the check calls BROKEN | still true, and the case asserts the check's sentence |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | --reverify at 1c3178a1 | executed output quoted as run at that commit |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | 2 places, none holding the recorded | a removed line in that pass's quoted diff |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/post-review-check.md` | 2 places, 2 holding the recorded | an added line in that pass's quoted diff, true of the commit it patched |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md` | it is re-pointed onto the one destination that reconstructs | the 0.18.3 item's spec, still true of `judge`'s destination |
| `tests/test_a_row_points_by_content.py` | was returned even when `blocked` was empty | `generic_units`' history, untouched by this range |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check.md` | A coordinate re-stamped on more than one walk | the 0.18.2 item's verifying pass, a record of that commit |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/plan.md` | keeps each coordinate's `left` line under the key its hash line | the 0.18.3 item's plan, a record |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md` | It rewrites the hash of every row whose anchor resolves | the 0.18.3 item's spec quoting the skill, whose sentence is still true |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md` | rewrite the hash of every resolvable row | the same spec quoting the usage text, still true |
| `skills/evidence-check/SKILL.md` | It rewrites the hash of every row whose anchor resolves | still true; the section was re-read and left (questions Q4) |
| `skills/evidence-check/scripts/evidence_check.py` | rewrite the hash of every resolvable row | the usage text, still true and extended by this range |
| `skills/evidence-check/scripts/evidence_check.py` | A citation is a ledger line no family grades | this range's docstring, true of the rewrite |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | judgment is about code coordinates: a citation is a ledger line | still true, and the case still passes |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/plan.md` | So a citation is right only when its cited file was walked | the 0.18.2 item's plan, a record of the order it chose |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check.md` | A coordinate one walk re-stamps and a later walk leaves | the 0.18.2 item's verifying pass, a record of the finding #801 fixed |
| `skills/evidence-check/scripts/evidence_check.py` | and a second run finds each the record's last word | `reverify_into`'s comment, untouched and still true |
| `seal/releases/0.18.0.md` | `skills/evidence-check/scripts/evidence_check.py#family_view@ | released row L1's grounds; `family_view` is unchanged by this range |
| `seal/releases/0.18.0.md` | a `Corrected ·` row supersedes the family of the row it cites | released row L1's claim, still true |
| `seal/releases/0.8.2.md` | The fourth is reading #177 as this row's falsification | a released row's history, unrelated to this range's subject |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | a coordinate is OK when one of its newest readings | the module docstring's S1, still true |
| `tests/test_a_released_row_is_read_again_in_a_fragment.py` | this run re-stamps the line it cites | the asserted line, whose words this range kept for a citation |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check.md` | moves are kept one per coordinate under the key | the 0.18.2 item's verifying pass, quoting a claim of that commit |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md` | a `left` line iff the last walk that was not | the 0.18.3 item's spec, a record of its scenario |
| `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/spec.md` | So a citation is hashed against the line the open plan will write | the 0.18.2 item's spec, a record, and still true of the rewrite |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md` | each coordinate's outcome is printed once, after the walks settle | the 0.18.3 item's spec, decision D2, a record of the walk it framed at its own commits |
| `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/plan.md` | printed once the walks end | the same item's plan row for D2, a record of the fold `walked_move` made at its commit (NAME NOT IN TREE) |
