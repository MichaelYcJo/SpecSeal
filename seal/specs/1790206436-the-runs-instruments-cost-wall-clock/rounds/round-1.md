# 1790206436-the-runs-instruments-cost-wall-clock — review round 1

| Field | Value |
|---|---|
| Target SHA | 01e5a25fb2cf61e7efd49a4cd35b8b600283df86 |
| Written late | no |
| Ran by | warden on Fable 5.1 |
| PR | 549 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `c698def6c8a90e886201f4278ca3d4f924c9a4e9..5bf1716fb060b5bb460812267a9d8fa733f03d73`, 1 commit |
| Contract changes | none |
| New units | test_a_flag_only_the_trees_copy_knows_still_reaches_it (depth 1) |
| Needs a fix | yes — 🟡 1, the redirect decided after `parse_args`; a justification in its place is acceptable if the smith holds that no branch adds a flag the sealer types |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 was asked to review the whole branch at 01e5a25f against `release/v0.15.1` (9f846733): spec compliance first against `spec.md`'s fifteen scenarios and `plan.md`'s gate table, then quality, in a clone under the round's own directory, narrow runs only, with the smith's handoff before round 1 as the account to audit rather than restate — the redirect branch in `broad_gate.py#main`, `caller_decided`'s heuristic, `add_xdist` after `ensure`, the five `#gate` re-read notes and the fragment's P2 row named as the places to open first.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the redirect is decided after `parse_args`, so an argument only the tree's copy knows is refused by the invoking copy and the tree's copy never runs | `skills/verify/scripts/broad_gate.py:1984` | **fixed** `5bf1716f` | fixed at 5bf1716f — `broad_gate.py#main` decides the redirect from `parse_known_args` and parses fully only on the path that runs here; `test_a_flag_only_the_trees_copy_knows_still_reaches_it` red at 01e5a25f (`assert 2 == 3`, `unrecognized arguments`, stub never ran), green after; fragment row G1's note says the vector reaches the tree's copy whatever this copy's parser knows; executed: stub-gate fixture, `--new-flag-only-the-tree-knows` → exit 2, `unrecognized arguments`, no stub output; without the flag → exit 3 and the stub's vector |
| ⬜ 2 | `caller_decided` does not recognise a clustered `-qn 2` or `-p=no:xdist`, so the caller's count is overridden or `-n auto` reaches a run with the plugin off | `.github/scripts/run_tests.py:193` | **fixed** `5bf1716f` | fixed at 5bf1716f — `caller_decided` recognises `-pno:xdist` and `-p=no:xdist`, the A4 case parametrised with the new spelling and seen red first; the docstring names the clustered `-qn 2` form as outside the list (`-rn` is a `-r` value) and records that pytest 9.1.1 itself refuses `-p=no:xdist` (`Error importing plugin "=no:xdist"`), so withholding `-n auto` there adds no second failure to an already failing command; executed: both spellings return `False`; neither is a spelling A4 names |
| ⬜ 3 | the capture example and the sealer's capture file redirect into a directory nothing guarantees exists | `skills/verify/SKILL.md:430` | **fixed** `5bf1716f` | fixed at 5bf1716f — `skills/verify/SKILL.md`'s example makes the capture directory first (`mkdir -p "$(dirname "$out")"`); `agents/sealer.md` §The command says the same of the capture file; read; the redirect fails before the command runs, so nothing is lost and one call is spent |
| ⬜ 4 | *the round you are* reads as an unfinished clause | `agents/warden.md:42` | **fixed** `5bf1716f` | fixed at 5bf1716f — `agents/warden.md`: *the round you are* → *the round you are in*; read; prose only |
| ⬜ 5 | the root is resolved twice per run, once in `main` and once in `gate` | `skills/verify/scripts/broad_gate.py:1992` | answered | `phases/phase-2.md`'s grounds stand: resolving the root once more in `main` costs one `git rev-parse` subprocess and keeps `gate`'s signature and the structural count of `args.base` reads; no change; read; `phases/phase-2.md` records the choice; one extra subprocess |
| 🟢 | A1–A6: the runner installs xdist on both strategies and into an adopted `.venv`, appends `-n auto` after the caller's arguments unless they decided or the install failed, and no loaded document states the serial figure | `.github/scripts/run_tests.py:76`, `:113`, `:408` | confirmed | executed: the new cases `8 failed, 1 passed` against the base runner and green at the target; `git grep` finds no carrier of the figure outside `seal/` and `CHANGELOG.md` |
| 🟢 | A7–A10: the tree's copy runs in place of the invoking one with the vector as parsed, the self check stops a loop, the `gate` row and the running line are on every run past root resolution | `skills/verify/scripts/broad_gate.py:278`, `:1715`, `:1992` | confirmed | executed: the new gate cases `7 failed, 2 passed` against the base gate and green at the target; the stub probe above |
| 🟢 | A11–A14: the three definitions carry the pinned sentences, and `/tmp/run.txt` is gone | `agents/sealer.md:75`, `agents/warden.md:40`, `skills/verify/SKILL.md:430` | confirmed | read against the files; the new module and the five prose pins green in my run |
| 🟢 | the `gate` divergence and the R6 divergence are recorded with grounds, and the eighteen re-stamped rows carry a dated re-read note that matches what the diff moved | `seal/ledger.md`, `overview.md` §*Where spec and implementation diverged* | confirmed | read: 18 `Re-read 2026-09-24 in work item 1790206436` notes in the diff; the five `gate` notes say *one argument added to the `panel` call*, which is the change |
| ❓ | the full suite, the repository-wide lint and the typecheck over this branch, and M1's second reading | the sealer's run | ❓ out of verified scope | not this round's to run (§2); the sealer, spawned with this tree's absolute `bin/broad-gate` because the installed 0.15.0 copy has no redirect |
| ❓ | the Windows paths — `Lib/site-packages/xdist`, the `.cmd` twin passing `%*` into a runner that appends `-n auto`, `under()` across drives | `.github/scripts/run_tests.py:106`, `skills/verify/scripts/broad_gate.py:302` | ❓ out of verified scope | built for and not executed here; CI's `windows-latest` leg at the pull request |

