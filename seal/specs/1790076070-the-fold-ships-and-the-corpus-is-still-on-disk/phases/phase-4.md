# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 28e98957 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`docs/review-chain-spec.md` and `docs/review-handoff-protocol.md` — the
checker's six items, the survivor sweep's two, the orchestrator's half, the
handoff, and the two ungrouped items `1788212517` and `1788224363`. Verified
as phase 3 was.

## What this phase found

### A fold onto an existing sentence is the cheapest correct fold

Nine of the twelve items wrote a rule that is **already stated** in one of
the two destination documents, in a section of its own. For those the fold is
one marker line above the standing sentence, and no prose at all:

| Item | Marked on |
|---|---|
| `1788272986` | chain spec §*The fix surface — `Contract changes` and `New units`* |
| `1788472135` | chain spec §*The floor — `Loses a record or crashes`* |
| `1788501054` | chain spec §*When the record was written — before the fixes it commissioned* |
| `1788212517` | chain spec §*`Fixes checked by` has to name a checker the repository can confirm* |
| `1789518345` | chain spec §*The declaration, and where the check went instead* |
| `1788491830` | protocol §*Ran by — what executed this segment* |
| `1788224363` | protocol §*The handoff before round 1* |
| `1788277657` | protocol §*After the run — the per-segment bars* |
| `1788873630` | protocol §*Where each half went*, one new paragraph |

`skills/settle/SKILL.md` §2 says to merge into a document that exists and to
write a rule rather than quoted fragments. Where the rule is already the
document's own sentence, writing a second copy beside it is the failure that
sentence names — so the marker goes on the original.

### Three items had no home, and they are one statement

`1788873640`, `1788912166` and `1789211172` are the survivor sweep: the check
itself, the range row a deletion owes, and a round record's exclusion from the
corpus **on both sides**. Nothing in either document described the sweep. They
are folded as one new section, `## The survivor sweep`, with a subsection for
the draft/ready asymmetry `1788912166`'s other two arms settle.

### Where a destination was checked rather than assumed

**`1788491830` is marked in the protocol, not in the chain spec**, although
its segment is `chain_check.py` and the chain spec also has a
§*What ran the round — `Ran by`*. The protocol is where the field's normative
contract lives — it is the document that says what the cell must contain and
what a missing one does — and the chain spec's section is about what the
check makes of it. A work item folds once; it folds where its rule lives.

**`1788277657` stays in the protocol** although its subject, how a segment's
cost is judged, is `docs/measuring-a-run.md`'s subject in phase 10. Its
segment is `docs/review-handoff-protocol.md`, which is to say its ledger rows
anchor in that file: the rule it wrote already lives there, in
§*After the run — the per-segment bars*. Moving the rule would be a rewrite,
not a fold.

No destination moved.

### What was dropped rather than folded

**`1788224363`'s meter half.** That work item settled five pieces, and the
first is `session_cost.py`'s turn-counting — keyed by message id, usage
counted once per message, model time attributed turn-aware. It is folded
nowhere here, because the `session_cost.py` segment's own seven work items
carry the meter's standing rules into `docs/measuring-a-run.md` in phase 10,
and the newest statement inside a segment wins. What this item's marker
records is the handoff rule, which is its own and is where it sits.

**Every `## Out` row again**, and one worth naming: `1788873630` explicitly
refused a style gate in `round_record.py new`, on the grounds that whether a
style rule can be checked mechanically is open. That is a decision about a
ticket, not a rule that governs anything — the open question outlived the
work item and lives in the tracker.

**`1789211172`'s docstring coordinate** (`:63-79`) went with the code. The
claim it made — that the exclusion applies to the pool and not the range — is
what the folded sentence states, in the form a reader can act on.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing from the tree — prose and markers only | none. The twelve directories go in phase 11 |
