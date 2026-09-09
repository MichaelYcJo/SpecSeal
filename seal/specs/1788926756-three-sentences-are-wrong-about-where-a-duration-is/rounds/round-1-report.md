# Round 1 — three sentences are wrong about where a duration is

| Field | Value |
|---|---|
| Target SHA | `d9e3749` |
| Base | `78d2c12` (`origin/release/v0.9.5`) |
| Branch | `fix/300-the-rows-do-not-partition-the-time` |
| Reviewed in | a `git clone --no-local` at the target SHA |

## The short of it

The arithmetic is right and I proved it myself. Every defect below is in a
sentence written about the change, which is the class this work item exists
to close, and one of them is in the disclosure the work item was opened to
add.

The headline is finding 1. The shipped skill now tells a reader who sees a
`command` share above 100 per cent to read it as "wall-clock seconds with
something running in the background". Over the 169 transcripts on this
machine, **none** of the overlap comes from a background command. All 8,332
seconds of it come from calls batched into one assistant message, which this
repository's own `CLAUDE.md` tells every agent to do.

## The code half, opened rather than accepted

The handoff labelled six facts *claimed, unverified by me*. I opened all of
them. Four hold as stated, one holds with a number the record gets wrong
(finding 4), and one is the sentence the prompt told me to open first.

**The subinterval sentence holds.** `load` sorts by start and `in_windows`
preserves that order, so a window's `calls[0]["start"]` is its minimum start
and `max(c["end"] ...)` its maximum end. A row's calls are a subset of the
run's, so a row's interval sits inside the run's. The difference is then the
gaps minus the overlap, and a negative one needs two rows covering the same
seconds. All of that is true, and the narrower claim in the module comment
that the refusal *can no longer fire on ONE row* is true with it. What is not
true is the wider claim two documents make from it, which is finding 5.

**The four new and changed cases all pin something.** I reverted each half of
the fix in the clone and watched the case go red: the span rule, the refusal's
cut clause, the `>= 0` guard, and the negative-span sentence. Four for four,
each restored byte-identical. §15 is satisfied and I did not take the record's
word for it.

**The 115.7 per cent transcript is real**, at 99 calls and 5,761.8 seconds of
overlap, and 72 of 169 transcripts carry more than a second. The negative-span
arm really does flip from minus sixty minutes to `120.0m`. The module passes at
the target SHA, though not at the count the record gives (finding 11).

---

## 1. The disclosure names a cause that produced none of the overlap 🔴

`skills/verify/SKILL.md:429-433`

> Where you see a share above 100, read it as command seconds against
> wall-clock seconds with something running in the background, never as a
> broken number.

`load` gives every `tool_use` block in one assistant message that message's
timestamp as its start. A batch of three calls therefore starts at one instant
and overlaps by construction, and it is what this repository's `CLAUDE.md`
asks for on every turn.

I decomposed the overlap machine-wide by collapsing each turn to one interval
before measuring:

| Source of overlap | Seconds | Share |
|---|---|---|
| calls batched into one assistant message | 8,332.1 | 100.0% |
| calls crossing a turn boundary | −0.1 | 0.0% |

The transcript that prints 115.7 per cent is 99 calls in 94 turns with a
largest batch of three, and every one of its 5,761.8 seconds is intra-turn.

A reader who follows this sentence goes looking for a background command and
finds none, and is back at *this number is broken* — the reading the sentence
exists to prevent. It is item 1's defect one file over: a printed sentence
naming a cause the transcript does not carry. It ships in 0.9.5.

## 2. Q3 rests on the same cause, and its answers fire on the wrong condition 🟡

`seal/specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is/questions.md`

Q3 says **A background command is the ordinary way in**. On the measurement
above it is not the way in at all.

The consequence is not cosmetic, because Q3's third answer is triggered on the
share passing 100 per cent. That happens in **1 of 169** readings. Overlap
above a second is in **72 of 169**, and 23 of 169 print a `command` share that
would differ if `command_s` became the union. So the answer the question
recommends leaves 22 of the 23 affected readings silently inflated, and the
trigger rather than the wording is what needs deciding.

Q3's second answer also has no number where its cost belongs. It says every
published `command` figure changes meaning, which both overstates and omits.
Measured over the same 169:

