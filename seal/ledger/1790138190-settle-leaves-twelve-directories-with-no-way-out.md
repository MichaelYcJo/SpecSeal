<!-- specs/1790138190-settle-leaves-twelve-directories-with-no-way-out -->

<!-- One work item's rows. No header — `fold_ledger.py` writes the `###` at
the release and moves this file into `seal/ledger.md`.

G4 re-founds the claim of the row this work item REMOVED from
`seal/ledger.md` §*Who checked the last round's fixes*: that row's only anchor
lay inside `seal/specs/1788184145-…/rounds/round-3.md`, a directory the next
fold retires, so the claim moves to the prose that already states it. No row
here anchors under `seal/specs/` (`spec.md` G4), or the next fold's guard
would keep this directory. -->

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| G4 · the last round's fixes are read by nobody, and the box saying the review passed is ticked by the session that wrote them — measured on two consecutive work items (#33), and the reason a round record carries `Fixes checked by` | `docs/review-chain-spec.md#"## Two records, and what each of them says"@61feb2c9` | **Read** 2026-09-23: the section states the #33 measurement — round 2 of the first work item found seven defects inside round 1's fixes and round 2's own went in unread; the work item after it ended the same way, four findings fixed by the orchestrator, opened by nobody, beside `- [x] Pass` — and derives the `Fixes checked by` field from it | 2026-09-23 | Replaces the `seal/ledger.md` row of the same claim, REMOVED by this work item because its one anchor lay inside `1788184145`'s `rounds/round-3.md`, which that row's own Notes said `settle` would have to drop. The section still names that record's path in prose; the path resolves until the fold that retires the directory, and `settle`'s citation listing hands it to that fold |
