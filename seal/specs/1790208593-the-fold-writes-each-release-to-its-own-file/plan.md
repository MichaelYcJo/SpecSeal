# Implementation Plan: the fold writes each release to its own file

<!-- seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-24 by the orchestrating session on the owner's `automation` answer, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

Five phases, in the order the risk is retired. Phase 1 widens every reader
by one glob, each with a fixture case red first — the half the ticket calls
*the reading half*, and the half that decides the milestone question: it is a
glob, not an anchor rule. Phase 2 moves the fold's target to
`seal/releases/<X.Y.Z>.md`, joining through C's helpers, and gives `--check`
its two new arms; the fixture case that reports equal checker totals across a
fold is what ties the two phases together. Phase 3 is `--split`, with its
anchor rewrite and a rehearsal over a copy of this repository's ledger.
Phase 4 is the documents and the ledger's header. Phase 5 verifies: the
fragment rows, the changelog entry with the corrected claim, the memo, the
sweep. **The split of the real tree is not a phase**: it runs at the
release-preparation commit, and `docs/release-checklist.md` §2 says so.

## Technical context

**The base this builds on.** This branch is cut from `release/v0.15.1` at
`9f846733` and is built on top of C's branch
(`fix/540-a-second-fold-writes-a-second-heading`, read at `171feacf` in
`wt-540`). What phase 2 reuses from C, by name: `section_heading` (the one
predicate for *is there a section*, now asked of the release file's text),
`insert` (the join — over a release file its walk to the next `## ` reaches
EOF, which is the arm the file's shape always takes), `doubled_versions`
(the reader `--split`'s refusal and the per-file `--check` arm use), and
`main`'s `found`/`heading` lines (the date a joined file keeps, the heading
a dry run prints). **If C's helpers are not in this tree when phase 2
opens, the branch merges `release/v0.15.1` in first** — C squashes there —
and phase 3's rehearsal needs C's `0.9.3` repair (`d08c671a`) in the copied
ledger, or `--split` refuses it and the case reports C's refusal.

**C's cases D keeps green, re-pointed to the release file** (their names,
so the reviewer can open them):
`test_a_second_fold_for_the_same_version_joins_its_section`,
`test_the_kept_date_wins_over_today_as_well`,
`test_a_dry_run_of_a_second_fold_shows_the_section_it_appends_into`,
`test_check_refuses_a_ledger_that_heads_a_version_twice` (its second half:
a release file headed twice), `test_a_fragment_whose_marker_is_already_in_the_ledger_is_refused`,
`test_check_passes_once_folded_and_says_what_it_counted`,
`test_no_version_heads_two_sections_of_this_ledger` (widened to both
shapes). **One C case is retired**:
`test_the_joined_section_is_one_section_wherever_it_stands` — its premise, an
area heading appended after the version section, cannot occur in a release
file, and `--check`'s per-file arm refuses a second `## ` version heading;
the phase record says so.

**`.github/scripts/fold_ledger.py`** (read whole at `9f846733`, and C's
diff): `section()` builds `## X.Y.Z — <date>` and the marked `### <id>`
blocks; `demote` moves fragment headings down two; `folded()` asks
`is_marked` over one text; `main` reads `LEDGER`, refuses a missing one,
runs the open-row guard before anything is written, removes fragments only
after the write, and `rmdir`s `FRAGMENTS`. Every printed path goes through
the `/`-joined constants (round 1's Windows finding of `1788326734`), and
`RELEASES` joins them.

**`skills/evidence-check/scripts/evidence_check.py#default_patterns`** is
the one list; `main` resolves it through `resolve_patterns` (inode-folded),
`reverify` and `migrate` take the same `ledgers`, `skipped_by_narrowing`
subtracts what was read from it, and `settle.py#anchored_rows` loads the
checker and calls it. So one line reaches five readers, and
`test_the_defaults_render_the_names_they_have_always_rendered` pins the line.
`unshipped` lists `<home>/ledger/` and skips a non-`.md` name; `tree_names`
excludes `<home>/specs/` and `<home>/ledger/` — a sibling directory is walked
and its rows stay in the name corpus, which is the semantics the docstring
argues for `seal/ledger.md`.

**`hooks/evidence-advisor.py#failing_rows`** and
**`hooks/ledger-migrate.py#HOME_GLOBS`** spell the list again (the advisor's
docstring says why `home` and `root` differ); each is one entry.

**`correction_check.py#ledger_listing`** runs `git ls-tree -r --name-only
<rev> -- LEDGER FRAGMENTS`; the release directory is a third argument.
`read_blobs` reads every listed path at four revs per merge, so the byte
total per merge does not change with the split (the same rows, in more
blobs) — the ticket's cost argument is not made for this reader and this
plan does not make it. The survival test identifies a row within one path;
a row that moved path at a merge is silent, and the docstring says so.

**`skills/settle/scripts/settle.py#coordinates`** attributes rows to a work
item by the marker line and resets on `## `; the same loop over each release
file attributes its rows the same way, because the file starts with one
`## ` and then the markers.

**`seal/ledger.md`** at `9f846733`: lines 1–20 the header, 21–102 the eight
standing areas, 103–2736 the release sections. Line 2521 (§0.13.1) is the
one row anchored into the file itself (two anchors, into §0.4.0 and
§0.5.0). The split's rewrite is a substitution over `seal/ledger.md#"…"`
coordinates whose first heading part is a `### ` or `#### ` line the split
moved; the hash stays, because the anchored region is byte-identical in the
new file.

**Tests reading the real tree by structure**, each of which must be green
on both shapes (a ledger still holding sections, and one split):
`test_no_version_heads_two_sections_of_this_ledger`,
`test_this_repository_has_one_root_laid_out_by_lifetime`,
`test_the_three_named_markers_are_live_in_this_repositorys_ledger`,
`test_this_work_item_wrote_its_own_fragment`, the five-copies case in
`test_a_record_precedes_the_fixes_it_commissions.py`, the real-tree glob in
`test_a_row_points_by_content.py`, `ledger_corpus` and the census case in
`test_a_merge_cannot_silently_drop_a_correction.py`. Each reads a folded
section from `seal/ledger.md` or from any release file after this work.

**The rows this work drifts** (spec §*The measured state*): re-read, given a
dated note and re-stamped with `evidence-check --reverify .` in
`seal/ledger.md`; none removed, none re-pointed. C re-stamped four of the
same rows at `deade859`, so D's merge of the release branch will meet them
as hunks; both sides' notes are kept, hunk by hunk.

**What breaks in six months.** Three readers spell the ledger's addresses
outside `default_patterns` (`evidence-advisor.py`, `ledger-migrate.py`,
`correction_check.py`), and a fourth address would have to reach all four.
That is the cost accepted rather than a shared constants module under
`hooks/` that the vendored checker cannot import (`seal_home`'s docstring
says why the copies diverge). The other failure is a release file written
by hand to `seal/ledger.md` out of habit, which `--check` refuses at the
release pull request naming `--split`, and which the hygiene case refuses
on every pull request once the real split has run.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Split the real tree in this branch** (the 37 sections move in a phase) | Every parallel branch of the milestone re-stamps rows of `seal/ledger.md`; at D's merge git sees D's deletions against their modifications, one conflict per re-stamped row; the survivor sweep reports the moved rows in the thousands and needs a whole-range `survivors.md` row; a sibling landing after the split repeats both | rejected — the split runs at the release-preparation commit, where none of that exists and a `--dry-run` is already read |
| **`seal/ledger/released/<X.Y.Z>.md`**, the ticket's first spelling | `tree_names` excludes `<home>/ledger/`, so released rows leave the name corpus; the layout case refuses a non-fragment under `seal/ledger/`; `main` cannot `rmdir` the fragments directory; a permanent file under a between-releases directory is the lifetime mixing `docs/one-root-by-lifetime.md` names as the defect | rejected — `seal/releases/` |
| **Flat files beside the ledger**, `seal/ledger-<X.Y.Z>.md` | The root listing gains one file per release forever, beside the six files a first-time reader is meant to see | rejected |
| **A `#` title and re-based heading levels in the release file** | `settle.py#coordinates` resets on every `## `, so `## <id>` after a marker attributes rows to nobody; C's helpers and every marker reader assume the section's shape | rejected — the file is the section byte for byte |
| **`--split` joins an existing target** | A target present before the first split is a tree in a state nobody planned; joining hides it | rejected — refuse, name it |
| **Re-point the self-anchored row by hand** | A person has to find it; the dependency rule says nothing may need finding when something moves; `root-migrate.py` rewrites prefixes for exactly this class | rejected — the split rewrites it, and the rehearsal asserts it |
| **`--check` refuses only a doubled heading in `seal/ledger.md`** (C's arm as it is) | A fold written to the old place, or a split not run, is a single heading and passes | rejected — any release heading there is refused, naming `--split` |
| **Collapse the narrowing notice to a count for the release directory** | `test_every_skipped_ledger_is_named_not_counted` and the checker's own rule: a skipped ledger is named | rejected; Q5 measures the length |
| **An overlay fragment for a branch's re-verifications** — the change that removes the measured conflict class | Changes where a hash is read from: the checker's baseline rule, a gate change with the four answers, and the design the ticket sends to 0.16.0 | not here — Q1, the owner |
| **A shared `.github/scripts/_ledger.py`** for the three helpers and the constants | The vendored checker and the hooks cannot import it; C rejected the same for the same reason | rejected |
| **Delete `--split` after the release runs it** | One-shot writers stay (`evidence-check --migrate`), and the `--check` refusal names it as the repair | kept |

## Phases

Vertical slices — each phase ends with something runnable and verified. The
row is the whole task; there is no prompt per phase (`agents/framer.md`).
Each phase closes with `phases/phase-N.md` from `templates/sdd-phase.md`,
the ledger rows drafted during the phase written in one pass, a commit, and
`python3 skills/evidence-check/scripts/evidence_check.py --strict .` read
directly (§1).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The readers widen.** `evidence_check.py#default_patterns` gains `<home>/releases/*.md` and its docstring the third location; `hooks/evidence-advisor.py#failing_rows`, `hooks/ledger-migrate.py#HOME_GLOBS`, `correction_check.py` (`RELEASES`, `ledger_listing`, the docstring's *What it reads* and the cross-path limit), `settle.py#coordinates`; `skills/evidence-check/SKILL.md`'s `--ledger` row and `skills/settle/SKILL.md` §4 name it. Cases S1–S4, each seen red on a fixture row in `seal/releases/0.4.0.md` that was unread; `test_the_defaults_render_the_names_they_have_always_rendered` re-pointed; `ledger_corpus` gains `cc.RELEASES`. Rows R1–R4 drafted; the `default_patterns` rows re-read | `bin/test tests/test_evidence_check.py tests/test_the_printed_ledger_name_is_the_file_that_was_read.py tests/test_a_narrowed_ledger_read_says_what_it_skipped.py tests/test_local_mode_resolves_under_the_git_dir.py tests/test_the_ledger_migrates_itself.py tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_settle_reads_before_it_removes.py tests/test_a_record_states_what_the_tree_has.py -q`, exit read directly; `uvx ruff check` and `uvx ruff format --check` over the edited scripts | |
| 2 | **The fold writes the release file.** `RELEASES`, `release_path`, `release_files`; `folded` over every release file; `main --version` writing or joining the file through C's `insert`, never `seal/ledger.md`; `--check`'s two new arms and the cross-file count line; the module docstring. Cases S5–S10 in the fold module, `fold()`/`released()` re-pointed, C's cases kept green as §Technical context lists, C's S4 case retired with the reason in the phase record; S6 is the case that proves phase 1 against the fold. Rows F1, F2 drafted; the §0.4.0/§0.5.0 `fold_ledger.py` rows re-read | `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_the_changelog_is_gathered_at_release.py -q`; ruff over the script and the module; `fold_ledger.py --dry-run --version 0.15.1` over this tree prints a fresh file's block (no `seal/releases/` exists yet) | | (NAME NOT IN TREE until the phase adds it)
| 3 | **The split.** `--split` and `--dry-run`: the cut, the remainder, the anchor rewrite, the three refusals; cases S11–S13 red first; the rehearsal S14 over a `tmp_path` copy of this repository's `seal/ledger.md` — 37 files, rows in exactly one file each, `check_ledger` findings equal in process, the line-2521 anchors rewritten and OK; S15's two real-tree pins widened and seen red on a planted file. Rows P1, P2, L1 drafted | `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_release_hygiene.py -q`; `fold_ledger.py --split --dry-run` over this tree, read and quoted in the phase record (executed, nothing written) | |
| 4 | **The documents and the header.** S16's list and S17's header paragraph; the paperwork-location sentence in its four carriers; `docs/release-checklist.md` §2's once-only `--split` line and C's sentence reworded; both READMEs. Row D1 drafted; rows anchored on edited document units re-read | `bin/test tests/test_docs_line_wrap.py tests/test_no_document_names_the_old_roots.py tests/test_the_contributor_has_a_procedure.py tests/test_the_ledger_fragments_fold_at_release.py tests/test_settle_reads_before_it_removes.py tests/test_a_segment_feeds_the_flow_log.py tests/test_release_hygiene.py -q`; `git diff --stat` shows `README.md` and `README.ko.md` together | |
| 5 | **Verify.** The fragment `seal/ledger/1790208593-….md` written in one pass from the drafted rows; `changelog.md` with the corrected claim; `overview.md` opened with the divergences met and `## Not verified` naming the sealer for the broad gate and the release session for the real split; `survivor-check --range origin/release/v0.15.1...HEAD` with a `survivors.md` row for anything reported (Q4); the narrowing notice measured (Q5); `evidence-check --strict .` exit 0; `git diff --stat` against the base read against S18's list | executed, each exit read directly; the hand-back carries the module runs, the red-first evidence per case, and the suite labelled `unverified — the sealer` | |

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

- **The release that ships this work runs one more command, once, before
  the fold**: `python3 .github/scripts/fold_ledger.py --split` (its
  `--dry-run` read first), and `seal/releases/` appears with 37 files. The
  release pull request's `fold_ledger.py --check` refuses a `seal/ledger.md`
  that still heads a release, naming the command, so a release that forgets
  it goes red with the repair on screen. `docs/release-checklist.md` §2 and
  §3 say so.
- **After the split, a re-stamp touches the release file whose row
  drifted**, and `seal/ledger.md` changes only for the standing rows. The
  same-row conflict measured at `0be23b80` is not removed: two branches that
  re-hash one row still conflict, in a 9–308-line file.
- **The widened default reaches every user of the plugin** at their next
  update: a repository with no `seal/releases/` reads exactly what it read
  before, and the vendored checker (`evidence-ci`) reads the new glob when
  it is next vendored.
- **This branch merges `release/v0.15.1` in with `seal/ledger.md` conflicts
  of the ordinary kind** — its own re-stamps of the `fold_ledger.py` rows
  against C's — resolved hunk by hunk with both sides' notes and checked by
  `correction-check` over the range. It carries no move of the real tree,
  so it is not ordered against its siblings.
- No migration hook, no new dependency, no new environment variable, no
  change to any workflow file. Python floor stays 3.12.
