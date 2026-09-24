# Feature Specification: the run's instruments cost wall clock

<!-- seal/specs/1790206436-the-runs-instruments-cost-wall-clock/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three instruments of a run each cost wall clock in the 0.15.0 run, and none
of the three costs was the work's own. The suite runner (`bin/test`,
`.github/scripts/run_tests.py`) runs serially because the environment it
builds has no `pytest-xdist`, and installs none because it does not pass
`-n auto` — six sealer runs at about thirteen minutes each where the same
suite ran in 3m04s by hand (#337). The sealer's `broad-gate` resolves on the
Bash tool's PATH to the installed plugin cache, so a branch that changes the
gate is measured by the copy that predates the change — a false refusal on
#497's branch, and a stamp that cannot say which gate drew it (#475). Every
agent of one session shares one scratchpad, so a warden's clone and a
sealer's capture file under a generic name were overwritten mid-round by a
sibling work item's, three times (#544).

This work makes the runner parallel by default in every environment it
builds or adopts, makes the gate run the copy the tree being gated ships
and say on the stamp which copy ran, and names the clone directory and the
capture file after the work item so two agents alive at once cannot share
one. Nothing here changes what any check judges; it changes what a run
costs and which copy measures it.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The measured cost of the released copy's gate was a false refusal that stopped an unattended run until a person re-spawned the sealer with a path (#475's comment). Between the two copies, the one that lets the run finish on its own is the cheaper one, and the argument is made here rather than assumed |
| `docs/the-broad-gate.md` §*What the gate runs, and how the list is kept true*: *The gate and CI ask about the same range* and *Every step CI runs is either mirrored by a named arm or excluded* | The gate exists so the sealer's one run says what CI will say. `.github/workflows/hygiene.yml` runs `python3 skills/code-review/scripts/chain_check.py` and the other arms from the checkout, so the checkout's copy is the CI-faithful one; a released copy asks a different gate's question of the same range |
| `docs/the-broad-gate.md` §*What the runner owes the person who typed it*: *A repository ships a command that runs its own suite, and it is cheap the second time* | The runner's warm call is decided by the filesystem and reaches no builder. The parallel default is added on those terms: whether `pytest-xdist` is present is a filesystem fact, and a warm call with it present pays nothing new |
| `skills/verify/SKILL.md` §*The cost of the run you repeat*: *the suite running serially while a parallel runner sat installed and unused, its recipe written in a comment … A recipe in a comment is not a recipe* | #337 is that paragraph measured on this repository: the recipe (`add xdist and pass it yourself`) sits in a comment above the command, and the 0.15.0 preparation followed it by hand. `.github/workflows/test.yml` has run `-n auto` on three platforms for every release, so parallel is the configuration with the evidence |
| `skills/agent-contract/SKILL.md` §7 (*A probe is named `test_tmp_*`, one file, run once, deleted*) and `skills/code-review/SKILL.md` §*Probes vs. regression tests*: *a scratch clone … is a leaving too* | A clone that a sibling agent can overwrite is a leaving nobody owns. Naming it for the work item and the round is what makes *every one of them is gone* answerable by the agent that made it |
| `skills/agent-contract/SKILL.md` §12 (*A defect belongs to a class — enumerate the class*) | #544's class is *an instruction that names a scratch location with a name any parallel agent would also pick*: the warden's clone (named nowhere), the sealer's capture file (named nowhere), and `skills/verify/SKILL.md` §*Capture once, filter locally*'s example `/tmp/run.txt`, which is shared across every session on the machine. All three are in scope |
| `skills/agent-contract/SKILL.md` §14 and §15 | Every changed sentence a person reads is pinned in the same commit, and every new case is shown red against the unfixed tree before it is committed. Phase 1 inverts an existing pin (`test_it_does_not_pass_n_auto`) rather than adding beside it |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Phase 2 changes which copy of the gate runs. Its four answers are in `plan.md` §*What each phase carries*; the direction is stated as *the same question the merge is judged by*, with the symmetric cost named rather than dismissed |
| `CONTRIBUTING.md` §*House rules*, on `seal/ledger.md`: a drifted row is re-read and re-stamped; a row whose anchor a change removes is removed and rewritten in the branch's fragment | The units this work edits carry standing rows; §*Data & interfaces* names each one and what happens to it |
| `agents/sealer.md` §*The command*: *A refusal about the row goes back to a person, and never to you* and *Quote the line in your report when it appears* (the moved-base line) | The gate line phase 2 prints is the same kind of line as the moved-base one: a fact about the run a reader learns nowhere else, quoted by the sealer and judged by nobody |
| `agents/warden.md` §*Where you work* and `agents/sealer.md` §*The one write, and why it is yours* | The clone rule and the sealer's write already live in these sections; #544's sentences are added where the rule they qualify already is, and the ticket's *Not this* for #475 — *not telling the sealer to type a path* — is honoured by putting the choice in the gate |

