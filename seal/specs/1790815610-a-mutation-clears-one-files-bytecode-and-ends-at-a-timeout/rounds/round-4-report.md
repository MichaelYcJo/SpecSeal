# 1790815610 — review round 4 report

Round 4 is the verifying round after the run's one reopening, so the run ends
here whatever it finds. Target `a86101f5332420645509eb65f545e88f534a639e`; the
diff verified is round 3's fix range
`db15439f629ba387423900385cad04b6f6247af2..37b3646f8b7f9a69d516adfac3b36791560937bb`
(`647c3395`, `37b3646f`). Worked in a `git clone --no-local` at the target;
the clone, the probes and their outputs were removed before handing over.

What round 3's record and the fix commits assert was read as claims and
checked against the code and by execution. Round 3's coordinates were carried;
none of its verdicts were.

## Round 3's three verdicts

**Round 3's finding 15 is closed, with its class.** `mutation_run` now opens
the restore's `try` before the baseline (`skills/verify/scripts/mutation_check.py:325`),
so every exit from the baseline on passes the compare-then-restore guard at
`:360-366`. Re-run of P5 in process (the first `_wait` interrupted after cases
that write `VALUE = 99`): exit 2, the interrupt line, the file back at
`VALUE = 1`. Re-run with a real signal as well: a `SIGINT` to the wrapper's
process group while the baseline's cases slept after writing `VALUE = 99`.
The file read `VALUE = 99` while they ran; the wrapper exited 2 within 0.3 s
with *holds the bytes it held before the command started*, the file was back
at `VALUE = 1`, and the cases' process was gone. So the printed line is true.
The class is the interrupt line's claim, and that line is the only printed
line that says what the file holds; it holds wherever the interrupt lands.

The case that pins it, the `baseline` parameter of
`test_an_interrupt_ends_the_run_it_started_and_restores_the_file`
(`tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py:1199-1277`),
fails on the defect it pins. Ma put back round 3's reach (the restore skipped
unless the baseline had passed), and that parameter alone went red.

**Round 3's note 16 is closed.** Both assertions now read
`. This was the run against the file as it is, before the mutation was written`
(`:808-811`, `:1107-1110`). M6 put round 2's clause form back, and the
cannot-start case and the bound case's `[baseline]` parameter both went red.
In round 3 the same mutation SURVIVED the whole module.

**Round 3's correction 17 is answered.** L2's orchestrator note ends *so the
claim holds.* and the round 3 note opens in bold after it. Every other note
boundary in L1, L3, L4 and L7 has its full stop too (read).

## The `no baseline` sentence in every baseline exit

*The break was never written* is printed only by `no baseline`
(`mutation_check.py:331-337`), and it is true there by construction: that
return comes before the write at `:347`. Each baseline exit was executed
through `bin/mutation-check`, with cases that write `VALUE = 99` to the target
first:

| Baseline exit | Printed | File after |
|---|---|---|
| red (cases exit 1) | `no baseline: … (exit 1) … The break was never written` | `VALUE = 1` |
| red, cases touch nothing (exit 5) | the same with `(exit 5)` | `VALUE = 1`, mtime unchanged, so nothing was written back |
| timed out (`--timeout 1`) | `timed out after 1s: … . This was the run against the file as it is, before the mutation was written` | `VALUE = 1` |
| cannot start | `could not start: FileNotFoundError … . This was the run …` | `VALUE = 1` |
| interrupt | `interrupted: … holds the bytes it held before the command started.` | `VALUE = 1` |

Md put *Nothing was written* back, and all three parameters of
`test_cases_that_fail_without_the_mutation_measure_nothing` went red. The
sentence is pinned.

## L2's note, and the fragment's other round 3 notes

L2's round 3 note says *Ctrl-C ends the group before the restore* now holds
in the baseline too. It does: `run_cases`' interrupt arm calls `_end` before
it re-raises (`:262-264`), and the restore is the `finally` above it. The
real-signal probe saw the cases' process gone. The notes of L1, L3, L4 and L7
match the diff. L7's *putting the clause form back and putting Nothing was
written back each turned a case red* is reproduced by M6 and Md.

