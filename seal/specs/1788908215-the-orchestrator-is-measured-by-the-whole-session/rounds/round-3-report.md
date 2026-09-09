# Review round 3 — the round that ends the run

| Field | Value |
|---|---|
| Target SHA | `54804b0` |
| Fix range read | `5da52f9..01a8fa5` |
| PR | #294 |
| Ran by | specseal:warden on claude-opus-5 |

**Round 2's finding 1 is fixed, and the fix pass was right on both places it
departed from my paste-ready text.** The wording it chose over mine states a
quantity a reader can check against the table printed above it, and the rider
it reverted would have drifted two shared ledger rows whose claims are outside
the pass. I verified both rather than taking them.

**Nothing here should stop the pull request.** Nothing loses a record and
nothing crashes. What I opened is one clause of the new refusal sentence and
one sentence of paperwork about where a fact was placed — plus one older thing
the same root reaches that no page mentions, which belongs to the owner.

## How the five findings relate

The fix prints a refusal where it used to print a negative. Findings 1 and 2
are the refusal's own sentence. Findings 3 and 4 are about where the fact
behind the refusal was recorded. Finding 5 is the same root arriving in the
plain report, which nothing in this range touched.

```
the guard          → 1  the named cause is not the head row's cut
                   → 2  the magnitude rounds to 0.0m and refuses anyway
where the fact went → 3  the ledger says a RIDER exists; none does
                   → 4  Q5's first option charges nothing for a disclosure
                        its own third column says does not exist
the same root      → 5  the PLAIN report prints command at 101% of the span
```

---

## 🟡 1 — The refusal names a cause the head row need not carry

`skills/verify/scripts/session_cost.py:1243` · `skills/verify/SKILL.md:421-422`

The refused line tells the reader *a call outlived a spawn's result*. For every
row but one that is right. The head row's boundary is not a spawn's result —
`spawn_cuts` opens its cut list at the first spawn's **start**, which round 2's
finding 6 established and which `session_cost.py:570` still does. So a head
call can outlive its own row's cut while ending before that spawn's result, and
the printed sentence then names a cause the transcript does not carry.

**Executed.** A head call at 0–8s, a spawn at 5–9s, calls at 6–9s and 9–10s:
row spans 8s, 4s and 1s against a run span of 10s, `outside` = **-3s**, and
`--spawns` printed *the rows' spans SUM PAST the run's own 0.2m by 0.1m … a
call outlived a spawn's result*. No call in that transcript ends after the
spawn's result at 9s. Exit 0.

**Why it is not `Needs a fix`.** The shape is unreachable in a real run. A
head-only overlap is bounded by the first spawn's own pairing duration — 1.5 to
3.7 seconds over the 67 spawns measured — and `outside` only goes negative when
the overlaps exceed the gaps between rows, which are minutes to hours on the
three runs read. So the false clause needs a run whose every between-row gap
totals under four seconds. The other half of the sentence is true wherever the
line fires at all: a call did outlive a cut.

`skills/verify/SKILL.md:422` carries the same clause, and that copy is the one a
person measuring a segment reads.

## ⬜ 2 — The refusal prints `by 0.0m` and refuses the figure anyway

`skills/verify/scripts/session_cost.py:1243`

The magnitude goes through `minutes`, which is one decimal place, so any
overlap under three seconds prints as `0.0m`. The reader is then told the figure
is withheld because the spans summed past the run by nothing.

**Executed.** A head call at 0–9s, a spawn at 5–7s, a call at 10–12s: run span
12s, row spans 9s + 2s + 2s, `outside` = **-1s**. Printed: *the rows' spans SUM
PAST the run's own 0.2m by 0.0m, so this run has no between-the-rows figure*.
The span column above it reads 0.1m, 0.0m, 0.0m — so at that scale the printed
table does not show a sum passing the span either, and the sentence and the
table cannot be reconciled.

