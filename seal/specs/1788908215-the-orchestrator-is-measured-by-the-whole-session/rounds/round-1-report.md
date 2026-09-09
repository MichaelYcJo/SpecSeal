# Round 1 — the orchestrator is measured by the whole session (#145)

| Field | Value |
|---|---|
| Target SHA | `e389fc11a036e427f7a2b6f3aed0da65d22ed241` |
| Branch | `chore/145-the-orchestrator-is-measured-by-the-whole-session`, base `release/v0.9.5` |
| Inherited | nothing — `rounds/` was empty |

## What the round found, in one shape

The partition works. The exclusion works. What does not work is the sentence
that tells a reader where the missing time went.

`analyse` never counts the gap before a window's first call, and a window's
`span_s` runs from its first call to its last rather than from cut to cut. So
the interval between a spawn's result and the next row's first call — which on
this harness is the subagent's whole run — is outside every row's `span_s`,
`command_s`, `model_s` and `delegated_s`. Nine pages say it is in the next
row's `model` while it stays under fifteen minutes. Measured on the three
transcripts the reading covers, it is in none of them.

The two findings below are that one cause seen from two sides. The first is
where the wall clock is; the second is which minutes the published
116-minute cycle is actually made of. Both reach `reading.md`, which is the
artifact meant to outlive the release.

---

## 🔴 1 — the agent's wall clock is in no column of any row, and every page says it is in the next row's `model`

**Location** — `skills/verify/scripts/session_cost.py:1144` (the printed
sentence), and the same claim at `:231`, `:632`;
`skills/verify/SKILL.md:413`; `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/changelog.md:41`;
`seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:8`;
`seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/reading.md:71`;
`overview.md:46`; `questions.md:39`; `tests/test_session_cost.py:2048`.

**The cause, at two lines.** `analyse`'s model walk opens with
`turn_key = turn_end = None` and adds a gap only `if turn_key is not None`
(`session_cost.py:466`), so the gap preceding a window's first call is never
counted — correct for the whole run, where there is no prior turn, and wrong
for a slice, where the prior turn is in the window before. And `span_s` is
`calls[-1]["end"] - calls[0]["start"]` (`:446`), so the same interval is
outside the row's span as well.

**Executed**, over the three transcripts `reading.md` covers, with the module
imported and each row's opening gap computed against its own cut:

- 2026-09-08 run — 17 of its 18 opening gaps are under the 900-second
  ceiling and total 1,507s. Not one of them is in its row's `model_s`.
- The three gaps the ledger row and `reading.md` both quote as the
  measurement — 351s, 768s, 962s — are that run's cycle 10, cycle 14 and
  tail opening gaps. Cycle 14 reads a 64s span with 12s of command and 50s
  of model, while 768 seconds of wall clock passed inside its own window.
- Synthetic control: one spawn accepted at +2s, the agent running 300s (well
  under the ceiling), then two calls. The tail row reads span 10s, command
  5s, model 5s. The 300s is in nothing.

**Why it matters beyond the wording.** `reading.md` closes §1 with *"Read the
bands with that in mind: a cycle's `model` is mostly the orchestrator
waiting, not the orchestrator thinking."* The opposite is true — the waiting
is excluded, so a cycle's `model_s` is the orchestrator's own gaps. That
sentence is the interpretation key for the band table being posted to the
durable log as the reference every later reading is compared against, and it
inverts the meaning of the column the comparison will turn on. The
`seal/ledger/` row carries the same claim under the **Executed** label,
which is the label that asserts somebody ran it.

---

## 🔴 2 — the 116-minute cycle is 105 minutes of nobody at the keyboard, not a subagent's run

**Location** — `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/reading.md:74`,
and the same attribution at `overview.md:47`, `questions.md:41`,
`changelog.md:43`.

Each of those four says the row whose span exceeds its own parts does so
because the delegated wait passed the 900 seconds `analyse` stops counting a
gap at.

**Executed**, on the row itself. The 116.3m figure `reading.md` publishes as
the top of the `specseal:smith` span range is one row of the 2026-09-07 run:
span 6,979s (116.3m) against 11.6m of parts. Its composition:

