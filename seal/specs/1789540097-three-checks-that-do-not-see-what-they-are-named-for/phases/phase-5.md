# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | f990cc73 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The two Grounds cells at `seal/specs/1789445605-…/rounds/round-2.md:39` and
`:40`, which render `fixed at 6233b769 — . ` where they should read
`fixed at 6233b769 — `, repaired in the shape `9919b265` used on the sibling
record. Scope that came here on somebody else's answer: Q1 of work item
`1789455558-…` assigns the cells to the fourth work item cut from
`release/v0.12.0` after `fix/401-402-…` merges, the one carrying #413, which
is this branch. **Only the rendering is repaired, never the prose** — a round
record holds what was true when it was written.

## What this phase found

**The class closes here, and it was eleven rather than two.** Round 3 of work
item `1789455558-…` deferred *the eleven cells already rendered wrong by
#414's cause* to this branch; nine of them were repaired by hand at
`9919b265`, in `round-1.md` of the same work item, and these two are the
remainder. Enumerated across the whole `seal/` root rather than at the two
coordinates the frame named (`agent-contract` §12):

| Shape searched | Hits | What they are |
|---|---|---|
| `— . ` | 8 | two cells, now repaired; six in documents that QUOTE the defect — `spec.md`'s before/after table, `changelog.md`, `phase-3.md`, `questions.md` Q5, the ledger fragment, and `round-3-report.md` |
| `— at  — ` | 1 | this work item's own `plan.md`, describing the `9919b265` repair |
| `— ; ` · `— , ` | 7 | ordinary prose, no empty first clause |

Every survivor is a document describing the defect. Repairing one of those
would delete the report of the thing, which is the opposite of the repair.

**No mutation, and the reason is the phase's subject rather than its size.**
The three phases before this one each proved a check by making the thing it
guards wrong. This phase repairs a RECORD. Its cause was #414 and was removed
on `release/v0.12.0`; the cases that hold the cause belong to work item
`1789455558-…` and are not this branch's to re-plant. What this phase owes is
that the corrected cells still parse for the reader that opens them, and that
is what the verifying command measures — `test_chain_check_at_the_pull_request.py`'s
`_real_records` case runs the checker over this repository's own committed
records. 114 passed, exit 0.

**The prose stayed, including a clause #413 shows to be incomplete.** Cell
`:39` says `test_both_ampersand_cells_name_both_shells` pins both cells, per
cell, in the list each cell is in. That was true of what round 2 could see
and is incomplete rather than false — phase 1 is the sentence's continuation,
not its correction — and a round record is not brought to a later wording.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The empty first clause `. ` in two Grounds cells | nowhere — it was a rendering artefact with no content, and every statement about it stays in the six documents that report it |
