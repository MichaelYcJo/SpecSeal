# 1790913304 — review round 1 report

Ran by `specseal:warden on claude-opus-5-5`, at `6fa87bed140daaf12087896156997a881a029cc8`
(the build's diff `2bf10c9e..6fa87bed`, where `2bf10c9e` merges
`origin/release/v0.17.0` @ `e4399b65`), in a `git clone --no-local` of the
worktree checked out at that SHA. The worktree was only read, and the one
file written in it is this report.

## In one view

```
fitted(blocks): one rung for the whole message
   files' scales -> 0.90 -> 0.80 -> 0.75 -> no disc  (returned whatever its size)
        |
        +-- 1 block  at #702's size: 6,277 at 0.90           fits, as specced
        +-- 2 blocks at #702's size: 9,356 at 0.75 > 9,000   -> no disc on either   (⬜ 2)
        +-- 8 blocks at #702's size: 10,118 with no disc     -> over the LIMIT       (🟡 1, executed)
```

Everything else the round was asked holds. The removed rows are passes by
construction, the `NOT SEALED` form is untouched, an older values file
still draws, claim-before-print is intact, the two-cell gap holds on every
text line at every rung, the twin keeps the footprint, and the five
corrections in place say what the code now does.

## 🟡 1 — Eight pending seals in one turn print a message the harness persists

`skills/verify/scripts/seal_stamp.py:647` (`fitted` returns `message(None)`
whatever its size), `hooks/sealer-stamp.py:106-136` (`drawings` claims every
pending file before `fitted` is asked).

**What is wrong.** The last rung is bounded per block and not per message.
Each block with no disc is about 1,265 characters over #702's values, so
`fitted` passes `MESSAGE_BUDGET` at eight blocks and `MESSAGE_LIMIT` with
them. Executed: eight values files in #702's shape, written for one session
in a scratch repository and drawn by calling `hooks/sealer-stamp.py` with a
`Stop` payload, printed a `systemMessage` of 10,118 characters. All eight
files were renamed `.drawn.json`, so the next turn has nothing left to draw.

**Why it matters.** This is the failure #717 exists to end, and three
documents promise it cannot happen:

- `spec.md` A3: *"Given any set of pending values files for a session …
  `len(systemMessage) <= MESSAGE_BUDGET`"*.
- `docs/the-broad-gate.md:136`: *"The hook holds its whole message under a
  budget"*.
- `changelog.md:17`: *"the harness never replaces a stamp with a 2 KB preview
  of a file again"*.

`fitted`'s docstring says only a record with an extreme number of deferral
homes could pass the budget at the last rung. That bound is about one block's
height. The count of blocks has no bound at all.

**Who meets it.** The `Stop` hook fires once, at the end of the main
session's turn. In an automation run, one turn spawns a sealer for each work
item it closes, so a milestone of eight or more work items writes that many
files before the one `Stop`. Files also build up wherever the hook cannot
draw for a while, for example a main session whose `python3` is under 3.12.
The A3 cases cover one file and two, and nothing drives more.

**Nothing is lost.** The persisted file holds the whole message, and the
values files are still on disk. So this answers `no` to the floor question.

**The fix** keeps claim-before-print. `drawings` draws every file before any
claim, as it does now. It then claims only the oldest files whose message
fits at the last rung, and leaves the rest pending for the next `Stop`. The
fix names a new helper, admitted, which is not in the tree yet. It is
fenced below, along with the case and the sentence the documents need.

## ⬜ 2 — Two seals in one turn both lose the disc at any real size

`skills/verify/scripts/seal_stamp.py:643-647`.

Executed over #702's values: one block is 6,277 characters at 0.90 and 4,677
at 0.75. Two blocks at 0.75 come to 9,356, which is over 9,000, so `fitted`
skips to the rung with no disc. Both stamps then come out as bare sheets,
2,528 characters together. Any turn that closes two work items will
therefore show no seal at all.

This is built as specced. S1 says *"one rung for the whole message … A
message with two stamps is two stamps at one scale"*, and
`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py#test_two_files_in_one_turn_are_under_the_budget_together`
passes at the rung with no disc. The prompt says the owner never saw the
frame's S1 rule, so this ⬜ is the owner's to read. A per-block rung (the
oldest at 0.90 and the rest without a disc) would come to 7,540 for the same
two files. Nothing is commissioned here.

