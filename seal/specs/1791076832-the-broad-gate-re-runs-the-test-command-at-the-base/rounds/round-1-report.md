# Round 1 report — 1791076832-the-broad-gate-re-runs-the-test-command-at-the-base

Target `9570fa1b` on `fix/747-the-broad-gate-re-runs-the-test-command-at-the-base`,
against `release/v0.18.1` at `e141980a`. Reviewed by warden. First round: no
earlier `round-N.md` exists, so nothing was carried and every verdict below is
this round's own.

## What the account claimed, and what was checked

The frame (`spec.md` Scope 1–8), `overview.md` and the ledger rows B1–B4 claim
four things. Each was opened against the code.

| Claim | Where it is made | What the code does | How it was checked |
|---|---|---|---|
| The cut is made at top-level operators of the shell's grammar; quotes, `$(…)`, backticks, `( … )` and `2>&1` are not cut | `spec.md` Scope 4 | Holds. `row_prefixes` (`skills/verify/scripts/broad_gate.py:1894`) keeps a stack of open quotes and groups and cuts only with the stack empty. `>&`/`<&` are excluded at line 1961 | read; the orchestrator executed the parametrised cases |
| `failing on base too` only on a `FAILED`/`ERROR` line naming the file (Q1) | `spec.md` Scope 3 | Holds. `verdicts_at_base` unions `FAILED_RE` and `ERROR_RE` | read |
| Rule 3 states both orders and recommends neither (Q2) | `questions.md` Q2 | Holds, at `templates/config.md:333`. The case at `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:429` pins it | read |
| #748's case polls the marker and is still red without the group kill | `spec.md` Scope 7–8, ledger B1 | Holds | **executed**. With the group kill in `_run_bounded` replaced by `proc.kill()` in a scratch clone, the case failed with `the row's loop outlived the bound`. Reverted, it passed three times out of three |
| **"No outcome gives a word a run did not measure"** | `spec.md` Scope 4, with `compare_at_base`'s docstring ("measured — never inferred") and rule 3 | **Does not hold.** Four row shapes that the gate accepts get `new` for a file the base fails. Findings 1, 2 and 5 below. Finding 4 is a fourth way to the same result, decided by terminal width | **executed** — probes A, C, D, and a pytest measurement |

The orchestrator's prompt reports that 4 modules and ruff passed at the target
(715 passed, 79 skipped). This round did not re-run that. It ran only the
#748 case and the probes listed below.

## Findings

The frame enumerates the class by how a row is **cut**. It does not enumerate
how the run that a cut selects is **read**, and this round found the
counterfeits in that second step. Findings 1, 2, 4 and 5 are all one claim
failing: that a `new` came from a run which ran the file. Finding 3 is a
second effect of the cut: a prefix can run a part in a way the row never runs
it.

### 🟡 1 — a `cargo test` line is read as pytest's summary, and the file reads `new`

`skills/verify/scripts/broad_gate.py:2032`. `compare_at_base` decides which
prefix "ran pytest" by calling `suite_counts(tried.text) is not None`.
`suite_counts` was written for the panel. It accepts **any** line where a
count word is followed by `in <n>s` later on the line. The line `cargo test`
prints is `test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured;
1 filtered out; finished in 0.00s`, and `suite_counts` accepts it.

Probe D used the row `CARGO_TARGET_DIR=… cargo test --offline && <pytest row>`
on a fixture where the base fails `tests/test_two.py`. Prefix 1 became
`cargo test --offline tests/test_two.py`. Cargo took the path as a test-name
filter, ran zero tests, and printed that line. The gate stopped at prefix 1
and printed `tests/test_two.py  new`, although the base fails that file and
pytest never ran at the base. The frame's outcome table puts "the runner is
not pytest" under **not measured**, and here it reads `new`. A
`cargo test && pytest` row is the ordinary shape for a Rust-extension Python
project.

Fix: decide "pytest ran" from a line that is **entirely** pytest's summary:
the counts and the clock, optionally between `=` rules, and nothing else. All
five of the phase-3 measured endings pass that test, and cargo's line fails
it. Both were checked with a scratch script against the regex below.

### 🟡 2 — a `cd sub && …` row reads `new` with no run at all

