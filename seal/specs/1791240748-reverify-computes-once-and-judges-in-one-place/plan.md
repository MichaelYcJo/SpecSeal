# Implementation Plan: `--reverify` computes once and judges in one place

<!-- seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

The work is one new function and one rewritten one in
`skills/evidence-check/scripts/evidence_check.py`, the documents that
describe them, and the records.

1. A judge — one function returning, for one coordinate, everything the three
   commands read: status, the check's detail, the places, which hold, the
   hash to write, the one provable destination. `classify`, `family_view`,
   `released_drift`, `reverify` and `reverify_into` all read it (spec D2,
   D3).
2. `reverify` rewritten around a plan computed whole: every code coordinate
   judged once from disk, every coordinate naming a planned ledger line
   judged against the plan until nothing changes, one write, MOVES as (hash
   before, hash after) (spec D1, D5). The narrowed-run `LEFT` line reads
   every ledger coordinate, not only citations (D4).
3. The sentences that described the walks, rewritten and re-pinned; the
   differential against the base script; this item's fragment, its
   `Corrected ·` rows and its changelog fragment (D6, D7).

## Technical context

Read at `6d763c40`; line numbers are that commit's.

- **Where the four judgments live today.** `classify` (`:1662-1808`) is the
  check's. `reverify`'s general path (`:3387-3540`) re-derives the places,
  with `if resurrected: places = []` at `:3407` where `classify` has `elif
  resurrected and not claim` at `:1738` — #809. The held-coordinate loop
  over `unplaced` (`:3597-3680`) is a third copy, and `current_hash`
  (`:3867-3888`) a fourth that returns `None` for any resurrected place.
  `left_because` (`:903-923`) words the reason a fifth way, answering
  `resurrected` before it counts places (#809's comment).
- **Where the order lives.** `cited_first` (`:3094-3149`) builds its graph
  from `row_citation` alone — #806. `reverify` walks `once` then `again` up
  to `bound` times (`walks()`, `:3280-3294`), and the per-walk bookkeeping
  (`first_old`, `parts`, `still`, `outcomes`, `walked`; `walked_move`,
  `owed_moves`, `walked_outcome` at `:3020-3063`) repairs the record and the
  lines after the fact. `citations_left` (`:3906-3978`) reads citing rows
  only, for the narrowed run.
- **What the plan mechanism already gives.** `PLANNED`, `read`, `put`,
  `apply_plan` (`:1074-1133`): `read(path)` answers from the open plan, so a
  coordinate judged while the plan is open is judged against planned text.
  That is the whole of the machinery D1's recomputation needs; the walk
  loop was using it one file at a time.
- **What stays as it is.** `left_alone` (`:3065-3092`, the #785 pre-run
  judgment), `family_view` (`:2407-2678`), `newest_hash` (`:3890-3904`),
  `released_drift` (`:3980-4066`, reading the judge), `why_still_drifted`
  and `still_drifted_line` (`:4068-4128`), `reverify_into` (`:4170-4361`,
  reading the judge's hash in place of `current_hash`), `record_pact_changes`
  (`:4506-4730`), and `main`'s reverify arm (`:5797-5967`): PLAN, RECORD,
  APPLY, `told`, the narrowed-run `LEFT` lines.
- **The shape of the recomputation (D1).** Partition the coordinates of the
  files to write: *static* where the named file's `planned_key` is not among
  the files to write, *dynamic* otherwise. Judge the static ones once, build
  the plan (edits, re-points, date cells, rows left whole), then: judge every
  dynamic coordinate against the current plan, rebuild the plan from static
  verdicts plus these, and repeat until the planned text of every file is
  unchanged from the previous round. Judging every dynamic coordinate
  against the *previous* round's plan, rather than against a plan being
  edited in file order, is what makes the result independent of file order
  (S4); the work may choose the other scheme if it proves the same
  property. A coordinate still moving at the bound is left at the hash the
  row held and named (S6). The date rule is applied inside each round,
  because a date cell written for one coordinate changes the line another
  one may quote.
- **The judge's shape (D2).** The sketch in the spec. Two things the shape
  has to carry that `classify` does not return today: the hash the
  coordinate holds now (what `current_hash` computed, including the claim's
  minor region and the unsure-with-claim case), and the one provable
  destination (what the general path recomputed through `content_matches`
  at `:3447`). `classify` already runs the scan for its detail, so the
  destination is a value it had and threw away.
- **The record (D5).** With one plan there is one hash per coordinate after
  the run. `pending`'s `(offset, coord, old, new)` entries, computed once
  from the final plan, are MOVES; `parts`, `walked_move` and `owed_moves`
  go. The citation skip and the `deferred`/`joined` rule for held
  coordinates stay.
- **The differential (D6).** The base script is
  `git show e6d5a055:skills/evidence-check/scripts/evidence_check.py`, saved
  to a scratch path. The suite's trees are reached by running the test
  modules' fixtures through both scripts: the cheapest route is a probe that
  imports the test module, builds each fixture tree once, copies it, runs
  one script in each copy, and diffs. The probe is `test_tmp_*`, run once,
  deleted (§7); its classified figures go in `phases/phase-N.md`.
- **Riders.** `evidence_check.py` carries a `# RIDER:` at `:185-210` on
  `ANCHOR_RE`'s path pattern; the rewrite does not touch that unit.

**What breaks in six months.**

- **A second judge.** Someone adds a branch to `reverify` that decides a
  place its own way — a fast path, a special case — and the two commands
  disagree again. The guard: every call site reads the judge, the `left`
  line is the judge's detail verbatim, and S7 fails where a recorded or
  printed hash is not the file's.
- **A coordinate read against the disk while the plan is open.** A new
  reader that opens the file directly instead of through `read` sees the
  pre-run text, and the result depends on order again. S4 is the case that
  fails.
- **A bound that silently stops.** A future edit to the bound that drops the
  `LEFT` line reintroduces the silent self-citation. S6 pins the line.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Patch: widen `cited_first` to every ledger coordinate (#806's checkbox) and align `reverify`'s unsure-claim branch with `classify` (#809's) | Leaves four judges, the AGAIN loop and its bookkeeping; the next instance of either class arrives in the next review chain, as #791, #792, #801 and #808 did. The owner delegated the decision and the orchestrator chose the rewrite. | Rejected |
| **One judge; every code coordinate judged once from disk; ledger coordinates recomputed against the plan until it settles; one write** | A row that never settles. Named and exit 1 (S6). | **Chosen** |
| Recompute by editing the plan in file order and re-walking (Gauss–Seidel) | Converges to the same fixed point where one exists, but a row that oscillates may settle on different text under different orders. If the work chooses it, S4 is the proof it must pass. | The work's (questions Q1) |
| A judge that returns the check's finding and a second function that says what `reverify` would do | Two readings of one coordinate again, one step removed. | Rejected |
| Keep `left_because` as a wording layer over the judge | The reason is wording, and wording is where #809's comment found the gap; the check's sentence is the sentence. | Rejected |
| Record a coordinate moved and then left at the intermediate hash (the old `owed_moves`) | There is no intermediate hash: nothing is written for a coordinate the plan leaves, so the file holds the recorded hash and the part is `(recorded, None)`. Recording a hash no file holds is #791's defect. | Rejected |
| Leave an unsettled row silently for `--strict`, as `cited_first` did | `--reverify` exits 0 over a row `--strict` refuses; the silence every round of this lineage reported. | Rejected |
| A permanent differential test reading the base script through `git show` | The base is wrong in the named cells, so the test carries an allowlist of differences that grows with every later fix, and pins an implementation nobody maintains. The suite is the standing differential. | Rejected; a probe with recorded figures instead |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The judge, read by the check (D2, D3).** The judge function with the full verdict; `classify` as its finding; `family_view.grade`, `check_text` and `released_drift` reading it; `reverify_into` reading the judge's hash in place of `current_hash` (removed). S3a's `--into` arm and S3b's check-side wording seen red, then green. D6's probes 1 and 2 run for `--strict` alone: byte-identical. | `bin/test tests/test_a_row_points_by_content.py tests/test_a_released_row_is_read_again_in_a_fragment.py tests/test_evidence_check.py tests/test_a_signatory_records_a_pact_change.py -q`; the probe's figures in `phases/phase-1.md` | |
| 2 | **`reverify` rewritten (D1, D4, D5).** First S2, S3a in place, S3b, S3c, S4, S5, S6, S7, S8, S9 planted and seen red at the base or under their mutations; the walk-order cases removed or rewritten as the spec's table says; the `left`-word assertions rewritten (S11). Then the recomputation, one write, MOVES from the final plan, the `left` lines from the judge, D4's reader of every ledger coordinate in files left out; `cited_first`, the walk loop, `first_old`, `still`, `walked_move`, `owed_moves`, `walked_outcome`, `left_because`, the `unplaced` copy and `citations_left` removed. `reverify`'s docstring and the usage text rewritten (D1, D5). D6's probe 2 for `--reverify`, every difference classified. | the phase 1 modules, `tests/test_two_branches_re_read_one_released_row.py`, `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`, `tests/test_a_rider_reaches_its_file.py`; `bin/mutation-check` on the judge and the recomputation; the probe's classification in `phases/phase-2.md` | |
| 3 | **The documents (S12, §14).** `docs/the-evidence-ledger.md`'s fifth item and *left*-reasons sentence; `docs/the-pact.md`'s in-place sentence (one sentence, see *Overlap with #822*); `skills/evidence-check/SKILL.md` §*Re-verifying* re-read and edited only where false; every pin updated and seen red with its sentence deleted or reverted. | `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py tests/test_a_signatory_records_a_pact_change.py tests/test_the_ledger_rules_have_one_home.py tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_docs_line_wrap.py -q` | |
| 4 | **The records (D6 probe 3, D7, S13–S15).** `survivor-check --range e6d5a055..HEAD` with a `survivors.md` row per place that stays true. This item's fragment through `bin/evidence-check --reverify --into seal/ledger/<this id>.md --checked <date>`, each cited claim read before the date is typed; the same run through the base script in a scratch copy, the two fragments and outputs diffed and classified. The `Corrected ·` rows of D7. The `changelog.md` fragment. | `bin/evidence-check --strict .` exits 0; `bin/test tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_a_folded_statement_names_what_enforces_it.py tests/test_the_ledger_fragments_fold_at_release.py -q`; the classification in `phases/phase-4.md` | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

**Order is not free.**

- Phase 1 is a refactor of the check with `--strict` byte-identical, so its
  differential is the cheap one and runs before anything behavioural moves.
  Its one behaviour change (`--into` on C8) is #809's own case.
- Phase 2 needs the judge's hash and destination, so it follows phase 1.
- Phase 3's sentences describe phase 2's code, and `tests/test_no_passage_is_pasted_into_a_second_file.py`
  reads them against the whole tree, so the words are settled after the code.
- Phase 4's `Re-read ·` and `Corrected ·` rows carry the final hashes of every
  unit phases 1–3 edited and of the two document sections, so it runs last.
  Its `--reverify --into` runs on the code this item ships, and is the third
  measurement of the differential.

**The changelog fragment is not written once.** Phase 4 writes
`seal/specs/<this id>/changelog.md`. Any later fix pass that changes what the
run writes or prints updates that fragment in the same fix range; the fragment
says what the run does at the branch's last commit.

**Released rows these edits drift, counted at `6d763c40`** (`grep -c` over
`seal/ledger.md` and `seal/releases/*.md`):

| Coordinate | Rows citing it | What they take |
|---|---|---|
| `evidence_check.py#reverify` | 62 | `Re-read ·` |
| `evidence_check.py#main` | 47 | `Re-read ·`, only if `main` is edited (D4's wiring may touch it) |
| `evidence_check.py#reverify_into` | 18 | `Re-read ·` |
| `evidence_check.py#classify` | 15 | `Re-read ·` |
| `evidence_check.py#check_text` | 14 | `Re-read ·`, only if edited |
| `evidence_check.py#released_drift` | 13 | `Re-read ·` |
| `evidence_check.py#family_view` | 9 | `Re-read ·`, only if edited |
| `docs/the-evidence-ledger.md#"## A released row is read again in the branch's fragment"` | 18 (#801's count) | `Re-read ·` |
| `docs/the-pact.md#"## A signatory records a pact change"` | not counted; the work measures it (questions Q3) | `Re-read ·` |
| `#current_hash` (0.18.0:24, 0.18.1:417), `#cited_first` and `#citations_left` (0.18.2:86, :90), `#left_because` (0.18.3:6), `#walked_outcome` (0.18.3:8) | 6 rows | `Corrected ·` |
| `seal/releases/0.4.0.md:59`, *never writes onto a place the declaration rule is unsure of* | 1 row | `Corrected ·`, narrowing the claim to a row with no claim |

Rows citing several of these are counted once per coordinate, so the number
of rows owed a re-read is smaller than the sum. `--into` writes one row per
released row. Each claim is read before the date is typed, because the date
says it was.

## Overlap with #822

`#822` (branch `feat/822-a-repository-that-keeps-a-pact-is-a-signer`) renames
the pact word `signatory` → `signer` across `docs/the-pact.md`,
`hooks/config.py`, `skills/evidence-check/scripts/pact_check.py`,
`skills/code-review/scripts/chain_check.py`, `templates/pact.md`,
`templates/pact-review.md`, and renames four test files, among them
`tests/test_a_signatory_records_a_pact_change.py` →
`tests/test_a_signer_records_a_pact_change.py`. Read from its working tree on
2026-10-06; the branch was not yet committed past its frame.

This item does not plan that rename, and keeps the rebase mechanical:

| File both touch | This item's edit | How the rebase goes |
|---|---|---|
| `docs/the-pact.md` | one sentence in §*A signatory records a pact change* (the in-place move clause) | #822 changes words on many lines of that section; this item changes one sentence's content. Git merges them where the lines differ; where the one sentence also carries the word, re-apply this item's sentence with #822's word. |
| `tests/test_a_signatory_records_a_pact_change.py` | new cases appended at the end (S3a's record arm, S3c), one parameter of `test_the_documents_say_what_the_writer_does` rewritten | A rename plus edits on both sides; `git rebase` follows the rename. Keep this item's additions at the file's end and in one parameter, so the hunks do not sit on lines #822 reworded. |
| `skills/evidence-check/scripts/evidence_check.py` | the units named above | #822 may rename `signatory` in this file's comments and docstrings (nine occurrences at `6d763c40`, in the module docstring and the pact-change section); this item's hunks are in `classify`, `reverify`, `reverify_into`, the walk units and the usage text. The usage text (`:77-80`) carries the word: if both edit it, re-apply this item's sentences with #822's word. |
| `skills/evidence-check/SKILL.md` | edited only if a sentence is false (phase 3) | #822 may rename the word in §*Re-verifying* (*In a signatory, the re-read also records a pact change*). Prefer no edit here; where one is needed, keep it to the sentence that is false. |

Whichever squashes second merges the release branch in and re-runs
`bin/evidence-check --strict .` before re-sealing: #822's heading rename
drifts every row citing `docs/the-pact.md#"## A signatory records a pact
change"`, which is #822's re-read to write, and this item's rows cite that
heading too.

## Operational impact

- **No migration and no new dependency.** A pact-change record written before
  this release keeps its hashes; the record's shape is unchanged.
- **Output a person sees changes in four places:**
  - Every `left` line of `--reverify` carries the check's own reason followed
    by ` — left`, where it carried `left_because`'s wording.
  - A row whose Code grounds quote its own line is named on a `LEFT` line and
    the run exits 1, where it was silent at exit 0.
  - A narrowed run names a non-citation ledger coordinate it moved in a file
    it did not write, where it named only a citation.
  - A claim on an unsure place is re-stamped and recorded as a move, where
    it was left and recorded `BROKEN` (#809); a tie among unsure places is
    named as the check names it.
- **One run where two were needed.** A tree that needed a second `--reverify`
  to clear a non-citation ledger coordinate (#806) clears in one.
- **Sibling work items cut from `release/v0.19.0` on 2026-10-06:** #823,
  #825, #826 (the orchestrator's redesign batch) and #822. Only #822 shares a
  file, as the section above says. Every sibling writes `Re-read ·` rows into
  its own fragment; two siblings re-reading one released row on one day tie,
  and a tie is a union.
