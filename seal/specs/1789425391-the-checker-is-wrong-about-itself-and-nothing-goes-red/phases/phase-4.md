# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `ed0dc56` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

## What this phase was asked

#335 and #334 together, in one module and in this order. First: `seal` refuses
`round-N` on a last record **before** the write — four values (`round-1`,
`round-9`, `round-2.md`, `ROUND-1`), each exiting 2 with no cell written and no
`round-record: sealed` line; the refusal's three-value sentence rewritten and
pinned (§14). Then: the case over the real pair — the real `seal` against a
fixture record in each of the two endings, asserting what the gate prints, with
the second route to the written-then-refused state named and asserted as the
route.

The acceptance is the mutation: change `round_record.py`'s `sealed` print to
any other word and a case must go red.

## What this phase found

**Q3 is answered, and it took two measurements rather than one.**

The first was the one `questions.md` asked for: four candidate routes to the
*cell written, then the chain check refuses* state, run against the real
`seal`.

| Candidate | Reached |
|---|---|
| an earlier record's `New units` emptied | yes — **chosen** |
| the last record's `Target SHA` unresolvable | yes |
| an earlier record's floor row emptied | yes |
| a stray `round-draft.md` under `rounds/` | **no** — exit 0 |

The first is chosen because it is furthest from anything `seal` reads: `seal`
opens the LAST record only, `chain_check.fix_surface` opens every record of the
item, and a present-and-empty row is refused on any record and grandfathered on
none — so the route does not age out with a cutoff.

**The second measurement is the one nothing asked for, and the case is wrong
without it.** Built with the emptied row COMMITTED, the case failed at exit 1
instead of 2, and the reason is a seam nobody had written down: `broad_gate`
runs `chain_check` **itself, at HEAD**, as one of its own checks, before it
ever calls `seal` — and `seal` runs `chain_check --worktree` **after** the
write. So a committed refusal fails the gate's own check first and `seal` is
never reached. That is a third ending, and it is neither of the two the
discriminator is about.

The route therefore has to exist in the working tree and not at HEAD, which is
exactly the window `--worktree` exists for. The case leaves the emptied row
uncommitted and asserts `round-record: sealed` is present, so it cannot quietly
stop reaching the state it was written for.

**#335's grounds, restated as what the code now relies on.** `seal` does not
*derive* lastness — it **selects by it**: `n, path = last_record(routing,
rounds)` is the line above the predicate. The objection the ticket carries is
that refusing everything but `no fixes to check` *pins into a subcommand a
conclusion `chain_check.checked_by` derives from the repository*; it does not,
because the fact is the subcommand's own selection criterion, and because both
parties read the same ratified sentence rather than one copying the other's
conclusion.

**§14 reached three surfaces here, not one.** The refusal's sentence *The row
holds one of three values* is true of the ROW and false where it is printed, so
it is rewritten and pinned. `agents/sealer.md` then turned out to list **two**
refusals where the subcommand has raised on **three** since #30's round 1 — a
gap that predates this work and that a reader of the definition would meet as a
surprise at exit 2. Both halves are corrected and both are pinned.

**Q4's answer for this phase, and the plan's forecast again overshoots.** The
plan counted `seal`, `last_record`, `broad_gate.py#gate` and `#seal_record`
moving. `last_record` and `broad_gate.py` were not touched at all. Two anchors
drifted — `round_record.py#seal`, carried by three shared rows, and
`agents/sealer.md#"## The one write, and why it is yours"`, carried by one.

Of those, **one clause is superseded rather than merely moved**:
`seal/ledger.md` S13's bolded *the row holds three values and everything
outside two of them is refused*. What the row is FOR — a capped run seals, a
run whose fixes nobody has read does not, and `Fixes checked by` tells them
apart — is untouched, so the clause is corrected in place rather than the row
removed, and the narrowing is a row of this work item's own fragment. S6's
count of `raise Refused` sites is still six; only the description of the third
changed.

**S12 was re-read on substance and drifted nothing**, which is itself the
finding the plan expected. Its three coordinates are the reading side of the
seam, and none of them moved — but the case its claim rests on drives a STUB
whose `round-record: sealed …` text the case itself writes. That is the whole
of #334: the claim was verified against a fixture's own words. The row now says
so, and the case over the real pair stands beside it with its coordinate in
this work item's fragment.

`evidence-check --strict`: exit 0, 1244 ok · 0 drifted · 0 broken.

**Q1's cost, carried forward to the memo.** This phase is what makes every
sealed record a member of the population `docs/review-chain-spec.md` records as
an open problem, rather than an edge of it. The owner answered (a), leave the
arm open; the sentence that pays for that answer goes in `overview.md`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The refusal's sentence *The row holds one of three values: `round-N`, `no fixes to check`, or `nobody — <why>`* | The refusal that replaces it, which names the one value the last record accepts and gives the reason each of the other two is refused. `chain_check`'s own three-value refusals are untouched, because they are about the row on ANY record and are still true there |
| `test_the_refusal_names_the_three_values_the_row_holds` <!-- NAME NOT IN TREE: this row is what removed it. --> , whose docstring argued that refusing everything but `no fixes to check` would hard-code a conclusion belonging to `chain_check` | `test_the_refusal_says_which_value_the_last_record_may_hold`, and `plan.md` §*The two judgments*, which answers that argument on the merits. The case name changed, so the anchor is gone rather than drifted; no ledger row carried it |
| `agents/sealer.md`'s count of two refusals | The same sentence at three, with the `Fixes checked by` one named |
