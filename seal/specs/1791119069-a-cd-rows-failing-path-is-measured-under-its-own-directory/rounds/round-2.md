# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — review round 2

| Field | Value |
|---|---|
| Target SHA | 73ba018c2a984faedce3e6d79156f6d5d4fb7677 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #787 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (`measured_summary` rejects a measured base run when a failing test's captured output carries an inner pytest's nothing-collected line, giving `new?` with a false reason where the base read `failing on base too`). |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of #761 (PR #787), the verifying round, at 73ba018c: open round 1's fixes (range 7e61b596..2bd38cec) and judge whether each closes its finding with no regression — the warnings-only nothing-collected line and `measured_summary` against pytest 9.1.1's summary shapes, plain and `-n 2`; the two-runner limit stated as a pinned rule-3 sentence and whether that judgment holds; the white fixes and answers; the survivor row and the re-stamped fragment rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `measured_summary` rejects the whole output if a nothing-collected line stands anywhere in it, so a base test that fails after printing an inner pytest run (`no tests ran`, or `1 warning in …`) reads `new?` with `NO_RUNNER`'s false reason, where c553bd92 and 94d7b2e0 read `failing on base too` | `skills/verify/scripts/broad_gate.py:1960` | open | executed, probe B plain and `-n 2` at the target and at 94d7b2e0; the fix below restores the measured word, 50 selected cases pass with it, and two of its four rows are red at the target |
| ⬜ 2 | Rule 3's two-runner sentence says `new` comes where the first runner's directory has no such file, and leaves out a same-named file there that passes at the base, which also gives `new` | `templates/config.md:333` | open | executed, probe p1c plain and `-n 2` at the target; the rule's advice covers it |
| ⬜ 3 | Rule 3's corrected clause "and never `new` unless it ran alone and that run collected nothing" is not pinned | `templates/config.md:333` | open | read; the only pin is a substring both wordings carry (contract §14) |
| ⬜ 4 | The `SUMMARIES` comment's `KNOWN_TYPES` list omits `subtests failed` and `subtests skipped`, and calls an all-deselected run's line a summary, which under `-n 2` is `3 warnings in …` | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4519` | open | executed, probe A; read against pytest 9.1.1's `_pytest/terminal.py` |
| ⬜ 5 | Round 1's record cites `2bd38ce1`, which resolves to no commit; the commit is `2bd38cec` | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/rounds/round-1.md:29` | open | executed, `git rev-parse --verify` exit 1; a paperwork correction |
| 🟢 | round 1's finding 1 is closed — a warnings-only nothing-collected line is not read as a summary, and a solo run giving it with exit 4 or 5 reads `new` | `skills/verify/scripts/broad_gate.py:1888` | confirmed | executed, probe A: 8 shapes plain and `-n 2` against pytest 9.1.1 and pytest-xdist 3.8.0; the enumeration read against `_pytest/terminal.py` |
| 🟢 | round 1's finding 2 is closed — rule 3, the docstring, `spec.md:57` and §*Out* state the two-runner limit, the permissive word included, and the fix-pass judgment that measuring it needs mechanism holds | `templates/config.md:333` | confirmed | executed, probe C p1 and p1b plain and `-n 2` at the target; the rule read in `skills/code-review/orchestration.md` |
| 🟢 | round 1's reading fixes 3, 4 and 8 close their findings | `skills/verify/scripts/broad_gate.py:2070` | confirmed | read |
| 🟢 | round 1's answers to 5, 6 and 7 hold | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:9` | confirmed | read |
| 🟢 | survivor-check over the fix range is clean, and the `survivors.md` row quotes text that stands | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/survivors.md:11` | confirmed | executed, exit 0 |
| 🟢 | the 12 fragment `Re-read ·` rows re-stamped in place resolve, and their claims do not rest on what changed | `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md:21` | confirmed | executed, `evidence-check --strict` exit 0; read |
| carried | round 1's confirmations of scope 1–6, the divergences, and `Corrected · B3` / `Corrected · S5` | `skills/verify/scripts/broad_gate.py:2061` | confirmed | carried from round 1; no code under them changed except the summary reading, judged above |

## Paste-ready fixes

```python
def measured_summary(text):
    """pytest's summary line in `text` where the run collected something, or
    None (#761 round 1).

    `PYTEST_SUMMARY_RE` reads any count and clock, and a run that collected
    nothing but counted warnings ends `1 warning in 0.00s`, which it reads.
    That run measured no file, so a line `NOTHING_COLLECTED_RE` reads is
    never a summary, whatever the exit code: read as one, a run of several
    files that the base lacks one of gave `new` for a file the base fails.

    **Only the last such line decides** (#761 round 2). pytest writes its own
    line after everything a test printed, and a failing test that runs
    pytest itself carries that inner run's `no tests ran` line in its
    captured output, above the real `1 failed in …`. Read anywhere, that
    line turned a run that measured the file into `new?`.
    """
    found = list(PYTEST_SUMMARY_RE.finditer(text))
    if not found:
        return None
    nothing = list(NOTHING_COLLECTED_RE.finditer(text))
    if nothing and nothing[-1].start() >= found[-1].start():
        return None
    return found[-1]
