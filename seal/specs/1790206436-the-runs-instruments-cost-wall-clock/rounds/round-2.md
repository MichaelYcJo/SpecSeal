# 1790206436-the-runs-instruments-cost-wall-clock — review round 2

| Field | Value |
|---|---|
| Target SHA | 424b097c656c8d2336356b6f047c2d7dfcec2b88 |
| Written late | no |
| Ran by | warden on Fable 5.1 |
| PR | 549 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `424b097c656c8d2336356b6f047c2d7dfcec2b88..23dc3ad00c934a42e60b503d179ee31b3bb49df9`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round at round 1's fixes: the range `c698def6..5bf1716f` on `fix/337-the-runs-instruments-cost-wall-clock`, one commit, plus the record commit that closed round 1, reviewed at 424b097c. It asked whether 🟡 1 is closed — the redirect decided from `parse_known_args` before this copy's parser can refuse a flag only the tree's copy knows, the new case red with 01e5a25f's gate swapped in — whether the non-redirect path still refusing an unknown flag is right, whether `handed` is the original vector, whether ⬜ 2's docstring measurement of pytest's own refusal of `-p=no:xdist` reproduces, and whether the five re-stamped ledger units match the diff. A round that opens nothing needing a fix does not consume the cap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's fix-or-justify finding 1 is closed — the redirect is decided from `parse_known_args` and the full parse happens only on the path that runs here | `skills/verify/scripts/broad_gate.py:1996` | verified | executed: `test_a_flag_only_the_trees_copy_knows_still_reaches_it` green at `424b097c`, red with `01e5a25f`'s gate swapped in (`assert 2 == 3`, `unrecognized arguments`); read: `handed` is the original vector; an unknown flag on the non-redirect path still exits 2, which is right because no other copy exists to know it |
| 🟢 | round 1's finding 2 is closed — `caller_decided` recognises `-p=no:xdist`, and the docstring states the clustered form and pytest's own refusal | `.github/scripts/run_tests.py:208` | verified | executed: A4 `1 failed, 8 passed` with `c698def6`'s runner (`own7` = `-p=no:xdist`), `9 passed` at target; pytest 9.1.1 `-p=no:xdist` exits 1, `Error importing plugin`, reproduced |
| 🟢 | round 1's finding 3 is closed — the capture directory is made before the redirect in both places | `skills/verify/SKILL.md:430`, `agents/sealer.md:142` | verified | read; class enumerated with `git grep`, four mentions, the two redirects both fixed, the other two made by `git clone` |
| 🟢 | round 1's finding 4 is closed — *the round you are in* | `agents/warden.md:42` | verified | read |
| 🟢 | round 1's finding 5 — the root resolved twice — stays answered | `skills/verify/scripts/broad_gate.py:1997` | answered | read: `gate`'s signature unchanged; executed: `test_the_gate_asks_the_range_ci_will_ask.py` green |
| 🟢 | the five drifted units re-stamped, and the four shared rows carry a second dated sentence that matches the diff | `seal/ledger.md`, `seal/ledger/1790206436-the-runs-instruments-cost-wall-clock.md` | verified | read against the word diff; executed: `bin/evidence-check --strict` exit 0, `1702 ok · 0 drifted · 0 broken` |
| ⬜ 6 | the pre-parse is the full parser, so `-h`, a missing `--base`, an ambiguous abbreviation and a known flag's value type are still judged by the invoking copy before the redirect | `skills/verify/scripts/broad_gate.py:1996` | answered | the pre-parse uses this copy's full parser, so `-h`, a missing `--base` and an ambiguous prefix are answered by the invoking copy before any redirect; the sealer's pinned command `broad-gate --base <base> --record <item>` meets none of the three, a missing `--base` is refused identically by every copy that has ever shipped, and a `--root`-only pre-parser is a second parser to keep in step for no call anybody types. No change; executed: over a stub-gate fixture, `-h` exits 0 with this copy's usage, no `--base` exits 2, `--r` exits 2 ambiguous, the stub never runs; the sealer's pinned command reaches none of them |
| ⬜ 7 | `spec.md` and `plan.md` still say the redirect comes after `parse_args`, and `overview.md`'s divergence table has no row for the change | `seal/specs/1790206436-the-runs-instruments-cost-wall-clock/spec.md:127`, `plan.md:71`, `overview.md` §*Where spec and implementation diverged* | answered | corrected at 23dc3ad0 — the overview's divergence table gains the row for the redirect's move to `parse_known_args`; `spec.md` and `plan.md` stay as the frame that was approved, and the divergence row is where the difference is recorded; read; paperwork correction, not counted in `Needs a fix` |
| ❓ | the full suite, the repository-wide lint and the typecheck over this branch, and M1's second reading | the sealer's run | ❓ out of verified scope | not this round's to run (§2); the sealer, spawned with this tree's absolute `bin/broad-gate` |
| ❓ | the Windows paths — `Lib/site-packages/xdist`, the `.cmd` twin passing `%*`, `under()` across drives | `.github/scripts/run_tests.py:106`, `skills/verify/scripts/broad_gate.py:302` | ❓ out of verified scope | built for and not executed; CI's `windows-latest` leg at the pull request |

