# 1790835050-the-delegated-note-compares-what-it-prints — review round 1

| Field | Value |
|---|---|
| Target SHA | 7d96a67bd7b3e3981464977f8214694e2184274b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 711 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `7d96a67bd7b3e3981464977f8214694e2184274b..28137a29f2fc0e375e4273dd9347b4a8f8e9ddae`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 targets `7d96a67b` and the diff `e83db346..7d96a67b`, the whole build. It was asked to check stage 1 against `spec.md` and the approved plan. It was then asked to be exact about four things: the new decision against what `minutes()` prints at every boundary and on several interpreters; the frame's class sweep and the batching line left as it is; the new case and its cell reader; and the seven re-stamped rows, including the build's edit to two lines of the frame.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | the note's decision agrees with the printed cell at every boundary, on six interpreters | `skills/verify/scripts/session_cost.py:2225` | confirmed | executed: zero disagreements between `round(x / 60, 1)` and `.1f` over about 1.4M values on 3.9, 3.11, 3.12 (two builds), 3.13 and 3.14; the page at 56.9, 57.0, 57.001, 59.6, 59.99 and 60.0 s never puts the note beside `1.0m`; the band is (57.0, 60) |
| 🟢 | the class sweep is complete, and leaving `:2115` is justified | `skills/verify/scripts/session_cost.py:2115` | confirmed | executed: an `ast` walk found 33 ordering comparisons, all accounted for; read: the ratio is never below 1.0, so *one at a time* is printed only at exactly 1.0 |
| 🟢 | the case is red on the defect and reads the right cell on its fixtures | `tests/test_session_cost.py:2661` | confirmed | executed: red at the base module (exit 1 at `:2681`), green at the target (4 and 192 passed) |
| 🟢 | the records hold: seven rows re-stamped with dated notes, and the frame edit was forced and neutral | `seal/releases/0.9.5.md:13` | confirmed | executed: `evidence-check .` exit 0 unscoped and `--strict`; the framed `spec.md` restored gives exit 2 at `spec.md:32`; read: no claim cell changed |
| ⬜ 1 | `cycle_label` is padded to 30 but never cut, so a long `subagent_type` shifts every cell of its row | `skills/verify/scripts/session_cost.py:2145` | deferred #712 | #712 — Predates the branch; filed with the round's paste-ready fix; executed: `cycle 1  vercel:performance-optimizer` put `1.0m` under `command`; predates the branch; fix it here or defer it as an issue, the smith's call |
| ⬜ 2 | the framer's definition does not warn against stamping a unit its own work will drift | `agents/framer.md:94` | deferred #713 | #713 — A rule for the framer's definition, which a fix pass may not add; filed with the round's draft paragraph; executed: the framed `spec.md:32` stamp makes `evidence-check` exit 2 once the fragment exists; process guidance, not this branch's code |

## Paste-ready fixes

```python
def cycle_label(row):
    """A slice's name in the printed table, cut to the column it is padded to.

    A cycle with no `subagent_type` still gets a name. The label is how a
    reader tells one row from the next, so `cycle 3  ?` is worth more than a
    row that reads as a blank. Cut from the right, as `segment_label` cuts a
    named agent: a label wider than `LABEL_WIDTH` pushes every cell of its
    row out from under its header."""
    if row["kind"] == "cycle":
        return f"cycle {row['cycle']}  {row['subagent_type'] or '?'}"[:LABEL_WIDTH]
    return row["kind"]
```
```markdown
**Name a unit your work will edit without a stamp.** Once the work item's
ledger fragment exists, `evidence-check`'s records arm reads every
`path#unit@hash` in `spec.md` and `plan.md` as a live anchor, and the build
moves that hash. Write the full path and give the hash in words — *at hash
`<hash>` when framed* — so the builder never has to edit your frame to pass
the check.
```

## Executed probes

| What was run | Result |
|---|---|
| the module's delegated cases with the repository's test runner, `-k delegated`, at the target | 4 passed, exit 0 |
| the new case with the base `session_cost.py` checked out in the clone | 1 failed at `tests/test_session_cost.py:2681`, exit 1; restored, tree clean |
| the session-cost and int-guard test modules at the target | 192 passed, exit 0 |
| `evidence_check.py .` and `--strict .`, unscoped, at the target | exit 0 both; 3312 ok · 0 drifted · 0 broken; records 5 read · 0 refused |
| `evidence_check.py .` with the framed `spec.md` restored | exit 2; BROKEN at `spec.md:32`, the bare-file stamp |
| `correction_check.py --range e83db346...7d96a67b` | exit 0, no merge commit |
| ruff check and format check over the two touched code files | exit 0 both |
| round-versus-format agreement on six CPython builds | zero disagreements |
| the `--spawns` page at six durations, at the target and the base, plus a two-spawn run and a long label | as tabled in §1 and ⬜ 1 |
| the broad gate: full suite, repository-wide lint, typecheck | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
