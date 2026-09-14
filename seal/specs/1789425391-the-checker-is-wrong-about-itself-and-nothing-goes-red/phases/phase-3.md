# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `dd6af99` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

## What this phase was asked

#395's prose and its figure. The docstring measurement re-taken by the method
in `plan.md` §*#331's trap*, with population, date and reader beside it, and
all three figures of the sentence re-derived in one pass. `OPEN_WORD`'s comment
stops describing the exact match that was replaced. The boundary claim made
accurate in every carrier. The short-row guard's single-row raise gets the
sentence ⬜ 5 asked for, and the three-word line from the rewrap is closed.

## What this phase found

**The figure, taken 2026-09-15 at `dd6af99`, in one pass.** Population:
committed `round-N.md` records that parse — **211 of the 212** this repository
carries. Readers: `round_record.table_body` under `VERDICT_HEADER` for the
rows, `chain.verdict_of` for each verdict cell, `round_record.says_open` for
the arm.

| What | Figure |
|---|---|
| verdict rows | 2,044, none short |
| verdict cells beginning `open` | **123** |
| of those, wider than the bare word | **9** — so equality reached **114 of 123** |
| reached by the space-or-comma boundary | all 123; every one of the 9 continues with a space or a comma |
| of the 123, in `CLOSED_WORDS` | 0 |
| no-digit `#` cells / admitted | 51 / 25 |
| of the 25, verdict outside `CLOSED_WORDS` | **15** — the grounds against a vocabulary test, re-derived in the same pass |
| of the 25, newly refused by this arm | **0** |

The two neighbouring claims reproduce exactly, which is what makes the triple
one measurement rather than three of different ages.

**Why round 4's replacement could not simply be carried.** `95 / 7 / 88 over
1,704 rows` was taken at `151792e`, in a clone of a branch that had not yet
met `release/v0.11.4`. The merge brought 35 more records in, so the same walk
over the same reader now gives 123 / 9 / 114 over 2,044. Copying the number
would have been the sixth failure repeated with a seventh number — which is
exactly what `plan.md` §*#331's trap* says must not happen.

**A figure I did carry across, and corrected.** `plan.md` and `spec.md` both
say *this repository's own 176 records*, and I repeated it in this work item's
own ledger fragment before measuring. 176 is round 4's count at `151792e`. The
fragment now says 211 of 212 and names where 176 came from. §5 twice in one
work item, both times on a count, both times caught by measuring.

**And a third time, on a name.** Phase 2 annotated `spec.md`'s `SUMMARY_WORDS` <!-- NAME NOT IN TREE: this paragraph's own finding, measured below. -->
by repeating `1789002694`'s own note — that the name *became* `SUMMARY_TAIL` <!-- NAME NOT IN TREE: this paragraph's own finding, measured below. -->
— without
opening the coordinate. Measured here: `git log -S` over `broad_gate.py` on
**every** branch finds neither name in any merged commit. Both existed only
between #30's round-1 fix and its round-2 fix, and the squash into
`release/v0.11.4` discarded them; `broad_gate.py` reads the summary line
through `COUNTS_RE` today. Both annotations now say that.

**`survivor-check` over `aa3000d..HEAD` reported four survivors and none is a
defect**, which the range's own shape explains: this work item REBUILDS a seam
that was reverted, so the wording it removes is wording the released 0.11.4
correctly describes as absent. Two are the released changelog and the fragment
it was gathered from; one is an earlier work item's acceptance scenario about
`chain_check --worktree`, a mode this range does not touch; one is
`committed_records`'s own docstring, where the sentence this range moved into
`_numbered` elsewhere is still true and still needed. All four are in
`survivors.md` with a quote, and the run is exit 0 against it.

**`survivor-check` cannot see the class this phase is actually about**, which
is why two cases were added instead. An overturned claim left standing is
removed from the diff nowhere, so the range check has nothing to match — round
3's 🟡 3 and round 4's 🟡 3 are the same class one round apart, and the second
happened inside the file the first was fixed in. `test_the_rules_have_one_owner.py`
now pins both sentences: that the ruling argues against a vocabulary test and
not against reading the cell, and that the boundary is spelled out rather than
borrowed.

**Q6 is answered, and the default stands.** The short-row guard stays an
immediate raise. Round 4's grounds hold and were re-checked here: the guard was
already immediate before the verdict arm and only its condition widened, and
zero of the 2,044 committed verdict rows are short, so the cost falls on a
reviewer's first draft and nowhere else. What round 4 left unwritten is now
written — the comment says which it is, why, and that making it a list is the
repair if anybody opens the function for another reason.

**Q4's answer for this phase.** Five drifted rows, two of them the same row
read twice: `skills/code-review/SKILL.md#"## Findings format"` and
`docs/review-chain-spec.md#"### Review arm — opt-in: seal/ at the repo root"`
in `seal/ledger.md`, and this work item's own `says_open` and `verdict_rows`
rows in its fragment. Both shared rows re-read on substance — the severity
block and the two opt-in headings are what those rows claim, and neither
moved — re-stamped in one write. `evidence-check --strict` exit 0 at 1238 ok ·
0 drifted · 0 broken.

**Round 4's ⬜ 6 was moot and is recorded as such.** The three-word line
`test, and the` came from a rewrap of a paragraph `1ff0a6c` reverted, so the
tree does not hold it; the paragraph this phase writes is wrapped inside 88
columns and `tests/test_docs_line_wrap.py` is green.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `**The verdict word cannot do this job.**` in `docs/review-chain-spec.md` | The paragraph that replaces it, which keeps the argument and narrows what it argues against — and `test_the_verdict_ruling_is_against_a_vocabulary_test_not_against_reading`, which asserts the old sentence is gone |
| `skills/code-review/SKILL.md`'s *nothing catches that one* sentence | The paragraph beside it, which says what still slips through and that it now takes two mistakes in two cells. The released `CHANGELOG.md` keeps the old sentence as accurate history of 0.11.4, exempted in `survivors.md` |
