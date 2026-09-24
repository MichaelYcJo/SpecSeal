# 1790260565-a-ledger-row-carries-two-readings-in-one — questions for the planner

<!-- seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. -->

**The tickets left these judgments open, and the tree answered them.** They
are listed so nobody reopens them. The grounds for each are in `spec.md` and
`plan.md`.

- **#568: which of the two pairs is the row's.** Neither pair alone. In S4
  and G5 the second pair repeats the first pair's opening and adds later
  markers, so the two pairs are one merge's two sides.
  `docs/the-evidence-ledger.md`'s halves paragraph makes a row's notes a
  union. The third row never had a second date.
- **#501: what `overwide_rows` still lacks.** It counts no row that sits
  under no header. Every fragment is headerless by rule, and 25 released
  rows are headerless today. The width to count them against is the one
  `templates/ledger.md` declares.
- **#569 ⬜ 2: which rule the exception names.** It names `chain_check.py`'s
  direction, as the code already says. §*The reopening*'s `blocks more` is
  the reopening check's own failure direction, which is a different rule.
- **Whether `CLAUDE.md` needs an owner's edit.** No. Every needle phase 3
  adds is already in it, and phase 2 keeps fragments headerless.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should the ledger's cell count also ship in the plugin, as a refusal in `evidence-check` that a consumer repository's ledger meets? **Why the tree cannot answer it:** #501 and the policy are written about this repository's files. Shipping the count decides what other people's builds refuse, and that is the product's shape, not a reading. | a person | **(a) Not in this work item.** The count stays this repository's case. The orchestrator carries the question to an issue (or to #566, which holds the same class of "a check that runs only as this repository's test"). **(b) Ship it.** A new arm in `evidence_check.py`, which the parallel chain `1790260566` is editing now. That would need sequencing after that chain, plus a README row and a version-moving change. | (a). The build proceeds unchanged, and nothing in this plan depends on the answer. | ⬜ |
| Q2 | Are the anchors of S4, G5 and the eleven-modules row `ok` or drifted at the build's moment, and would `--reverify` over their release files re-stamp any row this work does not read? **Why the tree cannot answer it now:** it needs a run of `bin/evidence-check`, and framing runs nothing. | a measurement | Lenient `bin/evidence-check --ledger seal/releases/0.8.2.md --ledger seal/releases/0.9.2.md --ledger seal/releases/0.9.3.md .` answers it. If only the three rows are drifted, `--reverify` over those files is safe. If others are drifted, write the three hashes by hand. | The hand-stamp path in `plan.md` *Technical context*, until the run says `--reverify` is safe | ⬜ |
| Q3 | Does S4's claim cell still state the rule the way `docs/issues-and-milestones.md` now does, given its `Corrected 2026-09-24` note says each half "gained the tagged clause" while the claim cell does not mention tagging? **Why the tree cannot answer it at framing:** it is a re-read of the claim against the section, which is phase 1's act. | the work | **Holds:** a `Re-read` note. **False:** correct the claim cell in place, with a `Corrected <date>` note. | Phase 1 decides it and records the reading in the row. | ⬜ |
| Q4 | Does `survivor-check` report the words phase 2 removes from the policy ("three of them a second date-and-notes pair") as still standing somewhere the branch did not correct? **Why the tree cannot answer it at framing:** the survivor sweep's exclusions for released text and ledger release files are the sweep's to apply, and the sweep is a run. | a measurement | `bin/survivor-check` over the branch at phase 2's end. **Reports nothing:** done. **Reports C2 or another row:** correct that row the same way. **Reports released `CHANGELOG.md` text:** record the exemption in this work item's `survivors.md`. | Correct every carrier the sweep names. Write a `survivors.md` row only for released text. | ⬜ |