`skills/verify/scripts/broad_gate.py:2021`. The absent check asks
`git cat-file -e HEAD:<file>` of the scratch worktree's **root**. pytest names
a failing file relative to the directory it ran in, and a leading `cd` changes
that directory. The frame names the `cd` part as something the prefixes
preserve ("a `cd`, an `export` … the runner runs in the context the row gave
it", `spec.md` Scope 1; `compare_at_base` docstring line 1990).

Probe A used the row `cd sub && <pytest row>`, with `sub/tests/test_two.py`
failing at both base and branch. The branch printed
`FAILED tests/test_two.py::…`. `HEAD:tests/test_two.py` does not exist at the
root, so the file went into `absent` and read `new` **without any run**: no
`suite-at-base-*.txt` was kept. This was already true before this branch, but
this branch is where the frame claims `cd` works and the docs promise
"measured".

Fix: absence at the base proves that the test arrived with this branch only
when the branch's own tree carries the same path at the root. When it does
not, the path is not relative to the root, and the honest answer is `new?`
with a reason.

### 🟡 3 — under `/bin/sh` a prefix ending at `&` runs a background part in the foreground, with no bound

`skills/verify/scripts/broad_gate.py:1964`, with `POSIX_CUTS` at line 1890.
`row_prefixes` cuts at a lone `&`, so `server & pytest -q` yields the prefix
`server`, and the gate runs `server <files>` in the foreground. The row never
runs that part in the foreground. `run` (line 1421) has no timeout. So a
backgrounded part that does not end makes the sealer's run hang at the base,
even though the branch run ended. A `make serve`, an `npm start` or a
`tail -f` behaves this way, and each of those takes appended arguments without
erroring. `templates/config.md` lists a non-trailing `&` under *Stays legal*,
and the frame's outcome table lists `&` as measured.

Probe B used the row `python -c "import time; time.sleep(12)" >/dev/null 2>&1 & <pytest row>`.
The branch run ended at once. At the base, `suite-at-base-1.txt` holds the
sleeper run in the foreground, and the gate took 13.7 s in total. Prefix 2
then measured correctly, so the cost here was time. A part that never ends
turns the cost into a hang. The old code cut only at `&&`, so this is a
regression for `&` rows. The case at
`tests/test_the_seal_is_taken_once_by_the_sealer.py:3852` pins this behaviour
as correct.

The same class, enumerated: a prefix that ends before `|` runs the producer
without its consumer. That is the point when the runner comes first
(`runner | tee x`), and it is harmless unless the producer never ends on its
own (`yes | …`). The fix below leaves `|` as it is and names it in the
docstring. Under `cmd.exe`, `&` runs the two commands in order, so it stays a
cut there.

### 🟡 4 — the early-stop rule needs `!!!`, and pytest writes a single `!` at a width of 40

`skills/verify/scripts/broad_gate.py:1850`, `STOPPED_EARLY_RE =
^!{3,} .+ !{3,}$`. pytest pads the rule to the terminal width with **at least
one** `!` on each side. Measured with pytest 9.1.1 from the `bin/test` venv:

- `COLUMNS=40` prints `! Interrupted: 1 error during collection !`.
- `COLUMNS=44` prints `!! Interrupted: … !!`.
- Below 40, pytest ignores `COLUMNS` and uses 80.

Fed to `verdicts_at_base` together with `ERROR tests/b.py` and the summary,
the 40-column ending reads `tests/f.py: new`. That is A6 exactly: a run
interrupted by one file's collection error, and an unnamed file counted as
passing. The `{3,}` comes from the 80-column measurement and not from
anything pytest promises. A sealer whose environment exports a narrow
`COLUMNS` gets the counterfeit.

Fix: `!+` on both sides. That rule matches both the narrow and the wide
renderings. A false match can only turn a `new` into a `new?`, never the
reverse.

### 🟡 5 — a part that prints pytest's summary without running the appended files gives `new`, and the docs say it cannot

`templates/config.md:333` (rule 3) and `skills/verify/scripts/broad_gate.py:1974`
(`compare_at_base`, "measured — never inferred"). The appended files reach
pytest only if the part passes its arguments on. A `sh -c '…'`, a `make`
target, or any wrapper that drops its arguments still prints a pytest summary.

Probe C used the row `sh -c '<pytest> tests/test_one.py' && <pytest row>`,
with the base failing `tests/test_two.py`. Prefix 1 ran only `test_one`,
printed `1 passed in 0.00s`, and the gate printed `tests/test_two.py  new`.
This was already true of the old first-`&&` cut. The new documents now
promise the opposite, and every reader of the word (`agents/sealer.md`,
`agents/smith.md`, `skills/verify/SKILL.md`) is told that `new` means
"measured at the base".

This round found no mechanical guard that keeps the cost the frame chose.
pytest under `-q` does not name files that passed, so the gate cannot see
whether the files ran. The fix is to name the limit where the rule and the
reading are stated, the way `( … )` groups are already named.

### ⬜ 6 — rule 3's operator list for `cmd.exe` reads backwards, and "never reached" is not what happens

`templates/config.md:333`: "`&&`, `\|\|`, `;`, `\|` and `&` under `/bin/sh`,
the same but `;` under `cmd.exe`". This reads as "the same, plus `;`", which
is the opposite of the code (`CMD_CUTS` has no `;`). Separately, "with its
output sent to a file is never reached": such a runner **is** reached and
run. Its summary is simply not in the output that is read. The paste-ready
fix for finding 3 rewrites this sentence, so both are corrected there.

### ⬜ 7 — `row_prefixes`' "Not modelled" list omits compound commands and `>|`

`skills/verify/scripts/broad_gate.py:1919`. `if …; then …; fi`,
`for/while … done` and `case … esac` are cut inside at their `;`, and `>|`
(noclobber override) is cut at its `|`. That leaves the prefix
`cmd > <files>`, which redirects into the first test file in the scratch
worktree. Each of these costs a measurement and fakes none, because the
prefixes are invalid or print no summary. The docstring promises "named
rather than claimed", and these shapes are not named. The fix for finding 3
adds them.

### ⬜ 8 — correction: `chain_check` does not read `plan.md`'s approval line

`seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/plan.md:7`.
After "when `smith` was spawned." the same line goes on with "Q1 and Q2
take the frame's defaults …". `chain_check` matches the approval as a whole line that ends at
"spawned.". A dry run of `round-record new` in the scratch clone printed
"plan.md's approval line is absent". That is reported and not refused. The
fix is to move the Q1/Q2 sentence onto its own line. This is the run's
paperwork, so it is a correction and stays out of `Needs a fix`.

## Regression tests to plant

All go to `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside the
#747 block. They are written out under *Paste-ready fixes*. Each must be seen
red against `9570fa1b` before it is committed, per the contract's §15:

- **finding 1**: a lint-first row whose first part is a stand-in printing
  cargo's measured line and exiting 0. It must read `failing on base too`.
  At `9570fa1b` it reads `new`, which probe D shows with real cargo.
- **finding 2**: a `cd sub && …` row. It must read the new `new?` reason. At
  `9570fa1b` it reads `new`, per probe A.
- **finding 3**: the `("a & b", …)` parameter becomes `["a & b"]`. It is red
  against the current `row_prefixes`.
- **finding 4**: a `MEASURED_ENDINGS` entry with the 40-column rule. At
  `9570fa1b` it reads `new` for the unnamed file, which was executed.
- **finding 5**: an extension of the A9 pin to the new rule-3 sentence.

## Facts for the evidence ledger

- pytest 9.1.1 honours `COLUMNS` from 40 upward and pads a `!` rule with at
  least one `!` per side. At 40 columns, "Interrupted: 1 error during
  collection" carries one `!` each side. Measured this round. It belongs
  beside B3's measured endings.
- `cargo test` (a stable toolchain, this machine) prints
  `test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out; finished in 0.00s`
  when given a test-file path as an argument. `suite_counts` reads that line
  as a summary. Measured this round.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The base re-run takes `cargo test`'s result line for pytest's summary, so a lint-first `cargo test && pytest` row reads `new` for a file the base fails | `skills/verify/scripts/broad_gate.py:2032` | open | executed, probe D: `tests/test_two.py  new` with the base failing it; prefix 1 printed only cargo's line |
| 🟡 2 | A `cd sub && …` row's failing file is asked about at the repository root, found absent, and reads `new` with no run at the base | `skills/verify/scripts/broad_gate.py:2021` | open | executed, probe A: `new`, no `suite-at-base-*.txt` kept, base fails the file |
| 🟡 3 | Under `/bin/sh` a prefix ending at a lone `&` runs the backgrounded part in the foreground with no bound, so a part that never ends hangs the gate at the base | `skills/verify/scripts/broad_gate.py:1964` | open | executed, probe B: 12 s sleeper ran in the foreground as prefix 1, gate 13.7 s; the old `&&`-only cut never did this |
| 🟡 4 | `STOPPED_EARLY_RE` needs three `!`, and pytest at 40–45 columns writes one or two, so an interrupted base run reads `new` for an unnamed file | `skills/verify/scripts/broad_gate.py:1850` | open | executed: pytest 9.1.1 at `COLUMNS=40` printed `! Interrupted: 1 error during collection !`; `verdicts_at_base` on that ending gave `new` |
| 🟡 5 | A part that prints pytest's summary but drops the appended files gives `new`, while rule 3 and `compare_at_base` say a word is only given from a run that measured it | `templates/config.md:333` | open | executed, probe C: `sh -c '…test_one.py'` first part, `tests/test_two.py  new` with the base failing it |
| ⬜ 6 | Rule 3 says "the same but `;` under `cmd.exe`" for a list that lacks `;`, and calls a runner whose output goes to a file "never reached" | `templates/config.md:333` | open | read; the finding-3 fix rewrites the sentence |
| ⬜ 7 | `row_prefixes`' "Not modelled" list omits compound commands and `>\|` | `skills/verify/scripts/broad_gate.py:1919` | open | read; each costs a measurement and fakes none |
| ⬜ 8 | `plan.md`'s approval line carries a second sentence after "spawned.", so `chain_check` reports it absent | `seal/specs/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base/plan.md:7` | open | executed: a dry run of `round-record new` in the scratch clone printed the notice; a correction, not counted in `Needs a fix` |
| 🟢 | #748's case polls and is red without the group kill | `tests/test_the_commit_gate_decides_at_the_commit.py:434` | confirmed | executed: red with `the row's loop outlived the bound` under `proc.kill()`, reverted, green 3 of 3 |
| 🟢 | Q1 (a base `ERROR` line reads `failing on base too`) and Q2 (rule 3 states both orders) are built as answered | `skills/verify/scripts/broad_gate.py:1841` | confirmed | read: `ERROR_RE` joins `FAILED_RE` in `verdicts_at_base`; rule 3's last sentences state both costs and pick neither |
| 🟢 | The cut does not split quotes, `$(…)`, backticks, `( … )` or `2>&1` in either grammar, and the base re-run stays in `compare_at_base`'s own body | `skills/verify/scripts/broad_gate.py:1894` | confirmed | read; the orchestrator executed the parametrised cases and the shell-site case |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A file the branch reports only as `ERROR` gets no base comparison | already deferred by the frame (`spec.md` Out, `overview.md` *Not done*) | the repository owner, as the frame names |
| `run` has no bound at the base, so a runner that hangs at the base hangs the gate whatever the cut | not filed; outside this work item, which concerns the cut and how the run is read | the repository owner — whether to file it |

## Paste-ready fixes

### 🟡 1 — read pytest's summary as a whole line

In `skills/verify/scripts/broad_gate.py`, beside `STOPPED_EARLY_RE`:

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

In `compare_at_base`:

```python
                if PYTEST_SUMMARY_RE.search(tried.text):
                    measured = tried.text
                    break
```

Case, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`:

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

### 🟡 2 — absence proves nothing where the path is not the root's

In `skills/verify/scripts/broad_gate.py`, beside `STOPPED_EARLY`:

```python
UNPLACED = (
    f"{NOT_MEASURED}: neither the base nor this branch carries this path at "
    "the repository root, so the row ran its tests somewhere else and the "
    "base was not asked"
)
```

In `compare_at_base`, replacing the `absent` / `present` / `verdicts` lines:

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

Case:

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

Add `gate.UNPLACED` to the whole-text pins in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it`.

### 🟡 3 — a lone `&` under `/bin/sh` ends a part and no prefix

In `row_prefixes`, replacing the cut block:

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

The docstring's operator sentence and its "Not modelled" paragraph (also
closes ⬜ 7):

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

