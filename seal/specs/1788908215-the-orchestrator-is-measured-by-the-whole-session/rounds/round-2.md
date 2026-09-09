# 1788908215-the-orchestrator-is-measured-by-the-whole-session — review round 2

| Field | Value |
|---|---|
| Target SHA | 2bb11cb |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #294 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | test_a_call_that_outlives_a_cut_prints_no_between_the_rows_figure (depth 1) |
| Needs a fix | yes — finding 1, the between-the-rows line printing a negative and naming it the wait. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round of a correction that was mostly prose, where the prose was
the defect. What it was asked is whether the nine-plus-four pages now say
something true about where the delegated wall clock is, and whether the two
numbers the fix pass refused to paste were right to refuse. The three
transcripts were identified by call and cycle counts rather than by minutes,
because the round-1 report had substituted one transcript for another. What
opened is the one line the correction itself prints.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The new between-the-rows line prints a negative and calls it the wait, when a call outlives a spawn cut | `skills/verify/scripts/session_cost.py:1200` | **fixed** `80528ab` | fixed at 80528ab — `` — the guard, the case seen red first, and the disclosure in `skills/verify/SKILL.md`. `01a8fa5` closes the same class in `report_spawns`' own docstring, which credited the negative guard to the `run_span` zero check. The refusal says the spans SUMMED PAST the run rather than naming an overlap of that size: `analyse` takes a span as the last call TO BEGIN's end minus the first call's start, so an outliving call shortens the run's span too and the difference carries both errors — the paste-ready wording *the rows' spans OVERLAP by 16.5m* would have stated a quantity nothing measured, which is a smaller instance of the class being closed. That span understatement is left standing as `questions.md` Q5; **Executed.** Head-row background call 0-1000s, spawn at 5-7s, calls at 10-12s and 990-995s: run span 995s, row spans 1000 + 2 + 985 = 1987s, `outside` = -992s, and `--spawns` printed `-16.5m of the run's 16.6m is BETWEEN the rows — mostly the wait`, exit 0. The guard is on `run_span > 0`, which cannot go negative; the subtraction can, because `in_windows` partitions the CALLS by start and not the spans. `in_windows`' own docstring names the outliving call and rules out double-assignment, but the span sum was not carried through it. Zero-spawn path safe — `report_spawns` returns before the block |
| 2 | ⬜ Three shared-ledger rows re-hashed at `cca5861` with their `Checked` dates left behind | `seal/ledger.md:873` · `:1037` · `:1141` | answered | corrected at `80528ab`. The three claims were re-read against the section as it now stands, not re-stamped on the strength of the hash: nine run-level table rows each naming its source, all three `usage` fields and the command in the counting rule, partial coverage in prose rather than as a column, no verdict, the rolling log rather than a third destination, the `Location` buckets, the `Broad gate` cell, and the main transcript named — F5's two labels with no issue number or title anywhere in the section, G5's two ends of the rolling log stated and no title. All three hold, so the dates move to 2026-09-09, the date that reading happened. The section moved again in this pass (`@1b459b88` → `@3123025c`) because finding 1's disclosure went into it, so the re-read was against the final content |
| 3 | ⬜ "delegated wait" names the opening gap on four pages that also name the `delegated` column | `changelog.md:54` · `reading.md:58` · `overview.md:57` · `questions.md:48` | answered | corrected at `80528ab`. All four pages now say *opening gap* with the `delegated` column's own reading beside it. §12 found two more instances the finding did not name: `seal/ledger/<work-item-id>.md` row 10, whose grounds said *a delegated wait of 580s*, and `reading.md`'s closing section, which asserted the identity one term over — *the time between the rows, which is the delegated wait* — beside a column reading seconds. Six live instances in total; what still carries the phrase names the defect rather than asserting it |
| 4 | Round 1 finding 1 — the wall clock in the next row's `model`, on nine pages | nine pages, per `round-1.md` | answered | **Confirmed fixed, and the report's two numbers were wrong.** The three runs are identified by call and cycle totals, not by minutes: 309 + 497 + 147 = 953 and 12 + 32 + 17 = 61, which no other combination on this machine gives. Between-the-rows measured at 30.7%, 12.0% and 25.6%, so **12-31% is right and the report's 12-26% was a five-point understatement** built on a 2026-08-30 transcript of 836 calls and 16 cycles that neither total admits. The whole band table reproduces row for row. Swept the tree: every live instance now reads 12-31%, the remaining `12-26` matches are the two round-1 records, and `phase-5.md` keeps the conclusion as the phase's own with the correction beside it. `survivor-check --range 2ef93a7..2bb11cb`: 741 files, 59 removed sentences, no survivors, exit 0 |
| 5 | Round 1 finding 2 — the 116-minute cycle credited to a subagent on four pages | four pages, per `round-1.md` | answered | **The answer is sound and the fix pass's count is right.** `docs/review-chain-spec.md:155` makes a finding whose Location is under `seal/specs/` a correction rather than a round, in those words, and all four Locations are. Executed on the rows: **four** rows over 5,000s within the three runs, five in the other transcripts — so the report's *five other rows* was counting across the machine. The 116.3m row is a `specseal:smith` cycle, 11.5m of parts, one internal gap of 6,285s = 104.8m, opening gap 580s. Above-ceiling internal gaps across the four rows are 1,038s to 6,285s, which is what the pages say |
| 6 | Round 1 finding 3 — the rows partition calls and not time | `session_cost.py:1120` · `:1181` · `reading.md:39` | answered | **Fixed, and the fix pass was right to refuse 300.** Executed on the synthetic: run span 317s, rows 1s + 2s + 10s = 13s, `outside` = **304s**, printed `5.1m of the run's 5.3m`. The stated reason is exact — `spawn_cuts` opens its cut list at the first spawn's START, so the head's boundary is t=5 while its last call ends at t=1, and those 4s are the head's last call to that cut. `mostly` is earned: the wait is 98.2%, 99.6% and 98.9% of the interval on the three runs, so `98 per cent` is the floor of the three. Finding 1 of this round is a defect inside this fix |
| 7 | Round 1 finding 4 — `overview.md` owes `Ran by` to the orchestrator | `overview.md:77` | answered | **Verified at the coordinates rather than taken.** `templates/sdd-phase.md:39-45` permits the spawning session to fill the row afterwards, in the quoted words, and `e389fc1` touches exactly five files with one insertion and one deletion each — the five `Ran by` rows and nothing else |
| 8 | Round 1 finding 5 — the re-run `spawn_cuts`, the plain-path `measure_cycles`, the dead default | `session_cost.py:719` · `:1236` · `:601` | answered | **Verified by tracing and by grep.** `report(data)` reads no `spawns` key anywhere in its body, so the `None` the plain path now passes reaches no reader. `spawn_cycles`, `measure_cycles` and `report_spawns` have one caller each, all in-module across the whole tree, so dropping `turns=()` breaks nothing. The kept `spawn_cuts` re-run stands on its measured grounds. §15 nuance: the new case is red against `2ef93a7` on its printed assertion, while `assert outside == 304` passes there too — the case pins the disclosure, which is the half that catches the defect |