| | |
|---|---|
| Its opening gap — the delegated wait | 580s, **under** the ceiling, and in no column |
| One internal gap ≥ the ceiling, dropped from `model_s` | 6,285s (104.8m), before a `cd …` shell call that reads a work item directory |

So the row's unexplained 104.8m is the orchestrator issuing nothing
mid-cycle, and the delegated wait it is credited to is 580 seconds. The
other five rows over 5,000s in these transcripts decompose the same way —
each has one or two internal gaps above the ceiling, with opening gaps of
18s to 835s.

**Why it matters.** `reading.md`'s *what is not claimed* section names the one
thing to check against this reading: *"whether the* in no column *share
shrinks once it is known what it is made of."* It is now known, and it is not
what the page says it is. A later reading that finds that share smaller would
read it as the delegated question having been answered, when what moved was
how long somebody was away.

---

## 🟡 3 — the rows partition the calls and not the time, and the report says the first without saying the second

**Location** — `skills/verify/scripts/session_cost.py:1120` and `:1181`;
`seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/reading.md:39`.

The printed header says *"every call in exactly one of them"* and the closing
line prints *"N calls over the rows above, of N calls in the transcript"*.
Both are true. Neither is true of time, and nothing on the page says so.

**Executed** — sum of the rows' spans against the run's span, on the three
transcripts the reading covers plus one more:

| Run | run span | sum of row spans | between the rows |
|---|---|---|---|
| 2026-09-06 | 539.4m | 450.2m | 89.2m (16.5%) |
| 2026-09-07 | 448.0m | 394.3m | 53.7m (12.0%) |
| 2026-09-08 | 164.0m | 122.1m | 41.9m (25.6%) |

`reading.md:39` tells its reader *"A row's `span` is wall clock"*. A reader
who adds the band table's spans is short by 12–26% of the run with nothing
on the page saying so — the #200 shape the whole design is defending
against, one column over.

Two smaller things sit inside this one. The call tally is structurally
incapable of disagreeing: both sides come from the same list through
`in_windows`, which assigns every item to exactly one window by
construction, so a line whose docstring says *"a reader gets to see it hold
instead of taking this file's word for it"* is a restatement wearing a
check's clothes. And the printed legend explains head, cycle, tail and
delegated but not `span`, which is the one column whose meaning changes
between a whole-run row and a cycle row.

---

## ⬜ 4 — `overview.md` still owes `Ran by` to the orchestrator, and `e389fc1` filled it

`overview.md:77` lists *"`Ran by` on all five phase records"* under **Not
verified** with the orchestrator as answerer. The target SHA is
`e389fc1 docs: the phase records name what ran them`, which filled all five
with `specseal:smith on claude-opus-5`. `templates/sdd-phase.md` permits
exactly that reach-back, so the row is stale rather than wrong. Paperwork
under `seal/specs/`, not a fix.

---

## ⬜ 5 — two cheap redundancies in the new path

`measure_cycles` returns `len(spawn_cuts(calls)[0])` (`session_cost.py:719`),
re-sorting the spawn list `spawn_cycles` already sorted one line above; and
`main` computes `measure_cycles` on every invocation, including the plain
printed path where nothing reads it. Also `spawn_cycles`' `turns=()` default
is unreachable — its only caller always passes the list.

---

## What I verified and am not reporting

Each of these was opened rather than taken from the handoff.

- **The partition of calls holds.** `in_windows` assigns by one instant per
  item; `spawn_cuts` runs its cuts through a running maximum so a
  result-before-call cannot invert a window; the head is bounded by the first
  spawn's **start**, which is `spec.md`'s acceptance row rather than
  `plan.md`'s parenthetical, and `phase-1.md` records that choice.
  **Executed** — sums equal on four real transcripts (953+ calls) and on the
  module's own fixture.
- **The `delegated_s` acceptance row.** Cycle 2 of the fixture reads
  `delegated_s` 1200, `command_s` 4, `model_s` 16 — which separates the three
  implementations the docstring names. **Executed.**
