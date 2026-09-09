# 1788908215-the-orchestrator-is-measured-by-the-whole-session — review round 1

| Field | Value |
|---|---|
| Target SHA | e389fc11a036e427f7a2b6f3aed0da65d22ed241 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #294 |
| Broad gate | not yet — the orchestrator's, once, after the rounds settle (contract §2) |
| Fixes checked by | round-2 |
| Contract changes | spawn_cycles → phase-1.md, plan.md, measure_cycles; report_spawns → round-1-report.md, round-1.md, main |
| New units | test_the_delegated_wait_is_in_no_column_of_any_row (depth 1) |
| Needs a fix | yes — findings 1 and 2, the false statement of where the delegated wall clock is and the false attribution of the published 116-minute cycle, in the code's printed report, `skills/verify/SKILL.md`, both fragments, the ledger row and the reading about to be posted; and finding 3, the missing disclosure that the rows do not partition the time. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The first review of a mode that produces a published number, built on a
premise its own construction measured false. What the round was asked is
whether the code does what the approved documents say, and whether every page
a reader meets is true about what the numbers mean. The class to enumerate was
the partition arms — head, each cycle, tail — and the report's two-armed
disclosure line. The broad gate was out of scope (§2), and the whole-run
family misclassification was declared deferred in `seal/follow-up.md` before
the round began.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The agent's wall clock is in no column of any row; nine pages say it is in the next row's `model` under fifteen minutes | `skills/verify/scripts/session_cost.py:1144` · `:231` · `:632` · `skills/verify/SKILL.md:413` · `changelog.md:41` · `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:8` · `reading.md:71` · `overview.md:46` · `questions.md:39` · `tests/test_session_cost.py:2048` | **fixed** `33a6fc7` | fixed at 33a6fc7 — `` for the three code sites, `cca5861` for the shipped skill, both fragments, the ledger row, `reading.md`, `overview.md` and `questions.md`, `46c3e04` for `phase-5.md`. Opened and confirmed by execution before fixing: `analyse` starts `span_s` at `calls[0]["start"]` and its model walk adds no gap while `turn_key is None`, so a 300s sub-ceiling wait lands in no column — probe on a synthetic run and on all eight orchestrator transcripts on this machine. **Two numbers in the finding are wrong and were not pasted.** The three runs `reading.md` covers are identified by their command and model minutes as the 546.2m, 448.0m and 164.0m transcripts; the report's table substituted a fourth transcript (539.4m, first call 2026-08-30) for the 2026-09-06 run and reported 16.5% where that run is 30.7%. The published range is therefore **12-31%**, not 12-26%. §12: the class is *the wait is in the model column*, and two instances the finding did not name — the `DELEGATING` comment's *that one is in the model column* and the ledger row's Notes cell — were fixed with it, plus two in Q4's own option table; Executed: `analyse:466` skips a window's opening gap and `:446` starts the span at the first call, so the interval is in no column. 17 of 18 opening gaps under the ceiling in the 2026-09-08 run, totalling 1,507s, none in `model_s`; the row quoted as 768s reads a 64s span. Synthetic control with a 300s wait: tail row 10s/5s/5s |
| 2 | The published 116-minute cycle is one internal 104.8m idle gap, not a subagent's run, and four pages credit it to the delegated wait passing the ceiling | `reading.md:74` · `overview.md:47` · `questions.md:41` · `changelog.md:43` | answered | **corrected at `cca5861` and `46c3e04`.** Every Location is under `seal/specs/`, so this is a correction rather than a round (`docs/review-chain-spec.md` §*A finding located in a record is a correction, not a round*). The finding holds and was executed on the row itself: span 6,979s against 11.5m of parts, one internal gap of 6,285s (104.8m) before a `cd` shell call, opening gap 580s — under the ceiling. Corrected on all four pages, and each now separates the two quantities. The report's *five other rows over 5,000s* counts across all eight transcripts; within the three runs the reading covers there are **four** such rows, opening gaps 6s-580s, internal gaps 1,038s-6,285s, and that is what the pages say |
| 3 | The rows partition calls and not time; the report asserts the first, `reading.md` calls a row's span wall clock, and 12–26% of each run lies between the rows | `skills/verify/scripts/session_cost.py:1120` · `:1181` · `reading.md:39` | **fixed** `33a6fc7` | fixed at 33a6fc7 — `` for `report_spawns`' new `run_span` parameter and the printed between-the-rows line, `cca5861` for `reading.md`'s legend. Executed: 167.6m of 546.2m, 53.7m of 448.0m, 41.9m of 164.0m. The line says **mostly** the wait rather than the wait, because the interval also holds each row's last call to the next cut — measured at 98% wait, and the new case pins both parts on a 304s total that is 300s of wait plus 4s of head. The finding's two smaller points are accepted as stated: the call tally cannot disagree, and the legend now explains `span`; Executed: 89.2m of 539.4m, 53.7m of 448.0m, 41.9m of 164.0m outside every row's span. The call tally cannot disagree — both sides come from one list through `in_windows` |
| 4 | `overview.md` still owes `Ran by` to the orchestrator; the target SHA filled it | `overview.md:77` | answered | **corrected at `cca5861`.** Location is `overview.md:77`, under `seal/specs/`. Judged at the coordinates rather than taken from the report: all five phase records read `specseal:smith on claude-opus-5`, and `templates/sdd-phase.md` permits the spawning session to fill the row afterwards — *"or fills the row afterwards, the reach-back `Fixes checked by` and the fix-surface rows already make"* — which is the shape of `e389fc1`, a commit touching those five rows and nothing else. Marked ✅ with what closed it, never deleted, and the answerer cell replaced so the closing is not left unproven (`skills/implement/SKILL.md` §4) |
| 5 | `spawn_cuts` re-run for a count already computed; `measure_cycles` computed on the plain path; a dead `turns=()` default | `skills/verify/scripts/session_cost.py:719` · `:1236` · `:601` | **fixed** `33a6fc7` | fixed at 33a6fc7 — ``. Two of the three: `measure_cycles` is no longer computed on the plain printed path, which does not read the key — measured at 25.5ms against `analyse`'s own 42.6ms on a 497-call transcript with 32 spawns, so it was half again the cost of the reading being printed; and `spawn_cycles`' `turns=()` default is removed, unreachable by grep across the tree and the tests. **The third is answered rather than fixed.** `measure_cycles` re-running `spawn_cuts` for its count costs 0.019ms of that 25.5ms — 0.07% — and it cannot disagree with the rows, being the same pure function on the same list. Every way of removing it either changes `spawn_cycles`' return shape, which two ledger rows are anchored at, or derives the count as `len(rows) - 2`, replacing a direct read with an identity a reader has to reconstruct; Read at the coordinates |

