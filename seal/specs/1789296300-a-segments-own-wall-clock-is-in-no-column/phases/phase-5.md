# 1789296300-a-segments-own-wall-clock-is-in-no-column — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `bea4a30` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and a value a segment sources from its own idea of what it is cannot be checked against anything |

## What this phase was asked

Build `plan.md`'s row 5: the sentence becomes a command.
`skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* names
the mode in place of one invocation per transcript and of the hand split; the
script's module docstring gains the mode; both README editions gain it in the
`session-cost` row; `changelog.md` and `seal/ledger/1789296300-….md` are
written.

Verified by cases in `tests/test_a_segment_feeds_the_flow_log.py`, red first.
**Both README editions checked for the parity cases that read them before
either is edited** — the frame's own named `unverified` item, and this segment
is its answerer.

## What this phase found

**The `unverified` item is answered: no parity case reads those rows.** The
only case that reads the cheat sheet at all is
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py::test_the_cheat_sheet_does_not_offer_the_runner`,
which opens `README.md` alone and asserts an **absence** — that the sheet does
not offer `bin/test`. `tests/test_docs_line_wrap.py` covers both editions but
its `prose_lines` skips any line starting with `|`, so a table row is exempt
from the wrap limit; its `test_both_readmes_are_covered_together` is about
membership in that list, not about content. Nothing compares the two editions'
rows. So the parity requirement is `CONTRIBUTING.md` §*Both READMEs move
together* plus `survivor-check` at the pull request, and both editions were
edited.

**One of this phase's four cases could not be seen red, and it is named
rather than counted as evidence.** `test_the_section_names_the_per_segment_mode`
passed against the section as it stood, because phase 2's word-pinning edit
had already put `--segments` there as the contrast with `--spawns`. It is a
guard against the name being dropped, not evidence for this phase. The other
three were red: the hand-split instruction still present, the mode's handling
of a resume unstated, and `§6` absent from the section — each quoted back by
its assertion.

**`evidence-check`'s record arm caught a divergence nothing else would
have.** Both `plan.md` and `phases/phase-1.md` named the function `plan.md`
proposed — `segment_rows()`, NAME NOT IN TREE — where the tree has
`measure_segments()`, named to pair with the `measure_cycles()` this file
already had, which is what tells a reader the two modes are siblings. The records are corrected, the phase record
keeps the proposed name behind a `NAME NOT IN TREE` marker so the rename is
not silent, and `overview.md` carries the divergence with both sides quoted.
Correcting a contract to match what was built is the thing a builder should
not do quietly; the divergence table is where it stops being quiet.

**Seven existing `seal/ledger.md` rows had to be touched, and the fragment
rule permits exactly this.** All seven anchor on
`skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"`,
whose content phases 2 and 5 changed, so `--reverify` moved every one from
`b1d57f7c` to `7837c909`. The repository rule forbids **appending** to that
file, and says a branch that changes what an existing row cites must touch it
to leave the ledger true. Each of the seven now carries a note saying what
moved; six of them cite the section for a claim about a part this work did not
touch, and the seventh — the orchestrator's boundary — has the note saying the
paragraph was split in two and the boundary half is unchanged in substance.
The check reports 1158 rows ok, 0 drifted, 0 broken, 0 refused.

**`seal/ledger/` did not exist in this repository.** This work item's fragment
is the file that creates it. No header, per the rule: every row carries its own
anchor and hash, so there is nothing for a header to declare.

**One thing was noticed and deliberately not fixed.** `survivor-check` has no
cheat-sheet row in either README either, found while answering the parity
question. It is a different command, and adding it would put a change outside
this work item's scope into a diff a reviewer is reading for something else.
It is in `overview.md` §Not done.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The instruction to run `session_cost.py` once per segment transcript, from `skills/verify/SKILL.md` step 1 | Replaced in the same step by `session_cost.py --segments` against the run's transcript, which walks them all. The single-transcript reading is not removed — the step still names it for a segment measured on its own |
| The instruction to split a resumed transcript by eye — *split it at the user lines where the coordinator sent it a new message, and measure only the slice that belongs to the segment just watched* | Replaced by the mode taking the split, stated in the same step so a reader with a resumed transcript is not left to do it anyway. `tests/test_a_segment_feeds_the_flow_log.py::test_the_section_no_longer_asks_for_the_split_by_hand` and `::test_the_section_says_the_mode_takes_the_resume_split` hold both halves, so the removal cannot come back and the replacement cannot go missing |
