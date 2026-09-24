# the fold checks run only as this repository's tests — questions for the planner

**Decided from the tree, so nobody reopens them.** Each has its grounds in
`spec.md` or in `plan.md`'s Alternatives table.

- How the values reach the command: three `seal/config.md` rows, with flags
  that override them for one run (`templates/config.md`'s row convention,
  `broad_gate.py#broad_command`'s reader, `CLAUDE.md` §*The goal*).
- What the two test modules become: this repository's pins over the shipped
  script, under the same names, with the constants gone and the prose pin
  reading the rows.
- One command, not two, and not a mode of `settle`.
- The over-ceiling listing ships with the command
  (`tests/test_a_document_has_room_for_the_next_fold.py`'s docstring records
  the intent to keep it).
- The `Enforced by:` line is exempt from the wrap limit, not joined across a
  wrap: 3,232 of 3,490 single `path::test` targets overflow alone (executed
  2026-09-24). A `nothing — <why>` line is not exempt.
- #530 is fixed as the class of container syntax before the first pipe, not
  as round 3's paste-ready five tokens.
- The four released ledger rows the move reaches are REMOVED or re-read as
  `CLAUDE.md` says, and their claims are written anew in this work item's
  fragment.

No row below needs a person. Nothing here blocks the build.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | How many statements does `fold-check --shape-from 0` name on this tree, and is it the 101 that #565 and the evidence-ledger prose count? | a measurement | One run after phase 2. Equal: #565's worklist is confirmed. Different: #565's frame starts from the measured number, and the prose that says 101 is a claim for that item to correct | #565 takes the measured number, whatever it is; this work item corrects no prose about 101 | ⬜ |
| Q2 | Which other ledger rows drift when phase 5 edits `skills/settle/SKILL.md` §2 and `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*? | the work | Found by `bin/evidence-check .` after the edits; each is re-read against the edit and re-stamped, its claim corrected in place first where the edit made it false | Phase 5 re-reads every drifted row it meets | ⬜ |
| Q3 | Does the wording of the absent-row line (S4) and the exit-2 line (S5) read right to someone running `fold-check` in a repository that never set either row? | the work | The phase that writes them pins them (§14). The review chain reads the pinned text | As phase 3 writes them | ⬜ |
