# 1790208593-the-fold-writes-each-release-to-its-own-file — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | d767fa4a — the tip every check below ran at; this record is committed after it |
| Ran by | smith on Fable 5.1 — the value the spawn gave; this phase ran after two resumes (a usage limit, then a session limit), the first under a harness notice naming Opus 5.5, so the spawning session is the one to confirm |

## What this phase was asked

Verify: the fragment `seal/ledger/<work-item-id>.md` in one pass,
`changelog.md` with the corrected claim, `overview.md`, `bin/survivor-check
--range 9f5902e5...HEAD` with a `survivors.md` row for anything reported,
`bin/evidence-check --strict .` exit 0, `bin/unverified-check --baseline
9f5902e5 seal/specs/` exit 0, `git diff --stat 9f5902e5..HEAD` read against
the spec's unchanged list; before the hand-back, every test module that reads
an edited document or loads an edited script, run, all of them. Framed as
phase 5; phase 6 since #553 joined.

## What this phase found

**The fragment was written in one pass**: 11 rows (R1–R4, F1–F2, M1,
P1–P2, L1, D1), 52 anchors, every one resolving before it was stamped (`0
broken` over the fragment with placeholder hashes, then `--reverify` narrowed
to it). D1 first cited two documents at their title heading, which hashes
the whole file; it now cites the units it edited, the evidence-ledger
policy's first `##` section and the ledger header's own line.

**Q4 — the survivor sweep reported 20, not none.** 18 are right where they
stand and have rows in `survivors.md` with a quote and grounds: the
changelog gather's code (on the unchanged list, and shaped like the fold's),
step C's frame, the owner's `CLAUDE.md`, and the marker line #553 kept for
each work item whose duplicate it removed. One was a copy of the conflict
rule in `docs/the-evidence-ledger.md`, corrected to name the release files.
One was a §0.4.0 row whose claim — *a fold moves the total by the rows two
files cited identically* — the release file made narrower; it carries a
dated `Corrected` note. Final run: exit 0, *every survivor is excused by a
row above (18)*.

**Q5 — the narrowing notice.** `--ledger seal/ledger/<this fragment>.md`
over this tree names 2 skipped ledgers (4 lines with its header and
footer). Over a scratch copy of this tree after `--split` it names 31 (33
lines). The frame's extrapolation to 39 rested on the 37 phase 4 corrected.
One name per line stays; the real figure is the release session's.

**The records arm refused the renamed test names.** C's cases renamed or
retired in phase 2 are quoted in this work item's `plan.md`, `spec.md` and
`phases/phase-2.md`. Those nine lines carry `NAME NOT IN TREE` now, and the
spec's quote of the self-anchored row dropped its two hashes, which the
checker read as live stamps and found drifted.

**S18 read at unit level, not only by `--stat`.** An `ast` comparison of
`fold_ledger.py` and `evidence_check.py` against `9f5902e5`: `section` and
`doubled_versions` changed although S18 lists them as unchanged (both in
`overview.md`'s divergences); every other named unit is byte-identical;
`evidence_check.py` changed in `default_patterns` alone. `git diff --stat`
over `gather_changelog.py`, `hooks/root-migrate.py`, `templates/`,
`.github/workflows/`, `chain_check.py`, `survivor_check.py`, `seal.py` and
`bin/` is empty.

**Every reader, run.** 109 of the suite's 123 modules — every one that names
an edited script (`fold_ledger`, `evidence_check`, `correction_check`,
`settle`, the two hooks), every one that reads an edited document (the same
grep phase 5 used), and every one that mentions the ledger — at `d767fa4a`,
tree clean: `4006 passed, 8 skipped`, exit 0. The 14 left out are the suite
the sealer runs; this run is a probe of the readers, not a seal.

**Ruff over all 17 edited Python files** exit 0 for check and format. The
first combined attempt reported an io error because zsh passed the file list
as a single argument; `xargs -0` over `git diff --name-only -z` is the form
that splits it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