## Paste-ready fixes

```python
    # The rows partition the CALLS. They do not partition the TIME: a row's
    # `span` starts at its own first call, so the wait after each spawn's
    # result is between two rows and in no column. Printed because it is
    # 12-31% of a measured run, and a reader adding the span column has no
    # other way to learn the total is short. `mostly` is measured: the wait
    # is 98% of the interval and the rest is each row's last call to the cut.
    #
    # And the subtraction can come out NEGATIVE, which is not an interval and
    # must not be printed as one. `in_windows` assigns a call by its start,
    # so a call that OUTLIVES a spawn's result stays in the row it began in
    # while the next row's calls have already started: the two rows' spans
    # overlap and can sum past the run. A background command in the head row
    # printed `-16.5m of the run's 16.6m is BETWEEN the rows — mostly the
    # wait`, which is the class of false printed line #145 exists to close.
    if run_span > 0:
        outside = run_span - sum(
            row["numbers"]["span_s"] for row in rows if row["numbers"]
        )
        if outside >= 0:
            print(
                f"  {minutes(outside)} of the run's {minutes(run_span)} is BETWEEN "
                f"the rows — mostly the wait\n  after each spawn's result, in no "
                "column above"
            )
        else:
            print(
                f"  the rows' spans OVERLAP by {minutes(-outside)} — a call "
                "outlived a spawn's\n  result, so this run has no "
                "between-the-rows figure to give"
            )
