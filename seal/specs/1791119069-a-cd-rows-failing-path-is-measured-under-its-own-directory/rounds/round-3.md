# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — review round 3

| Field | Value |
|---|---|
| Target SHA | cdcc9d1f72e06d8cf18b16e5626fa523f15d0e7a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #787 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (under `-s`, an inner run a failing base test writes to stderr hides the base run's own `FAILED` lines, so a file the base fails reads `new` where 0.18.1 read `failing on base too`, and only half of that is stated); the run is capped, so it is a `deferred #789` candidate. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of #761 (PR #787), the verifying round and the run's last, at cdcc9d1f: open round 2's fixes (range 20cbdcd9..c91587ca) and judge whether each closes its finding with no regression — base verdicts read only from pytest's own trailer (`measured_summary`'s last summary line, FAILED/ERROR after the last short-summary rule) over real runs plain, `-n 2`, `-r` variants, `-q`/`-qq`, inner runs in captured output and on stderr under `-s`; the two places left on purpose; the white fixes; the survivor rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Under `-s`, an inner pytest run that a failing base test writes to stderr lands after pytest's own lines, and its rule hides the run's own `FAILED` lines, so a file the base fails reads `new` where 0.18.1 and 73ba018c read `failing on base too`. `overview.md` states only that such a run "can still decide", and rule 3 and the changelog fragment state nothing | `skills/verify/scripts/broad_gate.py:1944` | deferred #789 | executed: `compare_at_base` end to end at the target and with 73ba018c's module, rows `pytest -q -s` and `pytest -q`. The statement half (rule 3, `overview.md:37`, the changelog fragment) is in text this run wrote, so it is rung 1's if the orchestrator takes it. The code half needs `run` to keep stdout and stderr apart, which is the ground #789 needs: one output carrying more than one pytest run's lines |
| ⬜ 2 | A run in which pytest wrote no rule (`-rN`, or `-rP` with no failures) or no summary line (`-qq`) reads a test's printed rule or summary as its own. The `SHORT_SUMMARY_RE` comment and round 2's "closed as a class" claim otherwise | `skills/verify/scripts/broad_gate.py:1853` | deferred #789 | executed: real pytest 9.1.1 runs read by the target's and 73ba018c's functions, which give the same words. Not a regression |
| 🟢 | round 2's 🟡 1 is closed — an inner run's `no tests ran` or `FAILED` line in captured output no longer decides | `skills/verify/scripts/broad_gate.py:1967` | confirmed | executed: real runs plain, `-q`, `-n 2`, `-n 2 -q`, `-s`, `-x`, `-x -n 2`, `-rA` with no failures, and an inner empty run plain, `-n 2` and `-s`, all measured right at the target and wrong at 73ba018c; the 9 new cases red at 73ba018c |
| 🟢 | round 2's ⬜ 2 is closed — the two-runner sentence names a same-named file that passes at the base, and its pin holds it | `templates/config.md:333` | confirmed | executed: clause deleted, pin red; the sentence's truth rests on round 2's p1c, and the code under it changed only in a way that gives a passing first runner no rule, so it still reads `new` |
| 🟢 | round 2's ⬜ 3 is closed — the "never `new` unless it ran alone" clause is pinned | `templates/config.md:333` | confirmed | executed: clause deleted, pin red |
| 🟢 | round 2's ⬜ 4 is closed — the `SUMMARIES` comment names the three subtests types and the xdist all-deselected ending | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4626` | confirmed | read against pytest 9.1.1's `KNOWN_TYPES`; executed `-k nomatch` plain and `-n 2` |
| 🟢 | the survivor rows for 0.18.1's frozen B3 excuse the coordinate list, and c91587ca's hashless quote leaves no stamp for the records arm | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/survivors.md:13` | confirmed | executed: survivor-check over `94d7b2e0..HEAD` and over the fix range, exit 0; `evidence-check --strict`, exit 0 |
| 🟢 | the `failing_files` place left on purpose is stated truly | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:36` | confirmed | read: a `;` row's last rule is the second runner's, and a failed suite arm joins `failures` whatever the words |
| carried | rounds 1 and 2's confirmations: scope 1–6, the divergences, `Corrected · B3` / `Corrected · S5`, round 1's findings closed, and round 2's ⬜ 5 answered | `skills/verify/scripts/broad_gate.py:2089` | confirmed | carried from rounds 1 and 2; the code under them changed only in the base reading, judged above |

## Paste-ready fixes

