# 1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout — review round 4

| Field | Value |
|---|---|
| Target SHA | a86101f5332420645509eb65f545e88f534a639e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 698 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `a86101f5332420645509eb65f545e88f534a639e..2d63e8af555a5105411d0bdd2d03fa8696fe110b`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 4 is the verifying round after the run's one reopening, so it ends the run. It targets `a86101f5` and verifies round 3's fix range `db15439f..37b3646f`, two commits. It was asked whether 🟡 15, ⬜ 16 and ⬜ 17 are closed with their class. That meant re-running probe P5, and checking that *The break was never written* is true in every baseline exit and that the suffix's boundary is pinned. It was also asked whether each extended parameter fails on the defect it pins.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 3's finding 15 is closed — an interrupt in the baseline leaves the file as the line says, and the restore covers every baseline exit | `skills/verify/scripts/mutation_check.py:319-378` | confirmed | Executed: P5 in process and P5 with a real SIGINT to the wrapper's group, each exit 2 with the interrupt line and the file back at `VALUE = 1`; Ma (round 3's reach put back) red on the interrupt case's `[baseline]` alone |
| 🟢 | round 3's note 16 is closed — the suffix's sentence boundary is pinned in both cases that reach it | `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py:808-811`, `:1107-1110` | confirmed | Executed: M6 (round 2's clause form) red on the cannot-start case and on the bound case `[baseline]`; it survived the module in round 3 |
| 🟢 | round 3's correction 17 is answered — L2's note has its full stop and bold opening | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L2 | confirmed | Read: every note boundary in L1, L2, L3, L4 and L7 ends in a full stop |
| 🟢 | `The break was never written` is true in every baseline exit, and pinned | `skills/verify/scripts/mutation_check.py:325-346` | confirmed | Executed: red, timed out, cannot start and interrupt, each with cases that rewrite the target; the file ended `VALUE = 1` each time; Md red on all three no-baseline parameters |
| 🟢 | L1, L2, L3, L4 and L7's round 3 notes are true of the fix range | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` | confirmed | Read against the diff; L7's two mutations reproduced as M6 and Md |
| ⬜ 18 | The restore after a `no baseline` exit and after a baseline timeout is held by no case; only the interrupt exit is pinned | `skills/verify/scripts/mutation_check.py:365` | deferred #706 | #706 — The run ended capped; #706 carries the regression case from this round, red under Mb and Mc; Executed: Mb and Mc SURVIVED the module; the proposed case was green at the target and red under each. Behaviour right, no printed line claims it |
| ⬜ 19 | `main`'s interrupt comment still says an interrupt in the baseline wrote nothing, and that the restore runs only once the break was written | `skills/verify/scripts/mutation_check.py:445-450` | deferred #706 | #706 — A comment behind the code since 647c3395; filed with ⬜ 18; Read: false since `647c3395`; a comment, so no line a person reads changes |
| ⬜ 20 | `not restored` is described as a file that may still hold the break, and a baseline exit whose restore fails now reaches it | `skills/verify/SKILL.md:157-158`, `skills/verify/scripts/mutation_check.py:39` | deferred #706 | #706 — Two descriptions of not restored behind the code; the printed line is true; filed with ⬜ 18; Executed: cases that rewrite and chmod the target, then exit 1, print `not restored`, exit 2, file `VALUE = 99`; the printed line is true and asks for the right act |
| 🟢 | The ledger holds unscoped | the whole tree | confirmed | Executed: `bin/evidence-check .` exit 0, 3223 ok, 0 drifted, 0 broken |

## Paste-ready fixes

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
```python
    except KeyboardInterrupt:
        # Reached only after `run_cases` ended what it started and
        # `mutation_run`'s `finally` put back any bytes that differ -- the
        # break, or what the baseline's cases wrote before any break existed
        # (round 3, finding 15). A failed restore raises `NotRestored` instead,
        # and is reported above, so the sentence holds wherever the interrupt
        # lands.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/mutation_check.py:255` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:302-306` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:355-383` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:190-192` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/mutation_check.py:107` | round 1's 🟡 5 — fixed |
| round-1 | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` | round 1's ⬜ 6 — answered |
| round-1 | `skills/verify/scripts/arm_check.py:783-789` | round 1's ⬜ 7 — answered |
| round-1 | `skills/verify/SKILL.md` §*`mutation-check` asks condition 2 of one unit* | round 1's ⬜ 8 — fixed |
| round-1 | `agents/`, `skills/`, `docs/`, `templates/` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_arm_check.py:1066-1131` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.6.0.md`, `0.8.1.md`, `0.9.5.md`, `0.12.0.md`, `0.15.1.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L5 | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/mutation_check.py#run_cases` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/mutation_check.py:207-208`, `bin/mutation-check.cmd` | round 1's ❓ — out of verified scope |
| round-2 | `skills/verify/scripts/mutation_check.py:313-328` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:337-350` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:428-438` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:196-267` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:116`, `:244` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/plan.md:164` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/mutation_check.py:319` | round 2's 🟡 10 — fixed |
| round-2 | `agents/smith.md:271-276`, `bin/mutation-check:11-15` | round 2's ⬜ 11 — fixed |
| round-2 | `skills/verify/scripts/mutation_check.py:320-328`, `:418-427` | round 2's ⬜ 12 — fixed |
| round-2 | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md:42` | round 2's ⬜ 13 — answered |
| round-2 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-8` | round 2's ⬜ 14 — fixed |
| round-2 | `skills/verify/scripts/mutation_check.py:218-221`, `bin/mutation-check.cmd` | round 2's ❓ — out of verified scope |
| round-3 | `skills/verify/scripts/mutation_check.py:347-370` | round 3's 🟢 — confirmed |
| round-3 | `agents/smith.md:272-278`, `bin/mutation-check:11-16` | round 3's 🟢 — confirmed |
| round-3 | `skills/verify/scripts/mutation_check.py:320-329` | round 3's 🟢 — confirmed |
| round-3 | `skills/verify/scripts/mutation_check.py:318-338`, `:443-449` | round 3's 🟡 15 — fixed |
| round-3 | `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py:804`, `:1100` | round 3's ⬜ 16 — fixed |
| round-3 | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` Q5 | round 3's 🟢 — confirmed |
| round-3 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-9` | round 3's 🟢 — confirmed |
| round-3 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L2 | round 3's 🟢 — confirmed |
| round-3 | the whole tree | round 3's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 18 — the restore after a `no baseline` exit and a baseline timeout is held by no case | rung 4: this record, named in the pull request body; the case is in the paste-ready fixes | nobody has agreed to act on it: the branch owns the unit, and the reopening bound lets this record commission nothing |
| ⬜ 19 — `main`'s interrupt comment says an interrupt in the baseline wrote nothing | rung 4: this record, named in the pull request body | nobody has agreed to act on it, for the same reason |
| ⬜ 20 — `not restored` is described as a file that may still hold the break | rung 4: this record, named in the pull request body | nobody has agreed to act on it, for the same reason |
| `skills/verify/scripts/arm_check.py`'s `run_arms` reads any non-zero exit as killed with no baseline: round 1's finding 1 class (already deferred in round 1, carried in rounds 2 and 3) | a new issue, beside #313 | the orchestrator, who files it when the pull request is opened |