In `tests/test_the_seal_is_taken_once_by_the_sealer.py:3852`:

```python
        ("a & b", ["a & b"]),
        ("a & b && c", ["a & b", "a & b && c"]),
```

Rule 3's operator sentence in `templates/config.md:333` (also closes ⬜ 6):

```text
It cuts the row at its top-level operators — `&&`, `\|\|`, `;` and `\|` under `/bin/sh`, where a lone `&` is never a cut because the part before it runs in the background, and `&&`, `\|\|`, `&` and `\|` under `cmd.exe`, where `;` separates nothing — and runs each prefix with the files appended until one prints pytest's summary.
```

and its last sentence:

```text
A runner inside a `( … )` group or behind a part that fails at the base is never reached, and one whose output goes to a file is run but not read: each reads `new?`.
```

### 🟡 4 — one `!` is pytest's narrowest rule

```python
# … `_pytest/terminal.py` writes a `!` separator for `shouldfail`, for
# `shouldstop` and for an interrupt, padded to the terminal's width with at
# least one `!` each side: at 40 columns, the narrowest pytest honours,
# `! Interrupted: 1 error during collection !` (round 1, finding 4).
STOPPED_EARLY_RE = re.compile(r"^!+ .+ !+$", re.M)
```

A `MEASURED_ENDINGS` entry, before the `None` row at line 4028:

```python
    (
        "ERROR tests/b.py\n"
        "! Interrupted: 1 error during collection !\n"
        "1 error in 0.06s\n",
        ["tests/b.py", "tests/f.py"],
        ["failing on base too", "STOPPED_EARLY"],
    ),
```

### 🟡 5 — name the wrapper that drops its arguments

Appended to rule 3 in `templates/config.md:333`:

```text
One shape the gate cannot see through: a part that prints pytest's summary without running the files appended to it — a `sh -c '…'`, a `make` target, a wrapper that drops its arguments — reads `new` for a file it never ran, because pytest under `-q` names no file that passed. Where the runner is such a part, write it so it passes its arguments on, or read its `new` as the row's claim rather than a measurement.
```

Appended to `compare_at_base`'s docstring paragraph on finding the part:

```text
    The one thing a summary does not prove is that the appended files ran:
    a part that drops its arguments -- a `sh -c '…'`, a `make` target --
    prints a summary over something else, and every file reads `new`.
    pytest under `-q` names no passing file, so nothing here can tell;
    `templates/config.md` rule 3 names it for the row's author.
```

Extend the A9 pin:

```python
    with open(os.path.join(ROOT, "templates", "config.md"), encoding="utf-8") as handle:
        assert "a wrapper that drops its arguments" in handle.read()
```

