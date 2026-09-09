# Round 2 — the verifying round

Target SHA `2bb11cb`, fix range `2ef93a7..2bb11cb`, four commits. Branch
`chore/145-the-orchestrator-is-measured-by-the-whole-session`, base
`release/v0.9.5`, draft PR #294.

Round 1 was a correction that was mostly prose, and the prose was the defect.
This round was asked two things: whether the nine-plus-four pages now say
something true about where the delegated wall clock is, and whether the two
numbers the fix pass refused to paste were right to refuse.

**Both answers are yes, and the fix pass was right on all three disputed
numbers.** Round 1's report — mine — carried a five-point understatement that
would have reached the durable log, and refusing to paste it is what kept it
out.

**One defect is in the fix itself.** The printed line the finding-3 fix added
can read a negative and call it the wait, which is the same class of false
printed line this work item exists to close. It is one guard.

## The three disputed numbers, measured again from the transcripts

I did not take the fix pass's account. I identified the three runs
`reading.md` covers by re-deriving the whole band table from the raw
transcripts and matching it row for row, then measured each claim.

| What round 1's report said | What the fix pass said | Measured this round |
|---|---|---|
| between the rows is 12–26% | 12–31% | **12.0%, 25.6%, 30.7%** — the fix pass is right |
| the new case asserts `outside == 300`, `5.0m of the run's 5.3m` | 304, `5.1m` | **304** — 300 fails; the fix pass is right |
| five other rows over 5,000s | four, within the three runs | **four** in the three runs, five in the others — the fix pass is right |

The three runs are identified beyond doubt, and not by their command and
model minutes: their call counts sum to the 953 `reading.md` claims and their
cycle counts to the 61, and no other combination on this machine does.

| Run | transcript | span | calls | cycles | between the rows |
|---|---|---|---|---|---|
| 2026-09-06 | `ceebefcf…` | 546.2m | 309 | 12 | 167.6m — **30.7%** |
| 2026-09-07 | `fdbb7b51…` | 448.0m | 497 | 32 | 53.7m — **12.0%** |
| 2026-09-08 | `b4b80fbb…` | 164.0m | 147 | 17 | 41.9m — **25.6%** |
| — the fourth the report substituted | `2f8df1f8…` | 539.4m | 836 | 16 | 89.2m — 16.5% |

309 + 497 + 147 = 953. 12 + 32 + 17 = 61. The 539.4m transcript is a
2026-08-30 run of 836 calls and 16 cycles, and neither total admits it.

The whole band table reproduces exactly — head 3 rows at 9.4m median over
6.9–27.9m, `specseal:smith` 15 at 10.9m over 0.6–116.3m, `specseal:warden` 23
at 12.9m over 0.7–97.0m, batched 23 at 0.0m, tail 3 at 16.7m over
3.9–118.1m, and 67 rows carrying 953 calls. So the published page's numbers
are the three runs' numbers, and the report's were a fourth run's.

**On the four seconds the fix pass would not drop.** The case asserts 304 and
the reason it gives is exact: `spawn_cuts` opens its cut list at the first
spawn's *start*, so the head row's boundary is t=5 while the head's own last
call ends at t=1. Those four seconds are the head's last call to that cut,
and they are uncounted for the same reason the wait is. Measured on the
synthetic: run span 317s, rows 1s + 2s + 10s = 13s, outside 304s, printed as
`5.1m of the run's 5.3m`.

**On the 98 per cent.** Decomposing each run's interval into the wait after a
spawn's result and each row's last call to the next cut gives 98.2%, 99.6%
and 98.9% wait. `mostly` is earned and `98 per cent` is the floor of the
three, not an average — a reader checking the largest run will find 99.6.

**On the four long rows.** Within the three runs exactly four rows exceed
5,000s, with opening gaps 6s, 18s, 484s, 580s. Their above-ceiling internal
gaps are 1,038s, 1,076s, 1,397s, 2,297s, 2,745s and 6,285s, so
`reading.md`'s *internal gaps of 1,038 to 6,285* is the range of those and is
right. The 116.3m row is a `specseal:smith` cycle with 11.5m of parts and one
internal gap of 6,285s = 104.8m, opening gap 580s. Every figure on the page
checks.

## 🟡 1 — the new between-the-rows line can print a negative and call it the wait

`skills/verify/scripts/session_cost.py:1200-1212`

The finding-3 fix added a line that subtracts the rows' spans from the run's
span and prints the remainder as the interval between the rows. It is guarded
on `run_span > 0`, which is the wrong quantity: the guard cannot go negative
but the subtraction can.