Same knife edge as finding 1, and the same paste-ready fix closes both: print
the two sums rather than their difference. A reader subtracts two printed
figures; nothing rounds away; and on the case the suite pins, 33.1m against
16.6m is the same fact as *by 16.5m* with the arithmetic left to the reader.

## ⬜ 3 — The ledger fragment says a `# RIDER:` is at `analyse`; there is none

`seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:11`

The new row's note closes: *"it is a `# RIDER:` at that line rather than a row
in `seal/follow-up.md` — the file's own rule sends anything tied to a coordinate
to the coordinate."* Present tense, asserting a placement.

**Executed.** `grep -n "RIDER" skills/verify/scripts/session_cost.py` returns
nothing — not at `analyse`, not anywhere in the file. `seal/follow-up.md:16`
names `grep -rn "RIDER:"` as the repository-wide list, so the reader that rule
sends to the coordinate finds nothing there.

That row folds into `seal/ledger.md` at the release and becomes a durable
present-tense claim about the tree. This is the work item's own class one file
over: a page asserting something nothing carries.

**The revert itself was right, and I verified the grounds rather than taking
them.** Inserting a two-line `# RIDER:` inside `analyse` and running
`evidence_check.py` reports `DRIFTED skills/verify/scripts/session_cost.py#analyse`
against both `seal/ledger.md` and this work item's own fragment — 2 drifted,
exit 1. The two shared rows are `seal/ledger.md:101` and `:1818`, both anchored
`#analyse@e52dee1b`, and their claims are outside this pass. Re-stamping them
without re-reading is round 2's finding 2 exactly.

So the fact is adequately **placed** — `questions.md` Q5 holds it with the owner
as its answerer, and the comment at `session_cost.py:1224-1228` holds it for
whoever opens the refusal. What is wrong is only the sentence describing where
it went. Correct the sentence; do not write the rider inside a capped run.

## ⬜ 4 — Q5's first option charges nothing for a disclosure that does not exist

`seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/questions.md:87`

The row reads *"Leave it, and say so where a reader meets it | nothing | … with
only the refusal line hinting at it."* The option names an act — saying so where
a reader meets a published span — the cost column charges nothing for it, and
the third column says it does not happen. A reader choosing that option gets
the third column, not the first.

The three answers are otherwise the right three, and separable from the guard
the way Q5 says. What Q5 understates is what turns on them, which is finding 5.

## ⬜ 5 — The plain report prints command at 101% of the span

`skills/verify/scripts/session_cost.py:994-995` — pre-existing, and nothing in
this range touched it.

`command_s` sums call durations and `span_s` reads the end of the last call **to
begin**, so a call that outlives every later call is counted in full against a
span it ends after. The share then passes 100%.

**Executed.** A call at 0–1000s with calls at 10–12s and 990–995s: `span_s`
995, `command_s` 1007, and the plain report printed `command 16.8m 101%`,
exit 0. The `idle` line is correctly suppressed — its guard is
`idle > span_s * 0.1`, which a negative cannot pass — so nothing prints a
negative here.

This matters more than Q5 currently says, because it is the **plain** path.
Every segment reading this repository publishes goes through it, `--spawns` is
the narrower reader, and a background command is the ordinary way in. No
published number is affected: the three runs read 47.2m of 546m, 65.0m of 448m
and 33.3m of 164m.

Its home is Q5's own option table, whose second and third options both narrow
it. It is not this run's fix.

---

## Round 2's verdicts, re-derived

**Finding 1 — fixed, and the changed wording is better than mine.** The printed
figure is `sum(span column) - run_span`, which a reader reproduces from the
table above it: the pinned case prints head 16.7m, cycle 0.0m, tail 16.4m —
33.1m against a run of 16.6m, difference 16.5m. My *"the rows' spans OVERLAP by
16.5m"* would have been false: the intervals are [0,1000], [5,7] and [10,995],
whose union is 1000s, so the actual overlap is 987s and not 992s. The 5s gap
between the two is the run's own span understatement, which is exactly what the
pass said and what Q5 now records. The new wording names no quantity nothing
measured.

