# 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base — review round 1

| Field | Value |
|---|---|
| Target SHA | 9570fa1b6379f4797d090c6e7896b114cc91f39e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #758 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `88b8c632b85a00e167d6ab1aa5c0d0a390c6fe57..457f773e103efd22d7cca1cb84011cfa6b18cfd5`, 3 commits |
| Contract changes | none |
| New units | PYTEST_SUMMARY_RE (depth 1); SUMMARY_LINES (depth 1); test_only_pytests_own_summary_line_says_pytest_ran (depth 1); test_the_one_counterfeit_the_gate_cannot_see_is_named (depth 1); test_a_part_that_is_not_pytest_is_passed_over_though_it_prints_counts (depth 1); test_a_file_named_below_a_cd_is_run_at_the_base_and_not_called_new (depth 1) |
| Needs a fix | yes — 🟡 1 (cargo's line read as pytest's summary), 🟡 2 (a `cd` row's file reads `new` unasked), 🟡 3 (a lone `&` runs a background part in the foreground at the base), 🟡 4 (the `!{3,}` rule misses pytest at 40–45 columns), 🟡 5 (a summary-printing wrapper's `new` is documented as measured) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item `1791076832-the-broad-gate-re-runs-the-test-command-at-the-base` (#747 and #748, PR #758), target `9570fa1b` against `release/v0.18.1` at `e141980a`. Spec compliance comes first: the cutting scanner over the `/bin/sh` and `cmd.exe` grammars (quotes, `$(…)`, backticks, `( … )` and `2>&1` are not cut), the prefix attempts at the base, the verdict rules (`failing on base too` only on a `FAILED`/`ERROR` line naming the file, `new` only with a summary and no early-stop banner, everything else `new?` with its reason), Q1 (a base `ERROR` counts) and Q2 (rule 3 states both orders), and #748's polling case still failing with the group kill removed. Quality comes second. The risk to weigh is a verdict that reads as measured when it is not: a `new` or `failing on base too` the gate cannot stand behind. Enumerate the row shapes the gate accepts by construction (`templates/config.md` §*Broad gate*). The orchestrator verified the 4 changed test modules (715 passed, 79 skipped) and ruff on the 5 changed Python files at the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The base re-run takes `cargo test`'s result line for pytest's summary, so a lint-first `cargo test && pytest` row reads `new` for a file the base fails | `skills/verify/scripts/broad_gate.py:2032` | **fixed** `c3a5bd80` | fixed at c3a5bd80 — `0b208e42`; executed, probe D: `tests/test_two.py  new` with the base failing it; prefix 1 printed only cargo's line |
| 🟡 2 | A `cd sub && …` row's failing file is asked about at the repository root, found absent, and reads `new` with no run at the base | `skills/verify/scripts/broad_gate.py:2021` | **fixed** `c3a5bd80` | fixed at c3a5bd80; executed, probe A: `new`, no `suite-at-base-*.txt` kept, base fails the file |
| 🟡 3 | Under `/bin/sh` a prefix ending at a lone `&` runs the backgrounded part in the foreground with no bound, so a part that never ends hangs the gate at the base | `skills/verify/scripts/broad_gate.py:1964` | **fixed** `c3a5bd80` | fixed at c3a5bd80; executed, probe B: 12 s sleeper ran in the foreground as prefix 1, gate 13.7 s; the old `&&`-only cut never did this |
| 🟡 4 | `STOPPED_EARLY_RE` needs three `!`, and pytest at 40–45 columns writes one or two, so an interrupted base run reads `new` for an unnamed file | `skills/verify/scripts/broad_gate.py:1850` | **fixed** `c3a5bd80` | fixed at c3a5bd80; executed: pytest 9.1.1 at `COLUMNS=40` printed `! Interrupted: 1 error during collection !`; `verdicts_at_base` on that ending gave `new` |
| 🟡 5 | A part that prints pytest's summary but drops the appended files gives `new`, while rule 3 and `compare_at_base` say a word is only given from a run that measured it | `templates/config.md:333` | **fixed** `c3a5bd80` | fixed at c3a5bd80; executed, probe C: `sh -c '…test_one.py'` first part, `tests/test_two.py  new` with the base failing it |
| ⬜ 6 | Rule 3 says "the same but `;` under `cmd.exe`" for a list that lacks `;`, and calls a runner whose output goes to a file "never reached" | `templates/config.md:333` | **fixed** `c3a5bd80` | fixed at c3a5bd80; read; the finding-3 fix rewrites the sentence |
| ⬜ 7 | `row_prefixes`' "Not modelled" list omits compound commands and `>\|` | `skills/verify/scripts/broad_gate.py:1919` | **fixed** `c3a5bd80` | fixed at c3a5bd80; read; each costs a measurement and fakes none |
| ⬜ 8 | `plan.md`'s approval line carries a second sentence after "spawned.", so `chain_check` reports it absent | `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/plan.md:7` | answered | corrected at `c3a5bd80`: `plan.md`'s Approved line now ends at its one sentence, and the Q1/Q2 note sits on the line below; `APPROVED_RE` matched 0 lines before and 1 after; executed: a dry run of `round-record new` in the scratch clone printed the notice; a correction, not counted in `Needs a fix` |
| 🟢 | #748's case polls and is red without the group kill | `tests/test_the_commit_gate_decides_at_the_commit.py:434` | confirmed | executed: red with `the row's loop outlived the bound` under `proc.kill()`, reverted, green 3 of 3 |
| 🟢 | Q1 (a base `ERROR` line reads `failing on base too`) and Q2 (rule 3 states both orders) are built as answered | `skills/verify/scripts/broad_gate.py:1841` | confirmed | read: `ERROR_RE` joins `FAILED_RE` in `verdicts_at_base`; rule 3's last sentences state both costs and pick neither |
| 🟢 | The cut does not split quotes, `$(…)`, backticks, `( … )` or `2>&1` in either grammar, and the base re-run stays in `compare_at_base`'s own body | `skills/verify/scripts/broad_gate.py:1894` | confirmed | read; the orchestrator executed the parametrised cases and the shell-site case |

## Paste-ready fixes

```python
# The line that says pytest ran: its counts and its wall clock and nothing
# else, bare under `-q` or between `=` rules -- `1 failed, 1 passed in
# 0.02s`, `== 768 passed in 612.34s (0:10:12) ==`. `suite_counts` takes any
# line where a count is followed by a clock, which is right for the panel and
# wrong here: `cargo test` handed a test file prints `test result: ok. 0
# passed; 0 failed; …; finished in 0.00s`, and read as pytest's it gave
# `new` for a file the base fails (round 1, finding 1).
PYTEST_SUMMARY_RE = re.compile(
    r"^=*\s*\d+ [a-z]+(?:, \d+ [a-z]+)* in \d+(?:\.\d+)?s"
    r"(?: \(\d+:\d\d:\d\d\))?\s*=*$",
    re.M,
)
```
```python
                if PYTEST_SUMMARY_RE.search(tried.text):
                    measured = tried.text
                    break
```
```python
# What `cargo test` printed when handed a test file, measured in round 1.
CARGO_LINE = (
    "test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; "
    "1 filtered out; finished in 0.00s"
)


def test_a_line_that_only_carries_counts_and_a_clock_is_not_pytest(tmp_path):
    """Round 1, finding 1. The first part prints what `cargo test` prints for
    a filter that matched nothing; it is not pytest, so the comparison goes
    on to the part that is, and the base's failure is found."""
    cargo = f"{sys.executable} -c \"print('{CARGO_LINE}')\""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{cargo} && {SUITE_ROW}",
        {"tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE, out.stdout
```
```python
UNPLACED = (
    f"{NOT_MEASURED}: neither the base nor this branch carries this path at "
    "the repository root, so the row ran its tests somewhere else and the "
    "base was not asked"
)
```
```python
        absent = [
            f for f in files if git(scratch, "cat-file", "-e", f"HEAD:{f}") is None
        ]
        # pytest names a file relative to where it ran, and a `cd` part moves
        # that. Absence at the base says the test arrived with this branch
        # only where the branch carries the same path at the root; otherwise
        # the question was asked of the wrong directory (round 1, finding 2).
        unplaced = [
            f for f in absent if git(root, "cat-file", "-e", f"HEAD:{f}") is None
        ]
        present = [f for f in files if f not in absent]
        verdicts = {f: (UNPLACED if f in unplaced else NEW) for f in absent}
```
```python
def test_a_file_named_below_a_cd_is_not_called_new_unasked(tmp_path):
    """Round 1, finding 2. The row runs pytest from `sub`, so the failing
    file is named `tests/test_two.py` and the root carries no such path.
    It used to read `new` with no run at the base, which fails it."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {SUITE_ROW}",
        {"sub/tests/test_two.py": FAILING_TEST, "sub/tests/test_one.py": PASSING_TEST},
        {"sub/tests/test_two.py": FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().UNPLACED, out.stdout
```
```python
            if op and not (op == "&" and command[i - 1 : i] in ("<", ">")):
                # An operator before any command leaves nothing to run. Under
                # `/bin/sh` a lone `&` backgrounds the part before it, so a
                # prefix ending there would run that part in the foreground,
                # which the row never does -- and a server or a `tail -f`
                # there never ends (round 1, finding 3). `cmd.exe` runs the
                # two in turn, so there it is a cut like `;` is in `sh`.
                if command[:i].strip() and (cmd_exe or op != "&"):
                    prefixes.append(command[:i].rstrip())
                i += len(op)
                continue
```
```text
    A cut falls at a TOP-LEVEL operator of the grammar of the shell the row
    is handed to: `&&`, `||`, `;` and `|` for `/bin/sh`, where a lone `&`
    ends a part but no prefix, and `&&`, `||`, `&` and `|` for `cmd.exe`,
    which `cmd_exe` selects.

    **Not modelled, and named rather than claimed:** a `{ …; }` brace group,
    a compound command (`if`, `for`, `while`, `case`), a `${…}` holding an
    operator, a `>|` redirection, and a `#` comment, each of which can put a
    cut where the shell has none. A prefix ending before a `|` runs the
    producer without its consumer, which ends only where the producer ends
    on its own.
```
```python
        ("a & b", ["a & b"]),
        ("a & b && c", ["a & b", "a & b && c"]),
```
```text
It cuts the row at its top-level operators — `&&`, `\|\|`, `;` and `\|` under `/bin/sh`, where a lone `&` is never a cut because the part before it runs in the background, and `&&`, `\|\|`, `&` and `\|` under `cmd.exe`, where `;` separates nothing — and runs each prefix with the files appended until one prints pytest's summary.
```
```text
A runner inside a `( … )` group or behind a part that fails at the base is never reached, and one whose output goes to a file is run but not read: each reads `new?`.
```
```python
# … `_pytest/terminal.py` writes a `!` separator for `shouldfail`, for
# `shouldstop` and for an interrupt, padded to the terminal's width with at
# least one `!` each side: at 40 columns, the narrowest pytest honours,
# `! Interrupted: 1 error during collection !` (round 1, finding 4).
STOPPED_EARLY_RE = re.compile(r"^!+ .+ !+$", re.M)
```
```python
    (
        "ERROR tests/b.py\n"
        "! Interrupted: 1 error during collection !\n"
        "1 error in 0.06s\n",
        ["tests/b.py", "tests/f.py"],
        ["failing on base too", "STOPPED_EARLY"],
    ),
```
```text
One shape the gate cannot see through: a part that prints pytest's summary without running the files appended to it — a `sh -c '…'`, a `make` target, a wrapper that drops its arguments — reads `new` for a file it never ran, because pytest under `-q` names no file that passed. Where the runner is such a part, write it so it passes its arguments on, or read its `new` as the row's claim rather than a measurement.
```
```text
    The one thing a summary does not prove is that the appended files ran:
    a part that drops its arguments -- a `sh -c '…'`, a `make` target --
    prints a summary over something else, and every file reads `new`.
    pytest under `-q` names no passing file, so nothing here can tell;
    `templates/config.md` rule 3 names it for the row's author.
```
```python
    with open(os.path.join(ROOT, "templates", "config.md"), encoding="utf-8") as handle:
        assert "a wrapper that drops its arguments" in handle.read()
```

## Executed probes

| What was run | Result |
|---|---|
| Probe A: gate on a fixture with row `cd sub && <pytest row>`, base and branch failing `sub/tests/test_two.py` | `tests/test_two.py  new`; no `suite-at-base-*.txt` kept |
| Probe B: row `<python sleep 12> >/dev/null 2>&1 & <pytest row>`, base failing `tests/test_two.py` | gate took 13.7 s; `suite-at-base-1.txt` is the sleeper run in the foreground; prefix 2 gave `failing on base too` |
| Probe C: row `sh -c '<pytest> tests/test_one.py' && <pytest row>`, base failing `tests/test_two.py` | `tests/test_two.py  new`; prefix 1 printed `1 passed in 0.00s` |
| Probe D: row `CARGO_TARGET_DIR=… cargo test --offline && <pytest row>`, base failing `tests/test_two.py` | `tests/test_two.py  new`; prefix 1 printed cargo's `test result: ok. 0 passed; … finished in 0.00s` |
| pytest 9.1.1, `COLUMNS` 30/34/40/44, `-x` with and without `-n 2`, and a collection error | widths below 40 render at 80; at 40 the collection interrupt is `! … !`, at 44 `!! … !!`; under xdist `-x` the plain `stopping after` rule still has 6 or more `!` |
| `verdicts_at_base` on `ERROR tests/b.py` + `! Interrupted: 1 error during collection !` + `1 error in 0.06s` | `{'tests/b.py': 'failing on base too', 'tests/f.py': 'new'}` |
| The proposed whole-line summary regex against the five measured pytest endings, cargo's line, `no tests ran`, `Found 2 errors.` | accepts all five pytest lines; rejects the other three; `suite_counts` accepts cargo's |
| #748 case with `os.killpg` replaced by `proc.kill()` in `_run_bounded` | `1 failed`: `the row's loop outlived the bound`; reverted |
| #748 case, unmutated, three runs | `1 passed` ×3, 2.05–2.29 s |
| `evidence-check` over the scratch clone with this report staged, and again without it | 149 names read with it, 102 without; 0 refused either way |
| `tests/test_no_real_identifiers.py` in the scratch clone with this report staged | `5 passed` |
| `round-record new` dry run on this report in the scratch clone | exit 0; `Needs a fix` and `Loses a record or crashes` rows written; the approval-line notice of ⬜ 8 |
| The broad gate: the full suite, the repository-wide lint and the typecheck at `9570fa1b` | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A file the branch reports only as `ERROR` gets no base comparison | already deferred by the frame (`spec.md` Out, `overview.md` *Not done*) | the repository owner, as the frame names |
| `run` has no bound at the base, so a runner that hangs at the base hangs the gate whatever the cut | not filed; outside this work item, which concerns the cut and how the run is read | the repository owner — whether to file it |