## Paste-ready fixes

```python
    if delegated_max < 60:
        print(
            f"\n  `delegated` never reaches a minute here — {delegated_max:.0f}s at "
            "most — so on this\n  harness the `Agent` result is written when the "
            "spawn is ACCEPTED rather than\n  when its report arrives. The agent's "
            "own wall clock is then in NONE of the\n  columns above, in this row or "
            "any other: it is the gap between one row's\n  last call and the next "
            "row's first, and a row's `span` starts at its own\n  first call while "
            "`model` never counts the gap before it. Its own transcript\n  under "
            "`<session-id>/subagents/` is where that number is."
        )
```
```python
# spawn is ACCEPTED, the agent then runs for a median of about 1,000 seconds,
# and that interval is in NO column of any row. It is the gap between the
# cycle that spawned and the next row's first call: `analyse` starts a
# window's `span_s` at that first call and never counts the gap before it,
# whether the wait is above the 900-second ceiling or below it. Measured over
# the same three runs, that is 12-26% of each run's wall clock.
```
```python
    **The waiting is NOT in that band on the harness measured in
    `DELEGATING`, and a reader has to know where it went.** A subagent runs
    for a median of about 1,000 seconds there while the orchestrator issues
    nothing, and that whole interval falls between two rows: it precedes the
    next row's first call, where `span_s` begins and where the model walk
    starts counting. So a cycle's `model_s` is the orchestrator's own gaps
    and not the wait, the rows partition the run's CALLS rather than its
    time, and 12-26% of a measured run's wall clock is in no row at all.
```
```markdown
   Where a harness writes it when the spawn is ACCEPTED, the column reads
   seconds and the agent's own wall clock is in **none** of the row's
   columns and none of any other row's. It is the gap between one row's last
   call and the next row's first, and a row's span starts at its own first
   call while its model time never counts the gap before it. So the rows
   partition the run's calls and not its wall clock — measured at 12 to 26
   per cent of a run — and the agent's own transcript is where its number
   is, either way.
```
```markdown
  when the spawn is **accepted**, the agent then runs for a median of about
  1,000 seconds, and that wall clock is in none of the columns of any row: it
  falls between two rows, because a row's span starts at its own first call
  and its model time never counts the gap before it. So the rows partition
  the run's calls and not its wall clock, and the table prints how much time
  sits between them. A `delegated` column of seconds is the tell, and the
  report prints the sentence saying so rather than leaving a reader to take
  zeroes for *nothing was delegated*.
```
```markdown
The wait then shows in NO column of any cycle row -- 351s, 768s and 962s measured after three consecutive spawn results, each of them the opening gap of the row that follows, and 17 of one run's 18 opening gaps are under the 900s ceiling and in `model_s` for none of them. `analyse` starts a window's `span_s` at its first call and never counts the gap before it, so 12-26% of a run's wall clock falls between the rows
```
```markdown
So the delegated wall clock is **not** in the column named for it, and it is
not in any other column either. It falls **between** two rows: a row's
`span` starts at its own first call, and its `model` never counts the gap
before that call, so the wait after a spawn's result belongs to no row at
all. On these three runs that is 89.2m of 539.4m, 53.7m of 448.0m and 41.9m
of 164.0m — 12 to 26 per cent of each run's wall clock, sitting between the
rows. The exclusion `--spawns` performs is therefore correct and nearly free
here rather than wrong, and it is the whole answer on a harness that writes
the result at completion. What `delegated` should measure instead has three
costed answers in the work item's `questions.md` Q4 and is the owner's call;
the join a future answer needs is already exact, since a subagent
transcript's first stamp **is** its spawn's result stamp.

Read the bands with that in mind: a cycle's `model` is the orchestrator's own
gaps and **not** the wait, which is outside the table entirely.
```
```markdown
The whole-run *in no column* figures above are a different thing again, and
one smith cycle shows why: it reads a 116-minute span against 11.5 minutes of
parts, and the 104.8 minutes between them is a **single gap inside the
cycle** — the orchestrator issuing nothing between two of its own calls,
above the 900 seconds `analyse` stops counting a gap at. That row's delegated
wait is 580 seconds. Every row over 5,000 seconds in these three runs
decomposes the same way, so a long cycle span is a reading about the
orchestrator's own idle time and never about a subagent's run.
```
```python
    print(
        f"\n  {plural(counted, 'call')} over the rows above, of "
        f"{plural(total_calls, 'call')} in the transcript"
    )
    # The rows partition the CALLS. They do not partition the time: a row's
    # `span` starts at its own first call, so the wait after each spawn's
    # result is between two rows and in no column. Printed because it is
    # 12-26% of a measured run, and a reader adding the span column has no
    # other way to learn it is short.
    if run_span > 0:
        outside = run_span - sum(
            row["numbers"]["span_s"] for row in rows if row["numbers"]
        )
        print(
            f"  {minutes(outside)} of the run's {minutes(run_span)} is BETWEEN "
            f"the rows — the wait after each\n  spawn's result, in no column "
            "above"
        )
```
```python
def report_spawns(spawns, path, total_calls, run_span=0.0):
```
```python
    if args.spawns and not args.json:
        report_spawns(
            spawns, path, len(calls), timings["span_s"] if timings else 0.0
        )
        return 0
```
```markdown
A row's `span` runs from its own first call to its own last, which is not the
whole window: the wait after each spawn's result is between two rows and in
no column. `command` is tools running; `model` is the gap between one turn's
last result and the next turn's first call, inside a row only. Medians, with
the full range beside the span.
```
```python
def test_the_delegated_wait_is_in_no_column_of_any_row(tmp_path):
    """Where the agent's wall clock actually goes, on the ACCEPTED harness.

    A window's `span_s` starts at its own first call and the model walk never
    counts the gap before that call, so the wait after a spawn's result is in
    no column of the row that follows it — under the 900s ceiling as much as
    above it. Nine pages said it was in the next row's `model` while it
    stayed under fifteen minutes; this is the case that would have caught
    that, and it is the number a reader of the band table needs."""
    lines = call("z", 0, 1, "git status --short")
    lines += spawn("A", 5, 7, "specseal:smith")
    # 300s of silence: the agent running, well under the 900s ceiling.
    lines += call("b", 307, 310, "git log --oneline -5")
    lines += call("c", 315, 317, "cat seal/specs/x/spec.md")
    path = tmp_path / "accepted.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    tail = rows[-1]["numbers"]
    assert tail["span_s"] == 10, tail  # 307 to 317, not 7 to 317
    assert tail["model_s"] == 5, tail  # 315-310 alone; the 300s is not here
    assert tail["command_s"] == 5, tail
    assert tail["delegated_s"] == 0.0, tail
    data = json.loads(run(["--json", str(path)]).stdout)
    outside = data["span_s"] - sum(
        row["numbers"]["span_s"] for row in rows if row["numbers"]
    )
    assert outside == 300, outside  # the whole wait, in no row
    out = run(["--spawns", str(path)]).stdout
    assert "in NONE of the" in " ".join(out.split()), out
    assert "5.0m of the run's 5.3m is BETWEEN the rows" in " ".join(out.split()), out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q` in a `--no-local` clone at the target SHA | 64 passed in 2.68s, exit 0 |