| Under the union | Count | Largest move |
|---|---|---|
| printed `command` minutes change | 58 of 169 (4 of this project's 16) | 315.1m → 219.1m |
| printed `command` share changes | 23 of 169 (1 of this project's 16) | 116% → 80%, 36 points |
| unchanged either way | 111 of 169 | — |

That is the figure the owner needs to weigh answer 2 against answer 3, and it
was measurable from the same sweep phase 1 already ran.

## 3. "No printed figure moves" is false machine-wide, and a third figure was never swept 🟡

`spec.md:76` · `questions.md` Q1 · `seal/ledger/1788926756-three-sentences-are-wrong-about-where-a-duration-is.md` row 4

Four documents in this work item make this claim and two of them make it
flatly. `changelog.md` and `overview.md` carry the corrected row-level result;
`spec.md`'s fact row and Q1 still say *No PRINTED figure moves*, and the new
ledger row's own clause says *at run level or at row level* while its
Verified cell names two moving row figures three lines later.

I swept every printed surface the span feeds rather than the two the record
covers:

| Printed surface | Moves | Recorded? |
|---|---|---|
| run `span` in the plain report | 0 (one span moves by 0.006s) | yes |
| row `span` in the `--spawns` table | 2 — 368.5m → 368.7m, 195.7m → 195.8m | yes |
| the between-the-rows figure | **3 — 6.7m → 6.6m, 24.4m → 24.2m, 3.3m → 3.2m** | **no** |
| `idle` line in the plain report | 0 | no |
| `model` share | 0 | no |
| whole-run `command` share | 0 | no |
| figure ↔ refusal branch | 0 flips | no |

The third row is the figure this work item is about, and nothing looked at it.

**The conclusion survives and the grounds do not.** Every move on every axis is
in another project's transcript, and this project's directory moves nothing —
so no marking line is owed on the readings posted to #51. What makes them safe
is that per-project measurement, not the flat claim the two documents make.

## 4. The case pinning item 2 never printed the figure item 2 is about 🟡

`seal/ledger/1788926756-three-sentences-are-wrong-about-where-a-duration-is.md` row 5 ·
`tests/test_session_cost.py` docstring of
`test_a_head_call_outlives_the_cut_without_outliving_a_spawns_result` ·
`seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/questions.md:100-101`

All three say the pinned fixture's three-second difference printed `by 0.0m`
beside a span column of `0.1m / 0.0m / 0.0m`. `minutes` is `f"{s/60:.1f}m"`, so
`minutes(3)` is **`0.1m`**. I ran the fixture with the old span rule restored:
the span column is **`0.1m / 0.1m / 0.0m`** and the old line read `by 0.1m`.

The shape that really printed `by 0.0m` is #145's round-3 one-second overlap
(head 0–9s, spawn 5–7s, call 10–12s), and `0.1m / 0.0m / 0.0m` is that
fixture's column. The two have been merged into one sentence in three places.

`spec.md`'s own scope text is correct — *a sub-three-second overlap printed `by
0.0m`* — and `minutes(1)` is indeed `0.0m`. It is the fixture that does not
match the scope, not the scope.

**And on this fixture the new line does not carry what the record claims it
does.** It prints `sum to 0.2m against the run's own 0.2m`: 13s and 10s both
round to `0.2m`, so the reader who subtracts still gets 0.0m. The claim that
two sums "carry the same fact and never round one of them away" is not met by
the case that pins it. What the new line does gain is that it no longer asserts
a magnitude of zero, which is a real improvement and a smaller one than
claimed.

## 5. The refusal does not fire strictly less often 🟡

`plan.md:20-24` · `phases/phase-2.md:44-49`

> so the refusal in items 1 and 2 fires strictly less often afterwards

Both sides of the subtraction grow, and the rows can grow by more in total than
the run does. Executed, on head `Bash` 0–100s with a call at 1–2s, spawn 3–4s,
and calls at 10–11s and 12–13s:

| Rule | What printed |
|---|---|
| old | `0.1m of the run's 0.2m is BETWEEN the rows — mostly the wait` |
| new | `the rows' spans sum to 1.7m against the run's own 1.7m` — the refusal |

The new reading is the correct one, because the head row really does cover the
tail's seconds and the old figure was the false line. So this is a wrong
sentence about the change and not a defect in it.

The module comment's narrower claim — *this can no longer fire on ONE row* — is
true and I verified it. `phases/phase-2.md` is where the two are conflated: it
proves the one-row fact and then writes *that is the prompt's strictly less
often*, which does not follow.

## 6. Four sentences still name the retired cause, one twelve lines from the comment forbidding it 🟡

§12 asks for the class rather than the instances. The change fixed the two
printed sentences and left four unprinted ones saying the thing the printed
ones stopped saying.

| Coordinate | The standing text |
|---|---|
| `skills/verify/scripts/session_cost.py#in_windows` | "would put one that outlived a report in two rows" |
| `skills/verify/scripts/session_cost.py#report_spawns`, the comment above the guard | "a call that outlives a spawn's result stays in the row it began in" |
| `tests/test_session_cost.py`, docstring of `test_a_call_that_outlives_a_cut_prints_no_between_the_rows_figure` | the same sentence, in the test whose own assertion is `"outlived a spawn's result" not in out` |
| `tests/test_session_cost.py`, docstring of `test_every_call_lands_in_exactly_one_row` | "a call that outlived a report" |

The second is twelve lines above the comment that says naming the result
"names a cause the transcript does not carry".

## 7. An unshipped changelog fragment ships a false release note beside the correction 🟡

`seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/changelog.md:59-66`

`gather_changelog.py --check` exits 1 and lists this fragment as never having
reached `CHANGELOG.md`, so it ships in the same release section as this work
item's own. It says:

> **And where a call outlives a spawn's result**, the between-the-rows figure
> is refused rather than printed. … the report says the spans summed past the
> run instead.

Neither is what the report says at this SHA. A reader of 0.9.5's notes gets one
entry describing behaviour that never shipped and another, three entries down,
correcting it.

`CLAUDE.md` already permits touching another work item's file to keep an
existing statement true, and phase 3 used exactly that grounds for #145's Q5
and its ledger fragment. This file was missed.

## 8. Two rows in the re-stamped fragment carry content the re-read did not catch 🟡

`seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md`

**Row 8** quotes the deleted expression inside a Verified-behavior cell:
`(calls[-1]["end"] - calls[0]["start"])`. The row was re-read and re-stamped
for this change, and its appended note discusses the `delegated_max` block and
`#report_spawns` without mentioning that the parenthetical it carries is the
expression #300 removed.

**Row 11** carries the old figure into the new argument. It opens *992s is not
the rows' overlap* and then gives the subinterval grounds. Under the new rule
the difference on that fixture is **987s** (rows 1987s against a run of 1000s);
992s was the old difference against the old 995s run span. The claim that the
two coincide is true of 987 and false of 992, and 987 is what the test says.

Rows 5, 6, 7, 9 and 10 I checked against the code and each holds.

## 9. F5's appended note narrows the clause it sits under 🟡

`seal/ledger.md:873`

F5 holds that the shipped skill may name no tracker state existing in this
repository alone. This change put `#300` into the anchored section at
`skills/verify/SKILL.md:423` and appended a note saying the absence still
holds, on the grounds that `measurement` and `log: measurement` are still
absent. That is two words, not the clause. An issue number is this
repository's own tracker state, and the row's own body warns against exactly
this move: *a later edit that moves a sentence from the script's docstring into
the skill for symmetry is exactly what this refuses*. That is what happened —
the `#300` reasoning in `analyse`'s docstring was mirrored into the skill,
citing the issue.

**Stated for accuracy, because it changes what the fix is:** `(#272)` was
already at `skills/verify/SKILL.md:188` at the base SHA, outside F5's anchored
section. So the clause was already false at whole-file scope before this
change, and `test_the_shipped_skill_names_no_repository_specific_tracker_state`
stays green either way because it asserts three literals and has no
issue-number check. What this change wrote is the note asserting an absence
that is not there. The clause needs correcting or the case needs widening, and
that is bigger than this work item.

## 10. The dead expression is restated in the present tense in four live documents ⬜

`spec.md:75` and `plan.md:12-13` in this work item, and
`seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/plan.md:16` with
`overview.md:19` quoting it. This work item's `spec.md` row is the one worth a
marker: it sits in an evidence table labelled `read`, two of whose rows phase 1
rewrote to post-change values, so the table mixes both states with nothing
saying which is which. #145's Q5 already models the past-tense framing.

## 11. The proof line's test count is one short ⬜

`overview.md` records `bin/test tests/test_session_cost.py` at **68 passed**.
At the target SHA it is **69 passed**, executed in the clone.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The span disclosure tells a reader to read a share above 100% as a background command; 100% of the measured overlap is batched calls in one message and 0% crosses a turn | `skills/verify/SKILL.md:429-433` | open | executed — 8,332.1s of 8,332.0s intra-turn over 169 transcripts; the 115.7% run is 99 calls in 94 turns, largest batch 3 |
| 2 | Q3 repeats that cause and triggers its answers on the share passing 100%, which is 1 of 169 readings against 72 of 169 carrying overlap; option 2's cost column carries no number | `questions.md` §Q3 | open | executed — 23 of 169 shares and 58 of 169 minutes move under the union, largest 116% → 80% |
| 3 | *No printed figure moves* is flat in two documents and false machine-wide; the between-the-rows figure moves on 3 transcripts and was never swept | `spec.md:76`, `questions.md` Q1, `seal/ledger/1788926756-*.md` row 4 | open | executed — full printed-surface sweep; every move is in another project, so the conclusion stands and the grounds do not |
| 4 | Three documents say the pinned fixture printed `by 0.0m` beside `0.1m/0.0m/0.0m`; `minutes(3)` is `0.1m` and the column is `0.1m/0.1m/0.0m` | `seal/ledger/1788926756-*.md` row 5, `tests/test_session_cost.py` head-cut docstring, #145 `questions.md:100` | open | executed — fixture re-run with the old span rule restored; two fixtures merged into one sentence |
| 5 | *The refusal fires strictly less often* is false; both sides of the subtraction grow and the rows can grow by more | `plan.md:20-24`, `phases/phase-2.md:44-49` | open | executed — a shape that printed the figure under the old rule prints the refusal under the new one |
| 6 | Four unprinted sentences still name a spawn's result or a report as the cause, one twelve lines above the comment forbidding it | `#in_windows`, `#report_spawns`, two `tests/test_session_cost.py` docstrings | open | read |
| 7 | #145's changelog fragment is ungathered and ships beside the correction, still saying the report names a spawn's result and prints the sum passing the run | `seal/specs/1788908215-*/changelog.md:59-66` | open | executed — `gather_changelog.py --check` exit 1 lists it |
| 8 | Row 8 quotes the deleted expression in a Verified cell; row 11 opens with 992s where the new difference is 987s | `seal/ledger/1788908215-*.md` rows 8 and 11 | open | read, arithmetic checked — rows 1987s against a run of 1000s |
| 9 | F5's appended note narrows *no tracker state* to two words after `#300` entered the anchored section | `seal/ledger.md:873` | open | read — `(#272)` already at `SKILL.md:188` at the base, so the clause was already false at file scope |
| 10 | The old expression restated in the present tense in four live documents, one an evidence table phase 1 half-rewrote | `spec.md:75`, `plan.md:12`, `seal/specs/1788700685-*/plan.md:16` and `overview.md:19` | open | read |
| 11 | The proof line says 68 passed; the module passes 69 at the target SHA | `overview.md` §verified | open | executed |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| What the report should print where `command` exceeds 100% of the span | `questions.md` Q3, with finding 2's correction to its trigger and its missing number | the owner |
| Whether the disclosure belongs in the report's own output as well | `questions.md` §*Open, and it is small* | the owner |
| F5's clause versus any issue number in the shipped skill, `(#272)` included, and whether `test_the_shipped_skill_names_no_repository_specific_tracker_state` should read for the shape rather than three literals | finding 9 — bigger than this work item | the owner |
| `seal/follow-up.md`'s row with the carried-over grounds | `phases/phase-3.md`, handed over rather than edited | work item `1788912166-red-for-following-the-documents-green-for-ignoring-one` |
| `docs/flow.md:77` still saying the fix is paste-ready and could not be taken | out of this work item's scope by the round brief | the orchestrator |
| Windows | #103's standing gap | nobody has run it |

## ❓ out of verified scope

The full suite, the repository-wide lint and the typecheck. §2 keeps them off
this segment and the round brief agrees; the base's 2973 passed at `78d2c12` is
the last reading I have. The orchestrator answers, once, after the rounds
settle. Nothing in my prompt asked me to widen past that, so nothing was
declined.

## Paste-ready fixes

**1 — `skills/verify/SKILL.md`, the last sentence of the new span paragraph**

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

**2 — `questions.md` Q3, the paragraph and the answer table**

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

**3 — `spec.md` fact row and `questions.md` Q1, both flat claims**

```
| **No PRINTED figure in THIS PROJECT's transcripts moves under `max(end)`, and three move elsewhere on the machine** — this project's directory: 16 transcripts, 12 to 836 calls, 0 spans and 0 rows move. Every project: 169 transcripts, one run span moves by 0.006s and prints 10.3m either way; 2 row spans move a printed figure (368.5m → 368.7m, 195.7m → 195.8m); the between-the-rows figure moves on 3 transcripts (6.7m → 6.6m, 24.4m → 24.2m, 3.3m → 3.2m). `idle`, `model` share and the whole-run `command` share move nowhere, and the figure/refusal branch never flips | `~/.claude/projects/*/*.jsonl` | **executed 2026-09-09** — the safety of the published readings is the per-project result, not a machine-wide absence |
```

```
| 1 | The readings already posted to #51 need no marking line for the span's new definition | **Executed, on every printed surface.** This project's 16 transcripts move nothing: no run span, no row span, no between-the-rows figure. Machine-wide three printed figures do move — 2 row spans and 3 between-the-rows figures — and every one is in another project's transcript. So no reading posted to #51 moves, which is a per-project measurement rather than a property of the rule, and that is what `skills/verify/SKILL.md` now says where a reading is taken |
```

**4 — the merged fixture, in three places**

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

**5 — `plan.md` §Technical context and `phases/phase-2.md`**

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

**6 — the four unprinted sentences**

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

**7 — #145's changelog fragment**

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

**8 — the two fragment rows**

```
`analyse` starts a window's `span_s` at its own first call and its model walk
adds no gap before that call
```

```
987s is not the rows' overlap.
```

**9 — F5's appended note**

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

## The broad gate

**Not yet.** No full-suite, repository-wide lint or typecheck run has happened
on this branch. The last reading is the base's 2973 passed at `78d2c12`. It is
not due while findings stand.

---

Needs a fix: yes — findings 1 and 7 ship reader-facing sentences that are
false about the code beside them, and findings 3, 4, 5, 8 and 9 are records
asserting things the code and the arithmetic contradict.

Loses a record or crashes: no — every defect is a sentence, the arithmetic is
correct on every axis I swept, and nothing leaves the root or raises.

## Proof

Opened, in the clone at `d9e3749` unless noted:

- `skills/verify/scripts/session_cost.py` — `load`, `analyse`, `spawn_cuts`,
  `in_windows`, `spawn_cycles`, `measure_cycles`, `share`, `report`,
  `report_spawns`, `main`
- `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*
- `tests/test_session_cost.py` — the four new and changed cases and their
  neighbours
- `seal/specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is/` —
  `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`,
  `survivors.md`, `routing.md`, `phases/phase-1.md`, `phases/phase-2.md`,
  `phases/phase-3.md`
- `seal/ledger/1788926756-three-sentences-are-wrong-about-where-a-duration-is.md`
  — all five rows
- `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md`
  — rows 5 to 11
- `seal/ledger.md` — rows at lines 101, 873, 1037, 1141, 1335, 1818, 1821
- `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/` —
  `changelog.md`, `questions.md` §Q5
- `bin/test`, `.github/scripts/gather_changelog.py`
- `git diff 78d2c12 d9e3749` in full

Not opened: `docs/flow.md` beyond the line the sweep named, the subagent
transcripts themselves, and anything under `seal/specs/*/rounds/`, which
describe their own target SHAs.