## Scope

### In

| Ticket | What it is | Where it goes |
|---|---|---|
| #337 | `run_tests.py#build` installs `pytest` alone, so a fresh `.venv` has no `pytest-xdist`; `#main` builds the command without `-n auto` because a fresh build would refuse it. The two sentences hold each other in place. Measured in the ticket: 350 s serial against 62 s parallel on one checkout, and `exit 4, unrecognized arguments: -n` in a fresh worktree of the same clone — the same command meaning three things in one repository | Phase 1 |
| #475 | `bin/broad-gate` on PATH is the installed copy's, and the script it execs resolves every arm relative to itself; the tree being gated is never asked whether it ships a gate of its own. The stamp says `tree` and `base` and nothing about which gate. Measured twice: seven arms in the tree against five installed (#468's sealer), and a chain refusal from the 0.13.0 copy over a state the branch repairs (#497's sealer) | Phase 2 |
| #544 | `agents/warden.md` names the clone's shape (`git clone --no-local` at the target SHA) and no directory; `agents/sealer.md` names no capture file; `skills/verify/SKILL.md`'s capture example is `/tmp/run.txt`. Four work items ran their chains in parallel from one session and one scratchpad: two wardens cloned to the same `r2clone`, a third's clone had its HEAD moved by a foreign checkout for fifty-five seconds, and two sealers wrote `broad-gate.out` over each other | Phase 3 |

Every carrier of the serial cost as a stated figure — `bin/test`'s comment
(*about five minutes*), `run_tests.py`'s docstring, `CONTRIBUTING.md`
§*Running the checks*' `# everything, about five minutes`, and the failure
message in `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` that
names *this repository's own five-minute suite* — is reworded in phase 1 so
that no loaded document states a serial figure with no moment. The measured
before-and-after goes in the changelog fragment and the phase record, with
its date and machine, which is the shape `seal/follow-up.md`'s row on *a
figure about a corpus, stated with no moment* asks for.

