# Implementation Plan: one `--reverify` leaves the ledger clean and records only a real move

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

## Summary

The work is three edits to `skills/evidence-check/scripts/evidence_check.py`'s
re-read writer, plus the sentences and pins that describe it:

1. `reverify_into` records a move from the newest reading's hash, and
   `record_pact_changes` drops a part that did not move (#774).
2. The in-place walk visits a cited file before the files that cite it, so one
   unfrozen run leaves no citation drifted. A narrowed run names the citation
   it cannot reach (#772).
3. A citation re-stamp is not recorded as a pact change.

Then the trigger is completed where it is stated short, three copies are
pinned, the pact paragraph's `Enforced by:` line is updated, and the released
row about a Notes trace is corrected (#775).

## Technical context

Read at `33410fe7` (this branch's routing commit, cut from `94d7b2e0`):

- **Where the old hash comes from.** `released_drift` (`evidence_check.py`,
  `def released_drift`) keeps the released member's match for a coordinate
  whose newest reading is newer and holds other content. Its comment says so:
  *DRIFTED, or OK and outranked by a newer reading holding other content*.
  `reverify_into` then appends `m.group("hash")` as the old hash at four sites:
  - the refusal arm under `if stale is not None`;
  - the `new is None` arm;
  - the written arm;
  - the `for at, coord, detail, key, recorded in broken` loop.
- **Where the newest reading lives.** `family_view` already computes `newest`
  as `{root: {coord: (date, row)}}`. `later_reading` reads it, and treats a row
  outside every family as its own reading. D1 reads the same structure: from
  the row `newest` names, take the match whose `coordinate_of` equals the
  coordinate, and use its hash.
- **The guard's place.** In `record_pact_changes`, `parts =
  list(dict.fromkeys(coords))` is where a part with `old == new` is dropped. A
  group left empty adds no entry.
- **Why one run leaves a citation drifted.**
  - `main`'s unfrozen arm calls `reverify(ledgers, …)` with `PLANNED` open.
  - The ledgers come from `resolve_patterns`, which returns
    `sorted(out)`: `seal/ledger.md`, then `seal/ledger/*.md`, then
    `seal/releases/*.md`, with `0.10.0.md` before `0.9.0.md`.
  - `reverify` hashes a citation by `read()`, and `read()` answers from the
    open plan. So a citation is right only when its cited file was walked
    first.
  - A fragment is walked before the release it cites. Its citation is hashed
    against the old line, and then the release's re-stamp moves that line.
- **How the order is computed.** Each ledger's citing rows are found by
  `citing_verb` over `ledger_table_rows`. Each citation's file is the first
  coordinate's path, resolved as `place` resolves it. That gives a graph of
  file identities, sorted by Kahn's algorithm with ties in the given order. A
  cycle cannot be written legally: a citation into a fragment is `MALFORMED`,
  and a fold only cites older releases. If one appears anyway, the rest keep
  the given order, and `--strict` still reports the drift.
- **Where the narrowed `LEFT` goes.** `main` already prints
  `LEFT … still DRIFTED … run it without --ledger` after the unfrozen walk.
  D2's narrowed line sits beside it. The findings come from a `family_view`
  over the full view, read while the plan is still open: a citing row in a file
  outside `ledgers` whose citation is `DRIFTED` against a file the plan writes.
  A citation that was already drifted before the run is not this run's to name.
- **Which coordinate is the citation.** A citing row's citation is the first
  coordinate in its Code grounds (the usage text, and `citation_for`'s shape).
  D3 skips appending a move for that coordinate in `reverify`'s `pending`. The
  hash is still re-stamped.

**What breaks in six months.** Suppose a later writer appends a move whose old
hash is not the newest reading's, for example a third arm added to
`reverify_into`. The guard catches the `h → h` half of that mistake, but not a
wrong old hash that differs from the new one. S1's case is the pin for that
half, and the guard does not cover it. Separately, someone may drop D2's order
in favour of plain `sorted`; S5 is the case that fails then.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #774 as the ticket words it: keep the released member's hash and drop a part whose two hashes agree | P3's real move `h2 → h1` is never recorded. Code under a clause returns to a hash the pact repository last saw changed, and nothing is owed there. `docs/the-evidence-ledger.md` forbids this: *a pact change is never lost*. | Rejected. The guard is kept as a second line, not as the fix. |
| D1: old hash from the newest reading, plus the guard | The newest row may spell the coordinate with a minor anchor, and then the match lookup misses. Mitigation: fall back to the member's match and record a divergence row. | **Chosen** |
| #772 by a second full pass of `reverify` | The told reports and the `dated` lists print twice, and every coordinate is re-read twice. It also needs a stop rule. | Rejected |
| #772 by kind order: released files first, then fragments | Misses instance (ii): a release file citing an older release, unfrozen, with `0.10.0` before `0.9.0`. | Rejected |
| D2: dependency order within the one walk, plus the narrowed `LEFT` | A hand-written cycle falls back to the given order, which is the base's behaviour, still reported by `--strict` | **Chosen** |
| D3: record citation parts as today | Under `always`, a row whose only move is a citation re-stamp is recorded as a code change the pact repository is asked to review. Its released row's code move is already recorded on its own row. | Rejected |
| D4: paste round 3's text into `templates/config.md` | Shares a 15-word run with `docs/the-pact.md`, a pair `BASELINE` does not hold, so the ratchet fails. It would also be a third prose copy of the trigger. | Rejected. The template points at the home instead. |
| Fold the 0.18.1 hash churn into D2 | A different mechanism: family-blind in-place re-stamping of outranked members. The fix changes which rows the in-place writer touches and dates. | Out of scope (questions Q2) |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#774.** First, S1 (both arms), S2 and S3, each seen red at the base. Then D1 at the four append sites in `reverify_into`, and the guard in `record_pact_changes`. Then one sentence in `docs/the-pact.md` §*A signatory records a pact change* saying which hash a recorded move starts from, pinned through `test_the_documents_say_what_the_writer_does`. The paragraph's `Enforced by:` line gains the two #746 cases and S1's case (D6). | `bin/test tests/test_a_signatory_records_a_pact_change.py tests/test_a_released_row_is_read_again_in_a_fragment.py tests/test_a_folded_statement_names_what_enforces_it.py -q`; each new case red with the base's `evidence_check.py` swapped in | 1dea315c |
| 2 | **#772 and D3.** S4 (the pinned case rewritten), S5, S6 and S7, each seen red. Then D2's dependency order in `reverify`, the narrowed `LEFT` in `main`, and D3's skip of a citation's move. In `docs/the-evidence-ledger.md`, the fifth item's unfrozen sentence and the lead-in's *except where the last item says a second run clears it* are rewritten. Their pins in `test_the_home_names_each_thing_no_re_read_clears` move with them, and the *second run* parameter is replaced, not deleted. The usage and the skill are checked for a *second run* claim (none at framing). | the two pact and re-read modules above, plus `tests/test_evidence_check.py`; S4–S7 red at the base | 98f2651a |
| 3 | **#775's documents and this item's records.** D4: `templates/config.md`'s pointer is pinned, and the section comment is completed. D5: round 3's two paste-ready parameters, each seen red by deleting its sentence. D7: re-read 0.18.0:79 against `reverify_into`, `reverify` and the *Without the row* paragraph, then write the `Corrected ·` row. This item's fragment rows. `Re-read ·` rows via `--reverify --into seal/ledger/<id>.md --checked <date>`, narrowed to what was read. The `changelog.md` fragment. | `tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_the_ledger_rules_have_one_home.py tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py`; `bin/evidence-check --strict --ledger seal/ledger/<id>.md` exit 0 | |

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

**Phase 2 also runs one probe for questions Q2**, under §7: one file, run
once, then deleted. It builds a family with two fragment `Re-read ·` rows, the
older one outranked by the newer, which holds the current code. It runs
`--reverify --checked` without `--into` under a freeze, and reports whether
the older row is re-stamped while `--strict` reads it OK. The result goes in
`phases/phase-2.md` and in `overview.md` §*Not done*, so the orchestrator can
file an issue against a coordinate.

**Order is not free.** Phase 1 and phase 2 both edit `reverify_into`'s
neighbourhood and `main`'s reverify block, so they run in order. Phase 3's
`Re-read ·` rows depend on the final code hashes, so it runs last.

## Operational impact

- **No migration and no new dependency.** A record written before this
  release keeps its old hashes, because the record is permanent.
- **Output a person sees changes in three places:**
  - Where a newer reading outranks the released one, a recorded move's old
    hash is now the newest reading's.
  - An unfrozen narrowed run can now exit 1 with a new `LEFT` line.
  - An unfrozen repository needs one run where it needed two.
- **Sibling items.**
  - F (#759) owns `hooks/config.py#pact_declaration` and `config_rows`. This
    item does not edit `hooks/config.py`.
  - Both items may edit `templates/config.md` §*Pact* (this one changes only
    the `Pact notify` paragraph's first sentence).
  - Both may edit `docs/the-pact.md` (this one changes only §*A signatory
    records a pact change*'s first paragraph and its `Enforced by:` line).
  - Both may add cases to `tests/test_a_signatory_records_a_pact_change.py`.
  - If F's rule reaches the vendored path, both edit `record_pact_changes` in
    `evidence_check.py` (this one adds the guard where `parts` is built).
  - Whichever squashes second merges the release branch in and re-reads these
    four places.
