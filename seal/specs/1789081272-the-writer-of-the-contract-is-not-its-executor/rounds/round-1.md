# 1789081272-the-writer-of-the-contract-is-not-its-executor — review round 1

| Field | Value |
|---|---|
| Target SHA | 67c47ce60c2f55238fe0531cd84a4ef34058191c |
| Ran by | warden on Opus 5 (1M context) |
| PR | #352 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 2, 3 and 4, all three in `tests/`. Findings 1 and 5 through 10 are corrections owed at the closing commit rather than a fix pass, and finding 1 is the one that must land before the pull request is read, because the `ledger` job is red without it. |
| Loses a record or crashes | no — nothing found leaves the root or crashes. Finding 1 fails a CI job; it does not lose or corrupt anything. |

- [ ] Pass

## What this round was asked

Round 1 of the work item, against the whole branch diff — 46 files, `origin/release/v0.11.0...HEAD`. Stage 1 against `spec.md`'s S1–S14 and `plan.md`'s Phases table; stage 2 on quality.

Four departures from written rules were named in the spawn prompt rather than left to be found, because each was a builder's decision recorded in the tree: a ledger row re-pointed where `CLAUDE.md:121` says REMOVED; the constant count diverging from `spec.md` §Data & interfaces; `plan.md` row 5's Status reading `deferred #350` where the template names two values; and `fold_ledger.py --check` exiting 1 by design on a feature branch.

Phase 5 is absent on purpose — deferred to #350 by the repository owner on 2026-09-11.

The ledger check was named in the UNSCOPED form, with the reason: three rounds of an earlier work item all ran the narrow form, all reported clean, and the unscoped read at the pull request found fifteen drifted rows and one broken claim. The broad gate was excluded under contract §2 as the sealer's one act.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | `bin/evidence-check` exits 2 at this SHA on seven `NOT-IN-TREE` refusals, and `test.yml`'s `ledger` job fails on any exit ≥ 2. Base exits 0 | `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/survivors.md:11`; `phases/phase-2.md:77`, `:133`, `:166`; `phases/phase-4.md:35`, `:36`, `:82` | open | Executed at base and at HEAD, exit codes read directly. Marking the seven lines in the clone took the run to exit 1 / `0 refused`, which CI renders as a warning. A record location, so a correction per `docs/review-chain-spec.md:155` — but the CI failure is live |
| 2 | `test_a_person_answerable_row_reaches_the_report_in_full` cannot fail: inverting the rule it exists for leaves it green | `tests/test_a_question_says_who_can_answer_it.py:121` | open | Executed. `agents/framer.md:223` inverted to its opposite, module run: 6 passed. Each of the four assertions is satisfied by text the inversion did not touch |
| 3 | `test_the_report_does_not_reduce_the_frame_to_counts` pins the phases half and not the out-of-scope half | `tests/test_a_question_says_who_can_answer_it.py:150` | open | Executed. `agents/framer.md:217` changed to a count, `-k` run: 1 passed, 5 deselected. `"out of scope"` is a heading fragment that survives the change |
| 4 | `BESIDE_THE_ROOT` does not carry `specseal-planner`, so the case its comment describes builds five of six | `tests/test_the_records_can_be_carried_out_and_in.py:55` | open | Executed. Adding the entry gives 96 passed, so the exclusion is structural and the list is merely stale. Two sibling enumerations were swept on this branch and this one was not |
| 5 | The new follow-up row sits outside its table and renders as literal text | `seal/follow-up.md:65-66` | open | Read, then checked against `tests/test_a_rider_reaches_its_file.py:52`: the parser still sees it, so no check is bypassed; only a human reader loses it |
| 6 | Five ledger rows were re-hashed with `Checked` left stale; two contradict their own `Notes` | `seal/ledger.md:275`, `:276`, `:277`, `:283`, `:284` | open | Executed against the diff: ten rows re-hashed, five moved 2026-09-10 → 2026-09-11, these five did not. `:275` and `:283` say **Re-read 2026-09-11** beside `Checked` cells of 2026-09-08 and 2026-09-02 |
| 7 | `the other two ship answered` is now a miscount, in the paragraph the new `Planning` comment redirects readers to | `templates/sdd-routing.md:59` | open | Read. Three other axes now, and `Planning` also ships as a placeholder |
| 8 | S10's acceptance row is the only place the #350 deferral is not written | `spec.md:87` | open | Read against seven places that do record it |
| 9 | The `specseal-planner` tree-diagram line is one column out in both editions | `docs/one-root-by-lifetime.md:111`, `docs/one-root-by-lifetime.ko.md:109` | open | Read |
| 10 | `plan.md`'s third `Status` value is argued only inside this work item; `templates/sdd-plan.md` still states two, and no follow-up row carries it | `plan.md:96-104`, `templates/sdd-plan.md:93` | open | Read. The argument is sound; it has no home the next work item reads |
| 11 | Named item 1 — the ledger row re-pointed rather than removed | `seal/ledger.md:275`, `CONTRIBUTING.md:105-119` | withdrawn | `CONTRIBUTING.md:116` names the rename case and sanctions `--reverify` re-anchoring. Phase 4b took the branch the rule assigns |
| 12 | Named item 2 — three constants where `spec.md` names four | `hooks/routing.py:61-66` | withdrawn | The fourth was an alias; `PLANNING_ANSWERS` says the thing by using `BY_SESSION`. Recorded as a divergence |
| 13 | Named item 3 — `deferred #350` as a `Status` value | `plan.md:90` | withdrawn | Satisfies the rule's stated reason; see finding 10 for the part still owed |
| 14 | Named item 4 — `fold_ledger.py --check` exit 1 on this branch | `plan.md` row 6, `.github/workflows/hygiene.yml:115` | withdrawn | Reproduced; the hygiene steps gate on `base_ref == main` and exit 0 early otherwise |
| 15 | The broad gate — full suite, repository-wide lint, typecheck | `seal/config.md` `Broad gate` row | ❓ out of verified scope | Contract §2 makes it one act with one owner and `agents/sealer.md` is the owner. Not run. Answerer: the orchestrator, through the sealer spawn |

