# Implementation Plan: the survivor sweep reads removed and moved text as a correction (#603, #591, #592)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-25 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

Three changes to `skills/code-review/scripts/survivor_check.py#corrected` and
`#paired_across_paths`, in dependency order:

1. **#592.** The cross-path pairing chooses the departure a key's arrival pairs
   with by path affinity. Today it takes the first in path order.
2. **#591.** A retired directory's sentences take part in the pairing and
   leave the range after it. Today they leave before it.
3. **#603.** A ledger row the range removed, where an anchor resolved at `a`
   and does not at `b`, leaves the removed wording after the pairing, the way
   step 2's retired side does.

Step 2 needs step 1: once retired departures compete for arrivals, the choice
between two departures decides the verdict, not just the printed coordinate.
Step 3 reuses step 2's order: pair everything, then drop the departures that
take an exit.

## Technical context

The code this builds on, by unit. Read these before the phase that touches
them. The spec's *judgments* section says why each was chosen.

- `survivor_check.py#corrected`. It builds the path list and filters it with
  `records_a_past_state` and `a_gathered_fragment`. It then drops
  `retired_directories` from `paths` **before** reading any blob. Then comes
  the per-path loop (`gone`, `fresh`, the `CHANGELOG.md` arm with `moved`,
  `held` and `split`), and after the loop one call to `paired_across_paths`.
  Step 2 changes the drop: the retired paths are read at `a` and join `gone`,
  and after the pairing every departure under a retired directory is dropped.
  A retired directory is gone at `b`, so it adds nothing to `fresh`.
- `survivor_check.py#paired_across_paths`. It is pure over `(gone, fresh)`
  and counts one for one in both directions. Its docstring's last paragraph
  says why `wanted` can only grow. That argument still holds, and the new
  docstring keeps it.
- `survivor_check.py#retired_directories` and `#reader`. `reader()` is the
  pattern for loading a sibling by path and refusing with exit 2 when it is
  missing. Step 3 loads `skills/evidence-check/scripts/evidence_check.py`
  the same way, **only when the range's path list holds a ledger file**, as
  `retired_directories` loads only when it has a candidate.
  `tests/test_unverified_rows_close.py#test_every_reader_of_a_retirement_calls_the_one_predicate`
  pins that the module still calls `retired_by_rule`.
- `survivor_check.py#gathered_fragments`. This is the pattern for reading a
  line through `unverified_check.py#live_lines`. Step 3 reads a ledger row
  the same way, so a row in a fence or an HTML comment is never a row.
- `evidence_check.py#ANCHOR_RE` finds a row's anchors (`path`, `locator`).
  `evidence_check.py#resolve_unit(path, locator, text)` answers
  `(places, resurrected)` for a blob's text. "Resolves" means `places` is
  non-empty. Several places is still "resolves", which is the direction that
  keeps a row measured. `evidence_check.py#default_patterns` names the four
  ledger locations. The sweep reads git paths, not the disk, so it spells the
  four as path shapes, and a case holds the spelling against
  `default_patterns`' tails.