`docs/release-checklist.md` §3's suite line, `uv run --quiet --with pytest
--with pytest-xdist pytest tests/ -q -n auto`, becomes `bin/test -q` in
phase 1. That form was the hand-run workaround for the serial runner (the
0.15.0 preparation ran it, 4397 passed in 3m04s); once the runner is parallel
the checklist typing a second spelling of the same run is the *three
meanings* defect one document over.

### Out

| Left out | Why, and who answers |
|---|---|
| The `Broad gate` cell's format (`<sha> against <base>`, newest first, `earlier run` behind it) | #475 asks that the **stamp** say which gate ran, and the stamp is what phase 2 changes. The cell is parsed by `chain_check.py#broad_gate` and written by one path in `round_record.py` (ledger rows A5, A9, A11 of 1790174138); widening it is a change to what a gate reads and a different work item. The stderr line phase 2 prints is what a reader of the record's sealer report sees |
| CI's own `-n auto` (`.github/workflows/test.yml`) | Already parallel on three platforms; #337 says so and touches nothing there. The floor pin `test_ci_runs_the_suite_at_the_floor_the_runner_holds` reads that file and stays green |
| A per-agent scratchpad from the harness (#544's *stronger answer*) | Not the repository's to build. Measured on this framer's own spawn: the scratchpad the harness gave is session-scoped, and the orchestrator sent this framer to a sub-directory by hand. The definitions name the sub-directory so the hand stops being needed; if the harness ever scopes it per agent, the named directory is still correct |
| The orchestrator's spawn prompts (`skills/code-review/orchestration.md`, `docs/review-handoff-protocol.md` §*What a prompt is left holding*) carrying the clone directory | #544 names the definitions as where a rule arrives by mechanism; a prompt is where the rule went missing (#330's subject). A definition that names the directory needs no prompt to repeat it |
| Installing `pytest-xdist` on the `uvx --with pytest` no-write fallback in `CONTRIBUTING.md` | The fallback exists for a reader who wants no `.venv` in the tree and is labelled with its cost; it is not the sealer's command and not the form a segment types. Adding `--with pytest-xdist -n auto` to it is one line the repository owner can take or leave; not taken here because the section states its floor once and pins the count, and a second command carrying flags is a second place to drift |
| Refusing an adopted `.venv` that lacks `pytest-xdist`, the way a below-floor one is refused | A missing speed-up is not a wrong interpreter: the suite runs correctly without it. Phase 1 installs it into the adopted environment instead, by the same two strategies `build` already uses, and runs serially with a sentence where the install fails — see *Judgments the tree answered*, 2 |
| `docs/` | A work item does not write policy; `settle` folds this spec at the release. `docs/the-broad-gate.md`'s statements stay true under this work and are cited above rather than edited |
| `bin/broad-gate` and `bin/broad-gate.cmd` | The redirect lives in the Python the pair execs, so both platforms take it from one place; the wrapper pair is pinned as it stands by `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_wrapper_runs_the_same_gate` and its bin-twin case, and neither moves |

## User scenarios & acceptance *(mandatory)*

