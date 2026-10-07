# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8229c227 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 2: `base_word` gives the unread reason after
`UNENDED_AT_BASE`; `failure_lines` says how many lines of the record at
`HEAD` did not parse; `UNENDED_AT_BASE` and `UNENDED_HERE` name a stop pytest
made; `RAN_TO_ITS_END`'s comment is rewritten with #852's two corrections in
Q-M1's words; rule 3's two stop sentences become one clause, and the
**New?** bullet follows; the two rule-3 pins and the sentence cases move in
the same commits. Cases S6 (gate half), S7–S8 end to end at the base, S11.

## What this phase found

**`failure_lines` takes the head `RunRecord` here rather than in phase 3.**
It took `unplaced` and `unended` as two integers; a third would have been
replaced by the record one phase later anyway, so the signature is
`failure_lines(check, verdicts=None, record=None)` from this phase on, and
the counts move onto it in phase 3. No case called it with the old keywords.

**S8 needed an order no plain pytest gives by itself.** Without xdist, `-x`
stops in the file whose failure stopped it, which reads `failing on base
too`, and the files after it hold no line, which read `NOT_REACHED` — the
argument #849's comment made for leaving the limit named. A false `new`
needs a file that ran part-way before another file's failure: a conftest
that orders the tests by name (`RUNS_BY_NAME`) puts `tests/test_two.py`'s
first test before `tests/test_one.py`'s failures and its last test after
them. At 5623d728 that file read `new` under `-x` and under `--maxfail=2`;
it reads `new?` naming the session now. A failed collection under `-x` has
no gate-level case: no test runs after it, so every other file reads
`NOT_REACHED` on both sides of this change, and the recorder's case holds
its `stopped` in both orders.

**The unread line is said in a sentence that works for one and for many.**
`{count} of the lines … did not parse as the recorder's and each was passed
over` — `spec.md` S6 quoted a singular form, and the constants are pinned
verbatim, so one sentence serves every count rather than two.

**The New? bullet could not repeat rule 3's clause.**
`tests/test_no_passage_is_pasted_into_a_second_file.py` refused the first
wording, a 31-word run shared with rule 3; the bullet says the same thing in
other words, as `spec.md` asked (*the same clause in the reader's words*).
The bullet also gained one sentence on the unread line at the base and one
clause on it at `HEAD`, so a reader handed the new `new?` reason is told
what it means; rule 3 was left without it, since the line is a damaged
record rather than a row the gate cannot measure.

Shown red: the eleven new and re-aimed cases were run against 5623d728's
gate, recorder, rule 3 and bullet (checked out over the committed files,
then restored from the commit): all eleven failed. The three `pytest.exit`
codes and both `-x` / `--maxfail=2` cases read `new`; the two pins and the
two unit cases met sentences and names that were not there. Mutation: the
unread reason not given, its count fixed at 1, the form's unread line not
written, its count fixed at 1, and the form's unended line not written were
each red through `bin/mutation-check`; the count-fixed form mutant survived
on first pass and the case moved to a count of 2.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| rule 3's *as a `KeyboardInterrupt` or `pytest.exit()` in a test, a failed collection without `-x` and xdist under `-x` give* and its sentence *Two stops are named rather than closed: …* | rule 3's one clause on what the `end` line says; the two stops are closed, `RAN_TO_ITS_END`'s comment says how |
| the **New?** bullet's *as a `KeyboardInterrupt` or `pytest.exit()` in a test and xdist under `-x` give* | the bullet's clause on a stop the `end` line names |
| `failure_lines`'s `unplaced` and `unended` arguments | `record`, the head `RunRecord` |
