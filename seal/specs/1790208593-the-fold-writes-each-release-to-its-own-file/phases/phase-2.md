# 1790208593-the-fold-writes-each-release-to-its-own-file — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8faae73e |
| Ran by | smith on Fable 5.1 |

## What this phase was asked

The fold writes `seal/releases/<X.Y.Z>.md` — a new file, or C's `insert`
where it exists; `folded` sees every release file's markers; `--check`'s two
new arms (a release heading left in `seal/ledger.md` refuses and names
`--split`; a release file whose name and heading disagree, or that heads
twice, refuses) and the cross-file marker count; C's cases re-aimed at the
release file, naming which are kept and which one retires; Q2 and Q3
decided here; `--dry-run --version 0.15.1` over this tree prints a fresh
file's block.

## What this phase found

**Q2 — `append` stays, and the premise of the question is false.** The row
said `append` is unused once a new file is `section()`'s block and a join is
`insert`. `insert`'s no-section arm calls `append` (`return append(ledger_text,
block)` where `section_heading` finds nothing), so removing it means editing
`insert`, which S18 pins unchanged and C's F1 row anchors. That arm is
unreachable from `main` now — a release file that does not head its version
is refused before `insert` is asked — and the helper stays as the arm's
one-line body. The §0.4.0 row citing `#append@e091419b` keeps the anchor,
with a dated note saying why.

**Q3 — one reader, `version_headings`, with `doubled_versions` as its
filter.** `--check`'s shared-ledger arm reads every `## X.Y.Z` line;
`misnamed` reads each release file for *one version, once, the file's own*;
`doubled_versions` keeps its name and body shape for C's cases and
`tests/test_release_hygiene.py`. `--split` will read `version_headings` in
phase 4.

**C's cases, by name.** Kept and re-pointed to the release file:
`test_a_second_fold_for_the_same_version_joins_its_section`,
`test_the_kept_date_wins_over_today_as_well`,
`test_a_dry_run_of_a_second_fold_shows_the_section_it_appends_into`,
`test_a_fragment_whose_marker_is_already_in_the_ledger_is_refused`,
`test_check_passes_once_folded_and_says_what_it_counted`.
`test_check_refuses_a_ledger_that_heads_a_version_twice` became
`test_check_refuses_a_release_file_that_heads_its_version_twice` (the
second half the plan named). Retired:
`test_the_joined_section_is_one_section_wherever_it_stands` — its premise, an
area `## ` appended after the version section, cannot occur in a release file,
and `--check` refuses a second version heading there. Its anchor is dropped
from C's F1 row in `seal/ledger/1790206437-….md` (narrowed, not
re-pointed), and the renamed case's anchor from C's F2 the same way.

**One case of the original fold work item changed premise, not only
target.** `test_the_one_thing_a_fold_changes_is_a_duplicate_counted_once`
relied on the fold putting a fragment's repeat of a shared-ledger row into
the SAME file, where `check_ledger` de-duplicates on `(coordinate, hash)`.
The fold writes a release file now, so the repeat stays in a file of its own
and the total does not move: `4 ok` before and after, executed. Renamed
`test_a_row_a_fragment_repeats_from_the_shared_ledger_is_still_counted_twice`.
`test_the_section_is_appended_below_the_existing_areas` became
`test_the_release_file_is_the_section_and_the_shared_ledger_is_untouched`; C's
`spec.md` line 92 names the old name, so that line carries `NAME NOT IN TREE`
now, because the records arm refused it (`--strict` exit 2 with `0 drifted ·
0 broken`).

**Red first.** With the module re-pointed and the script untouched: `30
failed, 20 passed` — every case that goes through `fold()` reddens on
*exited 0 and wrote no release file*, and the four new `--check`/refusal
cases on their own assertions. Green after: `76 passed` over the fold module
and the changelog module.

**Mutations, one at a time, restored from kept bytes:** `misnamed` returning
`None` — 2 red; the shared-ledger arm skipped — 1 red; `folded` finding
nothing — 3 red; the count over the shared file alone — 3 red; the join arm
replaced by a fresh block — 2 red.

**`--dry-run --version 0.15.1` over this tree** (executed, exit 0) prints
`## 0.15.1 — 2026-09-24` and C's fragment `1790206437-…` under its marker,
with no *appending into* line: no `seal/releases/` exists yet. `--check`
over this tree exits 1 on two arms — C's fragment unfolded, and `seal/ledger.md
still heads a release … 0.4.0 at line 103` — which is the shape the release
preparation resolves with `--split` then `--version`.

**Rows re-read:** `seal/ledger.md` lines 297, 299, 303 (§0.4.0's
`fragments`/`section`/`append`/`main`, `marker`/`is_marked`/`folded`,
`MARKER_LINE_RE`/`main`) and C's F1, F2 in its fragment; `--reverify .`
re-stamped `main`; `--strict .` exit 0 at the close.

**A #553 phase joins the plan here**, as phase 3, on the coordinator's
instruction after this phase opened: the fold strips a fragment's own
leading marker; `--check` refuses a marker standing twice; the shared
ledger's doubled markers are removed. Measured on this base before the
phase: `grep '^<!-- specs/' seal/ledger.md | sort | uniq -d` names **20**
work items, not the ticket's two — the coordinator's correction arrived
with the same twenty. Phases 3–5 of the frame are 4–6 now.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_the_joined_section_is_one_section_wherever_it_stands` (C's S4 case) | nowhere — its premise cannot occur in a release file, and `--check`'s per-file arm refuses the state it guarded; recorded here and in C's F1 row's note |
| the fold writing to `seal/ledger.md` | `seal/releases/<X.Y.Z>.md`, which `fold()` in the module now asserts on every fold |
