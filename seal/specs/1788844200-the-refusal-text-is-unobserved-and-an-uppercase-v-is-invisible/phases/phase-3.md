# 1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 5b6c533 |
| Ran by | specseal:smith on claude-opus-5[1m] — the harness's own model identifier; the spawn prompt named none |

## What this phase was asked

#205 — delete "or a narrower prefix" from the case docstring and from the
ledger note, replaced by one line saying a narrower `/` entry takes the same
date check and so is order-independent by construction. Add no assertion.

#206 — one sentence in `docs/issues-and-milestones.md` making the three
documents that name the version check agree, with the below-the-running half
stated so the line about which release an issue shipped in reads as protected
rather than as an oversight. Leave `docs/release-checklist.md` and
`docs/flow.md` alone.

## What this phase found

**The R1 note lives in `seal/ledger.md`, not in a fragment.** `seal/ledger/`
is empty — the 0.9.1 release folded every fragment away — so both corrections
had to be made in the shared file. That is the permitted case: the rule is
about appending, and a correction is not an append.

**Correcting two rows drifted two anchors, and one of them was not this
phase's.** The scoped check found exactly two drifted rows and no more: the
docs heading my #206 sentence sits under, and
`test_the_message_has_a_route_for_every_token_the_check_refuses` from phase 2.
Both are units this work item actually re-read, so `--reverify` scoped to
`seal/ledger.md` was honest — the measurement before running it is what made
it honest, because a blanket re-stamp over a file also re-stamps rows nobody
here has read, and row G5 carries a note from an earlier session that hit
exactly that.

**The coordinator's mid-task correction was already in force.** The narrowed
evidence check had been typed as `--strict --ledger <fragment> .` throughout.
Executed for the record: the form the original handoff gave prints `no evidence
ledgers found — nothing to check`, `total: 0 ok`, and exits 2 on the records
arm rather than on the ledger arm — so it checks nothing and its non-zero exit
names a directory listing rather than a row.

**#205's claim was reproduced before it was written down**, including a
direction the ticket does not state: running each arrangement with the entries
in both orders shows the exact-path one is the only arrangement whose answer
moves at all. That is what "order-dependent" has to mean, and it is a sharper
statement than the four-row table.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| "or a narrower prefix" from `test_the_exemption_list_does_not_depend_on_the_order_it_is_written_in`'s docstring | the same docstring, restated as the reason it was never true |
| the sentence in `seal/ledger.md`'s R1 note calling a narrower prefix the same mechanism | corrected in place in that row, with the re-execution beside it |
| *"whether it has shipped or is still ahead"* from `docs/issues-and-milestones.md` | the same paragraph, as at-or-above with the below-the-running half stated; ledger fragment row S4 |
