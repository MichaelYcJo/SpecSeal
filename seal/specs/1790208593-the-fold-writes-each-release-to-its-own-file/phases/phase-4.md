# 1790208593-the-fold-writes-each-release-to-its-own-file — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 84f04568 |
| Ran by | smith on Fable 5.1 — the value the spawn gave; this phase ran after the resume under a harness notice naming Opus 5.5, so the spawning session is the one to confirm |

## What this phase was asked

`--split`: sections cut byte-identical (first line `## X.Y.Z — <date>`, no
title), the one self-referring anchor rewritten, the refusals (target exists
→ refuse, never append; a version headed twice; nothing to move),
`--dry-run`; the rehearsal over a copy of the real `seal/ledger.md` (every
row in exactly one file, checker findings identical in process, the anchor
rewritten and OK); the hygiene real-tree cases widened to be green in both
shapes. The real tree's sections are NOT moved on this branch. Framed as
phase 3; it is phase 4 since #553 joined.

## What this phase found

**29 releases, not 37.** The frame's measured-state row says *38 `## X.Y.Z`
headings (37 versions)*, and the spawn prompt and S14 carry 37 files. Counted
at `9f846733`: 38 `## ` headings in all, of which 8 are standing areas and 30
are version headings for 29 distinct versions (C's doubled `0.9.3`). Here, on
C's base: 37 `## ` headings, 29 of them versions. The 37 is the count of
every `## ` heading. The rehearsal asserts the file set equals the versions
the copy heads rather than a number, so it holds at any release. The
documents in phase 5 state no count. The spec's other figures hold: the
shared ledger keeps lines 1–102 (header and eight areas), and the sections
run from 10 lines (`0.11.2`) to 307 (`0.4.0`).

**The dry run over this tree**, executed at `810c1c09`, exit 0, nothing
written (full output kept in the session's scratch, first and last lines
here):

```
would move 29 release sections out of seal/ledger.md:
  0.4.0  lines 103-409  -> seal/releases/0.4.0.md  (102 rows)
  …
  0.15.0  lines 2620-2694  -> seal/releases/0.15.0.md  (30 rows)
would rewrite 2 anchors into a moved section:
  seal/releases/0.13.1.md:66  seal/ledger.md#"### 1788331011-two-roots-hold-three-lifetimes" -> seal/releases/0.4.0.md
  seal/releases/0.13.1.md:66  seal/ledger.md#"### 1788398967-local-modes-records-never-leave-the-clone" -> seal/releases/0.5.0.md
nothing written
```

**The rewrite is by heading, and names what it cannot place.** An anchor
`seal/ledger.md#"<locator>"` is rewritten when the locator's first heading
part (split on ` / `, `evidence_check.py#HEADING_SEP`) is a heading line of
exactly one moved section. The hash is untouched, and that is safe because
the checker's `normalise` drops blank lines, so a section's trailing blanks
(cut at EOF now instead of before the next `## `) cannot drift a unit. An
anchor whose first part is neither a kept heading nor a moved one — a
quoted text line inside a moved section, say — is printed under *could not
place — open them by hand* and left. The real tree has none.

**Green in both shapes, measured rather than argued.** Every test module
that names the ledger (44, by `grep -l 'ledger\.md\|seal/ledger\|"ledger"'
tests/*.py`) was run with the tree as committed, then again after a real
`--split` in this worktree, with `seal/ledger.md` and C's fragment restored
from kept bytes and `seal/releases/` removed afterwards (confirmed
byte-equal). Pre-split: `1 failed, 1978 passed`, and the one is
`test_every_spec_directory_that_reached_the_ladder_has_an_overview`, red
because this work item's `overview.md` is phase 6's. Split shape: `5 failed,
1974 passed`. The four new ones each read folded sections from
`seal/ledger.md` alone:
`test_a_record_precedes_the_fixes_it_commissions.py#test_the_declared_limit_names_what_escapes_with_the_words_unchanged`,
`test_settle_reads_before_it_removes.py#test_the_rule_over_this_repositorys_ledger_loses_no_section`,
`#test_no_section_of_this_repositorys_ledger_loses_a_coordinate`, and
`test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger`.
Each now reads `seal/ledger.md` and every release file, per file. The
same six targets re-run in both shapes: `53 passed` each. Each of the four
was red in the split shape before its edit, which is how it was seen red.
`test_a_row_points_by_content.py`'s real-tree glob did not go red; it went
blind (it read fewer files), and it reads the release glob now.

**Red first for the cases written after the code**, by mutation, each
restored from kept bytes: no anchor rewritten → S12, S13, S14 red; the cut
running to EOF → S11, S12, S13, S14 red; existing targets not refused → the
target case red; doubled versions not refused → that case red; the row count
counting header rows → S13 red. The six S11–S13 cases were red on the missing
flag before `--split` existed. S15's two pins went red on files planted in the
real tree (`seal/releases/0.4.0.md` heading `0.4.1`; a `notes.txt`), then
removed.

**One cascade in the ledger.** Re-stamping the S1 layout row (§0.4.0) changed
text inside `### 1788331011-…`, which the self-anchored row hashes, so the
next `--strict` read 1 drifted. That row was re-read and noted, and
re-stamped at `84f04568`. The same cascade will recur whenever a row under
those two headings is re-stamped. It is the ordinary cost of an anchor into a
ledger section, not something this work introduced.

**The probe's cost:** two 44-module runs of about nine minutes each, taken
because *green in both shapes* is a claim about modules nobody could list by
reading.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this branch moves no section of the real tree; `--split` runs at the release | `docs/release-checklist.md` §2 (phase 5) |
