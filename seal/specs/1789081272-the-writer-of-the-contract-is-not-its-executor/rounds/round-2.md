# 1789081272-the-writer-of-the-contract-is-not-its-executor — review round 2

| Field | Value |
|---|---|
| Target SHA | 8b3146a |
| Ran by | warden on Opus 5 (1M context) |
| PR | #352 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no — all three of what this round opened are corrections owed at the closing commit, none of them changes behaviour, and none is a defect a release would ship. What comes due instead is the sealer spawn: contract §2's one broad act, which neither round ran and neither round was allowed to. |
| Loses a record or crashes | no — nothing this round found leaves the root or crashes, and nothing round 1 found did either. The one thing that ever failed a CI job, finding 1, is fixed and the check now exits 1, which is a warning. |

- [x] Pass

## What this round was asked

The verifying round required by `agents/smith.md` and `docs/review-chain-spec.md`: spawned at the diff of round 1's fixes, `1d1b6e9..8b3146a`, asking whether each closed finding is actually closed. Round 1's verdicts were inherited rather than re-derived, and the branch outside the fix diff was out of scope.

Three judgments were named in the spawn prompt rather than left to be found, each a decision the fix pass made rather than a repair it performed: a case whose meaning was narrowed to make it pass (`test_this_repositorys_own_records_state_nothing_the_tree_lacks`, now filtering DRIFTED and EXTERNAL); finding 6 closed on the date half of its remedy alone; and the boundary the fix pass drew around §12's class, which left seven session-state names unswept.

The broad gate was excluded under contract §2 as the sealer's one act, and neither round ran it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | `bin/evidence-check` exits 2 on seven `NOT-IN-TREE` refusals | `survivors.md:11`; `phases/phase-2.md:77`, `:133`, `:166`; `phases/phase-4.md:35`, `:36`, `:82` | answered | Executed at the target SHA, exit code read directly and never through a pipe: **exit 1**, records `0 refused · 1 drifted`, ledger `1121 ok · 0 drifted · 0 broken`. All seven markers present and each names the removed name it stands for. `test.yml:89-94` renders exit 1 as a warning |
| 2 | `test_a_person_answerable_row_reaches_the_report_in_full` cannot fail | `tests/test_a_question_says_who_can_answer_it.py:136` | answered | The assertion now pins the bullet's own literal, and `agents/framer.md:223` carries it verbatim. Executed: module green in a 160-passed run |
| 3 | `test_the_report_does_not_reduce_the_frame_to_counts` pins half of what it claims | `tests/test_a_question_says_who_can_answer_it.py:167` | answered | Same repair on the other half; `agents/framer.md:217` carries the literal. Executed, green |
| 4 | `BESIDE_THE_ROOT` does not carry `specseal-planner` | `tests/test_the_records_can_be_carried_out_and_in.py:53` | answered | The entry is present and the case builds seven files plus `specseal-worktree-choice`. Executed, green. The comment around it is finding 16 |
| 5 | The follow-up row sits outside its table | `seal/follow-up.md:65` | answered | The blank line is gone and the row rejoined the table — and the line that replaced it is finding 10's own deferral row, so one edit closed both. Read, and `tests/test_a_rider_reaches_its_file.py` executed green |
| 6 | Five ledger rows re-hashed with `Checked` left stale | `seal/ledger.md:275`, `:276`, `:277`, `:283`, `:284` | answered | All five read 2026-09-11. Executed against git: `d950e8b` is dated 2026-09-11, touches exactly those five rows, and its message states each claim was re-read. `phases/phase-4.md:6` names it |
| 7 | `the other two ship answered` is a miscount | `templates/sdd-routing.md:59` | answered | The sentence now names `Planning` beside this row and `Review` and `Destination` as the answered pair; the arithmetic is right. The rewrap it left behind is finding 15 |
| 8 | S10's acceptance row is the one place the deferral is not written | `spec.md:87` | answered | The row is struck through and carries **deferred to #350**, milestone 0.11.1, in the shape §Scope item 7 uses. Read |
| 9 | The `specseal-planner` tree line is one column out | `docs/one-root-by-lifetime.md:111`, `docs/one-root-by-lifetime.ko.md:109` | answered | Both editions now align the description column with the `specseal-implementer` line below. Read, both editions |
| 10 | `plan.md`'s third `Status` value has no home | `plan.md:96-104`, `templates/sdd-plan.md:93` | answered | A `seal/follow-up.md` row now carries the argument, both sides of it, and names the repository owner as answerer. Read; the schedulable-row cases executed green |
| 15 | The broad gate | `seal/config.md` `Broad gate` row | deferred agents/sealer.md | agents/sealer.md |
| 16 | The fix for finding 7 left a 118-column line where the block wraps at 80, in a template every work item copies and no wrap check reaches | `templates/sdd-routing.md:62` | answered | corrected at 8eec47f |
| 17 | The rewritten `BESIDE_THE_ROOT` comment sends a reader to a document that names three of its seven entries, and the docstring beside it enumerates a name the tuple lacks while omitting one it has | `tests/test_the_records_can_be_carried_out_and_in.py:52`, `:216` | answered | corrected at 8eec47f |
| 18 | Row 15 of the round record reads `answered` where the report it was generated from reads `❓ out of verified scope` — a settled verdict's word on the one check neither round ran | `rounds/round-1.md:47` | answered | corrected at 8eec47f |