## ⬜ 3 — The reserve covers two failed gates, and the code says so

`skills/verify/scripts/seal_stamp.py:221-230`. Phase 1 measured 1,274
characters for three failed gates. With a stamp close to 9,000, the message
would then pass the limit. The comment states that limit, and S1 asked for
*at least 1,000*. So this is built as specced. Three gates fail at once only
where a shared module is broken, and in that case `sealer-stamp.py` usually
fails to load too. Recorded so that nobody reads the reserve as unbounded.

## ⬜ 4 — A wide character in a branch moves the disc's row on that line

`skills/verify/scripts/seal_stamp.py:546-556` (`covered` and the width
calculation count code points). Executed with a Korean branch name, rendered
as the twin: that line came out about 11 columns wider than the others, so
the wax on that row is drawn shifted right of the circle. The gap still
holds, cell by cell. The old panel's `|` frame was misplaced in the same way,
because `broad_gate.fit` and `seal_stamp.letter` count code points too. So
the class predates this work item. This repository's branch names are ASCII
by convention.

## ⬜ 5 — A continuation row whose value is `SEALED` is inked as the title

`skills/verify/scripts/seal_stamp.py:584` picks `TITLE` with
`said.strip() == "SEALED"`. Executed: the row `("", "SEALED")` came out in
124. The only way to reach this is a branch named `SEALED`. The test could
key on line 1 of the sheet instead (`ln == 1`).

## What the round was asked, answered

**1. The budget.** Answered by 🟡 1. Executed results for the other inputs
the prompt named:

- A long label is inside the measured text, because `fitted` measures the
  label too and steps down for it.
- A continuation-heavy record passes the limit at the last rung only past
  about 120 continuation rows: 11,583 characters at 120 rows, and 8,829 at
  40.
- The disc-less rung over budget is the case 🟡 1 reaches through the count
  of blocks.
- A unicode branch name (read only): `MESSAGE_LIMIT` was measured with `▀`,
  which is one UTF-16 unit. A character outside the BMP is one Python `str`
  unit and two JavaScript units. Which of the two the harness counts was not
  measured (❓ below). At most one label and one 23-column value are exposed,
  and the reserve is far larger.

