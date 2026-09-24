# Round 1 report — 1790206436-the-runs-instruments-cost-wall-clock

Target SHA `01e5a25f` on `fix/337-the-runs-instruments-cost-wall-clock`,
base `release/v0.15.1` (`9f846733`). Whole-branch review, no earlier
rounds. Reviewed in a `git clone --no-local` of the worktree under the
round's own directory (`<scratchpad>/<work-item-id>/round-1/clone`, the
path this branch's `agents/warden.md` now names); the clone is left as it
was cloned, and the one probe script was deleted after its run.

## Stage 1 — spec compliance

Every scenario row of `spec.md` §*User scenarios & acceptance* was checked
against the code, and the branch delivers all fifteen. What follows is the
audit of the smith's account, claim by claim, not the account restated.

**A1–A6 (#337, the runner).** Claimed: the inverted pin and five new cases
red at the frame commit. **Executed** here another way: the base
`run_tests.py` at `9f846733` swapped into the clone and the module's new
cases run against it gave `8 failed, 1 passed` — the inverted pin
(`test_the_whole_suite_runs_in_parallel_by_default`), both build-strategy
cases, both adopted-environment cases, the failed-install sentence, the
narrow-form tail and the absent-figure case. Green at the target (`75` of
the `590 passed` below). Read: `PACKAGES` is the one list both strategies
install (`.github/scripts/run_tests.py:76`, `:306`, `:312`); `has_xdist`
reads a directory and never a subprocess (`:113`); `add_xdist` runs after
`ensure` returned so `hide_from_git`'s exit guarantee is not widened, which
I confirmed by reading `ensure`'s `finally` and `main` (`:408`–`:419`);
the flag is appended after the caller's arguments, so the narrow form is
still the file named (`:426`–`:428`). A6 holds tree-wide, not only in the
three pinned files: `git grep` for *five minutes* / *five-minute* /
*thirteen minutes* over tracked files outside `seal/` and `CHANGELOG.md`
finds no carrier about the suite (the hits are #36's *two prompts inside
five minutes* and unrelated prose).

**A7–A11 (#475, the gate).** Claimed: nine cases red at `2e5a4729`.
**Executed**: the base `broad_gate.py` swapped in, the new gate cases gave
`7 failed, 2 passed` — the stub redirect, the self case, the sealed-run
row and line, the refusal line, the row's value and width, and
`test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before`
against the grown `HISTORICAL_ROWS` (`At index 4 diff: 'suite' != 'gate'`).
The two that stayed green are the symlink self case and the sealer prose
pin, which the module docstring's claim did not include in its count of
seven code cases — consistent. Read: `shipped_gate` is a realpath check on
one path (`skills/verify/scripts/broad_gate.py:278`–`:283`); the redirect
reads `args.root` and never `args.base` (`:1992`), and the structural count
in `test_the_gate_asks_the_range_ci_will_ask.py` held in my run; `panel`'s
`gate` row sits between `from` and the first blank (`:1715`); `gate_copy`
elides at `PANEL_VALUE_WIDTH` (`:331`); `under` answers `False` across
drives (`:302`). **The redirect has one hole, finding 🟡 1 below**: it is
decided after `parse_args`, so an argument only the tree's copy knows is
refused by the copy that predates it — the class #475 names.

**The `gate` divergence.** `spec.md` §*Data & interfaces* said `#gate` is
untouched; the code adds `gate_copy(root)` to its `panel` call (`:1953`).
`overview.md` and `phases/phase-2.md` record it with grounds I checked:
`Base` carries ref and commit only, and `panel` has no other way to learn
the root. The five rows anchored on `gate` carry a
`Re-read 2026-09-24 in work item 1790206436` note saying *one argument
added to the `panel` call … `args.base` is still read once* — that is what
the diff shows. The spec's *R6 anchors a line that does not move* was also
wrong (the unit is the whole comment block) and is recorded the same way.

**A12–A14 (#544, the names).** Read against the three files: the clone
directory and the round home (`agents/warden.md:40`–`:43`), the capture file
and the *outputs kept under* instruction (`agents/sealer.md:142`–`:148`),
the bound `out=` variable and no `/tmp/run.txt` (`skills/verify/SKILL.md:430`).
The new module's three cases passed in my run; their red-first claim (at
`5d51b319`) is §15's second form — the sentence absent — and follows from
the three files having carried none of those strings at the base, which
the diff shows.

**A15 and `plan.md` §*Operational impact*.** The installed 0.15.0 copy has
no redirect, so this branch's sealer must be spawned with this tree's
absolute `bin/broad-gate`. Stated in the plan, the overview's *Not
verified* table and the fragment's G3 row; not verifiable here.

**`CONTRIBUTING.md` §*What a change to a gate must carry*.** The four
columns are filled in `plan.md` for each phase. Test seen red: confirmed
above by execution for phases 1 and 2. Failure direction: phase 2's is
stated as *the question the merge is judged by* with the symmetric cost
named — and finding 🟡 1 is a case where the direction is not yet fully
delivered, not a case where it is wrong. Prompt budget: zero, and nothing
in the diff asks. Platform honesty: Windows built for, not executed, named
to CI's `windows-latest` in `overview.md`.

## Stage 2 — quality

### 🟡 1 · the redirect is decided after `parse_args`, so a flag only the tree's copy knows never reaches it

`skills/verify/scripts/broad_gate.py:1984`–`:1998`. `main` calls
`parser.parse_args(argv)` first and resolves the root and the shipped copy
after it. argparse refuses an unknown argument with exit 2 before that
point, so a branch whose gate adds an argument is still measured — and
refused — by the installed copy. **Executed**: over a fixture repository
shipping a stub gate (prints its `sys.argv[1:]`, exits 3), this tree's gate
with `--base base --root <fixture>` exits 3 and the stub prints the vector
as given; the same call with `--new-flag-only-the-tree-knows` appended exits
2 with `broad-gate: error: unrecognized arguments:` and the stub never
runs.

Why it matters: #475's class is *a branch that changes the gate is measured
by the copy that predates the change*, and a gate that grows an argument is
inside that class. The remedy is the one the ticket's *Not this* rejects —
spawning the sealer with an absolute path. A7 says the copy is run *with
the same argument vector*, which today holds only for the vector the older
parser already accepts. Whether a future branch will add a flag the sealer
types is a judgment the smith can answer with grounds (the sealer's command
is pinned as `broad-gate --base <base> --record <item>`); the fix is small
enough that I would rather it were in. Decide the redirect from
`parser.parse_known_args` and parse fully only on the path that runs here; NAME NOT IN TREE
`--base` stays required either way, so a call with no base is refused by
the same parser as before. The paste-ready fix is below, with a regression
case to plant beside `test_the_gate_runs_the_copy_the_tree_ships_with_the_same_arguments`
(`tests/test_the_seal_is_taken_once_by_the_sealer.py:671`).

### ⬜ 2 · `caller_decided` misses two spellings argparse accepts

`.github/scripts/run_tests.py:193`–`:199`. A short-option cluster ending in
the worker count (`-qn 2`, `-xn 2`) and the `-p=no:xdist` form are not
recognised. **Executed** by calling the function: `caller_decided(["-qn",
"2"])` and `caller_decided(["-p=no:xdist"])` both return `False`. For the
first, `-n auto` is appended after the caller's `-n 2` and argparse takes
the later value, so a caller who wanted fewer workers (the oversubscription
`plan.md` §*Operational impact* names) silently gets all of them; for the
second, `-n auto` reaches a run with the plugin off — the ticket's middle
row, exit 4. Neither spelling is one A4 names, both are unusual, and
`-p no:xdist` as two tokens is the remedy on the list, so this ships no
defect a documented caller meets. Worth a sentence in `caller_decided`'s
docstring naming the two as outside the list; adding `arg == "-p=no:xdist"`
beside line 197 is one line if wanted, while the cluster form is better left
undetected than guessed at (`-rn` is a `-r` value, not a count).

### ⬜ 3 · the capture example and the sealer's capture file assume the directory exists

`skills/verify/SKILL.md:430` and `agents/sealer.md:142`. A shell redirect
into `<scratchpad>/<work-item-id>/run.txt` fails with *No such file or
directory* before the command runs when nothing has made
`<scratchpad>/<work-item-id>/` yet — a sealer in a session where no warden
cloned there, or a fresh session. The command does not run at all, so
nothing is lost and the agent recovers with one `mkdir -p`; that is one
extra call, not a defect. A `mkdir -p "$(dirname "$out")"` line ahead of the
redirect in the fenced example would close it in the place an agent copies
from.

### ⬜ 4 · a clause in the new warden sentence reads unfinished

`agents/warden.md:42`: *the round you are* — the sentence lists three
things the path is built from and the third has no verb complement. *the
round you are in* reads as intended. Prose only; the pin reads the path, not
this clause.

### ⬜ 5 · the root is resolved twice per run

`skills/verify/scripts/broad_gate.py:1992` and `:1793`. `main` calls
`repo_root` for the redirect decision and `gate` calls it again for
itself, so `git rev-parse --show-toplevel` runs twice. `phases/phase-2.md`
records this as chosen to keep `gate`'s signature and the structural count;
the cost is one subprocess. No change asked; noted so the next reader does
not open it as an oversight.

## Regression tests to plant

| Case | Destination | What it pins |
|---|---|---|
| `test_a_flag_only_the_trees_copy_knows_still_reaches_it` | `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside the A7 case at `:671` | the stub receives `--new-flag-only-the-tree-knows` in its vector and exits 3; the invoking copy does not refuse it | NAME NOT IN TREE

## Facts for the evidence ledger

- G1's claim *runs that file … with the argument vector as given* holds
  for the vector the invoking copy's parser accepts, and no wider; after
  🟡 1 is fixed or answered, the row's note should say which.
- The fragment's P1–P3, G1–G3 and N1 rows were read against the code and
  each claim matches what the diff does; nothing to add or remove.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the redirect is decided after `parse_args`, so an argument only the tree's copy knows is refused by the invoking copy and the tree's copy never runs | `skills/verify/scripts/broad_gate.py:1984` | open | executed: stub-gate fixture, `--new-flag-only-the-tree-knows` → exit 2, `unrecognized arguments`, no stub output; without the flag → exit 3 and the stub's vector |
| ⬜ 2 | `caller_decided` does not recognise a clustered `-qn 2` or `-p=no:xdist`, so the caller's count is overridden or `-n auto` reaches a run with the plugin off | `.github/scripts/run_tests.py:193` | open | executed: both spellings return `False`; neither is a spelling A4 names |
| ⬜ 3 | the capture example and the sealer's capture file redirect into a directory nothing guarantees exists | `skills/verify/SKILL.md:430` | open | read; the redirect fails before the command runs, so nothing is lost and one call is spent |
| ⬜ 4 | *the round you are* reads as an unfinished clause | `agents/warden.md:42` | open | read; prose only |
| ⬜ 5 | the root is resolved twice per run, once in `main` and once in `gate` | `skills/verify/scripts/broad_gate.py:1992` | open | read; `phases/phase-2.md` records the choice; one extra subprocess |
| 🟢 | A1–A6: the runner installs xdist on both strategies and into an adopted `.venv`, appends `-n auto` after the caller's arguments unless they decided or the install failed, and no loaded document states the serial figure | `.github/scripts/run_tests.py:76`, `:113`, `:408` | confirmed | executed: the new cases `8 failed, 1 passed` against the base runner and green at the target; `git grep` finds no carrier of the figure outside `seal/` and `CHANGELOG.md` |
| 🟢 | A7–A10: the tree's copy runs in place of the invoking one with the vector as parsed, the self check stops a loop, the `gate` row and the running line are on every run past root resolution | `skills/verify/scripts/broad_gate.py:278`, `:1715`, `:1992` | confirmed | executed: the new gate cases `7 failed, 2 passed` against the base gate and green at the target; the stub probe above |
| 🟢 | A11–A14: the three definitions carry the pinned sentences, and `/tmp/run.txt` is gone | `agents/sealer.md:75`, `agents/warden.md:40`, `skills/verify/SKILL.md:430` | confirmed | read against the files; the new module and the five prose pins green in my run |
| 🟢 | the `gate` divergence and the R6 divergence are recorded with grounds, and the eighteen re-stamped rows carry a dated re-read note that matches what the diff moved | `seal/ledger.md`, `overview.md` §*Where spec and implementation diverged* | confirmed | read: 18 `Re-read 2026-09-24 in work item 1790206436` notes in the diff; the five `gate` notes say *one argument added to the `panel` call*, which is the change |
| ❓ | the full suite, the repository-wide lint and the typecheck over this branch, and M1's second reading | the sealer's run | ❓ out of verified scope | not this round's to run (§2); the sealer, spawned with this tree's absolute `bin/broad-gate` because the installed 0.15.0 copy has no redirect |
| ❓ | the Windows paths — `Lib/site-packages/xdist`, the `.cmd` twin passing `%*` into a runner that appends `-n auto`, `under()` across drives | `.github/scripts/run_tests.py:106`, `skills/verify/scripts/broad_gate.py:302` | ❓ out of verified scope | built for and not executed here; CI's `windows-latest` leg at the pull request |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal/ledger.md`'s R6 row of `1788632199` still says *five-minute suite* in its clause cell | already deferred in `overview.md` §*Not done* to `seal/follow-up.md`'s row on a figure stated with no moment | the repository owner |

## Paste-ready fixes

### 🟡 1

Replace the block at `skills/verify/scripts/broad_gate.py:1984`–`:1999`
(from `args = parser.parse_args(argv)` through the `running_line` write):

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

The regression case, beside the A7 case in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`; red against the
target (exit 2 and no marker), green after:

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

Needs a fix: yes — 🟡 1, the redirect decided after `parse_args`; a justification in its place is acceptable if the smith holds that no branch adds a flag the sealer types
Loses a record or crashes: no

## Proof

Files opened in the clone at `01e5a25f`: `seal/specs/1790206436-the-runs-instruments-cost-wall-clock/{spec,plan,overview,questions,routing,changelog}.md`, its `phases/phase-1.md` … `phase-4.md`, `seal/ledger/1790206436-the-runs-instruments-cost-wall-clock.md`, the diff of `seal/ledger.md`, `.github/scripts/run_tests.py` (whole file through `main`), `skills/verify/scripts/broad_gate.py` (the new block, `panel`, `gate`'s panel call, `main`), `bin/test`, `bin/test.cmd`, `bin/broad-gate`, `CONTRIBUTING.md` (the diff), `docs/release-checklist.md` (the diff), `agents/sealer.md`, `agents/warden.md`, `skills/verify/SKILL.md` (the diff and the example), `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` (the diff), `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the diff), `tests/test_the_gate_names_every_step_ci_runs.py` (the diff and the historical-panel case), `tests/test_a_parallel_agent_names_its_scratch_after_the_work_item.py`, `tests/test_the_gate_asks_the_range_ci_will_ask.py` (grep for `args.base`). Executed: the runs in the table above. Not run: the broad gate.