`in_windows` assigns a call to a row by its **start**, which is what makes
the calls partition. It does not make the spans partition. A call that
outlives a spawn's result stays in the row it began in while the next row's
calls have already started, the two rows' spans overlap in time, and their
sum can exceed the run's span. `in_windows`' own docstring names this call —
*"one that outlived a report"* — and rules out putting it in two rows; the
sum over spans was not carried through the same reasoning.

Executed. A background command started in the head row, one spawn, then two
later calls:

```
run span_s = 995.0
  head span_s = 1000.0   cycle span_s = 2.0   tail span_s = 985.0
sum of row spans = 1987.0   outside = -992.0
```

and `--spawns` printed, exit 0:

```
  -16.5m of the run's 16.6m is BETWEEN the rows — mostly the wait
  after each spawn's result, in no column above
```

Why it matters: that is a printed sentence a reader acts on, asserting a
negative interval and naming it the delegated wait. It is the same class as
the nine pages round 1 closed — a line saying something false about where the
wall clock is — reintroduced by the fix for it. A background `Bash` call is
the ordinary way to reach it, and a long `gh` or suite call spanning a spawn
cut reaches it too.

The zero-spawn path is safe: `report_spawns` returns before this block.

Paste-ready fix below, with a case that fails against the code as it stands.

## ⬜ 2 — three `seal/ledger.md` rows were re-hashed and their `Checked` dates left behind

`seal/ledger.md:873` (F5) · `:1037` (R3) · `:1141` (G5)

`cca5861` edited `skills/verify/SKILL.md` under the heading three shared
ledger rows anchor at, so their content hash moved from `@9bf866ce` to
`@1b459b88`. The hashes were rewritten. The `Checked` dates were not: F5 and
R3 still read 2026-09-06 and G5 still reads 2026-09-08, against content
written on 2026-09-09.

`CLAUDE.md` says the `Checked` column holds the date somebody read the code,
and that re-verifying is re-reading and *then* running `--reverify`. The
command rewrites the hash and never touches the date — its own docstring says
recomputing the hash *"is a person saying they have re-read the code"*, and a
check that silently refreshed what it was checking *"would report OK
forever"*. With the date left behind, a reader cannot tell whether the three
claims were re-read against the new content or the hash was refreshed to keep
the check green. The checker cannot tell either: the tree reads 1007 ok, 0
drifted.

Location is `seal/ledger.md`, so this is a correction and not a round. The
tool-side half — that `--reverify` leaves no trace of when it wrote — is
handed over as a candidate rather than as a fix, because it predates this
branch.

## ⬜ 3 — "delegated wait" now names the opening gap, on pages that also name the column

`changelog.md:54` · `reading.md:58` · `overview.md:57` · `questions.md:48`

The corrected pages describe the four long rows as having *delegated waits of
6 to 580 seconds*, and the 116-minute row as having a *delegated wait of 580
seconds*. Those are the rows' **opening gaps**. The `delegated` column on
those same four rows reads 3s, 3s, 2s and 0s.

Under this branch's own thesis the opening gap is what the delegated wall
clock actually is, so the sentences are true. The trouble is that
`changelog.md` two paragraphs above says *"A `delegated` column of seconds is
the tell"*, and 6 seconds is inside that column's own range — so a reader has
nothing, neither vocabulary nor magnitude, to tell which quantity is meant.
That is the conflation round 1's finding 2 closed, one term over.

`changelog.md` is the one that reaches a reader: `gather_changelog.py` folds
it into the released `CHANGELOG.md`. Worth correcting before the release
gathers it. All four Locations are under `seal/specs/`, so this is a
correction.

## Round 1's five findings — what each one's fix or answer is worth

**Finding 1 holds, fixed.** The claim is gone from every live page and
survives only in the two round-1 records, where it belongs. Swept the tree
for `12-26`, `12 to 26`, `next row`, `in the model column`: every live
instance now reads 12-31% or says the wait is in no column, and the four
matches outside the records are `spec.md`'s and `questions.md`'s unrelated
*"the next row of this release"*. `phase-5.md` keeps the false conclusion as
what the phase concluded, corrected beside it — the right shape for a record.
`bin/survivor-check --range 2ef93a7..2bb11cb` examined 741 files against 59
removed sentences and reported no survivors, exit 0.

