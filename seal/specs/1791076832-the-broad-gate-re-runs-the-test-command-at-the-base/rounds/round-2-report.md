# Round 2 report — 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base

Target `eafc2021` on `fix/747-the-broad-gate-re-runs-the-test-command-at-the-base`,
against `release/v0.18.1` at `e141980a`. Reviewed by warden. This is the
verifying round for round 1's fixes, fix range `88b8c632..457f773e`
(`c3a5bd80`, `0b208e42`, `457f773e`), and `eafc2021` closes round 1's record.
I stayed inside that diff and the new units round 1's record names. I opened
two things outside it. One is the readers of the word `new` (`agents/sealer.md`,
`agents/smith.md`, `skills/verify/SKILL.md`), because round 1's finding 5 named
them. The other is `chain_check`'s `APPROVED_RE`, because finding 8 depends on it.

Carried from round 1, not re-established: the coordinates of every finding,
the pytest 9.1.1 measurements of the `!` rule at 40 and 44 columns, and the
cargo line. Re-derived here: every verdict.

## What the account claimed, and what was checked

| Claim | Where it is made | What I found | How |
|---|---|---|---|
| Round 1's new cases were red against `88b8c632` | ledger B3, *Executed* | Holds. The cargo case, the `cd` case, the 40-column ending, the `&` rows, the counterfeit pin and every `SUMMARY_LINES` row fail against `88b8c632`'s gate. The `SUMMARY_LINES` rows fail there because the attribute is missing, so that red says nothing about each line. The ledger's nine regex mutations are what holds each line, and I did not repeat them | **executed** |
| `PYTEST_SUMMARY_RE` alone now says pytest ran, and every pytest summary line reads | the unit's comment, ask 🟡1 | **Does not hold.** pytest 9.1.1 prints `2 failed, 1 subtests passed in 0.01s` when a failing file uses the built-in `subtests` fixture, and the regex rejects it. Finding 1 | **executed** |
| A path absent at the branch root is run at the base with the others, and where the base lacks it too the whole run reads `new?` | `compare_at_base` comment at `skills/verify/scripts/broad_gate.py:2054` | Holds. pytest 9.1.1 given one real and one missing path exits 4 with `no tests ran in 0.00s` and `ERROR: file or directory not found`. That matches neither the summary regex nor `ERROR_RE` | **executed** |
| The fix pass enumerated how a cut run is read, by axis, in its hand-back | the ask | **Not opened.** The hand-back is in no file of the work item or the branch. I enumerated by axis myself, below | read |

## How a cut run is read, enumerated by axis

There are five ways the reading can give a word no run measured. I enumerated
them by what the reading decides, not by example rows.

