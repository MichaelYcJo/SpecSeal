# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — review round 3

| Field | Value |
|---|---|
| Target SHA | c374404b6e2cd87f2aa55a97c16469469f40e6c8 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 696 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 10 (the `delegated` note's unrounded comparison), which predates the work item and lies outside every unit the run created, so it takes the filing ladder rather than a fix on this branch |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 is the verifying round after the run's one reopening, so it is the run's last. It targets `c374404b` and verifies round 2's fix range `090edf3b..6bdf8642`, one commit. It was asked whether round 2's 🟡 8 is closed with its class, meaning every comparison of an unrounded value against a threshold it prints rounded. It was also asked whether ⬜ 9 is closed, to review the new unit and the changed regex as finding surfaces, and to check the four re-stamped rows and the corrected changelog sentence.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 8 is closed — both plain-reading gates compare the ratio rounded to the two places it prints | `skills/verify/scripts/session_cost.py:2109`, `:2141` | confirmed | executed: the new unit red with each `round` removed in turn, green at the target; the ratio class enumerated: the grade at `:2519` rounded, the shape ternary at `:2115` correctly unrounded |
| 🟢 | the new unit pins its defect at both gates | `tests/test_session_cost.py:315` | confirmed | executed: red on `batching` with the advisory unrounded, red on `nothing obvious` with that gate unrounded |
| 🟢 | the cross-pin still fails when the script and the protocol disagree | `tests/test_the_handoff_before_round_one.py:611` | confirmed | executed: threshold moved to 1.3, red naming 1.3; comparison unrounded, red on the pattern; the `>= 1.2` gate is read by no pattern, as before the fix |
| 🟢 | round 2's finding 9 is closed at its three coordinates | `skills/verify/scripts/session_cost.py:2500`, `agents/framer.md:180`, `:198` | confirmed | read: widths measured; executed: `tests/test_docs_line_wrap.py` green, ruff check and format check exit 0 |
| 🟢 | the four re-stamped rows' notes and the changelog's corrected sentence are true | `seal/releases/0.8.3.md:126`, `seal/releases/0.9.4.md:32`, `:35`, `seal/releases/0.9.5.md:47` | confirmed | read against the `report` diff; unscoped `evidence-check .` exit 0 |
| 🟡 10 | the `delegated` note compares the unrounded maximum with 60 and prints it rounded, so 59.6 s reads `1.0m` in the column and *never reaches a minute here — 60s at most* under it | `skills/verify/scripts/session_cost.py:2219` | open | executed: a deleted probe, one spawn paired in 59.6 s; finding 8's cause on a duration, predates the work item (`93d27574`, #294) and lies outside every unit this run created, so it takes the filing ladder |
| ⬜ 11 | the changelog fragment's corrected sentence leaves one line at 109 columns — finding 9's class, written by the commit that closed it | `seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/changelog.md:32` | open | read: widths measured; a correction to the run's paperwork, outside `Needs a fix` |

## Paste-ready fixes

```python
    # Compared at what the `delegated` column prints, `minutes` to one place,
    # so the note never says a minute is not reached beside a `1.0m` cell —
    # finding 8's cause, on a duration (#640, round 3's 🟡 10).
    if round(delegated_max / 60, 1) < 1.0:
```
```python
def test_a_delegated_note_does_not_contradict_a_column_at_one_minute(tmp_path):
    """59.6 s prints `1.0m` in the `delegated` column; a note under it saying
    the column never reaches a minute contradicts the row it explains."""
    rows = spawn("A", 0, 59.6, "specseal:smith") + call("a", 80, 85, "git status")
    path = tmp_path / "band.jsonl"
    path.write_text("\n".join(rows) + "\n")
    out = run(["--spawns", str(path)]).stdout
    assert "never reaches a minute" not in out, out
```
```
  `kind` and `bar`. Both the grade and the plain reading's batching advisory
  compare the ratio rounded to the two places they print it to, so a reading
  printed at 1.20 is no longer flagged below 1.2; the advisory's verdict moves
  only for a ratio in [1.195, 1.2), and every other reading stays comparable.
  The protocol's bars table gains the `framing` row. The first reading the
  grade took, over the run that built this change, read this frame's own
  segment at 4.17 tools per turn, 50 calls over 12 turns with a largest batch
  of 11, on a prompt without the old prohibition; one reading, and nothing
  beyond it is claimed from it.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_session_cost.py`, `tests/test_the_handoff_before_round_one.py`, `tests/test_docs_line_wrap.py` at the target | exit 0, 206 passed |
| `bin/evidence-check .`, unscoped, at the target | exit 0; 3182 ok, 0 drifted, 0 broken |
| `ruff check` and `ruff format --check` over the three changed Python files | exit 0 and exit 0 |
| the advisory's `round` removed, new unit and cross-pin run | exit 1 and exit 1: `batching` in the output; *moved off its pattern*; reverted |
| the `nothing obvious` gate's `round` removed, new unit run | exit 1: `nothing obvious` missing; reverted |
| the advisory's threshold moved to `1.3`, cross-pin run | exit 1: names 1.3 against the protocol's sentence; reverted |
| a probe case: one spawn paired in 59.6 s, `--spawns` | exit 1: `delegated` column `1.0m`, note *never reaches a minute here — 60s at most*; probe deleted |
| broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:2507` | round 1's 🟡 1 — fixed |
| round-1 | `agents/framer.md:188` | round 1's 🟡 2 — fixed |
| round-1 | `agents/framer.md:175` | round 1's 🟡 3 — fixed |
| round-1 | `docs/review-handoff-protocol.md:633` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:2536` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:2360` | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_the_handoff_before_round_one.py:550` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/releases/0.4.0.md`, `seal/releases/0.15.7.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/phases/phase-4.md` | round 1's 🟢 — confirmed |
| round-1 | README.md, README.ko.md, `skills/`, `docs/`, `templates/`, `agents/` | round 1's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:2511` | round 2's 🟢 — confirmed |
| round-2 | `agents/framer.md:189` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:2540` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:2358` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_handoff_before_round_one.py:584` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_session_cost.py:3271` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.8.2.md`, `seal/releases/0.15.7.md` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:2102` | round 2's 🟡 8 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py:2500` | round 2's ⬜ 9 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 10 — the `delegated` note's unrounded comparison | a candidate for the filing ladder; no home yet | the repository owner, who opens the issue or names the existing one |
