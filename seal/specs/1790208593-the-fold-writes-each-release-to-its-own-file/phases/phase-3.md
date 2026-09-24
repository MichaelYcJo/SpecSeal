# 1790208593-the-fold-writes-each-release-to-its-own-file — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8531d71e |
| Ran by | smith on Fable 5.1 — the value the spawn gave; the run was stopped by a usage limit during this phase and resumed under a harness notice naming Opus 5.5, so the spawning session is the one to confirm what ran phases 3–6 |

## What this phase was asked

#553, joined on the coordinator's instruction during phase 2: the fold strips
a fragment's own leading marker line before writing its own; `--check`
refuses a marker standing twice in `seal/ledger.md` or a release file, naming
both lines, the way #540's arm refuses a doubled heading; the duplicate lines
(with their blanks) are removed from `seal/ledger.md`, every row
byte-identical; a fragment fixture that begins with its own marker seen red
first, and the real-tree case red against a copy of the ledger as it stands.
A second message corrected the count: twenty work items, not two, so the
real-tree case names all twenty pairs. The gate table's four answers are
carried below.

## What this phase found

**Twenty pairs, one shape.** Measured over `seal/ledger.md` at `f3ec093a`:
every pair is `marker`, `### <id>`, blank, `marker`, blank, then the
fragment's own `<!-- One work item's rows … -->` comment — the fragment
began with its marker and the fold copied it under its own. The removal
asserted that shape for each pair before dropping the second marker and the
blank under it: 40 lines out, `grep -c '^<!-- specs/'` 118 → 98, and the
sorted list of table rows (`^| `, 862 of them) identical before and after.

**The arm reads the corpus, not one file.** The first cut refused a marker
doubled inside one file and left one case red: after the fold, the extra
marker the case adds to `seal/ledger.md` duplicates the release file's
marker. That is a work item marked in two files, which over-counts
`--check`'s total exactly as a doubled line does (§12: one defect, two
shapes). So `doubled_markers` takes every ledger and reports each
`path:line`, and the hygiene case gathers the same way over `seal/ledger.md`
and every `seal/releases/*.md`.

**The fold's drop asks only the fragment's first non-blank line**, and only
for the fragment's own id, the way `demote` drops its `# <id>` title: a
marker quoted later in a fragment is text. A fragment that is nothing but its
marker becomes empty and takes the existing empty-fragment path (no section,
removed and named).

**Red first, each executed:**

| Case | Red on |
|---|---|
| `test_a_fragment_that_begins_with_its_own_marker_is_folded_with_one_marker` | the marker stood on two lines of the release file |
| `test_check_refuses_a_marker_that_stands_twice[seal/ledger.md]` | exit 0 (cross-file shape) |
| `test_check_refuses_a_marker_that_stands_twice[seal/releases/0.4.0.md]` | exit 0 (in-file shape) |
| `tests/test_release_hygiene.py#test_no_marker_stands_twice_in_this_ledger` | red against the ledger as it stood; re-run after the corpus rewrite with HEAD's `seal/ledger.md` bytes put back in place and then restored: red, and `fold_ledger.py --check` over those bytes exit 1 naming 20 pairs |

**Mutations**, restored from kept bytes: `own_marker_dropped` returning its
input — 1 red; `doubled_markers` returning nothing — 2 red.

**One docstring stated the doubled count in the present tense.**
`tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger`
said `seal/ledger.md` *carries* eleven marker lines twice; it says *carried*
now, with the twenty and #553, and why the reading stays per occurrence.

**The four answers `CONTRIBUTING.md` §*What a change to a gate must carry* asks:**

- Seen red: the four cases above, on a fixture and on the real ledger's bytes.
- Blocks more: `--check` at the release pull request refuses a work item
  marked more than once, and the hygiene case refuses it on every pull
  request. The wrong direction now is a refusal on a hand-edited ledger,
  and the message names each `path:line` and the repair.
- Prompt budget: zero; nothing asks a person.
- Platform honesty: text handling only, lines split on `\n`, no glob order
  relied on (the report is keyed by work item).

**Rows re-read:** `seal/ledger.md` 297, 302, 303, 311 (`fold_ledger.py`'s
`section`/`main`), 2427 and 2430 (the docstring-only case), and C's F1, F2;
`--reverify .` re-stamped 9 rows; `--strict .` exit 0. Row 311 cites `main`
and was re-stamped in phase 2 without a note; its note covers both phases.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the second marker line, and the blank under it, of twenty work items in `seal/ledger.md` | nowhere — the first marker of each pair stands above its `### ` heading, and every row is byte-identical |
