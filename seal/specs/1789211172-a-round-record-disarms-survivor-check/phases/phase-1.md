# 1789211172-a-round-record-disarms-survivor-check — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `392da83` |
| Ran by | `specseal:smith` on `unknown` — the spawn prompt named no model, and this template reserves the value for the spawning session rather than letting a segment source it from its own idea of what it is |

## What this phase was asked

Write the case first and run it against the unedited module. It must **fail**,
and this record quotes that failing output verbatim. A constructed repository
whose range removes a sentence in one file and adds a round record under
`seal/specs/<id>/rounds/` quoting it, with the same sentence standing in a
third file. Nothing in the module is edited.

## What this phase found

**Two cases, not one, because the filter goes on `paths` and a path list has
two sides.** `spec.md` §*Scope* in-item 1 argues for both sides and the
acceptance rows fold the removed side into A2's *no reported source sits
under a `rounds/` directory*, which A1's own range answers trivially — the
record it adds removes nothing, so no range in A1 can put a record in the
source position. A second case supplies a range that can: it edits a round
record and touches nothing else. Without that case the removed side of the
filter is unmeasured, and a later narrowing of the fix to the added side
alone would pass the suite.

**The two cases are red in opposite directions, which is what tells them
apart from one case written twice.** The added side is red at exit **0** —
the gate reporting success having measured nothing. The removed side is red
at exit **1** — the gate naming a record of a past state as the place a claim
was corrected, and asking somebody to go correct it.

**The corpus arithmetic had to be constructed, not assumed.** Both cases score
2.00 against the shipped floor of 1.6, and they reach it the only way this
module accepts evidence: two independent runs of shared wording with unshared
words between them. `weigh` scores a run by its rarest n-gram and `runs`
counts stretches rather than n-grams, so a single contiguous rewrite shares
one run and is correctly not reported. The sentence pair is the one
`test_a_claim_corrected_in_one_place_and_left_in_another_of_the_same_file`
already uses, for that reason. The rarity half is why each case carries a
`filler.md`: `weights` returns an empty map for a one-file corpus, and the
round record is out of the pool by construction, so the pool has to be built
from files that are not it.

**`records_a_past_round` matched the constructed path on its own shape, as
the module's docstring claims it does.** The fixture writes
`seal/specs/1700000000-a-claim-stands-in-two-places/rounds/round-1.md` into a
`tmp_path` repository that has no `seal/` root of its own and no config, and
the predicate held there — `rounds` in the parts, `specs` before it. That is
the claim `seal/ledger.md` row S6 records, executed against a tree that is not
this repository.

### The failing run, verbatim

`bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -k "round_record_the_range"`
at `8d707b3` with the module unedited:

```
E       AssertionError: guide.md still carries the wording this range removed from notes.md, and the round record quoting that wording is what silenced it -- the quote counted as wording the fix wrote; exit 0
E         survivor-check: examined 3 files at 848dc07, against 1 sentence(s) the range 7835cea..848dc07 removed
E           no removed wording is still standing
E
E       assert 0 == 1

tests/test_a_corrected_sentence_survives_elsewhere.py:486: AssertionError
________ test_a_round_record_the_range_edited_does_not_become_a_source _________
...
E       AssertionError: this range edited a round record and touched nothing else, and the check read that edit as a correction somebody has to chase into guide.md; exit 1
E         survivor-check: examined 2 files at 9f84bb0, against 1 sentence(s) the range fad3d50..9f84bb0 removed
E
E         guide.md:3
E           standing    The verdict cell is written by the reviewing round itself and the orchestrator never edits it afterwards.
E           corrected   seal/specs/1700000000-a-claim-stands-in-two-places/rounds/round-1.md:5 -- The verdict cell is written by the reviewing round itself and the orchestrator never edits it afterwards.
E           shared      2 phrase(s), 2.00: “by the reviewing round itself and the”, “the orchestrator never edits it afterwards”
E
E         1 place(s) still carry wording this range removed. Correct each, or record it in seal/specs/<work-item-id>/survivors.md with the grounds and a quote from the surviving text
E
E       assert 1 == 0

=========================== short test summary info ============================
FAILED tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_round_record_the_range_added_does_not_subtract_the_survivor_it_quotes
FAILED tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_round_record_the_range_edited_does_not_become_a_source
2 failed, 43 deselected in 6.88s
```

The second failure prints the defect in full rather than as an exit code: the
coordinate the reader is sent to correct is `rounds/round-1.md:5`, a record of
a past state at the SHA it was written against.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase adds two cases and edits nothing | none |
