# Round 2 report — 1790206436-the-runs-instruments-cost-wall-clock

The verifying round. Target SHA `424b097c` on
`fix/337-the-runs-instruments-cost-wall-clock`, base `release/v0.15.1`
(`9f846733`). The diff under review is round 1's fix range
`c698def6..5bf1716f` (one commit, `5bf1716f`), read against round 1's record
and report. Reviewed in a `git clone --no-local` at
`<scratchpad>/<work-item-id>/round-2/clone`; the clone was restored with
`git checkout` after each swap and `git status --short` was clean at the end.
The one probe script was deleted after its run, and so was its fixture.

Carried from round 1 rather than re-established: the coordinates of `main`,
`shipped_gate`, `caller_decided` and the A7 stub case, and the fact that
`args.base` is read once, in `gate`. Re-derived here: every verdict on the
five rows round 1 opened.

## What the fix pass claimed, and what the code does

**Round 1's finding 1 — the redirect decided after `parse_args`.** Claimed:
`main` decides the redirect from `parse_known_args` and parses fully only on
the path that runs here, with `--base` still required. The code at
`skills/verify/scripts/broad_gate.py:1996`–`:2004` does exactly that. `known`
comes from `parse_known_args(argv)`, the root is resolved from `known.root`,
and where `shipped_gate` names a file the redirect returns before
`parser.parse_args(argv)` is reached. `handed` is still
`sys.argv[1:] if argv is None else list(argv)`, the original vector and not
the parsed one, so the tree's copy receives the unknown flag in the position
it was typed. `running_line` is written after the full parse on the path that
runs here, as before.

**Executed**: `test_a_flag_only_the_trees_copy_knows_still_reaches_it` passes
at the target. With `01e5a25f`'s `broad_gate.py` swapped in, it fails with
`assert 2 == 3` and `broad-gate: error: unrecognized arguments:
--new-flag-only-the-tree-knows` in the captured stderr. The fix pass's
red-first claim holds.

**What an unknown flag does on the non-redirect path.** Where the tree ships
no copy, or the running file is the tree's copy, `parse_args` still refuses
an unknown flag with exit 2. That is right. There is no other copy that could
know the flag, so the refusal comes from the only parser present and says so
in argparse's own words, as it did before the branch. The tree's own copy is
the case that matters here: it finds itself by realpath, parses fully, and
refuses a flag it does not know. That is the behaviour a gate should have.

What the fix does not reach is finding ⬜ 6 below. The pre-parse is the full
parser, so everything it can judge about the arguments it *does* know is
still judged by the invoking copy before the redirect.

**Round 1's finding 2 — `caller_decided`.** Claimed: `-p=no:xdist` is
recognised, the A4 case is parametrised with it and was seen red first, and
the docstring names the clustered form as outside the list and records
pytest's own refusal. The code at `.github/scripts/run_tests.py:208`
compares against both spellings. **Executed**: with `c698def6`'s runner
swapped in, `test_the_callers_own_choice_wins` goes `1 failed, 8 passed`, and
the failing case is `own7`, which is `["-p=no:xdist"]`. All nine pass at the
target.

The docstring's measurement **reproduces**: pytest 9.1.1 with `-p=no:xdist`
exits 1 with `ModuleNotFoundError: No module named '=no:xdist'` raised
through `Error importing plugin`, while `-p no:xdist` as two tokens exits 0.
The docstring's cluster claim, that a clustered count is overridden by a
later `-n auto`, was checked on a plain argparse parser with a counting `-q`
and a storing `-n`: `-qn 2 -n auto` parses to `numprocesses='auto'`. That is
argparse's rule and not a run of pytest itself, so it is labelled read-backed
rather than a pytest measurement.

**Round 1's finding 3 — the capture directory.** `skills/verify/SKILL.md:430`
now binds `out` and runs `mkdir -p "$(dirname "$out")"` before the redirect,
and `agents/sealer.md:142`–`:145` says the directory is made first. The class
was enumerated with `git grep '<scratchpad>/<work-item-id>'` over `agents`,
`skills`, `docs` and `CONTRIBUTING.md`, which finds four mentions. The two
that are redirects are the two fixed. The other two are the warden's clone
path, which `git clone` creates together with its leading directories, and
the directory the warden's probes sit under, which exists once the clone
does. That last point is read, not measured: this round made its directory
before cloning.

**Round 1's finding 4 — *the round you are in*.** `agents/warden.md:42`
reads as intended.

**Round 1's finding 5 — the root resolved twice.** Answered, and the answer
still stands: `main` resolves the root once more, `gate`'s signature is
unchanged, and `test_the_gate_asks_the_range_ci_will_ask.py` passed in this
round's run.

