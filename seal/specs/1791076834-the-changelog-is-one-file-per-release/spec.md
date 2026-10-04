# Feature Specification: the changelog is one file per release (#728)

<!-- seal/specs/1791076834-the-changelog-is-one-file-per-release/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

`CHANGELOG.md` is 8,891 lines at e141980a, with 44 `## X.Y.Z — <date>`
sections (0.0.1 through 0.18.0) and 170 `<!-- specs/<id> -->` marker lines
(read: `wc -l`, `grep -c '^## '`, `grep -c '^<!-- specs/'` on the worktree at
acc3bae6). A reader who wants one release reads or greps all of them. This
work moves each section into `changelog/<X.Y.Z>.md`, keeps `CHANGELOG.md` as
a short index, and moves every reader and writer of the sections with it.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-record-layout.md` §*What is decided and not built yet*, **F2** | The target: `changelog/<X.Y.Z>.md`, every existing section migrated and not frozen, `CHANGELOG.md` kept as a short index linking each one, the GitHub Release reading the release's own file. Migrated rather than frozen because no branch writes the changelog in parallel, and a link at an old tag keeps resolving at that tag. This is a ratified decision, so this frame does not reopen it |
| `docs/the-record-layout.md` §*Every kind of record, at a glance* (row *The changelog*) and §*The size a reader takes whole* | The row and the bullet name `CHANGELOG.md` as over target and F2 as unbuilt. Both are rewritten by this work: the home becomes `changelog/<X.Y.Z>.md`, the index is the file name by version, and the bullet leaves the over-target list |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | Unchanged in substance: a change still writes `seal/specs/<work-item-id>/changelog.md`, and the fragment's no-`## `-line rule stands. Only *concatenated into the released section of `CHANGELOG.md`* becomes *into the release's own file* |
| `docs/the-record-layout.md` §*The root records* | `CHANGELOG.md`'s row changes meaning (an index), and `changelog/<X.Y.Z>.md` gains a row |
| `CONTRIBUTING.md` §*House rules* (*One branch does edit `CHANGELOG.md`, and it is the one based on `main`*) | Read against F2: this feature branch rewrites `CHANGELOG.md` once, by the decision F2 records. The sentence is reworded to the new layout — the release-preparation branch writes the release's file and the index line — and it does not gain an exception for this branch, because after the migration no branch but that one writes either |
| `docs/branch-and-release.md` (the release-sequence bullets and §*The changelog entries arrive as fragments, and the release gathers them*) | The gather writes `changelog/X.Y.Z.md` and the index line; the note publishes from that file |
| `docs/release-checklist.md` §*2. Gather, fold, bump*, §*3. Verify before committing*, and the §5 box *A GitHub Release exists at `vX.Y.Z`* | The commands keep their spelling (`gather_changelog.py --version X.Y.Z`, `--check`); what they write and read moves. The new file must be on disk and staged before the suite runs (see *Data & interfaces*, D9) |
| `docs/review-chain-spec.md` §*The sweep reads only wording that still instructs somebody* and §*Only wording the range itself wrote is subtracted* | The survivor sweep excludes a released changelog section and a gathered fragment. After this work a released section also lives as a whole file under `changelog/`, and the sweep has to read that shape as released on both sides of a range, or the migration range and every later release range report released prose as survivors |
| `skills/update/SKILL.md` step 2b and step 3 | Step 2b verifies an install by `grep -m1 '^## ' "$p/CHANGELOG.md"` naming the version the installer reported. The skill that runs the update INTO 0.18.1 is the one the user's session loaded, so 0.18.0's — and it reads the NEW `CHANGELOG.md`. The index therefore keeps a `## X.Y.Z — <date>` line per release, newest first (D2) |
| `skills/implement/SKILL.md` §1 and the agent contract §12 | Every reader and writer is enumerated by construction, below, rather than from the issue's *about 20 Python files* — an aggregate the issue itself labels approximate |

## Scope

### In