## Findings — all from this round, all ⬜

Three things the fix left. None of them leaves a printed line false, so none
needs a fix. The reopening bound lets this record commission nothing, so each
one goes to the ladder (see Deferred).

**⬜ 18 — the restore after a `no baseline` exit and after a baseline timeout
is held by no case** (`mutation_check.py:365`, executed). The fix's comment at
`:319-324`, the no-baseline case's comment at `tests/…:637-639`, and L3's and
L7's round 3 notes all say the restore now puts back what the baseline's cases
changed, on every exit. Only the interrupt exit is pinned. Mb skipped the
restore after a `no baseline` exit only, and Mc after a baseline timeout only
(each added `and locals().get("before") != …` to the guard). Both SURVIVED the
whole module. The behaviour is right at the target, as the table above shows,
and no printed line claims it, so this is a regression case to plant. The
case under Paste-ready fixes was green at the target, red under Mb on its
`no-baseline` parameter, and red under Mc on its `timed-out` parameter.

**⬜ 19 — `main`'s interrupt comment still says an interrupt in the baseline
wrote nothing** (`mutation_check.py:445-450`, read). It says the `finally`
restored the file *when the break had been written*, and that *an interrupt
during the baseline wrote nothing*. Since `647c3395` the cases may have
written the file during the baseline, and the `finally` puts that back too.
The comment is the reasoning a later edit will read for this arm. It is in
the class the fix pass enumerated, the sentences that said the baseline
writes nothing, and it was not in the enumeration.

**⬜ 20 — `not restored` is described as a file that may still hold the
break, and a baseline exit can now reach it** (`skills/verify/SKILL.md:157-158`,
`mutation_check.py:39`, executed). Cases that write `VALUE = 99`, make the
target `0o400` and exit 1 used to print `no baseline` over a rewritten file.
Now they print `not restored: … writing it back raised PermissionError …
Restore it from your own commit`, exit 2, file `VALUE = 99`. The printed line
is true, and the action it asks for is the right one. The two descriptions
say the file *may still hold the break* (*the mutation*), where on this exit
the break was never written and the file holds what the cases wrote.

## Regression tests to plant

- `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`,
  beside `test_cases_that_fail_without_the_mutation_measure_nothing`: the
  two-parameter case in the first fence below (⬜ 18). Seen red under Mb and
  under Mc, as stated above.

## Facts for the evidence ledger

