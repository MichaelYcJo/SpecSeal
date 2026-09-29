# 1790635415-a-gate-that-fails-to-load-says-so — phase 3

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 43e05300 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s Phase 3: the words and the ledger. Replace the RIDER inside
`run_gate` with a comment saying what the catch does now. Correct
`dispatch.py`'s module docstring and the false sentence in
`hooks/implementer.py`'s docstring. Give `docs/commit-review-gate-spec.md`
§*Registration* the paragraph and an `Enforced by:` line, and put the
sentence into both READMEs. Write the changelog fragment and this work
item's ledger rows, and re-read the `run_gate` row in `seal/releases/0.4.0.md`
and N8 in `seal/releases/0.15.7.md` in place. Verified by `evidence-check`
with each drifted row re-read and `--reverify`d, `rider_check.py`, the rider,
editions and line-wrap cases, every case that pins the gate spec, and the
S14 doc pin seen red with the sentence deleted. The spawn also asked for
`CONTRIBUTING.md` §*What a change to a gate must carry* to be answered, with
its pull-request lines drafted here.

## What this phase found

- **Removing the RIDER turned a case red that the frame did not name.**
  `tests/test_a_rider_reaches_its_file.py#test_the_riders_exist_where_the_rows_said_they_would`
  lists `hooks/dispatch.py` among the files that must carry a `# RIDER:`. The
  entry left the list, and the case's docstring says why. `rider_check.py`
  reads 21 riders, all ok.
- **The class of sentences made false was wider than the frame's list,**
  enumerated by `git grep` for the silence's wording and for `run_gate`:
  - `hooks/evidence-advisor.py`'s docstring pointed at "the rider at
    `run_gate`";
  - `tests/test_gate_judges_the_repo_it_commits_to.py#test_a_broken_command_reader_leaves_no_verdict_rather_than_a_wrong_one`'s
    docstring called the silence one "this repository already has a rider
    on". Its assertion, that the `pre-bash` call itself is silent, still
    holds and is unchanged;
  - `skills/implement/scripts/seal.py#mode` and
    `tests/test_the_mode_is_a_row_and_a_command.py#test_check_does_not_pass_when_the_repository_cannot_be_resolved`
    called #28 "open". Both now say the shape "issue #28 was opened on",
    which stays true once this closes it. No ledger row cites either unit.

  Left as they stand, because they are still true:
  `docs/worktree-guard-spec.md`'s "`hooks/dispatch.py` skips a gate that
  raises", and the `test_the_guard_asks_once_per_session.py` docstrings saying
  the same. The skip is unchanged, and only the telling is new.
- **The mutation pass removed three units, and the frame's walk passed its
  own measurement.** At the close of the build, 41 single mutants were run
  against `hooks/dispatch.py` and the policy statement. Reading the units
  before that found three that no case could tell from their absence:
  clearing `FAILED` at the start of `main()`, `parse`'s dict check, and a
  dotfile filter in `draw`. Each was redundant with a fresh process, with
  `report`'s catch, or with a writer that makes no dotfiles, so each was
  removed rather than pinned. Eleven cases were added for the rest. The
  one first survivor, overwrite instead of exclusive create, lived because
  the case blinded `os.path.exists` everywhere, and `toplevel`'s walk with
  it. Narrowing the blind killed it.
- **`merge()` raises on a gate that prints a JSON array, a number or
  `null`.** `classify` calls `.get` on whatever `json.loads` returned. The
  group then dies with exit 1, and every other gate's decision in it is
  lost. This predates the branch, and it is not one of the two `merge()`
  drops `spec.md` §*Scope* Out names. No gate prints such a value today. It
  is named in `overview.md` §*Not done*, and it is why `beside`'s non-object
  branch is pinned directly rather than through `main()`.
- **`spec.md` named a harness attachment type,** `hook_non_blocking_error` (NAME NOT IN TREE),
  and `evidence-check --strict` refused it as a name the tree does not
  carry. The line now says NAME NOT IN TREE.
- **Survivors.** `survivor-check --range 2dc9a970..43e05300` reported one
  place: this frame's own quote of the `implementer.py` sentence it asked to
  correct. It is recorded in `survivors.md`.

### The pull request's lines for `CONTRIBUTING.md` §*What a change to a gate must carry*

- **A test seen red.** S1 was red against `2dc9a970`: no record was written,
  and `stop` printed nothing. S7 was red against the phase-1 tree: the
  planted gate's `sys.exit(0)` escaped `main()`, and the commit gate after it
  never decided. Every unit the report added was mutated once, 41 mutants,
  and each was killed.
- **A stated failure direction.** Unchanged. Every call a failing gate
  allowed before, it still allows, and the failing call's stdout is
  byte-identical to the same call with the gate absent. The work adds a line
  at the end of the turn. The one behaviour that moves is a gate whose
  module body calls `sys.exit`: it used to end the whole group, and now the
  gates after it decide. That direction is stricter, and it restores the
  isolation the dispatcher's docstring already promised.
- **A prompt budget.** Zero. A `systemMessage` asks nothing and stops
  nothing. At most one line per broken gate per session per clone, and none
  in a healthy install.
- **Platform honesty.** Exclusive create (`open(…, "x")`) and `os.replace`
  behave the same on Windows, and every path part is `basename`d on both. No
  process inspection is involved. Measured on macOS only, and the Windows
  render of a `Stop` `systemMessage` is unmeasured, the same open row #400
  carries. CI's Windows leg runs the new module.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `# RIDER:` inside `hooks/dispatch.py#run_gate` | resolved rather than moved: the comment that replaced it says what the catch does now, and `docs/commit-review-gate-spec.md` §*Registration* carries the rule |
| `hooks/dispatch.py` in the rider list of `tests/test_a_rider_reaches_its_file.py#test_the_riders_exist_where_the_rows_said_they_would` | the case's docstring, which says why it left |
| `dispatch.parse`, clearing `FAILED` in `main()`, and `draw`'s dotfile filter, all added in phases 1 and 2 | none: each was redundant, as *What this phase found* says |
