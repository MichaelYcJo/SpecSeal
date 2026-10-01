# Round 2 report — arm-check reads a run that measured nothing as a kill

Work item `1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill` (#703, draft PR #707).
Verifying round. Target `dc1b0d14`; the diff verified is round 1's fix range
`ac22a0d8..fc833b51`, four commits. Reviewed in a `git clone --no-local` at
the target, under this round's own directory. Coordinates were carried from
`round-1.md`; every verdict below was re-derived at the target. The smith's
account (the commit messages, `overview.md`, the ledger fragment's notes and
the code comments) was read as claims and checked against the code.

## Summary

Round 1's six `fixed` verdicts each hold at the instance they named. Every
round 1 probe the prompt listed was re-run against the target script, and
five of the six come back as asked. The sixth does not: the put-back that
closes round 1's finding 1 only reaches a module the command rewrote or
removed.

1. **A refused first run whose cases leave the module unreadable or
   unwritable now ends in a traceback.** The put-back's own `open` fails, the
   `OSError` leaves the `finally`, and the refusal line and the command's
   output never print. Exit 1. At `6bbaa4d1` the same runs refused cleanly at
   exit 2. So the fix turned a refusal into a crash for this shape. The
   class round 1's finding 1 opened is closed for a rewrite and a removal
   only. 🟡 1.
2. **The smith's R2 is not equivalent.** On a passing run the put-back is
   redundant with the loop's outer `finally`, as claimed. But the put-back
   also covers an interrupt during the first run, which the outer `finally`
   never reaches. Narrowed to a refusal, the put-back survives the whole
   module, and a real SIGINT then leaves the module rewritten. The behaviour
   at the target is right; no case holds it. ⬜ 2.

The smith's departure from round 1's paste-ready block is correct, and the
block it departed from was wrong. R10's survival is as recorded.

## Round 1's verdicts, answered

**Finding 1 (a refusal keeps the cases' rewrite): closed at the instance,
class open.** Executed. A first run that rewrites the module and exits 1
leaves it byte-identical to what was read, at exit 2. The line ends *…and it
was put back from the bytes read before it. No arm was measured.*, which is
true. The same holds for a first run that removes the module, and for both
shapes when the run passes (`--only` selecting nothing). At `6bbaa4d1` the
rewrite stayed and the line said *Nothing was written*. The unreadable shape
is 🟡 1 below.

**Finding 2 (a cp1252 console crashes the refusal): closed.** Executed. Under
`PYTHONIOENCODING=cp1252`, a first run printing `b'\xff'` and exiting 1 gives
exit 2, no `Traceback`, and the command's output follows the line as UTF-8
U+FFFD. Class: the entry block covers both streams of the only process that
prints. `_text` is the one decode of the first run's output, with
replacement.

**Finding 3 (a pair's strict decode drops the run): closed.** Executed. Under
every mutation, a pair whose cases print `b'\xff'` comes back `killed`, exit
0, no traceback. Class: the pair's `text=True` was the last decode of
captured output in `run_arms`. Nothing reads `run.stdout` any more, and the
timeout arm of the loop reads no output.

**Finding 4 (a signal-killed first run held by no case): closed.** Executed.
A first run that SIGKILLs itself gives `no baseline: exit -9.`, exit 2, and
its output follows. Mutation Mg (`!= 0` to `> 0`) is now red on the new
`a run killed by a signal` parameter, and on that alone.

**Finding 5 (a timed-out first run's output reaches no reader): closed.**
Executed. A first run printing then sleeping past `--timeout 1.5` gives the
bound in the line and the printed text below it. Mutation Mi (print only for
an `exit` reason) is now red on
`test_a_first_run_that_timed_out_carries_what_it_printed` alone.

**Finding 6 (the SKILL timeout paragraph): closed.** Read. The new sentence
says the first run is waited for under the same bound and leaks the same
way. That matches `run_arms`, where the first run's `subprocess.run` takes
`timeout=timeout` and nothing reaches past the direct child.

**Round 1's ⬜ 7** stays deferred to #313, as round 1 recorded.

## The smith's departure from the paste-ready block

**Correct, and better than the block.** Read, with the difference executed
through the case. Round 1's block read the module in an inner `finally`
inside the `try` whose `except OSError` reports a spawn failure. A module the
cases removed makes that read raise `FileNotFoundError`. The outer `except`
then reports it as the command failing to start. It sets no `rewrote`, so the
line says *Nothing was written*, and it never puts the module back. The
smith's shape records each outcome in its own `except` and reads and restores
in a `finally` beside them. Mutation Mu (an unreadable module read as
unchanged) is red on the `removes it` parameter, which holds the difference
`overview.md` names.

Its stated reason has a second half, and that half is where 🟡 1 sits. The
comment says the `finally` placement means *an `OSError` from putting the
module back is never read as the command failing to start*. That is true.
But nothing catches that `OSError` at all, so on a refusal it becomes the
run's outcome.

## Findings

### 🟡 1 — a first run that leaves the module unreadable or unwritable ends the refusal in a traceback (`skills/verify/scripts/arm_check.py:958-971`, `:1246-1259`)

**What is wrong.** Executed. The `finally` treats a read that raises
`OSError` as *changed*, with the comment *Removed, or made unreadable: either
way not what was read*. It then calls `restore`. `restore` opens the module
`wb` and reads it back `rb`. Removal is the only `OSError` shape `restore`
can repair.

| What the cases did, then exit 1 | At `6bbaa4d1` | At the target |
|---|---|---|
| `chmod 000` | exit 2, the line, the output; bytes intact | `PermissionError` traceback, exit 1, no line |
| `chmod 200` | exit 2, the line | `PermissionError` on the read-back, exit 1; the bytes were written back but nothing says so |
| rewrite, then `chmod 444` | exit 2, *Nothing was written* (false) | `PermissionError` traceback, exit 1; the rewrite stays |
| replace with a directory | exit 2, the line | `IsADirectoryError` traceback, exit 1 |

**Why it matters.** The prompt's acceptance was that a first run whose cases
make the module unreadable leaves it as it was, and that the refusal's line
is true either way. Neither holds. The line is gone, and so is the
command's own output. That output is the one thing round 1's design put in
front of the person so they can act without re-running. The comment claims
the unreadable shape is handled. The ledger's R1 note says *a module that
cannot be read counting as differing*, which is true of the read and silent
about the put-back.

The passing path (exit 0) crashes in every shape at `6bbaa4d1` and at the
target. That is the loop's first mutation write failing, as it did at the
base. The fix below leaves the passing path and the interrupt path
propagating, as they always have.

**Fix.** Executed on the clone. Catch the put-back's failure. On a refusal,
carry it to the line as the reason the module was not put back. On a pass or
an interrupt, re-raise. With it, all four rows give exit 2, the line names
the error, and the command's output follows. A rewrite and a removal still
say *was put back*. The module went 94 passed, 2 skipped with the two new
cases below, and `ruff check` and `ruff format --check` are clean. The new
case is red at the target, with a `PermissionError` traceback in place of the
line. The SKILL, the changelog fragment and the `bin/arm-check` header each
say what the line now says (§14).

### ⬜ 2 — R2 is not equivalent: the interrupt put-back is held by no case (`skills/verify/scripts/arm_check.py:965-968`)

**Claimed:** the put-back on a passing run is redundant with the outer
`finally`, so a refusal-only put-back survived (the ledger's R1 note and the
round 1 fix pass). **Found:** executed. The mutant
`if changed and refusal is not None:` survives the whole module, 92 passed.
Under it, a real SIGINT two seconds into a first run that had rewritten the
module leaves the module rewritten. At the target the same SIGINT leaves it
byte-identical. The code comment itself names the interrupt (*on a refusal,
and on an interrupt, nothing else does*), and `overview.md` §*Not done* says
an interrupt *leaves the module as it was read*. Both statements are true,
and nothing pins them. The redundancy holds for the pass alone. The
refusal-only mutant also removes the interrupt arm, and that arm has no
second witness.

The behaviour ships right, so this is ⬜. The case in the fixes section turns
red under the mutant and passes at the target. It costs one monkeypatched
call, so it belongs with 🟡 1's fix pass.

### R10 — confirmed as recorded

**Claimed:** `errors="replace"` on stdout is held by no case. Under UTF-8,
only a lone surrogate fails strictly, and one reaches stdout only through a
module path that is not UTF-8, which APFS cannot hold. **Found:** executed. I
tried a second route: a `--tests` naming a path that holds byte `\xff`, so
that the spawn failure's reason carries the surrogate. It does not reach
stdout raw. The `OSError` message reprs the filename, which escapes the
surrogate to ASCII, so `strict` printed the same line at exit 2. `_text`
decodes with replacement and produces no surrogates. So the only route on
this machine is the one the record names. On Linux, where a file name may
hold any byte, a module path with `\xff` would reach the f-string raw. The
ubuntu CI leg could pin it with a skip elsewhere. That is a choice for
whoever next touches the block, not a defect.

## Regression tests to plant

Both go in `tests/test_arm_check.py`, after
`test_a_refusal_survives_a_console_that_cannot_encode_its_output`. Their
text is in the fixes section.

- 🟡 1: a refusal names the put-back's failure when the module cannot be put back. POSIX only, skipped as root. NAME NOT IN TREE
- ⬜ 2: an interrupted first run puts back what the command changed. NAME NOT IN TREE

## Facts for the evidence ledger

- R1's notes: the put-back reaches a removed or rewritten module. A module
  left unreadable, unwritable or replaced by a directory cannot be put back.
  With F1 the line names the error, at exit 2. The refusal-only mutant
  survived the module's cases at `dc1b0d14`, because the interrupt arm had no
  case until ⬜ 2's. Executed in round 2.
- R4's notes: the stdout surrogate route through a spawn failure's reason
  does not exist, because the reason reprs the filename. Executed in round 2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A first run whose cases leave the module unreadable, unwritable or replaced by a directory makes the put-back raise out of the `finally`: a traceback at exit 1 in place of the refusal line and the command's output, where `6bbaa4d1` refused at exit 2 | `skills/verify/scripts/arm_check.py:958-971` | open | Executed: `chmod 000`, `chmod 200`, rewrite then `chmod 444`, and a directory, each then exit 1, all four `PermissionError` or `IsADirectoryError`, exit 1, at the target. All four exit 2 at `6bbaa4d1`. F1 gives exit 2 with the error named in all four |
| ⬜ 2 | The first run's put-back on an interrupt is held by no case; R2, the refusal-only mutant, is not equivalent | `skills/verify/scripts/arm_check.py:965-968` | open | Executed: the mutant survived the module, 92 passed. Under it a real SIGINT left the rewrite on disk, and at the target the module came back byte-identical. Behaviour right |
| 🟢 | round 1's finding 1 is closed at its instance — a rewrite or a removal is put back, and the line says so | `skills/verify/scripts/arm_check.py:958-971`, `:1246-1259` | confirmed | Executed: rewrite and remove, each at exit 1 and at exit 0, module byte-identical, line true. Mutations Mu and Mp red on the new case. The class is this round's finding 1 |
| 🟢 | round 1's finding 2 is closed — a cp1252 console gets the refusal | `skills/verify/scripts/arm_check.py:1270-1279` | confirmed | Executed: exit 2, no `Traceback`, output as UTF-8. Mutation Mc (reconfigure removed) red on the new case alone |
| 🟢 | round 1's finding 3 is closed — a pair printing non-UTF-8 keeps its verdict | `skills/verify/scripts/arm_check.py:990-1003` | confirmed | Executed: both arms `killed`, exit 0. Mutation Mt (`text=True` back) red on the new case alone |
| 🟢 | round 1's finding 4 is closed — a signal-killed first run is `no baseline` | `tests/test_arm_check.py:1721` | confirmed | Executed: `no baseline: exit -9.`, exit 2. Mutation Mg red on the signal parameter alone |
| 🟢 | round 1's finding 5 is closed — a timed-out first run's output reaches the person | `tests/test_arm_check.py:1851` | confirmed | Executed: the printed line follows the verdict at `--timeout 1.5`. Mutation Mi red on that case alone |
| 🟢 | round 1's finding 6 is closed — the SKILL timeout paragraph names the first run | `skills/verify/SKILL.md:83-86` | confirmed | Read against `run_arms` at the target |
| 🟢 | The smith's departure from round 1's paste-ready block is correct; the block was wrong | `skills/verify/scripts/arm_check.py:940-971` | confirmed | Read: in the block, a removed module's read raises into `except OSError` and is reported as a spawn failure, not restored. Executed: Mu red on `removes it` |
| 🟢 | R10, `strict` on stdout, is unreachable on this machine as recorded | `skills/verify/scripts/arm_check.py:1270-1279` | confirmed | Executed: a spawn failure naming a `\xff` path printed alike under `replace` and `strict`, because the reason reprs it. Linux could reach it through a module path |
| 🟢 | The three new cases were red before the fix | `tests/test_arm_check.py:2004`, `:2059`, `:2086` | confirmed | Executed: against the script at `6bbaa4d1` four of the six selected fail (both `CHANGES_THE_MODULE` parameters, the console, the pair). The other two pin behaviour that was already right, and Mg and Mi show them red |
| 🟢 | The ledger holds unscoped | `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 3200 ok, 0 drifted, 0 broken |
| ⬜ | round 1's ⬜ 7, a command that returned but left a child on the pipe | `skills/verify/scripts/arm_check.py:941-944` | deferred #313 | already deferred in round 1 |
| ❓ | The Windows leg: `HANG_BOUND` under `-n auto`, the cp1252 pipe for real, and the signal parameter's skip | `tests/test_arm_check.py` | ❓ out of verified scope | No Windows machine here. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_arm_check.py -q -p no:xdist` in the clone at `dc1b0d14` | 92 passed, 2 skipped, exit 0 |
| The target script, first run rewrites or removes the module, at exit 1 and at exit 0 (`--only` selecting nothing) | exit 2 and exit 0; the module sha256 as read in all four; the refusal line says *was put back* |
| The same, at `6bbaa4d1` | exit 2 with the rewrite left on disk, or the module gone, under *Nothing was written* |
| The target script, first run `chmod 000`, `chmod 200`, rewrite then `chmod 444`, a directory, each then exit 1 | `PermissionError` or `IsADirectoryError` traceback, exit 1, no refusal line, in all four |
| The same, at `6bbaa4d1` | exit 2 and the refusal line in all four |
| `PYTHONIOENCODING=cp1252`, first run prints `b'\xff'` and exits 1 | exit 2, no `Traceback`, output line `x U+FFFD y` in UTF-8 |
| Pairs whose cases print `b'\xff'` under a mutation | both arms `killed`, exit 0, no traceback |
| First run SIGKILLs itself after printing | `no baseline: exit -9.`, exit 2, its output follows |
| First run prints, then sleeps past `--timeout 1.5` | the bound in the line, the printed line below it, exit 2 |
| SIGINT two seconds into a first run that rewrote the module, target and R2 mutant | target: `KeyboardInterrupt`, module byte-identical; mutant: module left rewritten |
| `--tests` naming a nonexistent path holding byte `\xff`, stdout `replace` and `strict` | both: exit 2, the same line; the reason reprs the surrogate |
| Mutations against the whole module (narrow form): Mg, Mi, R2, Mu, Mp, Mc, Mt | Mg, Mi, Mu, Mp, Mc, Mt each red on the case named in the verdicts; R2 survived, 92 passed |
| The new cases against the script at `6bbaa4d1` | 4 failed, 2 passed (the signal parameter and the timed-out case, already right there) |
| F1 and the two proposed cases applied in the clone, the whole module | 94 passed, 2 skipped, exit 0; `uvx ruff check` and `uvx ruff format --check` exit 0 |
| F1, the four unreadable shapes and the two restorable ones, each then exit 1 | exit 2 in all six; the four name the error after *putting it back failed:*; the two say *was put back*; the output follows in all six |
| The two proposed cases at `dc1b0d14`, and under R2 | at `dc1b0d14`: the put-back case red, the interrupt case green; under R2: both red |
| `bin/evidence-check .` unscoped in the clone at `dc1b0d14` | exit 0, 3200 ok, 0 drifted, 0 broken |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's run, after the rounds settle; this round leaves finding 1 open, so it has not come due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's ⬜ 7, a command that returned but left a child on the pipe, refused as *did not return*; read here: the same reach lets a wrapper's grandchild rewrite the module after the first run's put-back | #313, the bound that reaches the direct child only | the orchestrator, by adding the grandchild shape to #313's existing comment when the round is recorded |

## Paste-ready fixes

### 🟡 1 — `skills/verify/scripts/arm_check.py`, the `NoBaseline` constructor and its docstring

```python
    `put_back` says the command itself changed the module during that run and
    it was restored from the bytes read before it, so the line a person reads
    cannot say *Nothing was written* over a write (round 1, 🟡 1).
    `not_put_back` is why the restore failed where the command left the
    module unreadable, unwritable or replaced, said on the line instead of
    as a traceback that loses it (round 2, 🟡 1).
    """

    def __init__(self, reason: str, output: str = "") -> None:
        super().__init__(reason)
        self.reason = reason
        self.output = output
        self.put_back = False
        self.not_put_back: str | None = None
```

### 🟡 1 — `skills/verify/scripts/arm_check.py`, the first run's `finally` in `run_arms`

```python
    finally:
        try:
            with open(path, "rb") as f:
                changed = f.read() != original
        except OSError:
            # Removed, made unreadable, or replaced: not what was read.
            changed = True
        not_put_back = None
        if changed:
            # On a pass the loop's outer `finally` would put it back as well;
            # on a refusal, and on an interrupt, nothing else does.
            try:
                restore(path, original, original_sha)
            except (OSError, RuntimeError) as exc:
                # A module the command made unwritable or unreadable, or
                # replaced with a directory, cannot be put back. On a refusal
                # that is said on the refusal's own line; a traceback there
                # loses the line and the command's output (round 2). On a
                # pass or an interrupt it propagates, as the loop's would.
                if refusal is None:
                    raise
                not_put_back = f"{type(exc).__name__}: {exc}"
    if refusal is not None:
        refusal.put_back = changed
        refusal.not_put_back = not_put_back
        raise refusal
```

### 🟡 1 — `skills/verify/scripts/arm_check.py`, the refusal line in `main`

```python
        echo(
            f"no baseline: {exc.reason}. --tests has to pass against "
            f"{args.module} as it is before anything is mutated, because a "
            f"failure under a mutation says nothing about the mutation. "
            + (
                f"The command changed {args.module} during that run, and "
                f"putting it back failed: {exc.not_put_back}. No arm was "
                f"measured."
                if exc.not_put_back
                else f"The command changed {args.module} during that run, and it "
                f"was put back from the bytes read before it. No arm was "
                f"measured."
                if exc.put_back
                else "Nothing was written and no arm was measured."
            )
        )
```

### 🟡 1 — the case, `tests/test_arm_check.py`

```python
@pytest.mark.skipif(
    os.name == "nt" or getattr(os, "geteuid", lambda: 1)() == 0,
    reason="POSIX modes, and root reads a mode-000 file",
)
def test_a_refusal_says_so_when_the_module_cannot_be_put_back(
    two_arms, tmp_path, capsys
):
    """Round 2. A command that leaves the module unreadable fails the
    put-back's own open, and raised out of the `finally` the refusal's line
    and the command's output went with it, at exit 1.

    Red how: at `dc1b0d14` a `PermissionError` traceback and no line.
    Executed."""
    module_path, _ = two_arms
    probe = tmp_path / "locks_the_module.py"
    probe.write_text(
        "import os\nimport sys\nprint('locked')\nos.chmod(sys.argv[1], 0)\n"
        "sys.exit(1)\n",
        encoding="utf-8",
    )
    tests = [sys.executable, str(probe), str(module_path)]
    try:
        status = ARM.main([str(module_path), "--tests", shlex.join(tests)])
    finally:
        os.chmod(module_path, 0o644)
    out = capsys.readouterr().out
    first = out.splitlines()[0]
    assert status == 2
    assert first.startswith("no baseline: exit 1."), first
    assert "putting it back failed: PermissionError" in first, first
    assert "Nothing was written" not in first and "was put back" not in first
    assert "locked" in out
```

### 🟡 1 — what a person reads (§14): `skills/verify/SKILL.md` at line 132, the changelog fragment's first entry, and the `bin/arm-check` header

```markdown
negative `--timeout`. If the command itself changed the module during that
run, the module is put back from the bytes read before it and the line says
so instead. Where it cannot be put back, because the command left it
unreadable, unwritable or replaced by a directory, the line names the error.
```

```markdown
  is the code a negative `--timeout` already gets. If the command itself
  changed the module during that run, the module is put back from the bytes
  read before it and the line says so instead, or names the error where the
  command left it so that it cannot be put back.
```

```sh
# with exit 2 unless it passes there -- nothing written, no arm measured,
# and anything the command itself changed in the module put back, or, where
# it cannot be, the reason said.
```

### ⬜ 2 — the case, `tests/test_arm_check.py`

```python
def test_an_interrupted_first_run_puts_back_what_the_command_changed(
    two_arms, monkeypatch
):
    """Round 2. The first run's `finally` is the only restore an interrupt
    there reaches: the loop's outer `finally` is never entered. Narrowed to
    a refusal, the put-back survived the whole module, because the
    refusal case and the passing case each have a second witness and this
    path has none.

    Red how: `if changed:` narrowed to `if changed and refusal is not None:`.
    Executed."""
    module_path, tests = two_arms
    before = module_path.read_bytes()

    def rewrites_then_interrupted(cmd, **kwargs):
        module_path.write_text("VALUE = 99\n", encoding="utf-8")
        raise KeyboardInterrupt

    monkeypatch.setattr(ARM.subprocess, "run", rewrites_then_interrupted)
    with pytest.raises(KeyboardInterrupt):
        ARM.run_arms(str(module_path), tests)
    assert module_path.read_bytes() == before
```

Needs a fix: yes — 🟡 1 (a first run that leaves the module unreadable, unwritable or replaced by a directory ends the refusal in a traceback at exit 1)
Loses a record or crashes: yes — 🟡 1 crashes a refusal that `6bbaa4d1` gave at exit 2, and the line and the command's output are lost

## Proof block

Files opened in this round, all in the clone at `dc1b0d14` unless named:
`seal/specs/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill/rounds/round-1.md`,
`seal/specs/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill/rounds/round-1-report.md` (its head),
`seal/specs/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill/routing.md`,
`seal/specs/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill/changelog.md`,
the fix range's diff of `skills/verify/scripts/arm_check.py`, `bin/arm-check`,
`tests/test_arm_check.py`, `skills/verify/SKILL.md`, `overview.md`,
`seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md`,
`seal/releases/0.9.5.md` and `seal/releases/0.15.1.md`;
`skills/verify/scripts/arm_check.py` (`NoBaseline`, `restore`, `run_arms`,
`main`, the entry block); `tests/test_arm_check.py` (`two_arms`,
`NO_BASELINE_SHAPES`, the refusal case, the three new cases);
`bin/arm-check`; `bin/test`; `skills/verify/scripts/unverified_check.py` (its
entry block).
Every probe file, fixture and the clone sit under this round's directory, and
are removed at hand-over.
