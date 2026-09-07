# Feature Specification: a record's claims about the tree are read, and the record says what bound the next round is under

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` § *The goal a design is chosen against* | Both tickets name three candidate shapes and argue for one on this clause. #190's argument is that a convention needs a person to remember; #207's is that enforcement arriving at the broad gate arrives after the decision it governs |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* | The rule #207 is about. `chain_check.py#stopping_floor` already implements the walk; what is missing is that it runs at the pull request and the decision is made at every round's end |
| `seal/follow-up.md` — *a rider's whole value is arriving at the person who opens the file* | #190's own framing: a figure in a record has no rider and no reader |
| `skills/code-review/SKILL.md` §*And commit the record before commissioning the fixes* | The record is the file the next segment opens, which is why what it says about the tree has to be true |

## Scope

**In.**

- **#190** — a check reads what a record states about the tree and refuses what the tree contradicts, over the records of work items that have not shipped.
- **#207** — `round_record.py new` says, as it writes a record, what bound the next round is under: whether this record ends the run, or one reopening remains.
- The boundary #190 needs, stated once and used by the check: **a work item whose `seal/ledger/<id>.md` fragment still exists has not shipped.** The fold removes the fragment at the release, and a released work item's records are records of a moment.

**Out.**

- Checking a count. `spec.md` and `plan.md` argue it out: this session produced four false counts and none of them is checkable without a convention for naming what is counted, which #190's own body calls a bigger claim than the first shape.
- Rewriting any record of a shipped work item. 129 occurrences sit there and they are history.
- Changing what `chain_check.py` refuses at the pull request. #207 adds a sentence at a moment; it does not move the enforcement.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A record naming a unit the tree does not have is refused | Given a live work item's record naming `` `some_helper` `` that appears nowhere outside `seal/specs/`; when the check runs; then it names the file, the line and the identifier | A case over a fixture record, seen red first, and the tree's own four occurrences of `chain_module` | <!-- NAME NOT IN TREE: `some_helper` and `chain_module` are both named here as names the tree does not have -->
| A shipped work item's record is left alone | Given the same shape in a work item whose ledger fragment has been folded; when the check runs; then it passes | A case; and the tree's 129 occurrences stay green |
| An invented name a reviewer marked is allowed | Given a record whose line carries the marker a paste-ready fix uses for a name it is proposing; when the check runs; then it passes | A case, and the marker named in one place rather than two |
| A stamp the tree contradicts is refused | Given a record naming `path#unit@hash` where the unit's content hashes to something else; when the check runs; then it says so | A case over a fixture; the tree's one real stamp stays green |
| A record that ends the run says so as it is written | Given the previous record's floor row reads `no` and one later record has closed on a fix; when `new` writes this record; then it prints that this record ends the run | A case over a fixture chain, seen red first |
| A record with a reopening left says that | Given the previous record met the floor and no later record has closed on a fix; when `new` writes; then it prints that one reopening remains | The same case, second arm |
| A first round says neither | Given no earlier record; when `new` writes round 1; then it prints nothing about the bound | A case — a sentence invented for a state that has none is worse than silence |

## Data & interfaces

No new file and no new CLI. `new` gains a printed line. The check is a new reader over `seal/specs/*/`; whether it is a new command or an arm of one that exists is `plan.md`'s.

## Open questions → questions.md

None. The three shapes each ticket names are settled in `plan.md`'s Alternatives, against measurements taken over this tree.
