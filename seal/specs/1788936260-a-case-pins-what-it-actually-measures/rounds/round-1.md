# 1788936260-a-case-pins-what-it-actually-measures — review round 1

| Field | Value |
|---|---|
| Target SHA | 47118c1 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 311 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | run_arms → round-1-report.md, round-1.md, main, pytest; _report → round-1-report.md, round-1.md, main, pytest |
| New units | DECLARED_EXCLUSIONS (depth 1); _LINE_END (depth 1); _lines (depth 1); TWO_SCOPES (depth 1); DECLARED (depth 1); test_the_declared_exclusions_are_named_where_the_total_is_printed (depth 1); test_every_declared_exclusion_is_classified_as_a_non_arm (depth 1); test_a_filtered_run_does_not_state_its_count_as_the_modules_total (depth 1); NOT_LINE_ENDS (depth 1); _TWO_ARM_SOURCE (depth 1); SPLICE_FIXTURES (depth 1); _PLAIN (depth 1); test_a_separator_the_tokenizer_ignores_does_not_move_a_spliced_arm (depth 1); test_a_command_that_never_returns_is_recorded_as_unmeasured (depth 1); test_a_spawn_failure_keeps_the_verdicts_already_measured (depth 1); test_the_skill_calls_its_survivor_counts_a_measurement_and_not_a_property (depth 1); test_a_sole_type_handler_is_measured_by_one_operator_and_not_by_both (depth 1) |
| Needs a fix | yes — findings 1 and 2 (`arm_check.py:745`: no timeout on the arm command, and a spawn failure discarding every measured verdict), 3 (`arm_check.py:520`: `str.splitlines` mis-indexing a splice), 4 (`test_a_segment_feeds_the_flow_log.py:562`: the clause-2 assertion pinning sentence position, verified red on an edit that changes no word of the clause), 5 (`SKILL.md:80`: two undated hand-taken numbers in durable prose), 6 (`arm_check.py:589`: one measurement reported as two operator rows), 7 (`arm_check.py:233`: the declared exclusions invisible in the report) and 8 (`arm_check.py:787`: `--only` mis-stating the module's total). Finding 9 is paperwork and finding 10 is one clause, so neither counts here. |
| Loses a record or crashes | yes — `skills/verify/scripts/arm_check.py:745`. `OSError` from `subprocess.run` is caught nowhere, so a `--tests` command that cannot be spawned, or one that stops being spawnable partway through, raises out of `run_arms` and `_report` is never reached: executed on a three-arm fixture with `subprocess.run` made to fail on its third call, the two verdicts already measured were discarded and nothing was printed. Nothing leaves the tree — the module is restored on that path and on every other one I read, `KeyboardInterrupt` included — and the working-tree loss in finding 1 needs a signal no `finally` sees, so it is not this line's answer. |

- [x] Pass

## What this round was asked

Round 1 of `fix/262-310-a-case-pins-what-it-actually-measures`, target
`47118c1`, base `origin/release/v0.9.5` (`0df9508`), draft PR #311. First
round: no verdict is inherited. Built by `specseal:smith`, and the
implementer's report has been verified by nobody.

**Ten things this round was told to try to break, in this order.** The first
five are where the diff's own argument would fail; #262's whole point is that
a checker whose enumeration goes short is worse than no checker.

1. **The classification is claimed total over the grammar** —
   `arm_check.py#ARM_SHAPES`/`NOT_ARMS`, pinned at
   `tests/test_arm_check.py#test_every_ast_constructor_is_classified`. Derive
   the constructor set yourself and check both directions. Then judge the
   *declared exclusions* rather than the totality: `Assert`, `For`/`AsyncFor`
   are excluded with grounds in `NOT_ARMS`, and an exclusion that is wrong
   makes the walk go short while the totality case stays green.
2. **The top-level-versus-flattened boolean member rule** — the ledger's
   second row says top-level members, `gh_segments` 5 not 7. Is the same rule
   applied by the counter *and* by the mutator, so the arm the report names is
   the member the mutation changed?
3. **The restore path.** Byte-for-byte restore is claimed, verified by hash,
   after every arm. Is it guaranteed on an exception, a `SyntaxError` from the
   mutation itself, a non-zero test command, and a `KeyboardInterrupt`? A
   checker that returns leaving the module mutated is the floor question for
   this diff — that is a working tree lost, not a finding.
4. **The bytecode cache clear** — `arm_check.py#clear_bytecode_cache`. Is the
   cache cleared for the target module only, or for everything the test
   command imports? Does it honour `sys.pycache_prefix`? What happens when the
   `__pycache__` directory is read-only or absent?
5. **Skip versus refuse, which is the module's own subject.** Does every
   arm × operator pair reach a named outcome, and does the report's arithmetic
   account for all of them? The first run printed `remove 31 asked` against 32
   arms — that defect is claimed fixed twice over (`Verdict#not_applicable`,
   `_report`). Try to construct a third path where a pair falls out of a
   denominator unnamed.
6. **The subprocess running `--tests`.** Shell or argv, `cwd`, `check=`,
   timeout, encoding, what a crafted `--tests` string or module path reaches,
   and whether a hung command is bounded. `code-review`'s own probe rule was
   written after a 68-minute hang.
7. **#310's replacement assertions** —
   `tests/test_a_segment_feeds_the_flow_log.py#test_the_section_names_batching_as_the_way_a_share_passes_one_hundred`
   over `skills/verify/SKILL.md`. Two questions, not one: does the whole-clause
   assertion pin the *claim* (the ranking and the direction), and does it now
   **over**-pin — would a legitimate re-wrap or a harmless rewording break it?
   `section_body()`'s whitespace collapse is the load-bearing part.
8. **What a person reads.** `arm-check`'s report text and refusal text are new
   output. Contract §14: is each pinned by a case, and does the report's own
   sentence about *a survivor is not automatically a defect* and about which
   operator row #262 compares with actually appear in the code rather than only
   in the changelog fragment?
9. **`bin/arm-check` and `bin/arm-check.cmd`.** Transcribed from
   `bin/survivor-check`/`.cmd` and **the `.cmd` has not been run**. Compare
   argument passing, quoting and exit-code propagation against the sibling
   pair.
10. **The records.** `overview.md`'s evidence line says the ledger fragment
    carries **4 rows**; `seal/ledger/1788936260-…md` carries **6**
    (orchestrator-executed, `grep -c '^| '` = 7 including the header). Judge
    that and sweep the four `phases/phase-N.md`, `plan.md`'s phase table and
    `overview.md` for the same class — a record stating a count of something
    the diff contains.

**Two axes to add to the table for this round**, beyond the standard ten:
**process and filesystem lifetime** (what is left behind when the run dies
mid-arm — the mutated module, a `__pycache__`, a temp file) and **the
instrument measuring itself** (the checker reports two of its own arms as
unwatched; is that report true, and is the exemption reasoning in
`phases/phase-3.md` sound or circular?).

**Facts handed over as coordinates, each labelled.** Executed by the
orchestrator in this session: the ledger fragment's row count above. Executed
by the implementer and **not** re-run here — treat as claims with coordinates
to open, per contract §5: `invert` 32 asked · 31 killed · 1 survived and
`remove` 32 asked · 20 killed · 12 survived over
`hooks/review-history-guard.py` against `tests/test_chain_hooks.py`; 122 AST
constructors classified; the per-function split `reader` 5 · `is_closed` 4 ·
`gh_segments` 5 · `main` 17. Read, not executed: #262's table of 33 and the two
commits (`341be0b`, `1dedd1e`) that postdate it — `questions.md` assumption 3
leaves the ticket as written, so a finding that the ticket is wrong is out of
scope; a finding that *this diff* mis-states the relationship is in.

**Out of scope, decided before the round.** What `arm-check`'s exit code should
mean (`questions.md` Q1, the owner's, report-only today and pinned by a case);
whether the twelve survivors are gaps (Q2); a sweep of the tree for other
cases that pin a document clause by substring (#310's inherited row).

**Run the unscoped `evidence_check.py .` read** — no `--ledger` — so a row this
branch may have falsified elsewhere is visible. The broad gate is not this
round's: contract §2, the orchestrator's, once, after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A hung `--tests` command is unbounded, and a kill during the hang leaves the module mutated with no copy on disk | `skills/verify/scripts/arm_check.py:745` | **fixed** `7b48498` | fixed at 7b48498 — the bound on the arm's command. The kill-loses-uncommitted-work half is mechanism a fix pass may not add and went to #312, recorded in Deferred; Read: no `timeout` argument; every ordinary path and `KeyboardInterrupt` restore, verified across both `finally` blocks. No `finally` sees `SIGKILL` |
| 2 | A `--tests` command that cannot be spawned raises out of `run_arms`, discarding every verdict measured so far and printing no report | `skills/verify/scripts/arm_check.py:745` | **fixed** `7b48498` | fixed at 7b48498; Executed: a nonexistent command raises `FileNotFoundError`; `subprocess.run` made to raise on its third call discarded two measured verdicts |
| 3 | `_splice` uses `str.splitlines`, which splits on separators `ast` does not, so one form feed files every arm below it as an unasked pair | `skills/verify/scripts/arm_check.py:520` | **fixed** `d4209bd` | fixed at d4209bd — the row it stands on was re-read and re-stamped at 33be6ca, after the pin was widened; Executed: spans correct, `mutate` raises `IndentationError`; the proposed `_lines` is `OK` on all five separator cases (NAME NOT IN TREE — the fix below defines it) |
| 4 | #310's clause-2 assertion is case-sensitive on its first letter, so it pins the clause's sentence position | `tests/test_a_segment_feeds_the_flow_log.py:562` | **fixed** `facac61` | fixed at facac61; Executed: `In practice, ` inserted before the clause, ranking and direction intact, exit 1. Lowering both sides leaves arms A and B red and arm C green |
| 5 | The new skill section writes `1 of 32` and `12 of 32` into durable prose with no date, no SHA and no case | `skills/verify/SKILL.md:80` | **fixed** `5b55671` | fixed at 5b55671; Executed: numbers reproduced and correct today. Read: no test in `tests/` reads that section |
| 6 | For a sole-type `except`, `invert` and `remove` produce identical text, so the two operator rows report one measurement twice — including for the headlined survivor `main:189` | `skills/verify/scripts/arm_check.py:589` | **fixed** `5b55671` | fixed at 5b55671 — applied rather than answered; re-measured by the orchestrator at c37e909 in a separate clone; Executed: the two mutations compare equal; three such arms in the guard, one of them the single survivor |
| 7 | `Assert`, `For` and `AsyncFor` are excluded by declaration and the report never says so, so `N arms` reads as the module's branch count | `skills/verify/scripts/arm_check.py:233` | **fixed** `125bae0` | fixed at 125bae0 — the smaller fix, which names the declared exclusions statically and adds no second walk; Executed: a module with an assert pair and a `for`/`else` reports `1 arms`. The grounds for the exclusions themselves hold |
| 8 | `--only` makes the report header state the filtered count as the module's total | `skills/verify/scripts/arm_check.py:787` | **fixed** `125bae0` | fixed at 125bae0; Executed: `--only reader` prints `— 5 arms` for a 32-arm module |
| 9 | `overview.md` says 4 ledger rows against 6, and 26 cases against 35; both sibling phase records are correct | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:5` | answered | corrected at 5b55671 |
| 10 | The `PYTHONDONTWRITEBYTECODE` self-report is true; the reason given for keeping it names a path `dict(os.environ)` makes narrower | `tests/test_arm_check.py:744` | answered | corrected at 5b55671 |
| 🟢 11 | Grammar totality, both directions, on two interpreters | `skills/verify/scripts/arm_check.py:87` | answered | Executed: 122 classified, 122 derived, empty both ways, no overlap, on CPython 3.12.11 and 3.13.9 |
| 🟢 12 | The two `bin/` wrappers are faithful transcriptions and are already pinned class-level | `bin/arm-check.cmd:7` | answered | Executed: non-comment diff against the sibling pair differs in the script path alone; `test_every_posix_wrapper_resolves_its_own_directory[arm-check]` collects, and the `.cmd`-twin case enumerates `bin/` — 53 passed |
| 🟢 13 | The run leaves no mutated module, no bytecode for the target and no temp file | `skills/verify/scripts/arm_check.py:767` | answered | Executed: clone `git status` empty after 64 mutations; `hooks/__pycache__` holds no `review-history-guard` entry |
| 🟢 14 | This branch falsifies no ledger row elsewhere | `seal/ledger.md` | answered | Executed: `evidence_check.py .` unscoped, exit 0, `1056 ok · 0 drifted · 0 broken`. An earlier reading showed one DRIFTED row and was my own concurrent mutation of the guard, not a finding |

## Paste-ready fixes

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
```python
    lines = _lines(source)
```
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
```python
    if not args.tests:
        every = arms_of_file(args.module)
        found = [a for a in every if a.scope == args.only] if args.only else every
        for arm in found:
            echo(f"  {arm}")
        _report(args.module, [], [], counts(found), echo, of_total=len(every))
        return 0
```
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
```markdown
· evidence: `seal/ledger/1788936260-a-case-pins-what-it-actually-measures.md` — 6 rows
· verified: executed — 35 cases in `tests/test_arm_check.py`, each seen red against a mutation of the checker; the #310 case red on all five of its arms and green unmutated; the checker's first run over `hooks/review-history-guard.py`. Read — #262's and #310's bodies, and the two commits the ticket's table predates. Unverified — the full suite, the repository-wide lint and the typecheck (contract §2: the orchestrator's, once, after the rounds), and every platform but macOS.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| What `arm-check`'s exit code should mean | `questions.md` Q1 — already deferred, report-only today and pinned by `test_the_checker_is_report_only_and_exits_zero_over_the_real_module` | the repository owner |
| Whether the twelve `remove` survivors are gaps | `questions.md` Q2 — already deferred, with `phase-4.md:38`'s table of the twelve as the input | a later work item |
| A sweep of the tree for other cases pinning a document clause by substring | #310's inherited `Not verified` row and `overview.md:32` — already deferred, and out of scope for this round by the spawn prompt | whoever builds that sweep; #310 stays open on it |
| #262's table of 33 left as written | `questions.md` assumption 3 — already deferred | nobody; a deliberate refusal |
| **Finding 1's second half** — a run killed mid-arm loses uncommitted work in the module under check, because the only copy of it is in the dead process's memory. The bound on the arm's command is fixed at `7b48498`; this is the sidecar copy the paste-ready block proposed | **#312**, opened by the fix pass. It is mechanism a fix pass may not add — a new on-disk protocol with its own failure modes, and at least four things somebody has to decide: who removes a left-behind sidecar, how a live one is told from a dead one, how *the run leaves no mutated module and no temp file* (finding 13, executed) becomes conditional, and where the copy goes when the module's directory is not writable. #312 also carries the smaller answer to cost first — refuse to run at all over a module carrying uncommitted edits, since that is the only case where anything is lost | the repository owner, at #312 |
| The full suite, repository-wide lint and typecheck | contract §2: the broad gate is the orchestrator's, run once after the rounds settle. Nine narrow modules were run in this round and are labelled above; `ruff` is not installed in the clone's virtual environment | **the review orchestrator** |
| Windows and Linux | `overview.md:29` — already deferred. `bin/arm-check.cmd` has been run by nobody; its equivalence to a sibling that has been run is **read**, not executed | CI's windows and linux legs |