```
```python
def test_a_call_that_outlives_a_cut_is_reported_as_an_overlap(tmp_path):
    """The rows partition the CALLS, and the difference can go the other way.

    `in_windows` assigns a call by its start, so a call that outlives a
    spawn's result stays in the row it began in while the next row's calls
    have already started. The two rows' spans then overlap and can sum past
    the run, and the subtraction the between-the-rows line prints is not an
    interval. It printed `-16.5m of the run's 16.6m is BETWEEN the rows --
    mostly the wait`: a negative interval, named as the delegated wait, in
    the one report this work item exists to make honest."""
    lines = call("bg", 0, 1000, "npm run dev")
    lines += spawn("A", 5, 7, "specseal:smith")
    lines += call("b", 10, 12, "git status --short")
    lines += call("c", 990, 995, "git log --oneline -5")
    path = tmp_path / "outlives.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    spans = sum(row["numbers"]["span_s"] for row in rows if row["numbers"])
    data = json.loads(run(["--json", str(path)]).stdout)
    # The premise: the spans overlap, so they sum past the run's own span.
    assert spans > data["span_s"], (spans, data["span_s"])
    out = " ".join(run(["--spawns", str(path)]).stdout.split())
    assert "the rows' spans OVERLAP by 16.5m" in out, out
    assert "is BETWEEN the rows" not in out, out
```
```
seal/ledger.md, the Checked cell of rows F5 (:873), R3 (:1037) and G5 (:1141)

Re-read the three claims against `skills/verify/SKILL.md` under
"## Measure the segment, and feed the flow log" as `cca5861` left it, then
set each row's Checked cell to the date that reading happened. If the three
claims were NOT re-read and only the hash was refreshed, say so in the row
instead: the point of the column is that a person can tell the two apart.
```
```
seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/changelog.md:54

  three runs measured decomposes that way, with opening gaps of 6 to 580
  seconds beside internal gaps of 1,038 to 6,285. The `delegated` column
  reads 0 to 3 seconds on those same four rows, which is the point: the
  agent's wall clock is the opening gap and never the column named for it.

