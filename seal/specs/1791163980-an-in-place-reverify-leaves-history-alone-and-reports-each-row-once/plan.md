# Implementation Plan: an in-place `--reverify` leaves history alone and reports each row once

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-05 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

## Summary

The work is three edits to `skills/evidence-check/scripts/evidence_check.py`'s
in-place writer, one corrected sentence, and the records:

1. `reverify` leaves alone a code coordinate whose family already holds it, or
   whose family is superseded. It judges that once, before the first walk,
   with `family_view`'s own `held` and `superseded` (#785, D1).
2. `reverify` keeps each coordinate's `left` line under the key its hash line
   uses, and prints the folded outcome once the walks end (#792's comment, D2).
   `main`'s family `LEFT` line then names the `--ledger` remedy only where a
   file the run did not write is the reason, and otherwise says the run left
   the coordinate itself (#792, D3).
3. `docs/the-evidence-ledger.md`'s *dated note* names the `Checked` date, and
   its pin follows (#781, D4).

## Technical context

Read at `e5cede76` (this branch's routing commit, cut from `a3aa139a`).

- **Where the family-blind re-stamp happens.** `reverify`'s per-coordinate
  loop (`for m in ANCHOR_RE.finditer(unquoted(text))`) compares each
  coordinate's recorded hash with the code, and appends an edit and a
  `pending` move wherever they differ. It knows nothing of families.
  - Under the freeze, `main` calls it with the fragments only (`writable`).
  - Without the freeze, `main` calls it with every ledger.
  - The judgment D1 needs already exists: `family_view(paths, …)` returns
    `families`, `superseded` and `held`. It is keyed by root row, then by
    `coordinate_of(m)`.
  - The test D1 adds is one membership lookup per coordinate. The row is
    `(file_identity(ledger), line number)`, the line number is
    `bisect.bisect_right(starts, m.start())`, and the coordinate is
    `coordinate_of(m)`. A citation is not in `readings`, so it never matches.
- **Where the view's paths come from.** `main` builds `view = ledgers +
  default_patterns(root)` for `released_drift`. `reverify` builds the same set
  itself, before `cited_first` runs and while `PLANNED` is still empty, so it
  reads the files as they are on disk.
  - That costs one more `family_view` per run. A run already pays one in
    `released_drift`, and the scan cache can be shared where the code allows
    it. That is the work's choice.
- **Where the `left` lines are printed.** Six `say(...)` calls inside the
  loop. Each `left` that has a `pending` entry is folded into `parts` through
  `walked_move`. The two static reasons (*path escapes*, *not in any known
  checkout*) have no `pending` entry.
  - `say = quiet if repeat else print` keeps walk 0's lines and drops every
    later walk's.
  - D2 replaces the printing with a dict keyed by `key_at[m.start()]`, last
    walk wins, cleared by `still()` and by a landed move. It is printed after
    the walk loop and before the `report` closure is handed to `told`.
  - The fold is `walked_move`'s. The work either keeps the line beside the
    held state in `parts` (for citations too, which `parts` now skips), or
    keeps a second dict folded by the same function. Either way **one
    function decides both**, so the record and the lines cannot disagree.
- **Where `main` names the family.** The unfrozen arm calls
  `released_drift(ledgers, view, …)` after the walk, with the plan open, and
  prints one `LEFT` line per owed root with the `--ledger` clause hard-coded.
  - D3 needs, per owed coordinate: (i) whether a member reading of it that
    does not hold sits in a file outside `ledgers`, which comes from the view
    `released_drift` returns; and (ii) whether `reverify` left it on a member
    in a file it wrote, which comes from the new keyword list.
  - The undatable rows are already listed in `undatable`. The work decides
    whether they join the list or are read from it.
- **The 0.18.2 design D2 must not undo**, each held by a case:
  - `first_old`: one hash line per coordinate, from the hash before the run.
    Held by `test_one_unfrozen_run_names_each_coordinate_it_restamps_once`.
  - `owed_moves`: a move and then BROKEN at the hash the file holds. Held by
    `test_a_restamp_a_later_walk_leaves_is_a_move_and_then_broken`.
  - `still()`: left, then unchanged, records nothing. Held by
    `test_a_coordinate_left_and_then_read_unchanged_records_nothing`.
  - D3 of that item: a citation hands MOVES nothing.
  - The `told` gate: no write claimed before it lands.
  - The bounded re-walk (`cited_first`'s `bound`). Held by
    `test_the_walk_order_survives_a_self_citation_and_a_cycle`.
  - The walked-file skip in `citations_left`. Held by
    `test_one_unfrozen_run_names_a_citing_row_it_left_whole_once`.

**What breaks in six months.**

- **A second reader of the family rule.** Someone may add a reader that
  judges *held* its own way, for example by comparing dates in `reverify`.
  The in-place writer and `--strict` would then disagree on a tie or on a
  calendar-invalid date. The guard is that D1 reads `family_view`'s `held`
  and computes nothing of its own, and S3 is the case that fails.
- **A new `left` reason printed straight through `print`.** It would
  reintroduce walk 0's untaken-back line. S8 drives the unit that collects the
  lines, so a reason added outside it is not covered. The `reverify`
  docstring therefore says every `left` line goes through that unit.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| D1 judged live, against the open plan, at each coordinate | A re-stamp adds `--checked` to a row's dates, which can make it the newest reading mid-run. A drifted family's older member is then re-stamped or left depending on whether its file was walked before the newer member's. Same tree, two answers. | Rejected |
| **D1 judged once, before the first walk, with `family_view`'s `held` and `superseded`** | The pre-run view and the walk could disagree about a coordinate's spelling. They do not: both match `ANCHOR_RE` on `unquoted` text and key by `coordinate_of`. | **Chosen** |
| D1 also leaves an outranked member of a *drifted* family, re-stamping only the newest reading | The newest reading may sit in a released file under the freeze, or in a file the narrowing left out, so the run cannot write it. Then which member takes the re-read? That is a new rule, and the `--into` paragraph tells the reader to read every row citing a drifted coordinate. #785 asks only for a family that already holds. | Out of scope (spec §*Out*) |
| D1 without superseded families | Without the freeze, a superseded released row is still re-stamped and dated, though `--strict` judges none of its coordinates. That is the same false reading #785 names. `released_drift` already skips superseded families. | Rejected |
| D2 as a third pass that re-reads every coordinate after the walks and prints its state | It hashes every coordinate a third time and needs its own `left` reasons, which then drift from the walk's. | Rejected |
| D2 by printing every walk's `left` lines | This removes the missing later `left` but keeps walk 0's, so the run says a coordinate is both left and clean. | Rejected |
| **D2: the `left` lines folded under the hash line's key, by `walked_move`'s rule, and printed once the walks end** | The walk could meet a coordinate in an order other than the one it prints. The work prints in first-met order, as the hash lines do. | **Chosen** |
| D2's lines routed through `told` | A run that cannot record writes nothing, so it would also print no `left` line, though the run did leave those coordinates. A `left` line claims no write. | Rejected |
| D3 keyed on `args.ledger` (narrowed or not) | A `--ledger` naming every file is narrowed and writes everything, so the remedy is still false there. In a narrowed run whose coordinate the run left itself, the remedy is also false. | Rejected |
| **D3 keyed per coordinate on reasons (i) and (ii)** | A coordinate with neither reason found (questions Q3). The line then names no remedy, rather than a false one. | **Chosen** |
| #781 by writing a Notes trace in place | Owner's decision, 2026-10-05: the document is fixed, not the writer. | Rejected by the owner |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#785 (D1).** First S1 (with S6 as a parameter), S2 (narrowed and not), S3, S4 and S7, each seen red at the base, and S5 seen red under its mutation. Then the pre-walk family judgment in `reverify`, and D1's sentence in `reverify`'s docstring, the usage text, `skills/evidence-check/SKILL.md` §*Re-verifying is recomputing the hash*, and `docs/the-evidence-ledger.md` §*A released row is read again*. Each sentence is pinned and seen red with the sentence deleted. `docs/the-pact.md` §*A signatory records a pact change* is re-read, and edited only if a sentence there became false. | `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py tests/test_a_signatory_records_a_pact_change.py tests/test_evidence_check.py -q`; each new case red with the base's `evidence_check.py` swapped in | 5d2282bd |
| 2 | **#792 (D2, D3).** First S8, S9, S10 and S12, each seen red, and S11's assertion tightened. Then D2's collected `left` lines printed once from the shared fold, the new keyword list `main` reads, and D3's per-coordinate remedy clause. The *Without the row* paragraph gains the unnarrowed half. `reverify`'s docstring loses *a walk after the first names nothing the first one named* and says every `left` line goes through the fold. Pins follow, each seen red. | The phase 1 modules, plus `bin/mutation-check` on the units this phase adds | 9c7e0bf7 |
| 3 | **#781 (D4) and the records (D5).** The *dated note* sentence and its `RE_READ_SENTENCES` pin and comment, seen red with the old sentence restored. Then `survivor-check --range a3aa139a..HEAD`, with a `survivors.md` row for each place it reports that stays true. Then this item's fragment rows. Then `Re-read ·` rows through `bin/evidence-check --reverify --into seal/ledger/<this id>.md --checked <date>`, narrowed with `--ledger` to the files whose rows were read; each claim is read against the edit first. Then the `Corrected ·` row over `seal/releases/0.18.2.md:91`, and a `Corrected ·` row over any other released claim the edits made false. Then the `changelog.md` fragment. | `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_the_ledger_rules_have_one_home.py tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_a_folded_statement_names_what_enforces_it.py -q`; `bin/evidence-check --strict --ledger seal/ledger/<this id>.md .` exits 0 | |

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

- Phase 2 reads D1's skip: a left-alone coordinate has no `left` line and is
  no reason (ii). So phase 2 runs after phase 1.
- Phase 3's `Re-read ·` rows carry the final hashes of every unit phases 1
  and 2 edited, and of the ledger section D4 edits. So phase 3 runs last.
  Its `--reverify --into` is itself an in-place run over this item's
  fragment, so it runs on the code this item ships.

**The changelog fragment is not written once.** Phase 3 writes
`seal/specs/<this id>/changelog.md`. Any later fix pass that changes what the
run writes or prints updates that fragment in the same fix range (#797). The
fragment says what the run does at the branch's last commit, not at
phase 3's.

**Released rows these edits drift, counted at `e5cede76`**
(`git grep -c -F` over `seal/ledger.md` and `seal/releases/`, summed):

| Coordinate | Rows citing it |
|---|---|
| `evidence_check.py#reverify` | 40 |
| `evidence_check.py#main` | 35 |
| `docs/the-evidence-ledger.md`, the *read again* section | 18 |
| `tests/test_a_merge_cannot_silently_drop_a_correction.py#…` | 14 |
| `evidence_check.py#released_drift` | 13, only if phase 2 edits it |
| `evidence_check.py#family_view` | 9, only if edited |
| `skills/evidence-check/SKILL.md` §*Re-verifying* | 8 |

Rows citing several of these are counted once per coordinate, so the number
of rows owed a re-read is smaller than the sum. `--into` writes one row per
released row. Each claim is read before the date is typed, because the date
says it was (questions Q2).

## Operational impact

- **No migration and no new dependency.** A record written before this
  release keeps its hashes.
- **Output a person sees changes in four places:**
  - An in-place run re-stamps, dates and names fewer rows: none whose family
    already holds the coordinate, and none in a superseded family.
  - Without the freeze, a run narrowed to a released file whose family a
    fragment reading already holds now exits 0 where it exited 1.
  - A `left` line is printed once, for a coordinate the run actually left at
    the end.
  - The family `LEFT` line names `--ledger` only where a file the run did not
    write is the reason.
- **Sibling items (cut together from `release/v0.18.3` at `a3aa139a`):**
  - B (#790, #780) edits `hooks/worktree-guard.py` and `hooks/tokens.py`.
    No file in common.
  - C (#789) edits the broad gate. No file in common.
  - D (#797) adds a check that a fix range left the changelog fragment
    behind. If D lands first, this item's later fix passes are held to it,
    which the plan's changelog paragraph already asks for.
  - Every sibling writes `Re-read ·` rows into its own fragment. Two siblings
    re-reading one released row on one day tie, and a tie is a union, so
    neither falsifies the other.
  - Whichever squashes second merges the release branch in and re-runs
    `bin/evidence-check --strict` before re-sealing.
