# 1789996780-the-census-and-the-tie-that-nothing-holds — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 02ec71ee |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#470. Enumerate the class *statements that `seal/ledger.md` carries 404 marker
occurrences on 190 rows* **by construction over the tracked tree**, never from
round 3's list of six; correct every present-state site and leave every
past-state record; correct row C1 with the ledger's own sentence-case marker;
correct the SDD records under the `<!-- CORRECTED … -->` marker adopted from
work item 1789996775; replace the positional coordinates with content ones
(A9); leave `CHANGELOG.md` §0.12.2 under Q1's default and disclose it.

## What this phase found

**Round 3's list of six was three short, and enumerating by construction is
what found them.** `.github/workflows/hygiene.yml:270`, work item 1789969379's
`questions.md:31` and its `spec.md:86` each state a figure of the class, and
none appears in the list. Two of the six had also moved under it, exactly as
`spec.md` A4 predicted: the ledger fragment was folded into `seal/ledger.md`
as row C1, and the changelog fragment was gathered into `CHANGELOG.md` §0.12.2
— which is a seventh site, and the one a reader outside the work item actually
meets.

**Two more arrived from `survivor-check` rather than from the grep**, because
they state the same class of fact in different words: ledger row C2's claim
cell (*would watch 10 rows and ignore 185*) and row C4's Notes (*123 rows
carrying one of two first cells*). Neither contains the string the grep
enumerates on, and both were stale — the split is 16 against 196 at this tip,
and 126 rows share a first cell. A grep enumerates a **spelling**; the class
is a **kind of claim**, and the two do not coincide. That is the phase's
sharpest finding and it is why Q5's check earned its run.

**Round 3's figures reproduce exactly at round 3's own SHA**, which is what
made it safe to keep them in the SDD records with a moment attached rather
than re-take them. Re-measured at `31b320e5` with this work's own unbounded
instrument: 404 occurrences in `seal/ledger.md`, 190 rows carrying 401, 3 in
prose, and 412 / 412 / 413 across the three fragments at bounds of three, four
and five. Findings 9 and 10 are both confirmed by execution rather than
inherited from prose (`agent-contract` §5).

**The workflow's correction-check leg is sliced on a bare literal, and a
comment naming the script breaks it.**
`test_a9_the_leg_asks_the_range_the_pull_request_is_about` does
`text.split("correction_check.py")[1]`, so the first edit to that comment —
which pointed a reader at `correction_check.py`'s census note — moved the
slice to the text between the comment's mention and the real run line and
turned the case red on correct YAML. The comment was reworded to avoid the
token. The fragility is latent, it is mechanism a fix may not add, and it is
in `overview.md` §*Not verified* for the owner.

**The correction to row C1 had to replace the false sentence, not merely
narrate it.** The cell's own convention, set by rounds 1 and 2, is that each
correction quotes the superseded text and the superseded text goes. The first
attempt left round 2's *404 occurrences on 190 rows, 401 in cells and 3 in
prose* standing beside a marker quoting it, so the cell asserted the
contradiction and its correction at once.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `correction_check.py`'s module docstring figures — *404 marker occurrences on 190 rows*, *10 rows … against 185*, *39 of this repository's 404 markers* | the census note beside `MARKER`, the one site A1 permits, which phase 4 rewrites |
| the `SIZE_CAP` comment's *the shared file in this repository is 1.07 MB* and `standing`'s docstring *123 rows carrying one of two first cells* | nowhere — both reworded to a proportion that survives a release, so no figure is created to drift |
| the test module's *404 marker occurrences on 190 rows* and *39 of its 404 markers* docstrings | the census note, which the docstrings now point at |
| the hygiene workflow's *39 of the file's 404 markers* | the census note, named without the token that slices the leg |
| `seal/ledger.md:1172` as the address of the longest qualifier, at four sites | the spelling itself, plus the fact that it stands in prose rather than on a row |
| row C1's *404 occurrences on 190 rows, 401 in cells and 3 in prose* | the corrected split, re-measured at the tip in phase 4 |
