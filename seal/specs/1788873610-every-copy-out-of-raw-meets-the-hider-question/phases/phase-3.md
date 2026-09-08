# 1788873610-every-copy-out-of-raw-meets-the-hider-question — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 5e51ca0 |
| Ran by | specseal:smith on claude-opus-5 |

## What this phase was asked

Close the third of the ticket's `Done when` lines: *the four documents say
what the code does, and the completeness argument names the property rather
than the count*. The spawn prompt named the four —
`seal/specs/1788668335-…/overview.md`, the grid comment above the constants
in `tests/test_the_record_is_generated.py`, that work item's changelog
fragment, and ledger row **F2** — and told this phase to sort them by
kind: a record of a moment is corrected at its coordinate, a shipped entry is
history, and a row whose verified claim is false is re-verified rather than
re-pointed.

## What this phase found

**The changelog fragment has shipped, so there are three living documents and
one piece of history.** `seal/specs/1788668335-…/changelog.md` is
byte-identical to `CHANGELOG.md`'s `## 0.8.2 — 2026-09-06` section and
`gather_changelog.py --check` reports all 46 fragments gathered. Its false
sentence is *"What is left is one cell, named rather than assumed"* — the
literal wording the ticket quotes, *a fourth copy would add a row … neither
exists*, stands in the overview and in the test file's grid comment and not
in the changelog. So the fragment was left as written, `questions.md` Q1 puts
the choice to the repository owner, and 0.9.3's own fragment carries the
correction.

**F2's anchors all survive, so it is a re-verification and not a removal.**
`CLAUDE.md` sends a row whose anchor a change REMOVES to be deleted and its
claim rewritten in the branch's fragment; F2's twelve anchors — `swallowed`,
`build`, `fenced_after`, five message constants, `SENTINEL` and five cases —
all still resolve, and four of them drifted. So F2 keeps its row, its second
sentence is struck with the correction inline, its Notes carry what moved,
and the rule that replaces it is a NEW row (F6) in this work item's own
fragment, which is where CLAUDE.md puts a new claim. A reader who opens
either is pointed at the other.

**Nine rows of `seal/ledger.md` drifted, not one.** The unscoped read named
six anchors; mapping them to rows gave eleven rows, of which F1 and F2 were
already in hand and nine had to be re-read one at a time before the file
could be re-stamped. All nine claims stand: what left `swallowed` sits above
the three positional loops F3, F4 and F5 are about, and what changed in
`new`, `close` and `build` is the write and the hider question rather than
any derivation those rows name. Each row now carries a sentence saying what
moved and why its claim survived, which is the shape F2's own Notes already
used for two earlier re-stamps.

**Writing the words `# RIDER:` in prose creates a rider.** The comment that
replaced the deleted rider at `swallowed` said *"the `# RIDER:` that carried
it is gone"*, and `rider_check.py` read that mention as a rider with no
stamp: BROKEN, and three cases of `tests/test_a_rider_reaches_its_file.py`
red. That is the checker's intended behaviour — the `1788826000-…` work item
records *a `#` comment DESCRIBING the convention inside a scanned root
becomes a rider with no stamp* as the design's intent — so the sentence was
rephrased to say *the rider* instead. It is the same class of trap the
fixes-file's code-span marker is: a marker in prose is a marker.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the grid comment's claim that the three copies are every place a text reaches the record | the same comment, rewritten as the destination property, plus the case that walks the module's syntax tree. The grid's own table is KEPT, because each of its rows now names a case rather than an argument, and two rows were added for the two shapes that were wrong |
| F2's second sentence, and the sentence in its Notes saying the straddle stays open at a rider | struck in place, with the correction beside it. F6 of `seal/ledger/1788873610-…` holds the rule that replaces it |
| the stale clause of `docs/flow.md`'s #182 row — *"`spec.md` and `plan.md` for it were drafted during 0.8.3 and are in that run's scratch, not in the tree"* | nowhere: it stopped being true when this work item wrote both fresh |
| nothing else | `none` |
