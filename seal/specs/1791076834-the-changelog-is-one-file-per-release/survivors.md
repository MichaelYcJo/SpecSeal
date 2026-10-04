# Survivors — the changelog is one file per release

`survivor-check --range e141980a..HEAD`, run by the builder before the
hand-back, reported four places. All four stand in released ledger files,
which `Ledger frozen from` in `seal/config.md` keeps from ever being edited
(`docs/the-evidence-ledger.md` §*A released row is read again in the branch's
fragment*). Each says what was true at its release. Where a row's own claim
named `CHANGELOG.md` and is no longer true, it is corrected by a
`Corrected ·` row in `seal/ledger/1791076834-the-changelog-is-one-file-per-release.md`;
where the wording stands in a row's notes or grounds and the claim still
holds, the row is re-read there.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.11.2.md` | a third filter on the same list, for a changelog fragment the tip's | a re-read note of 2026-09-24 in a released row's notes cell, describing `corrected` as it stood that day; the row's claim (S1, the `rounds/` records) still holds and is re-read in this work item's ledger fragment |
| `seal/releases/0.13.0.md` | it now counts the markers `CHANGELOG.md` carries and refuses a corpus with neither | released row S2's claim, true at 0.13.0; corrected by this work item's `Corrected ·` row citing it, which says the check counts the markers of every release file under `changelog/` |
| `seal/releases/0.4.0.md` | The section is appended, where the changelog gather inserts at the top | a released row's grounds at 0.4.0, about where the ledger fold put a section then; the fold has written a file per release since #547, and the row's claim is not this work item's to restate |
| `seal/releases/0.15.1.md` | F1 · a release commit that moves `## Unreleased` under a version heading removes no sentence: for `CHANGELOG.md` | released row F1's claim, true at 0.15.1 and still true of the root file; corrected by this work item's `Corrected ·` row citing it, which names every path `a_changelog` reads |
