# 1788908215-the-orchestrator-is-measured-by-the-whole-session — review round 3

| Field | Value |
|---|---|
| Target SHA | 54804b0 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #294 |
| Broad gate | e381105 against 86dd599 |
| Fixes checked by | no fixes to check — the run is capped |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The round that ends the run. It reads the fixes to a correction whose own
correction printed a negative, and it is the last reader before the reading
reaches the durable log. What it was asked is whether every page a reader
meets is now true about where a duration is, including the new guard's own
sentence — and, because the bound was already spent, to give anything it
found a home and an answerer rather than another fix pass.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The refusal names *a call outlived a spawn's result*, and the head row's cut is the first spawn's START | `skills/verify/scripts/session_cost.py:1243` · `skills/verify/SKILL.md:422` | deferred #300 | **Deferred to #300**, which carries the paste-ready fix and its case. A fix pass may not take it: findings 1 and 2 are inside the unit round 2's own fixes created, and `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it* refuses depth 2. A `# RIDER:` is refused by measurement — four rows of this item's fragment anchor at `#report_spawns@432e8ac5`. **Executed.** Head call 0-8s, spawn 5-9s, calls 6-9s and 9-10s: row spans 8s + 4s + 1s = 13s against a run span of 10s, `outside` = -3s, and the refusal printed the result as the cause while no call ends after the spawn's result at 9s, exit 0. Unreachable in a real run: a head-only overlap is bounded by the first spawn's pairing duration, 1.5-3.7s over 67 spawns, and `outside` goes negative only when the overlaps exceed the between-row gaps, which are minutes to hours on the three runs. One clause, and the paste-ready fix closes finding 2 with it |
| 2 | ⬜ The refusal prints `by 0.0m` on a sub-three-second overlap and withholds the figure on that grounds | `skills/verify/scripts/session_cost.py:1243` | deferred #300 | **Deferred to #300**, closed by the same clause as finding 1. **Executed.** Head call 0-9s, spawn 5-7s, call 10-12s: run span 12s, row spans 9s + 2s + 2s, `outside` = -1s, printed *SUM PAST the run's own 0.2m by 0.0m*, exit 0. The span column beside it reads 0.1m, 0.0m, 0.0m, so the sentence and the table cannot be reconciled at that scale. Printing the two sums rather than their difference removes the rounding and lets the reader subtract |
| 3 | ⬜ The ledger fragment's new row says the `span_s` property *is a `# RIDER:` at that line*; `session_cost.py` carries no rider at all | `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:11` | answered | **Corrected by the orchestrator at the commit carrying this record.** The row's closing clause now names where the fact actually is — Q5 with the owner as answerer, and the comment at the refusal — and records that a rider at `report_spawns` is refused for the same reason as one at `analyse`, one measure further out: four rows of this fragment anchor there. **Executed.** `grep -n "RIDER" skills/verify/scripts/session_cost.py` returns nothing, and `seal/follow-up.md:16` names that grep as the repository-wide list, so the reader the rule sends to the coordinate finds nothing. The row folds into `seal/ledger.md` at the release as a present-tense claim about the tree. **The revert was right**: a two-line rider inserted inside `analyse` makes `evidence_check.py` report `DRIFTED …#analyse` against both `seal/ledger.md` (rows at `:101` and `:1818`, both `@e52dee1b`) and this item's own fragment — 2 drifted, exit 1 — and re-stamping shared rows whose claims are outside the pass is round 2's finding 2. The fact is placed: Q5 with the owner as answerer, and the comment at `session_cost.py:1224-1228`. Only the sentence about where it went is wrong |
| 4 | ⬜ Q5's first option charges `nothing` for a disclosure its own third column says does not exist | `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/questions.md:87` | answered | **Corrected by the orchestrator at the commit carrying this record.** Q5's first option now charges the sentence it needs and names the plain report's 101%. **Read.** The row is *"Leave it, and say so where a reader meets it \| nothing \| … with only the refusal line hinting at it."* The act the option names has a cost and the third column says it does not happen. The three answers are otherwise the right three and separable from the guard, as Q5 says |
| 5 | ⬜ The PLAIN report prints `command` at 101% of the span when a call outlives every later call — pre-existing, outside this range | `skills/verify/scripts/session_cost.py:994` | deferred #300 | **Deferred to #300**, which states what Q5's table did not: this is the plain path every published segment reading uses. **Executed.** Calls at 0-1000s, 10-12s and 990-995s: `span_s` 995, `command_s` 1007, printed `command 16.8m 101%`, exit 0. `idle` was correctly suppressed at -12s by the `idle > span_s * 0.1` guard, so nothing prints a negative. Same root as Q5 and reachable — a background command is the ordinary way in — and it is the plain path every published segment reading uses, which Q5's table does not say. No published number is affected: 47.2m of 546m, 65.0m of 448m, 33.3m of 164m. Goes to Q5, not to a fix |
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:1144` · `:231` · `:632` · `skills/verify/SKILL.md:413` · `changelog.md:41` · `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md:8` · `reading.md:71` · `overview.md:46` · `questions.md:39` · `tests/test_session_cost.py:2048` | round 1's 1 — fixed |
| round-1 | `reading.md:74` · `overview.md:47` · `questions.md:41` · `changelog.md:43` | round 1's 2 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:1120` · `:1181` · `reading.md:39` | round 1's 3 — fixed |
| round-1 | `overview.md:77` | round 1's 4 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:719` · `:1236` · `:601` | round 1's 5 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py:1200` | round 2's 1 — fixed |
| round-2 | `seal/ledger.md:873` · `:1037` · `:1141` | round 2's 2 — answered |
| round-2 | `changelog.md:54` · `reading.md:58` · `overview.md:57` · `questions.md:48` | round 2's 3 — answered |
| round-2 | nine pages, per `round-1.md` | round 2's 4 — answered |
| round-2 | four pages, per `round-1.md` | round 2's 5 — answered |
| round-2 | `session_cost.py:1120` · `:1181` · `reading.md:39` | round 2's 6 — answered |
| round-2 | `session_cost.py:719` · `:1236` · `:601` | round 2's 8 — answered |

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
