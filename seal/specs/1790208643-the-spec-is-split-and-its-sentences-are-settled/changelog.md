- **The two comments above `kept_broad_gate`'s calls, and the sealer's seal
  sentence, say the newest entry of a same comparison is replaced (issue
  #556).** `round_record.py close` and `seal` each carried a comment saying a
  run the cell already holds is always kept behind the new entry, and
  `agents/sealer.md` said every earlier run is. The call they describe
  replaces the newest entry where it is the same commit against the same
  base, which is the ordinary case of a sealer re-run over an unchanged
  checkout. Both comments now name that replace (`same_run`), and the sealer
  says every earlier comparison is kept. Comments and one definition
  sentence; no behaviour moved.
