# 1790635415-a-gate-that-fails-to-load-says-so — phase 5

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 8b6b0a00 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s Phase 5, which the owner added after round 1 so that #662
is fixed in this branch. The commit gate keeps a `cd` across a newline: `cd W
&& … <heredoc>` with `git commit` on the next line was judged in the
session's directory, and prompted the person during an `automation` run. Both
directions are pinned: an undeclared session directory with a declared `cd`
target reads silent, and a declared session directory with an undeclared
target is asked. Find why the gate's path does not carry the `cd`, and fix it
in `hooks/cmdline.py` for every gate that reads a directory from a command.
The verification: the three shapes of #662 through the gate's `main()` plus
the reverse direction, seen red at `e8e5f977`; `bin/test` over the gate and
`cmdline` modules; one mutant per changed branch.

Mid-phase the owner added #665 to it: a heredoc body fed to a known non-shell
interpreter reading its program from stdin is data to the gate, not shell.
Shells, `eval`, `ssh`, `xargs` and unknown consumers are still read as shell.
The command that prompted the person, this phase's own `python3 -` patch, is
the seen-red case, and both directions are cases.

The spawn also asked for the ledger rows and changelog entries naming both
issues, every drifted row re-read in place, and this record's pull-request
lines for `CONTRIBUTING.md` §*What a change to a gate must carry*. Mid-phase,
every file edit moved to the `Edit` tool. It asked for scratch only under
`<scratchpad>/1790635415/`, and for staying out of `hooks/routing.py`, where
work item B works. Phase 5 did not need `routing.py`.

## What this phase found

