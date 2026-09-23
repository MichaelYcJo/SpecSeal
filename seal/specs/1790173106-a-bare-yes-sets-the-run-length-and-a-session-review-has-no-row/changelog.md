- **A bare `yes` in a round record's `Needs a fix` row no longer buys the run
  a round (issue #138).** The floor's count of later records restarts at the
  record whose `Needs a fix` says the run reopened, and a `yes` with nothing
  after it used to say exactly that — three characters that the row beside
  it, `Loses a record or crashes`, had refused from the day it was read.
  Now the two rows take one vocabulary at both ends: `chain_check.py` refuses
  a bare `yes` on the record that carries it, in the floor row's words, for
  work items begun at or after `NEEDS_FROM` (it prints before that, under
  the row's existing grandfathering — no committed record carries one, so no
  new cutoff), and in the count walk a bare `yes` reads as no reopening at
  all, the value an unreadable cell already has. `round_record.py new`
  refuses the report one command earlier, for either terminal line, and its
  printed bound reads the cell through the gate's own reader, so the line a
  session reads before spawning and the gate cannot disagree about it.
  `docs/review-chain-spec.md`'s `Needs a fix` table, `templates/sdd-round.md`
  and the checker's own inventory say so, each pinned.
