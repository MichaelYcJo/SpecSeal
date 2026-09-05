# Implementation Plan: the repository ships a way to run its own suite

<!-- seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/plan.md -->

## Summary

One `bin/` pair and one paragraph, and the whole difficulty is in what
`bin/test` does about its environment. The repository has no `pyproject.toml`
and one test dependency, so the command has to acquire `pytest` somehow, and
every acquisition strategy the repository has tried so far is either slow on
every call (`uvx --with pytest`, measured at 55–58 s each) or invisible to
everyone but the machine that made it (the `.venv` that already exists in one
checkout and hides itself from git).

The answer is the second one, made **discoverable and reproducible** rather
than accidental: `bin/test` creates a virtualenv on first use if there is none,
reuses it afterwards, and says which it used.

## Technical context

- **[read]** `bin/session-cost` is the shape to copy: a POSIX `sh` script that
  resolves `here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)`, `exec`s with
  `"$@"`, and carries a comment saying why it exists. Every `bin/` entry has a
  `.cmd` sibling for Windows.
- **[read]** `CONTRIBUTING.md` §*Running the checks* (`:3-31`) already names
  the slow form, states the 3.12 floor with the reason macOS makes it
  necessary, and ends with the *run the broad ones once* rule. The new command
  goes at the top of that block; the floor sentence stays.
- **[read]** `.github/workflows/test.yml` installs `pytest pytest-xdist`
  itself. Out of scope, but it is the reason `-n auto` may not work locally:
  **xdist is CI's, not the tree's**, and a local `bin/test` that passes `-n
  auto` fails on a fresh virtualenv. Either install it too or do not pass it.
- **[executed, orchestrator, 2026-09-06]** the full suite from this worktree
  through an existing `.venv`: **2287 passed, 2 skipped, 4 failed in 306 s**
  serially. The four failures are #160, macOS-only, identical at the base.
- **[read]** #156 records that `uv venv` writes `.venv/.gitignore` containing
  `*`, so the directory hides itself from git. Confirm it; if the strategy
  chosen does not self-ignore, this work item adds the ignore.

**What breaks in six months.** A `bin/test` that silently creates a
virtualenv is a command that writes to the tree, and the first time it does so
on a machine with no `uv` it has to fail in a way that names what to install
rather than half-creating something. That is the failure to design against:
**a broken environment must produce a sentence, not a traceback.**

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `bin/test` wrapping `uvx --with pytest` | It is the line `CONTRIBUTING.md` already has, renamed. The 55 s per call — the whole measured cost — stays | **rejected** |
| A `pyproject.toml` with a test extra | Larger than the release is measuring, and the owner chose the `bin/` answer | **rejected**, question 1 |
| `bin/test` reusing a virtualenv, creating it on first use | Writes to the tree; needs a self-ignoring directory and an honest failure when the tool is missing | **chosen** |
| Documenting the `.venv` that already exists | It exists in one checkout by accident and reaches no clone | **rejected** — the issue says so |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `bin/test` and `bin/test.cmd`: reuse a virtualenv, create it on first use, pass arguments through, resolve from the script's own path, fail with a sentence when the tool is missing. Self-ignoring from git | executed: both calls timed and the pair recorded; a run from a subdirectory; an argument-passing run; the missing-tool path forced. Plus a case over `bin/` for the sibling shape | |
| 2 | `CONTRIBUTING.md` §*Running the checks* names it first, keeps the floor sentence and the broad-once rule, and whatever names the runner to a spawned segment says `bin/test` rather than an absolute path — without widening §2 | the module that reads `CONTRIBUTING.md`, plus a new case per sentence | |
| 3 | The closing set: ledger fragment, changelog fragment, `overview.md`, and `docs/flow.md`'s #156 box | the modules that read those, `evidence-check`, and the orchestrator's broad gate after the rounds | |

## Operational impact

A new command that writes a virtualenv into the working tree on first use. No
dependency is added to what CI installs, nothing existing is renamed, and no
gate changes its verdict.
