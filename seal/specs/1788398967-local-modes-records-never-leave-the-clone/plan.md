# Implementation Plan: local mode's records never leave the clone

<!-- seal/specs/1788398967-local-modes-records-never-leave-the-clone/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

One shipped command, `bin/seal`, with `export` and `import`. It walks the
root `hooks/optin.py` already resolves, writes it to a zip with a manifest,
and merges a zip back without ever overwriting a file. `seal export --check`
is the release-preparation reminder.

The work alters observable behaviour — two new commands, text a person reads
and acts on, and a file format another machine will read — so `spec.md` and
this plan come before the first line of it.

## Technical context

What it builds on:

- `hooks/optin.py#home_at` — the root, and with it the mode. The command
  goes through it rather than spelling `<repo>/seal` or `.git/seal`, which
  is why phase 1 exists: `home_at` answers *which root is in force* and the
  import also needs *where the other one would be*.
- `bin/evidence-check` + `bin/evidence-check.cmd` — the wrapper pair. The
  POSIX one resolves the script relative to itself; the `.cmd` prefers
  `py -3` and falls back to `python`. Four pairs exist; this is the fifth.
- `hooks/console.py#to_utf8` — the streams. The five scripts under
  `skills/*/scripts/` spell the loop inline rather than importing it,
  because they are standalone by design; this one does the same.
- `.github/scripts/fold_ledger.py` — the shape of a release-preparation
  script: `--check` verifies and writes nothing, every message names a
  `/`-joined path, and a run that wrote nothing exits 1.
- `tests/conftest.py#local_home` — the local-mode fixture, and
  `declare_routing(..., home=...)` for a work item under it.

Constraints:

- Standard library only. `zipfile` ships with it — **executed** on
  2026-09-03 under the 3.12.11 the suite runs on, which is the supported
  floor; `ruff.toml` and the workflows install only pytest and ruff, so
  adding a dependency would be this repository's first.
- Windows is a supported platform, so every path that goes into the zip is
  `/`-joined and every path read back is validated before it becomes a disk
  path.
- The suite runs on macOS, Linux and Windows. Symlink cases skip where the
  privilege is absent (`conftest.symlink_or_skip`).

**What breaks in six months.** The manifest gains a field and an old build
reads a new zip. That is why `format` is in it and why an unknown number is
refused rather than tolerated: a zip whose fields moved, read by a build
that assumes the old ones, merges records at the wrong paths — and the merge
is the operation this whole command is built to make safe.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `zipfile.ZipFile.extractall` for the import | The classic path-traversal sink: a member named `../../.git/hooks/pre-commit` is written where it says. A zip is untrusted input — it arrived from another machine by a route nobody controls | **Rejected.** Every member's name is validated, then the file is written by an explicit open, at a path built from segments this code produced |
| Refuse a member that escapes, import the rest | A partial import from a hostile archive is still a decision made by the archive. The user then holds records they believe are a copy and cannot say of what | **Rejected.** One bad member refuses the whole zip, before a byte is written |
| Two commands, `seal-export` and `seal-import` | Four wrapper files instead of two, and the design document, the issue and the README all write the pair with a space | **Rejected.** One `bin/seal` with subcommands, which is also where a later `settle` goes |
| A third subcommand for the reminder (`seal changed`) | A third name for a thing that runs once per release, and `--check` is already this repository's word for *the release step verifies and writes nothing* (`fold_ledger.py`, `gather_changelog.py`) | **Rejected.** `seal export --check` |
| `seal export` writes a zip in shared mode too, for symmetry | The zip is a second copy of committed files that nothing keeps current, and importing it elsewhere scatters `.incoming` files through a tree that already has everything. Symmetry buys a footgun | **Rejected.** Exit 1 with the message that answers what the user was asking: shared mode, here is the path, here is the `mv` if you meant to go local |
| Exit 0 for that refusal | `seal export && cp seal-*.zip /backup` would copy nothing and report success | **Rejected.** Exit 1, matching `fold_ledger.py`'s *nothing to fold* |
| Default the zip into the current directory | The normal place to run it is the repository root, and an untracked zip there is one `git add -A` away from committing the records local mode exists to keep out of the tree | **Rejected.** The default is the parent of the repository root, printed. `--output` overrides and warns if the path is inside the tree |
| Compare remote URLs as strings | ssh at one machine and https at another is the ordinary case, and it would refuse every real import | **Rejected.** Normalised (spec.md, *How two remote URLs are compared*), with the asymmetry written down: a wrong accept needs two repositories at the same host and path |
| Trust the zip's remote without comparing | Another project's records merge in, keyed by id, spread across files, silently | **Rejected.** Refuse and name `--allow-other-repo` |
| The reminder measures file mtimes against a stored timestamp | A copy, a checkout, or a restore resets mtimes; the reminder then reports work nobody did, or misses work somebody did | **Rejected.** Digests per work item, stored in the manifest |
| Store the last-export manifest inside the root | It would ride into the next zip and into a shared-mode commit, and it is this machine's state | **Rejected.** `<git-common-dir>/specseal-last-export.json`, beside the root with the other machine-local state |
| Enumerate the zip's members and the digest's files separately | The two lists drift — a symlink or an unreadable file excluded from one and not the other reports a change nothing made | **Rejected.** One walker, and a test that asserts the zip's namelist equals what it yields |
| Have `seal import` run `evidence-check` | The command would report a pass it did not read, and the check can be slow on a large ledger | **Rejected.** Import prints the command as the next step |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `hooks/optin.py#home_paths` — the two places `seal/` is read from, in order, so nothing outside this module spells either path. `home_at` reads through it and still costs one `git` call | `tests/test_optin_home.py` (existing cases, unchanged) plus a new case for the pair | |
| 2 | `seal export`: the walker, the digest, the manifest, the zip, the shared-mode refusal, the fail directions. `bin/seal` + `bin/seal.cmd` | S1–S4, S12, S16, and the walker/namelist seam case | |
| 3 | `seal import`: name validation, the three outcomes, `--into`, the foreign-zip refusal | S5–S11, S17–S20 | |
| 4 | `seal export --check`: the one-line reminder and the state file it reads | S13–S15 | |
| 5 | The documents that already promise this pair: `README.md`, `README.ko.md`, `seal/README.md`, the changelog and ledger fragments, the closing memo | the doc-wrap and identifier tests; a read of each edited paragraph | |

Each phase ends with something runnable: phase 1 with the suite's opt-in
cases, phases 2–4 with the command doing the thing the phase names, phase 5
with the documents saying what the command does.

**Status is empty, or the commit that closed the phase.** Re-read the column
after any rebase — this branch squashes into `release/v0.5.0`, so these
hashes stop resolving at the merge, and nothing measures from them.

## Operational impact

- **A new shipped command.** `bin/seal` and `bin/seal.cmd` go on the Bash
  tool's PATH while the plugin is enabled, so `bin/` changing is a change to
  what ships. The hygiene step that asks for a version bump exits 0 for a
  base that is not `main`, so this pull request into `release/v0.5.0` does
  not move `plugin.json`; the release that merges to `main` does.
- **A new machine-local file**, `<git-common-dir>/specseal-last-export.json`.
  Nothing else reads it, it is never committed, and deleting it costs one
  reminder that reports every work item as changed.
- **No new dependency, no migration, no compatibility break.** Nothing that
  exists today reads a zip or that state file.
- **Prompt budget: zero.** Neither subcommand asks a question — the design
  says a collision is "reported and not asked about" — and neither is a
  hook, so nothing new fires during a session. Every decision a person has
  to make is a message they read after the command has exited.
