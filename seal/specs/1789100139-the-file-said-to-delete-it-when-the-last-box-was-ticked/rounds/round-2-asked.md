# round 2 — the verifying round's paragraph

| | |
|---|---|
| Target | the **diff of round 1's fixes**, `bfe8cdb..17a4737` — not the branch |
| Review at | `17a4737d1c565e6ed1474b46fc6c58f698e20b08` |
| Base of the branch | `origin/release/v0.11.1` = `5646717` |
| Draft pull request | #358 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-1.md`, closed — 3 fixed, 5 answered, 1 deferred |

## The job, and what it is not

**The answers, not new findings.** For each of round 1's nine verdicts, is it
actually closed. `round-1.md`'s `New units` row reads `none`, so there is no
new-unit surface in this diff to treat as a finding surface — the whole target
is a verification surface.

`round-1.md`'s `Needs a fix` named findings 1 and 2. Five more were answered as
corrections and one is deferred to the repository owner.

## What the fix pass says it did, to be checked rather than inherited

`rounds/round-2-fixes.md` is the table `close` applied, with its own
`## Verification of this pass`. Four claims in it are worth opening because
each is the kind that reads true and can be false:

- **Finding 1's §15 probe.** The new assertion is claimed red under a mutated
  `hooks/routing.py` — an absent `Planning` row reading as `framer` — naming
  `1788177600-the-tree-that-arrives-without-its-history/routing.md`. The
  parser is claimed restored from bytes kept before the mutation rather than
  from HEAD. Re-derive the probe.
- **Finding 1's stated limit.** The case's `Implementation` arm is claimed
  unexercised by the tree, because 0 of 73 declarations omit that row: the
  claim is that mutating the default to `smith` leaves this case green and
  three fixture cases in the same module red. A limit stated in a docstring is
  a claim like any other.
- **Finding 8's second attempt.** The first move of phase 6's row is claimed
  to have left a blank line that broke the table the same way the prose did,
  and to have been caught by parsing the table back. Check that the table in
  `plan.md` now parses to contiguous rows 1 through 6.
- **Finding 5's arithmetic.** 32 is claimed to split 29 records to 3 loaded
  files, and the withdrawn bullet's place is claimed absent from the reported
  set. Both are countable.

Two things the pass reports finding on its own, beyond what round 1 asked:

- Two more instances of finding 9's class in `plan.md`'s phase 1 and 2 Status
  cells, and a correction to round 1's own figure — 467 single-space `Checked`
  cells rather than 468.
- A §12 survivor at `seal/ledger.md:1366` that it calls a survivor **by
  construction**: finding 6's fix deleted a duplicate, so the original now
  reads as wording the range removed. It was given a sixth `survivors.md` row.
  Whether a by-construction survivor may be excused by a row rather than
  corrected is a judgement this round makes.

## Executed by the orchestrating session at `17a4737`

Exit codes read directly, no pipe:

- `bin/test -q tests/test_routing_is_recorded.py
  tests/test_waiver_decided_at_start.py` → **48 passed, exit 0**. The case
  round 1 found red is green.
- `git status --porcelain` → empty.

## Unverified

The broad gate. It is the `sealer`'s spawn, and it comes due when this round
closes the run — not before, and not yours.

## The commands, in the form to use

`bin/test`, narrow, one module at a time. `bin/evidence-check --strict` —
never narrowed to this work item's fragment.
`bin/survivor-check --range bfe8cdb..17a4737 --exempt
seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/survivors.md`
if you want to see the §12 surface for yourself.

## The line the run ends on

Answer the job in a line of its own — `Needs a fix: no`, or `yes` and what
does. A 🟡 answered with grounds is `no`, so this round may report findings and
still end the run. The reopening is **one**: if this round opens something, its
own fixes get one more verifying round and a second is refused.
