# 1790913304 — review round 2 report

Ran by `specseal:warden on claude-opus-5-5`, at `3a42459ea1acdd00954cac4b545ce8fa8e88b5df`.
This is a verifying round. Its target is round 1's fix range
`59666b18..237dbc52`, six commits. The work ran in a `git clone --no-local`
of the worktree checked out at the target SHA, under this round's own
scratch directory. The worktree was only read, and this report is the one
file written in it. The clone and the probe were removed before handover.

## In one view

```
round 1's findings                     this round
  finding 1  every file claimed  --->  closed: one Stop draws what fits with its disc,
             and printed past the        the rest wait; 2/6/8/12 files of #702's size
             limit                       drain one per Stop at 6,277 units, none lost
  finding 2  two seals, no disc  --->  closed by the same change
  finding 3  reserve, 3 gates    --->  the answer holds; finding 8 is one more reach of its class
  finding 4  wide characters     --->  the deferral to #720 holds
  finding 5  SEALED value inked  --->  closed; the twin carries no ink, so it cannot disagree

new units: admitted is correct on 176 sets (0 violations); 11 mutations, 9 caught
  survivors -> finding 7: oldest-first and exactly-at-the-budget are not pinned
  and the A3 case cannot see a file claimed and not printed -> finding 6
```

Nothing this round found needs a fix. Everything it opened is ⬜.

## 1. The hook drains the queue in order, with the disc

Executed. The hook ran through `hooks/dispatch.py stop` in a scratch
repository, over 2, 6, 8 and 12 values files with #702's values in the rows
#717's panel returns. Each block measures 6,277 at 0.90, which is the figure
round 1 measured. At 9,000 two of them do not fit together even at 0.75.

So every `Stop` printed one block of 6,277 UTF-16 units, at 0.90 and with
its disc. The other files stayed pending under their own names, in order.
For 2, 6, 8 and 12 files the queue drained in 2, 6, 8 and 12 `Stop`s, and
the next `Stop` printed nothing. No file was lost, none was drawn twice, and
on every turn the message's labels were exactly the files that turn renamed.

A mixed queue of twelve files was also run. Five could not be drawn: one
not JSON, scale 0.5, scale NaN, an integer `item`, and malformed `rows`. Seven
could, and those seven drained in seven `Stop`s in their order:

- a seal at 0.90;
- one whose own scale is 0.75, drawn at 0.75;
- one with sixty deferral homes, drawn alone with no disc (6,423 units);
- one at 1.0, drawn at 1.0;
- one whose branch holds a lone surrogate (6,242);
- one whose branch holds forty U+1D54F (6,316 units, 6,276 Python characters);
- a last seal at 0.90.

All five bad files were still pending at the end, and none stalled the queue.

## 2. `admitted` is monotone and terminates, and no set was found that it handles wrong

Read first. In the floor pass, `used` only grows while it stays at or below
`budget`, and it stops at the first block that does not fit. That makes the
result a prefix, so the order is oldest first. The raise pass changes each
block's size once. It accepts a rung only where `rest + more <= budget`, so
`used` never passes `budget`. Both loops are bounded by the number of blocks
times four rungs.

Executed. A probe checked `admitted` against named sets and against 160
random sets: one to four blocks, four row sets, seven scales, four labels,
budgets from 300 to 20,000. On each set it checked six things:

- the result is never empty;
- `fitted` is the join of `admitted`'s blocks;
- every block is the drawing at one of its rungs;
- the rung with no disc appears only alone, and only when 0.75 does not fit;
- the total stays under the budget, and the count is maximal;
- no block could take a higher rung beside the others' final sizes.

176 cases ran with no violation. The named sets the prompt asked about came
out as follows:

| Set | Rungs drawn |
|---|---|
| one seal, budget exactly its 0.75 size | `[0.75]`; one under is `[None]` |
| one seal, budget exactly its 0.90 size | `[0.9]` |
| two equal, `2·s75 + 2` / `2·s75 + 1` | `[0.75, 0.75]` / `[0.9]` |
| two equal, `s90 + s75 + 2` / `s90 + s80 + 2` | `[0.9, 0.75]` / `[0.9, 0.8]` |
| small after large, and large after small, at 9,000 | `[0.75, 0.75]` both ways |
| small, then one too large to sit beside it, then small | `[0.9]`: the third waits behind the second |
| own scale 0.75, or 0.78, at any budget | never above it |
| lone-surrogate label; forty-astral label exactly at its size; one under | `[0.9]`; `[0.9]`; `[0.8]` |
| empty | `[]`, and `fitted` returns `""` |

A file whose own scale is below 0.75 never reaches `admitted`. `check_scale`
refuses it inside `drawings`, and the file stays pending, as the mixed queue
shows.

## 3. Every count of the message is in UTF-16 units, except the reserve's

