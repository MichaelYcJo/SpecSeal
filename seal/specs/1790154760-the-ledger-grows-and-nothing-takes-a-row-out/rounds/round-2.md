# 1790154760-the-ledger-grows-and-nothing-takes-a-row-out — review round 2

| Field | Value |
|---|---|
| Target SHA | 6d3f4296e2709cf24c74f9c61968407cdc5f76c0 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 531 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no — both round-1 findings are closed; ⬜ 3 is a correction to C3's enumeration and the counts in spec.md and changelog.md, which are records, not code |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of #519 is a verifying round. It checked whether round 1's two findings, both recorded `fixed` at `7b0e9b75`, are actually closed.

- **Finding 1 (🟡):** it re-derived the stale-cost class on its own: every place in the tree that states what evidence-check, the ledger, the advisor or the session-start hooks cost. Each place is either corrected with an instrument and a date, or left with sound grounds. That covers the three sentences the smith left. It spot-checked the smith's re-measured numbers in a `--no-local` clone, and judged the new ledger row C3 and the corrected C2, `spec.md`, `overview.md` and `changelog.md`.
- **Finding 2 (⬜):** it read the two docstrings.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `hooks/ledger-migrate.py` stated the checker's full run as "~130 ms", undated and with no instrument | `hooks/ledger-migrate.py:32-40` | answered | Carried from round 1. At `7b0e9b75` every figure has an instrument, a date, the interpreter and the platform. Executed in a clone at the target: scan 144 ms, hook 192 ms, session-start group 262 ms, `--strict .` 1.94–2.07 s; the scan alone is 125 ms of that, so the stated cause holds |
| 2 | ⬜ `py_spans`'s docstring and the parse-count case's docstring gave "1,328 parses … 15.8 s" with no instrument | `skills/evidence-check/scripts/evidence_check.py:169-174`, `tests/test_a_row_points_by_content.py:126-129` | answered | Carried from round 1. Both now name the instrument and the date (read) |
| 3 | ⬜ C3 says "every other place" that states a cost of the check or its hooks names the instrument, date and platform. Its enumeration misses `README.md:171-174` / `README.ko.md:170-172` (per-Bash-call gate cost; the post-bash group runs the advisor; undated, no instrument) and `seal/ledger.md:132` (dated by `Checked`, no instrument). `spec.md`'s corrected opening and `changelog.md` count the same short list. Both texts can stand on C3's own dispatch.py grounds; what is wrong is the paperwork's claim of completeness | `seal/ledger/1790154760-the-ledger-grows-and-nothing-takes-a-row-out.md` C3, `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md` opening, `.../changelog.md` | open | Read: grep of all tracked files, `hooks/dispatch.py:35-54` groups, `git log -S` (`716d8548`). A correction to the run's records, not a fix |
| 🟢 | The rider timings near `ANCHOR_RE`, `hooks/dispatch.py`'s start-up figures and `session_cost.py`'s figures are rightly left | `skills/evidence-check/scripts/evidence_check.py:79-97`, `hooks/dispatch.py:5-8`, `skills/verify/scripts/session_cost.py` | not a defect | Read. Dated by the rider's stamp; a gate start-up cost #519 did not change; session durations |
| 🟢 | `skills/evidence-check/SKILL.md`'s rename-scan figures are dated and have their instrument, and their conclusion holds | `skills/evidence-check/SKILL.md:457-461` | not a defect | Executed: empty-ledger CLI 48 ms with the direct interpreter, about 40 ms more through the pyenv shim; the stated 67 ms lies between |
| 🟢 | Round 1's Deferred row on "~24 ms / ~60 ms" is answered: the smith re-measured instead of dating | `hooks/ledger-migrate.py:32-40` | not a defect | Executed, as in 1 |
| 🟢 | C2's correction, the `py_spans` row's re-verified hash and note, `overview.md`, and the record commit `6d3f4296` match the fix diff | `seal/ledger/1790154760-…md:15`, `seal/ledger.md:119`, `rounds/round-1.md` | not a defect | Read; `--strict .` exit 0 executed |

## Paste-ready fixes

```
C3 Notes, appended after the session_cost.py sentence:
`README.md`'s and `README.ko.md`'s "220ms → 104ms before a Bash call, 323ms → 120ms after" is the gate group's start-up cost per Bash call, which this work did not change, and the advisor in the post-bash group returns before loading the checker on a call that is not a commit; left on the dispatch.py grounds. `seal/ledger.md`'s `scan_candidates` row states 110 ms / 36 ms / 130 ms for its 2026-09-10 fixture, dated by its `Checked` cell and already re-read by this work item. The grep above did not reach `seal/`; this row was found by round 2.
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree, checked out at `6d3f4296`; a probe timing a fresh interpreter that loads the checker and runs `old_format_rows` over `seal/ledger.md` and `seal/ledger/*.md`, five runs | 171/156/143/144/144 ms, median 144 ms, no old-format rows, 3 files |
| `hooks/ledger-migrate.py` fed a SessionStart payload, `time.perf_counter` around `subprocess.run`, five runs, scratch `HOME` | 612 (cold)/192/189/189/196 ms, median 192 ms, exit 0, silent |
| `hooks/dispatch.py session-start`, the same way | 913 (cold)/265/256/258/262 ms, median 262 ms, exit 0, silent |
| `evidence_check.py --strict .` at the clone's root, three runs | 2.07 / 1.94 / 1.94 s, exit 0, 0 drifted |
| The scan split in process: checker load, file reads, `old_format_rows` | load 17–29 ms, read 1–4 ms, scan 125 ms over 1,216,723 bytes |
| `evidence_check.py .` on a scratch repository with an empty ledger, direct pyenv interpreter, five runs; `/usr/bin/time -p python3 -c pass` through the shim | median 48 ms; the shim alone takes 0.11–0.12 s real |
| Clean-up | clone, scratch home, scratch repository and both probe scripts removed; the worktree's `git status` is clean apart from this report |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it. It belongs to the sealer, and this round leaves nothing that needs a fix, so the sealer's spawn has come due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/ledger-migrate.py:32-35` | round 1's 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:169-172`, `tests/test_a_row_points_by_content.py:126-128` | round 1's 2 — fixed |
| round-1 | `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md` §1–§3, Scope | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:152-222` | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:186-222`, `:363-371`, `:638-641` | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:180-183` | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:186`, `hooks/evidence-advisor.py:118-120` | round 1's 🟢 — not a defect |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:186-195` | round 1's 🟢 — not a defect |
| round-1 | `.github/scripts/rider_check.py:331`, `:555` | round 1's 🟢 — not a defect |
| round-1 | `hooks/evidence-advisor.py:6-14` | round 1's 🟢 — not a defect |
| round-1 | `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md` Scope 4 | round 1's 🟢 — not a defect |
| round-1 | `tests/test_a_row_points_by_content.py:822` | round 1's 🟢 — not a defect |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `ledger` CI job's wall time on Linux after the change | `overview.md` §Not verified. Already deferred by the smith and carried by round 1 | the orchestrator, reading PR #531's CI run |
| Whether `README.md`'s "220ms → 104ms / 323ms → 120ms" gate-group figure still holds now that the post-bash group runs five gates, one of them the advisor | not this work item's cost. Left with the dispatch.py grounds, and named in ⬜ 3 so C3 can list it | the orchestrator, when it writes ⬜ 3's correction into C3 |