**Finding 2's answer is sound.** All four Locations are under `seal/specs/`,
and `docs/review-chain-spec.md:155` makes such a finding a correction rather
than a round in exactly those words. The row closes `answered` with the two
corrective SHAs in its grounds; the spec's literal form is `answered —
corrected at <sha>`, and the information is present either way.

**Finding 3 is fixed, and finding 🟡 1 above is in that fix.** The
`run_span` parameter, the printed line and `reading.md`'s legend are all
there. The line's own arithmetic is right on every real run and wrong in the
overlap case.

**Finding 4's answer is verified at the coordinates, not taken.**
`templates/sdd-phase.md:39-45` does permit the spawning session to fill the
row afterwards, in the words quoted. `e389fc1` touches five files with one
insertion and one deletion each — the five `Ran by` rows and nothing else.

**Finding 5's answer is verified by measurement and by tracing.**
`report(data)` never reads the `spawns` key, so the `None` the plain path now
passes cannot reach a reader — confirmed by reading every reference in the
function's body. `spawn_cycles`, `measure_cycles` and `report_spawns` each
have exactly one caller, all in-module, so removing the `turns=()` default
breaks nothing. The kept `spawn_cuts` re-run stands on its own grounds.

One nuance for the record on §15. The new case is genuinely red against
`2ef93a7` — it fails on the printed assertion, and the old code prints the
false *"inside the NEXT row down: in `model`"* sentence in its place. But
`assert outside == 304` passes on the old code too, because `outside` is a
property of `analyse` that the fix did not change. The case pins the
disclosure, not the arithmetic, and that is the half that would have caught
the defect.

**The `run_span=0.0` default is decorative.** Its only caller always passes
the argument, which is the same shape as the dead `turns=()` default finding
5 removed in the same commit. Nothing behaves wrong, so it is not a finding —
noted because the two decisions sit two hundred lines apart in one diff.

## The checker gap, since I was asked whether it is worse than reported

It is the same silence the module names as its own one unacceptable outcome.
`ANCHOR_RE` requires `@[0-9a-f]{6,12}`, so a coordinate whose hash is five
characters does not match the anchor pattern at all — and it does not match
`OLD_COORD_RE` either, which needs a `:<digits>`. The row is therefore not a
row: it contributes to no total, and `evidence_check.py`'s own comment above
`HASH_LEN` says a ledger full of unrecognised coordinates once read `0 ok · 0
drifted · 0 broken`, exit 0, *"which stripped an updating user's whole
coverage without one printed word."* A short hash reproduces that one row at
a time.

So the fix is not widening `{6,12}`. It is an arm that refuses a
hash-shaped coordinate the anchor pattern declined, because widening the
range moves the boundary and leaves the silence on the other side of it.
`HASH_LEN = 8` is what the writer emits, which bounds how a short hash
arrives — hand-editing, or a tool that truncates — but not what happens when
one does.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The new between-the-rows line prints a negative and calls it the wait, when a call outlives a spawn cut | `skills/verify/scripts/session_cost.py:1200` | open | **Executed.** Head-row background call 0-1000s, spawn at 5-7s, calls at 10-12s and 990-995s: run span 995s, row spans 1000 + 2 + 985 = 1987s, `outside` = -992s, and `--spawns` printed `-16.5m of the run's 16.6m is BETWEEN the rows — mostly the wait`, exit 0. The guard is on `run_span > 0`, which cannot go negative; the subtraction can, because `in_windows` partitions the CALLS by start and not the spans. `in_windows`' own docstring names the outliving call and rules out double-assignment, but the span sum was not carried through it. Zero-spawn path safe — `report_spawns` returns before the block |
| 2 | ⬜ Three shared-ledger rows re-hashed at `cca5861` with their `Checked` dates left behind | `seal/ledger.md:873` · `:1037` · `:1141` | open | **Executed** — extracted both versions: `@9bf866ce` → `@1b459b88` on F5, R3 and G5, while `Checked` stays 2026-09-06, 2026-09-06 and 2026-09-08 against content written 2026-09-09. **Read** — `reverify` at `evidence_check.py:1570` rewrites the hash and never the date, and its docstring makes recomputing the hash the person's assertion that they re-read. The tree reads 1007 ok · 0 drifted, so nothing catches it. Correction, not a round: Location is `seal/ledger.md` |
| 3 | ⬜ "delegated wait" names the opening gap on four pages that also name the `delegated` column | `changelog.md:54` · `reading.md:58` · `overview.md:57` · `questions.md:48` | open | **Executed** — the four rows over 5,000s carry `delegated_s` of 3s, 3s, 2s and 0s, while the pages' *delegated waits of 6 to 580 seconds* are their opening gaps, measured at 6s, 18s, 484s and 580s. True under the branch's thesis and unreadable beside `changelog.md`'s own *"a `delegated` column of seconds is the tell"*, since 6s is inside that column's range. `gather_changelog.py` folds the fragment into the released `CHANGELOG.md`, so this one reaches a reader. All Locations under `seal/specs/` — correction |
| 4 | Round 1 finding 1 — the wall clock in the next row's `model`, on nine pages | nine pages, per `round-1.md` | answered | **Confirmed fixed, and the report's two numbers were wrong.** The three runs are identified by call and cycle totals, not by minutes: 309 + 497 + 147 = 953 and 12 + 32 + 17 = 61, which no other combination on this machine gives. Between-the-rows measured at 30.7%, 12.0% and 25.6%, so **12-31% is right and the report's 12-26% was a five-point understatement** built on a 2026-08-30 transcript of 836 calls and 16 cycles that neither total admits. The whole band table reproduces row for row. Swept the tree: every live instance now reads 12-31%, the remaining `12-26` matches are the two round-1 records, and `phase-5.md` keeps the conclusion as the phase's own with the correction beside it. `survivor-check --range 2ef93a7..2bb11cb`: 741 files, 59 removed sentences, no survivors, exit 0 |
| 5 | Round 1 finding 2 — the 116-minute cycle credited to a subagent on four pages | four pages, per `round-1.md` | answered | **The answer is sound and the fix pass's count is right.** `docs/review-chain-spec.md:155` makes a finding whose Location is under `seal/specs/` a correction rather than a round, in those words, and all four Locations are. Executed on the rows: **four** rows over 5,000s within the three runs, five in the other transcripts — so the report's *five other rows* was counting across the machine. The 116.3m row is a `specseal:smith` cycle, 11.5m of parts, one internal gap of 6,285s = 104.8m, opening gap 580s. Above-ceiling internal gaps across the four rows are 1,038s to 6,285s, which is what the pages say |
| 6 | Round 1 finding 3 — the rows partition calls and not time | `session_cost.py:1120` · `:1181` · `reading.md:39` | answered | **Fixed, and the fix pass was right to refuse 300.** Executed on the synthetic: run span 317s, rows 1s + 2s + 10s = 13s, `outside` = **304s**, printed `5.1m of the run's 5.3m`. The stated reason is exact — `spawn_cuts` opens its cut list at the first spawn's START, so the head's boundary is t=5 while its last call ends at t=1, and those 4s are the head's last call to that cut. `mostly` is earned: the wait is 98.2%, 99.6% and 98.9% of the interval on the three runs, so `98 per cent` is the floor of the three. Finding 1 of this round is a defect inside this fix |
| 7 | Round 1 finding 4 — `overview.md` owes `Ran by` to the orchestrator | `overview.md:77` | answered | **Verified at the coordinates rather than taken.** `templates/sdd-phase.md:39-45` permits the spawning session to fill the row afterwards, in the quoted words, and `e389fc1` touches exactly five files with one insertion and one deletion each — the five `Ran by` rows and nothing else |
| 8 | Round 1 finding 5 — the re-run `spawn_cuts`, the plain-path `measure_cycles`, the dead default | `session_cost.py:719` · `:1236` · `:601` | answered | **Verified by tracing and by grep.** `report(data)` reads no `spawns` key anywhere in its body, so the `None` the plain path now passes reaches no reader. `spawn_cycles`, `measure_cycles` and `report_spawns` have one caller each, all in-module across the whole tree, so dropping `turns=()` breaks nothing. The kept `spawn_cuts` re-run stands on its measured grounds. §15 nuance: the new case is red against `2ef93a7` on its printed assertion, while `assert outside == 304` passes there too — the case pins the disclosure, which is the half that catches the defect |

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

