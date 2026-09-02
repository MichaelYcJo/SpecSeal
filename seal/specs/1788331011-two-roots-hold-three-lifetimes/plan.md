# Implementation Plan: two roots hold three lifetimes

Approved 2026-09-02 by the repository owner, after reading the frame; Q1–Q8 stand at their defaults. Spawning the phase-1 smith is the approval.

<!-- specs/1788331011-two-roots-hold-three-lifetimes/plan.md — HOW, in
phases. This is the Design Gate's artifact: the work changes what every gate
reads, so approval of this plan is the gate. Each phase is sized for one
smith spawn; the spawn that wrote this built nothing. -->

## Summary

`.specseal/` and `specs/` become `seal/`, laid out by lifetime. The opt-in
becomes the folder's presence at either of two places, read once in
`hooks/optin.py`. A new session-start hook moves an existing tree once per
repository, refuses a dirty one, and re-points the ledger rows that cite a
moved file. Every gate, checker, release script, template, skill, agent and
document follows. Three phases, one spawn each: the code and this
repository's own move; everything that is re-pointed by script; the test
fixtures and the READMEs.

## Technical context

Coordinates are as of `07a0fc8` on this branch. Every fact marked
*executed* was run by the framing spawn; the rest were read.

- `hooks/optin.py#home` — the one address every gate reads. `HOME` at line
  25 is the whole signal; the `scratch` file at line 30 is the opt-out;
  `repo_root` already carries a rider about the cost of resolving the root
  in every caller. Four hooks each carry their own `git_dir()`
  (`implementer.py:41`, `review-skill-gate.py:96`, `session-lease.py:42`,
  `worktree-guard.py:1193`); the common-git-dir lookup this work adds to
  `optin.py` is a fifth unless one of them moves in.
- `hooks/ledger-migrate.py` — the model for the new hook: `attempted()` /
  `stamp()` on a one-root-per-line marker, `dirty()` through
  `git status --porcelain -- <paths>`, one `systemMessage` line, silence when
  there is nothing to do. `hooks/dispatch.py:46` runs the session-start group
  in order, so the root move must precede the ledger-format migration for
  the second to see the new globs.
- `skills/evidence-check/scripts/evidence_check.py#check_ledger` — scans
  each ledger with `ANCHOR_RE` and reads no tables, so a row that moves
  between files is the same anchor. **Executed**: 190 anchors across
  `.specseal/map.md` and seven fragments, `160 ok · 0 drifted · 0 broken`
  after per-file de-duplication; exactly one anchor's path is under a
  directory this work moves (`.specseal/map.md` →
  `specs/1788184145-the-gate-stops-the-session-editing-its-tests/rounds/round-3.md`).
  So `git mv` alone leaves one BROKEN row, and the handoff's unverified
  claim holds only with the rewrite in spec §"The move, in order", step 6.
- `skills/code-review/scripts/chain_check.py:1586` — `changed_routing`
  takes every `routing.md` in `git diff --name-only base...HEAD`, and only
  falls back to `declared_for_this_branch` when that set is empty. A rename
  shows up in that diff under its new path, so the move would put all
  fifteen declarations under review on this pull request, each needing its
  round records' `Target SHA` to resolve. Spec S10 excludes renames.
- `skills/verify/scripts/unverified_check.py` — the deletion check lists
  `overview.md` at the base ref and keeps those under the path arguments,
  so `--baseline origin/release/v0.4.0 seal/specs/` sees nothing at the
  base and reports nothing gone. No special case is needed for this pull
  request; the same is true of any later one.
- `.github/scripts/fold_ledger.py`, `gather_changelog.py` — `marker()`
  writes `<!-- specs/<id> -->` and `--check` looks for it. The text stays
  (Q2): it names the work item by its sub-directory, which is still
  `specs/`, and changing it would make every released entry read as
  ungathered.
- `tests/conftest.py#declare_routing` builds `repo / "specs" / item`; two
  test files define their own `make_repo(path, opted_in)` writing
  `.specseal/`. **Executed**: 31 test files mention `.specseal` or `specs/`
  (the record counted 20), the heaviest being
  `test_a_row_points_by_content.py` (70 lines) and
  `test_the_ledger_fragments_fold_at_release.py` (46).
