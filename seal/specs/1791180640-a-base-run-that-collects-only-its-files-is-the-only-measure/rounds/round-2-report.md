# Round 2 report — 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure

| Field | Value |
|---|---|
| Target SHA | c8d6c785 |
| Base | `release/v0.18.3` at a3aa139a |
| Fix range checked | `165a6ca8..36e5fb46` (code in fd98c2c8 and 75855657) |
| Pull request | #814 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Round 1's two blocking findings are closed for every layout round 1 built.
Layouts A, A2 and B read `new?` with `COMPANY`, and layout C reads
`MULTI_RUNNER`. The decisive property still does not hold, though. The fix
for round 1's first finding compares counts, and a count can be made up by
another file. Two shapes still give `failing on base too` where a3aa139a
gave `new`. Both were executed end to end against pytest 9.1.1, and both are
regressions against the base:

1. **Another file's failures beside the others make up the count** (🔴 1).
   A file fails only alone, and the base passes it in the row. A second
   file of the same group fails more tests beside the others than alone.
   The group's count then equals the files' counts one by one, so the first
   file keeps the word it earned alone. One sibling that sets state at
   import produces both effects, and so does a flaky test that fails in the
   group's run and passes in its run alone. Rule 3 calls this "two
   dependencies whose counts cancel". That undersells it: one dependency is
   enough, a flaky test is none, and "cancel" is really "match or exceed".
   It also reproduces under this repository's own row (`bin/test -q`,
   xdist on). There, all three files of the group read `failing on base
   too`, and the base's own group run passes the regressed one.
2. **The measuring runner's output never reaches the gate** (🟡 2). One
   runner measured, and its output went to a file. A later runner listed
   only the failing file. The proof's one visible session is the later
   runner's, so it proves nothing about the run that measured. Rule 3's
   "prints nothing it can read" covers the class, but its "Both are as they
   were before the proof run existed" is false for this shape. a3aa139a
   read `new` here.

A reading finding goes with them. The `COMPANY` reason claims the group
"failed fewer tests than they fail one by one" in the route where a file has
no count alone (🟡 3). That is not what happened there.

Everything else I attacked holds. That covers the proof reader and the
outcome line (`RAN_RE`), the S3–S5 shape (four of the 18 words rebuilt, and
the base fails the file each time), a 15-layout sample of the corpus (30
runs, no leak), xdist, the seal, and this repository's row in its normal
and sibling-on-the-path shapes.

## What this round was asked

This is the verifying round over round 1's fixes, `165a6ca8..36e5fb46`. It
is the item's last round. Every path to `failing on base too` at the target
had to be enumerated and attacked: the proof pass, the new `COMPANY` count
comparison and `RAN_RE`. Round 1's layouts A, A2, B and C were to run at
the target, at a3aa139a and at cdb57895. The phase-2 corpus was to be
sampled, with at least two S3–S5 words rebuilt. Rule 3, the `SKILL.md`
bullet, the reasons, the changelog and `overview.md` were to be checked
against the code, and the seal against this repository's row.

## Enumeration: every path to `failing on base too` at c8d6c785

Read at c8d6c785. `ON_BASE` is assigned at one site,
`skills/verify/scripts/broad_gate.py:2323`, and only from a proof pass. A
proof pass is queued at `:2346` only for a file whose run alone failed. The
word can later be taken away at one site, `:2359-2365`, and only for files
of the group of several. So each route to a run alone is checked
differently:

| Route to a run alone | Code | Proof | Company check | At a3aa139a |
|---|---|---|---|---|
| a candidate (the root's tree lacks the path) | `:2255-2258`, `:2271` | yes | **none** | run alone too |
| the one failing file the root carries | `:2272-2273` | yes | **none** | run alone too (a group of one) |
| a file of the group of several | `:2340-2341` | yes | the sum test at `:2362` | judged by the group's run |

The proof (`proof_refused`, `:2033-2050`) asks that exactly one trailer be
present and no outcome line, with the listing and the error lines naming
only the file. Executed attacks on each piece are below.

## Findings — from execution

### 🔴 1 — another file's failures beside the others make up the group's count

`skills/verify/scripts/broad_gate.py:2362`
(`if None in counts or failing < sum(x for _, x in counts)`).
**Regression against a3aa139a: yes.**

The check asks whether the group as a whole failed fewer tests than its
files fail one by one. It cannot ask whether each file that earned the word
alone also fails in the group, because no count is per file. Any file that
fails *more* beside the others than alone pays for a file that fails only
alone.

Executed through `compare_at_base` of three gates, with pytest 9.1.1 and the
files-only row `python -m pytest -q -p no:cacheprovider`. The files came
from the branch's own `FAILED` lines:

| Layout | File | a3aa139a | cdb57895 | c8d6c785 |
|---|---|---|---|---|
| cancel: test_a sets `MODE` at import and fails a pre-existing test; test_b needs `MODE` (the branch regresses it); test_c asserts `MODE` is unset | test_b | `new` | **failing on base too** | **failing on base too** |
| cancel2: the same, and test_c also holds a pre-existing failure | test_a / test_b / test_c | on / `new` / on | on / **on** / on | on / **on** / on |
| outweigh: test_c fails two tests beside test_a, more than test_b's one alone | test_b | `new` | **failing on base too** | **failing on base too** |
| flaky2: layout A's test_a and test_b, and a test_c holding a pre-existing failure and a test that fails on its first two runs (the branch's and the group's) and passes after | test_b | `new` | not run | **failing on base too** |
| cancel under `-n 2` | test_b | `new` | **failing on base too** | **failing on base too** |
| cancel2 under this repository's own row (`uvx ruff check . && uvx ruff format --check . && bin/test -q`, xdist `-n auto`), in a clone at c8d6c785 | all three | not run | not run | **failing on base too** ×3 |

In the last row the base's own group run is kept as `suite-at-base-3.txt`
(`3 failed, 1 passed`). Its report holds test_b's one test with no
`failure` child. So the base passes test_b in the row, and the gate says
the base fails it. In cancel2 and flaky2, every failing file reads `failing
on base too`. The red suite then carries no `new` at all, and the
regression reads as inherited.

**Ordinary or contrived.** Rule 3 says *"Two dependencies in one group
whose counts cancel, one file failing only beside the others and another
only alone"*. The changelog says *"a group whose files depend on each other
both ways"*. Neither describes what was executed:

- **one dependency is enough.** One sibling's import-time state that one
  file needs and another trips over is the same test pollution round 1
  called ordinary. It only needs a third file in the failing group;
- **a flaky test is no dependency at all.** It fails in the group's run and
  passes alone. A release branch with a known flaky test and one new
  company-dependent regression is this shape. pytest-randomly's reordering
  is another source of the same count noise (read, not run);
- **the counts need not cancel.** The check is `<`, so a group that fails
  *more* than its files do one by one also keeps its words. The outweigh
  row shows it.

**Why no count closes it.** I checked two count-only variants by hand.
`!=` instead of `<` leaves the exact match (cancel, cancel2, flaky2)
standing. A leave-one-out run (the group without each file, which
`overview.md` names as the finer alternative) also fails. In a two-file
group where test_b fails only alone and test_a fails one more test only
beside test_b, the group without test_b is test_a alone. Its count plus
test_b's alone equals the group's count, so the word stands. A flaky test
defeats any rerun. What would close it is a per-file answer from the
group's own run, and the report's names are the only per-file thing that
run produces. #812 removed names because they *granted* the word wrongly.
Reading them only to *take the word away* is a different trade, and it is
the owner's call, not this round's.

The paste-ready fix below is the one that stops the release from telling a
person something wrong: rule 3, the docstring and the code comment name the
shape as it is. Whether that is acceptable against S17 ("no `failing on base
too` where a3aa139a did not give it, except S3–S5") is the orchestrator's
call. The case under *Regression tests to plant* is red at c8d6c785, and it
is planted with whichever choice is made.

### 🟡 2 — a measuring runner whose output never reaches the gate

`skills/verify/scripts/broad_gate.py:2034-2036` (the proof counts the
sessions it can see) and `templates/config.md:333` (*"Both are as they were
before the proof run existed."*). **Regression against a3aa139a: yes.**

Executed with row `python -m pytest -q -p no:cacheprovider tests/unit >
unit.log; python -m pytest -q -p no:cacheprovider tests/integration`. At
the base, `tests/unit/test_u.py` holds a pre-existing failure, and the
branch regresses `tests/integration/test_i.py`:

| Gate | Word for `tests/integration/test_i.py` |
|---|---|
| a3aa139a | `new` (no summary at prefix 1, so it measured at the whole row, where the second runner passes the file) |
| cdb57895 | **failing on base too** |
| c8d6c785 | **failing on base too** |

Prefix 1 writes the report. It collected `tests/unit` and the handed file,
and its one failure is `tests.unit.test_u`'s. That run's output went to
`unit.log`. The proof's output (`collected-at-base-1.txt`) holds one session,
the second runner's, and that session lists `tests/integration/test_i.py: 1`
alone. So the proof proves the other runner.

Rule 3's heading *"A second runner … that prints nothing it can read"*
covers the silent runner if "second" may mean the measuring one. Its
examples do not include output sent to a file. Its closing claim, that the
word is as it was before the proof run existed, is false: a3aa139a settled
on printed output and read `new`. This is the half of round 1's settling
divergence that the outcome-line check does not reach. That is why it is
🟡 rather than 🔴: the class is named and the shape is rarer, since it needs
a second runner whose collection is exactly the failing file. But it is
the same S17 exception.

A code alternative, not built here: give the measuring runner, after the
inserted file, `-o verbosity_test_cases=-1`. The command line then outranks
the variable for that runner alone, so it lists `path::test` node ids that
no other runner prints, and the proof can require them. I read this from
pytest's option order and did not execute it.

## Findings — from reading

### 🟡 3 — the `COMPANY` reason states a count comparison that the no-count route never made

`skills/verify/scripts/broad_gate.py:1938-1943` and `:2362`. The reason
says *"the run of the failing files together at the base failed fewer tests
than they fail one by one"*. It is also given where `None in counts`, that
is, where a file of the group wrote no report alone. The planted
`a-file-with-no-count-alone` parameter is that route: test_a reads
`COMPANY` while the group failed one test and test_a alone fails one. No
"fewer" happened there. The narrow run executes that parameter, and it
passes with this text. The word is right and the sentence a person acts on
is not. The person goes looking for a smaller count that is not in the
kept files. `skills/verify/SKILL.md:510` repeats the same claim. Not a
regression: the reason is new at fd98c2c8.

### ⬜ 4 — rule 3 does not name the two routes that never meet a group

`templates/config.md:333`. A file run alone from the start is never checked
against company. That is the one failing file the root carries, or every
failing file of a `cd sub` row, where the root's tree lacks the paths. A
sibling the branch passes is never run at the base either. Executed: layout
A under `cd sub && pytest -q` with `sub/pytest.ini` (test_b), and layout A
with test_a passing (a group of one). Every gate, a3aa139a included, reads
`failing on base too`. **Not a regression**, so ⬜. Rule 3 now says the
row's context must agree, and it presents its limits as a complete list,
so these two belong beside them.

### ⬜ 5 — the run's paperwork says only S3–S5 is left

`seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md`
(*Not done*: "After round 1's fix pass only one is left: the S3–S5 shape",
and "A leave-one-out run … would see it"). The same work item's
`changelog.md` says *"a group whose files depend on each other both ways"*,
and PR #814's body is right only as scoped to the corpus. 🔴 1 and 🟡 2
falsify the first two sentences, and 🔴 1's two-file case falsifies the
leave-one-out claim. This is a correction under `seal/specs/`, so it is
outside `Needs a fix`. The fenced text is below.

## Round 1's verdicts, re-checked

- **Round 1's first blocking finding (company):** closed for layouts A, A2
  and B, and for the no-count shape. Executed: all three read `COMPANY` at
  c8d6c785, and `new` / on / `new` at a3aa139a as round 1 recorded. Also
  closed under `-n 2` (xdist-A: `COMPANY` for both). The class is not
  closed, and the remainder is 🔴 1 above.
- **Round 1's second blocking finding (a first runner without the
  environment):** closed. Layout C reads `MULTI_RUNNER` at c8d6c785 and
  `failing on base too` at cdb57895 (executed). Attacks on `RAN_RE` are
  under *What was checked and holds*.
- **Round 1's ⬜ 3:** closed. Rule 3 carries the per-version example (read,
  `templates/config.md:333`), and the test pins it.
- **Round 1's ⬜ 4:** closed as answered. PR #814's body now scopes its
  claim to the corpus and round 1's four layouts (read via `gh pr view`).
  ⬜ 5 above is the part this round's findings make false.
- **Round 1's ❓ (the strict variant):** carried out. The warnings-only
  group and the interrupted group now read `COMPANY`. The cases assert it,
  and the narrow run passes them.

## What was checked and holds

- **The proof reader and `RAN_RE` (executed on real and constructed
  output).** A `-q` outcome line, a ruled one, and pytest-sugar's own
  (which keeps pytest's line) all read `MULTI_RUNNER`. These do not count
  as a session, so a lint or install line before the runner costs nothing:
  `12 files checked in 0.3s`, uv's `Installed 3 packages in 12ms`, tox's
  `py: OK (…)`, `no tests ran in 0.01s`. A runner that ran nothing cannot
  have failed the file anyway. A pseudo-terminal's `\r\n` endings (captured
  from a real pty with `script`) would hide the line from the regex.
  `run()` reads in text mode, and Python's subprocess converts `\r\n` and
  `\r` to `\n` there, so the gate never sees them (read: the subprocess
  documentation's universal-newlines rule). Colour around the line is
  stripped by `COLOUR_RE` first (executed on the pty capture). A collect-only
  trailer never matches `RAN_RE`. A runner *with* the environment cannot
  print an outcome line under `--collect-only`, so `RAN_RE` can only make a
  word stricter. What stays out of reach is in rule 3: `-qq` or quieter
  without the environment, and 🟡 2.
- **Round 1's layouts at three gates (executed):** A, A2, B, C and the
  normal control, as in the table under *Executed probes*. The normal
  shape keeps `failing on base too` / `new`.
- **The S3–S5 shape (executed, four of the 18 words):** the first frame's
  Axis A construction, where the outer test runs pytest on an inner
  `tests/test_g.py` that fails and the base fails the outer test, under the
  files-only row with `-q -rN` (inner run on stderr), `-q -rN` (on stdout),
  `-q -n 2 -rN` (on stderr), and a stderr inner run under `-q -s`. Each:
  a3aa139a `new`, c8d6c785 `failing on base too` for `tests/test_err.py`.
  By hand at the base, `pytest -q tests/test_err.py` exits 1 with `1
  failed`, and `tests/test_g.py` exits 0. The base truly fails the file.
- **The corpus (executed, sampled):** 15 layouts of the planted case's
  `REGRESSED` list, each under its own row and the files-only row: P1,
  P3-sh, P7-mixed, Q1, Q4, Q5, Qf-env, Qs2, R1-row, R2b, R3, N1, N1-xdist,
  N1c and N7. That is 30 runs and 32 file words at a3aa139a and c8d6c785.
  No `failing on base too` appears at the target where a3aa139a gave
  another word, and every target word equals the planted table's. The fix
  range does not touch the planted table, and the narrow run passes all 55
  parameters at the target.
- **The other company attacks (executed):** layout B under `-n 2` reads
  `failing on base too` at every gate. That is the base's truth there: each
  worker's last test carries the teardown error, and the group run fails
  both files. A `-x` row names one failing file on the branch, so its group
  is a group of one.
- **The seal (read, plus the row measured).** A green run never reaches
  `compare_at_base`: its one call sits at `:3498`, inside `if name ==
  SUITE` and `if files`, and the fix range has no hunk in `gate`. This
  repository's row was measured through c8d6c785's `compare_at_base` in a
  clone, with `ruff` clean on each base tree. The normal shape reads
  `failing on base too` / `new`, and the sibling-on-the-path shape reads
  `COMPANY` for both. Each proof shows the two `ruff` lines, `bin/test`'s
  own line, and one session listing only the file, at `-n auto`. The cancel
  shape is 🔴 1.
- **Rule 3, `SKILL.md`, the reasons, the changelog and the overview against
  the code (read):** the outcome-line sentence, the company sentence, the
  version example and the `MULTI_RUNNER` / `COLLECTED_BEYOND` texts match
  the code. The exceptions are 🔴 1 (the cancel sentence, unpinned by any
  case), 🟡 2 (the "as before" sentence), 🟡 3 (the `COMPANY` reason and
  `SKILL.md:510`), ⬜ 4 and ⬜ 5.
- **§2 audit:** `overview.md` labels the full suite, lint and typecheck
  `unverified` and names the sealer as the one who runs them. No record
  claims a broad run, so the label is honest.

## Regression tests to plant

Destination: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, after
test_a_first_runner_without_the_gates_environment_costs_the_word. Both were
run in the clone at c8d6c785 through `run_gate`, and both are red there, each
on `assert 'failing on base too' != 'failing on base too'` (2 failed). Plant
🔴 1's case with whichever answer the orchestrator chooses. If the limit is
named rather than closed, it pins the limit, and its last assertion becomes
`==` with the sentence that names it.

```python
# One sibling's import-time state helps one file and hurts another, so the
# group's count matches its files' counts alone (#789 round 2's 🔴 1).
POLLUTER = "import os\n\nos.environ['MODE'] = 'ready'\n\n\n" + PRE_EXISTING
NEEDS_MODE = (
    "import os\n\n\ndef test_b():\n    assert os.environ.get('MODE') == '{want}'\n"
)
HURT_BY_MODE = (
    "import os\n\n\ndef test_default_mode():\n    assert 'MODE' not in os.environ\n\n\n"
    + PRE_EXISTING.replace("test_old", "test_c_old")
)


def test_a_count_another_file_makes_up_does_not_earn_the_word(tmp_path):
    """#789 round 2's 🔴 1. `test_b` fails only alone, `test_c` fails one
    test more beside `test_a`, and the group's count equals its files'
    counts alone. The branch's regression in `test_b` is not the base's."""
    repo = base_then_feature(
        tmp_path / "repo",
        FILES_ROW,
        {
            "tests/test_a.py": POLLUTER,
            "tests/test_b.py": NEEDS_MODE.replace("{want}", "ready"),
            "tests/test_c.py": HURT_BY_MODE,
        },
        {"tests/test_b.py": NEEDS_MODE.replace("{want}", "gone")},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_b.py") != gate_module().ON_BASE, (
        out.stdout
    )


def test_a_measuring_runner_whose_output_the_gate_never_sees_earns_no_word(tmp_path):
    """#789 round 2's 🟡 2. The runner that measures sends its output to a
    file, and the runner after it lists only the failing file: the one
    session the proof sees is not the one that measured."""
    row = f"{FILES_ROW} tests/unit > unit.log; {FILES_ROW} tests/integration"
    repo = base_then_feature(
        tmp_path / "repo",
        row,
        {
            "tests/unit/test_u.py": PRE_EXISTING,
            "tests/integration/test_i.py": "def test_i():\n    assert True\n",
        },
        {"tests/integration/test_i.py": "def test_i():\n    assert False\n"},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert (
        verdict_of(out.stdout, "tests/integration/test_i.py") != gate_module().ON_BASE
    ), out.stdout
```

## Facts for the evidence ledger

- R3 (the groups): the company check compares the group's failing count
  with the sum of its files' failing counts alone (`<`). A file that fails
  more beside the others can make up for a file that fails only alone, so
  the check holds no per-file claim.
- R2 (the proof pass): a measuring runner whose output does not reach the
  gate leaves the proof reading whatever single session it sees.
- Measured this round: Python's subprocess text mode turns `\r\n` and `\r`
  into `\n`, so a pseudo-terminal's line endings never reach `RAN_RE`
  through `run`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A file the base fails only alone keeps `failing on base too` when another file of its group fails more beside the others (one sibling's import-time state with two effects, or a flaky test); the sum check cannot see per file, and rule 3's "two dependencies whose counts cancel" undersells it | `skills/verify/scripts/broad_gate.py:2362` | open | executed: cancel, cancel2, outweigh, flaky2 and cancel under `-n 2` through three gates' `compare_at_base`, and cancel2 under this repository's own row in a clone; a3aa139a `new` for the regressed file each time; regression against a3aa139a; a planted case red at c8d6c785 |
| 🟡 2 | A measuring runner whose output goes to a file, followed by a runner listing only the failing file, reads `failing on base too`; rule 3 says such limits are "as they were before", and a3aa139a read `new` | `skills/verify/scripts/broad_gate.py:2035` | open | executed: the swallow layout through three gates; the proof's one session is the second runner's; regression against a3aa139a; a planted case red at c8d6c785 |
| 🟡 3 | The `COMPANY` reason says the group "failed fewer tests than they fail one by one" where it is given because a file had no count alone | `skills/verify/scripts/broad_gate.py:1938` | open | read, plus the `a-file-with-no-count-alone` parameter executed in the narrow run; not a regression (new at fd98c2c8) |
| ⬜ 4 | Rule 3 does not name the two routes that never meet a group: a file run alone from the start (the one failing file, or a `cd sub` row's candidates) and a sibling the branch passes | `templates/config.md:333` | open | executed: cdsub and passing-sibling layouts read `failing on base too` at all three gates; not a regression |
| ⬜ 5 | `overview.md` says only S3–S5 is left and that leave-one-out would see the cancel; the changelog fragment says "depend on each other both ways" | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md` | open | a correction to the run's paperwork; falsified by 🔴 1 and 🟡 2 |
| 🟢 | round 1's first blocking finding is closed for layouts A, A2, B and the no-count shape; its class's remainder is this round's 🔴 1 | `skills/verify/scripts/broad_gate.py:2359` | confirmed | executed: each reads `COMPANY` at c8d6c785, also under `-n 2` |
| 🟢 | round 1's second blocking finding is closed — a first runner without the gate's environment | `skills/verify/scripts/broad_gate.py:2035` | confirmed | executed: layout C reads `MULTI_RUNNER`; `RAN_RE` attacked on real and constructed output with no permissive gap at `-q` |
| 🟢 | round 1's ⬜ 3 is closed — rule 3's per-version example | `templates/config.md:333` | confirmed | read; pinned in the rule 3 case |
| 🟢 | round 1's ⬜ 4 is closed — the PR body's acceptance sentence is scoped to the corpus | PR #814 body | confirmed | read via `gh pr view`; ⬜ 5 is this round's remainder |
| 🟢 | round 1's ❓ is carried out — the strict variant | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4795` | confirmed | executed: the narrow run passes both changed cases |
| 🟢 | The S3–S5 shape is the base's failure | `tests/test_the_seal_is_taken_once_by_the_sealer.py:6001` | confirmed | executed: four of the 18 words rebuilt; the base fails `tests/test_err.py` by hand each time |
| 🟢 | The corpus sample leaks nothing | `tests/test_the_seal_is_taken_once_by_the_sealer.py:6001` | confirmed | executed: 15 layouts × 2 rows, 32 file words, at a3aa139a and c8d6c785 |
| 🟢 | A green run is unchanged; this repository's row measures its normal and sibling shapes right | `skills/verify/scripts/broad_gate.py:3498` | confirmed | read (no hunk in `gate`); executed (the row through `compare_at_base` in a clone) |

## Executed probes

| What was run | Result |
|---|---|
| The narrow module run in the clone at c8d6c785, the five modules the prompt names | 725 passed, 1 skipped, exit 0 |
| `bin/evidence-check --strict .` in the clone at c8d6c785 | exit 0 |
| Round 1's layouts A, A2, B, C and the normal control through `compare_at_base` of a3aa139a, cdb57895 and c8d6c785 (pytest 9.1.1) | A/A2: on, `new` → on, on → `COMPANY` ×2; B: `new`, on → on, on → `COMPANY` ×2; C: `new` → on → `MULTI_RUNNER`; normal: on/`new` at all three |
| cancel, cancel2, outweigh, flaky2, cancel under `-n 2` through the same gates | the regressed test_b: a3aa139a `new`, c8d6c785 `failing on base too` in each; cancel2 and flaky2 put the word on all three files |
| This repository's row (`uvx ruff check . && uvx ruff format --check . && bin/test -q`) through c8d6c785's `compare_at_base` in a clone: normal, sibling on the path, cancel2 | on/`new`; `COMPANY` ×2; `failing on base too` ×3, with the base's group run passing the regressed file (`3 failed, 1 passed`) |
| The swallow row through three gates | a3aa139a `new`; cdb57895 and c8d6c785 `failing on base too`; the proof's one session is the second runner's |
| cdsub (`cd sub` row, ini in `sub`), passing-sibling, xdist-A, xdist-B, `-x` | cdsub and passing-sibling: on at every gate (⬜ 4); xdist-A: `COMPANY` at c8d6c785; xdist-B: on at every gate, the base's truth there; `-x`: a group of one |
| S3–S5 rebuilt: Axis A's inner `tests/test_g.py`, under `-q -rN` (stderr), `-q -rN` (stdout), `-q -n 2 -rN` (stderr), and a stderr inner run under `-q -s` | `tests/test_err.py`: a3aa139a `new`, c8d6c785 `failing on base too`; by hand at the base it exits 1 (`1 failed`) |
| Corpus sample: 15 `REGRESSED` layouts × own and files-only rows, at a3aa139a and c8d6c785 | 32 file words, no leak, every target word equal to the planted table's |
| `proof_refused` at c8d6c785 on outcome-line shapes, and a real pseudo-terminal capture via `script` | `-q`, ruled and pytest-sugar lines → `MULTI_RUNNER`; uv, tox, `files checked`, `no tests ran` → proven; raw `\r\n` would be proven, and `run`'s text mode removes it before the reader |
| The two cases under *Regression tests to plant*, in the clone at c8d6c785 | 2 failed, each on the permissive word |
| Broad gate: the full suite, lint and typecheck after the rounds | not yet — not run by this round; the sealer's, once the rounds settle |

## Paste-ready fixes

### 🔴 1 — name the shape as it is (rule 3, the docstring, the comment), and pin it

```text
templates/config.md, rule 3 — replace:
  Two dependencies in one group whose counts cancel, one file failing only beside the others and another only alone, also leave a word standing.

With:
  **The files of a failing group are compared by counts, never one by one.** Where one file fails only alone and another fails more tests beside the others than alone, the group's count can match or pass its files' counts, and every word the files earned alone stands, a regression the base passes in the row included: one sibling's import-time state that one file needs and another trips over does it, and so does a flaky test that fails in the group's run and passes alone. 0.18.2 read such a file `new`.
```

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ compare_at_base docstring
-    runner, also as before (this work item's `questions.md` Q1). Two
-    dependencies whose counts cancel, one file failing only beside the
-    others and another only alone, leave a group's count equal and its
-    words standing.
+    runner, also as before (this work item's `questions.md` Q1). The
+    company check compares counts and never files: where one file fails
+    only alone and another fails more beside the others than alone -- one
+    sibling's import-time state with both effects, or a flaky test that
+    fails in the group's run -- the group's count matches or passes its
+    files' counts and every word they earned alone stands (#789 round 2).
@@ the comment above the check
-        # failure in the row, and no count says whose: every word a file of
-        # the group earned alone falls back to `COMPANY`. A file with no
-        # count alone counts the same way (#789 round 1).
+        # failure in the row, and no count says whose: every word a file of
+        # the group earned alone falls back to `COMPANY`. A file with no
+        # count alone counts the same way (#789 round 1). A file that fails
+        # more beside the others makes up for one that fails only alone,
+        # and then nothing here sees it: rule 3 names it (#789 round 2).
```

```diff
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written, the sentences rule 3 must carry
+        # #789 round 2's 🔴 1.
+        "**The files of a failing group are compared by counts, never one by "
+        "one.**",
+        "one sibling's import-time state that one file needs and another trips "
+        "over does it, and so does a flaky test that fails in the group's run "
+        "and passes alone. 0.18.2 read such a file `new`.",
@@ the sentences that must be gone
+        "Two dependencies in one group whose counts cancel",
```

### 🟡 2 — the silent measuring runner in rule 3's limit, and the "as before" sentence

```text
templates/config.md, rule 3 — replace:
  **A second runner the proof run does not reach, or that prints nothing it can read** — one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq`, one started without the gate's environment at `-qq` or quieter — leaves the row read as one with a single runner, so a file another runner named can read `failing on base too` from the measuring runner's directory. And where a row runs pytest twice and the base passes the file under the runner a prefix reaches first, the file reads `new` from that runner. Both are as they were before the proof run existed.

With:
  **A runner the proof run does not reach, or that prints nothing it can read** — one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq`, one started without the gate's environment at `-qq` or quieter, one whose output goes to a file — leaves the row read as one with a single runner, so a file another runner named can read `failing on base too` from the measuring runner's directory. Where the silent runner is the one that measured and a later runner lists only the file, the proof reads the later runner's session, and the word is new: 0.18.2 read `new` there. And where a row runs pytest twice and the base passes the file under the runner a prefix reaches first, the file reads `new` from that runner, as it did before the proof run existed.
```

The pinned sentence in
test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written
moves with it.

```diff
-        "**A second runner the proof run does not reach, or that prints "
-        "nothing it can read** — one behind `\\|\\|`, one behind a part that "
-        "exits non-zero under collection alone, one at `-qqqq`, one started "
-        "without the gate's environment at `-qq` or quieter — leaves the row "
-        "read as one with a single runner, so a file another runner named can "
-        "read `failing on base too` from the measuring runner's directory.",
+        "**A runner the proof run does not reach, or that prints nothing it "
+        "can read** — one behind `\\|\\|`, one behind a part that exits "
+        "non-zero under collection alone, one at `-qqqq`, one started without "
+        "the gate's environment at `-qq` or quieter, one whose output goes to "
+        "a file — leaves the row read as one with a single runner",
+        "Where the silent runner is the one that measured and a later runner "
+        "lists only the file, the proof reads the later runner's session, and "
+        "the word is new: 0.18.2 read `new` there.",
```

### 🟡 3 — a `COMPANY` reason that is true on both routes

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ -1938,6 +1938,7 @@
 COMPANY = (
     f"{NOT_MEASURED}: the base fails this file run alone, but the run of the "
     "failing files together at the base failed fewer tests than they fail one "
-    "by one (kept as suite-at-base-<k>.txt and suite-at-base-<k>-{n}.txt), so "
-    "the failure alone may not be the base's failure in the row"
+    "by one, or one of them wrote no report alone (kept as suite-at-base-<k>.txt "
+    "and suite-at-base-<k>-{n}.txt), so the failure alone may not be the base's "
+    "failure in the row"
 )
--- a/skills/verify/SKILL.md
+++ b/skills/verify/SKILL.md
@@ -508,3 +508,4 @@
   pytest more than once when the gate asked it only to collect, or the
   failing files run together at the base failed fewer tests than they fail
-  one by one. It is a
+  one by one or one of them wrote no report alone. It is a
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ test_the_unmeasured_word_says_so_and_every_reader_is_told_it
     assert gate.COMPANY.format(n=2) == (
         "new? not measured: the base fails this file run alone, but the run of "
         "the failing files together at the base failed fewer tests than they "
-        "fail one by one (kept as suite-at-base-<k>.txt and "
-        "suite-at-base-<k>-2.txt), so the failure alone may not be the base's "
-        "failure in the row"
+        "fail one by one, or one of them wrote no report alone (kept as "
+        "suite-at-base-<k>.txt and suite-at-base-<k>-2.txt), so the failure "
+        "alone may not be the base's failure in the row"
     )
@@ the SKILL.md phrases every reader is told
-        "run together at the base failed fewer tests than they fail one by one",
+        "run together at the base failed fewer tests than they fail one by one "
+        "or one of them wrote no report alone",
```

### ⬜ 4 — the routes that never meet a group

```text
templates/config.md, rule 3 — after the 🔴 1 sentence, add:
  A file that runs alone from the start meets no group to be compared with — the one failing file the base carries at the root, or every failing file of a `cd sub` row, whose paths the root's tree does not carry — and a sibling the branch passes is never run at the base, so a module or state another file gives it in the row is not seen there either, as before the proof run existed.
```

### ⬜ 5 — the run's paperwork (a correction)

```text
overview.md, Not done — replace:
  After round 1's fix pass only one is left: the S3–S5 shape, …
With:
  After round 1's fix pass the S3–S5 shape is the one exception the corpus holds. Round 2 found two more outside it, both regressions against a3aa139a: a group whose count another file makes up (round 2's 🔴 1), and a measuring runner whose output never reaches the gate (round 2's 🟡 2).

overview.md, Not done — replace:
  A leave-one-out run, the group without each file, would see it at one more run per file the base fails alone;
With:
  A leave-one-out run does not see it either: in a two-file group the group without one file is the other file alone, and a flaky test defeats any rerun. Only a per-file answer from the group's own run would, and the report's names are the one such answer, which #812 stopped reading;

changelog.md — replace:
  One new limit is named beside them: in a group whose files depend on each other both ways, so that the counts cancel, the words stand.
With:
  One new limit is named beside them: the files of a failing group are compared by counts, so where one file fails only alone and another fails more beside the others — one sibling's import-time state, or a flaky test — the words they earned alone stand.
```

Needs a fix: yes — 🔴 1 (a group's count another file makes up keeps failing on base too on a regression), 🟡 2 (a measuring runner whose output never reaches the gate), 🟡 3 (the COMPANY reason is false on the no-count route)
Loses a record or crashes: no

## Proof block

Files opened this round, all at c8d6c785 unless named:
`skills/verify/scripts/broad_gate.py` (lines 1855–2372, `run`, `failing_files`,
the `gate` call site at 3470–3545), a3aa139a's and cdb57895's copies of it
(driven, not read in full), `templates/config.md` (rule 3, via the diff),
`skills/verify/SKILL.md` (the bullet, via the diff),
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the fix range's diff,
`build_repo`, `base_then_feature`, the planted corpus case and its
`REGRESSED_WORDS`, the rule 3 pins), `bin/test`, `seal/config.md` (the
`Broad gate` row), `.github/scripts/run_tests.py` (where the venv lives),
this work item's `rounds/round-1.md`, `rounds/round-1-report.md`,
`overview.md`, `changelog.md`, the fix range's diff of `phases/phase-1.md`
and `phases/phase-2.md`, `phases/phase-2.md` lines 1–106, the first build's
`spec.md` Axis A at a82f8f8f, the code-review skill's severity lines, and
PR #814's body. Not opened: `spec.md`, `plan.md`, `questions.md`,
`survivors.md`, `phases/phase-3.md`, and the ledger fragment beyond the fix
range's diff header.