Needs a fix: yes — finding 1, the between-the-rows line printing a negative and naming it the wait.
Loses a record or crashes: no

## Proof

Opened and read: `skills/verify/scripts/session_cost.py` (the whole diff plus
`spawn_cuts`, `in_windows`, `spawn_cycles`, `measure_cycles`,
`report_spawns`, `main`, `minutes`, and `report`'s body for the `spawns`
key) · `tests/test_session_cost.py` (the diff and the new case) ·
`skills/verify/SKILL.md:400-425` · `seal/ledger.md` at both SHAs, rows F5, R3,
G5 · `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md`
· the work item's `reading.md`, `overview.md`, `questions.md`, `changelog.md`,
`survivors.md`, `phases/phase-5.md`, `rounds/round-1.md` ·
`docs/review-chain-spec.md:155-181` · `templates/sdd-phase.md:15-50` ·
`skills/evidence-check/scripts/evidence_check.py` (`ANCHOR_RE`, `HASH_LEN`,
`reverify`) · `skills/code-review/scripts/round_record.py:2495-2535` ·
`bin/test`.

Executed: the fifteen probe rows above. Not executed: the broad gate, which
is the orchestrator's under §2, and mutation testing, which I did not re-run.
Nothing in the spawn prompt asked for a check §2 excludes.
