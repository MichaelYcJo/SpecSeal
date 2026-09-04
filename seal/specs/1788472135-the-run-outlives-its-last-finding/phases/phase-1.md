# 1788472135-the-run-outlives-its-last-finding — phase 1

<!-- seal/specs/1788472135-the-run-outlives-its-last-finding/phases/phase-1.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | a0c134f |

## What this phase was asked

Build phase 1 only, of the four-phase table in `plan.md`: state #110's floor —
*stop when a round finds nothing that leaves the root and nothing that
crashes; whatever else it found is deferred with a named answerer, or becomes
an issue* — in four files whose coordinates were given rather than searched
for.

- `docs/review-chain-spec.md:32-100`, the section that owns the cap's
  definition, with the bound table at `:47-51`. `:82` already carries *a round
  that opens nothing needing a fix does not consume the cap*, and that is a
  DIFFERENT rule — the cap's arithmetic, where this one is about stopping below
  the cap at all. The two sit side by side and neither may read as a
  restatement of the other; say plainly which is which.
- `skills/code-review/SKILL.md:254-296`, `## Orchestrator: the run ends with a
  verifying round`. The floor lands there because the reader who meets the cap
  is the reader who needs the floor, and because the verifying round is the
  round the floor must leave standing.
- `agents/warden.md:93-99`, the `Needs a fix:` report line. The floor answer
  takes the same shape and for the same reason: the reviewer answers it in a
  line of its own, the orchestrator copies it, and an orchestrator inferring it
  from a verdict table is a reading rather than a finding.
- `templates/sdd-round.md:11-19`, the field table, which gains
  `| Loses a record or crashes | <`no` — and the run stops here ·
  `yes — <what>`> |` where a reader meets it beside `Needs a fix`, explained in
  the comment block below the table the way every other row is explained.

`tests/test_the_pull_request_language_is_the_repositorys.py:955` holds
`ROUND_RECORD_FIELDS`, hand-copied from that template table and pinning it.
Run that parametrized case and watch it fail for the new row before the row
exists — that is the red this phase owes.

Constraints named for this segment: do not touch
`skills/code-review/scripts/chain_check.py` (phase 3's), write no changelog or
ledger entry (phase 4's), run the narrow cases only and never the full suite,
lint or typecheck.

## What this phase found

**The red the phase owes runs in the opposite direction from the way the task
described it.** `test_the_round_template_carries_the_fields_it_is_expected_to`
asserts each entry of `ROUND_RECORD_FIELDS` is present in
`templates/sdd-round.md`, and it checks that direction only — a row added to
the template and never added to the list stays green. So the case cannot fail
"for the new row before the row is in the list": the list is what it is
parametrized over. The red comes from adding the field to the LIST while the
template still lacks it, which is what was done (`1 failed, 11 passed`, exit
1, the failing parameter being `Loses a record or crashes`). The instruction's
two halves were inverted; the evidence it asked for exists either way.

**Two neighbouring pins fired on the new prose, and both were the class rather
than the coordinate.**

- `tests/test_the_last_rounds_fixes_are_checked.py`'s `CAP_BACKWARDS` refuses
  the literal `still consumes the cap` anywhere in the three files that carry
  the cap rule, because that phrasing is the inversion of it. A table cell here
  used the words about a different subject — a round that met the floor and did
  find something needing a fix — and a substring guard cannot tell subjects
  apart. The prose moved to `counts toward the cap`, which is the phrasing the
  same passage already uses; widening the guard to admit the new sentence would
  have weakened an existing pin to fit new prose.
- `templates/config.md`'s *What no row governs* list is checked by
  `test_the_exclusion_list_holds_every_field_a_pinned_case_reads`, so a new
  record field name has to join it or a repository that sets `Record language`
  is told it may translate the field. `Loses a record or crashes` is now on
  that list. **Phase 3 inherits this**: any further literal `chain_check.py`
  matches on for the new rows — a depth marker's spelling, for instance —
  belongs on the same list.

**The floor line has two homes in `agents/warden.md`, not one.** The task named
`:93-99`, the passage on the verifying round's job, which is where the
reasoning goes. `## Report` at `:196-229` is the format a reviewer actually
builds its report from, and it spelled out the `Needs a fix` line in a fenced
block. A line stated only in the first is a line nobody writes, so both carry
it, and `test_the_report_format_section_carries_the_line_too` pins the second
against exactly that.

**Three files claimed `Needs a fix` was *the* run's terminal condition.** With
a second answer that ends the run, each of those sentences ships a
contradiction two paragraphs from the new one. `templates/sdd-round.md`,
`skills/code-review/SKILL.md` and `agents/warden.md` were each corrected, and
`test_needs_a_fix_no_longer_claims_to_be_the_only_ending` holds the absence
half so the old sentence cannot come back beside the new one.

**What phase 3 parses, stated exactly.** The row as the template now carries
it:

```
| Loses a record or crashes | <`no` — and the run stops here · `yes — <what>`> |
```

and the reviewer's report line, in both of its homes:

```
Loses a record or crashes: no
Loses a record or crashes: yes — <what does>
```

The value written into the cell is what stands after the colon, never the
whole line — the rule `Needs a fix` already states and whose first user broke.
The sentence bounding what may follow is identical in
`docs/review-chain-spec.md`, `skills/code-review/SKILL.md` and
`templates/sdd-round.md`, and phase 3's refusal is its counterpart: *a record
that met the floor is followed by at most one more round record*.

**One check on this branch is red for a reason that is not this phase's.**
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
fails because this work item's directory carries `spec.md` and `plan.md` and no
`overview.md` yet. It fails identically on a tree built from the phase's base
commit, so it predates the phase; the closing memo is written when
implementation ends, which is after phase 4. Named here so it is not
rediscovered as a regression.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The claim that `Needs a fix` is *the* answer the run ends on — in `templates/sdd-round.md`, `skills/code-review/SKILL.md` and `agents/warden.md` | The same three files, now saying it is one of two; the second is `Loses a record or crashes`, and `test_needs_a_fix_no_longer_claims_to_be_the_only_ending` refuses the old wording coming back |
