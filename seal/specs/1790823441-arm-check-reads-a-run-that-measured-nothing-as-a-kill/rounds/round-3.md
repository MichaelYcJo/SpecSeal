# 1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill — review round 3

| Field | Value |
|---|---|
| Target SHA | e091150ab6bf660cf2000d3565ed9e340c792b0f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 707 |
| Broad gate | 0a6093b8 against e83db346; earlier run: 6009e57f against a340221b |
| Fixes checked by | no fixes to check |
| Fix range | `e091150ab6bf660cf2000d3565ed9e340c792b0f..c09f01a561052ac09d5dae6ba546707c49d95d83`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is the verifying round. It targets `e091150a` and verifies round 2's fix range `56268bb1..bdbda4e6`, four commits. It was asked to re-run round 2's probes against its two `fixed` verdicts, with the class closed: the four unreadable or unwritable shapes, an interrupt over a rewritten or removed module, and an interrupt over a locked one. It was also asked to judge the smith's re-raise on a pass or an interrupt, and to review `CANNOT_LOCK` and the extended parameters as finding surfaces.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The `RuntimeError` arm of the put-back guard is held by no case, and its line ends `stops here.. No arm was measured.` | `skills/verify/scripts/arm_check.py:977`, `:1271` | deferred #710 | #710 — The verifying round needs no fix; #710 carries the case and the full-stop fix; Executed: the guard narrowed to `except OSError` leaves the module green, 93 passed. In-process, `restore` raising as it does on a read-back mismatch gives exit 2 and the output, and the doubled period. Reachable through the grandchild shape deferred to #313 |
| ⬜ 2 | Two comments name the loop's first write as what makes the pass path safe; it is the outer `finally`'s `restore` | `skills/verify/scripts/arm_check.py:982-983` | deferred #710 | #710 — Two comments; filed with ⬜ 1; Executed: under the pass-only swallow mutant a locked or replaced module still ends in its traceback at exit 1 with `--only` selecting nothing, where the loop writes nothing. The same sentence is at `tests/test_arm_check.py:2072-2073` |
| ⬜ 3 | The case's parameters are a hand-written list beside `CHANGES_THE_MODULE`; a shape added to the dict is never run | `tests/test_arm_check.py:2008-2020` | deferred #710 | #710 — The parametrize list; filed with ⬜ 1; Read: it was `sorted(CHANGES_THE_MODULE)` before `8f231570` |
| ⬜ 4 | `CANNOT_LOCK` restates `CHMOD_STOPS_A_WRITE` under the opposite name | `tests/test_arm_check.py:2005` | deferred #710 | #710 — The duplicated constant; filed with ⬜ 1; Read: `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:498` holds the same predicate, negated |
| 🟢 | round 2's finding 1 is closed, and its class — a refusal over a module the command left so that it cannot be put back names the error at exit 2 | `skills/verify/scripts/arm_check.py:972-990`, `:1268-1280` | confirmed | Executed: `chmod 000`, `chmod 200`, rewrite then `chmod 444`, a directory, each then exit 1: exit 2, no traceback, the error after *putting it back failed:*, the output following. Rewrite and remove: *was put back*, byte-identical |
| 🟢 | round 2's finding 2 is closed — the first run's put-back on an interrupt is held | `tests/test_arm_check.py:2117-2133` | confirmed | Executed: R2 red on all three parameters. A real SIGINT over a rewrite and over a removal left the module byte-identical, exit -2 |
| 🟢 | An interrupt over a module that cannot be put back raises the failure chained to the interrupt | `skills/verify/scripts/arm_check.py:977-987` | confirmed | Executed: a real SIGINT over a `chmod 000` module gives the `KeyboardInterrupt`, then the `PermissionError` raised during it, at exit 1. The swallow-always mutant is red on `locks it` |
| 🟢 | The pass path left unpinned, with grounds — equivalent in outcome | `skills/verify/scripts/arm_check.py:1069` | confirmed | Executed: the pass-only swallow mutant survives, 93 passed, and a locked or replaced module still ends in its traceback at exit 1 under it. The reason stated is ⬜ 2 |
| 🟢 | `CANNOT_LOCK` and the extended parameters fail on the defects they pin | `tests/test_arm_check.py:2005`, `:2021` | confirmed | Executed: red against the script at `56268bb1` on `locks it`. Red under the guard removed, swallow-always, `main`'s branch dropped, `not_put_back` not carried, R2, output not echoed |
| 🟢 | The ledger holds unscoped | `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 3201 ok, 0 drifted, 0 broken |
| ⬜ | round 1's ⬜ 7, a command that returned but left a child on the pipe | `skills/verify/scripts/arm_check.py:941-944` | deferred #313 | already deferred in round 1 |
| ❓ | `CANNOT_LOCK`'s two conditions, root and Windows, and round 2's Windows leg | `tests/test_arm_check.py:2005` | ❓ out of verified scope | No root run and no Windows machine here; both read only. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request. No leg runs as root |

## Paste-ready fixes

```python
                f"The command changed {args.module} during that run, and "
                f"putting it back failed: {exc.not_put_back.rstrip('.')}. "
                f"No arm was measured."
                if exc.not_put_back
```
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
```python
                # A module the command left unreadable or unwritable, or
                # replaced with a directory, cannot be put back. On a refusal
                # that is said on the refusal's own line: raised from here it
                # took the line and the command's output with it, at exit 1
                # (round 2, 🟡 1). On a pass it propagates, as the outer
                # `finally`'s own restore would fail on it; on an interrupt it
                # propagates chained to the interrupt.
```
```python
        # (A pass that cannot put it back raises too, and the outer
        # `finally`'s restore fails on the same module, so that path is not
        # pinned.)
```
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
| round-2 | `skills/verify/scripts/arm_check.py:958-971` | round 2's 🟡 1 — fixed |
| round-2 | `skills/verify/scripts/arm_check.py:965-968` | round 2's ⬜ 2 — fixed |
| round-2 | `skills/verify/scripts/arm_check.py:958-971`, `:1246-1259` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/arm_check.py:1270-1279` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/arm_check.py:990-1003` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_arm_check.py:1721` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_arm_check.py:1851` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/SKILL.md:83-86` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/arm_check.py:940-971` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_arm_check.py:2004`, `:2059`, `:2086` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill.md` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/arm_check.py:941-944` | round 2's ⬜ — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's ⬜ 7, a command that returned but left a child on the pipe; ⬜ 1's `RuntimeError` reaches the line through the same grandchild | #313, already deferred in round 1 | the orchestrator, by adding the read-back mismatch to #313's existing comment when the round is recorded |