**The ledger.** The fragment's anchors for `#main`, `#caller_decided`, the A4
case, `agents/sealer.md#"## The command"` and
`agents/warden.md#"## Where you work"` moved to new hashes. The four shared
rows (S3, the absent-row refusal row, R7 and G3's shared twin) each carry a
second dated sentence naming what moved. Both sentences match the diff: the
sealer's section changed only in the capture sentence, and the warden's
section changed only in one word. G1's note now says the vector reaches the
tree's copy whatever this copy's parser knows, which is true for unknown
flags and not wider; ⬜ 6 names the edge. **Executed**:
`bin/evidence-check --strict` in the clone exits 0 with `1702 ok · 0 drifted
· 0 broken`.

## New in this round

### ⬜ 6 · the pre-parse still judges the arguments this copy knows before the redirect

`skills/verify/scripts/broad_gate.py:1996`. The redirect is decided by
`parser.parse_known_args(argv)` on the *full* parser. `parse_known_args`
passes unknown flags through, but it still acts on every flag it knows before
the redirect is reached.

**Executed**, over a fixture repository that ships a stub gate:

- `--base b --root <fixture> -h` exits 0 and prints the invoking copy's
  usage. The stub never runs. Someone asking the tree's gate which flags it
  takes is shown the older copy's list.
- `--root <fixture> --new-flag` with no `--base` exits 2 with
  `the following arguments are required: --base`. The stub never runs.
- `--root <fixture> --r x` exits 2 with `ambiguous option: --r could match
  --root, --record`, which is this copy's option set and not the tree's.

A value-type refusal (`--scale` given a non-number) falls the same way by
reading, and was not run.

Why this stays ⬜: the sealer's command is pinned as `broad-gate --base
<base> --record <item>`, and none of the three reaches it. The fix pass's
comment also says `--base` stays required *on purpose*. So the release ships
no defect a documented caller meets. The residue is still inside #475's
class, just narrower: a branch that changes what an existing flag means, or
makes `--base` optional, is judged by the copy that predates the change. The
next person to widen the gate's interface would need to know that. Either a
sentence in the `main` comment naming the three, or a pre-parser that knows
only `--root`, closes it. The second is fenced below in case it is wanted. It
changes which copy refuses a missing `--base` over a tree that ships its own
copy, and the tree's copy requires it too.

### ⬜ 7 · the spec and the plan still say the redirect comes after `parse_args`, and the overview does not record the change

`seal/specs/1790206436-the-runs-instruments-cost-wall-clock/spec.md:127`
(*`main` calls it after `parse_args`*) and `plan.md:71` (*the redirect goes
between `parse_args` and `gate`*) describe the shape round 1 found wanting.
`overview.md` §*Where spec and implementation diverged* has four rows and
none for this one. The code, the fragment's G1 note and the `main` comment
all say `parse_known_args`, so only the frame's two documents still say
otherwise. This concerns the run's paperwork and not the tool, so it is a
correction and is left out of `Needs a fix`. One row in the divergence table
closes it.

## Regression tests to plant

None. Round 1's two cases are planted, and this round saw both red against
the code they were written for.

## Facts for the evidence ledger

- G1's note, *the vector reaches the tree's copy whatever this copy's parser
  knows*, holds for flags this copy does not know. For `-h`, a missing
  `--base`, an ambiguous abbreviation and a known flag's value type, the
  invoking copy answers first (⬜ 6). If ⬜ 6 is answered with a sentence
  rather than a change, the note should say the same.
- `caller_decided`'s docstring measurement of `-p=no:xdist` reproduces on
  pytest 9.1.1 and pytest-xdist 3.8.0 (exit 1, `Error importing plugin`).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's fix-or-justify finding 1 is closed — the redirect is decided from `parse_known_args` and the full parse happens only on the path that runs here | `skills/verify/scripts/broad_gate.py:1996` | verified | executed: `test_a_flag_only_the_trees_copy_knows_still_reaches_it` green at `424b097c`, red with `01e5a25f`'s gate swapped in (`assert 2 == 3`, `unrecognized arguments`); read: `handed` is the original vector; an unknown flag on the non-redirect path still exits 2, which is right because no other copy exists to know it |
| 🟢 | round 1's finding 2 is closed — `caller_decided` recognises `-p=no:xdist`, and the docstring states the clustered form and pytest's own refusal | `.github/scripts/run_tests.py:208` | verified | executed: A4 `1 failed, 8 passed` with `c698def6`'s runner (`own7` = `-p=no:xdist`), `9 passed` at target; pytest 9.1.1 `-p=no:xdist` exits 1, `Error importing plugin`, reproduced |
| 🟢 | round 1's finding 3 is closed — the capture directory is made before the redirect in both places | `skills/verify/SKILL.md:430`, `agents/sealer.md:142` | verified | read; class enumerated with `git grep`, four mentions, the two redirects both fixed, the other two made by `git clone` |
| 🟢 | round 1's finding 4 is closed — *the round you are in* | `agents/warden.md:42` | verified | read |
| 🟢 | round 1's finding 5 — the root resolved twice — stays answered | `skills/verify/scripts/broad_gate.py:1997` | answered | read: `gate`'s signature unchanged; executed: `test_the_gate_asks_the_range_ci_will_ask.py` green |
| 🟢 | the five drifted units re-stamped, and the four shared rows carry a second dated sentence that matches the diff | `seal/ledger.md`, `seal/ledger/1790206436-the-runs-instruments-cost-wall-clock.md` | verified | read against the word diff; executed: `bin/evidence-check --strict` exit 0, `1702 ok · 0 drifted · 0 broken` |
| ⬜ 6 | the pre-parse is the full parser, so `-h`, a missing `--base`, an ambiguous abbreviation and a known flag's value type are still judged by the invoking copy before the redirect | `skills/verify/scripts/broad_gate.py:1996` | open | executed: over a stub-gate fixture, `-h` exits 0 with this copy's usage, no `--base` exits 2, `--r` exits 2 ambiguous, the stub never runs; the sealer's pinned command reaches none of them |
| ⬜ 7 | `spec.md` and `plan.md` still say the redirect comes after `parse_args`, and `overview.md`'s divergence table has no row for the change | `seal/specs/1790206436-the-runs-instruments-cost-wall-clock/spec.md:127`, `plan.md:71`, `overview.md` §*Where spec and implementation diverged* | open | read; paperwork correction, not counted in `Needs a fix` |
| ❓ | the full suite, the repository-wide lint and the typecheck over this branch, and M1's second reading | the sealer's run | ❓ out of verified scope | not this round's to run (§2); the sealer, spawned with this tree's absolute `bin/broad-gate` |
| ❓ | the Windows paths — `Lib/site-packages/xdist`, the `.cmd` twin passing `%*`, `under()` across drives | `.github/scripts/run_tests.py:106`, `skills/verify/scripts/broad_gate.py:302` | ❓ out of verified scope | built for and not executed; CI's `windows-latest` leg at the pull request |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal/ledger.md`'s R6 row of `1788632199` still says *five-minute suite* in its clause cell | already deferred in round 1, to `overview.md` §*Not done* and `seal/follow-up.md`'s row on a figure stated with no moment | the repository owner |

## Paste-ready fixes

### ⬜ 6 — optional; a pre-parser that knows only `--root`

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

### ⬜ 7 — one row for `overview.md` §*Where spec and implementation diverged*

```
| the redirect's place in `main` | `spec.md` §*Data & interfaces* and `plan.md` phase 2: after `parse_args`; round 1 measured an unknown flag refused by the invoking copy | decided from `parse_known_args`, the full parse only on the path that runs here | a flag only the tree's copy knows is inside #475's class (round 1's finding 1); `--base` stays required |
```

Needs a fix: no

Loses a record or crashes: no

The two open rows are ⬜: one prose-or-optional change to the pre-parse and
one paperwork correction. Neither counts toward `Needs a fix`. **With this
round, the broad gate comes due. What is owed is the sealer's spawn**, with
this tree's absolute `bin/broad-gate`, because the installed 0.15.0 copy has
no redirect.

## Proof

Files opened in the clone at `424b097c`:
`seal/specs/1790206436-the-runs-instruments-cost-wall-clock/rounds/round-1.md`,
`rounds/round-1-report.md`, `overview.md` (§*Where spec and implementation
diverged* through the end), `spec.md:120`–`:130`, `plan.md:68`–`:74`; the
fix diff `c698def6..5bf1716f` for `.github/scripts/run_tests.py`,
`agents/sealer.md`, `agents/warden.md`, `skills/verify/SKILL.md`,
`skills/verify/scripts/broad_gate.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py`, and the word
diff of `seal/ledger.md` and the fragment;
`skills/verify/scripts/broad_gate.py` (`main` whole, `repo_root`,
`shipped_gate`); `.github/scripts/run_tests.py` (`caller_decided` whole);
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (`run_gate`,
`STUB_GATE`, the A7 case); `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:744`–`:760`;
the fragment's P2 and G1 rows; `skills/code-review/scripts/chain_check.py:410`–`:457`
(the verdict vocabulary). Executed: the runs in the table above. Not run: the
broad gate.
