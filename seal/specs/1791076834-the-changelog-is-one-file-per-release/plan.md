# Implementation Plan: the changelog is one file per release (#728)

<!-- seal/specs/1791076834-the-changelog-is-one-file-per-release/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

Split `CHANGELOG.md`'s 44 sections into `changelog/<X.Y.Z>.md` byte for byte,
leave `CHANGELOG.md` as an index that keeps one `## X.Y.Z — <date>` line per
release, and move the gather, the release-note publisher, the shipped
survivor sweep, the update skill and every sentence and test that reads the
sections to the new files. The fragment convention a change writes is
untouched. The release that ships this, 0.18.1, is the first one the new
gather writes (spec D6).

## Technical context

Read on acc3bae6 (= `release/v0.18.1` at e141980a plus the routing commit).

- `.github/scripts/gather_changelog.py#main` opens `os.path.join(root,
  "CHANGELOG.md")` for both `--check` and the gather, and `#insert` places a
  section above the first `## ` line or appends into an existing one.
  `#live_markers` reads the marker lines through `unverified_check.py`'s
  `live_lines` and `gfm_lines`; that reading is kept and applied per file.
- `.github/scripts/publish_release_note.py#main` reads `ROOT/CHANGELOG.md`
  through `#section_body`; `#release_body` ends the note with a
  `blob/{tag}/CHANGELOG.md` link.
- `skills/code-review/scripts/survivor_check.py` compares `path == CHANGELOG`
  in `sentences`, `corrected` (the `newly_released` arm) and `score` (the
  split arm), and `#gathered_fragments` reads only `CHANGELOG.md` at a
  revision. `#released_lines` and `#blank_released` read regions off
  `VERSION_HEADING` and need no change if a release file keeps its heading.
- `skills/update/SKILL.md` step 2b reads the first `## ` line of the installed
  `CHANGELOG.md`; step 3 summarises the marketplace clone's `CHANGELOG.md`.
- Measured with a throwaway in-memory script on acc3bae6 (executed, nothing
  written): every one of the 44 headings is preceded by exactly one blank
  line after a non-blank one; the file begins `# Changelog\n\n`, ends with one
  newline, and has no CR; splitting at the headings, stripping each part's
  trailing newlines to one, and joining with one blank line reproduces the
  file exactly. The largest section is 33,766 bytes.

**Failure scenario of the chosen approach, six months on.** Three ways, each
with what catches it:

- The index line and the release file's heading drift apart (a hand edit, a
  bad conflict resolution). S2's standing case refuses it.
- A release preparation leaves `changelog/X.Y.Z.md` untracked and commits the
  index line only. The release pull request's suite fails S3 (the file for
  `plugin.json`'s version must exist), and if it got past that, the publisher
  exits 1 at the tag naming the file, which is the loud direction.
- A future reader is written against `CHANGELOG.md`'s text and finds only the
  index. The index's paragraph names the release files, and the class of
  readers is enumerated in `spec.md` §*The readers and writers, by
  construction* for the next person to extend.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Index as a bullet list of links, no `## ` lines | The update skill that runs the update into 0.18.1 is 0.18.0's, already loaded; its step 2b reads the first `## ` line of the installed `CHANGELOG.md`, finds none naming the new version, stops, and prints a repair that moves the install directory — for every user who updates | Rejected (spec D2) |
