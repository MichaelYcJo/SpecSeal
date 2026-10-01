# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — review round 2

| Field | Value |
|---|---|
| Target SHA | dc1b0d14bf6dc70ad5e362719acc30221ae75c77 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 707 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a first run that leaves the module unreadable, unwritable or replaced by a directory ends the refusal in a traceback at exit 1) |
| Loses a record or crashes | yes — 🟡 1 crashes a refusal that `6bbaa4d1` gave at exit 2, and the line and the command's output are lost |

- [ ] Pass

## What this round was asked

Round 2 is the verifying round. It targets `dc1b0d14` and verifies round 1's fix range `ac22a0d8..fc833b51`, four commits. It was asked to re-run round 1's probes against each of its six `fixed` verdicts with the class closed: a first run that rewrites, removes or makes the module unreadable, a cp1252 console, a pair printing non-UTF-8, a signal-killed first run, and a timed-out first run's output. It was also asked to judge the smith's departure from the paste-ready block and its two surviving mutants, R2 and R10.

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

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/arm_check.py:920-944` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:1222` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:965` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:939` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:1221-1222` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/SKILL.md:83` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:928-935` | round 1's ⬜ 7 — deferred |
| round-1 | `skills/verify/scripts/arm_check.py:920-944`, `:1210-1223` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_arm_check.py` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/arm_check.py:781-834`, `:927`, `:959`, `:988` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.5.md`, `seal/releases/0.15.1.md`, `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/`, `hooks/`, `.github/scripts/` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_arm_check.py`, `skills/verify/scripts/arm_check.py:1222` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's ⬜ 7, a command that returned but left a child on the pipe, refused as *did not return*; read here: the same reach lets a wrapper's grandchild rewrite the module after the first run's put-back | #313, the bound that reaches the direct child only | the orchestrator, by adding the grandchild shape to #313's existing comment when the round is recorded |
