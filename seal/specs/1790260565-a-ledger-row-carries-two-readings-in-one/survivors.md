# Survivors — a ledger row carries two readings in one

`bin/survivor-check --range d6cce923..e79665da`, run at phase 4's close,
reported two places carrying the sentence phase 4 corrected in
`docs/round-record-spec.md`. Both are records that quote the old sentence in
order to say what it was, so both are left standing. They are the first two
rows.

Run over the whole branch, it reported twelve more from `0f5f537b..e79665da`
and fourteen from the base, `c52e8350...e79665da`, the two extra being
sentences of the same openings split differently. Every one is from phase 1. Phase 1 deleted the second copy of S4's and G5's
Notes opening, and that opening still stands once in the same row, which is
the point of the union. The other places are the texts the opening was
written about: F5, the section it cites, and the cases that read it. None is
a defect. They are the remaining fourteen rows.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.8.2.md` | This row is the presence F5 is the absence of | G5's Notes opening, kept once where #568 removed its duplicate |
| `seal/releases/0.8.2.md` | The second tidy-up is deleting the tracker document's | G5's Notes opening, kept once where #568 removed its duplicate |
| `seal/releases/0.8.2.md` | The document's case reads the script's own constant rather than a literal | G5's Notes opening, kept once where #568 removed its duplicate |
| `seal/releases/0.9.2.md` | The half that was missing is what protects the sentence | S4's Notes opening, kept once where #568 removed its duplicate |
| `seal/releases/0.9.2.md` | Nothing pins the two documents agreeing | S4's Notes opening, kept once where #568 removed its duplicate |
| `seal/releases/0.9.2.md` | A row that cites the wrong document as its agreement is the same class as the count above | S4's Notes opening, kept once where #568 removed its duplicate. Reported from the base (`c52e8350...`) and not from `0f5f537b..`, because the sweep splits sentences per range |
| `seal/releases/0.8.2.md` | The tidy-up is moving the format into the skill for symmetry | G5's Notes opening, kept once where #568 removed its duplicate. Reported from the base only, as the row above |
| `seal/releases/0.8.0.md` | the shipped skill may name `flow-measurement` and `flow-baseline` | F5, the absence G5's opening names as its pair. It shares G5's words because the two rows are written to be read together |
| `seal/releases/0.8.0.md` | A later edit that moves a sentence from the script's docstring into the skill for symmetry | F5's notes, the same pairing with G5 |
| `seal/releases/0.8.0.md` | is the presence this row is the absence of | F5's notes, the same pairing with G5 |
| `docs/issues-and-milestones.md` | That half is not a detail | The section S4's opening describes. The document is the subject and the opening a reading of it |
| `tests/test_release_hygiene.py` | #179's second candidate | A docstring S4's opening echoes, on the rule's below-the-running half |
| `tests/test_a_release_rolls_the_flow_measurement_issue.py` | the obvious tidy -- retitle them into the new form | The case G5's opening describes, stating the tidy it refuses |
| `tests/test_a_release_rolls_the_flow_measurement_issue.py` | so both conventions are visible in the tracker forever | The case G5's opening describes, stating why old titles stay |
| `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/spec.md` | the `blocks more` direction `docs/review-chain-spec.md` §*The reopening* states | This work item's spec quotes the defect it frames. Rewording the quote would leave the spec describing a defect nobody can find |
| `seal/releases/0.9.1.md` | the `allow` exception names `docs/review-chain-spec.md` §*The reopening* as where the `blocks more` direction is stated | R4's dated `Re-read 2026-09-24` note records the sentence as that reading found it. The `Re-read 2026-09-25` note after it says what the sentence names now, and a note records a past reading, so it is not corrected |