- **The plain reading did not move.** `command_s` 1827 and `delegated_s` 0.0
  on the whole-run row. **Executed.**
- **The disclosure line has a case on each arm** — present at 3s maximum
  delegated, absent on the fixture's 1200s. **Executed** via the suite.
- **The ledger's eight → twelve correction is right.** Six subtractions
  (`analyse` at 446, 449, 467, 477, 485, 524) and six orderings (`load` 410,
  `spawn_cuts` 577, 581, 583, `in_windows` 597, `analyse` 464). Four of the
  orderings are this branch's. **Executed** by count at the coordinates.
- **Nothing was removed.** The four deleted lines are the old `analyse`
  signature, its naive `command_time` sum, the 4-tuple unpack and the `data`
  dict; each is re-established, and with `delegated` empty the new loop is
  the old sum value for value.
- **The whole-run prompt-as-command-line classification.** I agree with the
  deferral in `seal/follow-up.md`. Fixing it there would move a published
  number in the one path that must not move, which is the same argument that
  keeps `delegated_s` where it is.
- **The false premise left standing in the approved contract.** Right call,
  and `survivors.md`'s ten excused rows read as sound — including the two
  `CHANGELOG.md` arms, where a released entry records what was true then.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The agent's wall clock is in no column of any row; nine pages say it is in the next row's `model` under fifteen minutes | `skills/verify/scripts/session_cost.py:1144` · `:231` · `:632` · `skills/verify/SKILL.md:413` · `changelog.md:41` · `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:8` · `reading.md:71` · `overview.md:46` · `questions.md:39` · `tests/test_session_cost.py:2048` | open | Executed: `analyse:466` skips a window's opening gap and `:446` starts the span at the first call, so the interval is in no column. 17 of 18 opening gaps under the ceiling in the 2026-09-08 run, totalling 1,507s, none in `model_s`; the row quoted as 768s reads a 64s span. Synthetic control with a 300s wait: tail row 10s/5s/5s |
| 2 | The published 116-minute cycle is one internal 104.8m idle gap, not a subagent's run, and four pages credit it to the delegated wait passing the ceiling | `reading.md:74` · `overview.md:47` · `questions.md:41` · `changelog.md:43` | open | Executed on that row: span 6,979s, parts 11.6m, one internal gap of 6,285s before a shell call, opening gap 580s — under the ceiling. Five other rows over 5,000s decompose the same way |
| 3 | The rows partition calls and not time; the report asserts the first, `reading.md` calls a row's span wall clock, and 12–26% of each run lies between the rows | `skills/verify/scripts/session_cost.py:1120` · `:1181` · `reading.md:39` | open | Executed: 89.2m of 539.4m, 53.7m of 448.0m, 41.9m of 164.0m outside every row's span. The call tally cannot disagree — both sides come from one list through `in_windows` |
| 4 | `overview.md` still owes `Ran by` to the orchestrator; the target SHA filled it | `overview.md:77` | open | Read: `e389fc1` fills all five, and `templates/sdd-phase.md` permits the reach-back |
| 5 | `spawn_cuts` re-run for a count already computed; `measure_cycles` computed on the plain path; a dead `turns=()` default | `skills/verify/scripts/session_cost.py:719` · `:1236` · `:601` | open | Read at the coordinates |

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

Every probe file was named `test_tmp_*`, run once, and deleted; all of it ran
in the clone.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| What `delegated_s` should measure now the premise under it is false | `questions.md` Q4, three costed answers | the owner |
| A spawn's prompt classified as a command line in the whole-run reading | `seal/follow-up.md` | the owner |
| The full suite, repository-wide lint, typecheck | not run — `skills/agent-contract/SKILL.md` §2 | the orchestrator |
| 20 mutations, 0 survivors on the final code | the implementer's claim; I did not re-run mutation testing | the orchestrator |
| `bin/survivor-check` — it requires `--range A..B` and I did not run it. The ten excused rows read as sound grounds | `survivors.md` | the orchestrator |
| Windows | #103's standing gap | nobody has run it |

## Paste-ready fixes

Finding 1, the printed sentence — `skills/verify/scripts/session_cost.py`:

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

