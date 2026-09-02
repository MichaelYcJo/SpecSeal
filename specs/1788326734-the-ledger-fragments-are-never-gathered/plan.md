# Implementation Plan: the ledger fragments fold at release

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered/plan.md — HOW,
in phases. This is the Design Gate's artifact: the work changes what a
release does, so approval of this plan is the gate. The orchestrator
pre-answered the gate's questions in the spawn prompt; what it could not
answer is in questions.md. -->

## Summary

One script beside `gather_changelog.py`, shaped like it, that moves every
`.specseal/map/<id>.md` into `.specseal/map.md` under a release heading and
refuses while any `specs/<id>/evidence-todo.md` has an open row. One `--check`
step in the hygiene workflow for pull requests into `main`. Every document that
said *never gathered* corrected.

## Technical context

- `.github/scripts/gather_changelog.py` — the model. `marker()`,
  `fragments()`, `ungathered()`, `section()`, `insert()`, `main()` with
  `--version` · `--date` · `--check` · `--dry-run` · `--root`. Exit 0 done, 1
  nothing to gather or a fragment missing. The fold mirrors the names and the
  flags; where it differs (appends rather than inserts, removes the fragment
  after writing, carries the guard) the docstring says so.
- `skills/evidence-check/scripts/evidence_check.py#check_ledger` — scans a
  ledger with `ANCHOR_RE.finditer(text)`, reads no tables and no headings, and
  de-duplicates on `(coordinate, hash)` per file. This is what makes a fold
  invisible to the checker: an anchor is the same anchor in either file. The
  default globs at `main()` read both `.specseal/map.md` and
  `.specseal/map/*.md`, so nothing in the checker changes.
- `tests/test_the_changelog_is_gathered_at_release.py` — the test shape to
  mirror: a `tree` fixture under `tmp_path`, `run()` through `subprocess`
  with `--root`, a `gather()` helper that proves the effect landed rather than
  trusting the exit code (its round-1 🟡 9), and a "this repository" block
  pinning the workflow and the documents.
- `.github/workflows/hygiene.yml`, step "every changelog fragment reached the
  released file" — the `base_ref != main → exit 0` shape the fold's check
  step copies.
- The two `evidence-todo.md` files in the tree — one `drained` above the
  table, one below; neither has a status column. The rule in `spec.md`
  reads both as closed.

**What breaks in six months.** Two things, and both are named so a reader
can weigh them rather than discover them.

- A fragment written after its work item was folded — the same id, a second
  time — is refused rather than folded twice, and the refusal says the marker
  is already there. Someone has to compare by hand. The alternative, folding
  it under a second marker, would put the same claim in the file twice with
  no way to tell which is current.
- The `drained` word is a convention two files happen to share, and a file
  that closes its rows some third way — a status column, say — reads as open
  and stops the release. That is the right direction: a stop names the file,
  and the fix is to write `drained` or ✅, both of which are documented. A
  guard that guessed at a third spelling would go quiet exactly where it
  should not.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Mirror `gather_changelog.py`: marker per work item, `--check` on release pull requests, append a release section to `map.md`, remove the fragment** | a copy-edit inside a folded section never reopens the fragment (marked, not matched); a fragment re-created after its fold is refused with the marker named, and a person compares. The cost is that `map.md` grows by release rather than by area, which the spec's "Out" accepts on purpose | **chosen** |
| B. Merge each fragment's rows into `map.md`'s existing `## area` sections by heading text | a fragment's area headings are its own, so almost nothing matches and the step invents new areas anyway; where a heading does match, the rows land under it with no marker, and `--check` has nothing to look for. A release step that makes a judgment per row is one nobody runs unattended | rejected |
| C. Fold into the gathered ledger but keep the fragment, marked | the directory keeps one file per work item forever, which is the half of the defect this ticket exists to end; and every row would be in the tree twice, counted twice by the checker | rejected |
| D. Put the guard in a separate script and let the fold assume it ran | the fold runs without the guard once — the order is a thing somebody remembers — and a work item's only copy of a fact is removed with its fragment while its `evidence-todo.md` still says the fact never reached the ledger | rejected; the guard is inside the fold, before the first write |
| E. `--check` verifies fragments only, not the evidence-todo rows | a fold done by hand, or a release branch where someone moved rows themselves, reaches `main` with an open row; the last moment anyone is looking is the release pull request | rejected; `--check` runs the guard too |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `fold_ledger.py` folding two fragments into `map.md` on a fixture: marker, order, byte-identical rows, fragment removed, `--dry-run`, refusal on a present-and-marked fragment, nothing-to-fold exit 1; the test file with those cases | the new test file's fold cases, green; the `evidence_check.py` totals equal before and after on the fixture | `024f374` |
| 2 | The evidence-todo guard: `spec.md`'s four-step rule in code, refusal naming the file with nothing written, one case per closed shape (`drained` above, `drained` below, ✅ rows, header only, no file); `--check` covering fragments left and open rows | the guard cases, green; `--check` in both directions | `024f374` |
| 3 | The hygiene step, and every document corrected: `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, `README.ko.md`, `docs/branch-and-release.md`, `docs/flow.md`, `.specseal/README.md`, `.specseal/map.md`'s header, `templates/map.md`, `templates/specseal-README.md`, `skills/implement/SKILL.md`, `skills/evidence-check/SKILL.md` | the "this repository" cases: the workflow step gated on `main`, no document says *never gathered*, the release sequence names the fold; `tests/test_docs_line_wrap.py` on the covered files | `72cf296` |
| 4 | The record: the fold executed on a copy of this repository's own ledger with checker totals compared; `changelog.md`; `.specseal/map/<id>.md` with the executed rows; `overview.md`; this column | `evidence_check.py --strict .` at 0 broken; the fragment rows opened against the code | `e59282f` |
| 5 | Round 1's fix pass: `/`-joined message paths through `under()`, the self-check test reading the marker after a fold, a line-anchored `is_marked` for the fold and `--check` alike, `open_rows` and `demote` split on `\n` alone with trailing whitespace kept and fenced `#` lines left as text, the fragment's branch-commit citation rewritten, `map.md`'s "empties" sentence, `evidence-todo.md` drained, tests-todo rows 1–5 planted | the fold test file green with the six new cases; four of them red against the unfixed script on this platform (the backslash case can only go red on Windows, where `os.path.join` differs, and the after-fold case pins the test body rather than the script); the guard on this tree reporting no open row; `evidence_check.py --strict .` | |

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.** Feature branches squash here, so these
commits stop resolving at the merge, and a rebase during the work orphans
them earlier; nothing measures from this column.

## Operational impact

- **The release sequence gains one command.** `docs/branch-and-release.md`'s
  "Release preparation runs:" block now lists the fold beside the gather.
  Both run in the same release-preparation commit; running the gather alone
  leaves the release pull request red on the new hygiene step.
- **A release pull request can now be refused for an old work item.** A work
  item released in an earlier version whose `evidence-todo.md` was never
  drained stops the fold. The remedy is to drain the file on the release
  branch. Both files in the tree today are drained.
- **`.specseal/map.md` grows again**, once per release, by the rows the
  release's work items wrote. `.specseal/map/` empties at each release.
- No new dependency; the script is stdlib only, like its sibling. Nothing in
  the shipped plugin (`skills/`, `hooks/`, `agents/`, `templates/`, `bin/`)
  changes behaviour: the script lives in `.github/scripts/`, and the template
  and skill edits are wording.
