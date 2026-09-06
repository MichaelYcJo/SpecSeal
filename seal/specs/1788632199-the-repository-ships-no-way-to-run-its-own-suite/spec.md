# Feature Specification: the repository ships a way to run its own suite

<!-- seal/specs/1788632199-the-repository-ships-no-way-to-run-its-own-suite/spec.md -->

Closes #156.

## The issue's premise is half wrong, and the half that is wrong changes the fix

#156 says *"There is no `pyproject.toml`, no dev-requirements file, and
nothing in either README that names a command."* Two of those three hold.
The third does not: **`CONTRIBUTING.md` §*Running the checks* already names
one**, `uvx --with pytest python3 -m pytest tests/ -q`, with the Python floor
beside it.

So the gap is not that nothing names a command. It is that **the command the
repository names is the one that pays for its environment on every call** —
the same `uvx --with pytest` form whose setup cost #133 measured at 55–58
seconds on each of seventeen test calls, 1.9 minutes attributed to repeats in
one segment. A session that finds that line and follows it lands exactly in
the cost this work item exists to remove.

That is why the answer is a `bin/` entry rather than a line of prose. A line
already exists; what does not exist is a command that is cheap the second time
it runs.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | the fix belongs at the cause rather than in every spawn prompt — a per-segment fix an orchestrator applies by hand is the shape this goal refuses |
| #51 observation 4 | *"handing it over is the fix for a segment; a virtualenv in the tree is the fix for the cause"* |
| `CONTRIBUTING.md` §*Running the checks* | the section that already names a command, and therefore the section that has to name this one |
| `skills/agent-contract/SKILL.md` §2 | `bin/test` runs the FULL suite, which the contract forbids to smith and warden. Whatever it is, it must not read as an invitation to break §2 |

## Scope

**In.**

1. `bin/test` and `bin/test.cmd`, beside the five pairs already there
   (`evidence-check`, `unverified-check`, `session-cost`, `deferral-check`,
   `seal`). It resolves its own path the way its siblings do, passes arguments
   through, and **does not pay for its environment twice**: a reused
   virtualenv, created on first use, so the second call is fast.
2. `CONTRIBUTING.md` §*Running the checks* names it, and the `uvx --with
   pytest` line stops being the first thing a reader copies.
3. The README that a session opens gets the one line it needs, if the
   repository's own convention puts commands there — check before writing.
4. The per-segment fix stops being needed: whatever names the runner to a
   spawned segment says `bin/test` rather than an absolute path into somebody's
   checkout.
5. Cases pinning each of the above.

**Out.**

- **A `pyproject.toml`.** The owner chose the `bin/` answer from the four the
  issue enumerates. Declaring the package is a larger change than this release
  is measuring, and the suite needs one dependency.
- **Changing what CI installs.** `.github/workflows/test.yml`'s `pip install
  pytest pytest-xdist` is the runner's own arrangement and works; making it
  call `bin/test` is a separate argument about CI, not about a session.
- **Making the full suite cheap to run often.** It takes five minutes. §2 says
  a segment must not run it at all, and this work item must not make that
  easier to ignore.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A session finds the command where it already looks | Given a session about to run a test · when it opens `CONTRIBUTING.md` §*Running the checks* · then the first command named is `bin/test` | a case over `CONTRIBUTING.md` |
| The second call is cheap | Given `bin/test` has run once · when it runs again · then it does not re-resolve or re-download its dependency | measured: time both calls and record the pair |
| It runs from anywhere | Given any working directory inside the repository or a worktree of it · when `bin/test` runs · then it finds the suite and the interpreter without a path from the caller | executed from the worktree and from a subdirectory |
| Arguments pass through | Given `bin/test tests/test_session_cost.py -q` · when it runs · then only that module runs | executed |
| It is a sibling, not a special case | Given the five existing `bin/` pairs · when `bin/test` is read beside them · then it resolves its own directory the same way and carries the same shape of comment | a case over `bin/`, and a read |
| §2 is not quietly widened | Given a segment reading whatever names the runner · when it does · then the text still says the full suite is the orchestrator's, once | a case over the file that names it |

## Data & interfaces

No API. One new pair of executables in `bin/`, and prose in `CONTRIBUTING.md`.
Whatever virtualenv `bin/test` uses must be invisible to git — the issue
records that `uv venv` writes `.venv/.gitignore` containing `*`, so a `.venv`
hides itself; confirm that rather than assuming it, and if the chosen tool does
not do it, the ignore is this work item's to add.

## Open questions → questions.md
