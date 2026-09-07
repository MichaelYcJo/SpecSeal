# Implementation Plan: a record's claims about the tree are read, and the record says what bound the next round is under

## Summary

Two tickets, one sentence: **a record knows things nothing reads it for.** #190
is about what a record asserts about the tree; #207 is about what a record
could say and does not. Both are repaired where the record is written or read,
and neither needs a convention a person has to remember.

## Technical context, and the measurement that decided #190

**[executed]** at `a6b6b17`, over every `.md` under `seal/specs/`:

| What a record can state about the tree | Occurrences today |
|---|---|
| a `path#unit@hash` stamp | **2**, and one of them is a fixture (`mod.py#helper@deadbeef`) |
| a backticked identifier that appears nowhere outside `seal/specs/` | **179** — of which 50 are distinct names once commit SHAs are excluded |
| the same, in a work item whose `seal/ledger/<id>.md` fragment still exists | **4**, and all four are one name |

The four are `chain_module`, in `rounds/round-2.md` and `rounds/round-3.md` of
`1788749195-…`. **That is the instance review round 3 of that work item found
by reading**, three weeks of records later. A check would have named it at the
commit that wrote it.

**The 129 in shipped work items are not defects.** A plan from 0.4.0 proposing
a helper that was built under another name is a record of what was decided
then. The fold is the boundary and it already exists: `fold_ledger.py` moves a
work item's fragment into `seal/ledger.md` and removes the file at the release,
so *a fragment exists* is *this work item has not shipped* with no new state to
maintain.

Other coordinates:

- `skills/code-review/scripts/chain_check.py#stopping_floor:2477` and
  `#closed_with_a_fix:1348` — **[read]** the reopening walk, already written.
  #207 needs the answer this computes, one round earlier and from the writer's
  side.
- `skills/code-review/scripts/round_record.py#reach_back:953` — **[read]**
  `new` already opens the previous record and reads a named row out of it, to
  set `Fixes checked by`. The floor row is a row of the same table.
- **[read]** `NAME NOT IN TREE` is the marker reviewers already write beside an
  invented name in a paste-ready fix. It appears **0 times** inside records —
  the reports carried it and the records did not, which is what #187 was about
  and is now fixed. It is the escape hatch, and it costs no new convention.

**What breaks in 6 months.** The identifier check grows a false positive — a
record naming a symbol from another project, or a name in prose that reads like
one — and somebody widens the exemption instead of narrowing the pattern. The
repair is that the exemption is a marker on the line, not a list in the
checker: a list is edited by whoever is annoyed, and a marker is written by the
person who knows the name is invented.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#190** — a stamp check alone, the ticket's argued choice | Measured: two stamps in the whole tree and one is a fixture. It is a mechanism guarding one occurrence, and the class it is written for produced seven instances in this release's own two chains, none of them a stamp | **Kept, and not alone** — it is exact and cheap, and it is the shape `evidence_check` already resolves |
| **#190** — a count check | Four of this session's instances were counts (`33 passed` for 31, *the 58 cases the row names* for four, *two arms* for four). Not one is checkable without the record saying what it counts, and the ticket calls that a bigger claim than the first shape. It also has no failing example that a convention would not have prevented more cheaply | **No**, and the reason is written into the check's own message so the next author does not re-derive it |
| **#190** — a convention: records name shapes and never numbers | Costs nothing to enforce because nothing enforces it, which is how the class arrived. The ticket says so itself | **No** |
| **#190** — an identifier check over every record | 129 occurrences in shipped work items, every one a record of a moment. A check that refuses history is the mistake #179's branch refused twice | **No** |
| **#190** — an identifier check bounded by the ledger fragment | A work item whose fragment is folded early loses the check before its records stop being live. Measured: the fold happens at the release, which is exactly when a record stops being the file the next segment opens | **Yes**, with the stamp check beside it |
| **#207** — the spawn-prompt guidance names the bound instead of the cap | A fourth document saying what two already say, which #180's own *Not this* refuses. Measured this release: the session that carried the wrong bound had both documents open | **No** |
| **#207** — the record carries the bound as a field | A new row is a contract change for every reader of the record, and the value is true only until the next record is written | **No** |
| **#207** — `new` prints the bound as it writes the record | A printed line scrolls past. It arrives at the moment before the orchestrator decides whether to spawn again, which is the moment the enforcement at the broad gate does not reach — and it costs no contract change | **Yes** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The boundary: a reader that answers *has this work item shipped* from the presence of `seal/ledger/<id>.md`, with the fold as its stated grounds | Cases for both arms; the tree's own two unreleased items | |
| 2 | The identifier arm — a record of a live work item naming a backticked identifier the tree does not have is refused, naming file, line and name; a line carrying the invented-name marker is not | Cases seen red first; **the tree's own four `chain_module` occurrences red before phase 3 and green after**, and the 129 shipped ones green throughout | |
| 3 | The four occurrences corrected, and the marker written where a reviewer will meet it | Phase 2's check over the tree, exit 0 | |
| 4 | The stamp arm — a record naming `path#unit@hash` is resolved the way a ledger anchor is | A case over a fixture whose unit was edited; the tree's one real stamp green | |
| 5 | **#207** — `new` prints the bound it can already compute, from the previous record's floor row and the walk `chain_check` implements. Round 1 prints nothing | Cases for the three states, each seen red first | |
| 6 | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` | The fragments; `fold_ledger.py --check` | |

Phase 2 before phase 3, and the order is the deliverable: the check has to be
red on the tree's own four before they are corrected, or nothing shows it reads
what it claims to.

## Operational impact

One new check to run, and a printed line at every record. No migration: the
boundary is derived from a file the fold already removes, and a shipped work
item's records are outside the check by construction.