| `python3 skills/evidence-check/scripts/evidence_check.py .` | 1007 ok · 0 drifted · 0 broken · 0 external · 0 old-format; the work item's fragment 9 ok. Exit 0 |
| `tests/test_no_real_identifiers.py` | 2 passed |
| Probe: the module imported, `spawn_cycles` run over the four orchestrator-shaped transcripts in this project, each row's opening gap computed against its own cut and compared with the row's `model_s` | Every opening gap is outside its row's `span_s`, `command_s`, `model_s` and `delegated_s`. 2026-09-08: 17 of 18 under the 900s ceiling, 1,507s total, none in `model_s`. 2026-09-07: 32 of 33 under it, 2,001s total |
| Probe: a synthetic transcript — one spawn accepted at +2s, then 300s of silence, then two calls | Tail row span 10s, command 5s, model 5s, delegated 0. The 300s is in no column of any row |
| Probe: decomposition of every row with a span over 5,000s | The published 116.3m row is one internal gap of 6,285s (104.8m) before a shell call; its opening gap is 580s. Five other rows: internal gaps of 1,327s to 226,102s, opening gaps 18s–835s |
| Probe: sum of the rows' spans against the run's span | 89.2m of 539.4m (16.5%) · 53.7m of 448.0m (12.0%) · 41.9m of 164.0m (25.6%) lie between the rows |
| The ledger's twelve `parse_time`-ordered sites, counted at the coordinates | Six subtractions and six orderings; the correction is right and four orderings are this branch's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| What `delegated_s` should measure now the premise under it is false | `questions.md` Q4, three costed answers | the owner |
| A spawn's prompt classified as a command line in the whole-run reading | `seal/follow-up.md` | the owner |
| The full suite, repository-wide lint, typecheck | not run — `skills/agent-contract/SKILL.md` §2 | the orchestrator |
| 20 mutations, 0 survivors on the final code | the implementer's claim; I did not re-run mutation testing | the orchestrator |
| `bin/survivor-check` — it requires `--range A..B` and I did not run it. The ten excused rows read as sound grounds | `survivors.md` | the orchestrator |
| Windows | #103's standing gap | nobody has run it |