| Release files titled `# X.Y.Z` | Every section reader's predicate (`section_heading_re`, `VERSION_HEADING`, `heading_re`, the hygiene readers) changes with the path, and the migration can no longer be shown lossless by concatenation | Rejected (spec D1) |
| Freeze `CHANGELOG.md` and write only new releases to `changelog/` | Contradicts F2 (*migrated, not frozen*), and every reader reads two layouts for good | Rejected by policy |
| A one-time `--split` flag in `gather_changelog.py` | Mechanism with one act; the fold's `--split` had to be retired by #715 for exactly that | Rejected; a throwaway script and the S1 probe instead |
| Let the old gather write 0.18.1 and migrate after the tag | This branch squashes into `release/v0.18.1` before release preparation, so the preparation would run on a migrated tree; the old gather would insert a full section into the index. Migrating after the tag means a 0.18.2 carrying only this | Rejected (spec D6) |
| The survivor sweep leaves `changelog/` out by path | Equivalent today, because a release file is all released lines. But a release file that lost its heading would be silently out of the sweep, where reading it as a changelog puts its lines back in, which a person sees. And it is a second rule beside the region rule the module already has | Rejected; one predicate reads both shapes as changelogs (spec D5) |
| Read both layouts in the gather and the publisher during a transition | No tag after the migration carries the old layout, and a tag before it runs the script at that tag. A dual reader would be code with no caller | Rejected |
| **One file per release with its `## ` heading; an index with one heading and one link per release; every reader moved by path; the new gather writes 0.18.1** | The three listed under *Technical context* | **Chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.
"Narrow" below means the named modules alone; the full suite, lint and
typecheck are the sealer's (`agents/sealer.md`), and no phase runs them.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 0 | `origin/release/v0.18.1` merged in (a merge, never a rebase) once the wave-1 branches have squashed; the two by-construction greps of `spec.md` §*The readers and writers* re-run on the merged tree, and any reader a sibling added is put in the phase where it belongs (written in `phases/phase-0.md`) | The two greps' output, quoted | |
| 1 | **The migration and the writer.** `changelog/<X.Y.Z>.md` × 44 written by a throwaway script, `CHANGELOG.md` rewritten as the index (spec D2); `gather_changelog.py` writes and checks the new layout (scope 3); `tests/test_the_changelog_is_gathered_at_release.py` moved to the new layout with S4–S8; S2 and the file-exists half of S3 as standing real-tree cases; `tests/conftest.py#gathered_entry` and `tests/test_handoff_outlives_the_merge.py` read the release files (S13); `changelog` classified in `tests/test_the_release_check_watches_what_ships.py` and excluded beside `CHANGELOG.md` in `tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py` (S14) | S1 probe once (§7, deleted, output in `phases/phase-1.md`); narrow: the gather module, `test_release_hygiene.py`, `test_chain_hooks_hardening.py`, `test_handoff_outlives_the_merge.py`, `test_a_record_precedes_the_fixes_it_commissions.py`, `test_the_release_check_watches_what_ships.py`, `test_a_pact_anchor_is_no_coordinate_of_the_signatory.py`; `python3 .github/scripts/gather_changelog.py --check` on the real tree, its count of marked work items equal to the count before the migration; S13's command count before and after | |
| 2 | **The publisher.** `publish_release_note.py` reads `changelog/<version>.md` and links to it (scope 4); `tests/test_a_release_publishes_its_note.py` moved to the new layout (S9); `publish-release.yml`'s header comment reworded | Narrow: that module; one probe (§7) calling `section_body` on `changelog/0.18.0.md` and on `git show <base>:CHANGELOG.md` for 0.18.0, the two bodies equal. Not a real-tree `DRY_RUN=1` of the script: `main` asks `release_exists` before it reads `DRY_RUN`, so against a tag that already has a release it exits 0 having printed no body | |
| 3 | **The shipped survivor sweep.** One changelog-path predicate in `survivor_check.py` (spec D5), the module docstring and `docs/review-chain-spec.md`'s two paragraphs rewritten to name both shapes; S10 cases beside the existing ones, each seen red against the old `path == CHANGELOG` comparison (§15) | Narrow: `test_a_corrected_sentence_survives_elsewhere.py`, `test_every_reader_ends_a_line_where_gfm_does.py`, `test_the_changelog_is_gathered_at_release.py` (its survivor case); the sweep run over this branch's own range, reporting no released sentence from `CHANGELOG.md` or `changelog/` | |
| 4 | **The words.** `skills/update/SKILL.md` step 3 (scope 6); every prose site in `spec.md` §*The readers and writers* (docs, `CONTRIBUTING.md`, `skills/verify/SKILL.md`, the `session_cost.py` printed line with its pin in `tests/test_session_cost.py`, the `settle.py` and `fold_ledger.py` docstrings, the workflow comments, the two `seal/follow-up.md` coordinates); `docs/the-record-layout.md` F2 marked built and its rows rewritten (scope 9); `docs/release-checklist.md` §2's staging line (D9); this work item's `changelog.md` fragment and `seal/ledger/1791076834-the-changelog-is-one-file-per-release.md` | Narrow: `test_session_cost.py` (the pinned line), `test_release_hygiene.py` (the step-2b pin), `test_the_changelog_is_gathered_at_release.py` (the documents cases), `test_the_ledger_rules_have_one_home.py`, `test_one_word_one_meaning.py`, `test_no_document_names_the_old_roots.py`; the two greps of phase 0 re-run, every remaining hit either in a record or justified in `overview.md` | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **No new dependency, environment variable or manifest change.** The install
  path is a copy of the whole tree, so `changelog/` arrives with the release
  (spec §*What an installed plugin needs*).
- **Release preparation, from 0.18.1 on:** the same two commands; the gather
  now creates `changelog/X.Y.Z.md` and edits `CHANGELOG.md`, and both are
  staged before the suite (spec D9).
- **A user updating from 0.18.0 or earlier into 0.18.1** runs their old update
  skill. Step 2b still verifies (the index heads the new version); step 3
  meets the index and has to follow its link to summarise (spec D7). From the
  next update on, the new step 3 runs.
- **Published release notes before 0.18.1** keep their `blob/<tag>/CHANGELOG.md`
  links, which resolve at those tags.
- **Merge order.** #729 (F3) and #730 (F4) also edit
  `docs/the-record-layout.md`; this work edits only the *Every kind of
  record* row, the size bullet, the fragment paragraph, the root-records
  table and the F2 paragraph, so a conflict there is in different
  paragraphs. #741 adds an encoding check over the plugin's file I/O; every
  new `open()` here names `encoding="utf-8"`.
