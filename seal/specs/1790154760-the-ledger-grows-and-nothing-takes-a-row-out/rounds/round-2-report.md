# 1790154760-the-ledger-grows-and-nothing-takes-a-row-out — review round 2 report

Target SHA `6d3f4296e2709cf24c74f9c61968407cdc5f76c0`, PR #531. A verifying
round: its target is round 1's fix commit
`e554d21cd3253e601e7fb41d6e52ff1f0e2bb36a..7b0e9b75d60b4530c75084ff5bf5b105435eeb07`
and the record commit `6d3f4296`, not the branch.

## What this round was asked

Round 2 of #519 checks whether round 1's two findings, both recorded `fixed`
at `7b0e9b75`, are actually closed. For 🟡 1 it re-derives the stale-cost class
independently: every place in the tree that states what evidence-check, the
ledger, the advisor or the session-start hooks cost, each judged as corrected
with an instrument and a date or as left with sound grounds. That includes the
three sentences the smith left: `hooks/dispatch.py`'s start-up figures, the
rider timings near `ANCHOR_RE`, and `session_cost.py`. It spot-checks the
smith's re-measured numbers in a `--no-local` clone, since the smith replaced
the old ~24 ms / ~60 ms rather than dating them. It judges the new ledger row
C3 and the corrected C2, `spec.md`, `overview.md` and `changelog.md`. For ⬜ 2
it reads the two docstrings. No full suite, lint or broad gate.

## Findings

### Round 1's 🟡 1 is closed

`hooks/ledger-migrate.py:32-40` no longer states "~130 ms". The bullet now
names the date, the interpreter, the platform, the sample (median of five),
and the instrument for each figure. In a clone at the target I re-measured
three of its four numbers with the same instrument. All three agree:

| Stated | Measured here (executed) |
|---|---|
| scan, checker load plus `old_format_rows` in process, ~160 ms | 143–171 ms, median 144 ms |
| this hook wall, ~200 ms, silent | 189–196 ms (median 192 ms), exit 0, empty stdout and stderr |
| whole session-start group, ~300 ms | 256–265 ms (median 262 ms), silent |
| `--strict .`, ~2.0 s | 1.94–2.07 s, exit 0 |

The group figure reads about 13 % low here. My runs used a scratch `HOME`, so
`version-check` and the migrate markers took a different path from a real
home. "~300 ms" is a rounded figure, and the order of magnitude is what the
bullet argues from. That is not a defect.

The bullet also gives a cause: "The scan grows with the ledger's bytes, which
is why it no longer reads ~24 ms". I tested it rather than trusting it,
because the new figure includes loading the checker and the old one may not
have. Split in process: the checker load is 17–29 ms, reading the three files
takes 1–4 ms, and `old_format_rows` over 1,216,723 bytes takes 125 ms. The
scan itself is most of the cost, so the causal sentence holds (executed).

The smith re-measured instead of pasting round 1's text. That was right:
round 1's paste-ready fix carried "~24 ms" and "~60 ms" forward with a
2026-09-01 date, and the scan now measures 125 ms by itself. Round 1's first
Deferred row ("whether ~24 ms and ~60 ms still hold") is answered by this
re-measurement and is closed.

### Re-deriving the class

I grepped every tracked file outside `seal/specs/`, `seal/ledger*` and
`CHANGELOG.md` for a number followed by ms, s, seconds or minutes. I read each
hit in `hooks/`, `skills/`, `docs/`, `agents/`, `templates/`, `README*`,
`CONTRIBUTING.md`, `.github/` and `bin/`. The hits that state a cost of the
check, the ledger, the advisor or a session-start hook:

- `hooks/evidence-advisor.py:6-14`: dated, with its instrument (C2). Holds.
- `hooks/ledger-migrate.py:32-40`: dated, with its instrument (C3). Holds, as above.
- `skills/evidence-check/SKILL.md:457-461`: dated, with its instrument (C3).
  I did not rebuild its 200-file fixture. I timed the CLI on an empty ledger
  instead: 48 ms median with the pyenv interpreter called directly, and about
  40 ms more through the `python3` shim. The stated "~67 ms for an empty
  ledger" falls between those two, so the launcher decides the figure. The
  sentence's point, that the interpreter and the import are nearly all of it,
  holds either way (executed).
- `skills/evidence-check/scripts/evidence_check.py:79-97` (the `ANCHOR_RE`
  rider): these time a regex over ledger rows, and the rider's `Verified`
  stamp dates them. **The grounds for leaving it are sound.**
- `hooks/dispatch.py:5-8`: the start-up cost of a gate process, "on the
  author's machine". This work did not change that cost, and the checker does
  not run on that path. **The grounds for leaving it are sound**, although the
  sentence has no date.
- `skills/verify/scripts/session_cost.py`: session durations, outside the
  class. **The grounds for leaving it are sound.**

Two hits are members of the class that C3's enumeration does not name:

- **`README.md:171-174` and `README.ko.md:170-172`**: "measured: 220ms →
  104ms before a Bash call, 323ms → 120ms after". This is the gate group's
  cost per Bash call. The post-bash group runs `hooks/evidence-advisor.py`
  (`hooks/dispatch.py:39-44`), so it is a stated cost of one of the check's
  hooks, with no date and no instrument. It comes from the initial commit
  (`716d8548`). For a Bash call that is not a commit, the advisor returns
  before it loads the checker. So the dispatch figure is not what #519
  changed, and the dispatch.py grounds apply to it too. The text can stand.
  What is missing is the enumeration: C3 says its grep covered `README*.md`,
  and its list of what was left does not name this line.
- **`seal/ledger.md:132`** (the `scan_candidates` row): "measured at 110 ms
  for one broken row against 200 files and 36 ms degraded past the cap,
  against a 130 ms clean run". The row's `Checked` cell dates it 2026-09-10.
  Its #519 re-read note already says those timings belong to that date's
  fixture and are untouched. The grounds are sound. But C3's clause says
  "**every other place** that states what the check or one of its hooks costs
  names the instrument, the date and the platform". This row names a date and
  no instrument, and C3's grep scope (`hooks/`, `skills/`, `docs/`,
  `README*.md`, `CONTRIBUTING.md`) never reached `seal/`.

Both locations are paperwork: C3's clause and Notes, and the counts in
`spec.md`'s corrected opening and `changelog.md` ("the two other places that
stated one"). No shipped behaviour or user-facing cost statement is wrong. So
this is one ⬜ correction (3 below), and it is left out of `Needs a fix`.

### Round 1's ⬜ 2 is closed

`evidence_check.py:169-174` (`py_spans`) now names `cProfile` and
`/usr/bin/time -p`, the date, the interpreter and the platform.
`tests/test_a_row_points_by_content.py:126-129` names the instrument and the
date; it has no platform, which round 1's finding did not ask for. The
sentence still reads as one sentence (read).

### The corrected records

- **C2** (`seal/ledger/1790154760-…md:15`): the `Corrected 2026-09-23` note
  says what the old count missed and points at C3. Accurate (read).
- **C3** (`:16`): its anchors resolve. `--strict .` exits 0 in the clone with
  0 drifted (executed). Its executed figures match mine within the ranges
  above. The clause is wider than the grep behind it (⬜ 3).
- **`seal/ledger.md:119`** (the `py_spans` row): the hash was re-verified to
  `86eb45b4`. The appended sentence says the fix pass touched only the
  docstring's figures, which matches the diff (read). Editing an existing row
  that the branch re-verified is not an append, so the fragment rule holds.
- **`spec.md`** opening, **`overview.md`** "How many places carried 114 ms",
  **`changelog.md`**: each has a `Corrected` note or plain wording that
  matches the diff. The counts omit the README line (⬜ 3).
- **The record commit `6d3f4296`**: `round-1.md` gains its `Fix range`,
  `Contract changes` and `New units` rows and the ticked `Pass`, and both
  verdict cells move from `open` to `fixed`. Consistent with `7b0e9b75` (read).

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `ledger` CI job's wall time on Linux after the change | `overview.md` §Not verified. Already deferred by the smith and carried by round 1 | the orchestrator, reading PR #531's CI run |
| Whether `README.md`'s "220ms → 104ms / 323ms → 120ms" gate-group figure still holds now that the post-bash group runs five gates, one of them the advisor | not this work item's cost. Left with the dispatch.py grounds, and named in ⬜ 3 so C3 can list it | the orchestrator, when it writes ⬜ 3's correction into C3 |

## Paste-ready fixes

```
C3 Notes, appended after the session_cost.py sentence:
`README.md`'s and `README.ko.md`'s "220ms → 104ms before a Bash call, 323ms → 120ms after" is the gate group's start-up cost per Bash call, which this work did not change, and the advisor in the post-bash group returns before loading the checker on a call that is not a commit; left on the dispatch.py grounds. `seal/ledger.md`'s `scan_candidates` row states 110 ms / 36 ms / 130 ms for its 2026-09-10 fixture, dated by its `Checked` cell and already re-read by this work item. The grep above did not reach `seal/`; this row was found by round 2.
```

Needs a fix: no — both round-1 findings are closed; ⬜ 3 is a correction to C3's enumeration and the counts in spec.md and changelog.md, which are records, not code

Loses a record or crashes: no

## Proof block

Files opened this round: `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/rounds/round-1.md`,
the full diff `e554d21c..7b0e9b75` and `git show 6d3f4296`, `hooks/ledger-migrate.py`,
`hooks/dispatch.py:1-54`, `hooks/cmdline.py:10-25`, `hooks/hooks.json`,
`hooks/evidence-advisor.py` (lines matched), `README.md:160-176`,
`skills/evidence-check/scripts/evidence_check.py:70-100`,
`skills/code-review/scripts/round_record.py:3578-3592`,
`tests/test_a_row_points_by_content.py:782-808`, `seal/ledger.md:132` (the timing and re-read spans),
and the grep output over the tracked tree.