1. **The migration.** Each of the 44 sections of `CHANGELOG.md` at the
   branch's base becomes `changelog/<X.Y.Z>.md`, byte for byte: the file is
   the section from its `## X.Y.Z — <date>` heading up to (not including) the
   blank lines before the next `## ` heading, ending in one newline. Markers
   move with their entries. Nothing in a released section is corrected on
   the way (see *Out*).
2. **The index.** `CHANGELOG.md` becomes `# Changelog`, one paragraph saying
   where the notes are, and per release, newest first, its heading line
   exactly as the release file's first line, a blank line, and one link line
   to the file (D2).
3. **The writer.** `.github/scripts/gather_changelog.py --version X.Y.Z`
   writes `changelog/X.Y.Z.md` (a new file, or entries appended into the
   existing one with its date kept, #289's rule carried over), and inserts
   the index entry at the top of `CHANGELOG.md` when the version has none.
   `--dry-run` writes nothing. `--check` reads the markers of every
   `changelog/*.md` file. Every refusal it has today stays (#586's `## ` line,
   #584's unclosed block, nothing to gather, nothing to check).
4. **The publisher.** `.github/scripts/publish_release_note.py` reads
   `changelog/<version>.md`, fails as today when it has no section for the
   tag, and the note's closing link points at
   `https://github.com/<repo>/blob/<tag>/changelog/<version>.md`.
5. **The shipped survivor sweep.** `skills/code-review/scripts/survivor_check.py`
   reads `changelog/<version>.md` as a changelog on the terms it reads the
   root `CHANGELOG.md` by today: released lines blanked in the pool and the
   range, `newly_released` and the gathered-split rule applied per changelog
   path, and `gathered_fragments` reading the markers of every such path at
   the revision. The root `CHANGELOG.md` keeps its reading unchanged, because
   the script ships to repositories that keep one file (D5).
6. **The update skill.** `skills/update/SKILL.md` step 2b keeps reading
   `CHANGELOG.md`'s first `## ` line (the index keeps it valid); step 3 reads
   the release files under `changelog/` in the marketplace clone for every
   version between the old and the new one.
7. **Every document, docstring and printed sentence that says the released
   entries are in `CHANGELOG.md`.** The enumeration is in *The readers and
   writers, by construction* below; a sentence a person reads is changed with
   the case that pins it (contract §14).
8. **Every test that reads `CHANGELOG.md`'s entry text, or excludes it by
   name**, re-pointed so it reads the same text or excludes the same text
   (D8). Plus the new real-tree cases in *Acceptance*.
9. **`docs/the-record-layout.md` marks F2 built**, the issue's second box.
10. **The two `seal/follow-up.md` rows that cite `CHANGELOG.md` §0.12.2**
    (lines 70 and 72 at acc3bae6): their location is rewritten to
    `changelog/0.12.2.md`. Their decision stays open and stays the owner's.

### Out

| Left out | Why |
|---|---|
| Correcting any released entry while moving it — including the two §0.12.2 sentences `seal/follow-up.md` rows 70 and 72 wait on | Those are the owner's open decision (Q1 of work items 1789996775 and 1789996780), and a migration that also edits text cannot be shown lossless by concatenation. The rows keep their answerer; only their coordinate moves |
| A one-time `--split` flag in `gather_changelog.py` | The fold's `--split` (#547) was mechanism that had to be retired by #715 once its one act was spent. The migration is a one-off write verified by a probe (§7), and the commit is the record (D6) |
| `docs/one-root-by-lifetime.md` and its `.ko.md` edition | `tests/test_release_hygiene.py#RECORDS_OF_A_MOMENT` and `tests/test_no_document_names_the_old_roots.py#DESIGN_RECORD` both name them the 0.4.0 design record. Their `CHANGELOG.md` sentences describe that design and stay true of it |
| Reading both layouts in `gather_changelog.py` and `publish_release_note.py` | Both belong to this repository alone (`broad_gate.py` says so of the gather), and no tag after the migration carries the old layout. A tag before it runs the script at that tag (D6) |
| A refusal to gather into a release file older than the newest | `fold_ledger.py` has one for the ledger because `Ledger frozen from` freezes released ledger files. No policy freezes a released changelog file by a machine rule, and adding one is new mechanism the ticket did not ask for |
| `skills/implement/orchestration.md` §§ about a changelog every branch appends to, `agents/smith.md`'s *let the entry accumulate unreleased* | Repository-agnostic guidance for repositories that install the plugin; it names no file of this one |
| Rewriting published GitHub Release notes for tags before 0.18.1 | `publish_release_note.py` never republishes, on purpose, and their `blob/<tag>/CHANGELOG.md` links resolve at those tags |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 Lossless migration | Given `CHANGELOG.md` at the branch's merge base with `origin/release/v0.18.1`; when the files `changelog/*.md` are read newest first and joined by one blank line under `# Changelog` and a blank line; then the result is byte-identical to that file | A one-off probe (`test_tmp_*`, contract §7), run once against `git show <base>:CHANGELOG.md`, its output quoted in the phase record. Not a standing case: a shallow CI checkout has no base object |
| S2 The index and the files agree | Given the tree; then every `changelog/<v>.md` has exactly one `## ` line, its first line, naming `<v>`; `CHANGELOG.md` has exactly one `## ` line per file, identical to that file's first line, followed by a link to it; no other `## ` line; the order is newest first by version | A standing real-tree case, files enumerated with a glob on disk, not `git ls-files` (D9) |
| S3 The newest index heading is the shipping version | Given `plugin.json` at `X.Y.Z`; then `CHANGELOG.md`'s first `## ` line names `X.Y.Z` and `changelog/X.Y.Z.md` exists | Existing `tests/test_release_hygiene.py` newest-entry case, kept green; plus the file-exists half added |
| S4 A gather writes the release file and the index line | Given fragments and the new layout; when `gather_changelog.py --version 0.2.0 --date D` runs; then `changelog/0.2.0.md` is `## 0.2.0 — D`, a blank line, and each fragment under its marker in id order; and `CHANGELOG.md` gains `## 0.2.0 — D` and the link above every older entry | Fixture cases in `tests/test_the_changelog_is_gathered_at_release.py`, rewritten to the new layout |
| S5 A second gather appends | Given `changelog/0.2.0.md` exists; when a new fragment is gathered for 0.2.0; then it is appended to that file, the date is unchanged, and the index gains no second line | Same module; #289's existing case moved to the file |
| S6 `--dry-run` writes nothing, in either file | When `--dry-run` runs; then neither `CHANGELOG.md` nor anything under `changelog/` changes, and nothing is created | Same module |
| S7 `--check` reads the release files | Given 3 markers spread over two `changelog/*.md`; then `--check` reports all fragments gathered and 3 work items marked; with a fragment whose marker is in no release file it exits 1 naming the fragment; with neither fragment nor marker it exits 1 | Same module; the printed wording pinned (§14) |
| S8 Refusals unchanged | A fragment carrying a `## ` line, or leaving a fence or comment open, is refused before anything is written, in either file | Existing #586 and #584 cases, re-pointed |
| S9 The note reads the release's own file | Given `changelog/0.2.0.md`; when `publish_release_note.py` runs with `TAG=v0.2.0 DRY_RUN=1`; then the folded section is that file's body and the closing link is `…/blob/v0.2.0/changelog/0.2.0.md`; given no such file, it exits 1 and the message names `changelog/0.2.0.md` and the gather command | `tests/test_a_release_publishes_its_note.py`, re-pointed |
| S10 The sweep reads a release file as released | Given a range that adds or edits `changelog/0.2.0.md` and a range whose base has the one-file `CHANGELOG.md` and whose tip has the migrated layout; then no sentence of a released section is reported removed or as a survivor, and a fragment whose marker stands in a release file at the tip is out of the pool and the range | New cases in `tests/test_a_corrected_sentence_survives_elsewhere.py` beside the existing `CHANGELOG.md` cases, each seen red against the old predicate (§15) |
| S11 The root-file reading is untouched | Every existing `CHANGELOG.md` case in `tests/test_a_corrected_sentence_survives_elsewhere.py` and `tests/test_every_reader_ends_a_line_where_gfm_does.py` stays green with its fixture unchanged | Those modules |
| S12 An update into this release still verifies | Given an installed copy of the new release; when 0.18.0's step 2b runs `grep -m1 '^## ' "$p/CHANGELOG.md"`; then it prints the new version's heading | S2/S3 cover it in the tree; the step-2b pin in `tests/test_release_hygiene.py` stays green |
| S13 A test that read entry text still reads it | `tests/test_handoff_outlives_the_merge.py` finds the `git mv` commands it found before (they are in the 0.4.0 section), and `tests/conftest.py#gathered_entry` returns the same text for a retired item's marker | Those modules; for the first, a count of commands examined before and after, quoted in the phase record |
| S14 Nothing new escapes the shipping check | `changelog` is classified in `tests/test_the_release_check_watches_what_ships.py` as staying home | That module |

## Data & interfaces

**D1. A release file is the section, heading included.** `changelog/0.18.0.md`
begins `## 0.18.0 — 2026-10-03`. Chosen over a `# 0.18.0` title because every
section reader already in the tree finds a section by that line —
`publish_release_note.py#section_heading_re`, `survivor_check.py#VERSION_HEADING`,
`gather_changelog.py#heading_re`, `tests/test_release_hygiene.py`'s
duplicated-heading reader — so the readers move by path and keep their
predicate, and the migration is provable by concatenation (S1).

**D2. The index keeps one heading per release.** Shape:

```
# Changelog

<one paragraph: each release's notes are in changelog/<X.Y.Z>.md, newest first>

## 0.18.0 — 2026-10-03

[changelog/0.18.0.md](changelog/0.18.0.md)

## 0.17.0 — 2026-10-03
…
```

About 180 lines. Chosen over a bullet list of links because the update skill
that runs the update into this release is 0.18.0's, already installed in the
user's session, and its step 2b stops the update and prints a repair that
moves the install directory unless `CHANGELOG.md`'s first `## ` line names
the new version. A list with no heading would send every updating user down
that path. It also keeps `tests/test_release_hygiene.py`'s newest-heading,
duplicated-heading and `## Unreleased` cases meaningful without a rewrite.
The cost, stated: the heading line exists twice, in the index and in the
release file, and S2 is the case that holds them identical. Recorded in
`questions.md` as decided by the framer.

**D3. The gather's interface does not change.** Same flags, same exit codes,
same refusals. Its printed lines name `changelog/X.Y.Z.md` where they named
`CHANGELOG.md`. Functions other documents cite by name keep their names:
`marker`, `section`, `live_markers`, `section_heading`, `load_reader`,
`insert`, `fragments` (cited from `docs/`, `skills/` and other scripts —
`git grep -o 'gather_changelog\.py#[a-z_]*'`). A rename updates every
citation in the same commit.

**D4. The publisher reads `changelog/<version>.md` through `section_body`.**
The function and its name stay (`publish_release_note.py#section_body` is
cited five times). Applied to a release file it returns the body under the
heading, as it does today.

**D5. Which paths the survivor sweep reads as a changelog.** The root
`CHANGELOG.md`, as now, and `changelog/<name>.md` at the repository root
where `<name>` is version-shaped (the `VERSION_HEADING` shape). One predicate,
used everywhere the script compares `path == CHANGELOG` today: `sentences`,
`gathered_fragments`, `corrected`'s `newly_released` arm, and `score`'s split
arm (`survivor_check.py` lines 836, 919, 1345 and 1582 at acc3bae6). The
module's own docstring paragraph *A released changelog section, and a
gathered fragment* and `docs/review-chain-spec.md`'s two paragraphs are
rewritten to name both shapes. `CHANGELOG = "CHANGELOG.md"` stays, because a
test monkeypatches it.

**D6. The transition: 0.18.1 is gathered by the NEW tooling.** This branch
squashes into `release/v0.18.1` after the wave-1 branches and before release
preparation, so the preparation commit runs the new `gather_changelog.py`
from the release branch's tip. The old one cannot run on the migrated tree
correctly — it would insert the whole 0.18.1 section into the index above
its first `## ` line, which half-reverts the layout. And
`publish-release.yml` runs the script at the tagged commit, so the 0.18.1 tag
runs the new publisher against the file the new gather wrote. Every release
from 0.18.1 on is in the new layout and every release before it is migrated,
so no script has to read both. The two readers that do meet both — the
survivor sweep over a range spanning the migration commit, and the update
skill of 0.18.0 reading 0.18.1's index — are handled by D5 and D2. The
migration itself is done once, by a throwaway script whose output S1 checks;
the commit that writes it is the record.

**D7. The one-time cost of D6, stated.** 0.18.0's update skill, step 3,
summarises *`CHANGELOG.md`* from the marketplace clone. On the update into
0.18.1 it meets the index, whose paragraph names `changelog/<X.Y.Z>.md`; a
session that does not follow the link summarises less than before. From the
update after that on, the new step 3 runs. Not mitigated further: duplicating
the newest release's text into the index would give one record two homes.

**D8. Tests that read `CHANGELOG.md` by name — the class, enumerated.**
`git grep -l CHANGELOG -- tests` at acc3bae6 gives 17 files. Sorted by what
the name does there:

| Kind | Files | What changes |
|---|---|---|
| Reads entry text, which moves | `conftest.py#gathered_entry`; `test_handoff_outlives_the_merge.py` (the `git mv` scan); `test_the_changelog_is_gathered_at_release.py` (its real-tree cases and fixtures) | Read the `changelog/*.md` files instead |
| Reads the headings, which the index keeps | `test_release_hygiene.py` (`shipped_versions`, newest entry, duplicated heading, `## Unreleased`); `test_chain_hooks_hardening.py#test_plugin_version_is_in_changelog` | Stays on `CHANGELOG.md`; S2 adds the per-file half |
| Excludes it by name | `test_a_pact_anchor_is_no_coordinate_of_the_signatory.py` (line 158, the tree-drawing grep); `test_the_release_check_watches_what_ships.py#STAYS_HOME` | Excludes or classifies `changelog/` as well — the moved text carries the same drawings |
| Pins a printed sentence that names it | `test_session_cost.py` (line 3184); the gather's `N work items marked in CHANGELOG.md` assertions | Move with the sentence (§14) |
| Builds a one-file fixture for a shipped reader | `test_a_corrected_sentence_survives_elsewhere.py`, `test_every_reader_ends_a_line_where_gfm_does.py`, `test_a_release_publishes_its_note.py` | Survivor fixtures stay (S11) with new cases beside them; the publisher's fixture moves to the new layout |
| Names it in a comment only | `test_a_record_precedes_the_fixes_it_commissions.py` (its message reads through `gathered_entry`), `test_a_segments_record_says_what_it_was_asked.py`, `test_one_word_one_meaning.py`, `test_no_document_names_the_old_roots.py` (a `KEEP` reason), `test_the_root_migrates_itself.py` (a docstring) | Reword where the sentence becomes false; no behaviour |
| Quotes the record layout's *Instead of* row | `test_the_ledger_rules_have_one_home.py` (line 66, *an entry under `CHANGELOG.md`'s `## Unreleased`*) | Stays: the row says what a change does instead of the old append, which is still true |

**D9. The new release file must be visible to the suite before it is
staged.** `docs/release-checklist.md` §3 already warns that the suite reads
`git ls-files` and that a fold leaves unstaged deletions. A gather now
creates an untracked file. The standing cases in S2 enumerate with a glob on
disk, and the checklist's §2 says to `git add changelog/ CHANGELOG.md` with
the fold's paths before §3.

**D10. Every new file read or write names `encoding="utf-8"`.** #741, a
sibling in this milestone, adds a check over the plugin's file I/O.

## The readers and writers, by construction

Enumerated with `git grep -n CHANGELOG` and `git grep -n -i changelog` over
the tree less the records (`seal/specs`, `seal/releases`, `seal/ledger.md`,
`CHANGELOG.md`), and with `git grep` for every importer of a section or
marker reader (`section_body`, `live_markers`, `gathered_fragments`,
`gathered_entry`) — the namesakes in `round_record.py`, `chain_check.py`,
`fold_ledger.py#live_markers` and three tests read other files and are not
in the class. Read on acc3bae6; the smith repeats both greps after merging
`origin/release/v0.18.1` (*plan.md*, phase 0).

| Where | Kind | Changes in this work |
|---|---|---|
| `.github/scripts/gather_changelog.py` | writer, marker reader | yes — scope 3 |
| `.github/scripts/publish_release_note.py` | section reader, link | yes — scope 4 |
| `.github/workflows/hygiene.yml` (the `every changelog fragment reached the released file` step and its comment) | runs `--check` | comment only; the step name stays, because `skills/verify/scripts/broad_gate.py#ONLY_AT_MAIN` and `tests/test_the_gate_names_every_step_ci_runs.py` hold it by name |
| `.github/workflows/publish-release.yml` (header comment) | prose | reworded |
| `.github/scripts/fold_ledger.py` (docstring lines 55, 67–68, 128–129) | prose | reworded; no code reads `CHANGELOG.md` there |
| `skills/code-review/scripts/survivor_check.py` | shipped reader | yes — scope 5 |
| `skills/update/SKILL.md` steps 2b and 3 | shipped reader | step 3 rewritten; 2b kept (D2) |
| `skills/verify/SKILL.md` (lines 808, 828) and `skills/verify/scripts/session_cost.py` (line 2755, a printed line) | prose naming where #377 and #642 are listed | reworded to name the release's file under `changelog/`; the printed line's pin moves with it |
| `skills/verify/scripts/unverified_check.py` (lines 86, 173, 289–290) | prose citing gather functions | unchanged while the functions keep their names (D3) |
| `skills/settle/scripts/settle.py` (docstring line 29) | prose, a measurement | reworded to *the changelog* — the measurement was of markers, which moved |
| `docs/the-record-layout.md` | policy | scope 9 and the grounding rows |
| `docs/branch-and-release.md` (lines 58, 225–241) | policy | reworded |
| `docs/release-checklist.md` (§2, §3 line 168, §5 box line 310) | procedure | reworded; D9's staging line |
| `docs/review-chain-spec.md` (lines 937–938, 976) | policy | reworded (D5) |
| `docs/issues-and-milestones.md` (line 50: *`CHANGELOG.md` turns either description back into a number in one grep*) | policy | reworded to `changelog/`; line 401 (*release dates*) stays true of the index |
| `CONTRIBUTING.md` (line 246) | procedure | reworded (grounding row) |
| `seal/follow-up.md` rows at lines 70 and 72 | records with an answerer | coordinate only (scope 10) |
| `hooks/`, `bin/`, `install.sh`, `.claude-plugin/`, `README*.md` | — | no reader: `git grep -i changelog` finds only README prose about *changelog entries*, which stays true |
| the 17 test files | D8 | D8 |

**What an installed plugin needs.** The install path is a copy of the whole
repository tree at the release — `~/.claude/plugins/cache/specseal/specseal/0.18.0/`
and the marketplace clone both list `CHANGELOG.md`, `seal/`, `tests/` and
every other top-level entry (read: `ls` of both, 2026-10-04). So
`changelog/` arrives in both with no manifest change, and `plugin.json`
names no file list to extend.

## Open questions → questions.md

Nothing here blocks the build. D1, D2, D5 and D6 are listed there as
answered from the tree; Q1–Q4 (the index entry's content, D7's one-update
cost, no freeze rule for a released file, the follow-up rows' coordinate) are
decided by the framer with their defaults in force; Q5–Q6 are measurements
and Q7–Q8 the work's.

Framed 2026-10-04 by framer, before the build.