(and the same substitution of `opening gap` for `delegated wait` in
reading.md:58, overview.md:57 and questions.md:48)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q` in a `--no-local` clone at `2bb11cb` | 65 passed in 2.50s, exit 0 — one more than round 1's 64 |
| The new case against `2ef93a7`, with `2bb11cb`'s test file overlaid on the pre-fix module | 1 failed, exit 1 — red at `assert "in NONE of the columns above" in out`, and the old code printed *"inside the NEXT row down: in `model` while the wait stays under the 15 minutes"* in its place. `assert outside == 304` passes on the old code too |
| Every orchestrator-shaped transcript under `/Users/x/.claude/projects/…`, loaded through the module: run span, calls, cycles, sum of row spans, between-the-rows share | 11 transcripts with spawns. The three the reading covers: 546.2m/309/12/167.6m/**30.7%**, 448.0m/497/32/53.7m/**12.0%**, 164.0m/147/17/41.9m/**25.6%**. The report's fourth: 539.4m/836/16/89.2m/16.5%, first call 2026-08-30. 309+497+147 = 953 and 12+32+17 = 61, matching the page |
| The band table re-derived from the three transcripts and compared row for row | Exact on all five rows and both totals: head 3/9.4m/6.9-27.9m/2.3m/5.1m/27, smith 15/10.9m/0.6-116.3m/1.1m/5.4m/13, warden 23/12.9m/0.7-97.0m/0.7m/8.5m/13, batched 23/0.0m/0.0-0.1m/1, tail 3/16.7m/3.9-118.1m/0.9m/15.7m/14; 67 rows, 953 calls |
| Each run's between-the-rows interval decomposed into the wait after a spawn's result and each row's last call to the next cut | Wait is 98.2%, 99.6% and 98.9%. The remainder is 0.8m, 0.6m and 0.6m, matching the new case's comment |
| Every row over 5,000s in the three runs, with opening gap, above-ceiling internal gaps and `delegated_s` | Four rows. Opening gaps 6s, 18s, 484s, 580s. `delegated_s` 0s, 3s, 3s, 2s. Above-ceiling internal gaps 1,038s, 1,076s, 1,397s, 2,297s, 2,745s, 6,285s. The 116.3m row: smith, 11.5m of parts, 6,285s internal, 580s opening. Five more such rows in the other transcripts |
| The synthetic case decomposed — head, cycle and tail spans against the run's | Run span 317s; rows 1s, 2s, 10s; sum 13s; `outside` 304s. The 4s is the head's last call (end t=1) to the cut at the first spawn's start (t=5) |
| Probe: a call outliving a spawn cut — background command 0-1000s, spawn 5-7s, calls 10-12s and 990-995s | Run span 995s, row spans 1987s, `outside` -992s. `--spawns` printed `-16.5m of the run's 16.6m is BETWEEN the rows — mostly the wait`, exit 0. Finding 1 |
| `bin/survivor-check --range 2ef93a7..2bb11cb` | 741 files examined at `2bb11cb` against 59 removed sentences — no removed wording still standing, exit 0 |
| `python3 skills/evidence-check/scripts/evidence_check.py .` | 1007 ok · 0 drifted · 0 broken · 0 external · 0 old-format, the work item's fragment 9 ok, exit 0 |
| `tests/test_no_real_identifiers.py` | 2 passed, exit 0 |
| Tree sweep for `12-26`, `12 to 26`, `next row`, `in the model column`, `12-31` | Every live page reads 12-31%. The `12-26` matches are `round-1.md` and `round-1-report.md` alone; the `next row` matches outside the records are `spec.md`'s and `questions.md`'s unrelated *"the next row of this release"* |
| Callers of `report_spawns`, `spawn_cycles`, `measure_cycles` across the tree; `report()`'s body read for the `spawns` key | One in-module caller each, none elsewhere. `report()` reads no `spawns` key, so the plain path's `None` reaches no reader |
| `seal/ledger.md` at both SHAs, hashes and `Checked` dates extracted | F5, R3, G5 re-hashed `@9bf866ce` → `@1b459b88`; `Checked` unchanged at 2026-09-06, 2026-09-06, 2026-09-08. Finding 2 |
| `e389fc1 --stat` | Five phase records, one insertion and one deletion each, nothing else |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:1144` · `:231` · `:632` · `skills/verify/SKILL.md:413` · `changelog.md:41` · `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:8` · `reading.md:71` · `overview.md:46` · `questions.md:39` · `tests/test_session_cost.py:2048` | round 1's 1 — fixed |
| round-1 | `reading.md:74` · `overview.md:47` · `questions.md:41` · `changelog.md:43` | round 1's 2 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:1120` · `:1181` · `reading.md:39` | round 1's 3 — fixed |
| round-1 | `overview.md:77` | round 1's 4 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:719` · `:1236` · `:601` | round 1's 5 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `--reverify` rewrites a hash and leaves no trace of when it wrote, so a re-anchored row can show a `Checked` date older than the content it hashes | candidate for `seal/follow-up.md` — it predates this branch and every `--reverify` run has had it | the orchestrator |
| `evidence_check` silently skipping a coordinate whose hash is under six hex characters | already with the orchestrator | the orchestrator — my read of the severity is in this report |
| The empty code span beside each SHA in `round-1.md` rows 1 to 3 | already known and RIDER-documented at `round_record.py#fix_table`, which names it as a prior round's finding and sends it to `seal/follow-up.md`; it predates this branch | already recorded — not re-opened here |
| What `delegated_s` should measure now the premise under it is false | `questions.md` Q4, three costed answers | the owner |
| A spawn's prompt classified as a command line in the whole-run reading | `seal/follow-up.md` | the owner |
| The full suite, repository-wide lint, typecheck | not run — `skills/agent-contract/SKILL.md` §2 | the orchestrator, once, and it is now due on finding 1's fix |
| 20 mutations, 0 survivors on the final code | the implementer's claim; I did not re-run mutation testing | the orchestrator |
| Windows | #103's standing gap | nobody has run it |
