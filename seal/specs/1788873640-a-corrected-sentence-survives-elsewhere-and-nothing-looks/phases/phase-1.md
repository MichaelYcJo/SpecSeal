# 1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | f168d33 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

Build one check: a thing that can fail, run over the tree, that takes a fix
and asks whether the sentence it corrected is still standing somewhere else.
Four conditions from the task, and the design was mine to choose:

- it reports survivors rather than forbidding a phrase — an observation with a
  list, not a corpus-wide ban;
- it is not a hand-written list of phrases, because a list rots the way #210's
  did. The distinguishing terms come from the change itself;
- it runs unattended, so it belongs where CI or `bin/` reaches it, and its
  refusal names the file and the surviving sentence rather than a count;
- false positives are the real risk, and `plan.md` answers for them with a
  named escape that is not turning it off.

Two named cases from this repository's own history, to be used as the case set
rather than inventing fixtures: **#267**, a corrected sentence left standing in
two ledger rows, one of them shared; and **#269**, a document fix shipped
pinned by nothing, whose second clause is about a check that exists but is not
where the act happens. And the whole of its credibility: **the check must be
seen failing on a real historical survivor**, not only on a fixture.

## What this phase found

**Both cases resolve to a single commit each, and finding them was the first
half of the work.** #267's ticket names `8b4b4b6` as where the six findings
were *closed*; the range that demonstrates the defect is the one before it,
`ad6f81a`, round 2's fix pass, which corrected the docstring and left the
class. #269 names `eef8610` as a target but the commit that reworded the
sentence and left its pin behind is `7bcf36a`. All the branches are unsquashed
in this clone, so both ranges are runnable.

**The two obvious mechanics each fail one of the two cases, which is what
decided the metric.** A literal grep fails #269 because the pin is one sentence
split across two adjacent string literals and no line holds it. A
longest-common-phrase floor fails #267 because the ledger rows paraphrase
rather than copy and the longest identical run is three words. Neither is a
judgment — both were checked against the text.

**Three things were measured that no amount of reading would have produced.**

`seal/ledger.md` carries **17** `~~` markers — an odd number, so one is
unpaired. A DOTALL strike span offset every pairing after the stray one and ran
across lines, swallowing row R3: the check reported the fragment and stayed
silent about the shared file, which is the carrier the ticket is about. A strike
is bounded to one line now.

**Overlapping n-grams are one piece of evidence written four ways.** The first
calibration's clearest false positive shared *be a second reader of the* — one
six-word run, four overlapping trigrams, each scored on its own. So the score
counts maximal independent runs and weighs each by its rarest n-gram, and the
discriminator became how many separate places wording is shared in rather than
how much of it is. Both real survivors share exactly two runs; that false
positive shares one.

**The threshold is calibrated over 77 real ranges** — every commit of five
unsquashed work-item branches that carried a review chain. The curve, at the
shipped metric:

| Floor | Reports over 77 ranges |
|---|---|
| 1.0 | 80 |
| 1.4 | 34 |
| **1.6** | **26** |
| 1.7 | 25 |
| 1.8 | 20 |
| 2.0 | 14 |

The two survivors score **1.89** and **1.79**, so anything above 1.79 loses
#267's shared-file row. 1.6 keeps 0.19 of room below the weaker rather than
sitting on it, at a cost of six reports over 77 ranges against 1.8. Every one
of the 24 reports at the old equivalent threshold was read: all of them are a
claim restated in a ledger row, a phase record, an overview or a test comment
while a commit changed its wording elsewhere. None is a coincidence of
vocabulary.

**What the next phase needs from this one.** The report already names the
standing text and the corrected sentence, so the CI step's failure message
needs nothing added. And the exemption reader has to anchor on content: the
survivors this range finds are ledger rows, which are edited constantly, so a
line-anchored exemption would rot within a release.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase only adds a script | none |