Finding 1, the `DELEGATING` comment — replace the paragraph ending *"in
`model_s` while the wait is under the 900-second ceiling `analyse` puts on a
gap, and in nothing at all above it"*:

```python
# spawn is ACCEPTED, the agent then runs for a median of about 1,000 seconds,
# and that interval is in NO column of any row. It is the gap between the
# cycle that spawned and the next row's first call: `analyse` starts a
# window's `span_s` at that first call and never counts the gap before it,
# whether the wait is above the 900-second ceiling or below it. Measured over
# the same three runs, that is 12-26% of each run's wall clock.
```

Finding 1, `spawn_cycles`' docstring — replace the paragraph beginning *"The
waiting is in that band"*:

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

Finding 1, `skills/verify/SKILL.md` — replace the sentence beginning *"Where a
harness writes it when the spawn is ACCEPTED"*:

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

Finding 1, the changelog fragment — replace *"and that wall clock lands in the
next row's model time — or, past the fifteen minutes model time stops counting
at, in none of the columns, which is where a row's span exceeds its own parts
by an hour"*:

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

Finding 1, the ledger row — replace the Evidence cell's sentence *"The wait
then shows as the orchestrator's model gap -- 351s, 768s and 962s measured
after three consecutive spawn results -- and `analyse` drops a gap at 900s"*:

```markdown
The wait then shows in NO column of any cycle row -- 351s, 768s and 962s measured after three consecutive spawn results, each of them the opening gap of the row that follows, and 17 of one run's 18 opening gaps are under the 900s ceiling and in `model_s` for none of them. `analyse` starts a window's `span_s` at its first call and never counts the gap before it, so 12-26% of a run's wall clock falls between the rows
```

Finding 1, `reading.md` — replace the paragraph beginning *"So the delegated
wall clock is not in the column named for it"* and the one-line coda:

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

Finding 2, `reading.md` — the sentence that explains the 116-minute row. It is
in the *in no column* passage above; this replaces the clause *"and why one
smith cycle reads a 116-minute span against 11.5 minutes of parts"*:

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

Finding 3, the printed report — make the missing time visible rather than only
disclaimed. In `report_spawns`, after the call tally:

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

`report_spawns` takes the run's span as a fourth argument, and `main` passes
it from the whole-run reading it already computes:

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

Finding 3, `reading.md:39` — the legend:

```markdown
A row's `span` runs from its own first call to its own last, which is not the
whole window: the wait after each spawn's result is between two rows and in
no column. `command` is tools running; `model` is the gap between one turn's
last result and the next turn's first call, inside a row only. Medians, with
the full range beside the span.
```

Finding 1, a case that pins where the wait lands. It fails against the code as
it stands, because the current sentence claims the opposite:

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

Needs a fix: yes — findings 1 and 2, the false statement of where the delegated wall clock is and the false attribution of the published 116-minute cycle, in the code's printed report, `skills/verify/SKILL.md`, both fragments, the ledger row and the reading about to be posted; and finding 3, the missing disclosure that the rows do not partition the time.
Loses a record or crashes: no

## Proof

Files opened at the target SHA, in a `git clone --no-local` at
`e389fc11a036e427f7a2b6f3aed0da65d22ed241`:

- `skills/verify/scripts/session_cost.py` (whole of the new path: 216–420,
  414–724, 1082–1284)
- `tests/test_session_cost.py` (1605–2093, and the case index)
- `skills/verify/SKILL.md` (the diff hunk at 384–416)
- `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/`
  — `spec.md`, `plan.md`, `overview.md`, `questions.md`, `reading.md`,
  `survivors.md`, `changelog.md`, `phases/phase-1.md`, and the `Ran by` row
  of all five phase records
- `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md`
- `seal/ledger.md` (the diff — the nine re-anchored rows and the R1 correction)
- `seal/follow-up.md` (the appended row)
- `templates/sdd-phase.md` (the `Ran by` rule)
- `CONTRIBUTING.md` (the runner, and the narrow-run rule)
- `CLAUDE.md`, `~/.claude/CLAUDE.md`