- Documents mentioning the old paths, **executed** counts: `README.md` 19,
  `README.ko.md` 19, `docs/review-chain-spec.md` 14, `CONTRIBUTING.md` 7,
  `CLAUDE.md` 7, `docs/branch-and-release.md` 7,
  `docs/review-handoff-protocol.md` 3, `docs/flow.md` 1; agents 5 · 4 · 1.
  `docs/one-root-by-lifetime.md` and its twin (40 each) are left alone.
- The suite runs as `pytest tests/ -q -n auto` (`.github/workflows/test.yml:68`).

**What breaks in six months.** Named so a reader can weigh it.

- A repository that never starts a session after updating keeps
  `.specseal/`, and every gate is silent there until it does. The silence
  is the fail direction the record fixes, and the hook is the only thing
  that ends it; a person who reads the CHANGELOG entry can run the move by
  hand, and the entry says how.
- The marker is per machine. A second machine with the same clone finds the
  tree already moved and does nothing, which is right; a second clone on
  the same machine is a different root and gets its own line.
- `~/.claude/specseal/` keeps its name after the root does not. A reader
  who expects every `specseal` to have become `seal` finds the exception
  in the state directory, and Q1 says why it stays.
- Prose paths inside released round records and overviews still say
  `specs/<id>/`. They are true of the SHA they name, and rewriting history
  is not on offer; a reader following one lands one directory up from the
  file and finds `seal/`.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. One move, no fallback: the hook moves everything once, every reader learns the new path, the old path is an error that names the destination** | a repository that never starts a session keeps the old tree and silent gates until it does. The cost is a one-line message at the first session start and a `git diff` to review, which the ledger migration already asks for | **chosen** |
| B. A compatibility period: `optin.home()` returns whichever of `seal/` and `.specseal/` exists, every reader takes both, the old one is dropped in 0.5.0 | two places to look in the one module every gate imports, forever or until a date nothing enforces (the handoff protocol's exact words for why the round records did not get this); a repository with both — the state a half-finished move leaves — has no defined answer; fifteen readers each carry the pair and drop it separately | rejected, `docs/review-handoff-protocol.md` §"Why the records moved a second time" |
| C. Move by a command a person runs (`seal migrate`) rather than at session start | the remembering is the cost the ledger migration's docstring rejects; a person who does not know the layout changed cannot know to run it, and the gates give no sign because the fail direction is silence | rejected; the command stays available through the hook's module for CI and by hand |
| D. Move only `.specseal/` and leave `specs/` in place until `settle` | two roots remain, which is the defect; `routing.md` and the rounds stay where `settle` will not look, and the sub-directory decision (Q1) is deferred to an item that has no reason to make it | rejected |
| E. Rename the markers to `<!-- seal/specs/<id> -->` for consistency | every released entry in `CHANGELOG.md` and every folded section in the ledger reads as ungathered at the next `--check`, and the release pull request goes red for history; fixing that means rewriting the released file, which is the copy-edit case the marker was designed to survive | rejected, Q2 |
| F. Keep the `scratch` opt-out as a file in `seal/` | a committed `seal/scratch` silences every gate in every clone, which is the hazard `test_this_repository_carries_no_scratch_marker` exists for; a marker under the common git dir cannot be committed and needs no such test | rejected in favour of `.git/specseal-scratch`, Q4 |
| G. Look only at `<repo>/seal/` in 0.4.0 and add `.git/seal/` in #80 | #80 then edits the one module every gate imports, and every hook that joined a path under the root; the two-place lookup is two `isdir` calls and the ticket's own done-when names both | not chosen; Q3 leaves it to the owner |

## Phases

Vertical slices — each phase ends with something runnable and verified, and
each is one smith spawn. The test scope per phase is the files the phase
touches; the full suite runs once after the review rounds settle.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The root and the opt-in.** In this repository: `git mv .specseal/map.md seal/ledger.md`, `.specseal/map seal/ledger`, the rest of `.specseal/` to `seal/`, every `specs/<id>` to `seal/specs/<id>`, the one ledger row re-pointed, `seal/README.md` rewritten from the new template, `seal/ledger.md`'s header re-pointed. In code: `optin.py` (`HOME`, the common-dir second place, `specseal-scratch`), `routing.py`, the commit gate's `DOC_ROOTS` and prompt text, `dispatch.py`'s group, the new `root-migrate.py` with its marker and the seven-step move, `ledger-migrate.py` and `evidence-advisor.py` globs, `evidence_check.py` defaults and parity path, `fold_ledger.py`, `gather_changelog.py`, `chain_check.py` (prefix, and renames excluded). The tests for each of those files re-pointed so they pass, and the new `test_the_root_migrates_itself.py` for S5–S9 | `evidence_check.py .` executed before and after the move, both at `160 ok · 0 broken`, outputs in the fragment (S8); `chain_check.py --baseline origin/release/v0.4.0` executed on the branch and read (S10); `gather_changelog.py --check` and `fold_ledger.py --check` executed and read (S13); the test files named in S2–S13 green, plus `test_dispatch.py` and `test_the_ledger_migrates_itself.py` | `ea988a5` — the move itself is in `e2a0dfe` |
| 2 | **Everything re-pointed by script.** `hygiene.yml`'s argument; the templates (`specseal-README.md` → `seal-README.md`, `map.md` → `ledger.md`, the five SDD headers, `sdd-overview.md`'s proof-block line); the skills (`implement` layout table and bootstrap section, `code-review`, `verify`, `evidence-check`, `parity-setup`, `legacy-parity`, their `SKILL.md` prose); the three agents; `docs/review-chain-spec.md`, `docs/review-handoff-protocol.md`, `docs/branch-and-release.md`, `docs/flow.md`; `CONTRIBUTING.md`, `CLAUDE.md`. Done by one Python script written with `Write` and run once, every substitution asserted, then committed with the script's output in the commit body. The S15 test over the list | the S15 test green; `tests/test_docs_line_wrap.py` on the covered files; `tests/test_the_set_a_work_item_always_has.py`, `tests/test_handoff_outlives_the_merge.py`, `tests/test_release_hygiene.py` green; `grep -rn "\.specseal\|specs/<" hooks skills agents templates docs CONTRIBUTING.md CLAUDE.md` executed and read, with the design record and `root-migrate.py` as the only hits | `7f34111` |
| 3 | **The fixtures and the READMEs.** `conftest.py#declare_routing` on `seal/specs`; both `make_repo` helpers writing `seal/`; every test that asserted the old paths in its own fixture or message (`test_a_row_points_by_content.py`, `test_the_ledger_fragments_fold_at_release.py`, `test_optin_home.py`, `test_handoff_outlives_the_merge.py`, `test_routing_is_recorded.py`, `test_unverified_rows_close.py`, `test_the_changelog_is_gathered_at_release.py`, `test_evidence_check.py`, `test_review_skill_gate.py`, the rest of the 31); `README.md` and `README.ko.md` together, in one commit, so the hygiene warning stays quiet; the fragment `seal/ledger/<id>.md` with the executed rows from all three phases; `overview.md`; `changelog.md` final; this column | the 31 test files green, run as one command; the two READMEs in one commit (`git show --stat` read); `evidence_check.py --strict .` at 0 broken; the fragment's rows opened against the code | |

