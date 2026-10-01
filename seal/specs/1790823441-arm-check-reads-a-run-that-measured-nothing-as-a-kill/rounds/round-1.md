# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — review round 1

| Field | Value |
|---|---|
| Target SHA | 6bbaa4d1d7cf4e1bc3b225a5764d75af35394e5e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 707 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `ac22a0d839470c71127c64997f4bbe09047db212..fc833b5154b360227ec6fc239b567f9b21c52fa5`, 4 commits |
| Contract changes | test_a_first_run_that_timed_out_carries_what_it_printed → pytest only |
| New units | KILLS_ITSELF (depth 1); CHANGES_THE_MODULE (depth 1); test_a_refused_run_leaves_the_module_as_it_was_before_the_command (depth 1); test_a_refusal_survives_a_console_that_cannot_encode_its_output (depth 1); test_a_pair_whose_cases_print_a_byte_that_is_not_utf8_keeps_its_verdict (depth 1) |
| Needs a fix | yes — 🟡 1 (a refusal leaves a module the cases rewrote, which the base put back) and 🟡 2 (the refusal crashes on a non-UTF-8 console); 🟡 3 is fix or justify with a home named |
| Loses a record or crashes | yes — 🟡 2 ends a refusal in a traceback at exit 1, 🟡 3 crashes a run and discards every verdict measured before it, and 🟡 1 drops the module bytes `arm-check` held and leaves the cases' rewrite |
<!-- New units: bin/arm-check read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1 targets `6bbaa4d1` and the diff `a340221b..6bbaa4d1`, the whole build. It was asked to check stage 1 against `spec.md` S1–S11 and the approved plan. It was then asked to attack `arm-check` with every defect #641's four rounds found in `mutation-check`: false kills, the first run's side effects on the target, the bound held by a case, the prefix with `cwd=None` unchanged, the texts pinned with the behaviour, the ledger, and the class.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A refused run leaves the module however the cases wrote it during the first run; at the base the outer `finally` put it back, and the line still says *Nothing was written* | `skills/verify/scripts/arm_check.py:920-944` | **fixed** `47f66b2c` | fixed at 47f66b2c; Executed: P4, a command writing `VALUE = 99` and exiting 1, left the module `VALUE = 99` at the target and byte-identical at `a340221b`; fix F4 restores it, and F5 shows an untouched module is still never written |
| 🟡 2 | The refusal's output crashes on a console that is not UTF-8: U+FFFD from `_text` raises `UnicodeEncodeError`, exit 1, contradicting `_text`'s docstring; `arm_check.py` lacks the stream reconfigure five other skill scripts carry | `skills/verify/scripts/arm_check.py:1222` | **fixed** `47f66b2c` | fixed at 47f66b2c; Executed: P2 under `PYTHONIOENCODING=cp1252` printed the line and then a traceback, exit 1; exit 2 under UTF-8; fix F2 exits 2 under cp1252 |
| 🟡 3 | A pair's `text=True` strict decode turns a mutation whose cases print a non-UTF-8 byte into a traceback that discards every verdict; the output is never read | `skills/verify/scripts/arm_check.py:965` | **fixed** `47f66b2c` | fixed at 47f66b2c; Executed: P3 crashed with `UnicodeDecodeError`, exit 1, at the base and at the target; fix F3 gives both arms `killed`, exit 0. Predates the branch, and is the same class as the decode it fixed |
| ⬜ 4 | A first run killed by a signal (negative return code) is held by no case | `skills/verify/scripts/arm_check.py:939` | **fixed** `47f66b2c` | fixed at 47f66b2c; Executed: mutation Mg (`!= 0` to `> 0`) survived the module, 87 passed. Behaviour right |
| ⬜ 5 | The output a timed-out first run printed reaches `NoBaseline.output` under a case, and reaches the reader under none | `skills/verify/scripts/arm_check.py:1221-1222` | **fixed** `47f66b2c` | fixed at 47f66b2c; Executed: mutation Mi (print only when the reason starts with `exit`) survived the module. Behaviour right |
| ⬜ 6 | The SKILL timeout paragraph names a timed-out pair as what leaks a wrapper's suite; the first run leaks it the same way now | `skills/verify/SKILL.md:83` | **fixed** `47f66b2c` | fixed at 47f66b2c; Read against `run_arms` at the target. The help's sentence covers it; the paragraph does not |
| ⬜ 7 | A command that exits 0 but leaves a child holding stdout is refused as *did not return within* the bound | `skills/verify/scripts/arm_check.py:928-935` | deferred #313 | Executed: P5 printed `no baseline: the command did not return within 2.0s` at 2.0 s for `sh -c 'sleep 20 & exit 0'`. The pairs had it before the branch; the wait is #313's direct-child reach |
| 🟢 | The three shapes, a timeout, a spawn failure and non-UTF-8 output each refuse the run at exit 2 with nothing written | `skills/verify/scripts/arm_check.py:920-944`, `:1210-1223` | confirmed | Executed: P1 against real pytest (exit 5, 4, 1) at base and target; P2 default console; Python 3.9.6 refusal; module case 87 passed |
| 🟢 | The first run's bound is held by a case | `tests/test_arm_check.py` | confirmed | Executed: mutation Ma (`timeout=None` on the first run) red on the bound case alone |
| 🟢 | `clear_bytecode_cache(path, cwd=None)` reads a relative prefix against `cwd`, keeps the old reading with no `cwd`, and all three call sites pass `cwd` | `skills/verify/scripts/arm_check.py:781-834`, `:927`, `:959`, `:988` | confirmed | Executed: mutations Mb to Me each red on the `[relative]` parameter; P7 with a relative `--cwd` saw `clean` five times; M1 re-run on 3.9.6, 3.13, 3.14 |
| 🟢 | An interrupt during the first run, and a target read-only from the start, leave the module untouched | `skills/verify/scripts/arm_check.py:920-944` | confirmed | Executed: P6 SIGINT during the first run, sha256 and mtime unchanged; P8 read-only target, a traceback at base and target alike, file unchanged |
| 🟢 | The ledger holds unscoped; 0.9.5's `run_arms` row is corrected in place and its `clear_bytecode_cache` row and 0.15.1 N2 re-read | `seal/releases/0.9.5.md`, `seal/releases/0.15.1.md`, `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 3196 ok, 0 drifted, 0 broken. Read: the three notes against the diff |
| 🟢 | No other shipped script reads an exit code as a mutation verdict without a baseline | `skills/`, `hooks/`, `.github/scripts/` | confirmed | Executed: `git grep` over every `returncode` reader; each reads a git or setup step's status |
| ❓ | The Windows leg: `HANG_BOUND = 1.0` under `-n auto`, and 🟡 2's cp1252 pipe as it occurs there | `tests/test_arm_check.py`, `skills/verify/scripts/arm_check.py:1222` | ❓ out of verified scope | No Windows machine here; 🟡 2 was reproduced with `PYTHONIOENCODING`. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request |

## Paste-ready fixes

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
```python
                    run = subprocess.run(
                        tests,
                        cwd=cwd,
                        capture_output=True,
                        env=env,
                        timeout=timeout,
                    )
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 7, a command that returned but left a child on the pipe is refused as *did not return* | #313, the bound that reaches the direct child only | the orchestrator, by adding this shape to #313 as a comment when the round is recorded |
