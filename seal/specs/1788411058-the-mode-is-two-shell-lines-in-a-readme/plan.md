# Implementation Plan: the mode is two shell lines in a README

<!-- seal/specs/1788411058-the-mode-is-two-shell-lines-in-a-readme/plan.md —
HOW, as vertical slices. The Design Gate's artifact: approval of this file is
the approval to implement. -->

## Approach, and the two that were weighed

### Chosen: declared row + `seal mode`, with the folder still deciding

The row says what the repository wants; `hooks/optin.py#home_at` still says
what it has. `seal mode` is the only thing that reads the row, and a CI step
names a disagreement left standing. Everything the two README shell lines do,
plus the four things they cannot.

**What it costs.** A second place a person can write a mode, which can be
wrong. That is bought back by the check and by the row being read by nothing
at runtime — the whole of §"The row is not the signal" in `spec.md`.

### Rejected: a command with no row at all

`seal mode local` / `seal mode shared` and nothing in `config.md`. Simpler by
one file and one parser, and it answers the *nobody can find the two shell
lines* half of the issue.

**Failure scenario.** A repository migrated from the 0.3.x layout lands in
shared without being asked, which is the other half. With no row there is
nothing for a person to edit ahead of time and nothing for a check to read,
so *this repository was never asked which it wanted* stays unrecorded and
unaskable — and a teammate who wants local has no way to say so except by
running a command in a clone they may not have yet.

### Rejected: the row read at runtime, folder derived from it

One answer instead of two, and no disagreement possible.

**Failure scenario.** Every gate resolves the root through a hand-editable
file. One typo in `config.md` and each gate looks in a place with no folder;
`hooks/optin.py` is documented to fail toward *not opted in*, so the whole
workflow goes silent with nothing on screen that reads as being switched off.
That is the `.specseal/scratch` defect — a committed file silencing every gate
in every clone — rebuilt with a wider blast radius.

## Phases

Vertical slices: each one runs end to end before the next widens it.

| # | Phase | Verified by | Status |
|---|---|---|---|
| 1 | The row: the parser, `seal mode` reporting the folder, the row, and agreement; `--check`'s exit codes. No file is moved by anything in this phase | S1–S7 cases, executed | |
| 2 | The switch, both directions, with the guards of `spec.md` §"What the switch touches" | S8–S11, S14–S20, executed | |
| 3 | The two halves a `mv` leaves behind: the index and the workflow file, with the version substitution | S21–S25, executed | |
| 4 | What a person is told: the one-way-door line, the lost-clone line, the worktree note | S12, S13, S26, executed | |
| 5 | The documents — both READMEs, `docs/one-root-by-lifetime.md` and its mirror, `templates/config.md`, the skill's bootstrap, both hygiene workflows | the documentation cases in the same file, plus the existing suites that read those documents | |
| 6 | Mutation-test every case added, one at a time | each case reddened by a deliberate defect, recorded in `overview.md` | |

Phase 1 is first because it is the half that cannot break anybody's tree: a
reporting command with an exit code, shipped alone, is already the answer to
*nobody can find the two shell lines*. Phase 2 is the half that moves files,
and it is written against guards that already exist in the file it lands in.

## Testing strategy

`tests/test_the_mode_is_a_row_and_a_command.py`, in the shape
`tests/test_the_records_can_be_carried_out_and_in.py` uses: load `seal.py` as
a module, run `main(argv, cwd=repo)`, read `capsys`. Fixtures from
`tests/conftest.py` — `repo`, `local_home`, `symlink_or_skip`.

**Every case that asserts a refusal also asserts that nothing moved**: the
root's file list, the destination path, and `git status --porcelain` compared
before and after. A refusal that refuses and moves something anyway passes a
test that only reads the exit code.

**Nothing rests on a platform guarantee.** The one platform-dependent step is
the rename, and the case for S19 removes the guarantee rather than assuming
it — a destination parent that cannot be written, so the failure is produced
rather than described. `os.path.join` is never given a literal separator, and
every git pathspec is a forward-slash string handed to git rather than a path
built for this filesystem.
