# Implementation Plan: the release check never watched bin/

<!-- specs/1788302682-the-release-check-never-watched-bin/plan.md — HOW, in
phases. This work alters a gate's verdict, so approval of this plan is the
gate; the spawn instruction delegates that approval (recorded in
questions.md, Q0). -->

## Summary

Add `bin` to the hygiene step's *what ships* pattern, say so in the release
document, and pin the pattern with a test that classifies every tracked
top-level entry of the repository so the next shipping root cannot go
unwatched.

## Technical context

- `.github/workflows/hygiene.yml`, step `a change to what ships must move the
  version` — exits 0 unless `github.base_ref` is `main`, then filters the
  diff's file list through
  `grep -E '^(skills|agents|hooks|templates|\.claude-plugin)/'`. Five roots;
  `bin/` is absent.
- `bin/` holds four wrappers with `.cmd` twins. That it ships is verified two
  ways: **executed** — this session's `PATH` carries
  `~/.claude/plugins/cache/specseal/specseal/<version>/bin` and
  `command -v evidence-check` resolves there; **read** — the Claude Code
  plugin reference lists `bin/` as *Executables added to the Bash tool's
  PATH … while the plugin is enabled*, and `README.md` §CLI says the plugin
  puts `evidence-check` on PATH.
- `docs/branch-and-release.md` §Two things carry the version enumerates the
  five roots in prose; it has to say six.
- No test reads the pattern today (`grep -rn 'hygiene.yml' tests/` finds two
  files, both pinning other steps), which is how `bin/` fell out unnoticed.
- CI runs `pytest tests/ -q -n auto` on 3.12 across three OSes, so the test
  matches the pattern with Python's `re` rather than by spawning `grep`; the
  pattern uses only anchors, alternation and an escaped dot, which the two
  engines read alike.

**Failure scenario of the chosen approach** (what breaks in 6 months): a
loader-side change makes a new directory ship — `commands/` returns, say. The
classification test fails on the unclassified entry and whoever adds it has
to decide; if they classify it as home wrongly, the gap returns with a
written decision attached, which is the state this issue started without.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Add `bin` to the pattern and nothing else | the next shipping root falls out exactly the way `bin/` did — noticed while writing something up, never by a check | rejected |
| Invert the pattern: everything ships unless it is in a home list (`docs`, `tests`, `specs`, …) | a release PR that adds `SECURITY.md` or a `.gitattributes` line demands a version bump; a wrong deny at the release is a stopped release, and the home list rots the same way the ships list did — only now toward blocking | rejected |
| Add every component the plugin reference documents (`commands`, `workflows`, `output-styles`, `themes`, `monitors`, …) whether or not it exists here | the pattern names directories nobody can open, and a reader cannot tell a shipping root from a speculative one; the test below catches the arrival of any of them without the pattern carrying ghosts | rejected |
| Add `bin` to the pattern, and pin the pattern with a test that classifies every tracked top-level entry | the wrong-classification case above, which at least leaves a decision in the diff | **chosen** |

**Failure direction.** The gate blocks more: a release PR touching only
`bin/` now fails until the version moves. A wrong deny here costs one commit
to `plugin.json` on a PR that is a release anyway; the wrong allow it replaces
is a wrapper fix that reaches nobody. **Prompt budget:** zero — the step puts
no question in front of a person, before or after.

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | SDD set (spec, plan, questions) committed | files in the tree at the phase commit |289997e |
| 2 | the pin, seen red against the five-root pattern; then `bin` in the pattern and in the release document; the pin green | `pytest tests/test_the_release_check_watches_what_ships.py` red then green; mutation (remove `bin`) red; `ruff check` / `ruff format --check` on the test file |0924dfd |
| 3 | changelog fragment, ledger fragment, overview | the two hygiene-adjacent test files green; `evidence_check.py --strict .` clean |d768805 |

## Operational impact

None to a user of the plugin. To a release: a pull request into `main` that
touches `bin/` now needs `plugin.json` moved, which the release-preparation
commit already does.