## Paste-ready fixes

```
seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/survivors.md:11
phases/phase-2.md:77   phases/phase-2.md:133   phases/phase-2.md:166
phases/phase-4.md:35   phases/phase-4.md:36    phases/phase-4.md:82

Append to each line:  <!-- NAME NOT IN TREE: the name this branch removed, quoted as the record read it -->
```
```python
    assert "A row only a person can answer is reproduced in full" in report, (
        "the report no longer sends a person-answerable row's own text. "
        "Nobody can answer a question they were handed a count of, so a "
        "frame obeying the shorter rule ships an approval given against "
        "nothing"
    )
```
```python
    assert "What you put out of scope, and why, one line each" in report, (
        "the report gives a count of what was excluded instead of the "
        "exclusions. That is where a framing error hides: what was decided "
        "is visible and what was left out is not"
    )
```
```python
BESIDE_THE_ROOT = (
    "specseal-implementer",
    "specseal-planner",
    "specseal-reviewed",
    "specseal-parity",
    "specseal-scratch",
    "specseal-last-export.json",
    "specseal-session-lease",
)
```
```
seal/ledger.md:275   2026-09-08 -> 2026-09-11
seal/ledger.md:276   2026-09-02 -> 2026-09-11
seal/ledger.md:277   2026-09-05 -> 2026-09-11
seal/ledger.md:283   2026-09-02 -> 2026-09-11
seal/ledger.md:284   2026-09-02 -> 2026-09-11
```
```
     This one and the `Planning` row above ship as PLACEHOLDERS while
     `Review` and `Destination` ship answered, and the difference is
     deliberate:
```
```
| ~~S10 an agent's own wall clock is a number~~ — **deferred to #350**, milestone 0.11.1, on 2026-09-11 | ~~Given a transcript with subagent transcripts beside it · When `session-cost` runs in the new mode · Then one row per segment, named by the spawn's `subagent_type`, with its own span, calls and tokens — and the count of segments it could not name is printed rather than hidden~~ | ~~a new case over a built transcript tree, executed~~ — nothing in this work item answers it |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_implementer_is_recorded.py tests/test_routing_is_recorded.py` at target SHA, in the clone | 55 passed |
| `bin/test tests/test_the_records_can_be_carried_out_and_in.py` at target SHA | 96 passed |
| `bin/evidence-check` unscoped at target SHA, exit code read directly | ledger 1121 ok · 0 drifted · 0 broken; records 7 refused · 1 drifted; **exit 2** |
| `bin/evidence-check --strict` unscoped at target SHA | **exit 2** |
| `bin/evidence-check` unscoped at `origin/release/v0.11.0` | 1100 ok · 0 drifted · 0 broken; records 0 refused · 0 drifted; **exit 0** |
| `bin/evidence-check` with `NAME NOT IN TREE` added to the seven refused lines in the clone | 1121 ok · **0 refused** · 1 drifted; **exit 1** — which `test.yml` renders as a warning |
| `python3 .github/scripts/rider_check.py` at target SHA | 26 ok · 0 drifted; exit 0 |
| `python3 .github/scripts/fold_ledger.py --check` | exit 1 — the correct answer on a feature branch |
| `python3 .github/scripts/fold_ledger.py --version 0.11.0 --dry-run` | exit 0, wrote nothing |
| `python3 .github/scripts/gather_changelog.py --version 0.11.0 --dry-run` | exit 0, wrote nothing |
| Mutation: `agents/framer.md:223` inverted, then `bin/test tests/test_a_question_says_who_can_answer_it.py` | **6 passed** — the case cannot fail |
| Mutation: `agents/framer.md:217` reduced to a count, then `-k does_not_reduce_the_frame_to_counts` | **1 passed, 5 deselected** — half the case cannot fail |
| Mutation: `specseal-planner` added to `BESIDE_THE_ROOT`, module re-run | 96 passed — the exclusion is structural, the list is stale |
| Probe `test_tmp_notice_at_the_declaring_commit.py` — the notice against a `git commit` payload in three built repositories | Both axes unfulfilled → one line naming both; implementation only → byte-identical to the 0.7.0 wording; planning mark standing → speaks only for the axis that is missing. Deleted after the run |
| Broad gate — `bin/test -q && uvx ruff check . && uvx ruff format --check .` | **not yet** — not run by this round, and out of its scope |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the third routing axis's template pin should be widened the way the fourth's was | `seal/follow-up.md:66` — already open, and finding 5 is about how that row renders, not about re-opening it | the repository owner |
| Whether both README editions join `spec.md` §Scope item 8, and whether `agents/framer.md` preloads the two utility skills | `questions.md` Q4 — already open | the repository owner |
| Whether the records arm should tolerate a superseded coordinate quoted beside its successor | `overview.md:40` — already open; the DRIFTED line at `phases/phase-1.md:131` is exit-1 class and CI renders it as a warning | the repository owner |
| #350, the per-agent wall clock | `docs/flow.md:102` under 0.11.1, and `spec.md` §Scope item 7 | already scheduled |
