# Feature Specification: the fold writes each release to its own file

<!-- seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#547 asks for one change of shape: `seal/ledger.md` stops taking a release's
rows, and `.github/scripts/fold_ledger.py` writes each release's rows to a
file of its own. Every reader of the ledger widens by one glob, the 37
release sections the file holds today move once, and `seal/ledger.md` keeps
what is nobody's release — its header, the coordinate notation and the eight
standing areas from before the fragments existed.

**The checker's anchor rules do not change; its glob does.** A ledger row is
a content anchor, so a row moved between files is checked exactly as before
(`docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no
commit*). Measured on the fixture pattern the fold already carries: the same
totals before and after a move. One row in the tree anchors INTO
`seal/ledger.md` itself, and the split rewrites that row's path the way the
root move rewrote every `.specseal/` prefix (`hooks/root-migrate.py`, step 6
of its docstring). So this item stays in `release: 0.15.1`, as the milestone
rule says it does when only the glob widens.

**The ticket's benefit claim is corrected here, before anything is built.**
The ticket says this shape *removes the conflict class rather than a hunk of
it*. Executed at the frame: the merge the ticket cites, `0be23b80`, re-derived
with `git merge-tree --write-tree` over its two parents (`154287fc`,
`3dd24073`) — seven conflict blocks in `seal/ledger.md`, and in **all seven**
the two sides had edited the **same rows** (matched on the rows' first cells:
1, 3, 2, 2, 3, 5 and 1 shared rows). Three branches ran `--reverify` over
units they had each changed, and `--reverify` re-stamps every row citing a
drifted unit (`seal/follow-up.md`, the row on the drift report naming a
coordinate once). A row that moves to `seal/releases/0.12.2.md` is still one
row that two branches re-hash differently, so the seven hunks would have
conflicted in four smaller files instead of one large one. What the split does
buy is stated in *Scope* and in the changelog entry, and nothing else is
promised. What would remove the class — a branch recording its
re-verifications somewhere other than the shared row — changes where a hash
is read from, which is the checker's baseline rule and the 0.16.0 design the
ticket reserves (`questions.md` Q1).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit*: *the checker reads `seal/ledger.md` and the `seal/ledger/*.md` glob alike, and a row is a content anchor, so the release that folds a fragment into the shared file changes nothing either one measures* | The whole reason the move is a glob change: a row is checked wherever it sits. The clause gains the third address |
| `docs/one-root-by-lifetime.md` §*The problem, as measured*: *Things with different lifetimes share a folder, and things with the same lifetime are split across two* — and §*The proposed tree*: `ledger/<id>.md` is *folded into ledger.md at release, then removed*; `ledger.md` is *Permanent* | Decides the directory. A release's rows are permanent; a fragment lives between releases. So the release files do not go under `seal/ledger/`, and `tests/test_release_hygiene.py#test_this_repository_has_one_root_laid_out_by_lifetime` — which refuses a non-fragment under `seal/ledger/` — keeps pinning that |
| `docs/one-root-by-lifetime.md` §*The dependency rule*: *nothing may need to be found and updated when something else moves* | The split rewrites the one anchor that names `seal/ledger.md` as a path, in the same act, rather than leaving a person to find it; and the checker keys on content, so no other row needs finding |
| `docs/branch-and-release.md` §*The ledger fragments fold in the same commit* and `docs/release-checklist.md` §2 *Gather, fold, bump* | Where the fold runs, and where the one-time split runs: the release-preparation commit, whose `--dry-run` a person reads first. The two paragraphs gain the new place |
| `docs/release-checklist.md` §2, the paragraph C (#540) added: *a second `fold_ledger.py --version X.Y.Z` joins the section `seal/ledger.md` already heads and keeps its date* | The join moves with the section: a second fold joins the release FILE and keeps its date. C's helpers `section_heading` and `insert` do that unchanged over the file's text, because the file IS the section |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* and `CONTRIBUTING.md` §*House rules*, the same paragraphs | Where a row goes (unchanged: the fragment), where a removal goes (the file the row stands in — now one of three places), and the conflict-resolution rule (*hunk by hunk, read both sides*), which after this work applies to every ledger file. Both name the new place |
| `CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not re-pointed* | Bounds the anchor rewrite: the split rewrites a path whose content moved WITH the file, byte for byte, hash unchanged — the class `hooks/root-migrate.py` step 6 already handles — and never an anchor whose content went |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides where the one-time split runs. In this branch it is a 2,600-line move that every parallel branch of the milestone conflicts with at D's merge and that the survivor sweep reports in the thousands; at the release-preparation commit it meets no parallel branch, no sweep (the sweep skips a pull request into `main`) and one `--dry-run` a person already reads |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `fold_ledger.py --check`, `evidence_check.py`, `correction_check.py` and `settle` are gates or gate readers. Each change carries the four answers: seen red, blocks more, prompt budget zero, no platform behind a glob |
| `skills/agent-contract/SKILL.md` §12 (*enumerate the class*), §14 (*documents it and pins it*), §15 (*seen red*) | The class is *every reader that names a ledger address*, enumerated below by grep over the tree rather than from the ticket; every message a person reads is pinned; every case is red first |
| `skills/settle/SKILL.md` §4: *Every ledger `evidence-check` reads is read — `seal/ledger.md`, every `seal/ledger/*.md` and any `docs/**/_evidence.md`* | `settle` reads the checker's own `default_patterns` for the anchored-row guard (automatic) and its own loop for `coordinates` (an edit). The sentence gains the third address |

## Scope

### In

| What | Where it goes |
|---|---|
| Every reader of the ledger reads `seal/releases/*.md` beside `seal/ledger.md` and `seal/ledger/*.md`: `evidence_check.py#default_patterns` (the checker, `--reverify`, `--migrate`, the narrowing notice and `settle`'s anchored-row guard all follow it), `hooks/evidence-advisor.py#failing_rows`, `hooks/ledger-migrate.py#HOME_GLOBS`, `skills/evidence-check/scripts/correction_check.py#ledger_listing` (and the constants it reads), `skills/settle/scripts/settle.py#coordinates` | Phase 1 |
| The fold writes `seal/releases/<X.Y.Z>.md` — a new file holding `section()`'s block, or the existing file joined through C's `insert` — and refuses a fragment whose marker stands in ANY release file; `--check` counts markers across every file, refuses a `seal/ledger.md` that still heads a release (naming `--split`), and refuses a release file that is not named for the one version it heads once | Phase 2 |
| `fold_ledger.py --split`: moves every `## X.Y.Z — <date>` section of `seal/ledger.md` into `seal/releases/<X.Y.Z>.md` byte for byte, rewrites every `seal/ledger.md#"<heading>"` anchor whose heading moved, refuses a target that exists and a version headed twice, prints a `--dry-run`; a real-tree rehearsal case over a copy of this repository's ledger | Phase 3 |
| The documents that name the address, and the ledger's own header | Phase 4 |
| The fragment rows, the changelog entry stating what the split buys and does not, the memo, the sweep | Phase 5 |
| **The split of this repository's 37 sections runs at the release-preparation commit of the release that ships this work** (`docs/release-checklist.md` §2 gains the line), not in this branch. The rehearsal case proves it on a copy; the release's `--dry-run` is the read before the write | the release step, by the session running the release tail |

What the split buys, measured, and all of what it buys:

- `seal/ledger.md` goes from 2,736 lines and 1.36 MB to about 100 lines
  (the eight standing areas are 82 lines under a 20-line header; `awk` over
  the `## ` headings at `9f846733`), and stops growing: a release adds a file.
- A re-stamp's diff and a conflict's hunks land in files of 9–308 lines
  (the section sizes at `9f846733`), where a person resolving a hunk reads
  the release the row belongs to and nothing else.
- A release-preparation commit creates a file instead of appending to the
  largest record in the tree, and a second fold for one version joins that
  file.

### Out

| Left out | Why, and who answers |
|---|---|
| Anything that changes where a hash or a re-verification is READ from — an overlay fragment for re-reads, a merge driver, `--reverify` narrowing to the rows a person opened | The checker's baseline rules; the ticket sends that to 0.16.0 with #159 and #526. `questions.md` Q1 puts the corrected claim in front of the owner without blocking this build |
| `seal/ledger/released/<X.Y.Z>.md`, the ticket's first spelling | Rejected on the lifetime rule and three readers: `evidence_check.py#tree_names` excludes `<home>/ledger/` from the name corpus (so released rows would leave it, and the docstring's argument for keeping `seal/ledger.md` IN would go false); `test_this_repository_has_one_root_laid_out_by_lifetime` refuses a non-fragment under `seal/ledger/`; `fold_ledger.py#main` removes `seal/ledger/` when empty. A sibling keeps all three as they are. `plan.md` §Alternatives |
| Re-basing heading levels in the release file (`# X.Y.Z` as a title, `## <id>` per work item) | `settle.py#coordinates` resets its section on every `## ` line, so a `## <id>` after the marker would attribute the rows to nobody; the release file is the section byte for byte, and every reader C wrote (`section_heading`, `insert`, `doubled_versions`) works over it unchanged |
| `hooks/root-migrate.py#LEDGER_GLOBS` | It moves a 0.3.x layout once and stamps; a tree with that layout has no release file. Left as it is, said here so nobody reads it as forgotten |
| `templates/ledger.md`, `templates/seal-README.md`, `skills/evidence-ci/SKILL.md` | The plugin ships no fold: a user repository's fragments have nowhere to fold to, and the templates describe the fragment rule, which is unchanged. The checker's widened default is documented in `skills/evidence-check/SKILL.md`, which ships |
| `docs/one-root-by-lifetime.md` and its Korean edition | A dated record, which `settle` extends with a dated section at the fold of this spec; a work item does not rewrite it |
| `correction_check.py` identifying a row across two paths | A row a merge MOVES from `seal/ledger.md` to a release file is not identified by the survival test on either path — the bias toward silence the check documents. The one move is the split, at one release, at a commit with no merge in its range; stated in the module docstring and measured at that release (`questions.md` Q6) |
| `seal.py export --check` counting a release file as a changed work item | Root-level files are not counted, by that command's documented rule; a release file is one more of them |
| `gather_changelog.py`, `CHANGELOG.md` | Unchanged; the changelog has one file by design |

## The measured state, before the build

Read and executed 2026-09-24 by the framer at `9f846733` (the v0.15.0 tag,
this branch's base) in this worktree, and against C's committed tree in
`wt-540` where marked.

| Fact | How known |
|---|---|
| `seal/ledger.md` is 2,736 lines, 1,356,047 bytes, 118 marker lines, 8 standing `## ` areas (82 lines) and 38 `## X.Y.Z` headings (37 versions; `0.9.3` twice until C's `d08c671a`); sections run 9–308 lines | executed — `wc`, `grep -c '^<!-- specs/'`, `awk` over `^## ` |
| The seven hunks of `0be23b80` are seven same-row conflicts | executed — the probe described above; deleted after the run |
| One row anchors into `seal/ledger.md` itself: the row at line 2521 (§0.13.1, `1790076070`) cites `seal/ledger.md#"### 1788331011-two-roots-hold-three-lifetimes"@9b037dcd` and `seal/ledger.md#"### 1788398967-local-modes-records-never-leave-the-clone"@e6b5771f`, both headings in §0.4.0 and §0.5.0. No fragment, document, skill, test or hook cites `seal/ledger.md#` | executed — `grep -rn 'seal/ledger\.md#'` over the ledger, `seal/ledger/`, `docs/`, `skills/`, `agents/`, `tests/`, `hooks/`, `.github/` |
| `evidence_check.py#default_patterns` is the one list — `<home>/ledger.md`, `<home>/ledger/*.md`, `<root>/docs/**/_evidence.md` — and `main`, `reverify`, `migrate`, `skipped_by_narrowing` and `settle.py#anchored_rows` all read it; `check_text` reads no heading and no file name; `unshipped` reads `<home>/ledger/` and skips a name that is not `*.md`; `tree_names` excludes `<home>/specs/` and `<home>/ledger/` and nothing else | read — the whole script |
| Three readers spell the list again: `hooks/evidence-advisor.py#failing_rows`, `hooks/ledger-migrate.py#HOME_GLOBS`, `hooks/root-migrate.py#LEDGER_GLOBS`; `correction_check.py` reads `LEDGER` and `FRAGMENTS` through `git ls-tree -r`; `settle.py#coordinates` opens `LEDGER` and globs `FRAGMENTS/*.md` | read |
| `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py#test_the_defaults_render_the_names_they_have_always_rendered` pins the exact default list; `tests/test_a_row_points_by_content.py` globs the two real addresses at line 1039; `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_corpus` reads `cc.LEDGER` and `cc.FRAGMENTS`; `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger`, `tests/test_a_record_precedes_the_fixes_it_commissions.py` (the five-copies case) and `tests/test_the_ledger_fragments_fold_at_release.py#this_work_items_rows_are_in_the_ledger` open `seal/ledger.md` for a work item's folded section | read — each named case |
| `tests/test_release_hygiene.py#test_this_repository_has_one_root_laid_out_by_lifetime` refuses a non-`.md` entry under `seal/ledger/` and lists no other directory; `LOADED` does not reach `seal/`, so a file named `0.15.1.md` is not a timer | read |
| C's branch at `171feacf` adds to `fold_ledger.py`: `section_heading`, `insert`, `doubled_versions`, a `--check` arm naming a version headed twice, `main` computing `heading` from the found section, and the join message; it repairs the doubled `0.9.3`; its fold-module cases are S3–S8 of its spec (`test_a_second_fold_for_the_same_version_joins_its_section`, `test_the_kept_date_wins_over_today_as_well`, `test_the_joined_section_is_one_section_wherever_it_stands`, `test_a_dry_run_of_a_second_fold_shows_the_section_it_appends_into`, `test_check_refuses_a_ledger_that_heads_a_version_twice`) and `test_release_hygiene.py#test_no_version_heads_two_sections_of_this_ledger` | read from C's committed diff `9f846733..171feacf` in `wt-540`, not from this tree; nothing uncommitted there was opened |
| The standing area of `seal/ledger.md` (lines 1–102) carries 8 `Re-read`/`Corrected` markers, so `test_the_bound_covers_every_candidate_marker_site_the_corpus_carries`'s assertion over the shared ledger's staged blob stays true after the split | executed — `grep -c` over `sed -n 1,102p` |
| `CLAUDE.md`'s ledger paragraphs sit outside the generated block (`<!-- specseal:end -->` at line 17, the rule at line 125), so they are edited in place | executed — `grep -n` |
| The survivor sweep's range is `git diff --name-only` less records of a past state, and `seal/ledger.md` is in it; a 2,600-line removal from the ledger would be needles found standing in the new files | read — `survivor_check.py#corrected`, `#corpus`, and the docstring's *A deletion is one row* section |
| Rows this work drifts, all in `seal/ledger.md`: 11 citing `fold_ledger.py#` (10 in §0.4.0, 1 in §0.5.0 — 4 of them re-read by C at `deade859`), 2 citing `evidence_check.py#default_patterns` (§0.8.0/§0.9.0), rows citing `correction_check.py#ledger_listing` and `settle.py#coordinates` if those units change, `evidence-advisor.py#failing_rows`, `ledger-migrate.py#HOME_GLOBS` | executed — `grep -c` per unit, `awk` for the section |

## User scenarios & acceptance *(mandatory)*

Every new case is seen red before it is committed (§15), and the hand-back
says how. Line numbers are as of `9f846733` and are for opening, never for
anchoring.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the checker reads a release file | Given the fold module's fixture with a row in `seal/releases/0.4.0.md` anchored on `src/service.py#handler`. When `evidence_check.py .` runs, then the row is counted (`N ok` includes it) and its file is printed as a ledger; `--reverify` re-stamps it; `--ledger seal/ledger.md` names `seal/releases/0.4.0.md` as skipped | red today: the row is unread, `3 ok` where 4; `test_the_defaults_render_the_names_they_have_always_rendered` red until the list gains `seal/releases/*.md` |
| S2 · the advisor and the migrate hook read it | The same fixture through `hooks/evidence-advisor.py#failing_rows` (a BROKEN row in a release file is reported at the commit) and `hooks/ledger-migrate.py#ledgers` (an old-format row in a release file is found) | red today in both modules; `tests/test_local_mode_resolves_under_the_git_dir.py`'s parametrised address case gains `releases/0.4.0.md` |
| S3 · `correction-check` reads it | Given a fixture history whose merge drops a `Corrected <date>` marker from a row in `seal/releases/0.4.0.md` while the row stands. When `correction-check --range` runs, then the loss is reported with that path | red today: the path is not in `ledger_listing`; the fragment case is the pattern |
| S4 · `settle` reads it | Given `tests/test_settle_reads_before_it_removes.py`'s tree with a work item's marked section in `seal/releases/0.4.0.md`. When `settle` runs, then the work item is grouped by the coordinates in that file, and a row there anchored inside a retiring directory keeps it | red today: `coordinates` opens `seal/ledger.md` and `seal/ledger/*.md` only; `anchored_rows` follows S1 and is asserted once |
| S5 · the fold writes the release file | Given the fold fixture. When `--version 0.4.0 --date 2026-09-15` runs, then `seal/releases/0.4.0.md` exists and begins `## 0.4.0 — 2026-09-15`, holds both marked `### <id>` sections in id order with the fragment headings demoted as today, every fragment row byte for byte; `seal/ledger.md` is byte-identical to before; the fragments are gone; the message names the file | red today on every assertion about the release file; `fold()` re-pointed |
| S6 · the checker reports the same totals before and after | The fixture's `check()` before and after S5: equal totals, exit 0 — the case the fold module already has, now proving S1's glob against the new home | red until S1 lands; this is the one case that ties phase 1 to phase 2 |
| S7 · a second fold joins the file | Given S5 and a late fragment. When `--version 0.4.0 --date 2026-09-16` runs, then the release file heads `0.4.0` once, keeps `2026-09-15`, holds the late section after the first fold's, one blank line each side, no run of three newlines; `--dry-run` says `appending into the existing file:` and prints the file's heading; the message says so; C's kept-date case holds with no `--date` | C's S3, S5, S6, S7 re-pointed to the file; red on the path today |
| S8 · a fragment already folded anywhere is refused | Given S5 and a re-created fragment for a folded id. When `--version 0.4.1` runs, then exit 1 naming the fragment and the release file its marker stands in; nothing written | C's marker-refusal case re-pointed; red today (the marker is not in `seal/ledger.md`) |
| S9 · `--check` after the fold | Given S5. When `--check` runs, then exit 0 and the count line names the markers across `seal/ledger.md` and the release files (`2 work items marked across seal/ledger.md and 1 release file`, or the phrase the work pins); a copy-edit to a folded note leaves it green | C's count case re-pointed |
| S10 · `--check` refuses a release still in the ledger | Given a `seal/ledger.md` heading `## 0.4.0 — …` (the pre-split shape). When `--check` runs, then exit 1 naming the version and line and `fold_ledger.py --split` as the repair; the fragment and open-row reports still print. Given a release file `0.4.0.md` heading `0.4.1`, or heading `0.4.0` twice, then exit 1 naming the file | red today; C's S8 case becomes the second half |
| S11 · the split moves every section byte for byte | Given a ledger fixture with a standing area and three version sections (one with a `####` heading and a fenced `#` line). When `--split` runs, then three release files exist, each the section's text ending in one newline; `seal/ledger.md` holds the header and the standing area only, ending in one newline; every table row of the file before is in exactly one file after; `--split` again exits 1 (`nothing to split`); with a target already present it exits 1 naming it and writes nothing; with a version headed twice it exits 1 naming it (C's reader) | new cases, red today (no `--split`) |
| S12 · the split rewrites the ledger's own anchors | Given S11's fixture with a row citing `seal/ledger.md#"### <id>"@<h>` where that heading is in a moved section. When `--split` runs, then the row cites `seal/releases/<X.Y.Z>.md#"### <id>"@<h>` — same hash — and `evidence_check.py` reports it OK before and after; an anchor into the standing area is left as it is | red today; the rewrite is `re.sub` over every ledger file the split wrote or kept |
| S13 · the dry run says what would move | `--split --dry-run` prints each version, its line range and row count, each anchor it would rewrite, and writes nothing | pinned; red today |
| S14 · the real tree, rehearsed | Given a `tmp_path` root holding a copy of this repository's `seal/ledger.md` at HEAD (C's `0.9.3` repair included). When `--split --root <tmp>` runs, then 37 files exist under `seal/releases/`, named `0.4.0.md` … `0.15.0.md`; every table row of the copy is in exactly one file; `check_ledger` over the copy before (root = this repository) and over the files after yield the same set of `(coordinate, hash, status)`, in process; the two anchors of the line-2521 row are rewritten to `seal/releases/0.4.0.md#…` and `seal/releases/0.5.0.md#…` and resolve OK. If the copy heads a version twice the case reports C's refusal rather than a mystery | executed at each run of the fold module; red today. The ledger is not staged in this branch, so `on_disk` needs no route here |
| S15 · the layout case pins the new directory | `test_this_repository_has_one_root_laid_out_by_lifetime` gains: if `seal/releases/` exists, every entry is `<X.Y.Z>.md`; C's `test_no_version_heads_two_sections_of_this_ledger` widens to: `seal/ledger.md` heads no version twice, and each release file heads exactly the version its name says, once — green on both shapes of the real tree | read; the widening is seen red on a planted file |
| S16 · the documents say it | `CLAUDE.md` and `CONTRIBUTING.md` §House rules name `seal/releases/<X.Y.Z>.md` as where the fold writes and `seal/ledger.md`'s conflict rule as *when a ledger file conflicts*; `docs/branch-and-release.md` §*The ledger fragments fold in the same commit*, `docs/release-checklist.md` §2 (the once-only `--split` line, and C's sentence reworded: a second fold joins the release file) and §3 (the first `seal/releases/`), `docs/the-evidence-ledger.md` (the opening sentence and §*A retirement would break…*'s list of what `settle` reads), `seal/README.md`'s layout, `README.md` and `README.ko.md`'s trees, `skills/implement/SKILL.md`'s tree and fragment paragraph, `skills/evidence-check/SKILL.md` (the `--ledger` row's default, *One fragment per work item*, the `correction-check` paragraph, *What counts as the tree*), `skills/settle/SKILL.md` §4, `agents/framer.md`'s reading list, and the four carriers of *a finding whose `Location` is under `seal/specs/`, `seal/ledger/` or `seal/ledger.md` is paperwork* (`agents/warden.md`, `skills/code-review/orchestration.md`, `docs/review-chain-spec.md`, `skills/verify/SKILL.md`) add the release files | read by the reviewer; `tests/test_docs_line_wrap.py` green; `test_no_document_says_the_fragments_are_never_gathered` green; both READMEs move together |
| S17 · the ledger's header is true on both shapes | `seal/ledger.md`'s header says a release's rows are its own file under `seal/releases/`, written by the fold, that this file keeps the notation and the rows from before the fragments, and that a section still standing here is what `fold_ledger.py --split` moves at the next release | read; the last clause is what keeps the sentence true until the release |
| S18 · nothing else moves | `fold_ledger.py#fragments`, `#demote`, `#marker`, `#is_marked`, `#open_rows`, `#section`, `#section_heading`, `#insert`: unchanged. `evidence_check.py`: `default_patterns` alone, and its docstring. `gather_changelog.py`, `hooks/root-migrate.py`, `templates/`, `.github/workflows/`: untouched | `git diff --stat` at hand-back read against this list |
| S19 · the ledger stays true | Every row the measured-state table names as drifting is re-read, given a dated note and re-stamped in `seal/ledger.md` (the pre-split shape, as every sibling of this milestone does); `evidence-check --strict .` exit 0 at each phase close | executed |
| S20 · the branch's own sweep | `survivor-check --range origin/release/v0.15.1...HEAD` at hand-back exits 0, with a `survivors.md` row for anything it reports (`questions.md` Q4) | executed at the verify phase |

## Data & interfaces

**`.github/scripts/fold_ledger.py`** — on top of C's tree.

- `RELEASES = "seal/releases"`; `release_path(version)` → `f"{RELEASES}/{version}.md"`,
  printed `/`-joined like `LEDGER` and `FRAGMENTS`, opened through `under()`.
- `release_files(root)` → `[(version, path, text)]` in version order, from
  `glob(RELEASES/*.md)`, the version read off the file name.
- `folded(ledger_text, frags)` → asks `is_marked` over `seal/ledger.md` AND
  every release file; the refusal names the file the marker stands in.
- `main`, `--version`: `block = section(...)`; where `release_path(version)`
  exists, `insert(file_text, block, version)` (C's, unchanged — the file's one
  `## ` heading is found by `section_heading`, the entries go before EOF);
  where it does not, the file is `block`. `seal/ledger.md` is never written
  by a fold. Message: `folded N fragments into seal/releases/X.Y.Z.md under
  ## X.Y.Z — <date>` with ` (appended into the existing file)` on a join.
  The date logic is C's (`insert` keeps the file's date; `heading` prints
  the found line).
- `main`, `--check`: the fragment arm and the open-row arm as they are; a
  third arm over `seal/ledger.md`: any `^## \d+\.\d+\.\d+` line is refused,
  naming the version, the line and `--split` (C's `doubled_versions` narrows
  to a helper this arm and `--split` share — the work decides its name); a
  fourth over each release file: the first heading's version must equal the
  file name and be the file's only version heading; the count line counts
  `MARKER_LINE_RE` across `seal/ledger.md` and every release file and names
  both.
- `--split`: refuse if `seal/ledger.md` heads a version twice (C's reader),
  if any target exists, or if there is nothing to move; else cut each
  section from its `## X.Y.Z` line to the next `^## ` line or EOF, write
  each file (text `.rstrip("\n") + "\n"`), write the remainder the same
  way, then rewrite anchors — over the remainder, every release file and
  every fragment — of the shape `seal/ledger.md#"<heading path>"` whose
  first heading part is a line inside a moved section, to
  `seal/releases/X.Y.Z.md#"<same>"`, hash untouched; print what moved and
  what was rewritten. `--dry-run` prints the same and writes nothing.
  Exit 1 for every refusal, 0 for a split, and a bare `--split` with
  nothing to move exits 1 saying so, like `--version` with no fragment.
- The module docstring: the layout in one paragraph, `--split` under the
  usage lines, the two new `--check` arms, the exit-code paragraph.
- `append()`: unused after this; whether it is removed (and the §0.4.0 row
  citing it narrowed, its dead anchor dropped) or kept is `questions.md` Q2.

**`skills/evidence-check/scripts/evidence_check.py`** —
`default_patterns` gains `os.path.join(home, "releases", "*.md")` between the
fragment glob and the pre-0.10 address, and its docstring says what the third
location is. Nothing else: `unshipped`, `tree_names`, `check_text`,
`resolve_patterns`, `skipped_by_narrowing` read the list or read no path.

**`hooks/evidence-advisor.py#failing_rows`** and
**`hooks/ledger-migrate.py#HOME_GLOBS`** — the same glob added.

**`skills/evidence-check/scripts/correction_check.py`** — `RELEASES =
"seal/releases"`; `ledger_listing` passes it to `ls-tree`; the docstring's
*What it reads* names it and states the cross-path limit in *Scope*'s words.

**`skills/settle/scripts/settle.py#coordinates`** — the `seal/ledger.md` loop
runs over `[LEDGER, *sorted(glob(RELEASES/*.md))]`; `anchored_rows` follows
the checker's list and is asserted once in S4.

**Tests** — `tests/test_the_ledger_fragments_fold_at_release.py` (S5–S14;
`fold()`, `ledger()` and every case reading the folded section re-pointed to
a `released(tree, version)` helper; C's S4 case retired with the reason in (NAME NOT IN TREE until the phase adds it)
the phase record: a release file holds one section by construction, and
`--check` refuses a second heading), `tests/test_release_hygiene.py` (S15),
`tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` and
`tests/test_a_narrowed_ledger_read_says_what_it_skipped.py` (S1),
`tests/test_local_mode_resolves_under_the_git_dir.py` and
`tests/test_the_ledger_migrates_itself.py` (S2),
`tests/test_a_merge_cannot_silently_drop_a_correction.py` (S3; `ledger_corpus`
gains `cc.RELEASES`), `tests/test_settle_reads_before_it_removes.py` (S4),
`tests/test_a_row_points_by_content.py` line 1039's glob,
`tests/test_unverified_rows_close.py`,
`tests/test_a_record_precedes_the_fixes_it_commissions.py` and the fold
module's `this_work_items_rows_are_in_the_ledger` read a folded section from
`seal/ledger.md` or any release file (green on both shapes of the real tree).

**Documents** — as S16 and S17 list them. `seal/ledger.md`'s header
paragraph only; no row is appended.

**`seal/ledger/1790208593-the-fold-writes-each-release-to-its-own-file.md`**
— the new rows: R1 the widened default and the three readers that follow
it (S1), R2 the advisor and the migrate hook (S2), R3 `correction-check`
(S3), R4 `settle` (S4), F1 the fold's target and the join (S5–S9), F2 the
`--check` arms (S10), P1 the split, its rewrite and its refusals (S11–S13),
P2 the rehearsal (S14), L1 the layout pins (S15), D1 the documents and the
header (S16, S17). Each names the case that saw it red.

**`seal/specs/1790208593-…/changelog.md`** — one entry. It states what the
split buys in *Scope*'s words, that the seven hunks of the incident were
same-row conflicts the shape does not remove, and that the 37 sections move
at the release that ships it.

**Unchanged on purpose**: `.github/workflows/hygiene.yml` (`--check` is
already the step), `gather_changelog.py`, `hooks/root-migrate.py`,
`templates/`, `chain_check.py`, `survivor_check.py`, `seal.py`, `bin/`.

## Judgments the tree answered

Listed so nobody reopens them; each can be overturned by opening what is
cited.

1. **The checker's anchor rules do not change.** `check_text` reads no
   heading and no file name; the fixture case that reports equal totals
   across a move is the fold's own. One row's PATH is rewritten by the split
   (S12), the class `root-migrate.py` step 6 already handles. So the item
   stays in 0.15.1.
2. **The ticket's conflict claim is corrected, and the item is built
   anyway by default.** Seven of seven hunks were same-row (executed). What
   the split buys is listed and measured; the build proceeds on the owner's
   `automation` answer, with the corrected claim in the spec, the changelog
   entry and Q1.
3. **The release files are a sibling directory, `seal/releases/`**, not
   `seal/ledger/released/`: the lifetime rule, and three readers that key on
   *everything under `seal/ledger/` is a fragment* (`tree_names`, the layout
   case, `main`'s `rmdir`). The ticket delegated the choice to the frame.
4. **A release file is the section byte for byte**, first line `## X.Y.Z —
   <date>`, no title, no preamble: `settle.py#coordinates` and C's three
   helpers work over it unchanged, and the split is a cut.
5. **The one-time split runs at the release-preparation commit**, not in
   this branch: in the branch it is a 2,600-line move every parallel branch
   conflicts with at D's merge (the milestone's A, B and C all re-stamp
   `seal/ledger.md`), and the survivor sweep would report the moved rows in
   the thousands; at the release commit it meets neither, and the person
   already reads the `--dry-run`. The rehearsal case (S14) is what this
   branch proves; the fold's own first run had the same shape.
6. **`--check` refuses ANY release heading in `seal/ledger.md`**, not only a
   doubled one: after the split the file heads none, a section standing
   there is a fold written to the old place or a split not run, and the
   refusal names the repair. C's doubled-version refusal survives inside
   `--split` and over each release file.
7. **`--split` refuses an existing target rather than joining it.** The
   split is one act; a join is the fold's (`--version`), and a target
   present before the split means the tree is in a state a person should
   look at.
8. **The self-anchored row is rewritten by the split, not removed and
   rewritten by hand.** Its content moved with the file, hash unchanged;
   *REMOVED, not re-pointed* is about content that went.
9. **The narrowing notice stays one name per line** after it grows to 39
   names: the rule is *named, not counted*
   (`test_every_skipped_ledger_is_named_not_counted`), and a `--ledger` run
   is the writing form a session chooses; Q5 measures the length.
10. **This branch re-stamps `seal/ledger.md` in its pre-split shape**, like
    every sibling, and merges the release branch in hunk by hunk with both
    sides read (`CLAUDE.md`). Its own rows citing `fold_ledger.py#main` will
    meet C's re-stamps of the same rows at that merge; that is the ordinary
    shape, resolved as the rule says and checked by `correction-check` over
    the range.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. The residue is six
rows: one for a person that does not block (Q1), two for the work (Q2, Q3)
and three measurements (Q4, Q5, Q6).

Framed 2026-09-24 by framer, before the build.
