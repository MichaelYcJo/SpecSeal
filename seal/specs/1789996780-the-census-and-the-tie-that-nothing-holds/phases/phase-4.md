# 1789996780-the-census-and-the-tie-that-nothing-holds — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 57c31e70 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#470 finding 1. Rewrite the census note as one site carrying the corpus, the
instrument, the moment and the conclusion the figures support, with every
figure **measured at the tip after phase 3's ledger edit** and none inherited
from the tickets or the round reports (A2, Q4, Q6). Then the ledger fragment's
new rows, and the anchor question: read by hand every row citing a drifted
coordinate **before** `evidence-check --reverify` runs (A10).

## What this phase found

**Q3's default is wrong in the direction that matters.** `questions.md` says
*assume `#MARKER` may drift and `#examine` does not*. Measured: the only
coordinate this work drifted in `seal/ledger.md` is
`correction_check.py#standing`, which the frame does not name anywhere. The
anchor `#MARKER` covers the assignment statement alone — lines 289–293 at this
tip — so the census note was rewritten whole with no drift, and `--reverify`
re-stamped it to `17486986`, the hash it already had. A comment above an
assignment is not part of the assignment's unit, which is a fact about this
repository's anchoring worth having: the census note can be re-taken at every
release without touching a row that cites it.

**Q4 and Q6, measured at the tip after every ledger edit this work makes.**
Over `seal/ledger.md` alone, with the unbounded verb-by-verb walk:

| | |
|---|---|
| marker occurrences in the file | 429 |
| standing on rows | 426, over 204 rows |
| in the file's prose | 3 |
| a bare `<verb> <date>` sees | 385 |
| qualified | 44, in ten spellings |
| run lengths | 0: 385, 1: 23, 2: 9, 3: 11, 5: 1 — **no run of 4** |
| bound of three / four / five | 428 / 428 / 429 |
| longest run | `Re-read and re-stamped a third time <date>`, five words, in prose |
| candidate sites `MARKER` does not see | 0 |

Q6's answer is that the spelling still stands and is still the longest, and
that the line it sits on was never the right way to say so.

**The figure had to be taken four times, and that is the work item's own
subject arriving.** 425 before anything; 426 after C1's marker; 427 after C2's;
429 after the two markers recording C3 and C4 being re-read. Each ledger edit
this work made moved the corpus the figure is over — which is #470's finding 9
exactly, met from the inside. The plan's phase order is what kept it from
shipping stale: the digits are written last, after the last marker, and the
note names the moment so the next reader knows what to re-take.

**The split the bound rests on had never been taken in three review rounds.**
All three of the file's prose markers are qualified and they are its three
longest runs; every table row's qualifier is three words or shorter. So the
survival test, which acts per row, would return the same verdicts today at a
bound of three, and the five-word run the bound exists to admit is one the
check has never acted on. The bound is deliberately not narrowed — the same
hands that wrote a five-word qualifier into prose will write one into a row,
and `markers()` is applied to whole-file text too — but the note now states
what it is answerable to, which is a property rather than a count.

**The frame's `spec.md` failed `evidence-check` at exit 2 before the fragment
was written.** Two cells wrote the coordinates with no path, and the records
arm reads a backticked coordinate-shaped token as a live claim wherever it
stands: both came back BROKEN. Fixing the paths took the arm to `0 refused`.

**The ledger fragment re-creates `seal/ledger/`, which the 0.12.2 fold had
emptied.** The census case reads its corpus through `LEDGER` and `FRAGMENTS`,
so it picked the new fragment up with no edit — which is the property that was
bought by not hard-coding the list, observed rather than argued.

**`survivor-check` fell from five reports to two, and three of the five were
real.** The two that stand are excused in `survivors.md` with quotes and
grounds: the released `CHANGELOG.md` copy, which is Q1's and a person's, and a
sentence in work item 1789969379's `spec.md` that is still true and was never
what the range corrected — verified by re-measuring that exactly one row, R4,
carries a qualifier on every marker it has.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the census comment's *411 across the three ledger files, against 412 at five* | nowhere — that corpus does not exist at this SHA, so there is no true version of the sentence. The comparison it supported is restated over `seal/ledger.md` at the tip |
| the census comment's *404 marker occurrences on 190 rows — 401 in table cells and 3 in the file's prose* | the same note, re-measured at the tip and stated as the file's total against the part on rows |
| the census comment's *Six commits in this repository's history introduced `Re-read again`* | the same note, re-measured: nine, and stated for what it shows — the qualifier is not a one-off somebody can be asked to stop writing |
| the census comment's address `seal/ledger.md:1172` | the spelling, and the fact that it stands in prose |
| the claim that `seal/ledger.md` is the corpus because *a branch cannot move it* — which #470 prescribed and this branch disproves twice | the note's corpus clause, whose grounds are now that it is what a release folds the fragments INTO |