## Paste-ready fixes

```python
    # The redirect is decided by a parser that knows `--root` and nothing
    # else, so every other argument — `-h`, `--base`, a value's type, an
    # abbreviation — is judged by the copy that runs, not by the one that
    # predates it (#475; round 1's finding 1, round 2's finding 6).
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--root", default=None)
    known, _unknown = pre.parse_known_args(argv)
    root = repo_root(os.path.abspath(known.root or os.getcwd()))
    if root is not None:
        shipped = shipped_gate(root)
        if shipped is not None:
            sys.stderr.write(redirect_line(root, shipped) + "\n")
            handed = sys.argv[1:] if argv is None else list(argv)
            return subprocess.run([sys.executable, shipped, *handed]).returncode
    args = parser.parse_args(argv)
```
```python
def test_help_over_a_tree_that_ships_its_own_gate_is_that_copys(repo, tmp_path):
    """Round 2's finding 6. `-h` over a tree shipping its own gate is
    answered by the tree's copy; red while the pre-parse is the full parser
    (exit 0, this copy's usage, the stub never ran)."""
    stub = repo / "skills" / "verify" / "scripts" / "broad_gate.py"
    stub.parent.mkdir(parents=True)
    stub.write_text(STUB_GATE, encoding="utf-8")
    out = run_gate(repo, "-h", keep=tmp_path / "out")
    assert out.returncode == 3, f"{out.stdout}\n{out.stderr}"
    assert "'-h'" in out.stdout, out.stdout
```
```
| the redirect's place in `main` | `spec.md` §*Data & interfaces* and `plan.md` phase 2: after `parse_args`; round 1 measured an unknown flag refused by the invoking copy | decided from `parse_known_args`, the full parse only on the path that runs here | a flag only the tree's copy knows is inside #475's class (round 1's finding 1); `--base` stays required |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the new case at `424b097c`, exit read directly | exit 0 |
| `01e5a25f`'s `broad_gate.py` swapped in, the new case run, the file restored with `git checkout` | exit 1, `assert 2 == 3`, `broad-gate: error: unrecognized arguments: --new-flag-only-the-tree-knows` |
| `c698def6`'s `run_tests.py` swapped in, `-k callers_own_choice` run, the file restored | `1 failed, 8 passed`, the failure `own7` = `["-p=no:xdist"]`; at target `9 passed` |
| `bin/test` over `test_the_seal_is_taken_once_by_the_sealer.py`, `test_the_suite_has_a_command_that_is_cheap_twice.py`, `test_the_gate_asks_the_range_ci_will_ask.py`, `test_docs_line_wrap.py`, `test_no_real_identifiers.py`, `-q -p no:cacheprovider` | `280 passed in 27.03s`, exit 0 |
| `bin/test` over `test_a_parallel_agent_names_its_scratch_after_the_work_item.py`, `test_the_gate_names_every_step_ci_runs.py`, `test_a_document_that_names_a_script_says_how_to_reach_it.py`, `test_one_word_one_meaning.py`, `test_a_moved_rule_leaves_its_definition.py`, `test_the_rules_have_one_owner.py` | `312 passed, 7 skipped in 8.01s`, exit 0 |
| pytest 9.1.1 with `-p=no:xdist --co`, then with `-p no:xdist --co`, over one module | exit 1, `ModuleNotFoundError: No module named '=no:xdist'` raised as `Error importing plugin`; exit 0 |
| a plain argparse parser (`-q` counting, `-n` storing) given `-qn 2 -n auto` | `numprocesses='auto'`: the later value wins |
| a `test_tmp_*` probe script driven from Python (§8): a git fixture shipping a stub gate; this tree's gate run with `-h`, with no `--base` and an unknown flag, and with `--r x`; the fixture and the script removed after | exit 0 with this copy's usage; exit 2 `required: --base`; exit 2 `ambiguous option`; the stub ran in none |
| `bin/evidence-check --strict` in the clone | exit 0, `1702 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `git status --short` in the clone after the swaps | clean |
| the full suite, the repository-wide lint and the typecheck over this branch (the broad gate) | not yet — nobody has run it; it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:1984` | round 1's 🟡 1 — fixed |
| round-1 | `.github/scripts/run_tests.py:193` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/verify/SKILL.md:430` | round 1's ⬜ 3 — fixed |
| round-1 | `agents/warden.md:42` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1992` | round 1's ⬜ 5 — answered |
| round-1 | `.github/scripts/run_tests.py:76`, `:113`, `:408` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:278`, `:1715`, `:1992` | round 1's 🟢 — confirmed |
| round-1 | `agents/sealer.md:75`, `agents/warden.md:40`, `skills/verify/SKILL.md:430` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger.md`, `overview.md` §*Where spec and implementation diverged* | round 1's 🟢 — confirmed |
| round-1 | the sealer's run | round 1's ❓ — out of verified scope |
| round-1 | `.github/scripts/run_tests.py:106`, `skills/verify/scripts/broad_gate.py:302` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal/ledger.md`'s R6 row of `1788632199` still says *five-minute suite* in its clause cell | already deferred in round 1, to `overview.md` §*Not done* and `seal/follow-up.md`'s row on a figure stated with no moment | the repository owner |
