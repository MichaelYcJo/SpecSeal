# 1788501054-a-check-reports-clean-while-something-is-missing — phase 4

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-4.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 9485fec |
| Ran by | specseal:smith on opus |

## What this phase was asked

Build phase 4 only: answer whether *the record carries what it says it
verified* is checkable — **either way**, in the spec if it is not — and write
the fragments. Verified by `evidence-check .` **unscoped**,
`fold_ledger --check` and `unverified-check`. Plus `docs/flow.md`: this
ticket's box, and a row for any ticket this work opens.

## What this phase found

**The answer is no, and the three rejected checks are worth more than the
answer.** Each of them fails in a way `docs/review-chain-spec.md` already
refuses somewhere else, which is why naming them matters: *a probe row naming
a fix* is a keyword match over free prose, the enumeration over an unbounded
domain the arrow's and the comma's limits already decline; *every record
carries a fenced block* refuses the ordinary case, where every probe was a
command; and *the block's content appears in the diff* contradicts phase 3's
own rule, because the record is written before the fixes exist. A document
that simply omitted the question would read as an oversight, and the next
person would write the first of those three.

**What is left is a declaration, and this document now has three.** `New
units`' depth, `Ran by`'s provenance, and this. Saying which facts a check
cannot reach is what keeps the checks that remain honest, so the count is
stated rather than left for a reader to notice.

**The unscoped read is what this phase is for, and it earned its keep on this
branch.** Before: 508 ok · 1 drifted · 0 broken. After phases 1–4: 517 ok · 1
drifted · 0 broken, and the nine rows that drifted along the way were all in
`seal/ledger.md` — the handoff section, the verifying-round section, the review
arm's heading, `evidence_check.py#main`, `#seal_home`, `chain_check.py#main`
and a comment anchor beside it. **Not one of them is in this work item's own
fragment**, so the scoped read this branch was told to stop using would have
reported clean the whole way. That is #153's measurement reproduced by the
branch that fixes it, which is the one demonstration the ticket could not
arrange for itself.

**The re-stamp is the cost the guidance now imposes on every branch, and
somebody has to pay it by hand.** `--reverify` has no row selector: it narrows
by FILE, so re-stamping this branch's own drift in `seal/ledger.md` re-stamps
S8 with it — a row whose claim is false and whose repair belongs to the
repository owner. It went `45edf260` → `75242cc8` and was put back by hand in
the same commit, so `evidence-check .` reports exactly one drifted row on this
tree, as it did on the base. That is now a recurring cost rather than a
one-off, because phase 1 sends every round to the unscoped read; it is Q2 in
`questions.md` with three options and the owner as answerer.

**No new numbered row went into `docs/flow.md`.** The only ticket this work
opens is Q2's, and it has no number — opening an issue is an outward-facing
act this session does not take. The box for #153 + #150 is ticked.

**Two rows in the shared ledger were re-read rather than re-stamped
blindly.** `chain_check.py#"# The vocabulary as a match ORDER…"` and
`docs/review-chain-spec.md#"### Review arm — opt-in…"` drifted because this
branch's new constant and new subsections sit inside those units. Both claims
are about things the branch did not touch — how a commit pattern is matched,
and that the two opt-in headings name `seal/` — so the rows are re-verified
rather than removed. No row anywhere cites something this branch deleted, so
`CLAUDE.md`'s *a row whose anchor a change removes is REMOVED* does not fire.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
