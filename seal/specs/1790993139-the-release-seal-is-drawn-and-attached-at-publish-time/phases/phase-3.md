# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 720c2765 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The rows and their sources. `suite_counts` reads JUnit. `chain_counts`
reads through the routing and chain_check readers, plus the labels.
`release_rows` holds the fixed set, with the continuation-row rule, and
`alt_text` says it in a sentence. A measurement over 0.17.0's tree goes in
this file, with the deferred rule's 12 against the owner's 13 explained or
left as Q10. Cases S8, S9, S10 and S11. The measurement runs against the
tree at `233f0455`, with the merged pull requests' head branches written
into a fixture, never fetched by a case.

## What this phase found

**The frame holds for this phase.** `hooks/routing.py#item_dir` and
`#rounds`, and `chain_check.py#verdict_table` and `#verdict_of`, are where
`plan.md` puts them, and they read the 0.17.0 records unchanged.

**The 0.17.0 measurement.** It used a scratch clone of this repository
checked out at `233f0455`. The input was the eleven pull requests
`gh pr list --base release/v0.17.0 --state merged --json number,headRefName,labels`
returned on 2026-10-03, saved to a file in the scratchpad. `chain_counts`
over that tree and that file gave:

| Row | Measured | The owner's hand count |
|---|---|---|
| items | 10 | 10 |
| rounds | 27 | 27 |
| capped | 6 | 6 |
| deferred | 12 | 13 |

The preparation pull request (#724) has no declaration, so it is not an
item. The twelve issues are #313, #701, #704, #706, #708, #709, #710, #712,
#713, #716, #720 and #721, the frame's list.

**Q10: the 13th issue is #722, and no verdict shape is missed.** Of the
`deferred` cells in the 27 records, every one that names an issue is read.
One cell, #700's round 2 finding 5, reads `deferred new issue` and names no
number, so the record gives nothing to count. The `## Deferred` sections
list five issues: #313, #704, #716, #721 and #722. Four of them are also in
a verdict cell. #722 is the one that is not: #717's round 3 lists it in its
`## Deferred` table as an observation, and no numbered finding carries it.
The union of the two readings is 13, the owner's count. The frame's default
stands, because the rule counts what the verdict tables say and the 13th was
never a verdict. Reading `## Deferred` as well would mean a second section
reader that no checker shares. Whether the seal should count it is a
question about the panel's meaning, and `questions.md` Q10 records the
answer.

**Settled while building.**

- **The tree's modules load when first asked for.** `release_seal.py`
  imports only the standard library at module level. `seal_stamp`,
  `routing`, `chain_check` and the markdown reader are loaded on first use
  through one cached loader. An import that fails at the top of the file
  would end the process before `main` could print today's note and exit 0,
  and phase 4's every-failure-exits-0 rule could not hold.
- **`PANEL_VALUE_WIDTH` is held, not imported.** `broad_gate.py` is the
  whole gate. A case holds the local 23 equal to `broad_gate`'s.
- **A row that needs two counts says `not read` when either is missing.**
  That applies to items with rounds, and to capped over items. One round
  and one issue are singular. The first mutation pass found that neither
  rule was watched, and the cases were extended.
- **`passed` keeps the frame's formula.** Mutating it to
  `tests − skipped` survives, and the survival is equivalent: a failure or
  an error raises before the subtraction is reached.

**Verified.**

- Red first (executed): all thirteen new cases failed before the units
  existed.
- Mutations through `bin/mutation-check .github/scripts/release_seal.py`
  against `tests/test_the_release_seal_is_drawn.py` (executed). Each of these
  went red: the width test `<`; the continuation written whole; every count
  plural; the tag cut at 7; errors not refused; a suite assigned rather than
  summed; the no-suite refusal removed; capped always 0; a pull request with
  no declaration counted; an unreadable table skipped; the unread guard
  removed; the readers' failure answered with zeros. Four survived the first
  pass and went red once the cases were extended: the items row reading one
  count; the capped row reading one count; the alt text's sanitiser removed;
  any cell mentioning *defer* counted. One survived and is equivalent:
  `passed` without failures and errors.
- `uvx ruff check` and `uvx ruff format --check` on the touched files
  (executed): clean.

**Ledger.** C1–C3 are in the fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `release_seal.py`'s module-level `import seal_stamp` and its `sys.path` edit | `release_seal.py#stamp`, through `#module` |
