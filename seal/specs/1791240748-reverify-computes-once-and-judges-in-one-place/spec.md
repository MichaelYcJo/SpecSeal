# Feature Specification: `--reverify` computes once and judges in one place

<!-- seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issue #824, closing #806 and #809. All three were raised from the review
chains of the 0.18.x work items on `evidence-check --reverify`: #786 (work
item `1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move`)
chose the walk order and the bounded re-walk, and #801 (work item
`1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once`)
repaired what that order did to the run's record three rounds in a row. The
owner delegated the decision to the orchestrator, who decided to reimplement
the core rather than patch it; this frame settles what the reimplementation
must keep, what it may drop, and how it is shown to agree with the old one
wherever the old one was right.

Everything below was read at `6d763c40` (this branch's routing commit, cut
from `release/v0.19.0` at `e6d5a055`). Nothing was executed.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit*: *An anchor degrades to `DRIFTED`, never to `BROKEN`. Only the major level can be broken. A stale minor anchor widens to its unit and says re-read* | Decides #809 (D3 below). A claim row whose only place is one the declaration rule is unsure of is a minor-level question, so the check's `DRIFTED` is the ratified verdict and `--reverify` acts on it: it re-stamps the minor region's hash where that region is found, and leaves the row where the region is gone. `tests/test_a_row_points_by_content.py::test_a_stale_claim_on_an_unsure_place_drifts_rather_than_breaking` already pins the check's half (round 8, 🔴 A). |
| The same section: *A row whose anchor a change removes is `REMOVED`, not re-pointed … Under the freeze a released row is never removed: a `Corrected ·` row retires it, or re-points a moved one* | Decides what this item's records owe for the released rows anchored on the units it removes (`cited_first`, `walked_move`, `owed_moves`, `walked_outcome`, `left_because`, `current_hash`, `citations_left`): each is a `Corrected ·` row in this item's fragment, never an edit to the release file (D7). |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, the family paragraph, the `--into` paragraph and the *Without the row* paragraph | The behaviour contract the rewrite must keep: one `Re-read ·` row per released row, `--checked` dating every row whose hash moves once, a held coordinate left where it stands (#785), a narrowed run naming by its root each family it could not clear and the remedy per coordinate (#792), `--into` refusing a stale `--checked` and still recording the moves (#746). Enumerated under *What must survive*. |
| The same section, *Five things `--reverify` leaves at exit 0 while `--strict` exits 2*, fifth item: *one run over every ledger re-stamps a released row and every citation of it that it moves, because it walks a cited file before every file citing it (#772). A release file citing a row of itself, which a second fold writes, is walked again until it settles.* | States the mechanism this item removes. The sentence changes to state the new one — every ledger coordinate, citation or not, is hashed against the text the run will write — and its pin in `tests/test_a_released_row_is_read_again_in_a_fragment.py::test_the_home_names_each_thing_no_re_read_clears` follows (§14). The fifth item's *freeze* half and the narrowed-run sentence stay true. |
| The same paragraph: *A `left` line names why: a path outside the repository or any known checkout, a file the run could not read, no one place holding the unit, or a quoted statement its file no longer has.* | A `left` line now carries the check's own reason (D2), and a ledger coordinate that never settles is a new reason. The sentence gains it and its pin (`test_the_documents_say_each_outcome_is_printed_once`, id *the home: every left reason*) follows. |
| `docs/the-pact.md` §*A signatory records a pact change*: *A re-stamp in place records each row's move from that row's own hash, one move per coordinate however many walks re-stamp it, and BROKEN after it at the hash it holds where a later walk leaves it (#791). A move whose two hashes agree is no move and is not recorded (#774).* | The record's contract, kept: a move is the pair (hash before the run, hash after it), one per coordinate, from the row's own hash in place and from the newest reading's under `--into`. The clause about walks is rewritten to say that, and its pin in `tests/test_a_signatory_records_a_pact_change.py::test_the_documents_say_what_the_writer_does` (id *the pact: an in-place move starts at the row's own hash*) follows. The same section's *`BROKEN` where the re-read leaves it because no one place holds it — its unit, its file or its quoted statement gone* is the definition of the record's `BROKEN`: it is the pact's word for *left by the re-read*, and not the check's status word (D3). |
| `docs/the-pact.md`, the same section: *The run records first and re-stamps after* and *A line saying the run wrote a ledger file prints only once that file is written* | Unchanged by this item, and the rewrite is held to both: the plan is computed whole, the record is written from it, and only then is the plan applied; every line claiming a write stays in `told`. |
| `docs/the-pact.md` §*A signatory records a pact change*: *The hash is a code coordinate's: a citing row's citation of a released row is a ledger line, so its re-stamp records nothing (#772)* | D3 of the 0.18.2 item, kept: a citation hands MOVES nothing. A non-citation ledger coordinate — one that names a ledger line without being the row's citation — is code under the row as far as the record is concerned, as `test_a_ledger_coordinate_restamped_on_two_walks_is_one_move` already holds, and it keeps recording one move. |
| `seal/config.md`, `Ledger frozen from \| 1790993141` | This repository's own re-reads go into this item's fragment through `--into`; a released row whose cited unit this item removes takes a `Corrected ·` row. The run that writes them is the first real use of the rewritten command on this repository's ledger, and it is also half of the differential check (D6). |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended*; `skills/implement/SKILL.md` §1 | Every judgment the tree could answer is answered here, with the grounds beside it, and `questions.md` holds the residue. The owner's and the orchestrator's decisions are recorded as answered. |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class each defect belongs to is enumerated below. Every sentence a person reads that changes is pinned in the same commit, and every new case is seen red before it is committed. |

**Two departures from the issues, decided from the tree.**

- #806's checkbox asks `cited_first` to order a file after every file whose
  lines any of its coordinates name. #824 supersedes that: there is no order
  to fix once no file is walked. The case #806 asks for is still planted
  (S2), red at the base, and it is green by construction rather than by a
  wider sort.
- #809's checkbox asks which verdict is right. The tree answers it: the
  check's. The policy sentence above has said since 0.4.0 that only the major
  level can be broken, and round 8 of that item pinned a claim on an unsure
  place as `DRIFTED`. The round-6 rule *`--reverify` never writes onto a
  place the declaration rule is unsure of* (`seal/releases/0.4.0.md:59`) was
  written for a row with no claim, where the recorded hash is the unit's own
  and can tell a declaration from a call; a claim row's hash is of a
  statement the row's author pointed at inside the place, so re-hashing that
  statement writes onto nothing the author did not already choose. The 0.4.0
  row's claim is narrowed to the major level by a `Corrected ·` row (D7).

## Scope

### In

**D1 (#806): every coordinate is judged once, and nothing moves between
judgments.** Code does not change during a run, so each coordinate naming a
file outside the plan — code, a document, a ledger file the run does not
write — is judged once from the tree on disk. A coordinate naming a line of a
ledger file the run writes, whether it is the row's citation or not, is
judged against the text the plan holds for that file, and the plan is
recomputed until no planned text changes. Then the plan is written, once.
`cited_first`, the once/again split, the walk bound, `first_old`, `still`,
`walked_move`, `owed_moves` and `walked_outcome` have nothing left to do and
are removed, with the tests that drive them by name (listed under *Tests that
pin walk-order artefacts*).

- A coordinate that never settles — one whose hash is part of the line it
  names, so every recomputation moves it — is left at the hash the ledger
  held, named on a `LEFT` line that says it does not settle, and the run
  exits 1. The old code left such a row silently *for `--strict` to name*
  (`cited_first`'s docstring); the check calls that row `DRIFTED`, and a
  `--reverify` that exits 0 over a row the check will refuse is the silence
  every round of this lineage was about. The bound on the recomputation is
  the work's (questions Q1); what is fixed here is that reaching it names the
  rows that still move and nothing else.
- The run's result is a function of the tree, never of the order files are
  listed or glob-sorted. S4 states the test: any permutation of `--ledger`
  arguments writes the same bytes.

**D2: one judgment function, and the `left` lines speak in its words.** A
function — the sketch is `judge(m, root, maps, default_repo, scan_cache) ->
Verdict`, the name and shape being the work's — returns for one `ANCHOR_RE`
match everything the three commands read: the status (`OK`, `DRIFTED`,
`BROKEN`, `EXTERNAL`), the coordinate, the check's detail sentence, the
places found, which of them hold the recorded content, whether the only
places are ones the declaration rule is unsure of, the hash the coordinate
holds now where exactly one region can be hashed (`None` otherwise), and the
one provable destination where the content reconstructs elsewhere (`None`
otherwise).

- `check_text`, `family_view`'s `grade` and `released_drift` read the status,
  coordinate and detail — what `classify` returns today — so `--strict`'s
  output does not change (S1, the differential).
- `reverify` acts on the status: `OK` writes nothing; `DRIFTED` with a hash
  re-stamps; `BROKEN` with one provable destination re-points the row, and
  every other `BROKEN` or `EXTERNAL`, and a `DRIFTED` with no hash to write
  (a claim whose minor region is gone), is left and named `  <coordinate>
  <the check's detail> — left`. `left_because` is removed; the words are the
  check's, so the two commands cannot describe one row differently, which is
  the whole of #809's comment (S3b).
- `reverify_into` reads the same hash in place of `current_hash`, which is
  removed; `released_drift`'s `BROKEN` list is the judge's.
- The held-coordinate loop in `reverify` (the `unplaced` block) and the
  general path stop carrying their own copies of the place logic. The #785
  rules they implement — a held coordinate is left alone unless its row is
  dated for another coordinate, and then takes the judge's verdict — are
  kept, as one lookup before the judge is applied.

**D3 (#809): an unsure place with a claim is `DRIFTED`, and the record's
`BROKEN` means *left*.** Where a claim row's only place is one the declaration
rule is unsure of and the minor region is found there with another hash, the
judge says `DRIFTED` (as the check does today), `--reverify` re-stamps the
minor region's hash, and MOVES gets the move. Where the minor region is gone,
the judge says `DRIFTED` with no hash, `--reverify` leaves the row and names
it, and MOVES gets `(recorded hash, None)`, which the record writes as
`BROKEN` because that word, in `docs/the-pact.md`, means *the re-read leaves
it* and names the quoted statement gone as one of its cases. The two
commands then agree on every cell of round 3's *`unplaced` matrix*: C8 is
re-stamped, CU and CU0 are named `locator is ambiguous — 3 places …`, C7 and
C10 keep their verdicts and C10 keeps its heal.

**D4: a narrowed run names every ledger coordinate it moved and left out,
not only citations.** `citations_left` reads citing rows alone, which is
#806's hole one arm over: a non-citation coordinate in a file the narrowing
left out, naming a line the run re-stamps, drifts unnamed. The judge, asked
about every coordinate of the view's unwritten files that names a planned
file, against the plan and against the disk, names each one that was `OK`
and is `DRIFTED` now, on the `LEFT` line `citations_left` prints today, with
the `--ledger` remedy. The line's words are kept where the coordinate is a
citation; a non-citation coordinate gets the same line with *its coordinate*
in place of *its citation*.

**D5: MOVES is the pair (hash before the run, hash after it).** One part per
coordinate whose final hash differs from the recorded one, and `(recorded,
None)` for each the run leaves. There is no intermediate hash to record,
because none is written: a coordinate that moves and then is left in the old
design (`moved_then_left`) is simply left here, at the hash the row held, and
its part is `(recorded, None)` alone. `record_pact_changes` is untouched and
reads the same tuple shape.

**D6: the differential.** The rewrite is shown to agree with the old
implementation wherever the old one was right, in three measurements, each a
`test_tmp_*` probe (§7) run once and deleted, its figures written into the
phase record and `overview.md`:

1. `--strict .` over this repository's own ledger (`seal/ledger.md`, every
   `seal/releases/*.md`, every `seal/ledger/*.md`) at the base script and at
   the rewrite: byte-identical stdout and exit code (questions Q2).
2. The whole `--strict` and `--reverify` test corpus — every tree the suite
   builds — run through both scripts, with the two outputs and the two
   written trees diffed, every difference classified as one of: a `left`
   line's words (D2), a cell the issues name (#806, #809, the CU wording), a
   walk-order artefact (D1, D5), or unexplained. Unexplained is a finding.
3. `--reverify --into <this item's fragment> --checked <date>` run over this
   repository by both scripts in two scratch copies of the worktree, the
   fragments and the stdout diffed and every difference classified the same
   way. The copy the rewrite wrote is this item's fragment.

**D7: this item's records.** Its fragment `seal/ledger/<this item's id>.md`,
written through `--into`; a `Corrected ·` row for each released row whose
anchor this item removes, carrying every coordinate the claim still rests on
(`seal/releases/0.18.0.md:24` and `0.18.1.md:417` on `current_hash`;
`0.18.2.md:86` and `:90` on `cited_first` and `citations_left`; `0.18.3.md:6`
on `left_because`; `0.18.3.md:8` on `walked_outcome`); a `Corrected ·` row
for `seal/releases/0.4.0.md:59`, narrowing *never writes onto a place the
declaration rule is unsure of* to a row with no claim; the `changelog.md`
fragment; a `survivors.md` where `survivor-check` reports a place sharing
words with a removed sentence.

### What must survive — the behaviour contract

Every case in these modules stays green, with its assertion changed only
where *Tests that pin walk-order artefacts* or *Tests that pin a `left`
line's words* names it: `tests/test_a_row_points_by_content.py`,
`tests/test_a_released_row_is_read_again_in_a_fragment.py`,
`tests/test_a_signatory_records_a_pact_change.py`,
`tests/test_evidence_check.py`, `tests/test_two_branches_re_read_one_released_row.py`,
`tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`,
`tests/test_the_ledger_rules_have_one_home.py`,
`tests/test_a_merge_cannot_silently_drop_a_correction.py`,
`tests/test_pact_check.py`, `tests/test_a_pact_review_takes_a_pact_change.py`,
`tests/test_the_ledger_fragments_fold_at_release.py`,
`tests/test_the_root_migrates_itself.py`, `tests/test_a_rider_reaches_its_file.py`,
`tests/test_every_reader_ends_a_line_where_gfm_does.py`,
`tests/test_a_row_wider_than_its_header_is_named.py`,
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`,
`tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`. In
particular, by document:

| Rule | Where it is stated | What the rewrite keeps |
|---|---|---|
| A released file is never written under the freeze; `--into` writes one `Re-read ·` row per released row, dated `--checked`, carrying each drifted coordinate at its current hash | the `--into` paragraph | `reverify_into`'s row shape, its refusals (no citation, a stale `--checked`, a reading after today), its `LEFT` lines |
| `--checked` dates a row once however many coordinates moved; a moved row with no date cell is left whole and named; without `--checked` every moved row is named with its date | the `--into` paragraph; `skills/evidence-check/SKILL.md` §*Re-verifying* | the date rule, the left-whole rule, the dated and undated lists |
| A coordinate its family holds, or a superseded family carries, is left where it stands; on a row the run dates for another coordinate it takes the new hash too; a coordinate naming a line the run writes is never judged held | the family paragraph (#785); `seal/releases/0.18.3.md:6` | `left_alone`'s pre-run judgment from `family_view`, unchanged in substance |
| A narrowed run names, by its root, each family it could not clear, with the remedy per coordinate; the exit is 1 | *Without the row* (#792) | `released_drift` against the open plan, `why_still_drifted`, `still_drifted_line`; `stayed` is the set of coordinates the final plan leaves |
| The run records first and re-stamps after; a line claiming a write prints after the write; a run that cannot record writes no ledger file | `docs/the-pact.md`, the pact-change section | `PLANNED`, `told`, `apply_plan`, `record_pact_changes` and `main`'s three steps, unchanged |
| A citation hands MOVES nothing; a non-citation ledger coordinate hands it one move | the pact-change section (#772); `test_a_ledger_coordinate_restamped_on_two_walks_is_one_move` | the citation test by `row_citation`, as today |
| A move's old hash is the row's own in place and the newest reading's under `--into`; a part whose two hashes agree is dropped | the pact-change section (#774) | `newest_hash`, and `record_pact_changes`'s guard |
| A claim whose minor content two or more places hold is `BROKEN`, named with how many hold it; a row with no claim and one holding place is `OK` | `classify`, round 8 and #808, #810 | the judge's tie rule, word for word |
| A cross-repository row is never scanned locally; a BROKEN row is re-pointed only onto the one destination that reconstructs the recorded hash; a name alone is a labelled fact | `seal/releases/0.4.0.md`, the broken-row section | the judge carries the destination, and `reverify` reads it there |
| `MALFORMED`, `OVERFLOW` and an unreadable ledger are named and left, exit 1 | the refusal section | unchanged |
| A row inside a closed fence is an example and is never rewritten | §*A row inside a fence is an example* | matching in `unquoted(text)`, splicing in `text`, as today |

### Tests that pin walk-order artefacts, and what each becomes

All in `tests/test_a_released_row_is_read_again_in_a_fragment.py`.

| Test | What it pins | Change |
|---|---|---|
| `test_the_walk_order_survives_a_self_citation_and_a_cycle` | `cited_first`'s once/again/bound over a six-file tree | Removed with the unit. Its tree is kept as S5: one run leaves `--strict` at 0 and writes the same bytes under every ordering of the six paths. |
| `test_every_walk_sequence_hands_over_what_the_file_holds` (36 parameters) | the fold `walked_move`/`owed_moves` | Removed with the units. The property it guarded — the record's part is what the file holds — is S7, asserted over the trees the suite already builds rather than over a sequence that no longer exists. |
| `test_every_walk_sequence_prints_what_the_file_holds` (36 parameters) | `walked_outcome` | Removed with the unit; S7 covers the printed line the same way. |
| `test_a_restamp_a_later_walk_leaves_is_a_move_and_then_broken` | an intermediate hash written on walk 1 and left on walk 2: MOVES `[(before, held), (held, None)]`, the file holding `held` | The artefact. Rewritten: the file keeps X1's recorded hash, MOVES holds `[(before, None)]`, and the `left` line carries the check's *anchored statement is gone* reason. Red at the base. |
| `test_a_ledger_coordinate_restamped_on_two_walks_is_one_move` | one move for a coordinate the old design re-stamped twice | Kept; its docstring stops describing walks. |
| `test_a_coordinate_left_and_then_read_unchanged_records_nothing`, `test_a_left_line_a_later_walk_takes_back_is_not_printed` | a `left` a later walk took back | Kept as behaviour; the fixtures' docstrings stop describing walks. |
| `test_one_unfrozen_run_restamps_a_citation_no_order_places` | the again-list | Kept as behaviour; retitled for what it holds (a self-citing release file settles in one run). |
| `test_one_unfrozen_run_names_a_citing_row_it_left_whole_once` | `citations_left`'s walked-file skip | Kept; D4 keeps the skip of files the run wrote. |
| `test_reverifys_docstring_no_longer_says_a_later_walk_is_silent` | a docstring sentence | Kept; trivially true. |

### Tests that pin a `left` line's words (D2, §14)

Each assertion moves to the check's detail sentence followed by ` — left`,
and each is seen red against the old words.

- `tests/test_a_row_points_by_content.py::test_reverify_names_a_claim_two_places_hold_as_the_check_does` (`2 places, 2 holding the recorded content, a tie the recorded hash cannot break — left` → the check's `locator is ambiguous — 2 places: … (2 hold the recorded content, a tie it cannot break) — left`).
- `tests/test_a_row_points_by_content.py::test_reverify_never_contradicts_the_checks_verdict` part (b) (`no place — the check calls this row BROKEN` → `locator not found` with its scan hint); the assertion that *unsure* is absent stays.
- `tests/test_a_released_row_is_read_again_in_a_fragment.py::test_a_held_coordinate_with_two_places_on_a_dated_row_is_left_and_named` (`2 places, none holding the recorded content`).
- `tests/test_a_released_row_is_read_again_in_a_fragment.py::test_a_held_coordinate_with_an_unsure_place_on_a_dated_row_heals_to_its_destination` (`only a place the declaration rule is unsure of, and no destination is provable — left` → `the declaration rule is unsure of the only place it found, and none holds the recorded content — …; record one by hand if it is still the unit — left`).
- `tests/test_a_released_row_is_read_again_in_a_fragment.py::test_a_held_claim_two_places_tie_on_a_dated_row_is_left_and_named` (`3 places, 2 holding …`).
- `tests/test_a_signatory_records_a_pact_change.py`, the `_leave` helper's *the anchored statement is gone* arm, where it asserts the line.
- The released rows quoting the old words are records of what those commits printed and stay as they are; `survivor-check` names any that reads as a present claim (D7).

### The class each defect belongs to, enumerated (§12)

| Class | Instances | In scope |
|---|---|---|
| A coordinate hashed against text the run later changes | (a) a citation whose cited file walks later (#772, fixed by order); (b) a non-citation coordinate naming a line of a ledger walked later (#806, p10); (c) a coordinate naming a line two walks move (#791's one-move rule); (d) a coordinate moved on one walk and left on the next (`moved_then_left`); (e) a self-citing release file (the again-list); (f) a row citing its own line (never settles) | all: D1. (f) is named and exits 1 where it was silent |
| A narrowed run moving a line a file it does not write names | (i) a citation (`citations_left`, #772's S6); (ii) a non-citation coordinate (#806 one arm over) | (i) kept; (ii) D4 |
| One coordinate judged by two implementations | `classify` against: the general path of `reverify` (unsure place, `if resurrected:` vs `elif resurrected and not claim`, #809 C8); the `unplaced` loop (its own copy, round 3 🟡 1 and 🟡 2); `current_hash` (`resurrected or len(places) != 1` → `None`, so `--into` says *no one place to hash* for C8); `left_because` (the resurrected branch first, #809's comment CU/CU0) | all: D2, D3 |
| A statement of the mechanism a person reads | the home's fifth item and *left* reasons sentence; `reverify`'s docstring (*Every `left` line goes through `walked_outcome`*, *A file is walked after every file of LEDGERS it cites*); the usage text; the pact doc's *however many walks re-stamp it*; `skills/evidence-check/SKILL.md` §*Re-verifying* (read, says nothing about walks; edited only if a sentence there is false at the end) | each changed sentence pinned (§14) |
| A released row anchored on a unit this item removes | the six rows in D7 | `Corrected ·` rows |

### Out, each with its reason

- **The vendored `Pact notify` reader (`notify_may_be_always`,
  `names_a_pact`, `PACT_WORD`, `HTML_CELL`, `UNDER_A_HEADER` in
  `evidence_check.py`, copies of `hooks/config.py`'s).** Not the same shape
  as #809. That duplication is deliberate — a copy of the checker shipped
  without `hooks/` — and `tests/test_a_signatory_declares_its_pact.py` holds
  the two equal. #809's class is two readings of one judgment inside one
  file with nothing holding them equal. Removing the vendored copy is #759's
  lineage, and it is not this item's.
- **`hooks/config.py`, `pact_check.py`, `chain_check.py`.** Owned by the
  concurrent #822 (the `signatory` → `signer` rename). Not touched. See
  `plan.md` §*Overlap with #822*.
- **An outranked member of a drifted family.** #801 put it out of scope with
  the reason that re-stamping only the newest reading needs a rule for a
  reading the run cannot write. The judge changes nothing there.
- **`record_pact_changes` and the record's format.** The tuple shape and the
  file are unchanged; a record written before this release keeps its hashes.
- **The `--migrate` writer.** It has its own one-shot reader of an unsure
  place (`file_units`, the stamp), and `test_migrate_answers_an_unsure_place_the_way_reverify_does`
  holds that it leaves an unproven unsure place, as `--reverify` does for a
  row with no claim. D3 changes the claim case only.
- **`seal/follow-up.md`.** Read whole. Its row *`--reverify` re-stamps every
  row that cites it* is about several families citing one unit and is not
  this item's prerequisite. No row is removed and the shared file is not
  edited.
- **A permanent differential test.** The base script is wrong in the cells
  the issues name, so an equality test against it would carry an allowlist
  of differences that grows with every fix after this one, and it would pin
  an implementation nobody maintains. The suite is the permanent
  differential: every existing case was written against the old behaviour,
  and the spec names each one whose assertion changes. The probe runs once
  and its figures are recorded (D6).

## User scenarios & acceptance *(mandatory)*

Every case lands in `tests/test_a_released_row_is_read_again_in_a_fragment.py`
unless the row says otherwise. Each new case is seen red at the base
`e6d5a055`, where the defect is old, or under the mutation the row names, and
the handover says how (§15).

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1: the check is unchanged | **When** `--strict .` runs over this repository's ledger, and over every tree the suite builds, at the base and at the rewrite. **Then** stdout and the exit code are byte-identical. | D6's probes 1 and 2, executed; figures in the phase record |
| S2: #806's probe p10 | **Given** no freeze. Fragment B re-reads R1 and also names, by a quoted line, a row Q of `seal/releases/0.2.0.md`; `handler` and `other` both change; B's file sorts before Q's. **When** one `--reverify --checked …` runs over every ledger. **Then** exit 0, `--strict` exits 0, and a second run writes nothing. | New case, red at the base (exit 1, `--strict` 2, cleared by a second run) |
| S3a: #809's cell C8 | **Given** a `.cs` unit whose only place the declaration rule is unsure of, and a claim row quoting a statement inside it at a stale hash. **When** `--strict`, then `--reverify`, then in a signatory `--reverify --into`. **Then** the check says `DRIFTED`; in place, the row is re-stamped to the minor region's hash and MOVES holds `(old, new)`; under `--into` the `Re-read ·` row carries that hash; nothing records `BROKEN`. | New cases in this module and in `tests/test_a_signatory_records_a_pact_change.py`, red at the base (left, BROKEN part; `no one place to hash`) |
| S3b: #809's comment, CU and CU0 | **Given** a claim over three places the rule is unsure of, two holding the recorded content, and the same with none holding. **Then** `--reverify`'s `left` line carries the check's `locator is ambiguous — 3 places: … (2 hold …)` and `(none holds …)`, and the verdict is `BROKEN` on both sides. | New case, red at the base (`only a place the declaration rule is unsure of`) |
| S3c: the minor region gone on an unsure place | **Given** S3a's row with the quoted statement deleted. **Then** the check says `DRIFTED` (*anchored statement is gone*), `--reverify` leaves the row with that reason, and the record's row says `BROKEN`. | New case; green at the base for the verdicts and red for the words |
| S4: order independence | **Given** S2's tree and the six-file tree of the removed `cited_first` case. **When** `--reverify --checked … --ledger …` runs with the ledger paths in every permutation (the six-file tree sampled to a dozen orderings). **Then** every run writes the same bytes to every file and prints the same lines, up to the order of lines about different files. | New case, parametrised; red under the mutation *judge ledger coordinates against the disk* |
| S5: a self-citing release file settles in one run | The six-file tree. **Then** one unnarrowed run exits 0 and `--strict` exits 0. | The removed case's tree, kept as this case; green at the base, red under the mutation *apply the plan after the first recomputation* |
| S6: a row that never settles | **Given** a released row whose Code grounds quote its own line, hash included. **When** `--reverify`. **Then** the row's hash is as it was, a `LEFT` line names the row and says it does not settle, the exit is 1, and the other rows of the file are re-stamped. | New case, red at the base (silent, exit 0) |
| S7: the record and the lines are what the file holds | For every tree the module builds that calls `reverify` with MOVES, after the run: each MOVES part's new hash is the hash the file holds at that coordinate, or `None` where the line is unchanged and a `left` line names it; each printed `a -> b` has `b` in the file. | New case or fixture-level assertion driving the existing trees; red under the mutation *record the first recomputation's hash* |
| S8: `moved_then_left` | The fixture's tree. **Then** X1 keeps its recorded hash, MOVES holds `[(recorded, None)]` for it, the `left` line says the anchored statement is gone. | The rewritten case, red at the base |
| S9: D4, a narrowed run leaving a non-citation ledger coordinate out | **Given** S2's tree. **When** `--reverify --ledger <Q's file>`. **Then** a `LEFT` line names B's row and its coordinate, says the run re-stamps the line it names and the narrowing left B's file out, and the exit is 1. | New case, red at the base (silent) |
| S10: the citation form of D4 is unchanged | `test_a_narrowed_unfrozen_run_names_the_citation_it_moved_and_left` and `…names_no_citation_it_did_not_move` stay green. | Existing cases |
| S11: the `left` words | Each test under *Tests that pin a `left` line's words* asserts the check's sentence. | Rewritten assertions, red against the old words |
| S12: the documents say it | The home's fifth item and *left* reasons sentence, `reverify`'s docstring, the usage text and the pact doc's in-place sentence each state D1 and D5; each pin fails with its sentence deleted or reverted. | `test_the_home_names_each_thing_no_re_read_clears`, `test_the_documents_say_each_outcome_is_printed_once`, `test_the_documents_say_what_the_writer_does`, the usage pin; §15 by deletion |
| S13: the differential over the real ledger | D6's probe 3. **Then** every difference between the two fragments and the two outputs is classified, and none is unexplained. | Executed in phase 4; the classification in `phases/phase-4.md` and `overview.md` |
| S14: the ledger reads clean | `bin/evidence-check --strict .` exits 0 with this item's fragment in place; each `Corrected ·` row names the claim's surviving coordinates. | Executed, phase 4 |
| S15: hygiene | `tests/test_no_passage_is_pasted_into_a_second_file.py`, `tests/test_docs_line_wrap.py`, `tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py`, `tests/test_a_folded_statement_names_what_enforces_it.py` pass. | Run narrow, phase 4 |

## Data & interfaces

- **`reverify`'s positional signature and keyword arguments are unchanged**
  (`ledgers, root, maps, default_repo, checked, moves, told, left_by_run`).
  Its callers are `main`'s two arms and the tests.
- **`reverify_into`'s signature is unchanged.**
- **`classify(m, root, maps, default_repo, scan_cache) -> (status, coord,
  detail)` keeps its name and shape** as the judge's finding, so
  `check_text`, `family_view` and `released_drift` need no change beyond
  reading it; whether it stays a function or becomes an attribute of the
  verdict is the work's.
- **MOVES tuples keep their shape** `(ledger, row number, coordinate, old,
  new-or-None)`.
- **Removed, with no caller outside this file and the named tests:**
  `cited_first`, `walked_move`, `owed_moves`, `walked_outcome`,
  `left_because`, `current_hash`. `citations_left` is replaced by D4's
  reader (its name is the work's). Nothing under `.github/scripts/`,
  `hooks/` or another skill imports any of them (read: the importers call
  `check_ledger`, `ledger_families`, `migrate`, `display_name`,
  `old_format_rows`, `resolve_unit`, `content_hash`, `read`, `unquoted`).
- **Printed lines.** The hash line `  <coord>  <old> -> <new>`, the re-point
  line `  <coord> -> <dest>  (identical content)`, the count line, the dated
  and undated lists, the `LEFT` lines for `MALFORMED`, `OVERFLOW`,
  `undatable` and `ledger unreadable`, and `reverify_into`'s lines keep their
  words. The `left` lines take the check's detail (D2). One `LEFT` line is
  new (S6). D4's line reuses `citations_left`'s words.
- **No migration, no new dependency, no record format change.**

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

Framed 2026-10-06 by framer, before the build.
