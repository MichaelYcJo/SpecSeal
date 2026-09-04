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

**Eight rows in the shared ledger were re-stamped, and this phase re-read
two of them.** The sentence that first stood here said the two and left the
other six to be inferred, which round 1 read as what it was — `CLAUDE.md`
says the `Checked` column holds the date somebody read the code, and six rows
got a new hash without one. The eight, by line, are `:79`, `:83`, `:102`,
`:189`, `:197`, `:359`, `:381` and `:434`.

| Rows | What happened, and when |
|---|---|
| `:83`, `:359` | re-read in **this phase**, on their merits: `chain_check.py`'s vocabulary comment and the review arm's heading drifted because this branch's new constant and new subsections sit inside those units, and neither claim is about anything the branch touched |
| `:79`, `:189`, `:197` | re-stamped here and **only re-read in the fix pass for round 1's 🟡 6**. Their `Checked` cells already read 2026-09-04, so the date could not show the difference — which is the sharper half of that finding. Round 2's 🟡 10 then found the answer: the date cannot show it and the **Notes** column can, so all eight rows now carry a `Re-read <date>` clause naming what the re-read found, and this table is no longer the only place the split is recorded |
| `:102`, `:381`, `:434` | re-stamped here with `Checked` left at **2026-09-02**, a date two days before the content the new hash covers. Corrected in the same fix pass, each with what the re-read found |

No row anywhere cites something this branch deleted, so `CLAUDE.md`'s *a row
whose anchor a change removes is REMOVED* does not fire — that part of the
original sentence stands.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
