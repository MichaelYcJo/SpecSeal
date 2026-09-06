# Implementation Plan: the printed ledger name is the file that was read

<!-- seal/specs/1788686494-the-printed-ledger-name-collapses-through-relpath/plan.md -->

## Summary

`os.path.relpath` normalises `..` the way `normpath` does, without consulting
the filesystem. Where a `--ledger` pattern crosses a symlink before a `..`,
the checker **opens** the file the pattern names (#153 round 13 fixed that)
and **prints** a lexical guess at it — a different file that exists. One
display helper, every ledger-path-to-name site through it, one integration
case and unit cases.

## Technical context

- `skills/evidence-check/scripts/evidence_check.py#resolve_patterns` — returns
  the pattern's own spelling, deliberately, and its docstring says why. The
  display side is the half that was never brought along.
- The sites, found by the property *a ledger path rendered for a person* and
  not by the issue's list: `check_ledger`'s `ledger unreadable` row, `migrate`'s
  `left` collector, `reverify`'s `unreadable` collector, `main`'s per-ledger
  header, and — **not in the issue's four** — the `--ledger narrowed this run`
  block, which prints `os.path.relpath(path, root)` under the name `path`
  rather than `ledger`. A grep for `relpath(ledger` finds four of five.
- `default_patterns(root)` joins under `seal_home(root)`, so an ordinary run's
  ledger spelling is `./seal/ledger.md` under root `.` and must keep printing
  `seal/ledger.md`.

**What breaks in 6 months.** A sixth site is added and calls `relpath` because
that is what the standard library offers. The phase-2 case that reads the
source for a `relpath` applied to a ledger path is what catches it; without
that case the helper is a convention, and a convention is what this defect
already was.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `os.path.realpath` on both sides, then `relpath` | A fixture that asks `realpath` for its own expected value agrees with a broken checker — round 14 declined exactly this on the reading side. It also renames a file the operator did not name | **No** |
| Print the pattern's spelling verbatim, always | An ordinary run's header becomes `./seal/ledger.md`, and in local mode an absolute path under the git directory. Correct and noisier every day to fix a case that is rare | **No** |
| Strip the root's own segments when the path literally starts with them, otherwise print the spelling verbatim; never fold `..` | A path under the root reached by a *different* spelling of the root prints verbatim — longer, never wrong | **Yes** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The display helper, its docstring naming why `relpath` cannot be used, and unit cases seen red against `relpath` | The new unit cases; `./bin/test` over the touched test modules | `fa53e67` |
| 2 | Every site in the class through the helper — the class enumerated by the property, with the scan-suggestion site judged in writing — plus the integration case pinning the printed header against the file read, and the source-reading case that refuses a future `relpath` on a ledger path | The integration case seen red first on the POSIX branch; `./bin/test` over the evidence-check modules | |

## Operational impact

None. No migration, no new dependency, no environment variable, no
compatibility break — the output text changes only where it was naming the
wrong file.