1. **Which run counts as pytest's (`PYTEST_SUMMARY_RE`).**
   - *False positive* (another tool's line is taken): closed. The line has to
     start with a digit, be lowercase count words and a clock, and nothing
     else. Cargo, `uv`'s `Resolved 12 packages in 3ms`, unittest, ruff and the
     unitless clock are all refused.
   - *False negative* (a pytest line is refused): open. It costs a
     measurement and never fakes one. But it is a regression, because
     pytest's own subtests line was read before the fix. Finding 1.
2. **Whether the appended files reached pytest.**
   - A wrapper that drops its arguments: documented as round 1 asked.
   - A `cd`: closed where the root lacks the path. One direction is still
     open: the root carries a different file at the same relative path. See
     *Deferred*.
   - A runner whose output goes to a file and a later part that prints it
     (`pytest -q > log; cat log`): the next prefix runs the full suite at the
     base without the files and prints its lines. That run includes the
     files, so it is measured. Expensive, but not a counterfeit.
3. **Whether the run named the file (`FAILED_RE`, `ERROR_RE`).**
   - `-rN` and `--no-summary` print the count line and no `FAILED` line, so
     the base would read `new` for a file it fails. Executed against pytest
     9.1.1.
   - It stays closed because the branch side is symmetric. `failing_files`
     reads the same `FAILED` lines, so a row with either flag compares
     nothing.
   - Only a pytest configuration that differs between the base and the
     branch could open it. Not probed.
4. **Whether every collected test ran (`STOPPED_EARLY_RE`).** Closed by
   `!+`. A false match can only turn `new` into `new?`.
5. **What the reason says when nothing was read.** `NO_RUNNER` says no part
   of the row "printed a pytest summary". With colour forced on, with `-qq`
   and with the subtests line, pytest did print one. Finding 2.

## Findings

### 🟡 1 — pytest's own subtests summary is not read as pytest's, so a file the base fails reads `new?` where it used to read `failing on base too`

The coordinate is `skills/verify/scripts/broad_gate.py:1861`. The new
`PYTEST_SUMMARY_RE` allows one word after each count. pytest 9 includes the
`subtests` fixture, and when a run has subtests the summary carries a
two-word label. Measured with pytest 9.1.1:

- a failing file printed `2 failed, 1 subtests passed in 0.01s`;
- a passing one printed `1 passed, 2 subtests passed in 0.00s`.

The regex rejects both.

I ran the whole gate on a fixture. The row is the runner alone, and the base
and the branch both fail `tests/test_two.py`, which uses one subtest.

- **At `eafc2021`:** `tests/test_two.py` reads `new? not measured: no part of
  the row printed a pytest summary at the base`.
- **Against `88b8c632`'s gate:** it read `failing on base too`, which is
  true, because `suite_counts` accepted the line.

So the fix for round 1's finding 1 traded a counterfeit for a lost
measurement in a shape the old reading got right. For a runner-first row
with parts after the runner, the cost is larger. Every later prefix is tried
too, and each one re-runs the runner without the files, which means the full
suite at the base.

Why it matters: a repository that uses the subtests fixture gets `new?` for
every failure that touches one. The reason printed beside it is false
(finding 2). Nothing in the comment or in rule 3 names this shape.

The class is a count label pytest or a plugin writes in more than one word,
which pytest builds from the category a plugin reports. The fix admits one
extra lowercase word per label. I checked it against every `SUMMARY_LINES`
row, both subtests lines, `Resolved 12 packages in 3ms` and `3 files would
be reformatted in 0.5s`: every pytest line is accepted and every other line
is refused. Patched into the scratch clone, the subtests fixture read
`failing on base too`, and the 28 #747 summary, cut and reading cases
stayed green.

### ⬜ 2 — `NO_RUNNER`'s reason says no pytest summary was printed, where the gate only failed to recognise one

The coordinates are `skills/verify/scripts/broad_gate.py:1869` and
`skills/verify/SKILL.md:505`. The reason reads "no part of the row printed a
pytest summary at the base". Rule 3 at `templates/config.md:333` now names
three shapes where pytest prints its summary and the gate does not read it:
colour forced on, `-qq` (which prints none), and, until finding 1 is fixed,
subtests. For the first and the last, the sentence a person reads is false.

The action it sends them to is still right: open the kept files and run the
file by hand. The word `new?` is correct. So this is ⬜.

Suggested wording: "no part of the row printed a line the gate reads as
pytest's summary". The reason is pinned whole by
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it`, so the pin
and `skills/verify/SKILL.md`'s *New?* bullet change with it.

## Round 1's verdicts, answered

- **Finding 1 (cargo).** Closed. The cargo case is green at the target and
  red against `88b8c632`. One new direction opened, finding 1 above.
- **Finding 2 (`cd`).** Closed. The fix departs from the reviewer's
  proposal: it runs the file at the base instead of reporting it `new?`
  unrun. I judge that choice sound. In every `cd` shape the fix measures at
  least what the proposal would have measured, and it never gives a word
  the proposal would have withheld. Executed:
  - a shared file under `cd` reads `failing on base too`;
  - a shared file and a branch-new file under `cd` both read `new?`, as the
    comment says. `88b8c632` gave both `new`;
  - the proposal would have given `new?` to every `cd` file, measured or not.

  Reading the working tree rather than `HEAD` is the right reference,
  because the failing names come from running the working tree.
- **Finding 3 (lone `&`).** Closed. Under `/bin/sh` the `&` ends no prefix,
  `cmd.exe` still cuts there, and `a |& b` cuts once, at the `|`. The three
  rows are green at the target and red against `88b8c632`.
- **Finding 4 (`!+`).** Closed. It is a superset of `!{3,}`, so it can only
  add `new?`. The 40-column ending is red against `88b8c632`.
- **Finding 5 (the wrapper).** Closed. Rule 3, the `compare_at_base`
  docstring and the `verdicts_at_base` docstring name it, and
  `test_the_one_counterfeit_the_gate_cannot_see_is_named` pins two of the
  three. The readers of `new` in `agents/` and `skills/verify/SKILL.md` do
  not claim more than rule 3 allows.
- **Findings 6 and 7 (prose).** Read and closed. Rule 3's list now matches
  `POSIX_CUTS` and `CMD_CUTS`. The "not modelled" list names compound
  commands and `>|`.
- **Finding 8 (approval line).** Closed. `APPROVED_RE` matches one line of
  `plan.md` at the target.

## Regression tests to plant

The destination is `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in
`SUMMARY_LINES`. The two subtests lines go in as rows that must be read as
pytest's. They are red against `eafc2021`'s regex: I executed the regex
against the lines, and the gate fixture read `new?`.

I propose no end-to-end case, because one would need the `subtests` fixture,
which only pytest 9 carries. The row-level pins do not depend on pytest's
version.

## Facts for the evidence ledger

- pytest 9.1.1 under `-q` prints `N passed, M subtests passed in Xs` when a
  run has passing subtests, and folds a failed subtest into `failed`.
  Measured this round.
- pytest 9.1.1, given a path that does not exist beside one that does,
  exits 4 and prints `no tests ran in 0.00s` and `ERROR: file or directory
  not found: <path>`. Measured this round.
- `PYTEST_SUMMARY_RE` changes content under the fix, so its anchor in ledger
  row B3 needs re-verification.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | pytest 9's subtests summary (`2 failed, 1 subtests passed in 0.01s`) is not read as pytest's, so a file the base fails reads `new?` where `88b8c632` gave `failing on base too` | `skills/verify/scripts/broad_gate.py:1861` | open | executed: the regex against pytest 9.1.1's measured lines; the gate on a subtests fixture gave `new?` at `eafc2021` and `failing on base too` at `88b8c632`; the proposed regex gave `failing on base too` and kept 28 cases green |
| ⬜ 2 | `NO_RUNNER` says no part printed a pytest summary, where with colour forced on or a two-word label pytest did and the gate did not read it | `skills/verify/scripts/broad_gate.py:1869` | open | read; the word `new?` and the action it asks for are right, the sentence is not |
| 🟢 | round 1's finding 1 is closed — a cargo line is no longer taken for pytest's | `skills/verify/scripts/broad_gate.py:2076` | confirmed | executed: the end-to-end cargo case green at `eafc2021`, red at `88b8c632` |
| 🟢 | round 1's finding 2 is closed — a file under a `cd` is run at the base | `skills/verify/scripts/broad_gate.py:2061` | confirmed | executed: shared file `failing on base too`; shared plus branch-new under `cd` both `new?`, where `88b8c632` gave both `new`; the departure from the proposal measures at least as much and fakes nothing |
| 🟢 | round 1's finding 3 is closed — a lone `&` ends no prefix under `/bin/sh` | `skills/verify/scripts/broad_gate.py:1988` | confirmed | executed: `a & b`, `a & b && c`, `a \|& b` green at `eafc2021`, red at `88b8c632` |
| 🟢 | round 1's finding 4 is closed — the `!` rule is read at one `!` a side | `skills/verify/scripts/broad_gate.py:1852` | confirmed | executed: the 40-column ending green at `eafc2021`, red at `88b8c632` |
| 🟢 | round 1's finding 5 is closed — the wrapper that drops its arguments is named | `templates/config.md:333` | confirmed | executed: the pin green at `eafc2021`, red at `88b8c632`; read: the readers of `new` claim no more than rule 3 |
| 🟢 | round 1's findings 6 and 7 are closed — rule 3's operator list and the not-modelled list | `templates/config.md:333` | confirmed | read |
| 🟢 | round 1's finding 8 is closed — `plan.md`'s approval line reads | `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/plan.md:7` | confirmed | executed: `APPROVED_RE` matches one line |

## Paste-ready fixes

### 🟡 1

```python
# The line that says pytest ran: its counts and its wall clock alone on a
# line, bare under `-q` or between `=` rules — `1 failed, 1 passed in 0.02s`,
# `== 768 passed in 612.34s (0:10:12) ==`. `suite_counts` takes any count
# followed by a clock, which is right for the panel and wrong for choosing the
# run at the base: `cargo test` prints `test result: ok. 0 passed; …; finished
# in 0.00s`, and read as pytest's it gave `new` for a file the base fails
# (round 1's 🟡 1). A label is the category pytest or a plugin reports, and
# one of pytest 9's own is two words — `2 failed, 1 subtests passed in
# 0.01s` (round 2's 🟡 1) — so a label is one lowercase word or two. A run
# whose line carries colour codes, a longer label, or no line at all (`-qq`)
# is not read as pytest's, and its files read `new?`.
PYTEST_SUMMARY_RE = re.compile(
    r"^=*\s*\d+ [a-z]+(?: [a-z]+)?(?:, \d+ [a-z]+(?: [a-z]+)?)* in \d+(?:\.\d+)?s"
    r"(?: \(\d+:\d\d:\d\d\))?\s*=*$",
    re.M,
)
```

```python
SUMMARY_LINES = [
    ("1 failed, 1 passed in 0.02s", True),
    ("1 error in 0.06s", True),
    ("2 failed, 1 passed, 2 errors in 0.22s", True),
    ("==== 768 passed, 1 skipped, 3 warnings in 612.34s (0:10:12) ====", True),
    # pytest 9.1.1 with the built-in `subtests` fixture (round 2's 🟡 1).
    ("2 failed, 1 subtests passed in 0.01s", True),
    ("1 passed, 2 subtests passed in 0.00s", True),
    (
        "test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; "
        "1 filtered out; finished in 0.00s",
        False,
    ),
    ("no tests ran in 0.00s", False),
    ("Found 2 errors.", False),
    ("Ran 3 tests in 0.001s", False),
    ("Resolved 12 packages in 3ms", False),
    ("4 checks in 12", False),
    ("1 passed in 0.01s, and a linter went on talking", False),
    ("\x1b[31m1 failed\x1b[0m, \x1b[32m1 passed\x1b[0m\x1b[31m in 0.02s\x1b[0m", False),
]
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the #747 cases of `tests/test_the_seal_is_taken_once_by_the_sealer.py` in a `--no-local` scratch clone at `eafc2021` | `62 passed` |
| The same cases with `88b8c632`'s `broad_gate.py` swapped in | `17 failed`: every `SUMMARY_LINES` row (attribute missing), `a & b`, `a & b && c`, `a \|& b`, the counterfeit pin, the cargo case, the `cd` case; the 40-column `MEASURED_ENDINGS` row failed in a separate run of `test_the_base_run_is_read_off_what_pytest_printed`; restored |
| pytest 9.1.1 endings, each run against `PYTEST_SUMMARY_RE`, `STOPPED_EARLY_RE`, `FAILED_RE`: subtests failing and passing, a missing path beside a real one, `--no-summary`, `-rN`, a plain failure | subtests `2 failed, 1 subtests passed in 0.01s` and `1 passed, 2 subtests passed in 0.00s` both refused by the regex, accepted by `suite_counts`; missing path exit 4, `no tests ran in 0.00s`, refused; `--no-summary` and `-rN` print the count line and no `FAILED` line |
| The gate on three fixtures (`base_then_feature`), at `eafc2021` and at `88b8c632` | subtests file the base fails: `new?` at the target, `failing on base too` before; `cd sub` with a shared and a branch-new failing file: both `new?` at the target, both `new` before; `cd sub` where the branch adds a passing `tests/test_two.py` at the root: `new` at both, with the base failing `sub/tests/test_two.py` |
| The proposed regex against every `SUMMARY_LINES` row, both subtests lines, `Resolved 12 packages in 3ms`, `3 files would be reformatted in 0.5s` | all as intended; patched into the clone, the subtests fixture read `failing on base too` and 28 summary, cut and reading cases passed; restored |
| `APPROVED_RE` over `plan.md` at the target | 1 line matches |
| `ruff check` and `ruff format --check` on `skills/verify/scripts/broad_gate.py` and the sealer test module | `All checks passed!`, `2 files already formatted` |
| The broad gate: the full suite, the repository-wide lint and the typecheck at `eafc2021` | not yet — the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `cd` row whose failing path the branch also adds at the root, as a different file, reads `new` unrun though the base fails the file below the `cd`; this is the residue of round 1's finding 2, older than this branch (the gate at `88b8c632` does the same) and only closable by deciding absence from a run at the base rather than from the tree | not filed; a design change to how absence is decided, outside this round's fix | the repository owner — whether to file it |
| A file the branch reports only as `ERROR` gets no base comparison | already deferred in round 1 (`spec.md` Out, `overview.md` *Not done*) | the repository owner, as the frame names |

Needs a fix: yes — 🟡 1 (pytest 9's two-word subtests label is not read as pytest's summary, so a file the base fails reads `new?`)
Loses a record or crashes: no

## Proof

Files opened this round: `skills/verify/scripts/broad_gate.py` (lines
1801–2090, 3195–3230), `tests/test_the_seal_is_taken_once_by_the_sealer.py`
(the fix diff, `base_then_feature`, `SUITE_ROW`, the A9 pin), `templates/config.md`
(rule 3, through the diff), `skills/verify/SKILL.md:498-512`,
`agents/smith.md:385-396`, `agents/sealer.md:40-48`,
`skills/code-review/scripts/chain_check.py:3946`, the work item's
`rounds/round-1.md`, `rounds/round-1-report.md`, `changelog.md`, `plan.md`
(through the diff), and the ledger fragment's diff in `457f773e`. The asked
paragraph for this round, from the orchestrator's scratchpad.