## Paste-ready fixes

```
     because the gate stops recognising the file and goes back to asking.
     A wrong answer here is never contradicted by
```
```python
# Session state that sits BESIDE the root under the common git directory.
# `docs/one-root-by-lifetime.md`'s tree diagram names the two agent marks and
# the opt-out; the review and parity marks, the export state and the lease are
# named where each is written. None may ever be in a zip, and the case that
# asserts it builds every one of them.
```
```python
    """S2. Everything `BESIDE_THE_ROOT` names sits beside the root — the two
    agent marks, the two review marks, the opt-out, the export state and the
    lease — and the worktree choices directory is built beside them here.
    None of them belongs to another machine."""
```
```
| 15 | The broad gate — full suite, repository-wide lint, typecheck | `seal/config.md` `Broad gate` row | ❓ out of verified scope | contract §2 makes it one act with one owner and `agents/sealer.md` is that owner; the orchestrator spawns the sealer once this round settles, and the `Broad gate` cell is where the answer lands |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the three changed modules at the target SHA, in the clone | **160 passed** |
| `bin/test` over `tests/test_docs_line_wrap.py`, `tests/test_a_rider_reaches_its_file.py`, `tests/test_one_word_one_meaning.py`, `tests/test_waiver_decided_at_start.py`, `tests/test_routing_is_recorded.py`, `tests/test_the_implementer_is_recorded.py` | **137 passed** |
| `bin/evidence-check` unscoped at the target SHA, exit code read directly, never through a pipe | ledger `1121 ok · 0 drifted · 0 broken`; records `0 refused · 1 drifted`; **exit 1**, which `test.yml:89-94` renders as a warning |
| `.github/scripts/rider_check.py` at the target SHA | `26 ok · 0 drifted`; **exit 0** |
| `uvx ruff check` and `uvx ruff format --check`, the three changed modules only | All checks passed · 3 files already formatted |
| Probe: one marker removed from `survivors.md:11`, the narrowed case re-run, the file restored from bytes kept before the run | unmutated **exit 0**; marker removed **1 failed**, `NOT-IN-TREE` in the assertion message. Restored byte-identical, `__pycache__` cleared |
| Statuses `check_records` can append, read out of `evidence_check.py:2233-2281` and compared to `main:2442-2444` | unreadable, not-in-tree, `BROKEN`, `DRIFTED`, `EXTERNAL` — the case's filter and `main`'s subtraction partition the same set |
| Longest line of `templates/sdd-routing.md` at `1d1b6e9` and at `8b3146a` | **94 → 118**, and the 118 is the line finding 7's fix wrote |
| The rows `d950e8b` touched in `seal/ledger.md`, against the five the fix pass re-dated | the same five, and `d950e8b` is dated **2026-09-11** |
| `specseal-` names carried by `docs/one-root-by-lifetime.md` | four, at `:111`, `:112`, `:113`, `:583` — against seven in `BESIDE_THE_ROOT` |
| New units and contract changes in `1d1b6e9..8b3146a` | no added `def`, `class` or module constant in `tests/`; no file under `skills/agent-contract/` touched. `New units: none` and `Contract changes: none` are honest |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. `agents/sealer.md` is the owner, and this report leaving nothing open is what makes the sealer spawn due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/survivors.md:11`; `phases/phase-2.md:77`, `:133`, `:166`; `phases/phase-4.md:35`, `:36`, `:82` | round 1's 1 — fixed |
| round-1 | `tests/test_a_question_says_who_can_answer_it.py:121` | round 1's 2 — fixed |
| round-1 | `tests/test_a_question_says_who_can_answer_it.py:150` | round 1's 3 — fixed |
| round-1 | `tests/test_the_records_can_be_carried_out_and_in.py:55` | round 1's 4 — fixed |
| round-1 | `seal/follow-up.md:65-66` | round 1's 5 — answered |
| round-1 | `seal/ledger.md:275`, `:276`, `:277`, `:283`, `:284` | round 1's 6 — answered |
| round-1 | `templates/sdd-routing.md:59` | round 1's 7 — answered |
| round-1 | `spec.md:87` | round 1's 8 — answered |
| round-1 | `docs/one-root-by-lifetime.md:111`, `docs/one-root-by-lifetime.ko.md:109` | round 1's 9 — answered |
| round-1 | `plan.md:96-104`, `templates/sdd-plan.md:93` | round 1's 10 — deferred |
| round-1 | `seal/ledger.md:275`, `CONTRIBUTING.md:105-119` | round 1's 11 — withdrawn |
| round-1 | `hooks/routing.py:61-66` | round 1's 12 — withdrawn |
| round-1 | `plan.md:90` | round 1's 13 — withdrawn |
| round-1 | `plan.md` row 6, `.github/workflows/hygiene.yml:115` | round 1's 14 — withdrawn |
| round-1 | `seal/config.md` `Broad gate` row | round 1's 15 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `BESIDE_THE_ROOT` should reach the seven session-state names beside the root that no work item's mark produced | nowhere yet — judged outside §12's class for this run, since the branch opened none of those hooks. It is a coverage question about untouched code, not a leaving of this fix pass | the repository owner, if it is ever worth a work item |
