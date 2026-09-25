- **The pull-request check stops going red on three shapes of record it had
  no claim to judge (issues #598 and #529).** A pull request that puts back a work
  item the base had retired, byte for byte, is no longer held to where the
  restored records' reviewed commits are. Those bytes were added, and their
  review enforced, by an earlier pull request. The check says where they
  came from, and one byte changed makes the record the pull request's claim
  again. On a draft, `Pass` beside `Fixes checked by: nobody — <why>` on the
  last record now prints and names the verifying round, because that is the
  state between `round_record.py close` and the verifying round's record.
  *Ready for review* still fails the pull request if the cell says `nobody`.
  `close` itself now exits 0 in that window. A record deleted and re-added
  on a side branch that merged back is judged on its latest add, as the
  review-chain spec already said, including when that branch's clock ran
  behind.