**Finding 2 — answered.** The three `Checked` cells read 2026-09-09 and the
section they cite re-anchored `@1b459b88` → `@3123025c`. `evidence_check.py`
reports 1008 ok · 0 drifted · 0 broken, exit 0.

**Finding 3 — answered, and §12's three extra instances hold.** The tree's
remaining `delegated wait` matches outside the round records are three, and each
names the defect rather than asserting it: the new case's docstring
(`tests/test_session_cost.py:2116`), `questions.md:51`, and the note column of
the ledger fragment's row 10. Every live page reads *opening gap*, with the
`delegated` column's own value beside it — 2 seconds on the 116-minute row in
`reading.md`, `overview.md` and `questions.md`, and 0 to 3 seconds across the
four rows in `changelog.md`, which matches round 2's measurement of 0s, 3s, 3s,
2s.

**The new unit, judged as code.** §15 is satisfied and I checked it rather than
reading the claim: the case overlaid on the module at `5da52f9` fails, exit 1.
All four mutations the ledger row claims are killed — guard removed, sign
flipped, refusal wording changed, magnitude unnegated, each exit 1 — and the
module was restored byte-identical after each. Findings 1 and 2 are what the
case does not reach, because it pins one shape and both live in the wording it
asserts.

**The class, enumerated.** The two subtraction sites in the module that could
print a negative as an interval are the run-level `idle` at `:1002`, guarded by
`span_s > 0 and idle > span_s * 0.1`, and the between-the-rows `outside` at
`:1230`, now guarded. There is no third. `share` already refuses a non-positive
whole, and `report` already has a negative-span arm at `:983`.

