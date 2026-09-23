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
- **A session that wrote a change and checked it itself has an honest
  `Review` answer, and it is the second of the two (issue #241).** The ticket
  asked for a third — *reviewed by the session* — because seven documents said
  `straight to the PR` requires nothing. It has not required nothing since
  `chain_check.py#direct_seal` began asking a ready pull request for the
  sealer's `broad-gate.md`: the one broad run, at a SHA, against the base.
  That is exactly what a session's own check leaves that CI can read; the
  reading half is prose, and a record its author writes about itself is what
  the chain's `Fixes checked by` and `Ran by` rows already refuse. So no third
  answer is added, and the seven places — the specification's declaration
  table, the checker's inventory, the orchestration skill's four-combinations
  table and closing paragraph, the commit gate's first option, that option's
  own test and the routing template — now say what the direct answer owes and
  what it turns off, which is the reviewer alone. The specification gains a
  paragraph beside the table saying why two answers and not three, the
  release checklist names its waived commit as the routing question's
  `no work item` answer, and a pinning module holds each carrier to the
  sentence that stands and the one that is gone.