One row per scenario — these become the review's stage-1 checklist and the
regression tests' skeleton.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · a fresh build has xdist | Given no `.venv`, when `bin/test` builds one, then both install lists (`uv pip install …` and `python -m pip install …`) name `pytest-xdist` beside `pytest`, and the command `main` builds carries `-n auto` | `test_it_does_not_pass_n_auto` inverted to `test_the_whole_suite_runs_in_parallel_by_default`, red at `9f846733` (asserts `-n` and `auto` are in the recorded command); a case reading `build`'s two step lists for `pytest-xdist` |
| A2 · an adopted environment without xdist gets it once | Given a `.venv` that `has_pytest` accepts and whose site-packages holds no `xdist` package, when `bin/test` runs, then one install step is run — `uv pip install --python <venv python> pytest-xdist` where `uv` is on PATH, else `<venv python> -m pip install --quiet pytest-xdist` — and the suite then runs with `-n auto`. A second call finds it by the filesystem alone and runs no install | A case with a fake venv lacking the marker and a `Recorder`: exactly one install call, then the pytest call carrying `-n auto`; a case with the marker present: the first recorded call is pytest. The check is a directory named `xdist` under `lib/python*/site-packages` (POSIX) or `Lib/site-packages` (Windows), never a subprocess — `test_a_built_environment_is_reused_and_never_rebuilt`'s rule, and `fake_venv` grows the marker so the existing warm-path cases keep meaning what they mean |
| A3 · a failed install is a sentence, and the suite still runs | Given the install step exits non-zero (no network, a broken `uv`), when `bin/test` runs, then one sentence on stderr names the package, says the run is serial, and names the remedy (`remove <venv> and run bin/test again`); the suite then runs without `-n auto` and the exit code is pytest's | A case with a `Recorder` returning 1 for the install call: sentence pinned, the pytest call carries no `-n`, `Traceback` absent |
| A4 · the caller's own choice wins | Given the caller passed any of `-n <x>`, `-n<x>`, `--numprocesses…`, `-p no:xdist` (also as `-pno:xdist`), or `--pdb`, when `bin/test` runs, then no `-n auto` is added and the arguments pass through as typed | One parametrised case over those spellings asserting the recorded command carries exactly the caller's arguments and no added `-n`. `--pdb` is in the list because pytest refuses it under distribution rather than because it is a `-n` spelling; the phase measures whether any further flag belongs (`questions.md` W1) |
| A5 · the narrow form stays the narrow form | Given `bin/test tests/test_x.py -q`, when it runs, then the command is `<python> -m pytest tests/test_x.py -q -n auto` — the file the caller named and nothing wider | `test_arguments_pass_through` updated to the new tail; red first under the old assertion |
| A6 · the runner's own comment is the record | Given `run_tests.py`, when read, then the comment above the command no longer says *No `-n auto`* and says why it used to; the module docstring and `bin/test` no longer state *about five minutes* | `test_the_placement_stands_on_what_it_actually_buys`'s sibling: a case asserting `No `-n auto`` is absent from the runner and `five minutes` absent from `bin/test`, the runner and `CONTRIBUTING.md` §*Running the checks*; red at `9f846733` |
| A7 · the gate runs the copy the tree ships | Given `broad-gate` invoked from an installed copy over a root whose `skills/verify/scripts/broad_gate.py` is a different file (by `os.path.realpath`), when it runs, then it re-runs that copy with the same argument vector under `sys.executable`, returns that copy's exit code, and writes one stderr line naming the copy it ran and the copy it was invoked as, before anything else runs | A case whose fixture root carries a stub `skills/verify/scripts/broad_gate.py` that prints a marker and exits 3: the real gate over that root exits 3, prints the marker, and the line names both absolute paths. Red at `9f846733` (exit 2 or 0 and no marker) |
| A8 · the tree's own copy does not redirect to itself | Given the copy that runs is the one under the gated root (the same realpath), when it runs, then no redirect happens and no loop | `shipped_gate(<plugin root>)` returns `None` on this repository's own root; and A7's stub, having no `skills/verify/scripts/broad_gate.py` beneath *its* root but being that file, is reached once |
| A9 · a repository shipping no gate is untouched | Given a root with no `skills/verify/scripts/broad_gate.py` — every fixture in the suite, every user repository — when the gate runs, then it runs exactly as before apart from the `gate` row and the gate line below | Every existing case in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `test_the_gate_asks_the_range_ci_will_ask.py` and `test_the_gate_names_every_step_ci_runs.py` green; `HISTORICAL_ROWS` in the last of those grows by the one row A10 adds, with its docstring saying why |
| A10 · the stamp says which gate ran | Given a sealed run, when the panel prints, then it carries a `gate` row whose value is `tree <version>` where the running copy's realpath lies under the gated root and `plugin <version>` otherwise, `<version>` read from the running copy's `.claude-plugin/plugin.json` and `?` where that file cannot be read; and every run — sealed, not sealed, refused after the root resolved — carries one stderr line naming the running copy's absolute path | A case driving `panel` with a fake plugin root; a case over the real gate asserting the row's label and the stderr line; the value fits `PANEL_VALUE_WIDTH` (23) by construction and a case asserts it for a nine-character version |
| A11 · the sealer quotes the gate line | Given `agents/sealer.md`, when read, then §*The command* says the gate prints which copy ran, that a `tree` value means the branch was measured by the gate it ships, and that the line is quoted in the report the way the moved-base line is | A case in `tests/test_the_seal_is_taken_once_by_the_sealer.py` beside `test_the_sealer_names_the_command_it_runs`, pinning the phrase; red at `9f846733` |
| A12 · the warden's clone is named for the work item and the round | Given `agents/warden.md` §*Where you work*, when read, then the clone directory is `<scratchpad>/<work-item-id>/round-<n>/clone` — the scratchpad the harness names, the work item id the prompt names — and every probe, capture or fixture the round makes outside the clone sits under `<scratchpad>/<work-item-id>/round-<n>/`; the sentence says why: agents of one session share the scratchpad, and the 0.15.0 run measured the collision three times | A new module `tests/test_a_parallel_agent_names_its_scratch_after_the_work_item.py`: the section contains `<work-item-id>` and `round-<n>` in the clone sentence; red at `9f846733` |
| A13 · the sealer's capture file is named the same way | Given `agents/sealer.md` §*The command*, when read, then a capture of the gate's output — where the sealer redirects it to a file to read — is `<scratchpad>/<work-item-id>/broad-gate.log` or another name carrying the work item id, and the gate's own `outputs kept under broad-gate-<random>/` line is quoted in the report so a capture that was overwritten can still be told apart, which is how the 0.15.0 sealers were not misread | The same module: the sentence contains `<work-item-id>`; red at `9f846733` |
| A14 · the generic example is gone | Given `skills/verify/SKILL.md` §*Capture once, filter locally*, when read, then the fenced example redirects to a file under the scratchpad carrying the work item id, and no `/tmp/run.txt` remains | The same module asserts `/tmp/run.txt` is absent from that file and the example carries `<work-item-id>`; red at `9f846733` |
| A15 · the branch is sealed by its own runner and, for this once, by its own gate by hand | Given this branch, when the sealer runs, then `bin/test -q` in the `Broad gate` row is this branch's runner and runs parallel; the gate that measures it is the installed 0.15.0 copy unless the orchestrator spawns the sealer with this tree's absolute `bin/broad-gate`, because the redirect is not in the installed copy yet | The sealer's report: the `gate` row and the gate line appear only where the tree's copy ran; `plan.md` §*Operational impact* says which path to spawn with |