**The reading is true where a reader meets it.** `reading.md` publishes a
positive between-the-rows figure for all three runs and does not need the
refusal; `skills/verify/SKILL.md` is where a later reading would meet it, and
that is where the fix put it. The whole-run *in no column* shares (43%, 41%,
10%) and the between-the-rows shares (30.7%, 12.0%, 25.6%) diverge because the
run-level model walk counts a between-row gap under 900s, which the page states
in those words.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The refusal names *a call outlived a spawn's result*, and the head row's cut is the first spawn's START | `skills/verify/scripts/session_cost.py:1243` · `skills/verify/SKILL.md:422` | open | **Executed.** Head call 0-8s, spawn 5-9s, calls 6-9s and 9-10s: row spans 8s + 4s + 1s = 13s against a run span of 10s, `outside` = -3s, and the refusal printed the result as the cause while no call ends after the spawn's result at 9s, exit 0. Unreachable in a real run: a head-only overlap is bounded by the first spawn's pairing duration, 1.5-3.7s over 67 spawns, and `outside` goes negative only when the overlaps exceed the between-row gaps, which are minutes to hours on the three runs. One clause, and the paste-ready fix closes finding 2 with it |
| 2 | ⬜ The refusal prints `by 0.0m` on a sub-three-second overlap and withholds the figure on that grounds | `skills/verify/scripts/session_cost.py:1243` | open | **Executed.** Head call 0-9s, spawn 5-7s, call 10-12s: run span 12s, row spans 9s + 2s + 2s, `outside` = -1s, printed *SUM PAST the run's own 0.2m by 0.0m*, exit 0. The span column beside it reads 0.1m, 0.0m, 0.0m, so the sentence and the table cannot be reconciled at that scale. Printing the two sums rather than their difference removes the rounding and lets the reader subtract |
| 3 | ⬜ The ledger fragment's new row says the `span_s` property *is a `# RIDER:` at that line*; `session_cost.py` carries no rider at all | `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:11` | open | **Executed.** `grep -n "RIDER" skills/verify/scripts/session_cost.py` returns nothing, and `seal/follow-up.md:16` names that grep as the repository-wide list, so the reader the rule sends to the coordinate finds nothing. The row folds into `seal/ledger.md` at the release as a present-tense claim about the tree. **The revert was right**: a two-line rider inserted inside `analyse` makes `evidence_check.py` report `DRIFTED …#analyse` against both `seal/ledger.md` (rows at `:101` and `:1818`, both `@e52dee1b`) and this item's own fragment — 2 drifted, exit 1 — and re-stamping shared rows whose claims are outside the pass is round 2's finding 2. The fact is placed: Q5 with the owner as answerer, and the comment at `session_cost.py:1224-1228`. Only the sentence about where it went is wrong |
| 4 | ⬜ Q5's first option charges `nothing` for a disclosure its own third column says does not exist | `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/questions.md:87` | open | **Read.** The row is *"Leave it, and say so where a reader meets it \| nothing \| … with only the refusal line hinting at it."* The act the option names has a cost and the third column says it does not happen. The three answers are otherwise the right three and separable from the guard, as Q5 says |
| 5 | ⬜ The PLAIN report prints `command` at 101% of the span when a call outlives every later call — pre-existing, outside this range | `skills/verify/scripts/session_cost.py:994` | open | **Executed.** Calls at 0-1000s, 10-12s and 990-995s: `span_s` 995, `command_s` 1007, printed `command 16.8m 101%`, exit 0. `idle` was correctly suppressed at -12s by the `idle > span_s * 0.1` guard, so nothing prints a negative. Same root as Q5 and reachable — a background command is the ordinary way in — and it is the plain path every published segment reading uses, which Q5's table does not say. No published number is affected: 47.2m of 546m, 65.0m of 448m, 33.3m of 164m. Goes to Q5, not to a fix |
| 6 | Round 2 finding 1 — the between-the-rows line printing a negative and calling it the wait | `skills/verify/scripts/session_cost.py:1229-1249` | answered | **Confirmed fixed, and the departure from my wording was right.** The printed figure is `sum(span column) - run_span` and a reader reproduces it from the table above: 16.7m + 0.0m + 16.4m = 33.1m against a run of 16.6m, difference 16.5m. My *OVERLAP by 16.5m* would have been false — the intervals [0,1000], [5,7], [10,995] have a union of 1000s, so the overlap is 987s, and the 5s between the two is the run span's own understatement. `bin/test tests/test_session_cost.py -q`: 66 passed, exit 0 |
| 7 | Round 2 finding 2 — three shared-ledger rows re-hashed with their `Checked` dates left behind | `seal/ledger.md:873` · `:1037` · `:1141` | answered | **Executed.** All three read 2026-09-09; the section re-anchored `@1b459b88` → `@3123025c`, which is the content the re-read was against. `evidence_check.py .`: 1008 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |
| 8 | Round 2 finding 3 — *delegated wait* naming the opening gap, plus §12's three extra instances | `changelog.md` · `reading.md` · `overview.md` · `questions.md` · ledger fragment row 10 · `report_spawns`' docstring | answered | **Executed by sweep.** The only live `delegated wait` matches outside the round records are three, each naming the defect rather than asserting it: `tests/test_session_cost.py:2116`, `questions.md:51`, and the note column of ledger fragment row 10. Every live page reads *opening gap* with the column's own value beside it — 2s on the 116-minute row in three pages, 0 to 3s across the four rows in `changelog.md`, matching round 2's 0s/3s/3s/2s |
| 9 | The new unit `test_a_call_that_outlives_a_cut_prints_no_between_the_rows_figure`, judged as code | `tests/test_session_cost.py:2106` | answered | **Executed.** Red where it must be: the case overlaid on the module at `5da52f9` fails, exit 1. All four mutations the ledger row claims are killed — guard removed, sign flipped, refusal wording changed, magnitude unnegated — each exit 1, module restored byte-identical after each. §15 satisfied. What the case does not reach is findings 1 and 2, both of which live inside the sentence it asserts |
| 10 | The negative-as-an-interval class, enumerated across the module | `skills/verify/scripts/session_cost.py:1002` · `:1230` · `:983` · `:957` | answered | **Read, with the guards executed at their boundaries.** Two subtraction sites can print a residue: run-level `idle`, guarded by `span_s > 0 and idle > span_s * 0.1` (a negative cannot pass), and `outside`, now guarded. No third. `share` refuses a non-positive whole and `report` has a negative-span arm. The `outside >= 0` boundary prints *0.0m … is BETWEEN the rows — mostly the wait* on an exact cover, which is the partition agreeing and is defensible as the comment says |

