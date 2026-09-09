# Round 1 — `fix/262-310-a-case-pins-what-it-actually-measures`

| Field | Value |
|---|---|
| Target SHA | `47118c1` |
| Base | `origin/release/v0.9.5` (`0df9508`) |
| Reviewed in | a `git clone --no-local` at the target SHA; nothing was written in the working tree but this report |
| Rounds inherited | none — `rounds/` was empty, so no verdict is carried |

## The account, and what the code said

The implementer's report reached me through the spawn prompt as claims with
coordinates. I opened every one of them and **every measured number in it is
correct**, which is worth saying plainly because it is the half of a review
that usually goes unrecorded.

Reproduced by running the checker myself over `hooks/review-history-guard.py`
against `tests/test_chain_hooks.py`, all 64 mutations: 32 arms split `reader`
5 · `is_closed` 4 · `gh_segments` 5 · `main` 17 · `<module>` 1; `invert` 32
asked · 31 killed · 1 survived; `remove` 32 asked · 20 killed · 12 survived;
the one arm nothing watches is `main:189`, `except Exception`; exit 0. No
`refused` section and no `not asked` section printed, so the `remove 31 asked`
defect `phase-3.md:73` describes is genuinely closed. The classification is
total over the grammar in **both** directions — 122 classified, 122 derived,
no overlap — and I checked it on two interpreters, CPython 3.12.11 and
3.13.9, rather than the one the records name.

One claim in the account is **not** what the code does, and it is the count of
ledger rows and of cases: `overview.md:5` says the fragment carries 4 rows
where it carries 6, and `overview.md:6` says 26 cases where
`tests/test_arm_check.py` holds 35. `phase-4.md:82` and `phase-3.md:160` state
6 and 35 correctly, so the diff contradicts itself in one file. Those are
records rather than mechanism and they are filed below as corrections.

## Findings

### 🟡 1 · A hung `--tests` command is unbounded, and the only copy of the module is in the dead process's memory

`skills/verify/scripts/arm_check.py:745`

`subprocess.run(tests, cwd=cwd, capture_output=True, text=True, env=env)`
carries no `timeout`. While the command runs, the module on disk holds the
mutation, and `capture_output=True` means nothing is printed, so a command
that never returns is indistinguishable from one that is slow.

Every code path restores. I read all of them and the outer `finally` at
`arm_check.py:767` covers the one gap the inner one leaves — an exception
between the write at line 741 and the inner `try` at line 744 — so
`phase-3.md:140`'s claim about what only the end-of-run restore covers is
accurate, and `KeyboardInterrupt` runs both. **What no `finally` covers is a
signal that is not delivered to Python**: a `SIGKILL`, an OOM kill, a closed
terminal, a machine that sleeps and is reset. The run then ends with the
target module mutated and `original` lost with the process.

Why it matters beyond an inconvenience: the design's own selling point is that
it never uses `git checkout`, because that reaches uncommitted work
(`SKILL.md:73`). Recovering from an abnormal exit needs exactly that
checkout — and if the module being checked carried uncommitted edits, they are
gone, because no copy of them exists anywhere on disk. The hang is what makes
the abnormal exit likely rather than theoretical.

Two fixes, and they are independent: a timeout so a hang becomes a named
unmeasured pair, and a sidecar copy so a kill is recoverable without git.

### 🟡 2 · A `--tests` command that cannot be spawned discards every verdict already measured

`skills/verify/scripts/arm_check.py:745`

`OSError` from `subprocess.run` is caught nowhere. Executed on a three-arm
fixture: a `--tests` of `definitely-not-a-command-xyz` raises
`FileNotFoundError` straight out of `run_arms`, and `main` never reaches
`_report`. The module is restored — the `finally` chain holds — but the run
produces no report at all.

The interesting case is not the typo, it is arm 20 of 32. Driven by making
`subprocess.run` raise on its third call: the two verdicts already measured
are discarded and nothing is printed. `bin/test` builds a virtual environment
on demand (`bin/test:2`), so a mid-run spawn failure is a reachable state
rather than a constructed one, and it costs the whole measurement rather than
one pair.

This is the module's own subject arriving from the other side. `Verdict`'s
`not_applicable` exists so that one unaskable pair is named instead of falling
out of a denominator; a spawn failure makes *every* pair fall out, and loudly
rather than silently, which is better but not enough. The same `except` clause
that fixes finding 1's timeout fixes this.

### 🟡 3 · `_splice` splits lines on separators the tokenizer does not, so one form feed mis-indexes every arm below it

`skills/verify/scripts/arm_check.py:520`

`source.splitlines(keepends=True)` splits on `\x0b`, `\x0c`, `\x1c`, `\x1d`,
`\x1e`, `\x85`, `\u2028` and `\u2029` in addition to the three line
terminators. None of those ends a line for `ast`, so `span.lineno` and the
list index part company at the first one.