Needs a fix: yes — 🟡 1 (cargo's line read as pytest's summary), 🟡 2 (a `cd` row's file reads `new` unasked), 🟡 3 (a lone `&` runs a background part in the foreground at the base), 🟡 4 (the `!{3,}` rule misses pytest at 40–45 columns), 🟡 5 (a summary-printing wrapper's `new` is documented as measured)
Loses a record or crashes: no

## Proof block

- **Opened**: `skills/verify/scripts/broad_gate.py` (diff, plus `run`, `git`, `failing_files`, `suite_counts`, `failure_lines`, `compare_at_base`, `row_prefixes`, `verdicts_at_base`, `cmd_exe_reads`); `tests/test_the_seal_is_taken_once_by_the_sealer.py` (diff, helpers 700–900); `tests/test_the_commit_gate_decides_at_the_commit.py` (diff, `_run_bounded`, the #748 case); `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` (diff); `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` (diff); `templates/config.md` §*What is refused, and what stays allowed* and §*Choosing a value*; `agents/sealer.md`, `agents/smith.md`, `skills/verify/SKILL.md`, `README.md`, `README.ko.md` (diffs); `bin/test`; this work item's `spec.md`, `questions.md`, `overview.md`, `phases/phase-3.md` (head); `seal/ledger/1791076832-the-broad-gate-re-runs-the-test-command-at-the-base.md` (head).
- **Executed**: probes A–D, once each in a scratch clone at `9570fa1b`, then deleted; the pytest width measurements; the regex check; the #748 mutation (once, reverted) and the unmutated case ×3.
- **Not run**: the four changed modules whole, ruff, the full suite. The orchestrator reports the first two. The full suite, the repository-wide lint and the typecheck are `unverified`, and the sealer answers for them after the rounds settle.
