# Round 1 report — arm-check reads a run that measured nothing as a kill

Work item `1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill` (#703, draft PR #707).
Target `6bbaa4d1`, base `a340221b`, diff `a340221b..6bbaa4d1`. Reviewed in a
`git clone --no-local` at the target. No earlier round exists, so nothing is
carried from a round record. The facts in the spawn prompt and in
`overview.md` were read as claims and checked below.

## Summary

Stage 1 holds. S1 to S9 are met as the spec states them. The three shapes, a
first run that times out, one that cannot start and one that prints
non-UTF-8 bytes each come back `no baseline`, exit 2, with nothing written.
`clear_bytecode_cache` reads a relative prefix against `cwd`. A caller that
passes no `cwd` gets the old reading, and all three call sites pass it. The
first run's bound is held by a case. The ledger holds unscoped.

Stage 2 found three defects, and each has a paste-ready fix that was checked
on a copy of the script:

1. **The first run moved outside the restoring `try`, and a refusal now
   leaves the module however the cases left it.** At the base, every run
   ended with the module put back. 🟡 1.
2. **The refusal's own output still crashes the command on a console that is
   not UTF-8.** `_text` decodes the bytes with replacement. Printing the
   replacement character then raises `UnicodeEncodeError`, and the command
   exits 1. Every other skill script avoids this by reconfiguring its streams,
   and `arm_check.py` does not. 🟡 2.
3. **The pairs still decode strictly.** Their output is never read, and a
   mutation whose cases print a byte that is not UTF-8 crashes the whole run
   with every verdict measured so far lost. This existed before the branch.
   It belongs to the same class as the decode the branch fixed, and
   `overview.md` §*Not done* declines it on grounds this report contests.
   🟡 3.

Four notes follow (⬜ 4 to ⬜ 7). None of them needs a fix.

## Stage 1 — spec compliance

**S1 to S3: executed.** Probe P1 used a two-arm fixture and real pytest from
the clone's venv. It ran the script at `a340221b` and the script at the
target with each of three commands: `-k` selecting nothing, a module path
that does not exist, and a case that already fails. The base printed
`killed` beside both arms, `0 watched by no case`, exit 0, and changed the
mtime. The target printed `no baseline: exit 5.`, `exit 4.` and `exit 1.`,
exit 2, with the sha256 unchanged and the mtime untouched. Python 3.9.6
loaded the script and refused a run at exit 5 with exit 2.

**S4: executed.** Mutation Ma set the first run's `timeout` to `None`. It
was red on `test_the_run_against_the_unmutated_module_is_bounded_by_the_timeout`
alone, after 41.8 s.

**S5: read and executed.** `FileNotFoundError` names the cause, and the
module case pins it.

**S6 and S7: executed.** The module run gave 87 passed and 2 skipped, which
matches the handover.

**S8: read.** These texts match the code at the target:

- the `--tests` help and the `--timeout` help;
- the header of `bin/arm-check`;
- the docstrings of `run_arms`, `NoBaseline` and `_text`;
- the SKILL section's step list and its new paragraph.

There is one gap, the SKILL timeout paragraph, in ⬜ 6. `_text`'s claim that
the decode keeps a refusal from becoming a traceback is false on a console
that is not UTF-8 (🟡 2).

**S9: executed.**

- Mutations Mb to Me were each red on the `[relative]` parameter of the
  prefix case. Mb removes the join; Mc, Md and Me each drop `cwd` from one
  of the three call sites.
- P7 ran from a directory `top/` with `--cwd sub`, which is relative, and
  `PYTHONPYCACHEPREFIX=rel`. It planted a `.pyc` in the mirror the cases
  read and saw `clean` at all five runs. That mirror was empty afterwards.
- Spec M1 was re-run on 3.9.6, 3.13 and 3.14. On each, `sys.pycache_prefix`
  stays relative.

**S10: partly executed.** `tests/test_a_script_says_which_interpreter_it_needs.py`
and `tests/test_release_hygiene.py` gave 72 passed. `ruff check` and
`ruff format --check` on the two touched `.py` files exit 0. The CI legs
are the pull request's to show.

**S11: unverified.** It is recorded in `overview.md` with its answerer: the
orchestrator of whichever branch lands second.

## Stage 2 — findings

### 🟡 1 — a refused run no longer puts back a module the cases rewrote (`skills/verify/scripts/arm_check.py:920-944`)

The first run sits outside the `try` whose `finally` restores. Its comment
gives the reason: *a refusal owes no restore and must not make one*. That
holds only while the cases leave the module alone. Probe P4 used a command
that writes `VALUE = 99` to the module and exits 1:

- At `a340221b` the module ended byte-identical to the original, because
  the outer `finally` always restored it.
- At the target it ended as `VALUE = 99`, and the run printed *Nothing was
  written and no arm was measured.*

`arm-check` held the original bytes the whole time and threw them away.

**Why it matters.** The module is usually uncommitted work. A suite that
writes its own input is uncommon, but it does occur: a formatter's
round-trip test, or a generator that regenerates a file in place. Before
this branch `arm-check` guaranteed the module came out of a run as it went
in. Now the refusal path breaks that guarantee, and the printed line reads
as though the guarantee still held. #641 met the same shape: its round 3's
🟡 15 led to round 4's *the restore covers every baseline exit*.

**The fix.** Compare the bytes after the first run, in a `finally`, and
restore only if they differ. A module the cases did not touch is still never
written, so `test_a_command_that_does_not_pass_against_the_module_refuses_the_run`'s
mtime pin stays green. Fix F4 was checked on a copy of the script: it exits
2, the module is back, and the line says it was put back. Fix F5 checked
that a `-k` selecting nothing still leaves the mtime untouched.

### 🟡 2 — the refusal crashes on a console that is not UTF-8 (`skills/verify/scripts/arm_check.py:1222`, `:1233`)

`_text` turns the captured bytes into text with `errors="replace"`, and
`main` prints that text through `print`. Probe P2 ran a first run that
writes `b'x \xff y'` and exits 1, under `PYTHONIOENCODING=cp1252`. The
command printed the `no baseline:` line, then raised
`UnicodeEncodeError: 'charmap' codec can't encode character '�'`, and
exited 1. Under the default UTF-8 console the same probe exits 2.

This is not only a contrived case. On Windows a pipe's encoding is the ANSI
code page, and a pytest child there writes in that code page. Any non-ASCII
byte in its output then decodes to U+FFFD, and cp1252 cannot encode that
character. The em dash this repository's assertion messages use is one such
byte. So on Windows, a refused run whose output is captured, as an agent's
always is, can end in a traceback at exit 1.

**The class (§12).** Five other skill scripts reconfigure stdout and stderr
before `main()`:

- `skills/code-review/scripts/chain_check.py`
- `skills/code-review/scripts/round_record.py`
- `skills/code-review/scripts/survivor_check.py`
- `skills/evidence-check/scripts/correction_check.py`
- `skills/evidence-check/scripts/evidence_check.py`

`hooks/console.py` owns the reasoning behind that block. `arm_check.py` is
the one script here that prints captured text and has no such block. The
report's own `—` and `·` already had this exposure on a cp949 or ascii
console before the branch. The branch adds the widest case, because the
output is arbitrary. It also adds a docstring that promises the opposite.
Fix F2, checked on a copy, exits 2 under cp1252.

### 🟡 3 — a pair's strict decode crashes the run and loses every verdict (`skills/verify/scripts/arm_check.py:965`)

The pairs run with `text=True`, and nothing ever reads `run.stdout` or
`run.stderr`. Probe P3 used a command that passes against the original and,
under any mutation, prints `b'boom \xff'` and exits 1. The base and the
target both crashed with `UnicodeDecodeError`, exit 1, and printed nothing
to stdout. The module was restored, but no verdict survived.

`overview.md` §*Not done* answers this: *that cause predates this item*.
That is true. But the branch already met this class and fixed it for the
first run, the fix here is to delete one line, and the line buys nothing.
Under §12 the class is *captured output decoded strictly*, and it has two
members in one function. Fix F3, checked on a copy, gives both arms
`killed`, exit 0, with the module restored. If the smith keeps the deferral,
it needs a home that someone will act on, which `overview.md` does not name.

### ⬜ 4 — a first run killed by a signal is not held by a case (`skills/verify/scripts/arm_check.py:939`)

Mutation Mg changed `!= 0` to `> 0`, so a negative return code reads as a
pass. It survived the module: 87 passed. The code is right. If a later edit
narrowed the check, an OOM-killed or SIGKILLed first run would read as a
green baseline and every arm after it as a measurement.

### ⬜ 5 — R2's *with what it printed before it* holds in `run_arms` and not in what a person sees (`skills/verify/scripts/arm_check.py:1221-1222`)

Mutation Mi printed the output only when the reason starts with `exit`. It
survived the module. `test_a_first_run_that_timed_out_carries_what_it_printed`
reads `NoBaseline.output` and never goes through `main`. The behaviour is
right, and the ledger row's claim is held one layer short of the reader.

### ⬜ 6 — the SKILL timeout paragraph names only a pair as what leaks (`skills/verify/SKILL.md:83`)

*A timed-out pair leaves that suite running* is still true. Since this
branch, a hang that does not depend on the mutation meets the bound in the
first run. That run leaks the wrapper's suite the same way. The help's
*only the command's own process is killed* covers it, and the paragraph
does not. N2's re-read says the paragraph is unchanged, and it is. One
clause would complete it.

### ⬜ 7 — a command that exits 0 but leaves a child on the pipe is refused as *did not return* (`skills/verify/scripts/arm_check.py:928-935`)

Probe P5 used `--tests "sh -c 'sleep 20 & exit 0'"` with `--timeout 2`. It
printed `no baseline: the command did not return within 2.0s` at 2.0 s.
The command returned at once, and the background child held stdout open.
This is #641's round 1 🟡 4, in `arm-check`'s shape.

The pairs had it before the branch, as two waits per arm. The branch turns
it into one wait and a refusal, which is the cheaper direction. Only the
cause it names is wrong. It belongs with #313, a bound that reaches the
direct child only, which the spec keeps out. So it is deferred there rather
than fixed here.

## What the account claimed, and what was found

| Claimed | Found |
|---|---|
| 87 passed, 2 skipped (orchestrator re-run) | Executed in the clone: 87 passed, 2 skipped |
| `no baseline: exit 5` through `bin/test` (Q2) | Not re-run through `bin/test`. Executed through pytest directly (P1): `exit 5`, exit 2 |
| 26 mutations red | Not re-run as listed. Seven of this round's own nine were red and two survived (⬜ 4, ⬜ 5) |
| Q3: 107.9 s → 110.5 s | Read only; not re-measured |
| 705 reader-module cases | Not checked. Not this round's to answer |
| The first run outside the `try` owes no write (R1, the code comment) | True of `arm-check`'s writes. False of the module's state when the cases write it (🟡 1) |
| A non-UTF-8 suite cannot turn the refusal into a traceback (`_text`) | False on a cp1252 console (🟡 2) |
| `evidence-check --strict .` 0 | Executed `bin/evidence-check .` unscoped: exit 0, 3196 ok, 0 drifted, 0 broken |

## The class (§12), enumerated

No other shipped script reads an exit code as a mutation verdict. Every
`returncode` reader under `skills/`, `hooks/` and `.github/scripts/` was
listed with `git grep`, and each reads a git or setup step's status as
*that command failed*. `broad_gate.py` already compares against a base. The
sibling `mutation_check.py` has its own baseline on #641's branch.

The decode class (🟡 2, 🟡 3) was enumerated in the same file and against
the other skill scripts' entry blocks.

## Regression tests to plant

All three go in `tests/test_arm_check.py`. Each was shown red at the target
by the probe named beside it, and green on the fixed copy.

```python
def test_a_refused_run_leaves_the_module_as_it_was_before_the_command(
    two_arms, tmp_path, capsys
):
    """Red at 6bbaa4d1 (probe P4): the module is left as the command wrote it."""
    module_path, _ = two_arms
    before = module_path.read_bytes()
    probe = tmp_path / "rewrites.py"
    probe.write_text(
        "import sys\nopen(sys.argv[1], 'w').write('VALUE = 99\\n')\nsys.exit(1)\n",
        encoding="utf-8",
    )
    tests = [sys.executable, str(probe), str(module_path)]
    status = ARM.main([str(module_path), "--tests", shlex.join(tests)])
    out = capsys.readouterr().out
    assert status == 2
    assert out.startswith("no baseline: exit 1."), out
    assert "put back" in out.splitlines()[0], out
    assert module_path.read_bytes() == before, "the module was left as the command wrote it"
```

```python
def test_a_refusal_survives_a_console_that_cannot_encode_its_output(two_arms, tmp_path):
    """Red at 6bbaa4d1 (probe P2): UnicodeEncodeError, exit 1."""
    module_path, _ = two_arms
    probe = tmp_path / "prints_a_byte.py"
    probe.write_text(
        "import sys\nsys.stdout.buffer.write(b'x \\xff y\\n')\nsys.exit(1)\n",
        encoding="utf-8",
    )
    tests = shlex.join([sys.executable, str(probe)])
    run = subprocess.run(
        [sys.executable, SCRIPT, str(module_path), "--tests", tests],
        capture_output=True,
        env=dict(os.environ, PYTHONIOENCODING="cp1252"),
    )
    assert run.returncode == 2, run.stderr.decode("utf-8", "replace")
    assert b"Traceback" not in run.stderr
```

```python
def test_a_pair_whose_cases_print_a_byte_that_is_not_utf8_keeps_its_verdict(
    two_arms, tmp_path
):
    """Red at 6bbaa4d1 (probe P3): UnicodeDecodeError out of run_arms."""
    module_path, _ = two_arms
    copy = tmp_path / "as_it_was.txt"
    copy.write_bytes(module_path.read_bytes())
    probe = tmp_path / "prints_on_a_mutation.py"
    probe.write_text(
        "import sys\n"
        "if open(sys.argv[1], 'rb').read() != open(sys.argv[2], 'rb').read():\n"
        "    sys.stdout.buffer.write(b'boom \\xff\\n')\n"
        "    sys.exit(1)\n",
        encoding="utf-8",
    )
    verdicts, refused = ARM.run_arms(
        str(module_path), [sys.executable, str(probe), str(module_path), str(copy)]
    )
    assert refused == []
    assert [v.killed for v in verdicts] == [True, True]
```

The second case uses `SCRIPT`, which the module already defines at its
head. It also needs `import subprocess`, which the module does not have yet.

## Facts for the evidence ledger

- R1 can carry this round's P1 as an independent execution: real pytest,
  exit 5, 4 and 1, exit 2, sha256 and mtime unchanged, and Python 3.9.6
  refusing at exit 5.
- Whatever fixes 🟡 1 belongs in R1's claim: *a refusal leaves the module as
  it was before the command, putting back what the cases changed*.
- R3's M1 holds on 3.9.6, 3.13 and 3.14: `sys.pycache_prefix` stays
  relative. A relative `--cwd` with a relative prefix clears the right
  mirror (P7).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A refused run leaves the module however the cases wrote it during the first run; at the base the outer `finally` put it back, and the line still says *Nothing was written* | `skills/verify/scripts/arm_check.py:920-944` | open | Executed: P4, a command writing `VALUE = 99` and exiting 1, left the module `VALUE = 99` at the target and byte-identical at `a340221b`; fix F4 restores it, and F5 shows an untouched module is still never written |
| 🟡 2 | The refusal's output crashes on a console that is not UTF-8: U+FFFD from `_text` raises `UnicodeEncodeError`, exit 1, contradicting `_text`'s docstring; `arm_check.py` lacks the stream reconfigure five other skill scripts carry | `skills/verify/scripts/arm_check.py:1222` | open | Executed: P2 under `PYTHONIOENCODING=cp1252` printed the line and then a traceback, exit 1; exit 2 under UTF-8; fix F2 exits 2 under cp1252 |
| 🟡 3 | A pair's `text=True` strict decode turns a mutation whose cases print a non-UTF-8 byte into a traceback that discards every verdict; the output is never read | `skills/verify/scripts/arm_check.py:965` | open | Executed: P3 crashed with `UnicodeDecodeError`, exit 1, at the base and at the target; fix F3 gives both arms `killed`, exit 0. Predates the branch, and is the same class as the decode it fixed |
| ⬜ 4 | A first run killed by a signal (negative return code) is held by no case | `skills/verify/scripts/arm_check.py:939` | open | Executed: mutation Mg (`!= 0` to `> 0`) survived the module, 87 passed. Behaviour right |
| ⬜ 5 | The output a timed-out first run printed reaches `NoBaseline.output` under a case, and reaches the reader under none | `skills/verify/scripts/arm_check.py:1221-1222` | open | Executed: mutation Mi (print only when the reason starts with `exit`) survived the module. Behaviour right |
| ⬜ 6 | The SKILL timeout paragraph names a timed-out pair as what leaks a wrapper's suite; the first run leaks it the same way now | `skills/verify/SKILL.md:83` | open | Read against `run_arms` at the target. The help's sentence covers it; the paragraph does not |
| ⬜ 7 | A command that exits 0 but leaves a child holding stdout is refused as *did not return within* the bound | `skills/verify/scripts/arm_check.py:928-935` | deferred #313 | Executed: P5 printed `no baseline: the command did not return within 2.0s` at 2.0 s for `sh -c 'sleep 20 & exit 0'`. The pairs had it before the branch; the wait is #313's direct-child reach |
| 🟢 | The three shapes, a timeout, a spawn failure and non-UTF-8 output each refuse the run at exit 2 with nothing written | `skills/verify/scripts/arm_check.py:920-944`, `:1210-1223` | confirmed | Executed: P1 against real pytest (exit 5, 4, 1) at base and target; P2 default console; Python 3.9.6 refusal; module case 87 passed |
| 🟢 | The first run's bound is held by a case | `tests/test_arm_check.py` | confirmed | Executed: mutation Ma (`timeout=None` on the first run) red on the bound case alone |
| 🟢 | `clear_bytecode_cache(path, cwd=None)` reads a relative prefix against `cwd`, keeps the old reading with no `cwd`, and all three call sites pass `cwd` | `skills/verify/scripts/arm_check.py:781-834`, `:927`, `:959`, `:988` | confirmed | Executed: mutations Mb to Me each red on the `[relative]` parameter; P7 with a relative `--cwd` saw `clean` five times; M1 re-run on 3.9.6, 3.13, 3.14 |
| 🟢 | An interrupt during the first run, and a target read-only from the start, leave the module untouched | `skills/verify/scripts/arm_check.py:920-944` | confirmed | Executed: P6 SIGINT during the first run, sha256 and mtime unchanged; P8 read-only target, a traceback at base and target alike, file unchanged |
| 🟢 | The ledger holds unscoped; 0.9.5's `run_arms` row is corrected in place and its `clear_bytecode_cache` row and 0.15.1 N2 re-read | `seal/releases/0.9.5.md`, `seal/releases/0.15.1.md`, `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 3196 ok, 0 drifted, 0 broken. Read: the three notes against the diff |
| 🟢 | No other shipped script reads an exit code as a mutation verdict without a baseline | `skills/`, `hooks/`, `.github/scripts/` | confirmed | Executed: `git grep` over every `returncode` reader; each reads a git or setup step's status |
| ❓ | The Windows leg: `HANG_BOUND = 1.0` under `-n auto`, and 🟡 2's cp1252 pipe as it occurs there | `tests/test_arm_check.py`, `skills/verify/scripts/arm_check.py:1222` | ❓ out of verified scope | No Windows machine here; 🟡 2 was reproduced with `PYTHONIOENCODING`. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_arm_check.py -q -p no:xdist` in the clone at `6bbaa4d1` | 87 passed, 2 skipped, exit 0 |
| P1: the base and target scripts over a two-arm fixture, `--tests` real pytest with `-k` matching nothing, a missing path, an already failing case | base: `killed` both arms, exit 0, mtime moved; target: `no baseline: exit 5.` / `exit 4.` / `exit 1.`, exit 2, sha256 and mtime unchanged |
| P2: first run writes `b'\xff'` and exits 1, default console and `PYTHONIOENCODING=cp1252` | default: exit 2; cp1252: `UnicodeEncodeError` after the refusal line, exit 1 |
| P3: pairs whose cases print `b'\xff'` under a mutation, base and target | both: `UnicodeDecodeError`, exit 1, no stdout, module restored |
| P4: first run rewrites the module to `VALUE = 99` and exits 1, base and target | base: module restored, exit 0; target: exit 2, module left `VALUE = 99` |
| P5: `sh -c 'sleep 20 & exit 0'`, `--timeout 2` | `no baseline: the command did not return within 2.0s`, exit 2, at 2.0 s |
| P6: SIGINT to `arm-check` one second into a 10 s first run | `KeyboardInterrupt`, sha256 and mtime unchanged |
| P7: relative `--cwd sub` and `PYTHONPYCACHEPREFIX=rel`, a `.pyc` planted in the cases' mirror and re-left by each run | `clean` at all five runs, mirror empty afterwards, exit 0 |
| P8: target `chmod 444` from the start, base and target | both: `PermissionError` traceback, exit 1, file unchanged |
| `PYTHONPYCACHEPREFIX=relprefix` on Python 3.9.6, 3.13, 3.14: `sys.pycache_prefix` and `cache_from_source` | relative on all three |
| Python 3.9.6 running the target script, a first run exiting 5 | `no baseline: exit 5.`, exit 2 |
| Mutations of the new units, each against `tests/test_arm_check.py -p no:xdist` | Ma, Mb, Mc, Md, Me, Mf, Mh red; Mg and Mi survived |
| Fixes F2 to F5 applied to a copy of the target script, P2 to P4 and P1's `-k` re-run | F2 exit 2 under cp1252; F3 both arms `killed`, exit 0; F4 exit 2 with the module back; F5 exit 2, mtime untouched |
| `bin/evidence-check .` unscoped in the clone | exit 0, 3196 ok, 0 drifted, 0 broken |
| `tests/test_a_script_says_which_interpreter_it_needs.py` and `tests/test_release_hygiene.py` | 72 passed, exit 0 |
| `uvx ruff check` and `uvx ruff format --check` on the two touched `.py` files | exit 0 both |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — the sealer's run, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 7, a command that returned but left a child on the pipe is refused as *did not return* | #313, the bound that reaches the direct child only | the orchestrator, by adding this shape to #313 as a comment when the round is recorded |

## Paste-ready fixes

### 🟡 1

Replace the first-run block in `run_arms`, so a refusal puts back whatever
the cases changed and never writes a module they left alone:

```python
    clear_bytecode_cache(path, cwd=cwd)
    rewrote = False
    try:
        try:
            baseline = subprocess.run(
                tests, cwd=cwd, capture_output=True, env=env, timeout=timeout
            )
        finally:
            # The cases may write the module themselves, and nothing below
            # restores on a refusal. Put back what they changed, and only
            # that: bytes that still match were never written and stay so.
            with open(path, "rb") as f:
                rewrote = f.read() != original
            if rewrote:
                restore(path, original, original_sha)
    except subprocess.TimeoutExpired as exc:
        raise NoBaseline(
            f"the command did not return within {timeout}s",
            _text(exc.stdout) + _text(exc.stderr),
            rewrote=rewrote,
        ) from exc
    except OSError as exc:
        raise NoBaseline(f"{type(exc).__name__}: {exc}", rewrote=rewrote) from exc
    if baseline.returncode != 0:
        raise NoBaseline(
            f"exit {baseline.returncode}",
            _text(baseline.stdout) + _text(baseline.stderr),
            rewrote=rewrote,
        )
```

```python
    def __init__(self, reason: str, output: str = "", rewrote: bool = False) -> None:
        super().__init__(reason)
        self.reason = reason
        self.output = output
        self.rewrote = rewrote
```

```python
        echo(
            f"no baseline: {exc.reason}. --tests has to pass against "
            f"{args.module} as it is before anything is mutated, because a "
            f"failure under a mutation says nothing about the mutation. "
            + (
                "The command rewrote the module during that run, and it was "
                "put back from the bytes read before it; no arm was measured."
                if exc.rewrote
                else "Nothing was written and no arm was measured."
            )
        )
```

The comment above the block (*Outside the `try` below on purpose …*) then
says that the inner `finally` restores only bytes that differ. The SKILL
sentence *writes nothing* gains *and puts back what the command itself
changed*.

### 🟡 2

The entry block the other skill scripts carry; `hooks/console.py` owns the
reasoning:

```python
if __name__ == "__main__":
    # A console that cannot encode what this prints -- the report's own
    # dashes, or the U+FFFD `_text` leaves where a suite printed a byte that
    # is not UTF-8 -- ends the run in a traceback after the verdict line.
    # `hooks/console.py` owns the reasoning behind these lines.
    for _name, _errors in (("stdout", "replace"), ("stderr", "backslashreplace")):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
```

### 🟡 3

Drop the strict decode of output nothing reads:

```python
                    run = subprocess.run(
                        tests,
                        cwd=cwd,
                        capture_output=True,
                        env=env,
                        timeout=timeout,
                    )
```

Needs a fix: yes — 🟡 1 (a refusal leaves a module the cases rewrote, which
the base put back) and 🟡 2 (the refusal crashes on a non-UTF-8 console);
🟡 3 is fix or justify with a home named
Loses a record or crashes: yes — 🟡 2 ends a refusal in a traceback at exit
1, 🟡 3 crashes a run and discards every verdict measured before it, and
🟡 1 drops the module bytes `arm-check` held and leaves the cases' rewrite

The broad gate has not come due: this round leaves 🟡 1 to 🟡 3 open.

## Proof block

Files opened in this round:

- `skills/verify/scripts/arm_check.py`: the module docstring, `NoBaseline`,
  `_text`, `clear_bytecode_cache`, `restore`, `run_arms`, the `_report`
  head and `main`
- `tests/test_arm_check.py`: the whole diff
- `bin/arm-check`: the diff
- `skills/verify/SKILL.md`: the `arm-check` section in full
- `seal/releases/0.9.5.md` and `seal/releases/0.15.1.md`: the changed rows
- this work item's `spec.md`, `plan.md`, `questions.md`, `overview.md` and
  `changelog.md`, and its ledger fragment
- `skills/evidence-check/scripts/evidence_check.py`: the entry block
- `skills/code-review/scripts/survivor_check.py`: `git` and the batch reader
- `.github/scripts/rider_check.py`: lines 585 to 606
- `tests/test_console_is_not_utf8.py`: lines 1 to 80
- #641's `rounds/round-1-report.md` to `round-4-report.md`: the verdict
  tables