Executed. A module with a single form feed on its own line above the arm:
`arms()` returns the correct spans, and `mutate()` raises `IndentationError`.
Because `IndentationError` subclasses `SyntaxError`, `run_arms:738` files it
as `not_applicable` — so every arm below the form feed comes back as an
unasked pair with `IndentationError` beside it and no hint that the reason is
the checker's own line arithmetic. That is the enumeration going short through
a door the totality case cannot see, which is the failure the module docstring
argues about at `arm_check.py:36`.

The refusal is the good outcome. The bad one is a mis-indexed splice that
still parses, which is a verdict recorded against a mutation nobody asked for
and which `restore`'s hash cannot see, for the same reason the bytecode cache
row in the ledger fragment gives.

Answerable with grounds: `git grep -lIP '\x0c' -- '*.py'` finds none in this
tree today, so nothing here triggers it. The checker is documented as a
general instrument in `skills/verify/SKILL.md` §2, which is what makes "no
module here has one" an argument about today rather than about the tool.

The fix is verified across five separator cases — plain, form feed, two form
feeds, CRLF, non-ASCII — and is `OK` on all five where `splitlines` is
`IndentationError` on two.

### 🟡 4 · #310's clause-2 assertion pins the clause's position in its sentence, which its own docstring says is not the claim

`tests/test_a_segment_feeds_the_flow_log.py:562`

The needle is `"Batching is the ordinary way in and a background command is
the rarer one"`, matched against `body` rather than `body.lower()`. The
capital `B` pins the clause to being sentence-initial.

Executed, three arms against the real document with the file restored from
held bytes and sha256-compared after each:

| Arm | Exit | Reading |
|---|---|---|
| unmutated | 0 | green as shipped |
| the two causes swapped | 1 | the #310 regression is genuinely closed |
| the measured direction inverted | 1 | closed |
| `In practice, ` inserted before the clause | **1** | **over-pinned** |

The third arm changes no word of the clause, keeps the ranking and keeps the
direction, and the case goes red. The case's fourth assertion lowers case
deliberately, saying *the same phrase returning at the start of a sentence is
the same regression* — so the case treats sentence position as noise in one
assertion and as the claim in another.

Why it matters: this is a false alarm on the repository's own prose. The next
person who adds a clause to that paragraph gets a red case whose message says
the ranking was reversed when it was not, and the cheap repair is to weaken
the assertion.

The fix lowers both sides. Verified: arm A stays red, arm B stays red, arm C
goes green, unmutated stays green.

### 🟡 5 · `skills/verify/SKILL.md` writes two hand-taken numbers into durable shipped prose with no date and no case

`skills/verify/SKILL.md:80`

The new section carries a table whose third column is headed *On
`hooks/review-history-guard.py`* and holds `1 of 32 survived` and `12 of 32
survived`. Both are correct today — I reproduced them. Neither carries a date,
a SHA, or the command that produced them, and no case in the tree reads that
section: `grep -rn "arm-check\|arm_check" tests/` returns only
`tests/test_arm_check.py` itself.

This is the work item's founding argument applied to the work item. #262's
table says 33 where the module holds 31 because the file changed twice after
the count was taken, and the diff's answer is a checker so that nobody types
the number again. The diff then types two numbers into a shipped skill, in a
column shaped like a property of the module, where they will rot the moment
either `hooks/review-history-guard.py` or `tests/test_chain_hooks.py` moves —
and the changelog fragment already records them properly, as a dated
measurement.

The fragment and `phase-4.md` are the right home for a measurement. The fix
is to date the column and say in the prose that the numbers are a
measurement, not a property.

Contract §14 is the other half: 45 lines of new prose a person reads and acts
on, pinned by nothing. I am not asking for the numbers to be pinned — a case
asserting `12 of 32` is the rotting list one file further on. What is worth
pinning is the claims: report-only exit 0, refusal rather than skip, and which
operator row #262's table compares with.

### 🟡 6 · For a sole-type `except`, `invert` and `remove` are byte-identical, so two rows report one measurement

`skills/verify/scripts/arm_check.py:589`

For a handler whose type is not a tuple, `_node_arms:428` sets `group` to the
type's own span and `group_without` to `NEVER_RAISED`. `remove` then splices
`NEVER_RAISED` over the type at line 581, and `invert` splices `NEVER_RAISED`
over the same span at line 590. Executed: `mutate(src, arm, "invert") ==
mutate(src, arm, "remove")` is `True`.

`hooks/review-history-guard.py` has three such arms — `is_closed:143`
(`OSError`), `gh_segments:173` (`ValueError`) and `main:189` (`Exception`) —
so three of the run's 64 subprocess calls are duplicates, at roughly 4.6s
each on this machine.

The cost that matters is not the time. `main:189` is the one arm the report
headlines as watched by nothing, and it prints `invert survived · remove
survived` — one measurement shown as two independent answers to the two
questions `OPERATORS`' docstring says are different. A reader comparing the
`remove` row's 12 with #262's nine is comparing a row in which one of the
twelve was measured by the other operator.

