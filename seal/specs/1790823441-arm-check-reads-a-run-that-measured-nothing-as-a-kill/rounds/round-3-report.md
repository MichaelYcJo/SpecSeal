# Round 3 report — arm-check reads a run that measured nothing as a kill

Work item `1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill` (#703, draft PR #707).
Verifying round. Target `e091150a`; the diff verified is round 2's fix range
`56268bb1..bdbda4e6`, four commits. Reviewed in a `git clone --no-local` at
the target, under this round's own directory. Coordinates were carried from
`round-2.md`; every verdict below was re-derived at the target. The smith's
account (the commit messages, the ledger fragment's notes, `overview.md`,
`changelog.md` and the code comments) was read as claims and checked against
the code.

## Summary

Both of round 2's `fixed` verdicts are closed, and so is the class of the
first. Every probe round 2 ran was re-run against the target and every one
now gives the answer round 2 asked for. The smith's addition, raising the
failure on a pass or an interrupt, is right in behaviour. The pass path's
grounds hold in outcome, though the reason the comment gives is not the
mechanism. The new surface, `CANNOT_LOCK` and the extended parameters of
`test_a_refused_run_leaves_the_module_as_it_was_before_the_command`, fails on
every defect it pins, and was red against the script before the fix.

Four ⬜ findings, none of which ships a defect. Nothing needs a fix.

## Round 2's finding 1 — closed, and its class

Claimed (`0c25511a`): a refusal whose command left the module so that it
cannot be put back names the error on its line at exit 2.

Found: `skills/verify/scripts/arm_check.py:972-990` guards the put-back with
`except (OSError, RuntimeError)`. On a refusal it carries the error as
`not_put_back`, and `main` (`:1268-1280`) prints it in place of the
*was put back* sentence. Executed, through the CLI at the target, each first
run printing a line and then exiting 1:

- `chmod 000`, `chmod 200`, rewritten then `chmod 444`: exit 2, no
  `Traceback`, the line ends `putting it back failed: PermissionError: [Errno
  13] Permission denied: '…/under_test.py'. No arm was measured.`, and the
  command's output follows.
- Replaced by a directory: the same, with `IsADirectoryError: [Errno 21]`.
- Rewritten, and removed: exit 2, *was put back from the bytes read before
  it*, the module byte-identical.

The class is the put-back failing in any way `restore` can fail, and both of
its exceptions are caught on the refusal path. A missing parent directory
and an unwritable directory reach the same `open` and raise `OSError`
subclasses. The one member nothing holds is `RuntimeError`, which is ⬜ 1.

## Round 2's finding 2 — closed

Claimed (`8f231570`): the first run's put-back on an interrupt is held.

Found: the interrupt part of the case (`tests/test_arm_check.py:2117-2133`)
drives each change and then a `KeyboardInterrupt`. Executed: under R2 (`if
changed:` narrowed to `if changed and refusal is not None:`) the case is red
on all three parameters. A real SIGINT sent to `arm_check.py` two
steps into a first run that rewrote, or removed, the module left it
byte-identical, and the process died by the signal (exit -2).

## The smith's addition — the failure raised on a pass or an interrupt

**On an interrupt it is right, and pinned.** Executed: a real SIGINT over a
module the command had `chmod 000`-ed ends in `KeyboardInterrupt`, then
*During handling of the above exception*, then the `PermissionError`, at
exit 1. The swallow-always mutant is red on `locks it` alone. One consequence
worth knowing and not a defect: such a Ctrl-C exits 1 rather than dying by
SIGINT, so a shell loop reads it as a failure and not as an interrupt. The
traceback says why.

**On a pass, the grounds hold in outcome, and the reason given is not the
mechanism.** A mutant that swallows the failure on a pass and raises it on an
interrupt only (`if refusal is None and exc.__context__ is not None:`)
survives the module, 93 passed. Executed under it, a passing first run that
locks the module or replaces it with a directory still ends in that error's
traceback at exit 1, with `--only` selecting no arm and with every arm. So
the mutant is equivalent in what a person sees. What makes it equivalent is
the outer `finally`'s unconditional `restore` at `arm_check.py:1069`, though,
and not *the loop's own first write*: with `--only` selecting nothing the
loop writes nothing, and on an interrupt the loop is never entered. The
comment at `:982-983` and the case's at `tests/test_arm_check.py:2072-2073`
both name the loop. That is ⬜ 2.

## The finding surface

**`CANNOT_LOCK` (`tests/test_arm_check.py:2005`).** It is False here, and
`locks it` ran rather than skipping. Read: both of its conditions are needed.
Under root a mode-000 module is still writable, so the put-back succeeds, the
line says *was put back*, and the case would fail for a reason that is not
the defect. On Windows `chmod(path, 0)` only sets read-only, the read-back
returns the same bytes, nothing is put back, and the interrupt part would see
a bare `KeyboardInterrupt`. Neither leg was executed here (❓ below). The
repository already holds the same fact under the opposite name, which is
⬜ 4.

**The extended parameters.** Executed: against the script at `56268bb1`
the `locks it` parameter is red and the other two pass. Each mutation of the
fix is red on the case:

- the guard removed: red on `locks it`;
- the failure swallowed always: red on `locks it`;
- `main`'s new branch dropped: red on `locks it`;
- `not_put_back` never carried onto the refusal: red on `locks it`;
- R2: red on all three;
- the command's output not echoed: red on all three, and on six other cases.

Two mutants survive, and both are named above. One is the pass-only swallow,
which is equivalent. The other is the `RuntimeError` arm, ⬜ 1. The
parameter list is now written out by hand beside `CHANGES_THE_MODULE`, where
it used to be `sorted(CHANGES_THE_MODULE)`, which is ⬜ 3.

## Findings

### ⬜ 1 — the `RuntimeError` arm of the guard is held by no case, and the line it gives reads wrong

`skills/verify/scripts/arm_check.py:977`, `:1271`. Narrowing the guard to
`except OSError` leaves the module green, 93 passed. `restore` raises
`RuntimeError` when the bytes read back are not the bytes it wrote, which a
writer the command left behind reaches; that is the grandchild shape already
deferred to #313. Executed in-process, with `restore` made to raise as it
does there, the refusal is right (exit 2, output follows), but the line ends
`…so the run stops here.. No arm was measured.` It carries a doubled period,
and a sentence about *every verdict after this point* in a run that measured
none. No defect ships: the exit code and the output are right. The fix below
strips the period and adds the parameter that holds the arm.

### ⬜ 2 — two comments name the loop's first write as what makes the pass path safe

`skills/verify/scripts/arm_check.py:982-983`, `tests/test_arm_check.py:2072-2073`.
Above: the outer `finally`'s `restore` is what raises on a pass, and nothing
in the loop runs on an interrupt. A reader who later makes that `restore`
conditional, which its own comment at `:1061-1068` invites by calling it the
second of two, would be told by these comments that the pass path is still
covered.

### ⬜ 3 — the parameter list no longer follows `CHANGES_THE_MODULE`

`tests/test_arm_check.py:2008-2020`. The dict's comment (`:1995-1997`) calls
it *the ways a suite can leave its own input changed*. A fifth shape added to
it is now never run, where `sorted(CHANGES_THE_MODULE)` ran every key.

### ⬜ 4 — `CANNOT_LOCK` restates `CHMOD_STOPS_A_WRITE` under the opposite name

`tests/test_arm_check.py:2005` and
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:498`. Two
predicates for one fact: a POSIX mode stops this process, and the process is
not root. They differ only on a platform that is neither `nt` nor has
`geteuid`. Answerable with grounds (test modules do not import each other
here); named so the next third copy is a choice.

## Regression tests to plant

- `tests/test_arm_check.py`: a `RuntimeError` parameter for the refusal's
  put-back, in the block under ⬜ 1.

## Facts for the evidence ledger

- R1's row at the target already names `CANNOT_LOCK` and the
  interrupt-chaining clause; `evidence-check` holds it (below). Nothing to add
  from this round unless ⬜ 1's case is planted, in which case the case's
  anchor joins R1.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The `RuntimeError` arm of the put-back guard is held by no case, and its line ends `stops here.. No arm was measured.` | `skills/verify/scripts/arm_check.py:977`, `:1271` | open | Executed: the guard narrowed to `except OSError` leaves the module green, 93 passed. In-process, `restore` raising as it does on a read-back mismatch gives exit 2 and the output, and the doubled period. Reachable through the grandchild shape deferred to #313 |
| ⬜ 2 | Two comments name the loop's first write as what makes the pass path safe; it is the outer `finally`'s `restore` | `skills/verify/scripts/arm_check.py:982-983` | open | Executed: under the pass-only swallow mutant a locked or replaced module still ends in its traceback at exit 1 with `--only` selecting nothing, where the loop writes nothing. The same sentence is at `tests/test_arm_check.py:2072-2073` |
| ⬜ 3 | The case's parameters are a hand-written list beside `CHANGES_THE_MODULE`; a shape added to the dict is never run | `tests/test_arm_check.py:2008-2020` | open | Read: it was `sorted(CHANGES_THE_MODULE)` before `8f231570` |
| ⬜ 4 | `CANNOT_LOCK` restates `CHMOD_STOPS_A_WRITE` under the opposite name | `tests/test_arm_check.py:2005` | open | Read: `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:498` holds the same predicate, negated |
| 🟢 | round 2's finding 1 is closed, and its class — a refusal over a module the command left so that it cannot be put back names the error at exit 2 | `skills/verify/scripts/arm_check.py:972-990`, `:1268-1280` | confirmed | Executed: `chmod 000`, `chmod 200`, rewrite then `chmod 444`, a directory, each then exit 1: exit 2, no traceback, the error after *putting it back failed:*, the output following. Rewrite and remove: *was put back*, byte-identical |
| 🟢 | round 2's finding 2 is closed — the first run's put-back on an interrupt is held | `tests/test_arm_check.py:2117-2133` | confirmed | Executed: R2 red on all three parameters. A real SIGINT over a rewrite and over a removal left the module byte-identical, exit -2 |
| 🟢 | An interrupt over a module that cannot be put back raises the failure chained to the interrupt | `skills/verify/scripts/arm_check.py:977-987` | confirmed | Executed: a real SIGINT over a `chmod 000` module gives the `KeyboardInterrupt`, then the `PermissionError` raised during it, at exit 1. The swallow-always mutant is red on `locks it` |
| 🟢 | The pass path left unpinned, with grounds — equivalent in outcome | `skills/verify/scripts/arm_check.py:1069` | confirmed | Executed: the pass-only swallow mutant survives, 93 passed, and a locked or replaced module still ends in its traceback at exit 1 under it. The reason stated is ⬜ 2 |
| 🟢 | `CANNOT_LOCK` and the extended parameters fail on the defects they pin | `tests/test_arm_check.py:2005`, `:2021` | confirmed | Executed: red against the script at `56268bb1` on `locks it`. Red under the guard removed, swallow-always, `main`'s branch dropped, `not_put_back` not carried, R2, output not echoed |
| 🟢 | The ledger holds unscoped | `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 3201 ok, 0 drifted, 0 broken |
| ⬜ | round 1's ⬜ 7, a command that returned but left a child on the pipe | `skills/verify/scripts/arm_check.py:941-944` | deferred #313 | already deferred in round 1 |
| ❓ | `CANNOT_LOCK`'s two conditions, root and Windows, and round 2's Windows leg | `tests/test_arm_check.py:2005` | ❓ out of verified scope | No root run and no Windows machine here; both read only. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request. No leg runs as root |

## Paste-ready fixes

### ⬜ 1

In `main`, so the line never doubles a period whatever `restore` raises:

```python
                f"The command changed {args.module} during that run, and "
                f"putting it back failed: {exc.not_put_back.rstrip('.')}. "
                f"No arm was measured."
                if exc.not_put_back
```

A case holding the `RuntimeError` arm, in `tests/test_arm_check.py` after
`test_a_refused_run_leaves_the_module_as_it_was_before_the_command`:

```python
def test_a_refusal_whose_put_back_reads_back_other_bytes_says_so(
    two_arms, tmp_path, capsys, monkeypatch
):
    """Round 3, ⬜ 1. `restore` raises `RuntimeError` when the bytes it reads
    back are not the bytes it wrote, which a writer the command left behind
    reaches (#313). On a refusal that is said on the line, like an `OSError`.

    Red how: the guard narrowed to `except OSError`. Executed."""
    module_path, _ = two_arms
    probe = tmp_path / "rewrites.py"
    probe.write_text(
        "import sys\nopen(sys.argv[1], 'w').write('VALUE = 99\\n')\n"
        "print('the cases ran')\nsys.exit(1)\n",
        encoding="utf-8",
    )
    real = ARM.restore

    def reads_back_other_bytes(path, original, original_sha):
        real(path, original, original_sha)
        raise RuntimeError(f"{path} was not restored: x != {original_sha}.")

    monkeypatch.setattr(ARM, "restore", reads_back_other_bytes)
    tests = [sys.executable, str(probe), str(module_path)]
    status = ARM.main([str(module_path), "--tests", shlex.join(tests)])
    out = capsys.readouterr().out
    first = out.splitlines()[0]
    assert status == 2
    assert "putting it back failed: RuntimeError" in first, first
    assert ".." not in first, first
    assert "the cases ran" in out
```

### ⬜ 2

`skills/verify/scripts/arm_check.py:979-983`:

```python
                # A module the command left unreadable or unwritable, or
                # replaced with a directory, cannot be put back. On a refusal
                # that is said on the refusal's own line: raised from here it
                # took the line and the command's output with it, at exit 1
                # (round 2, 🟡 1). On a pass it propagates, as the outer
                # `finally`'s own restore would fail on it; on an interrupt it
                # propagates chained to the interrupt.
```

and `tests/test_arm_check.py:2072-2073`:

```python
        # (A pass that cannot put it back raises too, and the outer
        # `finally`'s restore fails on the same module, so that path is not
        # pinned.)
```

### ⬜ 3

```python
@pytest.mark.parametrize(
    "change",
    [
        pytest.param(
            change,
            marks=pytest.mark.skipif(
                CANNOT_LOCK, reason="needs a POSIX mode root obeys"
            ),
        )
        if change == "locks it"
        else change
        for change in sorted(CHANGES_THE_MODULE)
    ],
)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_arm_check.py -q -p no:xdist` in the clone at `e091150a` | 93 passed, 2 skipped, exit 0; `locks it` ran, not skipped |
| The target script, first run prints then `chmod 000`, `chmod 200`, rewrite then `chmod 444`, a directory, each then exit 1 | exit 2 in all four, no `Traceback`, the error after *putting it back failed:* (`PermissionError` three times, `IsADirectoryError` once), the output following |
| The same, first run rewrites or removes the module | exit 2, *was put back*, module byte-identical |
| The target script, passing first run that locks or replaces the module, `--only` selecting nothing and every arm | the error's traceback, exit 1, in all four |
| The same under the pass-only swallow mutant | identical: the error's traceback, exit 1, in all four |
| A real SIGINT to `arm_check.py` during a first run that rewrote, removed, or `chmod 000`-ed the module | rewrite and remove: byte-identical, exit -2. Locked: `KeyboardInterrupt`, then the `PermissionError` raised during it, exit 1 |
| The case against the script at `56268bb1` | `locks it` red, the other two pass |
| Mutants against the whole module (narrow form): guard removed, swallow always, swallow on a pass only, `main`'s branch dropped, `not_put_back` not carried, R2, output not echoed, guard narrowed to `OSError` | red on `locks it` for four; R2 red on all three; output-not-echoed red on nine; swallow-on-a-pass and narrowed-to-`OSError` survive, 93 passed |
| In-process, `restore` raising `RuntimeError` after a refusal | exit 2, the output follows, the line ends `stops here.. No arm was measured.` |
| `uvx ruff check` and `uvx ruff format --check` on the two changed Python files | exit 0 both |
| `bin/evidence-check .` unscoped in the clone at `e091150a` | exit 0, 3201 ok, 0 drifted, 0 broken |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet run by anyone. Nothing in this round needs a fix, so it has come due: the sealer's spawn |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's ⬜ 7, a command that returned but left a child on the pipe; ⬜ 1's `RuntimeError` reaches the line through the same grandchild | #313, already deferred in round 1 | the orchestrator, by adding the read-back mismatch to #313's existing comment when the round is recorded |

Needs a fix: no
Loses a record or crashes: no

## Proof block

Opened in the clone at `e091150a`: `skills/verify/scripts/arm_check.py`
(`:846-1070`, `:1250-1310`), `tests/test_arm_check.py` (`:660-715`,
`:1993-2135`), `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`
(`:494-498`), `skills/verify/SKILL.md` (`:120-136`), `.github/workflows/test.yml`
(searched), the fix range's diff of `bin/arm-check`, `skills/`, `tests/` and
`seal/`, `rounds/round-2.md` and `rounds/round-2-report.md`. Every probe and
mutant was run in the clone or beside it under this round's directory, and
deleted with it.
