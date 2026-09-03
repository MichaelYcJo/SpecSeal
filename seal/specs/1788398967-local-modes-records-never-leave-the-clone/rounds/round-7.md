# 1788398967-local-modes-records-never-leave-the-clone — review round 7

<!-- The verifying round for round 6's fixes (target: the diff 7cc4fb3..3f8f846).
It is the round that ends the chain, and it ends it by a rule rather than by
running out: at a verifying round the orchestrator does not fix. Everything
this round opened is a record correction written here, a rider at its
coordinate, or a question with a named answerer. Nothing closes on a fix, so
nothing needs reading after it. Written by the review orchestrator, which did
not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | 3f8f846 (the fix diff from 7cc4fb3) |
| PR | none yet |
| Broad gate | at the tree this record is committed in — see the table below |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |

- [x] Pass

**Why this round is the last one.** Rounds 1 through 5 each found something and
each fix was read by the round after it. Round 6 found two 🟡 and the
orchestrator fixed them in the same commit as round 6's record — which
`chain_check.py` refused, correctly: a record cannot say `no fixes to check`
while its own table closes findings on a fix. That refusal names the shape of
the recursion issue #97 is about. **Every verifying round that finds something
and fixes it needs another verifying round.** The chain terminates only when a
fix pass declines to fix, so this one declines.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r6 🟡 1 | the closing line was held by nobody | `tests/test_the_records_can_be_carried_out_and_in.py` | answered — reproduced, and the pins are real under five separate mutations | reviewer deleted the closing block, changed `Exported at` to `Copied at`, changed the replacement phrase, widened `head[:12]` to `head` and narrowed it to `head[:8]`: each reddens, and neutering an unrelated unit reddens these two only through that unit's own reach. The new case's fixture head is 40 characters and `[:12]` of it is what the assertion names, with the trailing full stop |
| r6 🟡 2 | two `Contract changes` cells named the source and not the tests | `rounds/round-2.md`, `rounds/round-5.md` | answered — and see ❓ 4, which is what the fix exposed | reviewer built an AST call graph at every record's target SHA, at every record's fix commit, and at HEAD |
| 🟡 1 | the third of round 5's three type guards is pinned by nothing. The parametrised case covers `head` and `remote`; `exported_at` of the wrong type is in no case. Three mutations of `isinstance(when, str) and when` were green against the whole file, and the loosest of them prints `Exported at 12345 from …`. Round 6 went to this block for exactly this reason and left a third of it in the state it came to fix | `skills/implement/scripts/seal.py:1008`, `tests/…:1006` | **deferred — a `RIDER:` at the parametrise list**, per `seal/follow-up.md`'s rule that a coordinate-bound item rides its coordinate. Not fixed here: a fix at a verifying round needs a round to read it, and the code is correct today — this is coverage, not a defect | reviewer executed all three mutations. Orchestrator wrote the rider with the date, the SHA and the measurement |
| 🟡 2 | round 6's grounds say deleting the closing block reddens eight cases; it reddens two. Eight is only reachable if the deletion also took the two `print` statements below it, which six case-instances already asserted — a mutation that does not isolate the finding is not evidence the new assertions work | `rounds/round-6.md:36`, `:59` | **answered here rather than by editing round 6**: a record is what a round saw, and the correction belongs in the round that made it. The true numbers are in this record's probe table | reviewer executed the isolated deletion and four more mutations; `grep` over `tests/` finds the strings in three lines of one file, inside two cases |
| 🟡 3 | round 6's `New units` cell says "one test case and two assertions"; the diff adds one case and **one** assertion. Its own 🟡 1 row states it correctly. `New units` is the row the next round reads as its list of unreviewed surface, so it is the one place the count has to be right | `rounds/round-6.md:16` | **answered here**, same reason | reviewer read the diff |
| 🟡 4 | round 6's record names two record-only commits in its range and the range holds three; four `Contract changes` cells were rewritten, not two; and `rounds/round-5.md` is new in that range rather than a checkbox change | `rounds/round-6.md:11` | **answered here**, same reason | reviewer read `git log --stat` over the range |
| ❓ 5 | a `Contract changes` cell describes the fixes the round asked for, not the tree it reviewed — round 1 names `linked_path` and round 3 names `blocked_path`, neither of which exists at those records' target SHAs. Under that reading all five cells are real. Nothing in the record says which tree, the `Target SHA` row sits four lines above, and the natural reading is the wrong one | `templates/`, `rounds/round-*.md` | deferred — issue #89, where the handoff and record rules for 0.6.0 are collecting | reviewer checked both readings against an AST call graph; at HEAD every cell is real either way, so no check can tell them apart |
| 🟢 6 | the closing line's replacement phrase is in neither README | `README.md`, `README.ko.md` | deferred — issue #89, the same class this work item has now recorded five times | reviewer read |

## Round 5's fixes, spot-checked rather than taken

| Round 5 finding | Still closed at 3f8f846 |
|---|---|
| 🟡 2 `manifest.json/` outside the size bound | yes — `seal.py:606` and `:855` match the same pair of spellings |
| 🟡 3 the order comment | yes — the comment and `:828`–`:903` run the same order |
| 🟡 7 "Both limits" where there are three | yes — `seal.py:108` reads "All three limits" |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: three mutations of the `exported_at` guard | all three green — 🟡 1 |
| reviewer: the closing block deleted, isolated | 2 cases red, not 8 — 🟡 2 |
| reviewer: `Exported at` → `Copied at`; the phrase changed; `head[:12]` → `head`; → `head[:8]` | 2, 1, 2, 2 |
| reviewer: `blocked_path` neutered | 21 cases, these two among them through that unit's reach — not a false pin |
| reviewer: AST call graphs for five `Contract changes` cells, at three trees each | every cell real at its fix commit and at HEAD; round 2's is not real at its target SHA — ❓ 5 |
| reviewer: `git log --stat` over `7cc4fb3..3f8f846` | four commits, eight files — 🟡 4 |
| reviewer: the touched test file | 77 passed |
| orchestrator: the broad gate at this tree | see below |

## Broad gate

| Check | Result |
|---|---|
| `pytest tests/ -q -n auto` | filled in at the gate's commit |
| `ruff check .` · `ruff format --check .` | filled in at the gate's commit |
| `evidence_check.py --strict .` | filled in at the gate's commit |
| `unverified_check.py --baseline` | filled in at the gate's commit |
| `chain_check.py --baseline` | filled in at the gate's commit |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–6 | `#place`, `#write_members`, `#import_`, `#write_zip`, `#unused`, `#blocked_path`, `#unsafe`, `#normalise_remote` | eight units, every one changed in at least two rounds |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `exported_at` guard is pinned by nothing | a `RIDER:` at `tests/test_the_records_can_be_carried_out_and_in.py`'s parametrise list | whoever next opens that list |
| Which tree a `Contract changes` cell describes | issue #89 | the repository owner |
| A fix that adds a visible outcome should document AND pin it in the same commit | issue #89 | the repository owner |
| A clash on both sides takes two runs · the read-only-directory case skips as root | round 5's record | the repository owner |
| A root that is itself a symbolic link · whether 32 MB, 512 MB and 20,000 are right | `overview.md` §Not verified | the repository owner |
| The export accumulating unfolded work items | issue #101 | the repository owner |
| `evidence_check.py` drops a row with a non-hex hash silently | issue #97 | the repository owner |
| The reminder reading `1 work items changed` at N=1 | `questions.md` Q1, and the pull request body | the repository owner |