```
```python
    # #761 round 2: pytest writes its own line after everything a test
    # printed, so an inner run's line in a failing test's captured output,
    # above the real one, does not decide; a later one does.
    ("=== no tests ran in 0.01s ===\n1 failed in 0.18s", True),
    ("1 warning in 0.00s\n1 failed in 0.01s", True),
    ("1 passed in 0.10s\nno tests ran in 0.00s", False),
    ("1 passed in 0.10s\n1 warning in 0.00s", False),
```
```
and `measured_summary` reads a run as pytest's summary only where no line `NOTHING_COLLECTED_RE` reads stands at or after the last line `PYTEST_SUMMARY_RE` reads, whatever the exit, so an inner run's line in a failing test's captured output does not decide, while a warning count beside any other count stays a summary
```
```
A row that runs pytest in more than one directory — `pytest -q && cd sub && pytest -q` — is asked about every failing file by the first runner a prefix reaches, in that runner's directory: a file a later runner named reads `new` where that directory has no such file or a same-named file there passes at the base, and `failing on base too` where a same-named file there fails at the base.
```
```python
        # #761 round 2's ⬜ 3: the clause round 1's survivor-check corrected.
        "each file reads `new?` with the reason, and never `new` unless it "
        "ran alone and that run collected nothing (below).",
```
```python
# The last line of a pytest 9.1.1 run, and whether it is the summary of a run
# that collected something. `_pytest/terminal.py`'s
# `_build_normal_summary_stats_line` joins one `<count> <type>` per type
# counted, in `KNOWN_TYPES` order — failed, passed, skipped, deselected,
# xfailed, xpassed, warnings, error, then the three subtests types — and a
# plugin's own after them, and writes `no tests ran` where nothing was
# counted. A run that collected nothing counts no test outcome, so its line
# is `no tests ran` or a count of warnings alone (#761 round 1).
# `summary_stats` writes it between `=` rules, bare under `-q`, and not at
# all under `-qq`. A run whose tests were all deselected collected them, and
# plain its line is a summary; under pytest-xdist 3.8.0 the controller
# prints no deselected count, so the same run ends `no tests ran` or a
# warning count and reads as one that collected nothing (#761 round 2).
```
```
it was corrected in `2bd38cec`
```

## Executed probes

| What was run | Result |
|---|---|
| Probe A: pytest 9.1.1 / pytest-xdist 3.8.0 run in 8 shapes (missing file with and without an unknown ini key, missing plus present, a file with no test with an ini warning or a module warning, all deselected, a collection error, a failure), plain and `-n 2`; `measured_summary` and `collected_nothing` at the target, `PYTEST_SUMMARY_RE` at 94d7b2e0 | Every run that collected nothing: target summary false, nothing-collected true (exit 4 plain, 5 under `-n 2`, or 5 for a file with no test). All deselected plain: `1 deselected, 1 warning in 0.00s`, summary. All deselected `-n 2`: `3 warnings in 0.21s`, nothing-collected. Collection error: `1 warning, 1 error` (exit 2) / `3 warnings, 1 error` (exit 1), summary. 94d7b2e0 read every warnings-only line as a summary |
| Probe B: `compare_at_base` on a base whose failing test prints an inner pytest run of an empty directory, and on one printing `1 warning in 0.00s`; row `pytest -q`, plain and `-n 2`, at the target and at 94d7b2e0 | target: `new?` (`NO_RUNNER`) in all four; 94d7b2e0: `failing on base too` in all four; the kept `suite-at-base-1.txt` ends `1 failed in 0.18s` |
| Probe C: `compare_at_base` on `pytest -q && cd sub && pytest -q` (and its `-n 2` form) at the target: p1 root lacks the file and `sub`'s fails at the base; p1b root's same-named file fails and `sub`'s is absent; p1c root's same-named file passes and `sub`'s fails | p1 `new`; p1b `failing on base too`; p1c `new`; each plain and `-n 2` |
| The 🟡 1 fix and its four `SUMMARIES` rows applied in the clone: probe B, then the selected comparison cases (`-k` over the summary, nothing-collected, warnings, limit, `cd`-row, root-row, candidate, base-lacks, lint-first, runner-first, semicolon, no-pytest, stopped, not-pytest, solo-runs and unmeasured-word cases), `-n 4` | probe B `failing on base too` plain and `-n 2`; 50 passed |
| The four new `SUMMARIES` rows against the target's gate | 2 failed (the two `True` rows), 13 passed; the clone restored with `git checkout` |
| `survivor-check --range 7e61b596..2bd38cec --exempt …/survivors.md` in the clone | exit 0; 791 files examined against 39 removed sentences; nothing standing |
| `evidence-check --strict` in the clone at the target | exit 0; 5309 ok, 0 drifted, 0 broken; records: 1 work item read, 0 refused |
| `git rev-parse --verify 2bd38ce1^{commit}` | exit 1 |
| The full suite, lint and typecheck (the broad gate) | not yet — the sealer's, after the rounds settle; not run in this round, and not due while 🟡 1 is open |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