Phase 1 is the one that cannot be split: the move and the readers of the
moved paths have to land in one commit range, or the suite has no state in
which it passes. It is still several commits — the code first, the move
second, the tests third — because a ledger row names no commit and the
branch squashes.

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.** Feature branches squash here, so
these commits stop resolving at the merge, and a rebase during the work
orphans them earlier; nothing measures from this column.

## Operational impact

- **Every repository using this plugin is moved at its first session start
  after updating.** One line is printed, the moves are staged, and the
  person reviews `git diff --cached` and commits. A dirty `.specseal/` or
  `specs/` refuses the move with a line saying to commit first. A
  repository with `.specseal/scratch` is left alone. The CHANGELOG entry
  carries the by-hand sequence for a repository that cannot wait for a
  session.
- **Until that session start, every gate is silent in that repository.**
  The signal moved, and the old one is read by nothing but the migration
  hook. This is the fail direction the record keeps on purpose.
- **A new state-file:** `~/.claude/specseal/root-migrated`, one root per
  line, beside `ledger-migrated` and `version-check`.
- **A new opt-out location:** `<git-common-dir>/specseal-scratch`, a file.
  `.specseal/scratch` is read by nothing after this change, and a
  repository still carrying it is not migrated (S9).
- **CI:** `hygiene.yml` passes `seal/specs/` to `unverified_check.py`. The
  `ledger` job in `test.yml` is unchanged. The chain check no longer judges
  renamed declarations, on this pull request or any later one.
- **Templates renamed:** `templates/seal-README.md`, `templates/ledger.md`.
  Anything outside this repository that copied `templates/map.md` by name
  has to follow.
- **The version moves at the release**, not here: the pull request lands on
  `release/v0.4.0`, and `plugin.json` is left alone.
- No new dependency. Everything is stdlib and `git`.