- **#662: the frame's premise does not hold, and what does hold was
  measured before anything was built.** The gate never dropped the `cd` at a
  newline. `walk_directories` already reads a newline as `;`, and for each
  of #662's shapes it returned the `cd`'s target AND the session's
  directory. `;` and a newline run the next line whether the `cd` succeeded
  or not, so the walk parks the `cd`'s failure branch and they consume it.
  That is deliberate (#72, `test_a_semicolon_carries_the_commit_to_both`).
  The prompt came from that second directory. What is true of the shell is
  narrower: a `cd` into a directory that is there and can be entered does
  not fail.
- **The first fix was too wide, and four existing cases said so.** Dropping
  the failure branch of every such `cd` turned
  `test_or_reaches_both_the_session_and_the_destination`,
  `test_a_middle_segment_does_not_spend_another_repositorys_declaration`,
  `test_a_skipped_branch_still_reaches_the_gate` and
  `test_an_alias_on_cd_stops_the_commit` red.
  - The first three pin a forgery defence: `||` NAMES the failure branch, so
    a declaration in the target must not answer for `cd <B> || git commit`.
  - The fourth pins that after `alias cd=…` the reader cannot name the shell,
    and the failure branch of the next `cd` was the only thing marking it.

  The rule that holds all five: such a `cd`'s failure is parked in `named`,
  which a `||` consumes and a `;` or newline does not, and only when the
  shell it leaves is one the reader could name. All four cases pass
  unedited.
- **Two conditions were removed because nothing could tell them apart.**
  - `known`: an unnamed segment's states are already `Unresolved`.
  - `_enters`'s type checks: an `Unresolved` landing leaves the answer
    unreadable and therefore stopped.

  `target is not None` stayed. `false && cd C ; git commit` shows why: the
  failure of `false` skips the `cd`, and the commit runs where the shell
  started.
- **#665: the consumer is read in the pass that already finds the bodies.**
  `_heredoc_split` records, for each body, the text of the command its `<<`
  stands in, from the last `;`, `&`, `|`, newline or parenthesis outside
  quotes and comments. A second reading of the command could disagree with
  that pass about which body is which. `program_is_data` answers from those
  tokens: `python`, `node`, `ruby` or `perl`, with a version suffix, after
  any assignments, with no script argument or with `-` as the script. Any
  program flag (`-c`, `-m`, `-e`, `-E`, `-p`, `--eval`, `--print`), a
  script file, an untokenisable command and an unlisted name read as shell.
- **The seen-red command carries test data and was taken verbatim, except
  its worktree path.** It is `PROMPTED_PATCH` in the gate's module, with
  `/Users/x/repo-worktrees/item` for the path, which
  `tests/test_no_real_identifiers.py` requires. It was denied at
  `e8e5f977` ("cannot read") and reads silent now in a declared repository.
- **Mutants.**
  - #662: nine, each killed. The `isdir` check needed an executable regular
    file before a case told it apart from the execute check.
  - #665: fifteen, each killed. A program flag needed its argument glued on
    (`python3 -cprint(1)`, `node --eval=x`), because a separate argument
    already reads as a script.
- **Words this made false, enumerated and corrected:**
  - `docs/commit-review-gate-spec.md`: the `cd X ; git commit` table row, the
    paragraph on the two consuming operators, and the statement on heredoc
    bodies, whose `Enforced by:` line names the new cases;
  - agent contract §9, which said the gate reads every heredoc body as shell;
  - two case docstrings saying an interpreter list is what #75 declined;
  - `seal/ledger.md`'s row on heredoc bodies, corrected in place.

  Left as they stand, because they are still true:
  - `agents/smith.md`'s §9 paragraph and its RIDER. A patch to that file
    through `cat` or a shell still trips, and `_hides_a_commit` on the
    file's own text is unchanged.
  - `docs/worktree-guard-spec.md`'s `cd /no/such/dir ; git switch x`, whose
    directory is missing.
  - #72's docstring, exempted in `survivors.md`.
- **Both changes were parsed as Python 3.9.** A hook runs under whatever
  `python3` the harness finds. `zip(strict=True)` was avoided in phase 4
  for the same reason, and index loops replace it here too.

### The pull request's lines for `CONTRIBUTING.md` §*What a change to a gate must carry*

- **A test seen red.**
  - #662: `test_a_cd_on_one_line_carries_the_commit_on_the_next_to_its_target`
    (three of #662's four shapes) and
    `test_a_cd_into_a_directory_that_is_there_has_no_failure_branch` were red
    at `e8e5f977`.
  - #665: the command that prompted the person, replayed through the gate,
    was denied at `e8e5f977`. The consumer predicate and the body pairing
    cases were red there too.
  - The reverse directions held before and are pinned.
  - Twenty-four mutants were run, one per changed branch, and each was
    killed.
- **A stated failure direction.** Both changes allow more, and each only
  where the shell cannot do otherwise.
  - #662 stops judging the session's directory after a `cd` that cannot
    fail. A commit there would need a `cd` into an existing, enterable
    directory to fail between the hook and the shell, and `||` keeps that
    branch whenever the command names it.
  - #665 stops reading one body a known interpreter runs as its own
    program. `python3 -` running `subprocess.run(["git", "commit", …])` was
    never read as a commit before, so nothing is open that was closed.
    Every unlisted consumer stays on the asking side.
  - The cheaper mistake here is a false allow over a false prompt. The
    prompts were measured: four in one `automation` run for #665 and one
    for #662, each stopping a run that promised no question. The allows are
    bounded to states the shell does not reach.
- **A prompt budget.** It goes down. The change adds no question, and it
  removes the prompt for `cd <worktree> && …` followed by a commit on the
  next line, and for a `python3 -` patch whose body holds `git commit` as
  data.
- **Platform honesty.**
  - `os.access(X_OK)` on a directory means nothing on Windows, so there a
    `cd` into an existing directory is taken to succeed. The case that
    refuses entry by mode is skipped on Windows and as root, with the reason
    in its `skipif`.
  - Nothing inspects processes.
  - The cases ran on macOS only, and CI's three legs run them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `known` condition and `_enters`'s type checks, from the first version of the rule | none: each was redundant, as *What this phase found* says |
| `heredoc_bodies` as the gate's reader of bodies (the function stays, and the gate now reads `shell_bodies`) | `hooks/cmdline.py#shell_bodies` |
