# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — review round 2 report

Ran by: specseal:warden on claude-opus-5-5
Target SHA: 73ba018c2a984faedce3e6d79156f6d5d4fb7677 (PR #787, base `release/v0.18.2` at 94d7b2e0)
Round kind: verifying. The target is round 1's fix range `7e61b596..2bd38cec` and the closing commit `73ba018c`.
Worked in: a `git clone --no-local` at the target, under `<scratchpad>/<work-item-id>/round-2/clone`. That clone and every probe beside it were deleted before handover.

## Summary

Round 1's two fixes and its three reading fixes close their findings. The
answers to ⬜5, ⬜6 and ⬜7 hold. survivor-check is clean over the fix range,
the `survivors.md` row anchors on text that exists, and the 12 re-stamped
`Re-read ·` rows resolve.

One of the new units introduced a regression, and that is the finding this
round opens:

1. **`measured_summary` reads every line of the output, so it can veto a run that did measure the file (🟡 1).**
   Suppose a base test fails and its captured output carries a pytest run of
   its own, such as a pytester-based test or one that shells out to pytest.
   The inner run's `no tests ran` line, or its warnings-only line, now turns
   the whole run into `new?`. Its reason says no summary was printed, but the
   real `1 failed in …` line is the last line of the output. Both c553bd92 and
   94d7b2e0 read that file `failing on base too`. Measured plain and with
   `-n 2`.
2. Three wording or pinning gaps that change no behaviour (⬜ 2, ⬜ 3, ⬜ 4).
3. One wrong SHA in round 1's record, a paperwork correction (⬜ 5).

The smith enumerated the endings of pytest 9.1.1. I checked that enumeration
against `_pytest/terminal.py` and against real runs, plain and `-n 2`, and it
holds with one exception: under xdist, a run whose tests were all deselected
does not print its deselected count. That exception changes no word a
candidate gets, and ⬜ 4 records it.

I agree that telling two runners apart needs new mechanism. Rule 3 states
the limit truly, including the permissive `failing on base too`. One case is
left out of its enumeration (⬜ 2).

## What the account claimed, and what was checked

| Claimed (round-1.md, the fix commits, the ledger fragment) | Found |
|---|---|
| A run that collected nothing ends only with `no tests ran` or a count of warnings alone. `_build_normal_summary_stats_line` writes one `<count> <type>` per counted type in `KNOWN_TYPES` order, or `no tests ran` | **Holds.** I read the installed pytest 9.1.1's `_pytest/terminal.py`. `KNOWN_TYPES` is failed, passed, skipped, deselected, xfailed, xpassed, warnings, error, subtests passed, subtests failed and subtests skipped, with a plugin's own types appended after them. `no tests ran` is written only where no part was counted. Executed: 8 shapes, plain and `-n 2`, in probe A below |
| `summary_stats` writes the line between `=` rules, bare under `-q`, and not at all under `-qq` | **Holds.** `verbosity < -1` returns, and `display_sep = verbosity >= 0`. Read |
| "A deselected count means tests were collected, so `3 deselected in …` stays a summary" | **Holds plain, and under `-n 2` the count is not printed.** With `-k nomatch` and an unknown ini key, plain prints `1 deselected, 1 warning in 0.00s` (exit 5) and `-n 2` prints `3 warnings in 0.21s` (exit 5). Under xdist that run therefore reads as one that collected nothing. A solo run reads `new` either way, and a group reads `new?` instead of `new`, so both words stay honest. The `SUMMARIES` comment's "its line is a summary" is wrong under xdist (⬜ 4). Executed |
| `measured_summary` "never reads a line `NOTHING_COLLECTED_RE` reads as pytest's summary" | **Holds as written, and the implementation is wider than the sentence.** The guard searches the whole output, so such a line anywhere vetoes a real summary elsewhere (🟡 1). Executed |
| 🟡 2: a fail-closed verdict "needs new mechanism", which a fix pass may not add | **Holds.** `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it* says "A fix pass may not add mechanism. Not a rule, not a checker". Either count summary lines in the branch's output or run the whole row at the base: each is a new reading, so each is a checker. Round 1's own report also said the fix is the statement and its pin. Read |
| Rule 3's two-runner sentence: `new` "where that directory has no such file", `failing on base too` "where a same-named file there fails at the base" | **True, and incomplete.** p1 and p1b reproduce at the target, plain and `-n 2`. A third case, p1c, also reads `new`: the root carries a same-named file that passes at the base while `sub`'s file fails there (⬜ 2). Executed |
| ⬜ 3: rule 3's "never `new`" sentence was corrected in `2bd38ce1` | The sentence was corrected in `2bd38cec`. `2bd38ce1` resolves to no commit (⬜ 5). The new clause is true, and nothing pins it (⬜ 3). Executed (`git rev-parse --verify`) and read |
| The 12 fragment `Re-read ·` rows were re-stamped in place | **Holds.** The 12 rows moved `templates/config.md#"## Broad gate"` from `c0c82527` to `e5460edf`, S8's `# Repository config` from `511589d2` to `e5a6ae70`, and C4's `VERSIONS_OF_ANOTHER_PRODUCT` from `f063f519` to `61b300a7`. The fix range changed only rule 3 and one reason string. B4's claim ("names the rows it cannot measure") is strengthened, and none of the other claims rest on rule 3. `evidence-check --strict` exits 0 at the target. Executed and read |

## Findings from execution

### 🟡 1 — a pytest line in a failing test's captured output turns a measured base run into `new?`

**Where.** `skills/verify/scripts/broad_gate.py:1960`, the guard
`if NOTHING_COLLECTED_RE.search(text): return None` in `measured_summary`.
This is a unit that round 1's fixes created (New units, depth 1).

**What happens.** `compare_at_base` hands `measured_summary` the whole
output of one prefix. The guard rejects that output if any line anywhere in
it matches `NOTHING_COLLECTED_RE`. A failing test's captured stdout is
printed raw in the failures section, above pytest's own last line. If the
test ran pytest itself and printed that run, an inner
`===== no tests ran in 0.01s =====` or `1 warning in 0.00s` is alone on a
line there. The guard then discards a run whose last line is `1 failed in
0.18s`. The file reads `NO_RUNNER`, which says "no part of the row printed a
line the gate reads as pytest's summary at the base". That reason is false:
the row printed the summary, and it is the last line of the kept
`suite-at-base-1.txt`.

**Measured** (probe B, the base's only test failing after printing an inner
`python -m pytest` of an empty directory, and a second test printing
`1 warning in 0.00s`; row `pytest -q`, plain and `-n 2`):

| Gate | Inner `no tests ran` | Printed `1 warning in 0.00s` |
|---|---|---|
| target 73ba018c | `new?` (`NO_RUNNER`), plain and `-n 2` | `new?` (`NO_RUNNER`), plain and `-n 2` |
| 94d7b2e0 | `failing on base too`, plain and `-n 2` | `failing on base too`, plain and `-n 2` |
| target with the fix below | `failing on base too`, plain and `-n 2` | not re-run; the `SUMMARIES` rows cover it |

**Why it matters.** The word is fail-closed, so nothing gets through. But
this is a regression from a measured word to an unmeasured one, and the
reason given to the reader is false. A reader who trusts it goes looking for
a runner the row does have. Two kinds of suite meet this shape: one that
tests a pytest plugin with pytester, and one with a test that runs pytest in
a subprocess and prints its output. Both are suites a broad gate is pointed
at. The same lines read `failing on base too` at c553bd92, where the bare
`PYTEST_SUMMARY_RE` decided, so round 1's fix introduced the regression.

**The fix keeps the unit and changes its body.** pytest writes its own
stats line after everything a test printed, and the prefix being measured
ends at the runner. So the last line either pattern reads is the run's own
line. Decide on that line. The fix adds no unit. It changes
`measured_summary`'s body and adds rows to `SUMMARIES`, which is
the depth rule's allowance for a finding inside a depth-1 unit. The rule
does not allow a new unit to pin it.

Shown with the fix applied in the clone: probe B reads
`failing on base too` plain and `-n 2`. The selected comparison cases (the
`SUMMARIES` and `NOTHING_COLLECTED` tables, the warnings e2e case plain and
xdist, the limit case, the `cd`-row, root-row, candidate, lint-first,
runner-first and pin cases) gave 50 passed. Against the target's gate, the
two new `True` rows are red and the two new `False` rows are green. The
`False` rows are there to pin that the fix does not loosen the reading for
a run whose own last line is the nothing-collected one.

## Findings from reading (and from the probes that settled them)

### ⬜ 2 — rule 3's two-runner sentence names two of the three ways the row's words come out

**Where.** `templates/config.md:333`, the sentence beginning "A row that
runs pytest in more than one directory". It is pinned verbatim in
`test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`.

**What.** The sentence says `new` comes out "where that directory has no
such file". Probe p1c gives `new` in a third shape, plain and `-n 2`. There
the root carries a same-named `tests/test_two.py` that passes at the base,
and `sub/tests/test_two.py`, which the branch reports, fails at the base.
The file is not a candidate. The group's run measures the root's passing
file and gives `new`, though the base fails the file the row reported. The
advice that follows ("Read either word as the row's claim") covers this
case, so the rule's conclusion is right. A reader who checks the root and
finds a same-named file could still conclude this `new` is measured.
Behaviour and advice stand, so this is ⬜.

The permissive word is stated truly. p1b reproduces `failing on base too`
at the target, plain and `-n 2`, for a file the base never ran. The rule
names it, and so do the `compare_at_base` docstring and `spec.md` §*Out*. In
this gate the word labels a failure and never seals it. The gate's `SUITE`
arm fails whatever the verdicts are (`broad_gate.py:3308`, which feeds
`failure_lines` only).

### ⬜ 3 — rule 3's corrected "never `new`" clause is not pinned

**Where.** `templates/config.md:333`: "each file reads `new?` with the
reason, and never `new` unless it ran alone and that run collected nothing
(below)". Commit `2bd38cec` wrote it.

**What.** The only pin over that sentence is
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it`'s
`"each file reads `new?` with the reason"`, which both the old and the new
wording carry. Deleting the new clause turns nothing red. Contract §14 says a
change a person reads is pinned in the same commit. This is the same class
as round 1's ⬜ 8.

### ⬜ 4 — the `SUMMARIES` comment lists `KNOWN_TYPES` short and calls an all-deselected run's line a summary

**Where.** `tests/test_the_seal_is_taken_once_by_the_sealer.py:4519`. This
is a unit that round 1's fixes created.

**What.** The comment's `KNOWN_TYPES` list stops at "subtests passed". The
pytest 9.1.1 tuple also holds `subtests failed` and `subtests skipped`.
"A run whose tests were all deselected collected them, and its line is a
summary" is true plain (`1 deselected, 1 warning in 0.00s`). Under `-n 2`
the controller prints `3 warnings in 0.21s`, or `no tests ran`, with exit 5,
and the gate reads that as nothing collected. No word changes for a
candidate: a solo run reads `new` either way. A group reads `new?` where the
plain run reads `new`. The comment is what a later reader trusts about
xdist, and here it is wrong about xdist.

### ⬜ 5 — round 1's record cites a commit that does not exist (a paperwork correction)

**Where.**
`seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/rounds/round-1.md:29`.
The Grounds cell of ⬜ 3 says "it was corrected in `2bd38ce1`".

**What.** `git rev-parse --verify 2bd38ce1^{commit}` exits 1 at the target.
The commit that corrected rule 3 is `2bd38cec`
(`2bd38cec06d92409430f845f16944ce9ee3a9292`), the tip of the fix range. This
is a correction to the run's paperwork. It is left out of `Needs a fix`.

## Confirmations

- **Round 1's 🟡 1 is closed.** `NOTHING_COLLECTED_RE` (`broad_gate.py:1888`)
  reads `no tests ran` and a count of warnings alone, singular and plural,
  bare or between rules. Probe A ran the 8 shapes plain and `-n 2`.
  `measured_summary` was false and `collected_nothing` was true for every
  run that collected nothing: missing file with or without an ini warning,
  file with no test with an ini warning or a module-level warning, missing
  plus present, and all deselected under xdist. Every run that collected
  something gave a summary: a collection error with warnings (`1 warning, 1
  error`, exit 2; `3 warnings, 1 error`, exit 1 under xdist), a failure with
  warnings, and all deselected plain. 94d7b2e0's `PYTEST_SUMMARY_RE` read
  every warnings-only line as a summary, which was the defect. The e2e case
  passed in my selected run with the 🟡 1 fix applied. The orchestrator's
  run at the target is a claim I did not repeat. Reordering the walk (a solo
  run's `collected_nothing` first) changes no word: a solo run that collected
  nothing has no captured output and an exit of 4 or 5.
- **Round 1's 🟡 2 is closed as a statement.** Rule 3, the
  `compare_at_base` docstring, `spec.md:57`, `spec.md` §*Out* (`spec.md:153`)
  and the changelog fragment all say a two-runner row's words are the row's
  claim. The two-runner sentence is pinned. The "needs mechanism" judgment
  holds (see the table above).
- **⬜ 3, ⬜ 4 and ⬜ 8 fixes.** The docstring's second paragraph names
  `measured_summary` and no longer says "never `new`". The 9.1.1 exemption
  names `NOTHING_COLLECTED_RE`. The `SKILL.md` glob is pinned. Read.
- **⬜ 5, ⬜ 6 and ⬜ 7 answers.** `overview.md` holds six divergence rows.
  For ⬜ 6, this repository's row costs three prefix runs per candidate:
  `ruff check` three times, `ruff format --check` twice, `bin/test` once.
  Rule 3's "one more run of each prefix up to and including the runner"
  states it, and leaving the frame's `plan.md` as written is a paperwork
  choice I accept. For ⬜ 7, `new?` from an exit-remapping runner never lets
  a failure through. Read.
- **survivor-check.** `survivor-check --range 7e61b596..2bd38cec --exempt
  …/survivors.md` exits 0, "no removed wording is still standing". The
  exemption's quote stands at #747's `spec.md:50`, a frame of a released work
  item. Executed.
- **Carried from round 1, not re-derived:** the scope 1–6 confirmation, the
  divergence confirmation, and the `Corrected · B3` / `Corrected · S5`
  confirmation. No code under them changed in the fix range except the
  summary reading, and I re-judged that above. p1 and p1b re-ran at the
  target in probe C and gave round 1's words.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in `SUMMARIES`: the
  four two-line rows in the 🟡 1 fix below. Two are red at the target.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`:
  the ⬜ 3 clause, and the ⬜ 2 sentence if that wording is taken.

## Facts for the evidence ledger

- D1's `measured_summary` clause changes with the 🟡 1 fix. The wording is
  under Paste-ready fixes. Its `measured_summary` and `SUMMARIES` hashes
  re-stamp.
- pytest-xdist 3.8.0 does not print a deselected count on the controller's
  stats line. Executed in probe A: `-k nomatch -n 2` ends `3 warnings in
  0.21s`, exit 5.

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

## Paste-ready fixes

### 🟡 1

`skills/verify/scripts/broad_gate.py`, `measured_summary`, the whole function:

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

`tests/test_the_seal_is_taken_once_by_the_sealer.py`, four rows at the end of `SUMMARIES` (the case wraps each in `F.\n…\n`):

```python
    # #761 round 2: pytest writes its own line after everything a test
    # printed, so an inner run's line in a failing test's captured output,
    # above the real one, does not decide; a later one does.
    ("=== no tests ran in 0.01s ===\n1 failed in 0.18s", True),
    ("1 warning in 0.00s\n1 failed in 0.01s", True),
    ("1 passed in 0.10s\nno tests ran in 0.00s", False),
    ("1 passed in 0.10s\n1 warning in 0.00s", False),
```

The ledger fragment's D1, the clause after "never of a run of several, where collecting nothing does not say which file the base lacks;":

```
and `measured_summary` reads a run as pytest's summary only where no line `NOTHING_COLLECTED_RE` reads stands at or after the last line `PYTEST_SUMMARY_RE` reads, whatever the exit, so an inner run's line in a failing test's captured output does not decide, while a warning count beside any other count stays a summary
```

### ⬜ 2

`templates/config.md:333`, the two-runner sentence. The same text goes into the pinned tuple entry:

```
A row that runs pytest in more than one directory — `pytest -q && cd sub && pytest -q` — is asked about every failing file by the first runner a prefix reaches, in that runner's directory: a file a later runner named reads `new` where that directory has no such file or a same-named file there passes at the base, and `failing on base too` where a same-named file there fails at the base.
```

### ⬜ 3

A fifth entry in the tuple of `test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`:

```python
        # #761 round 2's ⬜ 3: the clause round 1's survivor-check corrected.
        "each file reads `new?` with the reason, and never `new` unless it "
        "ran alone and that run collected nothing (below).",
```

### ⬜ 4

`tests/test_the_seal_is_taken_once_by_the_sealer.py:4519`, the comment over `SUMMARIES`:

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

### ⬜ 5

`seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/rounds/round-1.md:29`, in ⬜ 3's Grounds cell:

```
it was corrected in `2bd38cec`
```

Needs a fix: yes — 🟡 1 (`measured_summary` rejects a measured base run when a failing test's captured output carries an inner pytest's nothing-collected line, giving `new?` with a false reason where the base read `failing on base too`).
Loses a record or crashes: no

## Proof block

Files opened at the target in the clone, or read from the installed tools:

- `skills/verify/scripts/broad_gate.py`: lines 1840–1975 (`ERROR_RE` through `measured_summary`), 2061–2180 (`compare_at_base`), 1421–1460 (`run`), 3280–3340 (the gate's call site), and the fix-range diff.
- `templates/config.md`: rule 3 at line 333, through the fix-range diff and `2bd38cec`'s diff.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: lines 4488–4660 (the new case, `SUMMARIES`, `NOTHING_COLLECTED`, the solo-runs pin) and `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`.
- `tests/test_release_hygiene.py`: the 9.1.1 exemption, through the diff.
- `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/`: `rounds/round-1.md`, `rounds/round-1-report.md` (summary, finding 2 and its fix), and the diffs of `spec.md`, `overview.md`, `changelog.md` and `survivors.md`.
- `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`: through the fix-range diff.
- `seal/releases/0.18.1.md`, `0.17.0.md` and `0.15.4.md`: the B4, P10 and S1 rows.
- `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/spec.md:50`: the survivor quote.
- `skills/code-review/orchestration.md`: lines 55–100 and §*A fix pass adds the unit that pins it*.
- `bin/test`.
- pytest 9.1.1's `_pytest/terminal.py`: `KNOWN_TYPES`, `summary_stats`, `build_summary_stats_line`, `_build_normal_summary_stats_line` and `format_session_duration` · NAME NOT IN TREE