- `Sentence.line` is the line the sentence starts on in the blob it was read
  from. Step 3 keys the removed rows by `(path, line at a)`. The phase checks
  the base (1-based `enumerate` matched in the framer's probe) with a case
  rather than trusting this sentence.
- Tests: `tests/test_a_corrected_sentence_survives_elsewhere.py`. Helpers:
  `build`, `run`, `over`, `resolves`, `FOUND`, `REPAIRED`, `FILLER`,
  `MORE_FILLER`. #517's block is `retired_range` and its cases, and #563's
  block is `test_a_file_moved_whole_still_reports_the_quote_it_carried`
  through `test_a_copy_written_beyond_the_ones_moved_is_the_ranges_writing`.
  `RELEASE_RANGES` pins four real ranges' reported coordinates. A real-commit
  case skips when its commit is absent, and `test_the_measured_commits_are_still_here`
  is the one that fails instead.
- **A verbatim copy scores at most 1.0** (the `FILLER` comment in the test
  file). Every "is reported" case therefore needs the correction to REWORD
  the sentence (`FOUND` → `REPAIRED`), so the source splits into two runs.
- `docs/review-chain-spec.md` is **962 lines against a ceiling of 1000**
  (`seal/config.md`, `Document line ceiling`), and `fold-check` enforces it.
  The three phases share 38 lines. The two statements this work edits are
  §*What the sweep reads, and what it counts as written*. Their
  `Enforced by:` lines must name targets that resolve to a `def` (fold-check's
  shape rule).
- Tests that read `docs/review-chain-spec.md`: `git grep -l review-chain-spec -- tests/`
  (conftest's `review_chain_text`, line wrap, one-word-one-meaning, room for
  the next fold, and others). A phase that edits the document runs the
  modules this names that read the edited section, plus
  `bin/fold-check`.

**What breaks in six months:**

- **#592.** A range that both corrects a sentence in a file AND moves a large
  share of that same file's other sentences to the arrival's path. The
  correction's path then has the higher affinity, and the move's departure
  stays as the source. The verdict and the score do not change; only the
  `corrected` coordinate names the moved file. The case pinning S1 names the
  shape the rule serves, so a reader meeting this one can see it is the
  other one.
- **#603.** A row retracted because its claim was false, in the same range
  that happens to remove one of its anchors. Its cells take the exit, and a
  document still stating the false claim is not reported. This is the silent
  direction. It is bounded by the ledger's own rules: a false claim is
  corrected in place with a `Corrected <date>` note, never removed
  (`CLAUDE.md` §*a change writes fragments*). And `evidence-check` refuses a
  BROKEN row a branch leaves standing, so condition (c) sees only rows a
  person removed.
- **#591.** None beyond #563's own: a larger `wanted` can merge two runs into
  one, which `paired_across_paths`' docstring already states.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #603: every ledger row line the range removed takes the exit | A row corrected in place is a removed line plus an added one, so its old claim leaves the removed wording. That is the one ledger act that IS a correction, and every document still stating the false claim goes silent | Rejected: silent direction |
| #603: the row takes the exit only when EVERY anchor left | Measured on `58629718^..58629718`: the three removed rows kept 4 of 7, 4 of 7 and 1 of 4 anchors live, so none qualifies and all 8 places are still reported. It does not fix the issue's own instance, and `docs/the-evidence-ledger.md` permits a removal that keeps a live anchor as the owner's choice | Rejected: measured to fix nothing |
| #603: an anchor "left" when its FILE is absent at `b` | `seal/releases/0.15.1.md` S1's anchors left `tests/test_a_document_has_room_for_the_next_fold.py`, and the file stayed. Two of the 8 places come from that row | Rejected: misses the measured shape |
| #603: key the exit on a `REMOVED` note in the ledger file's comment | No rule requires the note, and its wording is free prose. A convention the sweep reads and nobody is told to write is a list by another name | Rejected |
| #603: print a count of rows that took the exit | A new report line nobody asked for, in a patch release that adds no report section. The retired-directory exit prints nothing either | Rejected; open for a design release |
| **#603: a live ledger row, removed, with at least one anchor resolving at `a` and not at `b`, drops out after the pairing** | Six months: see *What breaks* | **Chosen.** Measured: 3 of 9 removed row lines qualify, exactly the three the range's notes call REMOVED; survivors go from 8 to 0 |
| #591: close as unreached (measured: no effect on #581's range) | The class stays open wherever a fold carries a sentence verbatim, and step 3 needs the same pair-then-drop order anyway | Rejected |
| #591: hold any `docs/` sentence whose key left a retired spec, with no count | Holds copies beyond the ones moved, which #563's M7 case (`test_a_copy_written_beyond_the_ones_moved_is_the_ranges_writing`) already showed is the range's own writing | Rejected |
| **#591: retired paths join `gone` for the pairing and are dropped after it** | See *What breaks* | **Chosen** |
| #592: prefer the departure from a path gone at `b`, as the primary rule | A document split into two files that both remain has no departure gone at `b`, so the tie falls back to path order: #592 again | Rejected as primary; kept as the first tie-break |
| #592: report every departure of the key on the `corrected` line | Changes the report's shape, and every departure but one is wrong | Rejected |
| **#592: affinity (distinct keys shared by the departure path and the arrival path), then gone at `b`, then path order** | See *What breaks* | **Chosen** |

## Phases

Every phase owes, in its own commit (contract §14): the code, the new cases
seen red first (§15, with how each was shown red written in
`phases/phase-N.md`), the module docstring's matching paragraph, the
`docs/review-chain-spec.md` sentence it makes true, and its ledger rows.
Rows go in `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md`.
Drifted rows in `seal/releases/*.md` are re-read and re-stamped there, and
`bin/evidence-check` names them. Every phase also states CONTRIBUTING's four
items in its phase record: the red test, the failure direction, the prompt
budget (0: the sweep asks nobody anything) and the platform note (pure text
over git blobs; `read_blobs` already normalises CRLF; paths come from git
with `/`).

Narrow runs only (contract §2): the test module, and the modules named in
*Technical context* for the units a phase touches. The full suite, the
repository-wide lint and the typecheck are the sealer's, once.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 · #592: a move pairs with its own origin | `paired_across_paths` orders each key's departures by affinity to the arrival's path, then by gone at `b`, then by path order. `corrected` passes it the paths present at `b`. The docstring says why. `docs/review-chain-spec.md`'s second statement gains the clause that the `corrected` coordinate names the correction, not the move. Failure direction: none on the verdict, since the key and so the n-grams are identical; only the printed coordinate moves | Spec S1 (red today: names `docs/m.md:3`), S2 (the moved file sorts first), S3 (one-sentence move). M6 and M7 (`test_a_move_holds_only_as_many_copies_as_it_carried`, `test_a_copy_written_beyond_the_ones_moved_is_the_ranges_writing`) stay green unedited. The whole module green. `RELEASE_RANGES` unchanged, or each moved coordinate explained (questions Q1) || `0de23540` |
| 2 · #591: a fold's verbatim text is held | In `corrected`, the retired directories' paths are read at `a` and their sentences join `gone` before `paired_across_paths`. After it, every departure under a retired directory is dropped. The module docstring's §*A retirement is out of the range* says the pairing runs first and why. `docs/review-chain-spec.md`'s second statement names a fold's verbatim text as a move. Failure direction: reports more, which is the cheaper mistake for a sweep whose silent failure is an unanswered finding | Spec S4 (red today: exit 0). S5, the #517 block unedited and green. S6: `survivor-check --range f673e3b1..8e13036c` and `--range 3c3f2342^..3c3f2342` at the phase's commit, output recorded in `phases/phase-2.md` against the framer's measurement (0 survivors, 44 removed). `tests/test_unverified_rows_close.py#test_every_reader_of_a_retirement_calls_the_one_predicate` green || `4910e445` |
| 3 · #603: a removed row's cells are not a correction | A predicate (named by the builder, a `def`, so `Enforced by:` can name it) returns the removed ledger rows of a range. A row qualifies when it is a live table row at `a` in a ledger path shape, its line is not in that file at `b`, and at least one `ANCHOR_RE` anchor in it resolves at `a` and not at `b` through `resolve_unit`. `evidence_check.py` is loaded by path only when the range holds a ledger path, and a missing sibling is exit 2 with a sentence. `corrected` drops those rows' departures after the pairing, beside step 2's drop. The module docstring's §*What is excluded* gains the paragraph. `docs/review-chain-spec.md`'s first statement gains the clause and its `Enforced by:` line the predicate. The changelog fragment `changelog.md`, one entry for all three issues. Failure direction: reports less. That is cheaper here because a removed row's claim went with its code, and the rules route a false claim to correction in place (*What breaks*) | Spec S7 (red today: exit 1), S8 (shown red against a mutation exiting every removed row line), S9 (shown red with condition (c) dropped), S10, S11, S12, and S13 over `58629718` (red today: 8 places). A case holding the four path shapes against `evidence_check.py#default_patterns`. A case for the missing-sibling refusal. The whole module green. `RELEASE_RANGES` re-run (Q1). `bin/evidence-check` clean, with drifted rows re-read. `bin/fold-check` clean over the edited statements | |

## Operational impact

- `survivor_check.py` now loads `skills/evidence-check/scripts/evidence_check.py`
  when a range touches a ledger file. It ships beside it under `skills/`, as
  `unverified_check.py` does, and a copy without it is refused with exit 2
  and a sentence saying which file is missing. This repository's workflow
  runs the sweep from the checkout (`.github/workflows/hygiene.yml`), and
  `templates/hygiene.yml` does not run the sweep.
- No new flag, exit code, environment variable or dependency.
- Work item E of this release edits `evidence_check.py` (#299). This work
  edits nothing there. If E renames `ANCHOR_RE` or `resolve_unit`, the release
  branch meets it, and the case that loads them goes red there.