## Data & interfaces

Schema deltas, endpoints, payload shapes. Reference, don't duplicate, the
evidence ledger's coordinates.

**`.github/scripts/run_tests.py`.** `build` gains `pytest-xdist` in both step
lists. A new `has_xdist(venv)` reads the filesystem only. A new
`with_xdist(venv)` (name the work's) runs one install step where `has_xdist` NAME NOT IN TREE
is false, by the same tool order `build` uses, and returns a sentence or
`None`; `main` calls it after `ensure` and passes `-n auto` unless the caller
decided (A4) or the install failed (A3). `ensure`, `has_pytest`,
`venv_version`, `hide_from_git`, `FLOOR` are untouched, so ledger rows R2 and
R7 of `1788632199` and R1 of `1788691941` keep their anchors. Rows anchored on
`build@ee6d6dd0` (R2, R3) and `main@323adce0` (R1) drift and are re-read and
re-stamped in phase 4; their claims still hold — R1's *a warm call decides by
the filesystem alone* is exactly the property A2 keeps.

**`bin/test`, `bin/test.cmd`.** Comment only (A6). `bin/test#"# Typed as
…"@768c73ec` (R6) anchors a line that does not move.

**`skills/verify/scripts/broad_gate.py`.** A new `shipped_gate(root)` returns
the tree's `skills/verify/scripts/broad_gate.py` where it exists and is not
this file by realpath, else `None`; `main` calls it after `parse_args`,
resolving the root the way `gate` does, and where it returns a path runs
`[sys.executable, path, *argv]` with inherited streams and returns its code —
before `gate()` is entered, so `gate@084b7e9f` (rows S7, S12 of `1789002694`,
the `not_as_written` row of `1789445605`, R2 of `1789956662`, G3 of
`1789985781`) is untouched and none of the five drifts. `panel` gains the
`gate` row (A10), so `panel@ea0e48ac` (R5 of `1789956662`) drifts and is
re-stamped; the gate line is written to stderr in `main` beside the redirect
decision. `--base` is still read exactly once, in `gate` (R2's structural
count). `HISTORICAL_ROWS` in `tests/test_the_gate_names_every_step_ci_runs.py`
gains `"gate"`.

**`agents/warden.md` §*Where you work*** gains the clone-directory sentence
(A12); `"## Where you work"@0e5f8a4b` (R5 of `1788632199`, S3 of `1788844127`)
drifts and both claims — the runner is found, the report path is named — still
hold; re-read and re-stamp in phase 4.

**`agents/sealer.md` §*The command*** gains the gate-line paragraph (A11) and
the capture-file sentence (A13); `"## The command"@c4f94c00` (the absent-row
row of `1789445605`, R7 of `1789956662`) drifts and both claims still hold.
The command pinned by `test_the_sealer_names_the_command_it_runs`,
`broad-gate --base <base> --record <item>`, is unchanged.

**`skills/verify/SKILL.md` §*Capture once, filter locally*** — the example
block only (A14). No ledger row anchors that section.

**`docs/release-checklist.md` §3** — one line (the suite command). No row
anchors it; `tests/test_release_hygiene.py` reads it for version names only.

**`CONTRIBUTING.md` §*Running the checks*** — the `about five minutes`
comment (A6). The section's pins — `bin/test` before `uvx`, the floor stated
once, `Run the broad ones once`, `agent-contract` and `sealer` named — are
unchanged.

**Tests.** `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`
(A1–A6; `fake_venv` grows an `xdist` marker directory),
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (A7, A8, A10, A11),
`tests/test_the_gate_names_every_step_ci_runs.py` (A9's tuple),
`tests/test_a_parallel_agent_names_its_scratch_after_the_work_item.py` (A12–A14,
new). New prose in the two definitions is held to `tests/test_docs_line_wrap.py`
(88 columns), `tests/test_no_real_identifiers.py` (`/Users/x/` only),
`tests/test_one_word_one_meaning.py` (no bare *the seal*), and
`tests/test_a_moved_rule_leaves_its_definition.py` (no contract sentence
restated).

## Judgments the tree answered

Listed so nobody reopens them; `questions.md` repeats the list by number.

1. **The gate runs the copy the tree ships, and the released copy is not
   the default.** #475 left this open (*the released copy is defensible*).
   CI runs the tree's scripts (`hygiene.yml`, every arm), the gate's stated
   purpose is to say what CI will say (`docs/the-broad-gate.md`), and the
   released copy's one measured cost was a false refusal that stopped an
   unattended run (#475's comment, #497). The symmetric cost — a tree that
   breaks an arm seals itself — is real, named on the stamp by the `tree`
   value (A10), and caught at the pull request by the same scripts CI runs.
2. **An adopted `.venv` without xdist is repaired, not refused.** The
   runner's precedent for an adopted environment that lacks something is
   split: a missing `pytest` reaches `build`, a below-floor interpreter is
   refused. A missing speed-up is neither — the suite runs correctly without
   it — so one install step, and a sentence plus a serial run where the step
   fails, is what keeps *the same command means one thing* (#337's sharper
   half) true for every `.venv` the runner built before this change — a
   worktree's, a clone's, a reviewer's — which is the ticket's middle row.
   The main checkout's `.venv` on this machine is the ticket's *first* row
   instead (read 2026-09-24: `site-packages/` holds `xdist` and
   `pytest_xdist-3.8.0.dist-info`, acquired by hand), so it is the one NAME NOT IN TREE
   environment here that takes no install. Refusing would turn a speed-up
   into a suite nobody can run, which `run_tests.py#venv_version`'s
   docstring already refuses to do for silence.
3. **`-n auto` is the default for the narrow form too.** #337 asks for the
   default *when the caller passed no `-n` of their own*, with no carve-out
   for one module; xdist's start-up on a small module is a fraction of a
   second, and a carve-out would be a second rule to remember. What the
   caller can still do is the whole of A4.
4. **The redirect lives in the Python, not in the wrapper pair.** The pair
   is two files kept in lockstep by a case; the script is one place both
   exec, so a redirect there is one edit, one case, and reaches Windows
   through the `.cmd` twin unchanged.
5. **The panel value is `<tree|plugin> <version>`, and the path goes to
   stderr.** A path does not fit 23 columns; a version alone does not
   discriminate a branch cut from the tag (same version, different content);
   the pair says where the copy came from and what release it belongs to,
   and the stderr line carries the path in full, the way `moved_line` and
   `coverage_line` already carry what the panel cannot.
6. **The clone directory carries the work item id and the round; the
   spelling is one per definition.** #544 proposes `<scratchpad>/r<N>-<id>/`;
   what matters is that two agents alive at once cannot pick the same name,
   and a directory per work item with a directory per round beneath it also
   gives every probe and capture of a round one home to remove. Any spelling
   carrying both is acceptable to the pin; the definitions use the one in
   A12 and A13.
7. **The three tickets are one work item, in three independent phases.**
   No file is shared between phases 1, 2 and 3; the milestone puts them in
   one step because each is a run instrument measured in wall clock, and one
   branch is one seal.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. Nothing in this frame
waits on a person; `questions.md` holds two measurements and two decisions
the work makes.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-09-24 by framer, before the build.