## Paste-ready fixes

```python
# skills/verify/scripts/session_cost.py, replacing the `if run_span > 0:` block
# at :1229. Closes findings 1 and 2 together: it names the cut a row ends at
# rather than a spawn's result, and prints the two sums rather than the
# difference that rounds away.
    if run_span > 0:
        spans = sum(row["numbers"]["span_s"] for row in rows if row["numbers"])
        outside = run_span - spans
        # `>= 0` and not `> 0`: an exact cover is the partition agreeing, and
        # the tally above is printed even when it agrees for the same reason.
        if outside >= 0:
            print(
                f"  {minutes(outside)} of the run's {minutes(run_span)} is BETWEEN "
                f"the rows — mostly the wait\n  after each spawn's result, in no "
                "column above"
            )
        else:
            # The two sums and not their difference. `minutes` is one decimal,
            # so an overlap under three seconds prints as `by 0.0m` and reads
            # as nothing having happened beside a refusal; two printed figures
            # the reader can subtract carry the same fact and never round it
            # away. And the cut a row ENDS at is the first spawn's START for
            # the head row and a spawn's RESULT for every other row, so
            # naming the result names a cause the head row need not carry.
            print(
                f"  the rows' spans sum to {minutes(spans)} against the run's own "
                f"{minutes(run_span)},\n  so this run has no between-the-rows "
                "figure: a call outlived the cut\n  its row ends at, and the row "
                "it began in covers seconds the\n  next row's does too"
            )
```

```python
# tests/test_session_cost.py:2138, the assertion the wording change moves.
    assert "the rows' spans sum to 33.1m against the run's own 16.6m" in out, out
    assert "no between-the-rows figure" in out, out
```

```python
# tests/test_session_cost.py — the case findings 1 and 2 need, planted beside
# the one above. Seen red before it is committed: on the module as it stands
# the refusal names a spawn's result, which this asserts is absent.
def test_a_head_call_outlives_the_cut_without_outliving_a_spawns_result(tmp_path):
    """The head row's cut is the first spawn's START, not a spawn's result.

    `spawn_cuts` opens its cut list at the first spawn's start, so a head
    call can outlive its own row's cut and still end before that spawn's
    result arrives. The refusal must not name a cause this transcript does
    not carry, and it must not print a magnitude that rounds to nothing."""
    lines = call("bg", 0, 8, "npm run dev")
    lines += spawn("A", 5, 9, "specseal:smith")
    lines += call("b", 6, 9, "pytest -q")
    lines += call("c", 9, 10, "git status --short")
    path = tmp_path / "head-cut.jsonl"
    path.write_text("\n".join(lines) + "\n")
    out = " ".join(run(["--spawns", str(path)]).stdout.split())
    assert "no between-the-rows figure" in out, out
    assert "outlived the cut its row ends at" in out, out
    # No call in this transcript ends after the spawn's result at 9s.
    assert "outlived a spawn's result" not in out, out
    # The two sums, so nothing rounds to `by 0.0m`.
    assert "sum to 0.2m against the run's own 0.2m" in out, out
```

