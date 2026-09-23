# Implementation Plan: the run's instruments cost wall clock

<!-- seal/specs/1790206436-the-runs-instruments-cost-wall-clock/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-24 by the orchestrating session on the owner's `automation` answer, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

Four phases. Phases 1 to 3 each close one ticket and share no file; phase 4
is the records. Phase 1 makes the runner parallel by default in every
environment it builds or adopts (#337) — the largest saving in wall clock,
and every later phase's narrow runs are cheaper for it. Phase 2 makes the
gate run the copy the tree being gated ships, and say on the stamp which copy
ran (#475). Phase 3 names the warden's clone, the sealer's capture file and
the verify skill's capture example after the work item (#544). Phase 4
re-stamps the ledger rows the edits drifted, writes the fragment, the
overview and the branch's own sweep.

The mechanisms are the ones each file already has. The runner already builds
by two strategies and decides its warm path by the filesystem; the parallel
default is one more filesystem fact and one more optional step on the same
two strategies. The gate already prints one-line facts to stderr beside the
command (`moved_line`, `coverage_line`) and already resolves every arm
relative to itself; the redirect is one decision before `gate()` and one
panel row. The two definitions already hold the rule each new sentence
qualifies.

## Technical context

Existing code this builds on, constraints, and the failure scenario of the
chosen approach.

- `.github/scripts/run_tests.py#build` — `steps` is two lists, `uv venv` +
  `uv pip install --python <venv python> pytest` and `python -m venv` +
  `<venv python> -m pip install --quiet pytest`; `pytest-xdist` joins each
  install step. `#has_pytest` decides the warm path by the filesystem
  (`venv_python(venv).exists()` and a `pytest*` script); the xdist check is
  the same shape, on `lib/python*/site-packages/xdist` (POSIX) and
  `Lib/site-packages/xdist` (Windows). `#main` builds
  `[python, "-m", "pytest", *(argv or ["tests"])]` under the comment `No
  -n auto: …`, which becomes the record of why it used to be otherwise.
  `#ensure`'s `finally` writes the ignore on every exit; the install step
  phase 1 adds runs after `ensure` returned, into a directory that already
  carries its ignore, so `hide_from_git`'s guarantee is not widened.
- `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` — `fake_venv`
  (interpreter file + `pytest` script), `Recorder` (records commands, runs
  none), `test_it_does_not_pass_n_auto` (the pin to invert),
  `test_arguments_pass_through` (the exact tail), `test_a_built_environment_
  is_reused_and_never_rebuilt` (the warm-path rule the xdist check must
  keep: `fake_venv` grows the marker, or that case runs a real `uv`).
- `skills/verify/scripts/broad_gate.py#main` — parses, asks `pick_shape`,
  calls `gate(args, …)` inside `try/except Refused`. The redirect goes
  between `parse_args` and `gate`: `root = repo_root(abspath(args.root or
  cwd))`; where `shipped_gate(root)` names a file, print the gate line and NAME NOT IN TREE
  `return subprocess.run([sys.executable, path, *argv]).returncode` with
  inherited streams (`argv` is `sys.argv[1:]` where `main` was given none).
  `HERE`/`PLUGIN` are the running copy's; `os.path.realpath(__file__)`
  against `realpath(join(root, "skills/verify/scripts/broad_gate.py"))` is
  the self test. `#panel` gains `("gate", value)` between the `from` row
  and the first blank, or after `chain` — the phase decides and
  `HISTORICAL_ROWS` records it. `#gate` is untouched: five ledger rows anchor
  it and `spec.md` §*Data & interfaces* says which.
- `skills/verify/scripts/seal_stamp.py#letter` — `PANEL_WIDTH = 36`,
  `PANEL_VALUE_WIDTH = 23` in the gate; `tree 0.15.0` and `plugin 0.15.0`
  fit, and a version of nine characters still does.
- `.claude-plugin/plugin.json` — `"version"` is where the running copy's
  version is read from, relative to `PLUGIN`; `?` where unreadable.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` — `build_repo` /
  `repo` fixture, `run_gate(repo, *extra, keep=, wrapper=)` running `GATE`
  (this tree's script) with `--base base --root <repo> --shape
  --keep-output`; `sealer_text()` and the pins on `agents/sealer.md`
  (`test_the_sealer_names_the_command_it_runs` at
  `broad-gate --base <base> --record <item>`). A7's stub fixture is a
  `repo` with `skills/verify/scripts/broad_gate.py` written into it.
- `tests/test_the_gate_names_every_step_ci_runs.py#HISTORICAL_ROWS` —
  `("SEALED", "tree", "base", "from", "suite", "row", "ledger", "chain")`,
  asserted equal to `panel`'s labels for a repository with no workflow.
- `agents/warden.md` §*Where you work*, first bullet: *A `git clone
  --no-local` of the repository at the target SHA, and only there.* The
  directory sentence goes in that bullet. §*Report* already spells `/Users/x/`
  as the user path and names paths relative to the root.
- `agents/sealer.md` §*The command*: the paragraph *Where resolving moves the
  answer the gate says so and runs anyway* is the shape the gate-line
  paragraph copies; *Your stdout is a pipe* is where the capture sentence
  sits.
- `skills/verify/SKILL.md` §*The cost of the run you repeat* → *Capture
  once, filter locally*: the fenced block `uv run pytest <scope> >
  /tmp/run.txt 2>&1; tail -8 /tmp/run.txt` and the `grep` line.
- `docs/release-checklist.md` §3, the line `uv run --quiet --with pytest
  --with pytest-xdist pytest tests/ -q -n auto`.
- Pins over the definitions' prose: `tests/test_docs_line_wrap.py` (88
  columns; `agents/warden.md`, `agents/sealer.md`, `skills/verify/SKILL.md`
  are covered), `tests/test_no_real_identifiers.py`,
  `tests/test_one_word_one_meaning.py`,
  `tests/test_a_moved_rule_leaves_its_definition.py`,
  `tests/test_the_rules_have_one_owner.py`.
- The installed copy on this machine is
  `~/.claude/plugins/cache/specseal/specseal/0.15.0/bin/broad-gate` (read:
  `which broad-gate`), and it has no redirect. See *Operational impact*.

**Failure scenario of the chosen approach, six months out.**

- Phase 1: pytest or xdist changes what `-n auto` refuses beside it (a new
  incompatible flag), and `bin/test --<that flag>` exits 4 with
  `unrecognized arguments` the way the ticket's middle row did. The guard is
  a list (A4), and a list rots. What bounds it: the list is in one function
  with one parametrised case, the ticket's remedy (`-p no:xdist`) is on it,
  and the sentence A3 prints for a failed install is not the sentence for
  this — so a reader meeting exit 4 has the runner's own `-n` pass-through
  to fall back on, as today.
- Phase 2: a tree that breaks an arm seals itself green with the broken arm
  and the stamp says `tree 0.16.0`. That is the ticket's stated cost of this
  choice; the reader has the `tree` value to weigh it by, and CI runs the
  same scripts at the pull request. The other direction — a user repository
  that happens to vendor a file at `skills/verify/scripts/broad_gate.py` —
  is a fork of this plugin, whose CI runs its copy too.
- Phase 3: a definition is a sentence an agent reads, and a spawn prompt
  can still name a directory that contradicts it. Nothing in the tree reads
  a prompt. What the pin buys is that the sentence cannot be dropped without
  a case going red; what it cannot buy is a harness that scopes the
  scratchpad per agent.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #337 · install xdist and pass `-n auto` in the runner, on both build strategies and on an adopted `.venv` that lacks it | A machine with no network fails the install step on a warm call — answered by A3: a sentence and a serial run, never a refusal | **Chosen** |
| #337 · pass `-n auto` only where the filesystem shows xdist, and print a sentence otherwise; never install into an adopted environment | Every `.venv` built before this change stays serial until somebody removes it; the ticket's *same command, three meanings* stays true for a worktree beside a checkout | Refused |
| #337 · refuse an adopted `.venv` without xdist, the way a below-floor one is refused | Turns a speed-up into a suite nobody can run; the below-floor refusal exists because the suite is *wrong* there, and it is not wrong here | Refused |
| #337 · keep the runner serial and put `-n auto` into `seal/config.md`'s `Broad gate` row | The row is a person's, and `bin/test -q -n auto` fails on every fresh build until xdist is installed — the loop the ticket names, moved into a file only a person edits | Refused |
| #337 · carve the narrow form out of the default (one module runs serially) | A second rule to remember, for a fraction of a second on a small module; and the reviewer's coverage probe over one module is the run that benefits most from parallel on a big one | Refused |
| #475 · the gate re-runs the tree's own copy where the tree ships one, and the stamp carries a `gate` row | A tree that breaks an arm seals itself; named on the stamp, caught by CI with the same scripts | **Chosen** |
| #475 · keep the released copy, and have the stamp say `plugin <version>` | The measured cost stands: #497's branch is refused by a chain arm it repaired, and the run stops for a person to re-spawn with a path — the interruption `CLAUDE.md`'s first goal is against. The stamp saying so does not make the run finish | Refused |
| #475 · `agents/sealer.md` tells the sealer to look for `<root>/bin/broad-gate` and type it | The ticket's *Not this*: a rule kept in prose goes missing; and the sealer opens no repository file by its own definition | Refused |
| #475 · the redirect in `bin/broad-gate` and `bin/broad-gate.cmd` | Two files, one per platform, kept in step by hand; the Python is one file both exec and one case pins it | Refused |
| #475 · the `Broad gate` cell records the gate beside the SHA and base | The cell is parsed at the pull request and written by one path; widening it is a change to what a gate reads, argued in a work item about the record, not here | Refused; out of scope |
| #544 · the definitions name the clone directory and the capture file with the work item id and the round | A prompt that names a different directory still wins in the moment; the pin keeps the sentence, not the obedience | **Chosen** |
| #544 · the orchestrator's spawn prompt carries the directory (what the 0.15.0 run did by hand from round 2) | Met until somebody forgets, which is the shape #156 measured for the runner and #330 for a rule kept in a prompt | Refused |
| #544 · the sealer passes `--keep-output <scratchpad>/<work-item-id>/` instead of naming a capture file | Changes the pinned command; and the gate's kept directory is already unique (`broad-gate-<random>/`) — the file that collided was the sealer's own redirect, not the gate's | Refused |
| #544 · leave `skills/verify/SKILL.md`'s `/tmp/run.txt` alone as an illustration | It is the same class one file over, shared across every session on the machine rather than one; §12 says enumerate the class | Refused |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The runner is parallel by default** (#337). `build`'s two install steps name `pytest-xdist`; `has_xdist` reads the filesystem; an adopted `.venv` without it takes one install step by the same tool order, and a failed step is a sentence plus a serial run; `main` adds `-n auto` unless the caller passed `-n…`, `--numprocesses…`, `-p no:xdist`/`-pno:xdist` or `--pdb`; the comment above the command becomes the record. `test_it_does_not_pass_n_auto` inverted and seen red; cases A2, A3, A4, A5, A6 each seen red first; `fake_venv` grows the marker. `bin/test`, the runner's docstring, `CONTRIBUTING.md` §*Running the checks* and the test module's failure message stop stating a serial figure; `docs/release-checklist.md` §3's suite line becomes `bin/test -q`. The changelog fragment entry carries the before-and-after with its date and machine | `bin/test tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` with the count read directly, the inverted case red at `9f846733` and green after; one real cold build in a scratch clone of this tree — driven from Python, deleted after — reading `-n auto` in the printed command and `xdist` under site-packages; `uvx ruff check` and `format --check` over the edited files | NAME NOT IN TREE |
| 2 | **The gate runs the copy the tree ships and says so** (#475). `shipped_gate(root)`; the redirect in `main` before `gate()` with the same argument vector; the gate line on stderr on every run; the `gate` row (`tree <version>` / `plugin <version>`) in `panel`; `HISTORICAL_ROWS` grows by one with its docstring saying why; A7's stub case, A8's self case, A10's row and width cases, each seen red first; `agents/sealer.md` §*The command* gains the paragraph A11 pins, and the pin | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_gate_names_every_step_ci_runs.py tests/test_the_gate_asks_the_range_ci_will_ask.py -q`, counts read directly; the stub case red at `9f846733`; `ruff` over the edited files; `bin/test tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_a_moved_rule_leaves_its_definition.py tests/test_the_rules_have_one_owner.py -q` for the definition's prose | NAME NOT IN TREE |
| 3 | **Two agents alive at once cannot share a scratch name** (#544). `agents/warden.md` §*Where you work* names `<scratchpad>/<work-item-id>/round-<n>/clone` and puts every probe, capture and fixture of the round under `<scratchpad>/<work-item-id>/round-<n>/`; `agents/sealer.md` §*The command* names the capture file with the work item id and says to quote the gate's `outputs kept under` line; `skills/verify/SKILL.md`'s example loses `/tmp/run.txt` for a name carrying the work item id. New module `tests/test_a_parallel_agent_names_its_scratch_after_the_work_item.py` (A12, A13, A14), red at `9f846733` | The new module red then green, count read directly; the four prose pins above over both definitions and the skill; `ruff` over the new test | NAME NOT IN TREE |
| 4 | **The records.** `evidence-check --reverify .` over the drifted rows `spec.md` §*Data & interfaces* names — `run_tests.py#build`, `#main`, `broad_gate.py#panel`, `agents/warden.md#"## Where you work"`, `agents/sealer.md#"## The command"` — each re-read first; the ledger fragment's new rows; `overview.md` with its `## Not verified` table; `questions.md` M1, M2, W1, W2 filled by what phases 1 and 2 measured; the branch's own sweep and its `survivors.md` if the sweep reports the reworded cost sentences standing in `CHANGELOG.md` or the ledger | `bin/evidence-check --strict .` exit 0; `bin/survivor-check --range origin/release/v0.15.1...HEAD --exempt <this item>/survivors.md` exit 0 with every `exempt` line naming a row; `bin/unverified-check --baseline origin/release/v0.15.1 seal/specs/` exit 0; every exit code read directly, never through a pipe | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

### Per `CONTRIBUTING.md` §*What a change to a gate must carry*

| Phase | Test seen red | Failure direction | Prompt budget | Platform honesty |
|---|---|---|---|---|
| 1 | The inverted `-n auto` pin; A2's one-install case; A3's sentence; A4's parametrised spellings; A6's absent phrases | Not a gate's verdict: the same suite, the same exit code, less wall clock. The wrong direction is a `-n auto` that pytest refuses beside a caller's flag (exit 4, `unrecognized arguments`), which is the ticket's middle row arriving from the other side; A4's list and the pass-through bound it | zero | the xdist marker's path differs by platform (`lib/python*/site-packages` against `Lib/site-packages`) and both spellings are checked; CI runs the module on ubuntu, macOS and windows, and the `.cmd` twin passes `%*` through unchanged |
| 2 | A7's stub (exit 3 and the marker), A8's self case, A10's row | The gate asks **the question the merge is judged by**: the tree's arms, which are the arms CI runs. Measured instance: a false refusal becomes a seal. The symmetric mistake — a tree's broken arm sealing itself — is the ticket's stated cost, named on the stamp by `tree`, and CI refuses it with the same scripts at the pull request. For every repository that ships no gate, nothing changes but one row and one line | zero — the redirect asks nobody, and the line it prints is quoted rather than answered | `os.path.realpath` and a `subprocess.run` under `sys.executable` on all three platforms; the `.cmd` twin runs `py -3 broad_gate.py`, and the child is spawned from `sys.executable`, so the twin is not consulted twice. Windows is exercised by `test_the_wrapper_runs_the_same_gate` on `windows-latest` |
| 3 | A12, A13, A14 against the unedited files | Not a gate. A definition names a directory where it named none; the wrong direction is a sentence an agent does not follow, which costs what today costs | zero | a path in prose; `<scratchpad>` is whatever the harness names on that platform |

## Operational impact

Migrations · new env vars · new dependencies · compatibility breaks — the
items a deployer must not miss.

- **`pytest-xdist` becomes a dependency of `bin/test`'s environment.** A
  `.venv` built before this change takes one install step on its next call
  (A2); a machine with no network at that moment gets a sentence and a serial
  run (A3). The `uvx` no-write fallback in `CONTRIBUTING.md` is unchanged and
  still serial.
- **`-n auto` uses every logical CPU.** Four chains running the suite at
  once from one session, as the 0.15.0 run did, oversubscribe the machine;
  the wall clock of one run under that load is `questions.md` M1's second
  reading, and nothing here limits the worker count. A caller who wants fewer
  passes `-n <k>` and the runner honours it (A4).
- **This branch's own seal is measured by the installed 0.15.0 gate unless
  the sealer is spawned with this tree's absolute `bin/broad-gate`.** The
  redirect ships in this branch and the installed copy does not have it, so
  the sealer's bare `broad-gate` resolves to
  `~/.claude/plugins/cache/specseal/specseal/0.15.0/bin/broad-gate`. The
  orchestrator spawns the sealer with
  `/Users/x/…/wt-337/bin/broad-gate --base release/v0.15.1 --record <item>`
  (this tree's path) so the branch is judged by the gate it ships — the
  workaround #475's comment records, needed exactly once more. The stamp then
  reads `gate  tree 0.15.0`.
- **The stamp gains a row for every repository.** A reader comparing stamps
  across releases sees `gate` from this one on; `HISTORICAL_ROWS`'s
  docstring says when and why.
- **No compatibility break.** The `Broad gate` row, the `Broad gate` cell,
  `bin/broad-gate`'s argument vector and `bin/test`'s pass-through are
  unchanged; every existing caller typing `-n <k>` or `-p no:xdist` is
  honoured.
