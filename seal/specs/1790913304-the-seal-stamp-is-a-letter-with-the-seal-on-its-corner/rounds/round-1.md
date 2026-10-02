# 1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner — review round 1

| Field | Value |
|---|---|
| Target SHA | 6fa87bed140daaf12087896156997a881a029cc8 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 719 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `59666b18f77850a0fa6e5a05ad1e8f315acc2e90..237dbc5216fd81dcab18f8d51c442d1847063f53`, 6 commits |
| Contract changes | none |
| New units | admitted (depth 1); test_the_title_is_the_sheets_first_line_whatever_a_value_says (depth 1); SMALL_ROWS (depth 1); test_seals_past_what_one_message_carries_wait_for_the_next_turn (depth 1); test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it (depth 1); test_a_character_outside_the_bmp_is_counted_as_two (depth 1) |
| Needs a fix | yes — 🟡 1, the hook claims and prints every pending seal at the last rung whatever the count, so eight or more in one turn reach the harness as a persisted preview. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 targets `6fa87bed`, over the build's diff `2bf10c9e..6fa87bed`. It was asked to check stage 1 against `spec.md` S1–S7 and A1–A20 and the approved plan, then quality, on six things: whether any values file or set of pending files can make the hook print past the limit; whether claim-before-print and both version pairings still hold; the drawing's geometry, the two-cell gap and the twin's footprint; whether the removed panel rows are always passes on a SEALED stamp; whether each new case fails on its defect; and the corrections made in place, with the builder's self-reported heredoc edit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Eight pending values files in one turn make the hook print 10,118 characters; `fitted`'s last rung is returned whatever its size and `drawings` has already claimed every file, so A3's *any set* does not hold and three documents promise otherwise | `skills/verify/scripts/seal_stamp.py:647` | **fixed** `6a2b1142` | fixed at 6a2b1142 — owner-directed change to S1 (questions.md Q6, 2026-10-02): the hook draws as many of the oldest seals as fit with their disc and leaves the rest for the next Stop; Executed: `hooks/sealer-stamp.py` over eight files in #702's shape printed 10,118, every file renamed drawn; `fitted` over n copies crosses `MESSAGE_BUDGET` at eight. `docs/the-broad-gate.md:136`, `changelog.md:17`, `fitted`'s docstring and `spec.md` A3 each claim the bound |
| ⬜ 2 | Two seals in one turn at #702's size both draw with no disc: 9,356 at 0.75 is over 9,000, so the one rung for the whole message is the bare sheet | `skills/verify/scripts/seal_stamp.py:643` | **fixed** `6a2b1142` | fixed at 6a2b1142 — the same change: two seals at #702's size come out as the first whole at 0.90, the second whole at the next Stop; Executed; built as S1 specs it (*two stamps at one scale*). A frame judgement the owner did not see, and the owner answers it. A per-block rung would draw 7,540 |
| ⬜ 3 | The reserve covers two failed gates (909) and not three (1,274) beside a stamp near the budget | `skills/verify/scripts/seal_stamp.py:229` | answered | The comment above MESSAGE_RESERVE states the reserve covers two failed gates and a third would pass the limit; S1 asked for at least 1,000 — built as specced; Read; the comment states the limit and S1 asked for at least 1,000. Built as specced |
| ⬜ 4 | A wide character in a branch value moves the disc's row on that line by its extra columns | `skills/verify/scripts/seal_stamp.py:548` | deferred #720 | #720 — Predates #717: fit, letter and compose all count code points, not display cells; Executed with a Korean branch in the twin; the same code-point counting misplaced the old frame, so the class predates #717 |
| ⬜ 5 | A continuation row whose value is `SEALED` is inked in the title's 124 | `skills/verify/scripts/seal_stamp.py:584` | **fixed** `3dbf8f47` | fixed at 3dbf8f47; Executed; reached only by a branch named `SEALED` |
| 🟢 | The rows #717 removes are always passes on a drawn panel, and the `NOT SEALED` form is unchanged | `skills/verify/scripts/broad_gate.py:2557` | confirmed | Read: `panel` only on empty `failures`, `failed` is `code != 0`, the ledger runs `--strict`; `failure_lines` and `not_sealed` carry no diff |
| 🟢 | Claim-before-print holds; a refused or malformed file stays pending; both directions of the 0.16.0 and 0.17.0 hook and file pairing draw | `hooks/sealer-stamp.py:125` | confirmed | Read, and the hook's cases green in the executed run |
| 🟢 | The disc hangs over the bottom and right edges, the two-cell gap holds on every text line, painted trailing cells are kept, and the twin has the block form's footprint | `skills/verify/scripts/seal_stamp.py:520` | confirmed | Executed over three row sets at three rungs, no exception found |
| 🟢 | A9's width is read correctly by the cases, and each new case fails on the defect it pins | `tests/test_the_seal_is_taken_once_by_the_sealer.py:154` | confirmed | Read; the one gap is the count of files, which is 🟡 1 |
| 🟢 | The corrections in place, phase 1's three notes and `spec.md`'s two markers are true of the target SHA | `seal/releases/0.15.7.md` | confirmed | Read whole; `bin/evidence-check .` executed, exit 0 |
| ❓ | Whether the harness counts a character outside the BMP as one or two against `MESSAGE_LIMIT` | `skills/verify/scripts/seal_stamp.py:220` | ❓ out of verified scope | The probe measured BMP characters only, and the warden was told not to run `claude -p`. At most a label and one 23-column value are exposed, against a 1,000 reserve. The orchestrator answers it, should a branch or item name ever carry one |

## Paste-ready fixes

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
```python
    returned whatever its size, because nothing comes after it: a sheet with
    no disc is about 70 characters a row with its colour codes (2,071 for
    the widest panel this tree can produce, measured 2026-10-02), and its
    width is bounded by `broad_gate.PANEL_VALUE_WIDTH`. Its height is one
    block's, so the count of blocks is bounded by the caller: the hook asks
    `admitted` how many of the pending files one message carries.
```
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
```markdown
  0.75 — and last without the disc. A stamp can come out smaller than its
  values file's `scale` says, or without its disc, and is never left
  undrawn; where more seals wait than one message can carry, the oldest
  are drawn and the rest wait for the next turn's end. `seal-stamp` and
  the gate's own terminal drawing are not budgeted.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
