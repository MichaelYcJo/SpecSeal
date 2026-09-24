# Survivors — the fold checks run only as this repository's tests

The sealer's first run at 49119e26 (`survivor-check --range c52e8350...HEAD`) reported
eight places. Every one comes from three ledger rows this branch REMOVED because
their anchors left `tests/`: 0.14.0's S1 and P1, and 0.15.1's S1. Their claims
were written anew in `seal/ledger/1790260563-the-fold-checks-run-only-as-this-repositorys-tests.md`
(F1–F8). A removed row's cells are removed wording to the sweep. The places
below either state the rule those rows cited, which is still true and is what
the new rows anchor, or share generic verification phrasing ("red again",
"case was red") with the removed rows' notes. None of them is a claim the range
corrected.

| Path | Quote | Grounds |
|---|---|---|
| `skills/settle/SKILL.md` | One subject, one document, and a document over its ceiling takes no new statement | the placement rule 0.14.0 P1 cited as a minor anchor; the rule stands, and F-rows in this item's fragment anchor it now |
| `tests/test_a_document_has_room_for_the_next_fold.py` | One subject, one document, and a document over its ceiling takes no new | the case pinning that same rule's sentence in settle §2, which still stands |
| `docs/the-evidence-ledger.md` | was split along its own headings by MichaelYcJo/SpecSeal#526 into itself | the ceiling statement 0.15.1 S1 cited; its claim is true and unchanged by this range |
| `docs/the-evidence-ledger.md` | No document is over the ceiling now, so none is listed. | the ceiling statement's sentence that 0.15.1 S1's claim restated; `Over the ceiling` is still `none` |
| `docs/the-evidence-ledger.md` | over that ceiling takes no new statement.** Two folds had put 29 of the 101 | the ceiling statement 0.14.0 P1's minor anchor named; the statement stands |
| `seal/releases/0.14.0.md` | the case was red on the space-only pattern, and restoring it reds it again | another row's own execution note (E1); it shares only the phrasing "reds it again" with removed S1's notes |
| `seal/releases/0.13.0.md` | The first case was red against `adb5607d`'s parent on its first assertion | another row's own execution note; it shares only "case was red" and "red again" with removed S1's notes |
| `skills/settle/SKILL.md` | A document above that ceiling takes no new standing statement | settle §2's ceiling sentence that 0.14.0 P1 cited; the rule stands |