**2. Nothing lost.** Read: `drawings` still validates each file at its own
scale before `claim`, and `fitted` cannot raise where that call did not. Its
rungs are `min(scale, rung)` inside the band, and the last rung calls no
`check_scale`. A refused file stays pending
(`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py#test_a_file_at_a_scale_the_band_refuses_is_left_pending`).
The 0.16.0 hook reading a 0.17.0 file gets rows with no `None`, which the
pre-#717 `letter` draws. The 0.17.0 hook reading an older file skips `None`
in `sheet_text`, and `read_values` still accepts it (A13's case, green).

**3. The drawing.** Executed over #702's values, `SAMPLE_ROWS` and #666's
older row shape at 0.90, 0.80 and 0.75. No text cell is covered, the two
cells after every line's last character are parchment, the disc's lowest
line is below the sheet's last, its rightmost column is right of the edge,
and the twin and the block form have equal width on every line. I looked at
the twin of a copy of #702's drawn file (`seal_stamp.py --from <copy>
--shape`), and at the block form's line ends: each sheet line ends in a
painted `187` cell and then `\x1b[0m`.

**4. The rows.** Read: `panel` runs only on the path where `failures` is
empty (`broad_gate.py:2988-3025`), and `Check.failed` is `code != 0`.
`evidence-check` runs with `--strict` (`broad_gate.py:2947`), so drifted and
broken are both 0 on a drawn panel. `chain exit 0`, the suite's `exit 0` and
`0 drifted . 0 broken` were always passes. `failure_lines` and `not_sealed`
carry no diff. `CI also  0 more steps` still prints
(`tests/test_the_gate_names_every_step_ci_runs.py#test_a_seal_that_answers_every_step_says_so`).

**5. The cases.** Read, each against the defect it pins:

- The gap case reads `wax[0] > end + GAP`, so a covered text cell moves `end`
  left and fails it.
- The two-file A3 case fails under `budget=MESSAGE_LIMIT`, because two files
  at 0.75 are about 9,800 characters.
- A9's width is read on the cells: every sheet line is `width` cells long
  unless the disc carries it further. That is the right reading of *"every
  sheet line the same width"*, because a line the disc hangs over is wider
  by design. A painted cell stripped by `colour_row` on any line would break
  the twin-and-block-form equality case, which compares every line.
- No case drives more than two files, which is how 🟡 1 passed.

**6. The records.**

- The five corrections in place (0.10.0 S2, 0.15.7 N5 and N7, #666's N5 and
  N10) each now state what the code does, each carries a
  `Corrected 2026-10-02` note naming the phase, and each points to this
  item's fragment for the new claim.
- The three notes phase 1 wrote (#666's N2, 0.15.7 N7 and 0.15.7 N9) read
  whole. No backtick was lost, no `$` was expanded, and
  each note is true of the code at the target SHA.
- `spec.md`'s two `NAME NOT IN TREE` notes (lines 93 and 100) mark names the
  build renamed or that live in the harness. Both are true.
- `bin/evidence-check .`, run unscoped, exited 0 (3,513 ok, 0 drifted,
  0 broken).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Eight pending values files in one turn make the hook print 10,118 characters; `fitted`'s last rung is returned whatever its size and `drawings` has already claimed every file, so A3's *any set* does not hold and three documents promise otherwise | `skills/verify/scripts/seal_stamp.py:647` | open | Executed: `hooks/sealer-stamp.py` over eight files in #702's shape printed 10,118, every file renamed drawn; `fitted` over n copies crosses `MESSAGE_BUDGET` at eight. `docs/the-broad-gate.md:136`, `changelog.md:17`, `fitted`'s docstring and `spec.md` A3 each claim the bound |
| ⬜ 2 | Two seals in one turn at #702's size both draw with no disc: 9,356 at 0.75 is over 9,000, so the one rung for the whole message is the bare sheet | `skills/verify/scripts/seal_stamp.py:643` | open | Executed; built as S1 specs it (*two stamps at one scale*). A frame judgement the owner did not see, and the owner answers it. A per-block rung would draw 7,540 |
| ⬜ 3 | The reserve covers two failed gates (909) and not three (1,274) beside a stamp near the budget | `skills/verify/scripts/seal_stamp.py:229` | open | Read; the comment states the limit and S1 asked for at least 1,000. Built as specced |
| ⬜ 4 | A wide character in a branch value moves the disc's row on that line by its extra columns | `skills/verify/scripts/seal_stamp.py:548` | open | Executed with a Korean branch in the twin; the same code-point counting misplaced the old frame, so the class predates #717 |
| ⬜ 5 | A continuation row whose value is `SEALED` is inked in the title's 124 | `skills/verify/scripts/seal_stamp.py:584` | open | Executed; reached only by a branch named `SEALED` |
| 🟢 | The rows #717 removes are always passes on a drawn panel, and the `NOT SEALED` form is unchanged | `skills/verify/scripts/broad_gate.py:2557` | confirmed | Read: `panel` only on empty `failures`, `failed` is `code != 0`, the ledger runs `--strict`; `failure_lines` and `not_sealed` carry no diff |
| 🟢 | Claim-before-print holds; a refused or malformed file stays pending; both directions of the 0.16.0 and 0.17.0 hook and file pairing draw | `hooks/sealer-stamp.py:125` | confirmed | Read, and the hook's cases green in the executed run |
| 🟢 | The disc hangs over the bottom and right edges, the two-cell gap holds on every text line, painted trailing cells are kept, and the twin has the block form's footprint | `skills/verify/scripts/seal_stamp.py:520` | confirmed | Executed over three row sets at three rungs, no exception found |
| 🟢 | A9's width is read correctly by the cases, and each new case fails on the defect it pins | `tests/test_the_seal_is_taken_once_by_the_sealer.py:154` | confirmed | Read; the one gap is the count of files, which is 🟡 1 |
| 🟢 | The corrections in place, phase 1's three notes and `spec.md`'s two markers are true of the target SHA | `seal/releases/0.15.7.md` | confirmed | Read whole; `bin/evidence-check .` executed, exit 0 |
| ❓ | Whether the harness counts a character outside the BMP as one or two against `MESSAGE_LIMIT` | `skills/verify/scripts/seal_stamp.py:220` | ❓ out of verified scope | The probe measured BMP characters only, and the warden was told not to run `claude -p`. At most a label and one 23-column value are exposed, against a 1,000 reserve. The orchestrator answers it, should a branch or item name ever carry one |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the five touched modules (stamp, sealer, CI steps, range, gate failure) | 413 passed, exit 0 |
| `bin/evidence-check .`, unscoped | `total: 3513 ok · 0 drifted · 0 broken`, exit 0 |
| `hooks/sealer-stamp.py` called with a `Stop` payload over 6, then 8, values files in #702's shape (new rows) in a scratch repository | 6 files: 7,588 characters, exit 0. 8 files: 10,118, over `MESSAGE_LIMIT`, no file left pending |
| `seal_stamp.fitted` over n copies of #702's block | n=1 6,277 with disc; n=2 2,528 with no disc; n=7 8,853; n=8 10,118 |
| `seal_stamp.stamp` sizes over #702's values, label included | new rows 6,277 / 5,440 / 4,677 / 1,263 at 0.90 / 0.80 / 0.75 / none; #666's rows 6,511 / 5,690 / 4,921 / 1,521 |
| One block with 8, 40, 120 and 150 continuation rows under `rounds` | 6,805, 8,829, 11,583, 14,163 |
| Geometry over #702's new and old rows and `SAMPLE_ROWS` at 0.90, 0.80, 0.75 | no covered text cell, two parchment cells after every line, disc below and right of the sheet, twin width equal on every line |
| `seal_stamp.py --from <copy of #702's drawn file> --shape`, and the block form's line ends | drawn, exit 0; each sheet line ends in a `48;5;187` cell and a reset |
| Twin with a Korean branch value, and a `("", "SEALED")` row | the disc's row shifted about 11 columns; the row inked 124 |
| `fitted` over two `SAMPLE_ROWS` blocks, timed | 0.12 s |
| The full suite, lint and typecheck (the broad gate) | not yet — the sealer's, once the rounds settle |

## Paste-ready fixes

### 🟡 1 — `skills/verify/scripts/seal_stamp.py`, after `fitted`

```python
def admitted(blocks, budget=MESSAGE_BUDGET):
    """How many of `blocks`, oldest first, one message carries under
    `budget` (#717). `fitted`'s last rung is bounded per block — the sheet
    is `PANEL_VALUE_WIDTH` wide — and not per message, so a turn that ends
    with more pending seals than the budget holds draws the oldest that fit
    and leaves the rest for the next turn's end. Never fewer than one: a
    single block is drawn at its smallest whatever its size."""
    count = len(blocks)
    while count > 1 and len(fitted(blocks[:count], budget)) > budget:
        count -= 1
    return count
```

### 🟡 1 — `fitted`'s docstring, the sentence about the last rung

```python
    returned whatever its size, because nothing comes after it: a sheet with
    no disc is about 70 characters a row with its colour codes (2,071 for
    the widest panel this tree can produce, measured 2026-10-02), and its
    width is bounded by `broad_gate.PANEL_VALUE_WIDTH`. Its height is one
    block's, so the count of blocks is bounded by the caller: the hook asks
    `admitted` how many of the pending files one message carries.
```

### 🟡 1 — `hooks/sealer-stamp.py#drawings`

```python
def drawings(stamp, directory):
    """...docstring as now, plus:

    Every file is drawn before any is claimed, and only the oldest files
    one message carries are claimed (`seal_stamp.admitted`, #717): the rest
    stay pending under their own names and are drawn at the next `Stop`."""
    ready = []
    for path in stamp.pending(directory):
        try:
            values = stamp.read_values(path)
            block = (stamp.label(values), values["rows"], values["scale"])
            stamp.stamp(values["rows"], values["scale"], shape=False)
        except Exception:
            continue
        ready.append((path, block))
    keep = stamp.admitted([block for _, block in ready]) if ready else 0
    blocks = []
    for path, block in ready[:keep]:
        if stamp.claim(path) is None:
            continue
        blocks.append(block)
    return blocks
```

### 🟡 1 — the case, `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, beside the two A3 cases

```python
def test_seals_past_what_one_message_carries_wait_for_the_next_turn(tmp_path):
    """A3, any set. Twelve files of a real run's size do not fit one
    message even with no disc, so the hook draws the oldest that fit,
    under `MESSAGE_BUDGET`, and leaves the rest pending for the next
    `Stop` rather than claiming them all and printing a message the
    harness persists. Red against `fitted` over every pending file: twelve
    blocks with no disc are over 15,000 characters."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    paths = [
        mod.write_values(str(repo / ".git"), "s-1", full_values(f"{n:08x}"), now=n)
        for n in range(1, 13)
    ]
    text = json.loads(stop(repo))["systemMessage"]
    assert len(text) <= mod.MESSAGE_BUDGET, len(text)
    drawn = [p for p in paths if os.path.exists(mod.drawn_path(p))]
    waiting = [p for p in paths if os.path.exists(p)]
    assert drawn == paths[: len(drawn)] and waiting == paths[len(drawn) :]
    assert drawn and waiting, (len(drawn), len(waiting))
    assert text.count("\n\n") == len(drawn) - 1, "a drawn file is not in the message"
    later = json.loads(stop(repo))["systemMessage"]
    assert len(later) <= mod.MESSAGE_BUDGET, len(later)
    assert os.path.exists(mod.drawn_path(waiting[0])), "the next turn drew nothing"
```

### 🟡 1 — `docs/the-broad-gate.md:145`, and its pin

```markdown
stamp can come out smaller or without its disc, and never undrawn; a seal
past what one message can carry stays pending and is drawn at the next
turn's end. The
```

```python
    # in test_the_policy_states_the_budget_and_names_its_case, after `rule = ...`
    # (`flat` has already joined the paragraph's lines with single spaces)
    assert "a seal past what one message can carry stays pending" in rule
```

### 🟡 1 — `changelog.md`, the budget bullet's last sentences

```markdown
  0.75 — and last without the disc. A stamp can come out smaller than its
  values file's `scale` says, or without its disc, and is never left
  undrawn; where more seals wait than one message can carry, the oldest
  are drawn and the rest wait for the next turn's end. `seal-stamp` and
  the gate's own terminal drawing are not budgeted.
```

Needs a fix: yes — 🟡 1, the hook claims and prints every pending seal at the last rung whatever the count, so eight or more in one turn reach the harness as a persisted preview.
Loses a record or crashes: no

## Regression tests to plant

- `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`: the
  twelve-file case above, seen red against the tree at `6fa87bed` before the
  fix lands. The hook over eight files printed 10,118 in this round's probe.

## Facts for the evidence ledger

- B2 in this item's fragment should gain the bound on the count of blocks
  once 🟡 1 is fixed: the hook claims only the oldest files `admitted`
  returns, and the rest stay pending. That row's claim, *"returned whatever
  its size"*, is true of `fitted` and does not cover the message.
- The executed sizes above (6,277 at 0.90 over #702's values with the new
  rows; 6,511 with #666's rows) match the build's L1 and the orchestrator's
  handover.

## Carried, not re-established

- `MESSAGE_LIMIT`'s measurement (phase 1's six headless turns) is carried
  from `phases/phase-1.md` as read. The prompt forbade `claude -p`, so it was
  not run again.
- The 47 mutations and the 495-pass count are the build's. This round did
  not re-run them.

## Proof block

Opened in this round: `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/spec.md`,
`overview.md`, `changelog.md`, `survivors.md`, `phases/phase-1.md`;
`skills/verify/scripts/seal_stamp.py` (whole); `hooks/sealer-stamp.py`
(95-171 and the diff); `hooks/dispatch.py` (45-100, 380-530);
`skills/verify/scripts/broad_gate.py` (the diff, 1411, 2474-2514,
2985-3030); `docs/the-broad-gate.md`, `skills/verify/SKILL.md` and
`agents/sealer.md` (the diff); the diffs of
`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (to its suite case),
`tests/test_the_gate_names_every_step_ci_runs.py` and
`tests/test_the_gate_asks_the_range_ci_will_ask.py`; the changed rows of
`seal/releases/0.10.0.md`, `seal/releases/0.15.7.md` and
`seal/ledger/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run.md`,
and the phase-1 commit `e81b6138`'s ledger diff. Not opened: `plan.md` beyond
its diff, `questions.md`, `phases/phase-2.md`, `phases/phase-3.md`.
