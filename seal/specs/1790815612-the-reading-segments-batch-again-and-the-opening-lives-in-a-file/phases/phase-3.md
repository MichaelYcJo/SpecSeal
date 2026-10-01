# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — phase 3

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 5572e7ba |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Spec I5, I6 and I7, `plan.md` phase 3: the kind-and-bar constants beside
`LABEL_WIDTH`, the lookup by basename, `kind` and `bar` on every row, the
block under the table with the counts, the exemption line, the three caveats,
and the cross-pin. Mutants named by the plan, each to be killed: smith rows
graded; a row at exactly its bar named; an unknown kind graded as warden; the
counts line printed while a row is under its bar; the verifying sentence
deleted; the bar read as `>` instead of `>=`. Cases S4–S11 red before the
block existed, S12 red with the script's constant moved alone, every existing
`--segments`, `--spawns`, own-file and plain-reading case green unchanged.

## What this phase found

- **The units.** `SEGMENT_BARS` (kind → the protocol's name for it and the
  bar, or None for exempt), `segment_kind` (basename after the last `:`),
  one loop at the end of `measure_segments` that gives every row both keys in
  both branches, and `report_grades`, called between the table loop and
  `report_breaches`. `report` and `report_spawns` are untouched, and so is
  every number on the page.
- **A divergence from S10, settled for I7.** `test_either_route_prints_the_same_slices`
  strips a fixed tuple of label keys and compares the rest, so two new keys on
  every row turned it red: an own file's rows carry `kind ""` where the walk's
  carry the spawn's kind, exactly as `agent` differs. I7 names the keys and S10
  says every existing assertion passes unchanged, and both cannot hold. The
  case's label tuple gained `kind` and `bar` and its claim, the numbers equal
  row for row, is the one it made before. `seal/releases/0.15.7.md` A2 is
  corrected for it in phase 4.
- **Two existing absence assertions shaped the wording.** The own-file cases
  refuse *no paired call* and *the parent could not name* anywhere on an
  own-file page, so the ungraded line says *a row no spawn named, a segment
  that made no call* instead. Found by the cases going red, not by reading.
- **`kind` now names two things in one `--json` reading.** `spawns.rows[*].kind`
  is `cycle`, `head` or `tail`; `segments.rows[*].kind` is the agent kind. They
  are different objects and a program reads them by path, and the spec fixed
  the name, so it was kept. `tests/test_one_word_one_meaning.py` holds no
  entry for it and is green. Recorded here so a later reader does not take it
  as an oversight.
- **Q5, second half: no case pins the table against the §6 block.** Nothing
  went red for the block landing between them; a new case,
  `test_the_grade_sits_between_the_table_and_the_section_six_block`, now pins
  that placement on the `segment_that_spawned` fixture.
- **One more shape, one more case.** Spec I5 says a row with `numbers` at
  null is ungraded, and no case of the first draft reached it;
  `test_a_row_with_no_paired_call_is_ungraded` does, and the mutant grading a
  null ratio is what showed it red.
- **Red first.** Nine of the ten grade cases failed before `report_grades`
  existed. The tenth, `test_the_plain_reading_and_spawns_carry_no_grade`, is a
  leak guard that passes at the base by construction; it was seen red under a
  mutant that computes the segments for the plain reading and prints the
  grade after it. S12 was seen red with the warden constant moved alone and
  with the framer constant moved alone.
- **The mutation pass, 16 mutants, one survivor on the first run.** Killed:
  smith graded; a row at its bar named (which is also the `>`-for-`>=`
  mutant); an unknown kind graded as warden; the meets line printed while a
  row is under; the verifying sentence deleted; the kind not cut to its
  basename; own-file rows given no kind; the block not printed; each constant
  moved alone; the plain reading printing the grade; the no-bar branch
  dropped; a null ratio graded; the bar left off the line; the bar dropped
  from the JSON keys. **Survived: the exempt count inverted** — with one smith
  and one warden, counting the warden as exempt gives the same three numbers.
  The smith case now counts two smiths, one of them bare (`5572e7ba`), and
  the mutant is killed. Each mutant was applied with an asserted single match,
  the file restored from bytes kept before the loop, and
  `skills/verify/scripts/__pycache__` and `tests/__pycache__` removed between
  mutants; the tree was byte-identical afterwards (`git status` clean).
- **The fixture shape.** `batched` writes one message per turn with its calls
  sharing the message id, which is how `load` counts a turn; ratios exactly at
  a bar (9/5 = 1.8, 7/5 = 1.4) are exact in binary floating point, so the
  boundary is tested at the bar itself.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
