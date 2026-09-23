# 1790174139-survivors-md-silences-what-it-quotes — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | b503e7e8 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

The records: `evidence-check --reverify .` over the rows `spec.md` §*Data &
interfaces* names as drifting, each re-read rather than re-pointed; the
ledger fragment's new rows; `overview.md` with its `## Not verified` table;
`questions.md` Q2–Q4 filled from the measurements; the branch's own sweep
over `origin/release/v0.15.0...HEAD` (S12) and its `survivors.md` if the
sweep reports anything; `bin/evidence-check --strict .`,
`bin/unverified-check --baseline origin/release/v0.15.0 seal/specs/`, every
exit code read directly. Before the hand-back, mutation-test every unit the
branch added.

## What this phase found

**The re-stamp**, executed: `bin/evidence-check --reverify .` rewrote 24
rows' hashes, exit 0 — the six `seal/ledger.md` rows the plan named
(`corrected` 6652b30d → c2c5ad3e, in S3 of `1788873640`, S1 of `1789211172`
and G5 of `1790138190`; `corpus` cfdd6a91 → 4d2c1cc4 in S6; `OWNER_DIR`
09c29ef5 → 482225d6 in G5 of `1788912166`; the docstring case 588fa7c1 →
1abe4cd8 in S3 of `1789211172`) and the fragment's placeholder hashes. Each
of the six carries a `Re-read 2026-09-24 by work item 1790174139` note
saying why the claim still holds. `bin/evidence-check --strict .` exit 0
after the notes.

**One anchor did not move, and the reason is the checker's rule.** The
docstring section anchor
`survivor_check.py#"## What is excluded, by construction rather than by list"`
kept `57f0406a` although two paragraphs were added under it:
`evidence_check.py#text_regions` gives the heading rule to markdown files
alone, so in a `.py` file a quoted heading owns the contiguous non-blank run
it sits in — its own line. Rows anchored on that section (S3 of
`1789211172`, and E2 and E5 of this item's fragment) therefore pin the
heading's presence, and the case's hash beside it is what pins the content.
Recorded in S3's re-read note; not a defect this work opens or closes.

**The branch's own sweep**, executed at `917eb800` before the exemption file
existed and at `b503e7e8` with it committed: nine places, every one a
carrier of a sentence from the `seal/follow-up.md` row phase 1 deleted, or
the old red message a ledger row recorded seeing. Each took a quote-anchored
row in this item's `survivors.md`. With the file committed — the first
exemption file written on a range checked by the fix it excuses — the same
nine stand without `--exempt` (exit 1) and print under `exempt` with it
(`every survivor is excused by a row above (9)`, exit 0). The folded copies
in `docs/review-chain-spec.md` that S12 anticipated were not reported: no
docstring sentence was removed, only added.

**`unverified-check --baseline origin/release/v0.15.0 seal/specs/`**, exit
0: this item's memo holds three open rows, each with an answerer.

**Mutations**, eight, executed with the module restored from kept bytes and
`tests/__pycache__` cleared between them, every one red: the `survivors.md`
arm off (4 red), the `phases/` arm off (3), the class collapsed to round
records (7), `corpus` and `corrected` each back on `records_a_past_round`
(**6 and 7** over the whole module at `84c6c5ff` — **Corrected 2026-09-24** by
round 2, since both arms of the pool case parametrised at `d3e544d6` go red
under the `corpus` reversion; first recorded here as 3 and 5, which
were the counts under the `-k` selections the mutation script ran, and
round 1's ⬜ b corrected them to the full-module counts, the path-list case
red in both), `OWNER_DIR`'s old tail (1 red, 1 green — the layout arm), and
each new docstring paragraph's opener broken (1 each).

**Narrow runs only.** The module was run at every phase boundary (60 → 64
→ 67 → 69 cases, all green) and ruff over the two edited files; the broad
gate is the sealer's and is the first row of `overview.md` §*Not verified*.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
