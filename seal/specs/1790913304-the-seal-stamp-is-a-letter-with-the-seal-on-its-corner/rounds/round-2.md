# 1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner — review round 2

| Field | Value |
|---|---|
| Target SHA | 3a42459ea1acdd00954cac4b545ce8fa8e88b5df |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 719 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `0bef982a0d12b8fd7e53100d1b442da585ccc09a..483c3770566a81110b30364b70ab8f6f3804bba9`, 6 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round at `3a42459e` over round 1's fix range `59666b18..237dbc52`. That range carries the owner's Q6 rule: the hook draws as many of the oldest seals as fit with their disc, and leaves the rest for the next Stop. For each of round 1's five verdicts the round was asked whether it is closed. It re-ran the hook over 2, 6, 8 and 12 values files, measuring in UTF-16 units. It also checked whether `admitted` is monotone and terminates over edge sets, and whether every place that measures the message counts the same way. The depth-1 units round 1 added were taken as a finding surface.

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
| ⬜ 6 | the A3 case passes against a hook that claims every file and prints one, because a claim makes the drawn name either way | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:577` | **fixed** `81e4730f` | fixed at 81e4730f; Executed: the mutation left this case green and turned two other cases red; round 1's version of the case carried the missing check |
| ⬜ 7 | oldest-first carrying and a single seal exactly at the budget are pinned by no case | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:679` | **fixed** `ea36c24f` | fixed at ea36c24f; Executed: `break` to `continue` and `>` to `>=` in the floor pass both survive the eight cases; the proposed lines go red on each |
| ⬜ 8 | the reserve's 533 and 909 are code points, and `MESSAGE_CAP` cuts by code points, so two gates with astral exception text pass the reserve | `skills/verify/scripts/seal_stamp.py:229` | **fixed** `2988a974` | fixed at 2988a974; Read; reachable only by exception text outside the BMP beside a stamp near the budget |
| ⬜ 9 | `admitted`'s docstring says a block may sit at its own scale below 0.75, which is refused before it arrives | `skills/verify/scripts/seal_stamp.py:627` | **fixed** `efe1c949` | fixed at efe1c949; Read: `check_scale` in `drawings`; a dead clause, behaviour right |
| ⬜ 10 | ledger B2 carries the same dead clause, a correction | `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md` | answered | corrected at 483c3770: ledger row B2, a correction to the record rather than a fix; Read; paperwork, re-stamped with `--reverify --checked` when edited |
| ❓ | whether the harness counts a character outside the BMP as two UTF-16 units | `skills/verify/scripts/seal_stamp.py:213` | ❓ out of verified scope | Measured by the fix pass with `claude -p`, which this round was told not to run; the orchestrator answers it |

## Paste-ready fixes

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
```python
# characters for one failed gate and 909 for two, separator included
# (measured 2026-10-02 over `dispatch.describe`); a third would pass the
# limit beside a stamp at the budget. Those are code points, and
# `MESSAGE_CAP` cuts an exception's text by code points too: a gate whose
# exception text lies outside the BMP adds up to 200 more units, so two
# such gates pass the reserve.
```
```python
    message without it. So the message carries as many of the oldest blocks
    as fit together WITH the disc, each at 0.75 — a scale below it is
    refused before a block reaches here — and then each, oldest first, at
    the highest rung the others leave room for: its own scale first, then
    each of `SCALE_LADDER`, never above its own scale. The blocks past
    those are not drawn here; the hook leaves their files pending, and the
    next `Stop` draws them whole.
```
```markdown
`admitted` carries as many of the oldest pending blocks as fit `MESSAGE_BUDGET` together with their disc at 0.75, and then lifts each, oldest first, to the highest rung the others leave room for
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/seal_stamp.py:647` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:643` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:229` | round 1's ⬜ 3 — answered |
| round-1 | `skills/verify/scripts/seal_stamp.py:548` | round 1's ⬜ 4 — deferred |
| round-1 | `skills/verify/scripts/seal_stamp.py:584` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2557` | round 1's 🟢 — confirmed |
| round-1 | `hooks/sealer-stamp.py:125` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:520` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:154` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.15.7.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py:220` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