## Paste-ready fixes

```python
    # The redirect is decided from `parse_known_args`, before this copy's
    # parser can refuse an argument only the tree's copy knows: a flag added
    # to the gate is a change to the gate, and the copy that predates it must
    # not be the one that answers (#475). `--base` is still required here, so
    # a call with no base is refused by the same parser as before. The gated
    # tree's own copy runs in place of this one with the same argument
    # vector, under the same interpreter, with inherited streams; its exit
    # code is this run's. `args.base` is not read here: the one read stays
    # in `gate`, and the child resolves it for itself.
    known, _unknown = parser.parse_known_args(argv)
    root = repo_root(os.path.abspath(known.root or os.getcwd()))
    if root is not None:
        shipped = shipped_gate(root)
        if shipped is not None:
            sys.stderr.write(redirect_line(root, shipped) + "\n")
            handed = sys.argv[1:] if argv is None else list(argv)
            return subprocess.run([sys.executable, shipped, *handed]).returncode
    args = parser.parse_args(argv)
    if root is not None:
        sys.stderr.write(running_line(root) + "\n")
```
```python
def test_a_flag_only_the_trees_copy_knows_still_reaches_it(repo, tmp_path):
    """A7's other half. A branch whose gate grows an argument is inside
    #475's class — measured by the copy that predates the change — so the
    redirect is decided before this copy's parser can refuse what only the
    tree's copy accepts. Red at 01e5a25f: exit 2, `unrecognized arguments`,
    and the stub never ran."""
    stub = repo / "skills" / "verify" / "scripts" / "broad_gate.py"
    stub.parent.mkdir(parents=True)
    stub.write_text(STUB_GATE, encoding="utf-8")
    out = run_gate(repo, "--new-flag-only-the-tree-knows", keep=tmp_path / "out")
    assert out.returncode == 3, f"{out.stdout}\n{out.stderr}"
    assert "'--new-flag-only-the-tree-knows'" in out.stdout, (
        f"the tree's copy was not handed the flag only it knows:\n{out.stdout}"
    )
    assert "unrecognized arguments" not in out.stderr, out.stderr
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over eleven modules in the clone — the four phase modules, `test_the_gate_asks_the_range_ci_will_ask.py`, `test_a_document_that_names_a_script_says_how_to_reach_it.py`, `test_no_real_identifiers.py`, `test_docs_line_wrap.py`, `test_one_word_one_meaning.py`, `test_a_moved_rule_leaves_its_definition.py`, `test_the_rules_have_one_owner.py`, with `-q -p no:cacheprovider`, exit read directly | `590 passed, 7 skipped in 34.97s`, exit 0; the clone's `.venv` was built cold by this branch's runner with xdist in it and the run went `-n auto` |
| the base `run_tests.py` (`9f846733`) swapped into the clone, the module's new cases run, the file restored with `git checkout` | `8 failed, 1 passed` — the inverted pin, both A1 build cases, both A2 cases, A3, A5, A6 |
| the base `broad_gate.py` (`9f846733`) swapped in, the new gate cases run, the file restored | `7 failed, 2 passed` — A7, the self case, A9/A10 sealed run and refusal, the row's value and width, the historical panel |
| a probe script driven from Python (§8): a git repository with a stub gate at `skills/verify/scripts/broad_gate.py` printing its vector and exiting 3; this tree's gate over it with `--base base --root <fixture>`, then again with `--new-flag-only-the-tree-knows`; the fixture and the script removed after | without the flag: exit 3, `STUB ['--base', 'base', '--root', …]`, the redirect line on stderr; with the flag: exit 2, `broad-gate: error: unrecognized arguments: --new-flag-only-the-tree-knows`, no stub output |
| `caller_decided` called on `["-qn", "2"]`, `["-p=no:xdist"]`, `["tests/x.py", "-n", "2"]`, `["--pdbcls=…"]` | `False`, `False`, `True`, `False` |
| `git grep -E "five minutes\|five-minute\|thirteen minutes\|13 minutes"` over tracked files outside `seal/` and `CHANGELOG.md` | no carrier about the suite (hits are #36's prompt story, `payload_meter.py`'s cache and unrelated prose) |
| `git status --short` in the clone after the swaps | clean |
| the full suite, the repository-wide lint and the typecheck over this branch (the broad gate) | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal/ledger.md`'s R6 row of `1788632199` still says *five-minute suite* in its clause cell | already deferred in `overview.md` §*Not done* to `seal/follow-up.md`'s row on a figure stated with no moment | the repository owner |
