# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — review round 2

| Field | Value |
|---|---|
| Target SHA | eafc2021d567c1bf7d4627548ad9bb7d118da842 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #758 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `4e981840fc3da6f9ba3a9546ba2c9f832a10b3fb..55b402872c51a5b0dd7bdce14433624dfd9e3e60`, 4 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (pytest 9's two-word subtests label is not read as pytest's summary, so a file the base fails reads `new?`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item `1791076832-the-broad-gate-re-runs-the-test-command-at-the-base` (#747 and #748, PR #758). It is the verifying round for round 1's fixes, range `88b8c632..457f773e`. Open each fix and judge whether each round-1 verdict is closed:
- 🟡1: only `PYTEST_SUMMARY_RE` now says pytest ran.
- 🟡2: a path absent at the branch root is run at the base with the others, instead of being called absent, and branch presence is read from the working tree.
- 🟡3: a lone `&` no longer ends a prefix under `/bin/sh`.
- 🟡4: `^!+ .+ !+$`.
- 🟡5: the argument-dropping wrapper is stated as a limit.
- ⬜6 and ⬜7: the prose.

The new units the fixes created are a finding surface: `PYTEST_SUMMARY_RE`, `SUMMARY_LINES` and the new cases. 🟡2 departs from the reviewer's proposal: it runs the file rather than reporting `new?` unrun, so judge that choice. The fix pass also enumerated how a cut run is read, by axis, in its hand-back. Check that enumeration for a direction that still yields a word no run measured.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | pytest 9's subtests summary (`2 failed, 1 subtests passed in 0.01s`) is not read as pytest's, so a file the base fails reads `new?` where `88b8c632` gave `failing on base too` | `skills/verify/scripts/broad_gate.py:1861` | **fixed** `542e1122` | fixed at 542e1122 — `cf441933`, `b2876cdb`; executed: the regex against pytest 9.1.1's measured lines; the gate on a subtests fixture gave `new?` at `eafc2021` and `failing on base too` at `88b8c632`; the proposed regex gave `failing on base too` and kept 28 cases green |
| ⬜ 2 | `NO_RUNNER` says no part printed a pytest summary, where with colour forced on or a two-word label pytest did and the gate did not read it | `skills/verify/scripts/broad_gate.py:1869` | **fixed** `542e1122` | fixed at 542e1122 — `cf441933`; read; the word `new?` and the action it asks for are right, the sentence is not |
| 🟢 | round 1's finding 1 is closed — a cargo line is no longer taken for pytest's | `skills/verify/scripts/broad_gate.py:2076` | confirmed | executed: the end-to-end cargo case green at `eafc2021`, red at `88b8c632` |
| 🟢 | round 1's finding 2 is closed — a file under a `cd` is run at the base | `skills/verify/scripts/broad_gate.py:2061` | confirmed | executed: shared file `failing on base too`; shared plus branch-new under `cd` both `new?`, where `88b8c632` gave both `new`; the departure from the proposal measures at least as much and fakes nothing |
| 🟢 | round 1's finding 3 is closed — a lone `&` ends no prefix under `/bin/sh` | `skills/verify/scripts/broad_gate.py:1988` | confirmed | executed: `a & b`, `a & b && c`, `a \|& b` green at `eafc2021`, red at `88b8c632` |
| 🟢 | round 1's finding 4 is closed — the `!` rule is read at one `!` a side | `skills/verify/scripts/broad_gate.py:1852` | confirmed | executed: the 40-column ending green at `eafc2021`, red at `88b8c632` |
| 🟢 | round 1's finding 5 is closed — the wrapper that drops its arguments is named | `templates/config.md:333` | confirmed | executed: the pin green at `eafc2021`, red at `88b8c632`; read: the readers of `new` claim no more than rule 3 |
| 🟢 | round 1's findings 6 and 7 are closed — rule 3's operator list and the not-modelled list | `templates/config.md:333` | confirmed | read |
| 🟢 | round 1's finding 8 is closed — `plan.md`'s approval line reads | `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/plan.md:7` | confirmed | executed: `APPROVED_RE` matches one line |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:2032` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2021` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1964` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1850` | round 1's 🟡 4 — fixed |
| round-1 | `templates/config.md:333` | round 1's 🟡 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1919` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/plan.md:7` | round 1's ⬜ 8 — answered |
| round-1 | `tests/test_the_commit_gate_decides_at_the_commit.py:434` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1841` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1894` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A `cd` row whose failing path the branch also adds at the root, as a different file, reads `new` unrun though the base fails the file below the `cd`; this is the residue of round 1's finding 2, older than this branch (the gate at `88b8c632` does the same) and only closable by deciding absence from a run at the base rather than from the tree | not filed; a design change to how absence is decided, outside this round's fix | the repository owner — whether to file it |
| A file the branch reports only as `ERROR` gets no base comparison | already deferred in round 1 (`spec.md` Out, `overview.md` *Not done*) | the repository owner, as the frame names |