- L3 or L7 could name the case above once it is planted. Until then, *the
  restore puts back what the baseline's cases changed* is true at the target
  (executed) and is pinned only for the interrupt exit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 3's finding 15 is closed — an interrupt in the baseline leaves the file as the line says, and the restore covers every baseline exit | `skills/verify/scripts/mutation_check.py:319-378` | confirmed | Executed: P5 in process and P5 with a real SIGINT to the wrapper's group, each exit 2 with the interrupt line and the file back at `VALUE = 1`; Ma (round 3's reach put back) red on the interrupt case's `[baseline]` alone |
| 🟢 | round 3's note 16 is closed — the suffix's sentence boundary is pinned in both cases that reach it | `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py:808-811`, `:1107-1110` | confirmed | Executed: M6 (round 2's clause form) red on the cannot-start case and on the bound case `[baseline]`; it survived the module in round 3 |
| 🟢 | round 3's correction 17 is answered — L2's note has its full stop and bold opening | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L2 | confirmed | Read: every note boundary in L1, L2, L3, L4 and L7 ends in a full stop |
| 🟢 | `The break was never written` is true in every baseline exit, and pinned | `skills/verify/scripts/mutation_check.py:325-346` | confirmed | Executed: red, timed out, cannot start and interrupt, each with cases that rewrite the target; the file ended `VALUE = 1` each time; Md red on all three no-baseline parameters |
| 🟢 | L1, L2, L3, L4 and L7's round 3 notes are true of the fix range | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` | confirmed | Read against the diff; L7's two mutations reproduced as M6 and Md |
| ⬜ 18 | The restore after a `no baseline` exit and after a baseline timeout is held by no case; only the interrupt exit is pinned | `skills/verify/scripts/mutation_check.py:365` | open | Executed: Mb and Mc SURVIVED the module; the proposed case was green at the target and red under each. Behaviour right, no printed line claims it |
| ⬜ 19 | `main`'s interrupt comment still says an interrupt in the baseline wrote nothing, and that the restore runs only once the break was written | `skills/verify/scripts/mutation_check.py:445-450` | open | Read: false since `647c3395`; a comment, so no line a person reads changes |
| ⬜ 20 | `not restored` is described as a file that may still hold the break, and a baseline exit whose restore fails now reaches it | `skills/verify/SKILL.md:157-158`, `skills/verify/scripts/mutation_check.py:39` | open | Executed: cases that rewrite and chmod the target, then exit 1, print `not restored`, exit 2, file `VALUE = 99`; the printed line is true and asks for the right act |
| 🟢 | The ledger holds unscoped | the whole tree | confirmed | Executed: `bin/evidence-check .` exit 0, 3223 ok, 0 drifted, 0 broken |

## Paste-ready fixes

### ⬜ 18 — the regression case

```python
@pytest.mark.parametrize(
    ("tail", "verdict", "extra"),
    [
        ("sys.exit(1)\n", "no baseline", []),
        ("import time\ntime.sleep(30)\n", "timed out after 1s", ["--timeout", "1"]),
    ],
    ids=["no-baseline", "timed-out"],
)
def test_a_baseline_whose_cases_rewrite_the_file_leaves_its_first_bytes(
    tmp_path, capsys, tail, verdict, extra
):
    """Round 4: the restore covers the baseline (round 3, finding 15), so a
    baseline that ends without a verdict puts back what its cases wrote, on
    every exit and not only on an interrupt."""
    target = tmp_path / "under_test.py"
    original = b"VALUE = 1\n"
    target.write_bytes(original)
    rewrites = probe(
        tmp_path,
        "import sys\n"
        "with open(sys.argv[1], 'w', encoding='utf-8') as f:\n"
        "    f.write('VALUE = 99\\n')\n" + tail,
        "rewrites.py",
    )
    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(rewrites, target),
            *extra,
        ],
        capsys,
    )
    assert code == 2, out
    assert out.startswith(verdict), out
    assert target.read_bytes() == original, "the baseline's write was left on disk"
```

### ⬜ 19 — `main`'s interrupt comment

```python
    except KeyboardInterrupt:
        # Reached only after `run_cases` ended what it started and
        # `mutation_run`'s `finally` put back any bytes that differ -- the
        # break, or what the baseline's cases wrote before any break existed
        # (round 3, finding 15). A failed restore raises `NotRestored` instead,
        # and is reported above, so the sentence holds wherever the interrupt
        # lands.
```

### ⬜ 20 — what `not restored` says

```text
skills/verify/SKILL.md:
  start`, `could not run`, `refused` (nothing was written), `not restored`
  (the file may still hold the break, or what the cases wrote; restore it
  from your commit), and `interrupted`.

skills/verify/scripts/mutation_check.py, the verdict table:
  not restored     exit 2   the file may not hold its first bytes; restore it
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the module, `-q -p no:xdist`, at the target | exit 0; 40 passed |
| P5 in process: the first `_wait` waits, then raises `KeyboardInterrupt`; cases write `VALUE = 99` | `interrupted: … holds the bytes it held before the command started.`, exit 2; file `VALUE = 1` |
| P5 with a real signal: `bin/mutation-check` in its own session, cases write `VALUE = 99` and sleep 30 s, `SIGINT` to the wrapper's group | file `VALUE = 99` during the baseline; the same line, exit 2, 0.3 s after the signal; file `VALUE = 1`; the cases' process gone |
| The wrapper, cases write `VALUE = 99` then exit 1 | `no baseline: … (exit 1) … The break was never written`, exit 2; file `VALUE = 1` |
| The wrapper, cases write `VALUE = 99` then sleep 30 s, `--timeout 1` | `timed out after 1s: … This was the run against the file as it is, before the mutation was written`, exit 2, 1.0 s; file `VALUE = 1` |
| The wrapper, a runner that does not exist | `could not start: FileNotFoundError … This was the run …`, exit 2; file `VALUE = 1` |
| The wrapper, cases that touch nothing and exit 5 | `no baseline: … (exit 5) …`, exit 2; file `VALUE = 1`, mtime unchanged |
| The wrapper, cases write `VALUE = 99`, make the target `0o400`, exit 1 | `not restored: … writing it back raised PermissionError … Restore it from your own commit …`, exit 2; file `VALUE = 99` (⬜ 20) |
| `bin/mutation-check` on `mutation_check.py`, whole module `-q -p no:xdist`: Ma the restore skipped unless the baseline passed (round 3's reach) | red: the interrupt case `[baseline]` alone |
| The same: Mb the restore skipped after a `no baseline` exit only | SURVIVED (⬜ 18) |
| The same: Mc the restore skipped after a baseline timeout only | SURVIVED (⬜ 18) |
| The same: M6 the suffix back to round 2's clause form | red: the cannot-start case and the bound case `[baseline]` |
| The same: Md *Nothing was written* back | red: the no-baseline case `[failing]`, `[nothing-selected]`, `[usage-error]` |
| The ⬜ 18 case added in the clone, selected alone by its name, at the target | exit 0; 2 passed |
| The same case under Mb, then under Mc | red: `[no-baseline]` under Mb, `[timed-out]` under Mc |
| `git status --porcelain` in the clone after the mutations and after reverting the scratch case | empty |
| `bin/evidence-check .`, unscoped | exit 0; 3223 ok, 0 drifted, 0 broken; records 2 work items read, 0 drifted |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: nobody has run it on this branch. Nothing needing a fix is open after this round, so it has come due, and what comes due is the sealer's spawn |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 18 — the restore after a `no baseline` exit and a baseline timeout is held by no case | rung 4: this record, named in the pull request body; the case is in the paste-ready fixes | nobody has agreed to act on it: the branch owns the unit, and the reopening bound lets this record commission nothing |
| ⬜ 19 — `main`'s interrupt comment says an interrupt in the baseline wrote nothing | rung 4: this record, named in the pull request body | nobody has agreed to act on it, for the same reason |
| ⬜ 20 — `not restored` is described as a file that may still hold the break | rung 4: this record, named in the pull request body | nobody has agreed to act on it, for the same reason |
| `skills/verify/scripts/arm_check.py`'s `run_arms` reads any non-zero exit as killed with no baseline: round 1's finding 1 class (already deferred in round 1, carried in rounds 2 and 3) | a new issue, beside #313 | the orchestrator, who files it when the pull request is opened |

Needs a fix: no

Loses a record or crashes: no

## Proof

Files opened in this round, in the clone at the target unless named:

- `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/rounds/round-3.md`
- `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md`
- `skills/verify/scripts/mutation_check.py` (lines 20-60, 140-479)
- `skills/verify/scripts/arm_check.py` (`restore`, 801-821)
- `skills/verify/SKILL.md` (145-165)
- `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` (595-660, 780-815, 1040-1112, 1195-1277)
- `bin/mutation-check`, `bin/test`
- `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped*, §*The reopening — one, and then the run is capped*, §*Where a leftover goes — the ladder, and why a new issue is not the default*
- `skills/code-review/scripts/round_record.py` (40-90)
- the fix range's diff, `db15439f..37b3646f`
