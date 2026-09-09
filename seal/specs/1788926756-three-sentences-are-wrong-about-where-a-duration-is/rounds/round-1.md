# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — review round 1

| Field | Value |
|---|---|
| Target SHA | d9e3749 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #306 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1 and 7 ship reader-facing sentences that are |
| Loses a record or crashes | no — every defect is a sentence, the arithmetic is |

- [x] Pass

## What this round was asked

The first review of a change that moved what a published number means, in a
file whose last two runs each found their worst defect in a sentence rather
than in code — and whose contract carries a false acceptance row on purpose.
The class to enumerate was every sentence in the tree saying what a span ends
at or where a duration is, by construction rather than by grep.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The span disclosure tells a reader to read a share above 100% as a background command; 100% of the measured overlap is batched calls in one message and 0% crosses a turn | `skills/verify/SKILL.md:429-433` | **fixed** `af44065` | fixed at af44065 — ``; executed — 8,332.1s of 8,332.0s intra-turn over 169 transcripts; the 115.7% run is 99 calls in 94 turns, largest batch 3 |
| 2 | Q3 repeats that cause and triggers its answers on the share passing 100%, which is 1 of 169 readings against 72 of 169 carrying overlap; option 2's cost column carries no number | `questions.md` §Q3 | answered | corrected at `8f3d12a` — Q3 keeps its three answers and gains the trigger it was missing; the fourth row is the trigger correction, not a replacement, and the decision stays the owner's |
| 3 | *No printed figure moves* is flat in two documents and false machine-wide; the between-the-rows figure moves on 3 transcripts and was never swept | `spec.md:76`, `questions.md` Q1, `seal/ledger/1788926756-*.md` row 4 | answered | corrected at `8f3d12a` (`spec.md` fact row, `questions.md` Q1, ledger fragment row 4) and `af44065` (the same flat claim in this work item's changelog fragment, which is the surface a reader outside the work item meets) |
| 4 | Three documents say the pinned fixture printed `by 0.0m` beside `0.1m/0.0m/0.0m`; `minutes(3)` is `0.1m` and the column is `0.1m/0.1m/0.0m` | `seal/ledger/1788926756-*.md` row 5, `tests/test_session_cost.py` head-cut docstring, #145 `questions.md:100` | **fixed** `af44065` | fixed at af44065 — `` for the case docstring, `8f3d12a` for the ledger row and `spec.md`'s acceptance row, `9d9e717` for #145's `questions.md`. Executed: the head-cut fixture's span column is 0.1m/0.1m/0.0m and its difference is three seconds, so the old line read `by 0.1m`; `by 0.0m` beside 0.1m/0.0m/0.0m is #145's round-3 one-second fixture. A fourth instance the report did not name — `spec.md`'s row said *Given a one-second overlap* while citing the three-second case — is corrected with it; executed — fixture re-run with the old span rule restored; two fixtures merged into one sentence |
| 5 | *The refusal fires strictly less often* is false; both sides of the subtraction grow and the rows can grow by more | `plan.md:20-24`, `phases/phase-2.md:44-49` | answered | corrected at `8f3d12a` in `phases/phase-2.md`. `plan.md` is the approved contract and a fix pass does not edit it, so the divergence is recorded in `overview.md` instead. Executed — head `Bash` 0-100s with a call at 1-2s, spawn 3-4s, calls at 10-11s and 12-13s prints the figure under the old rule and the refusal under the new one, and the new reading is the correct one |
| 6 | Four unprinted sentences still name a spawn's result or a report as the cause, one twelve lines above the comment forbidding it | `#in_windows`, `#report_spawns`, two `tests/test_session_cost.py` docstrings | **fixed** `af44065` | fixed at af44065 — ``; read |
| 7 | #145's changelog fragment is ungathered and ships beside the correction, still saying the report names a spawn's result and prints the sum passing the run | `seal/specs/1788908215-*/changelog.md:59-66` | answered | corrected at `af44065` |
| 8 | Row 8 quotes the deleted expression in a Verified cell; row 11 opens with 992s where the new difference is 987s | `seal/ledger/1788908215-*.md` rows 8 and 11 | answered | corrected at `9d9e717`. Row 11's Verified cell carried the same stale pair two clauses above the sentence the report named — *a run span of 995s* and *`outside` is -992s* — and moves with it. Executed on the pinned fixture: the run span is 1000s and the difference is 987s |
| 9 | F5's appended note narrows *no tracker state* to two words after `#300` entered the anchored section | `seal/ledger.md:873` | answered | corrected at `9d9e717`. The note now says the absence is not whole rather than asserting it is; the decision it turns on — narrow F5's clause or widen its case — is `questions.md` Q4 with the owner. Executed: `(#272)` is in the shipped skill's `## Scope` section, outside the anchor, so the clause was already false at file scope at the base |
| 10 | The old expression restated in the present tense in four live documents, one an evidence table phase 1 half-rewrote | `spec.md:75`, `plan.md:12`, `seal/specs/1788700685-*/plan.md:16` and `overview.md:19` | answered | corrected at `8f3d12a` for `spec.md:75`, which sits in an evidence table two of whose rows phase 1 rewrote to post-change values; it now says which state it is. `plan.md:12` and `1788700685`'s `plan.md:16` and `overview.md:19` are left standing: a plan's §Technical context states the code as it stood when the plan was written, which is what all three do, and they are correct at their own SHA |
| 11 | The proof line says 68 passed; the module passes 69 at the target SHA | `overview.md` §verified | answered | corrected at `8f3d12a` — executed, `bin/test tests/test_session_cost.py -q` gives 69 passed |

## Paste-ready fixes

```
   Where you see a share above
   100, read it as command seconds against wall-clock seconds with calls
   running at once, never as a broken number. Batching is the ordinary way
   in and a background command is the rarer one: every tool call in one
   assistant message carries that message's timestamp as its start, so a
   batch of three overlaps by construction. Measured over the transcripts on
   one machine, every second of overlap above a second came from calls
   batched into one message and none of it from a call that crossed a turn.
```
```
**It is not synthetic.** Sweeping every transcript under
`~/.claude/projects/*/*.jsonl` with the new rule: 169 with calls, **one
printing `command` at 115.7%** — 99 calls carrying 5,761.8 seconds of real
overlap — and overlap above one second in 72 of the 169. **Batching is the
ordinary way in**, not a background command: every tool call in one assistant
message starts at that message's timestamp, so a batch overlaps by
construction, and 100% of the machine's 8,332 seconds of overlap is
intra-turn with none of it crossing a turn. This is the plain path every
published segment reading uses.

**The trigger is the part that needs deciding, not the wording.** A share
above 100% is 1 of the 169. Overlap that moves a printed figure is in 23 of
them, so an answer that fires only above 100% leaves 22 of the 23 inflated
and silent.

| Answer | What it costs | What a reader gets |
|---|---|---|
| Leave it | nothing | a share over 100% of a span, which reads as arithmetic that cannot be right, in the path every reading uses |
| Take `command_s` to the union of the call intervals | the number stops being *command time* and becomes *wall clock with a command running*. **Measured:** 58 of 169 printed `command` minutes change and 23 of 169 printed shares change, the largest 116% → 80% and 315.1m → 219.1m; 111 of 169 are identical either way | a share that cannot pass 100%, and a break in the series for a third of the readings |
| Keep the sum and say so where the share passes 100% | one printed sentence, in `report` beside the share, plus its case | a true reading of the 1 transcript in 169 that passes 100%, and nothing for the other 22 whose share is inflated below it |
| Keep the sum and say so wherever calls overlapped at all | one printed sentence and one union computation, on every reading rather than on one in 169 | *1007s of command time in 1000s of wall clock — calls ran concurrently* wherever it is true, which is where the comparability actually breaks |
```
```
| **No PRINTED figure in THIS PROJECT's transcripts moves under `max(end)`, and three move elsewhere on the machine** — this project's directory: 16 transcripts, 12 to 836 calls, 0 spans and 0 rows move. Every project: 169 transcripts, one run span moves by 0.006s and prints 10.3m either way; 2 row spans move a printed figure (368.5m → 368.7m, 195.7m → 195.8m); the between-the-rows figure moves on 3 transcripts (6.7m → 6.6m, 24.4m → 24.2m, 3.3m → 3.2m). `idle`, `model` share and the whole-run `command` share move nowhere, and the figure/refusal branch never flips | `~/.claude/projects/*/*.jsonl` | **executed 2026-09-09** — the safety of the published readings is the per-project result, not a machine-wide absence |
```
```
| 1 | The readings already posted to #51 need no marking line for the span's new definition | **Executed, on every printed surface.** This project's 16 transcripts move nothing: no run span, no row span, no between-the-rows figure. Machine-wide three printed figures do move — 2 row spans and 3 between-the-rows figures — and every one is in another project's transcript. So no reading posted to #51 moves, which is a per-project measurement rather than a property of the rule, and that is what `skills/verify/SKILL.md` now says where a reading is taken |
```
```
The difference on that shape is three seconds, so `minutes` printed *by 0.1m*
beside a span column reading 0.1m/0.1m/0.0m. The shape that printed *by 0.0m*
is #145's round-3 one-second overlap — head 0-9s, spawn 5-7s, call 10-12s —
and `minutes` rounds any difference under three seconds away.
```
```
    The two sums are what removes the magnitude. `minutes` is one decimal, so
    a difference under three seconds printed `by 0.0m` as the grounds for
    withholding a figure: #145's round 3 measured that on a one-second
    overlap. The difference here is three seconds and printed `by 0.1m`; what
    this fixture pins is item 1, the cut rather than the result. Note that
    both sums round to 0.2m on it, so the reader's own subtraction gives 0.0m
    — the two figures stop the line ASSERTING a magnitude of zero, and they
    do not recover one.
```
```
because the difference went through a one-decimal formatter and read `by 0.0m`
on a one-second overlap.
```
```
**Order matters, and item 3 goes first.** Taking the span to `max(end)` makes
a window's own span cover every call assigned to it, so the refusal in items 1
and 2 can no longer fire on a row's own call at all — only on two rows
covering the same seconds. It is NOT strictly rarer: both sides of the
subtraction grow, and where the rows grow by more in total than the run does
it fires where the old rule printed a figure. Executed — head `Bash` 0-100s
with a call at 1-2s, spawn 3-4s, calls at 10-11s and 12-13s printed `0.1m of
the run's 0.2m is BETWEEN the rows` under the old rule and the refusal under
the new one, and the new reading is the correct one because the head row
really does cover the tail's seconds.
```
```
That is narrower than the prompt's *strictly less often*, and the wider claim
is false: the rows can grow by more in total than the run does, and such a
shape fires the refusal where the old rule printed a figure. What the
subinterval property gives is the one-row fact above and nothing more.
```
```
    Assignment is by ONE instant per item — a call's start, a turn's stamp —
    which is what makes the windows a partition: every item has exactly one
    of those and every instant falls in exactly one window. Assigning a call
    by overlap would put one that outlived the cut its row ends at in two
    rows, and a sum over the rows would then come out larger than the run.
```
```
    # And the subtraction can come out NEGATIVE, which is not an interval and
    # must not be printed as one. `in_windows` assigns a call by its START,
    # which is what makes the CALLS partition and is not enough to make the
    # spans partition: a call that outlives the cut its row ends at stays in
    # the row it began in while the next row's calls have already started, so
    # two rows' spans cover the same seconds and their sum can pass the run's
    # own span.
```
```
    `in_windows` assigns a call by its start, which is what makes the calls
    partition and is not enough to make the spans partition: a call that
    outlives the cut its row ends at stays in the row it began in while the
    next row's calls have already started, so two rows' spans cover the same
    seconds and their sum can pass the run's own span.
```
```
    A slice that drops the run's closing work, or one that charges a call
    that outlived the cut its row ends at to both rows either side of it,
    both pass every other case here and fail this one.
```
```
  **And where a call outlives the cut its row ends at, the between-the-rows
  figure is refused rather than printed.** Assigning a call by its start is
  what makes the calls partition, and it leaves a long-running one — a
  background command, a suite spanning a cut — in the row it began in while
  the next row has already started, so two rows' spans cover the same
  seconds and sum past the run. The subtraction is then a negative, and a
  negative printed as *the wait* is the one thing this change exists to
  stop; the report prints the two sums and refuses the figure instead. No
  run measured here reaches it.
```
```
`analyse` starts a window's `span_s` at its own first call and its model walk
adds no gap before that call
```
```
987s is not the rows' overlap.
```
```
**Re-read 2026-09-09 for #300**, whose two-paragraph rewrite of the
between-the-rows disclosure drifted this section. **The absence this row
names is no longer whole and the row cannot be re-stamped as though it
were:** the rewrite put `(#300)` into this section, and an issue number is
tracker state that exists in this repository alone. `(#272)` was already at
`skills/verify/SKILL.md:188`, outside this anchor, so the clause was
already false at whole-file scope before this change. The case stays green
because it asserts three literals — `log: measurement`, `#51` and a bare
backticked `measurement` — and reads for no issue number at all. Either the
clause narrows to those literals or the case widens to the shape; that is a
decision, and it is carried as such rather than settled here.
```

## Executed probes

| What was run | Result |
|---|---|
| both span rules over every transcript, run level and row level | 169 runs with calls, 1 run span moves by 0.006s and prints the same; 602 rows with calls, 8 move, 2 change a printed row span; 0 in this project's directory |
| every other printed surface the span feeds | `idle` 0, `model` share 0, whole-run `command` share 0, figure ↔ refusal 0 flips, **between-the-rows figure 3 moves** |
| overlap decomposed into intra-turn and cross-turn | 8,332.1s of 8,332.0s intra-turn (100.0%), cross-turn −0.1s; 72 of 169 carry over a second |
| `command_s` taken to the union of the call intervals | 58 of 169 printed minutes change, 23 of 169 printed shares change, largest 116% → 80% |
| four mutations, one at a time, each restored byte-identical | span rule reverted, refusal clause reverted, `>= 0` tightened to `> 0`, negative-span sentence reverted — each turned its own case red, exit 1 |
| the pinned head-cut fixture under both span rules | identical output; span column `0.1m/0.1m/0.0m`, refusal `sum to 0.2m against the run's own 0.2m` |
| a shape where the rows grow by more than the run | old rule printed the figure, new rule prints the refusal |
| `bin/test tests/test_session_cost.py -q` in the clone at `d9e3749` | 69 passed |
| `gather_changelog.py --check` | exit 1, three fragments ungathered including #145's |

```
# In a `git clone --no-local` at d9e3749, from the clone root.
# Probes were named test_tmp_*, run once, and deleted; the clone tree is clean.

./bin/test tests/test_session_cost.py -q ; echo $?
python3 .github/scripts/gather_changelog.py --check ; echo $?

# The overlap decomposition, in outline: for every transcript under
# ~/.claude/projects/*/*.jsonl, load the calls, take
#   overlap = sum(end - start) - union(intervals)
# then collapse each turn to [min start, max end] and repeat. The difference
# between the two is the overlap that is NOT batching.
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| What the report should print where `command` exceeds 100% of the span | `questions.md` Q3, with finding 2's correction to its trigger and its missing number | the owner |
| Whether the disclosure belongs in the report's own output as well | `questions.md` §*Open, and it is small* | the owner |
| F5's clause versus any issue number in the shipped skill, `(#272)` included, and whether `test_the_shipped_skill_names_no_repository_specific_tracker_state` should read for the shape rather than three literals | finding 9 — bigger than this work item | the owner |
| `seal/follow-up.md`'s row with the carried-over grounds | `phases/phase-3.md`, handed over rather than edited | work item `1788912166-red-for-following-the-documents-green-for-ignoring-one` |
| `docs/flow.md:77` still saying the fix is paste-ready and could not be taken | out of this work item's scope by the round brief | the orchestrator |
| Windows | #103's standing gap | nobody has run it |
