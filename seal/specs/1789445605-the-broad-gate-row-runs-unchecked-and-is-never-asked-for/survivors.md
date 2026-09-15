# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — survivors

<!-- What `survivor-check` reported over this work item's range and why each
report is not a defect. Two row shapes live here; this file uses the range
shape (#297), anchored on the range AND on this work item's directory. -->

`bin/survivor-check --range a99298b6..HEAD --root .` at `33661fb0` examined
1001 files against 40 sentences the range removed, and reported **88 places**:
85 in `seal/ledger.md` and three in other work items' closed records
(`1788993115-a-payload-is-written-again-on-every-spawn/spec.md` and its
`phases/phase-2.md`, `1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red/plan.md`).

**Every one of them traces to one deleted ledger row, and none is a defect.**
This branch removed S14 of work item 1788354065 from `seal/ledger.md`, because
its claim — the bootstrap *asks the mode question … and then the parity
question, and nothing else* — went with the code when phase 4 made it ask a
third. `CONTRIBUTING.md` §*House rules* says a claim that went with the code is
removed rather than re-pointed, so the row went and the new claim is in this
work item's own ledger fragment.

That row's Notes cell carried the boilerplate every row restated by work item
1788993115 (#292) carries — *Restated 2026-09-10 by work item 1788993115
(#292), which moved the Bootstrap section to `skills/implement/…*. Its
neighbours at `seal/ledger.md:1885-1891` carry the same sentence about their
own claims, which are still true and were re-read and `--reverify`'d on
2026-09-15. The three reports outside the ledger are closed records of other
work items, which are not this branch's to edit.

**What the check found where it would have mattered is nothing.** No file under
`skills/`, `templates/`, `agents/`, `tests/` or `docs/` is reported. The three
removals that carry meaning — rule 3's second copy in `skills/config/SKILL.md`,
`templates/config.md` §*Broad gate*'s closing paragraph, and
`broad_gate.missing_row`'s *write the repository's own broad command into it* —
survive nowhere in the tree.

| Range | Grounds |
|---|---|
| `origin/release/v0.12.0...HEAD` | The range removes one `seal/ledger.md` row whose claim went with the code (S14 of 1788354065, *and nothing else*). Every one of the 88 reports is that row's shared Notes boilerplate standing in neighbouring rows whose own claims are still true and were re-verified on 2026-09-15, or in another work item's closed record. Per-place rows do not scale here and none of the 88 is a repair: the three removals that carry meaning survive nowhere, and no file under `skills/`, `templates/`, `agents/`, `tests/` or `docs/` is reported at all |