Semantically the identical text is correct: dropping the only member of an
except tuple and aiming it elsewhere are the same edit. The report is what is
wrong, and this module's own discipline says which way to resolve it — name
the pair as not asked rather than ask it twice. The fix does that. Its cost is
that `invert`'s row becomes `29 asked` and four records re-state a number, so
this is the finding most open to being answered with grounds instead.

### 🟡 7 · The declared exclusions are invisible in the report, so `N arms` reads as the module's branch count

`skills/verify/scripts/arm_check.py:233`

`Assert`, `For` and `AsyncFor` are excluded by declaration rather than because
they carry no branch, and `NOT_ARMS` says so with the grounds beside each. I
judged the grounds and they hold: counting them would move every per-function
number away from the hand count the walk is checked against, and
`phase-2.md`'s §*What I refused* states it.

What does not hold is that the exclusion is auditable from the report.
Executed on a module whose branching is an `assert x > 0 and x < 10` and a
`for`/`else`: the report prints `declared_exclusions.py — 1 arms`, naming only
the inner `if` (NAME NOT IN TREE — that is the probe fixture's own filename).
Nothing says two node types were passed over by declaration.

The grounds live in the source. The report is what a person reads, and for the
general use `skills/verify/SKILL.md` §2 now advertises — *asks condition 2 of
a whole module* — `1 arms` on a module with an assert pair and a loop-else is
an answer that reads as *this module has one branch*. The fix names them where
the total is printed, which is cheaper than revisiting the exclusion and keeps
the exclusion overturnable by whoever reads the run.

### 🟡 8 · `--only` makes the header state the module's total as the filtered count

`skills/verify/scripts/arm_check.py:787`

`_report` computes its header from `counted`, which is already filtered.
Executed: `arm-check hooks/review-history-guard.py --only reader` prints
`hooks/review-history-guard.py — 5 arms` for a module that holds 32. Under
`--tests` the same line is built from `found = [v.arm for v in verdicts] + [a
for a, _ in refused]`, so it is filtered there too.

The line names the file and gives a total, so it reads as the file's total.
A run pasted into a record — which is what `phase-4.md` and the ledger
fragment do with this output — carries the wrong denominator with it, and the
`--only` flag that produced it is not in the pasted text.

### ⬜ 9 · `overview.md` states two counts its sibling records state correctly

`seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:5`
says the ledger fragment carries **4 rows**; it carries **6**
(`grep -c '^| '` returns 7, header included), and `phase-4.md:82` says 6.

The same line's successor, `overview.md:6`, says **26 cases** in
`tests/test_arm_check.py`; `grep -c '^def test_'` returns **35**, the module's
own run reports `35 passed`, and `phase-3.md:160` says 35.

Enumerated rather than fixed at the coordinate: I swept `plan.md`'s phase
table, all four `phases/phase-N.md`, `questions.md`, `spec.md`, `survivors.md`
and `routing.md` for the same class — a record stating a count of something
the diff contains — and found no others. `plan.md:15`'s total of 31 is the
pre-implementation number and `overview.md:20`'s divergence row answers it
explicitly. `phase-4.md:88`'s `1056 ok · 0 drifted · 0 broken` and the
fragment's 15 anchors both match what I ran.

Under `docs/review-chain-spec.md` §*The last round verifies* these are the
run's paperwork, so they are corrections and not in `Needs a fix`.

### ⬜ 10 · The `PYTHONDONTWRITEBYTECODE` exemption names a path the code makes narrower than stated

`tests/test_arm_check.py:744`

The self-report is **true** and I checked it rather than taking it: with
`env["PYTHONDONTWRITEBYTECODE"]` deleted, the per-arm
`clear_bytecode_cache(path)` in the inner `finally` still removes whatever the
subprocess wrote, so `test_the_run_leaves_no_bytecode_cache_behind` stays
green and the env var is genuinely an arm no case kills. `phase-3.md:134`'s
reasoning is sound and not circular, and the end-of-run restore's stated
narrow path — an exception between the write and the inner `try` — is
reachable exactly as described.

The one overstatement is the reason given for keeping the env var: *a
subprocess whose `PYTHONPYCACHEPREFIX` differs from this process's*.
`run_arms:726` builds `env` from `dict(os.environ)`, so the subprocess
inherits the parent's value and cannot differ through the environment. If the
parent was started with `-X pycache_prefix`, `clear_bytecode_cache:654` reads
`sys.pycache_prefix` and looks in the right place while the subprocess, having
no env var, writes to plain `__pycache__` — which is `roots[0]` and is also
cleared. The path is real only when the `--tests` command itself sets the
variable, which is narrower than the sentence suggests. Worth one clause, not
a change.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A hung `--tests` command is unbounded, and a kill during the hang leaves the module mutated with no copy on disk | `skills/verify/scripts/arm_check.py:745` | open | Read: no `timeout` argument; every ordinary path and `KeyboardInterrupt` restore, verified across both `finally` blocks. No `finally` sees `SIGKILL` |
| 2 | A `--tests` command that cannot be spawned raises out of `run_arms`, discarding every verdict measured so far and printing no report | `skills/verify/scripts/arm_check.py:745` | open | Executed: a nonexistent command raises `FileNotFoundError`; `subprocess.run` made to raise on its third call discarded two measured verdicts |
| 3 | `_splice` uses `str.splitlines`, which splits on separators `ast` does not, so one form feed files every arm below it as an unasked pair | `skills/verify/scripts/arm_check.py:520` | open | Executed: spans correct, `mutate` raises `IndentationError`; the proposed `_lines` is `OK` on all five separator cases (NAME NOT IN TREE — the fix below defines it) |
| 4 | #310's clause-2 assertion is case-sensitive on its first letter, so it pins the clause's sentence position | `tests/test_a_segment_feeds_the_flow_log.py:562` | open | Executed: `In practice, ` inserted before the clause, ranking and direction intact, exit 1. Lowering both sides leaves arms A and B red and arm C green |
| 5 | The new skill section writes `1 of 32` and `12 of 32` into durable prose with no date, no SHA and no case | `skills/verify/SKILL.md:80` | open | Executed: numbers reproduced and correct today. Read: no test in `tests/` reads that section |
| 6 | For a sole-type `except`, `invert` and `remove` produce identical text, so the two operator rows report one measurement twice — including for the headlined survivor `main:189` | `skills/verify/scripts/arm_check.py:589` | open | Executed: the two mutations compare equal; three such arms in the guard, one of them the single survivor |
| 7 | `Assert`, `For` and `AsyncFor` are excluded by declaration and the report never says so, so `N arms` reads as the module's branch count | `skills/verify/scripts/arm_check.py:233` | open | Executed: a module with an assert pair and a `for`/`else` reports `1 arms`. The grounds for the exclusions themselves hold |
| 8 | `--only` makes the report header state the filtered count as the module's total | `skills/verify/scripts/arm_check.py:787` | open | Executed: `--only reader` prints `— 5 arms` for a 32-arm module |
| 9 | `overview.md` says 4 ledger rows against 6, and 26 cases against 35; both sibling phase records are correct | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:5` | open | Executed: `grep -c` and the module's own `35 passed`. Class swept across `plan.md`, four phase records, `spec.md`, `questions.md`, `survivors.md`, `routing.md` — no other instance |
| 10 | The `PYTHONDONTWRITEBYTECODE` self-report is true; the reason given for keeping it names a path `dict(os.environ)` makes narrower | `tests/test_arm_check.py:744` | open | Read: `env` is inherited, and both `pycache` roots are cleared. Reachable only when the `--tests` command sets the variable |
| — | Grammar totality, both directions, on two interpreters | `skills/verify/scripts/arm_check.py:87` | answered | Executed: 122 classified, 122 derived, empty both ways, no overlap, on CPython 3.12.11 and 3.13.9 |
| — | The two `bin/` wrappers are faithful transcriptions and are already pinned class-level | `bin/arm-check.cmd:7` | answered | Executed: non-comment diff against the sibling pair differs in the script path alone; `test_every_posix_wrapper_resolves_its_own_directory[arm-check]` collects, and the `.cmd`-twin case enumerates `bin/` — 53 passed |
| — | The run leaves no mutated module, no bytecode for the target and no temp file | `skills/verify/scripts/arm_check.py:767` | answered | Executed: clone `git status` empty after 64 mutations; `hooks/__pycache__` holds no `review-history-guard` entry |
| — | This branch falsifies no ledger row elsewhere | `seal/ledger.md` | answered | Executed: `evidence_check.py .` unscoped, exit 0, `1056 ok · 0 drifted · 0 broken`. An earlier reading showed one DRIFTED row and was my own concurrent mutation of the guard, not a finding |

## Executed probes

| What was run | Result |
|---|---|
| `python3 skills/verify/scripts/arm_check.py hooks/review-history-guard.py` | 32 arms; `reader` 5 · `is_closed` 4 · `gh_segments` 5 · `main` 17 · `<module>` 1 — the account's split, cell for cell |
| `python3 skills/verify/scripts/arm_check.py hooks/review-history-guard.py --tests "bin/test tests/test_chain_hooks.py -q"` | exit 0. `32 arms mutated · 31 killed · 1 watched by no case`; `invert 32 asked · 31 killed · 1 survived`; `remove 32 asked · 20 killed · 12 survived`; survivor `main:189 ExceptHandler Exception`. No refused and no not-asked section |
| `.venv/bin/python -m pytest tests/test_arm_check.py -q` | `35 passed` (exit 0), on CPython 3.13.9 |
| `.venv/bin/python -m pytest tests/test_a_segment_feeds_the_flow_log.py -q` | `28 passed` (exit 0) |
| `.venv/bin/python -m pytest tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` | `53 passed` (exit 0); `test_every_posix_wrapper_resolves_its_own_directory[arm-check]` collected |
| `python3 skills/evidence-check/scripts/evidence_check.py .` unscoped, exit code read directly | exit 0, `total: 1056 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; the work item's fragment `15 ok`. **Taken twice, and the second reading is this report's own footprint.** In the clone, before this file existed, `485 names read`. Re-run in the working tree with this file present: exit **2**, three `NOT-IN-TREE` rows for `_lines` — a name finding 3's fix proposes and the tree does not have. Marked `NAME NOT IN TREE` on each of the three lines, and back to exit 0 with `521 names read` and `0 refused`. A later round reading a 2 here is reading the report, not a regression in the branch |
| Grammar derivation against `ast.AST`'s subclass tree, independently written, on CPython 3.12.11 and 3.13.9 | `derived - CLASSIFIED` empty and `CLASSIFIED - derived` empty on both; 122 = 122; `ARM_SHAPES ∩ NOT_ARM_NAMES` empty |
| `_splice` against five separator cases with `splitlines` and with the proposed `_lines` (NAME NOT IN TREE — the fix under finding 3 defines it) | `splitlines`: `IndentationError` on form feed and on two form feeds, `OK` on plain, CRLF and non-ASCII. `_lines`: `OK` on all five |
| `mutate(src, arm, "invert") == mutate(src, arm, "remove")` on a sole-type `except OSError` | `True` |
| `run_arms` with a nonexistent `--tests`, and with `subprocess.run` raising on its third call | `FileNotFoundError` out of `run_arms` both times; module restored both times; no report printed, two measured verdicts discarded in the second |
| `_report` on a module holding `assert x > 0 and x < 10` and a `for`/`else` | `declared_exclusions.py — 1 arms` (NAME NOT IN TREE — the probe fixture's filename); nothing names the excluded types |
| `_report` with `counts()` filtered to `reader` | `hooks/review-history-guard.py — 5 arms` for a 32-arm module |
| The #310 case against the real document, four arms, file restored from held bytes and sha256-compared after each | unmutated 0 · causes swapped 1 · direction inverted 1 · `In practice, ` inserted **1**. With the proposed fix applied: 0 · 1 · 1 · **0** |
| Non-comment diff of `bin/arm-check` and `bin/arm-check.cmd` against `bin/survivor-check` and `.cmd` | identical but for the script path line |
| `git -C <clone> status --porcelain` after all 64 mutations and every probe | empty |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| What `arm-check`'s exit code should mean | `questions.md` Q1 — already deferred, report-only today and pinned by `test_the_checker_is_report_only_and_exits_zero_over_the_real_module` | the repository owner |
| Whether the twelve `remove` survivors are gaps | `questions.md` Q2 — already deferred, with `phase-4.md:38`'s table of the twelve as the input | a later work item |
| A sweep of the tree for other cases pinning a document clause by substring | #310's inherited `Not verified` row and `overview.md:32` — already deferred, and out of scope for this round by the spawn prompt | whoever builds that sweep; #310 stays open on it |
| #262's table of 33 left as written | `questions.md` assumption 3 — already deferred | nobody; a deliberate refusal |
| The full suite, repository-wide lint and typecheck | contract §2: the broad gate is the orchestrator's, run once after the rounds settle. Nine narrow modules were run in this round and are labelled above; `ruff` is not installed in the clone's virtual environment | **the review orchestrator** |
| Windows and Linux | `overview.md:29` — already deferred. `bin/arm-check.cmd` has been run by nobody; its equivalence to a sibling that has been run is **read**, not executed | CI's windows and linux legs |

## Paste-ready fixes

Finding 1 and finding 2, one block — `skills/verify/scripts/arm_check.py`,
replacing the subprocess call and its `finally` at lines 744-751:

```python
                try:
                    run = subprocess.run(
                        tests,
                        cwd=cwd,
                        capture_output=True,
                        text=True,
                        env=env,
                        timeout=timeout,
                    )
                    by_operator[operator] = run.returncode != 0
                except subprocess.TimeoutExpired:
                    # A command that never returns is not a verdict. `killed`
                    # would read as *a case noticed* and `survived` as *none
                    # did*, and neither was measured -- so it goes where the
                    # un-asked pairs go, with the bound in the reason.
                    not_applicable[operator] = (
                        f"TimeoutExpired: the command did not return within "
                        f"{timeout}s, so this arm was not measured"
                    )
                except OSError as exc:
                    # The command could not be spawned. Every verdict taken
                    # before this one is real, so the report has to survive to
                    # print them: raising here discards the whole run for one
                    # failed spawn, and `bin/test` builds a virtualenv on
                    # demand, so a mid-run failure is reachable.
                    not_applicable[operator] = f"{type(exc).__name__}: {exc}"
                finally:
                    restore(path, original, original_sha)
                    clear_bytecode_cache(path)
```

with the parameter, in `run_arms`'s signature:

```python
def run_arms(
    path: str,
    tests: list[str],
    *,
    only: str | None = None,
    cwd: str | None = None,
    operators: tuple[str, ...] = OPERATORS,
    timeout: float | None = 900.0,
    echo=lambda _msg: None,
) -> tuple[list[Verdict], list[tuple[Arm, str]]]:
```

and the flag, in `main`:

```python
    parser.add_argument(
        "--timeout",
        type=float,
        default=900.0,
        help=(
            "seconds one arm's command may take before it is recorded as "
            "unmeasured rather than waited on. 0 removes the bound"
        ),
    )
```

```python
    verdicts, refused = run_arms(
        args.module,
        shlex.split(args.tests),
        only=args.only,
        cwd=args.cwd or os.getcwd(),
        timeout=args.timeout or None,
        echo=echo,
    )
```

Finding 1's second half, the sidecar — `skills/verify/scripts/arm_check.py`,
after `original_sha` is computed at line 717:

```python
    # A copy on disk, because `original` above lives only in this process and
    # no `finally` runs for a SIGKILL, an OOM kill or a closed terminal. The
    # module under check may carry uncommitted edits; without this, an
    # abnormal exit mid-arm loses them and `git checkout` -- which this
    # checker refuses precisely because it reaches uncommitted work -- is the
    # only way back. Its presence at the start of a run is what says the last
    # one died mutated.
    held = path + ".arm-check-original"
    if os.path.exists(held):
        raise RuntimeError(
            f"{held} already exists, so an earlier run ended without "
            f"restoring {path}. Compare the two and remove it before "
            f"running again -- overwriting it would discard the only copy "
            f"of what that run was handed."
        )
    with open(held, "wb") as f:
        f.write(original)
```

and in the outer `finally` at line 767:

```python
    finally:
        # An arm no case kills, and reported rather than removed -- which is
        # the verdict this whole module exists to produce, applied to itself.
        # The per-arm restore above already leaves the module clean, so
        # `test_the_module_is_restored_byte_for_byte_after_the_run` goes red
        # only when BOTH are gone (measured). What only this one covers is an
        # exception escaping between the write and the inner `try` -- a
        # `clear_bytecode_cache` that raises on a permissions error, say --
        # where the module would otherwise be left mutated on disk.
        restore(path, original, original_sha)
        os.remove(held)
```

Finding 3 — `skills/verify/scripts/arm_check.py`, a new helper above
`_splice`, plus `import re` beside `import os`:

```python
#: The line terminators `ast` counts, and only those.
_LINE_END = re.compile(r"\r\n|\r|\n")


def _lines(source: str) -> list[str]:
    """`source` split at the line terminators `ast` counts, keeping them.

    Not `str.splitlines`, which also splits on `\\x0b`, `\\x0c`, `\\x1c`,
    `\\x1d`, `\\x1e`, `\\x85`, `\\u2028` and `\\u2029`. None of those ends a
    line for the tokenizer, so a single form feed above an arm shifts every
    span below it by one line. Measured: one form feed turns every arm of a
    module into an un-asked pair with an `IndentationError` beside it, and a
    mis-indexed splice that happens to parse is a verdict recorded against a
    mutation nobody asked for -- which no hash catches, for the same reason
    the bytecode cache does not.
    """
    out, start = [], 0
    for match in _LINE_END.finditer(source):
        out.append(source[start : match.end()])
        start = match.end()
    if start < len(source):
        out.append(source[start:])
    return out
```

and the one line inside `_splice` that reads them:

```python
    lines = _lines(source)
```

The case that pins it, appended to `tests/test_arm_check.py` — seen red
against `source.splitlines(keepends=True)`, where it is `IndentationError`:

```python
def test_a_form_feed_does_not_move_the_line_an_arm_is_spliced_on():
    """`str.splitlines` splits on eight separators `ast` does not count.

    A form feed is the realistic one — it is a conventional page break in
    Python source. Split on it, `span.lineno` and the list index part company,
    and every arm below it comes back as an un-asked pair with an
    `IndentationError` beside it: the enumeration going short through a door
    `test_every_ast_constructor_is_classified` cannot see.

    Red how: `_lines` replaced by `source.splitlines(keepends=True)` raises
    `IndentationError` here. Executed."""
    source = "def f(a, b):\n\x0c\n    if a and b:\n        return 1\n    return 0\n"
    first, second = ARM.arms(source)
    assert first.source == "a", "the span itself is right either way"
    assert "if not (a) and b:" in ARM.mutate(source, first)
    assert "if a and not (b):" in ARM.mutate(source, second)
    for arm in (first, second):
        ast.parse(ARM.mutate(source, arm))
        ast.parse(ARM.mutate(source, arm, "remove"))
```

Finding 4 — `tests/test_a_segment_feeds_the_flow_log.py`, replacing the
assertion at lines 562-569:

```python
    assert (
        "batching is the ordinary way in and a background command is the "
        "rarer one" in body.lower()
    ), (
        "batching is the ordinary way a share passes 100% and the background "
        "command the rarer one; naming the two separately passes with the "
        "ranking reversed, which is the edit this case exists to stop. "
        "Lowered for the same reason the negative below is: the clause's "
        "POSITION in its sentence is not the claim, so prefixing the "
        "sentence leaves the ranking and the direction intact and must not "
        "turn this red"
    )
```

Finding 5 — `skills/verify/SKILL.md`, the operator table and one sentence
after it:

```markdown
**There are two ways to be wrong and the counts differ by a lot**, so the
report keeps them apart and the number you quote has to say which one it is:

| Operator | Asks | Measured 2026-09-09 on `hooks/review-history-guard.py` |
|---|---|---|
| `invert` | would a case notice this test being **backwards** | 1 of 32 survived |
| `remove` | would a case notice this arm being **absent** | 12 of 32 survived |

That third column is a measurement and not a property of the module: it moves
when either the module or `tests/test_chain_hooks.py` changes, which is the
rot this checker exists to end. Re-take it with the command above rather than
reading it as current — a number in a document is exactly what #262 says goes
stale.
```

Finding 6 — `skills/verify/scripts/arm_check.py`, in `mutate`, after the
`boolean`/`handler` lines at 561-562 and before the `bare except` refusal:

```python
    if handler and arm.group_without == NEVER_RAISED and operator == "invert":
        # A handler with ONE type: dropping its only member and aiming it
        # elsewhere are the same edit, byte for byte. Asked of both operators,
        # one measurement is reported as two independent answers -- and
        # `main:189` in `hooks/review-history-guard.py`, the arm the report
        # headlines as watched by nothing, is exactly this shape. `remove`
        # keeps it, because #262's table is a removal count. Refused rather
        # than silently skipped, so the pair is NAMED in the report.
        raise NoMutationDefined(
            f"{arm.where}: this handler has one type, so removing it and "
            f"aiming it elsewhere are the same edit. Measured by `remove`, "
            f"which is the row #262's table compares with."
        )
```

Applying this moves `invert`'s row from `32 asked · 31 killed · 1 survived` to
`29 asked · 28 killed · 1 survived`, so `skills/verify/SKILL.md`,
`phases/phase-3.md`, `phases/phase-4.md` and the ledger fragment's fourth row
each re-state one number. That cost is the reason this is the finding most
open to being answered with grounds instead — the lighter alternative is to
leave both operators asked and have `_report` say the pair is one measurement.

Finding 7 — `skills/verify/scripts/arm_check.py`, a helper beside `counts`:

```python
#: Node types excluded from the walk by DECLARATION rather than because they
#: carry no branch: `NOT_ARMS` gives the grounds for each. A module whose
#: branching lives in these reads as fewer arms than it holds, so the report
#: names them where it prints the total -- the grounds are in the source and
#: the report is what a person reads.
DECLARED_EXCLUSIONS = ("Assert", "For", "AsyncFor")


def excluded_counts(source: str) -> dict[str, int]:
    """How many declared-exclusion nodes this module actually holds."""
    out: dict[str, int] = {}
    for node in ast.walk(ast.parse(source)):
        name = type(node).__name__
        if name in DECLARED_EXCLUSIONS:
            out[name] = out.get(name, 0) + 1
    return out
```

and in `_report`, after the per-scope lines:

```python
    if excluded:
        echo("")
        echo(
            "  Excluded by declaration and NOT in the total above: "
            + " · ".join(f"{n} {c}" for n, c in sorted(excluded.items()))
        )
        echo(
            "  #262's rule does not count them and `NOT_ARMS` carries the "
            "grounds. An"
        )
        echo("  `assert` IS a test a mutation could flip.")
```

Finding 8 — `skills/verify/scripts/arm_check.py`, `_report`'s header. Keyword-only
with a default, so the four cases that call `_report` positionally stay green:

```python
def _report(path, verdicts, refused, counted, echo, *, of_total=None):
    echo("")
    shown = sum(counted.values())
    if of_total is not None and of_total != shown:
        # `--only` filtered this. The line names a file and gives a total, so
        # it reads as the file's total -- and this output gets pasted into
        # records, where the flag that produced it does not travel with it.
        echo(f"{path} — {shown} of {of_total} arms (--only)")
    else:
        echo(f"{path} — {shown} arms")
```

with both call sites in `main` passing the unfiltered total. The listing
branch:

```python
    if not args.tests:
        every = arms_of_file(args.module)
        found = [a for a in every if a.scope == args.only] if args.only else every
        for arm in found:
            echo(f"  {arm}")
        _report(args.module, [], [], counts(found), echo, of_total=len(every))
        return 0
```

and the mutating branch, where the total has to be taken before `--only`
narrows it. This block already carries finding 1's `timeout=` argument, so it
replaces rather than joins the `run_arms` call shown there:

```python
    every = arms_of_file(args.module)
    verdicts, refused = run_arms(
        args.module,
        shlex.split(args.tests),
        only=args.only,
        cwd=args.cwd or os.getcwd(),
        timeout=args.timeout or None,
        echo=echo,
    )
    found = [v.arm for v in verdicts] + [a for a, _ in refused]
    _report(args.module, verdicts, refused, counts(found), echo, of_total=len(every))
```

Finding 9 — `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md`,
lines 5-6:

```markdown
· evidence: `seal/ledger/1788936260-a-case-pins-what-it-actually-measures.md` — 6 rows
· verified: executed — 35 cases in `tests/test_arm_check.py`, each seen red against a mutation of the checker; the #310 case red on all five of its arms and green unmutated; the checker's first run over `hooks/review-history-guard.py`. Read — #262's and #310's bodies, and the two commits the ticket's table predates. Unverified — the full suite, the repository-wide lint and the typecheck (contract §2: the orchestrator's, once, after the rounds), and every platform but macOS.
```

Finding 10 — `tests/test_arm_check.py`, the sentence inside
`test_the_run_leaves_no_bytecode_cache_behind`'s docstring:

```python
    **This property has two mechanisms behind it and either one alone
    satisfies it** — the per-arm `clear_bytecode_cache` and the subprocess's
    `PYTHONDONTWRITEBYTECODE`. So the env var is an arm no case kills. It is
    kept for one narrow path: `run_arms` builds the child's environment from
    `dict(os.environ)`, so the subprocess cannot differ from this process
    through the environment — only a `--tests` command that sets
    `PYTHONPYCACHEPREFIX` itself puts the cache somewhere the clear does not
    look. Named here rather than pinned, because pinning the second mechanism
    separately would pin the implementation and not the claim."""
```

Needs a fix: yes — findings 1 and 2 (`arm_check.py:745`: no timeout on the arm command, and a spawn failure discarding every measured verdict), 3 (`arm_check.py:520`: `str.splitlines` mis-indexing a splice), 4 (`test_a_segment_feeds_the_flow_log.py:562`: the clause-2 assertion pinning sentence position, verified red on an edit that changes no word of the clause), 5 (`SKILL.md:80`: two undated hand-taken numbers in durable prose), 6 (`arm_check.py:589`: one measurement reported as two operator rows), 7 (`arm_check.py:233`: the declared exclusions invisible in the report) and 8 (`arm_check.py:787`: `--only` mis-stating the module's total). Finding 9 is paperwork and finding 10 is one clause, so neither counts here.

Loses a record or crashes: yes — `skills/verify/scripts/arm_check.py:745`. `OSError` from `subprocess.run` is caught nowhere, so a `--tests` command that cannot be spawned, or one that stops being spawnable partway through, raises out of `run_arms` and `_report` is never reached: executed on a three-arm fixture with `subprocess.run` made to fail on its third call, the two verdicts already measured were discarded and nothing was printed. Nothing leaves the tree — the module is restored on that path and on every other one I read, `KeyboardInterrupt` included — and the working-tree loss in finding 1 needs a signal no `finally` sees, so it is not this line's answer.

## Proof

Files opened, all in a `git clone --no-local` at `47118c1` unless noted:

- `skills/verify/scripts/arm_check.py` — read in full, 909 lines
- `tests/test_arm_check.py` — read in full, 1016 lines
- `tests/test_a_segment_feeds_the_flow_log.py` — the diff hunk in full, plus lines 1-115 for `read`, `section_body` and `section_text`
- `skills/verify/SKILL.md` — the diff hunk in full, plus the paragraph at lines 470-484 that the #310 case reads
- `bin/arm-check`, `bin/arm-check.cmd`, `bin/survivor-check`, `bin/survivor-check.cmd`, `bin/test` — all read in full
- `hooks/review-history-guard.py` — its `ExceptHandler` shapes enumerated by script; not read line by line
- `seal/ledger/1788936260-a-case-pins-what-it-actually-measures.md` — all 6 rows
- `seal/specs/1788936260-a-case-pins-what-it-actually-measures/` — `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`, `survivors.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md` (heads and tail), `phases/phase-3.md`, `phases/phase-4.md`
- `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` — lines 25-165, for the class-level `bin/` cases
- `.github/workflows/test.yml` — lines 20-60, for the interpreter matrix
- `CLAUDE.md` (repository root) and the user-level `CLAUDE.md`, for the conventions the diff is checked against

Not opened: `handoff.md` was read only for what it claims about the branch's
state; it is prose added at `47118c1` and nothing in this report rests on it.
`#262` and `#310` themselves were not fetched — the spawn prompt labels the
ticket's table of 33 as read-not-executed and `questions.md` assumption 3 puts
it out of scope, so no finding here depends on the ticket's own text.