Read and executed. `admitted` is the only place that measures what the hook
prints, and it counts with `encode("utf-16-le", "surrogatepass") // 2`. A
lone surrogate counts as one, which is what a JavaScript string gives it once
the harness decodes the `\ud800` escape that `json.dumps` writes. A pair
counts as two. The hook printed both without raising.

The cases measure with Python `len`. Their fixtures hold no character outside
the BMP, so both counts are equal there; the probe measured that on #702's
rows. The one exception is `test_a_character_outside_the_bmp_is_counted_as_two`,
which compares the two counts on purpose.

The reserve is the one measurement left in the other unit. `MESSAGE_RESERVE`'s
comment gives 533 and 909 characters for one and two failed gates, and
`hooks/dispatch.py` cuts each exception's text at `MESSAGE_CAP`, 200 code
points. A gate whose exception text lies outside the BMP can therefore add up
to 200 units, and two such gates pass the reserve. This is finding 8. It is
finding 3's class, what the reserve covers, along a second axis.

## 4. Finding 5 is closed, and the twin agrees

Executed. With `ln == 1` the title's 124 goes to the panel's first line and
to no other line. A continuation row reading `SEALED` is inked 94. An older
values file whose rows open with a blank row still gets the title on its
first line, because `sheet_text` drops blank rows.

The letter twin writes characters only and carries no colour, so there is no
ink in it to disagree with. Its footprint still equals the block form's on
every line.

A values file whose rows do not open with `("SEALED", "")` would now have its
first line inked as the title. Every panel `broad_gate.py` writes opens with
that row (`skills/verify/scripts/broad_gate.py:2634`), and so does every older
fixture. Read only.

## 5. Finding 3's answer and finding 4's deferral are both right

Read. The comment above `MESSAGE_RESERVE` (`skills/verify/scripts/seal_stamp.py:227`)
states 533 and 909 and says a third failed gate would pass the limit. S1 asked
for at least 1,000. The answer "built as specced" holds, and finding 8 adds
the axis it does not cover.

Issue #720 is open and describes the defect as round 1 reproduced it. `letter`
pads with `ljust` and `compose` measures with `len`, both in code points, and
the pre-#717 frame was padded the same way. So the class predates #717, and
#720 is where it belongs.

## Findings this round opened

### ⬜ 6 — The A3 case cannot see a file that was claimed and not printed

`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:577`. The case
`test_seals_past_what_one_message_carries_wait_for_the_next_turn` is the one
`docs/the-broad-gate.md` names for "a seal past what one message can carry
stays pending". Its "a file was lost" check reads `drawn_path`. A claim
creates that name whether or not the stamp is printed.

Executed. The hook was mutated to claim every ready file
(`for path, block in ready:`). It then printed one stamp and renamed all
twelve files, which loses eleven seals, and this case still passed.
`test_two_files_in_one_turn_are_under_the_budget_together` and
`test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it` went red,
so the suite catches the mutation and the release would not ship it. The case
named as the enforcement is the one that does not. Round 1's paste-ready
version of the case carried the missing check, and the fix pass dropped it.

### ⬜ 7 — Oldest first and exactly at the budget are not pinned

`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:679`. Executed:
two mutations of `admitted` survive all eight new and changed cases.

- **`break` changed to `continue` in the floor pass.** Under it a newer seal
  that fits is carried past an older one that does not. Read: the hook would
  then claim the older file, and `fitted`, recomputing over the claimed files,
  would not print it. That is a lost record. The hook and `fitted` agree on
  what is claimed only because the result is a prefix, and no case holds that.
- **`>` changed to `>=` in the floor test.** A single seal exactly at the
  budget would lose its disc.

The code is right today, and the probe in §2 shows it. The two paste-ready
lines below are shown red against each mutation and green against the code.

### ⬜ 8 — The reserve is measured in code points

`skills/verify/scripts/seal_stamp.py:229`. See §3. It can be reached only by a
failed gate whose exception text is outside the BMP, beside a stamp near the
budget. The fix offered is a sentence in the comment, not a change to the
reserve.

### ⬜ 9 — `admitted`'s docstring names a scale that cannot reach it

`skills/verify/scripts/seal_stamp.py:627`: *each at 0.75 or its own smaller
scale*. A scale below 0.75 is refused before `admitted` sees the block, and
`admitted` called with one directly raises inside `stamp`. The behaviour is
right. Only the clause is dead.

### ⬜ 10 — Ledger B2 carries the same clause (a correction)

`seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md`
B2: *together with their disc at 0.75 (or a file's own smaller scale)*. This
is paperwork, and it is not counted toward `Needs a fix`. Editing it moves
B2's hash, so it is re-stamped with `evidence-check --reverify --checked`.

## What this round did not verify

- **Whether the harness counts a character outside the BMP as two.** The fix
  pass measured it with `claude -p` (`MESSAGE_LIMIT`'s comment, and
  `overview.md`'s divergence table). This round was told not to run
  `claude -p`, so the code's count is checked and the harness's is not. The
  orchestrator answers it.
- **The broad gate.** Not yet. It belongs to the sealer, once the rounds
  settle. Nothing here needs a fix, so the sealer's spawn comes due once this
  round's record is written.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — the hook claims only what one message carries, and the rest wait in order | `hooks/sealer-stamp.py:142` | confirmed | Executed: 2, 6, 8 and 12 files of #702's size drained one per Stop at 6,277 units with the disc, none lost or drawn twice, the next Stop empty; the mixed queue drained seven in order past five bad files |
| 🟢 | round 1's finding 2 is closed — two seals of #702's size each keep the disc, one Stop apart | `skills/verify/scripts/seal_stamp.py:619` | confirmed | Executed: the two-file run drew 0.90 then 0.90; owner's rule Q6 |
| 🟢 | round 1's finding 3's answer holds — the comment states 533 and 909 and that a third gate passes the limit | `skills/verify/scripts/seal_stamp.py:227` | confirmed | Read; S1 asked for at least 1,000. Finding 8 is the axis it does not cover |
| 🟢 | round 1's finding 4's deferral to #720 is right — the class predates #717 | `skills/verify/scripts/seal_stamp.py:469` | confirmed | Read: #720 is open and describes it; `letter` pads with `ljust` and `compose` measures with `len`, as the pre-#717 frame did |
| 🟢 | round 1's finding 5 is closed — the title is the first line, and the twin carries no ink to disagree | `skills/verify/scripts/seal_stamp.py:593` | confirmed | Executed: a continuation reading SEALED is inked 94; twin has no colour and keeps the footprint; the case goes red with the old keying |
| 🟢 | `admitted` is monotone, terminates, returns a prefix, and leaves no block able to take a higher rung | `skills/verify/scripts/seal_stamp.py:658` | confirmed | Executed: 176 sets, 0 violations, the named sets included |
| 🟢 | every measurement of the printed message is in UTF-16 units, a lone surrogate counted without raising | `skills/verify/scripts/seal_stamp.py:651` | confirmed | Read and executed: the hook printed a lone-surrogate and an astral branch; the cases' `len` equals the units on their BMP fixtures |
| ⬜ 6 | the A3 case passes against a hook that claims every file and prints one, because a claim makes the drawn name either way | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:577` | open | Executed: the mutation left this case green and turned two other cases red; round 1's version of the case carried the missing check |
| ⬜ 7 | oldest-first carrying and a single seal exactly at the budget are pinned by no case | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:679` | open | Executed: `break` to `continue` and `>` to `>=` in the floor pass both survive the eight cases; the proposed lines go red on each |
| ⬜ 8 | the reserve's 533 and 909 are code points, and `MESSAGE_CAP` cuts by code points, so two gates with astral exception text pass the reserve | `skills/verify/scripts/seal_stamp.py:229` | open | Read; reachable only by exception text outside the BMP beside a stamp near the budget |
| ⬜ 9 | `admitted`'s docstring says a block may sit at its own scale below 0.75, which is refused before it arrives | `skills/verify/scripts/seal_stamp.py:627` | open | Read: `check_scale` in `drawings`; a dead clause, behaviour right |
| ⬜ 10 | ledger B2 carries the same dead clause, a correction | `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md` | open | Read; paperwork, re-stamped with `--reverify --checked` when edited |
| ❓ | whether the harness counts a character outside the BMP as two UTF-16 units | `skills/verify/scripts/seal_stamp.py:213` | ❓ out of verified scope | Measured by the fix pass with `claude -p`, which this round was told not to run; the orchestrator answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the two touched modules (stamp and sealer) | 299 passed, exit 0 |
| `bin/evidence-check .`, unscoped | `total: 3518 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow`, exit 0 |
| `hooks/dispatch.py stop` with a `Stop` payload, repeated until empty, over 2, 6, 8 and 12 values files of #702's values in the new rows | 2, 6, 8 and 12 Stops, each one block of 6,277 units at 0.90 with its disc; drained in order, none lost, none twice, the next Stop empty |
| The same over a mixed queue of twelve: seven drawable (0.90, own 0.75, sixty homes, 1.0, lone surrogate, forty astral, 0.90), five not (not JSON, 0.5, NaN, integer item, bad rows) | seven Stops drew the seven in order: 6,277 · 4,677 · 6,423 with no disc, alone · 6,779 at 1.0 · 6,242 · 6,316 units (6,276 characters) · 6,277; the five bad files still pending; the eighth Stop empty |
| `admitted` over the named sets and 160 random sets, against six invariants | 176 cases, 0 violations |
| Eleven mutations, each against the eight new and changed cases | one rung for all: 6 red · Python `len`: 1 red · no `surrogatepass`: 1 red · title keyed on the value: 1 red · hook claims all ready: 2 red, the A3 case green · no raising: 5 red · `break` to `continue`: 0 red · `used` from 0: 2 red · floor `>=`: 0 red · no-disc path returns empty: 2 red · raise `<`: 2 red |
| The lines proposed for findings 6 and 7, unmutated and under the three survivors | green unmutated; red under claims-all-ready, `break` to `continue` and floor `>=`; the files restored, `git status` clean |
| Title and twin over a `("", "SEALED")` continuation, a blank first row, and rows not opening with SEALED | continuation 94; blank first row gives the title on line 1; twin has no colour and keeps the footprint; rows not opening with SEALED have their first line inked 124 |
| The full suite, lint and typecheck (the broad gate) | not yet — the sealer's, once the rounds settle |

## Paste-ready fixes

### ⬜ 6

```python
    before = 0
    for turn in range(1, 13):
        text = json.loads(stop(repo))["systemMessage"]
        assert len(text) <= mod.MESSAGE_BUDGET, (turn, len(text))
        blocks = text.split("\n\n")
        assert all("\x1b[38;2;" in b for b in blocks), f"turn {turn} lost a disc"
        drawn_now = [p for p in paths if os.path.exists(mod.drawn_path(p))]
        waiting = [p for p in paths if os.path.exists(p)]
        assert drawn_now == paths[: len(drawn_now)], "not oldest first"
        assert waiting == paths[len(drawn_now) :], "a file was lost"
        assert len(drawn_now) >= turn, f"turn {turn} drew nothing new"
        # A claim renames the file whether or not its stamp is printed, so
        # the drawn names alone cannot see a file claimed and dropped.
        assert [b.split("\n", 1)[0] for b in blocks] == [
            mod.label(full_values(f"{n:08x}"))
            for n in range(101 + before, 101 + len(drawn_now))
        ], f"turn {turn} claimed a file its message does not carry"
        before = len(drawn_now)
        if not waiting:
            break
```

### ⬜ 7

```python
    assert mod.admitted(two, alone) == [at[0.9]], "both drawn, or not at 0.90"
    # Oldest first: a newer seal that would fit is not drawn ahead of an
    # older one that does not, which the hook would claim and not print.
    big = (LABEL, ROWS + [("", f"home-{k}") for k in range(60)], 0.9)
    one = (LABEL, ROWS, 0.9)
    past = len(at[0.9]) + 2 + len(at[0.75])
    assert mod.admitted([one, big, one], past) == [at[0.9]], "drawn past a seal that waits"
    # A single seal exactly at the budget keeps its disc.
    assert mod.admitted([(LABEL, ROWS, 0.75)], len(at[0.75])) == [at[0.75]]
```

### ⬜ 8

```python
# characters for one failed gate and 909 for two, separator included
# (measured 2026-10-02 over `dispatch.describe`); a third would pass the
# limit beside a stamp at the budget. Those are code points, and
# `MESSAGE_CAP` cuts an exception's text by code points too: a gate whose
# exception text lies outside the BMP adds up to 200 more units, so two
# such gates pass the reserve.
```

### ⬜ 9

```python
    message without it. So the message carries as many of the oldest blocks
    as fit together WITH the disc, each at 0.75 — a scale below it is
    refused before a block reaches here — and then each, oldest first, at
    the highest rung the others leave room for: its own scale first, then
    each of `SCALE_LADDER`, never above its own scale. The blocks past
    those are not drawn here; the hook leaves their files pending, and the
    next `Stop` draws them whole.
```

### ⬜ 10

```markdown
`admitted` carries as many of the oldest pending blocks as fit `MESSAGE_BUDGET` together with their disc at 0.75, and then lifts each, oldest first, to the highest rung the others leave room for
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, at `3a42459e` in the clone:

- `hooks/sealer-stamp.py`, whole
- `skills/verify/scripts/seal_stamp.py`: lines 182–276 and 382–690, and `write_values` through `label` (825–945)
- `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`: lines 21–76, 198–266, 312–349, 470–700
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the fix range's hunk
- `hooks/dispatch.py`: `report` (500–524) and `MESSAGE_CAP` (53)
- `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/rounds/round-1.md`, whole; `rounds/round-1-report.md`, lines 1–30
- `questions.md` Q6; the fix range's diff of `docs/the-broad-gate.md`, `changelog.md`, `overview.md`, `survivors.md`, `seal/releases/0.15.7.md` and the work item's ledger fragment
- `.github/scripts/run_tests.py`, the venv lines; `bin/test`
- #720 through `gh issue view`
- one drawn values file of #702 under the main checkout's git directory, read only, for its rows