```
skills/verify/SKILL.md:421-422, the same clause one file over.

   **Where the report gives no between-the-rows figure and says the spans
   summed past the run, a call outlived the cut its row ends at.** Assigning
   a call by its start is what makes the calls partition, and it leaves a
   long-running one — a background command, a suite spanning a cut — in the
   row it began in while the next row has already started, so two rows'
   spans cover the same seconds. The head row's cut is the first spawn's
   START and every other row's is a spawn's RESULT, which is why the line
   names the cut rather than the result.
```

```
seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:11,
the closing clause of the note column. Replace:

  and it is a `# RIDER:` at that line rather than a row in `seal/follow-up.md`
  — the file's own rule sends anything tied to a coordinate to the coordinate

with what the tree actually carries:

  and it is `questions.md` Q5 with the owner as its answerer, plus the comment
  at the refusal that says why the figure is not named an overlap. A `# RIDER:`
  at `analyse` is where `seal/follow-up.md`'s own rule would put it and was
  reverted for a reason outside this pass: a comment inside the function drifts
  `seal/ledger.md`'s two rows at `#analyse@e52dee1b`, and re-stamping a shared
  claim without re-reading it is round 2's own finding 2
```

```
seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/questions.md:87,
Q5's first option. Charge the option for the act it names, and say what the
plain path prints.

