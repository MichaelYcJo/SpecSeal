# every copy out of `raw` meets the hider question — questions for the planner

<!-- seal/specs/1788873610-every-copy-out-of-raw-meets-the-hider-question/questions.md -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | The false completeness claim stands in a **released** changelog entry, and one of the four documents the ticket names is that entry. `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/changelog.md` is byte-identical to `CHANGELOG.md`'s `## 0.8.2 — 2026-09-06` section, which `gather_changelog.py --check` reports as gathered. Its sentence *"What is left is one cell, named rather than assumed"* is false: what was left is that no copy path was asked about the record it lands in, which is a cell and a whole axis | **leave the shipped text as history** — 0.9.3's own fragment carries the correction, and the released section reads as what was believed on 2026-09-06 · **rewrite the released section** — the changelog then says what is true and stops being a record of what was known | leave it as history, and correct it in this work item's own fragment. Rewriting a dated section makes the changelog a statement of present truth, which is not what a reader opens it for, and the fragment beside it would have to be rewritten to match or stop matching | ⬜ |

Answerer: the repository owner. Nothing in this work item waits on it — the
correction is written either way, and Q1 only decides whether the 2026-09-06
section is edited as well.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
