# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 455c42c2 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 6: the changelog fragment with one entry per issue; the
ledger fragment's own rows for S1–S14; `evidence-check --reverify --into`
for the released rows that drifted, and `Corrected ·` rows for the list in
`spec.md` S15 (Q-W2); `overview.md` with its divergence rows and `## Not
verified`; every `phases/phase-N.md` in place. The orchestrator added, after
the run resumed: the eight suite-wide guard modules besides this item's own,
and the ledger fragment under the work item's full name.

## What this phase found

**Q-W2, from the checker's own output.** `evidence-check --reverify --into`
named 101 released rows citing a coordinate this work moved, and left 14
coordinates it could not re-read because the unit is gone. Each of the 101
cited claims was read and sorted by what it says: 23 say something this work
made false — a printed summary read by wall clock, `NO_SUMMARY`, the JUnit
reader and `SUITE_XML`, `RunRecord.skipped`, a stop read off the exit alone,
rule 3's two stops left open, a scale, the ladder, `check_scale` — and take a
`Corrected ·` row; the other 78 hold and take the checker's `Re-read ·` row.
The corrections were written FIRST and the re-reads after: a `Corrected ·`
row supersedes the row it cites, so the second `--into` wrote no re-read for
a row this work corrects, and left no coordinate behind. `spec.md` S15's list
was the frame's reading; against the checker it gains 0.15.3 A5, 0.18.0 W2,
0.20.0 W1, W3, W5, W8, `Corrected · D1` and `Corrected · W3`, and 0.20.0's
`Corrected · N5` and `Corrected · P1` stay re-reads (`overview.md` says why).

**The first `--into` was redone.** It ran before the corrections existed and
wrote a re-read for every drifted row, the 23 false ones included. That
uncommitted output was dropped with `git checkout` of the fragment, whose
committed state held only K1–K17, and the run was repeated after the
corrections were in.

**The records named names the tree no longer has.** `evidence-check
--strict` refused 17 names in this item's `spec.md` and `phases/phase-5.md`
— the retired scale names, two pytest internals — and each line now carries
`NAME NOT IN TREE`, the marker the frame already used.

**Survivors.** `survivor-check --range d6a443fd..HEAD` named 22 places still
carrying wording this build removed: released ledger rows, which never
change and are superseded here, other work items' records, and three
sentences sharing only a phrase. Each is in `survivors.md` with its quote.

**Guard modules, executed.** `tests/test_a_shrunken_corpus_declines_to_judge.py`,
`tests/test_a_rider_reaches_its_file.py`,
`tests/test_every_reader_ends_a_line_where_gfm_does.py`,
`tests/test_one_word_one_meaning.py`, `tests/test_no_real_identifiers.py`,
`tests/test_a_record_states_what_the_tree_has.py`,
`tests/test_release_hygiene.py`, `tests/test_docs_line_wrap.py`, with
`tests/test_a_question_says_who_can_answer_it.py`,
`tests/test_no_passage_is_pasted_into_a_second_file.py` and
`tests/test_a_corrected_sentence_survives_elsewhere.py`: 621 passed.
`bin/evidence-check --strict .` exit 0, `unverified-check --baseline
origin/release/v0.21.0` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase wrote records and removed nothing from the tree | none |