| Leave it, and one sentence where a reader meets a published span | that sentence, in `skills/verify/SKILL.md` beside the span's own definition — nothing today says it outside the refusal line | a run with a long-lived call reads a span shorter than its own last call, and the PLAIN report prints `command` as a share of it — 101% on a synthetic run with a background command, in the path every published segment reading uses |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q`, in a `--no-local` clone at `54804b0` | 66 passed in 2.52s, exit 0 — one more than round 2's 65 |
| The new case against the module at `5da52f9`, `54804b0`'s test file overlaid | 1 failed, exit 1. §15 satisfied |
| Four mutations of the guard — `if True`, `outside <= 0`, refusal wording changed, `minutes(outside)` unnegated — each run against the new case, module restored from kept bytes each time | 1 failed, exit 1, on all four. Module byte-identical after |
| The pinned shape — background call 0-1000s, spawn 5-7s, calls 10-12s and 990-995s | Row spans 1000s + 2s + 985s = 1987s, run span 995s, `outside` -992s. Printed *the rows' spans SUM PAST the run's own 16.6m by 16.5m*, exit 0. The table above prints 16.7m, 0.0m, 16.4m — 33.1m, so the figure is reproducible from the report |
| The `outside == 0` boundary — head call 0-8s, spawn 5-7s, call 10-12s | run span 12s, spans 8s + 2s + 2s, `outside` 0. Printed *0.0m of the run's 0.2m is BETWEEN the rows — mostly the wait*, exit 0 |
| A one-second overlap — head call 0-9s, spawn 5-7s, call 10-12s | `outside` -1s. Printed *SUM PAST the run's own 0.2m by 0.0m*, exit 0, against a span column of 0.1m/0.0m/0.0m. Finding 2 |
| A head call outliving the head's cut but not the spawn's result — 0-8s, spawn 5-9s, calls 6-9s and 9-10s | Row spans 8s + 4s + 1s = 13s, run span 10s, `outside` -3s. Printed *a call outlived a spawn's result* with no such call in the transcript, exit 0. Finding 1 |
| `run_span == 0` with a spawn present — all stamps at one instant | No between-the-rows line printed at all, exit 0, which is what the docstring at `:1105` says |
| The plain report on a background command — calls 0-1000s, 10-12s, 990-995s | `span_s` 995, `command_s` 1007, `model_s` 0. Printed `command 16.8m 101%`, exit 0; `idle` suppressed at -12s. Finding 5 |
| A two-line `# RIDER:` inserted inside `analyse`, then `evidence_check.py .`, then restored | `DRIFTED skills/verify/scripts/session_cost.py#analyse` against both `seal/ledger.md` and this item's fragment — 1006 ok · 2 drifted, exit 1. Module restored byte-identical. Confirms the revert's grounds |
| `python3 skills/evidence-check/scripts/evidence_check.py .` at `54804b0` | 1008 ok · 0 drifted · 0 broken · 0 external · 0 old-format, the item's fragment 10 ok, exit 0 |
| `bin/survivor-check --range 5da52f9..01a8fa5` | 741 files at `01a8fa5` against 20 removed sentences — no removed wording still standing, exit 0 |
| `tests/test_no_real_identifiers.py` | 2 passed, exit 0 |
| `tests/test_a_segment_feeds_the_flow_log.py` and `tests/test_one_word_one_meaning.py` — the modules the `SKILL.md` change touches | 36 passed, exit 0 |
| `grep -n "RIDER" skills/verify/scripts/session_cost.py`; every `#analyse` anchor in `seal/` | No rider in the file. Anchors: `seal/ledger.md:101` and `:1818`, this item's fragment rows 5 and 10, all `@e52dee1b`. Finding 3 |
| Tree sweep for `delegated wait` and for `BETWEEN the rows` outside the round records | Three live `delegated wait` instances, each naming the defect. `BETWEEN the rows` appears in the module, its test, the ledger fragment and nowhere in `docs/` |
| `seal/specs/…/survivors.md`'s new row read against `phase-5.md` and the replaced verdict row | The 1.90 match is two of three dates coinciding — `Checked` dates 2026-09-06, 2026-09-06, 2026-09-08 against run dates 2026-09-06, 2026-09-07, 2026-09-08. Excused with the standing line as its anchor, which is checkable |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 1 and 2 — the refusal's named cause and its rounded magnitude | a `# RIDER:` at `report_spawns`' refusal branch, or an issue; the paste-ready fix above is the whole change and needs no design | the orchestrator, to place |
| Finding 3 — the ledger fragment's rider sentence | the row itself, before the release fold; the replacement text is above | the orchestrator |
| Finding 4 — Q5's first option | `questions.md` Q5, the row itself | the owner, with Q5 |
| Finding 5 — `command` printing over 100% of the span | `questions.md` Q5's option table, whose second and third answers both narrow it | the owner |
| `questions.md` Q4 and Q5 themselves | already the owner's | the owner |
| The whole-run family misclassification | `seal/follow-up.md`, before round 1 | the owner |
| `evidence-check` silent on a short hash | issue #299, with round 2's diagnosis quoted | already placed |
| `--reverify` leaving no trace of when it wrote | candidate for `seal/follow-up.md`, from round 2 | the orchestrator |
| The full suite, repository-wide lint, typecheck | not run — `skills/agent-contract/SKILL.md` §2. It is due the moment this record is written | the orchestrator, once |
| 20 mutations, 0 survivors on the final code | the implementer's claim; I re-ran the four this range's own ledger row names, not the twenty | the orchestrator |
| Windows | #103's standing gap | nobody has run it |

Needs a fix: no
Loses a record or crashes: no

## Proof

Opened at `54804b0` in a `--no-local` clone: `skills/verify/scripts/session_cost.py`,
`skills/verify/SKILL.md`, `tests/test_session_cost.py`, `bin/test`,
`seal/config.md`, `seal/follow-up.md`, `seal/ledger.md` (the `#analyse` and
`Checked` rows), `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md`,
`skills/code-review/scripts/round_record.py` (the `close` subcommand and the
`Fixes checked by` reach-back), and this work item's `routing.md`, `overview.md`,
`questions.md`, `reading.md`, `changelog.md`, `survivors.md`, `rounds/round-1.md`
and `rounds/round-2.md`. Diffs read: `5da52f9..01a8fa5` in full, and `54804b0`.
Probes were four `test_tmp_*` files, run once each and deleted; `git status` is
clean in the clone.
