# 1789996775-the-gate-states-what-its-own-fixes-disproved — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | b4a8f0f4 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#465. Replace the three statements at `:19`, `:68` and `:377` of
`tests/test_the_gate_asks_the_range_ci_will_ask.py` with round 3's
paste-ready text (A6), leaving A3 of work item 1789956662's `spec.md`
untouched. Measure Q4 here.

## What this phase found

**A6's grep criterion comes back with two lines rather than none, and that is
the criterion being met rather than missed.** `spec.md` A6 asks that
`grep -n "byte-identical\|exactly as it did\|reading as it did"` return
*nothing that still claims the module was untouched*. It returns
`:22` — *all but ONE assertion … reading as it did* — and `:74` — *It is NOT
byte-identical*. Both hits are the corrections themselves, so what the grep
measures is the token and what the criterion asks about is the claim. That
distinction is the whole of #465: round 2 corrected one coordinate with a grep
over the corrected sentence, and three more copies of the claim stood three
hundred lines away in wording no such grep reaches. Rewording round 3's
paste-ready text to empty the grep would be departing from the reviewer's own
replacement for a checker's benefit, so the criterion is recorded as met and
the gap is `overview.md`'s.

**Only one of the three sites sits inside a unit an anchor can name.** The
module docstring and the fixture comment are at file level; `:377`'s is the
docstring of `test_a_repository_with_no_remote_at_all_resolves_to_the_ref_as_given`.
That is the shape of the defect rather than an accident of it — the claim was
standing in prose no unit encloses — and it is why the ledger's W3 row carries
one coordinate for three sites and says so.

**Q4 was clean at this phase and did not stay clean.** `survivor-check` over
`origin/release/v0.12.3...HEAD` at `b4a8f0f` reported *no removed wording is
still standing* against the 8 sentences the range had removed. Phase 3's
removals are what made it speak, which is recorded there: a survivor check run
at a phase boundary answers for the range up to that boundary and for nothing
after it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the module docstring's *keeps every fixture in … reading exactly as it did* | the same docstring, saying which assertion moved and why |
| the fixture comment's *the fallback keeps that module byte-identical (A3)* | the same comment, naming the assertion and the test that holds it |
| the resolver case's *what keeps that module reading as it did* | its own docstring, pointing at round 1's finding 3 |
