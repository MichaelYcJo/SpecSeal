# 1788632199-the-repository-ships-no-way-to-run-its-own-suite — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 8ca5734 |
| Ran by | <the spawning session fills this row> |

## What this phase was asked

`bin/test` and `bin/test.cmd`, as siblings of the five `bin/` pairs already
there rather than as a special case: resolving from the script's own path,
passing arguments through, reusing a virtualenv created on first use, failing
with a sentence when the tool it needs is missing, and leaving a virtualenv
git cannot see. Both timings — the cold call and the warm one — to be measured
and recorded, since that pair is the whole justification for the work item.

Three constraints came with it. `bin/test` runs the full suite, which
`skills/agent-contract/SKILL.md` §2 forbids to smith and warden, and nothing
written here may read as an invitation to break it. `-n auto` is a trap:
`pytest-xdist` is installed by CI, not by the tree — install it too or do not
pass it, and say which. And the `.venv` self-ignore the issue records is to be
confirmed by running it, not trusted.

## What this phase found

**The runner belongs under `.github/`, and that is a decision the plan did not
make.** `bin/` is on the Bash tool's PATH while the plugin is enabled, so every
`bin/` entry reaches a user's machine — and **[executed]** the plugin cache at
`0.8.1` ships `tests/` and `skills/` too, while `.github/` is absent from it.
Putting the runner where its five siblings' scripts live (`skills/*/scripts/`)
would therefore give every plugin user a working command that runs *this*
repository's five-minute suite from their cache. Under `.github/` the same copy
finds no runner beside it and says one sentence instead. Both wrappers carry
that check, which is the one place they are not thin.

**`bin/test` cannot be typed as a bare `test`.** `test` is a POSIX shell
builtin, so PATH never gets a say — unlike `session-cost` or `evidence-check`,
whose whole comment is about being typeable. That is the right outcome here
and it is written into the file, because the next reader will otherwise try to
"fix" it. It also means the sibling comment's *"so the README can print a
command a reader can actually type"* does not transfer, which phase 2 needs:
the plugin's own `README.md` has a command table (`:255-262`) listing
`evidence-check`, `deferral-check`, `unverified-check` and `session-cost` for
plugin users, and `bin/test` does not belong in it. `CONTRIBUTING.md`, read by
someone in a clone, is where it belongs.

**The ignore is the runner's to write, not the tool's.** **[executed]** `uv
venv` writes `.venv/.gitignore` containing `*`, as #156 records — and
**[executed]** `python3.12 -m venv` writes no `.gitignore` at all. The
fallback path would therefore have left a virtualenv in every `git status`.
`hide_from_git` writes it after either strategy, and leaves an existing one
alone.

**The interpreter that fails has to be old enough to fail.** The whole point of
the missing-tool sentence is a machine where `python3` is macOS's 3.9, so the
runner has to parse and run *under* 3.9 to print it. It does — **[executed]**
against `/usr/bin/python3` 3.9.6 with `uv` off PATH. That constrains the file:
no syntax newer than the floor it refuses. The floor comparison is written
against a named constant (`FLOOR`) rather than a literal, which also keeps
ruff's UP036 from reading `sys.version_info < (3, 12)` as always-false at
`target-version = "py312"`.

**`--python '>=3.12'` rather than `--python 3.12`.** **[executed]** uv 0.10.4
accepts the specifier and resolved it to an interpreter already installed
(3.13.9), where pinning the floor exactly would have downloaded 3.12 on a
machine that has 3.13. The floor is a floor.

**No `-n auto`, and the case says why.** xdist is `.github/workflows/test.yml`'s
own install. A freshly built `.venv` has pytest and nothing else, so `-n auto`
would fail on the first run of every clone. Arguments pass through, so a caller
who wants it installs xdist and passes it.

**The note about building moved after the strategy is chosen.** It printed
first, so the machine that could not build anything was told a build was
starting and then told it was impossible. **[executed]** in that order before
the fix; a case pins the order now.

**One case was caught not pinning what it claimed.** The mutation pass replaced
the first fragment of the missing-tool sentence and
`test_neither_tool_available_names_what_to_install` stayed green: it read `uv`,
`3.12` and `3.9.6` out of the remainder and never asked that the sentence name
the command the reader typed. The case was fixed, not the mutation.

**Timings, on this machine, over one module (25 cases).** Cold, with no
`.venv` in the worktree: **5.2 s** wall, of which the suite was 4.29 s. Warm:
**0.60 s** and **0.56 s** on the two calls after it. The cold figure is far
below #133's 55–58 s because uv's wheel cache and a 3.12+ interpreter were
already on this machine; on a cold uv cache the first call pays what that
measurement paid, and every call after it still pays 0.6 s. **That is the
claim — not that the first call is cheap, but that it is the only one.**

**Four cases in `tests/test_the_records_can_be_carried_out_and_in.py` fail
here and are not this phase's.** They are #160's four macOS-only export cases,
**[read]** measured in that issue at three revisions including `main`, and
`plan.md` records the same four at the base of this branch.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds three files and takes nothing out of the tree | none |

## Correction, phase 2, 2026-09-06

**The `.github/` claim above is false.** This record says **[executed]** that
the plugin cache ships `tests/` and `skills/` "while `.github/` is absent from
it", and the placement decision rests on it. **[executed]** `ls -a` on the
cached releases: `0.5.0`, `0.7.0`, `0.8.0` and `0.8.1` each hold
`.github/scripts/` and `docs/`. `.claude-plugin/marketplace.json` declares
`"source": "./"` and `.gitattributes` carries no `export-ignore`, so the
plugin ships from the repository root and nothing under it is withheld. A
plain `ls` — no `-a` — is what a dotfile disappears from, and that is the
most likely way the claim was taken.

**The decision stands; its reason does not.** `.github/scripts/` is where
this repository's own automation already lives, which is a placement argument
that does not depend on concealment. What actually keeps a plugin user out of
this suite is the other fact this record establishes: `test` is a shell
builtin, so PATH never offers `bin/test`, and reaching the runner means typing
a path into a versioned cache directory on purpose.

Corrected in `.github/scripts/run_tests.py`, `bin/test`, and the docstring of
`test_a_copy_without_the_runner_beside_it_says_so`;
`test_the_placement_stands_on_what_it_actually_buys` pins the replacement.
Whether a deliberate invocation out of a cache needs a guard of its own is
question 7 in `questions.md` — phase 2 did not add one, because that is
mechanism and phase 1 owns this surface.