```
A runner with `-s` lets a test write to stderr, and the gate reads stdout and then stderr, so what a failing test writes there stands after pytest's own lines: an inner pytest run written there is read as the run's own, so a file it names reads `failing on base too` and a file the base fails can read `new`. Read either word on such a row as the row's claim rather than a measurement.
```
```python
        # #761 round 3's 🟡 1: an inner run a `-s` test writes to stderr.
        "an inner pytest run written there is read as the run's own, so a file "
        "it names reads `failing on base too` and a file the base fails can "
        "read `new`.",
```
```
- Under `-s` a test's output is written live, and what it writes to stderr lands after pytest's own lines, because the gate joins stdout and then stderr. An inner pytest run written there is read as the run's own in both directions: a file it names reads `failing on base too`, and its `short test summary info` rule hides the run's own `FAILED` lines, so a file the base fails reads `new` — which 0.18.1 read `failing on base too`. Telling the two streams apart needs `run` to keep them apart, which a fix pass may not add; `templates/config.md` rule 3 names the shape, and #789 holds the ground.
```
```
  Under `-s`, what a test writes to stderr lands after pytest's own lines,
  so an inner run written there is still read as the run's own, and a file
  the base fails can read `new`; `templates/config.md` rule 3 names it.
```
```python
# The rule pytest writes above its own `FAILED` and `ERROR` lines, padded
# with `=` to the terminal's width (#761 round 2). What a test printed into
# its captured output stands above it, so where pytest wrote this rule a
# run's own lines are the ones after the last one. pytest writes it only
# where a line follows (none under `-rN`, and none for `-rP` on a run with
# no failures), and a test's stderr under `-s` lands after it; in those
# runs the last rule can be one a test printed (#761 round 3).
```

## Executed probes

| What was run | Result |
|---|---|
| Real pytest 9.1.1 / pytest-xdist 3.8.0 runs in a scratch project: a pytester test whose inner run fails `tests/test_g.py` and the outer fails; a pytester test whose inner run is empty; a subprocess test that writes an inner run to stderr; a passing pytester test that prints an inner failing run. Each output joined the way `run` joins it and read by `measured_summary` and `verdicts_at_base` at the target and at 73ba018c | target right, 73ba018c wrong: plain, `-q`, `-n 2`, `-n 2 -q`, `-s`, `-x`, `-x -n 2`, `-rA` with no failures, inner empty run plain/`-n 2`/`-s`, stderr inner run without `-s`. Target wrong: stderr inner run with `-s` and with `-s -n 2` (🟡 1). Both wrong alike: `-rN`, `-rP` with no failures (⬜ 2). `-qq`: both measured off the inner summary, words right (⬜ 2) |
| `compare_at_base` end to end on a scratch git repository, rows `pytest -q -s` and `pytest -q`, target module and 73ba018c's | `-s`: target `test_err.py` `new`, 73ba018c `failing on base too`. Without `-s`: target right on both files |
| The new cases with 73ba018c's `broad_gate.py` checked out in the clone (`-k` over the base-run, summary and inner-output cases) | 9 failed, 20 passed; the file restored with `git checkout` |
| The narrow cases at the target (`-k` over the summary, measured, inner-output, solo-runs, nothing-collected and warnings cases) | 64 passed |
| Each of the two rule-3 clauses deleted from `templates/config.md` in the clone, then the solo-runs pin | red both times; the file restored |
| `pytest -q -k nomatch` plain and `-n 2` | `1 deselected in 0.00s`; `no tests ran in 0.22s` |
| survivor-check `--range 94d7b2e0..HEAD` and `--range 20cbdcd9..c91587ca`, each with `--exempt` on this work item's `survivors.md` | exit 0 both; the fix range shows two 0.18.1 survivors, each excused |
| `evidence-check --strict` in the clone at the target | exit 0 |
| The full suite, lint and typecheck (the broad gate) | not yet — not run in this round; the sealer's, once the run ends |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:2126` | round 1's 🟡 1 — fixed |
| round-1 | `templates/config.md:333` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2049` | round 1's ⬜ 3 — fixed |
| round-1 | `tests/test_release_hygiene.py:159` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:9` | round 1's ⬜ 5 — answered |
| round-1 | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/plan.md:89` | round 1's ⬜ 6 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:1935` | round 1's ⬜ 7 — answered |
| round-1 | `skills/verify/SKILL.md:509` | round 1's ⬜ 8 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2034` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md:16` | round 1's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:1960` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4519` | round 2's ⬜ 4 — fixed |
| round-2 | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/rounds/round-1.md:29` | round 2's ⬜ 5 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:1888` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2070` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/survivors.md:11` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md:21` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2061` | round 2's carried — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1: under `-s`, an inner run on stderr hides the base run's own lines, and a file the base fails reads `new` | #789, as a comment: same ground (one output carrying more than one pytest run's lines). Its proposed summary count must not count an inner pytester run's summary in captured output, or every failing file of a pytest-plugin suite reads `new?` | #789's owner, the repository owner, who filed it as a `bug` in the review-chain backlog |
| ⬜ 2: a run with no rule or summary of its own (`-rN`, `-rP`, `-qq`) reads a test's printed rule or summary as its own | #789, as a comment, on the same ground | #789's owner, the repository owner |
