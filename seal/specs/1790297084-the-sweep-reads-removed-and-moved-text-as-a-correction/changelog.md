### Fixed

- `survivor-check` no longer reports a ledger row's claim as corrected
  wording when the row was removed because its code was (#603). A row whose
  anchor a change removes is removed with it, so a document still stating
  the rule survived nothing. A row counts as removed that way when at least
  one of its anchors resolved before the range and does not after it. A row
  reworded in place, or removed while all its anchors still resolve, is
  still measured. The range that removed three such rows in 0.15.3 reported
  eight places and now reports none.
- `survivor-check` holds text a fold carries verbatim from a retired work
  item into `docs/` (#591). The retired directory used to leave the range
  before moved text was paired, so the fold's copy could pair with a
  correction the same range made elsewhere and hide it. The retired side now
  takes part in the pairing and leaves the range after it.
- `survivor-check` names the correction, not the file that only moved, on
  each report's `corrected` line (#592). When the same sentence was
  corrected in one file and moved out of another, the moved copy used to
  pair with whichever file came first in path order. It now pairs with the
  file it shares the most sentences with, then with a file gone at the tip.
  The places reported and their scores are unchanged.
