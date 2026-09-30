# 1790745049-the-guard-and-consent-stop-depending-on-the-walks-order — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 37f29c96 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

The ledger fragment for this item; the rows in 1790660768's fragment that
describe guard or consent behaviour (I13, I15 and any other) re-read and
corrected in place with `Corrected 2026-09-30` notes; the policy sentences in
both specs; this item's changelog fragment, and 1790660768's, whose guard
claims must not stay false; a short `spec.md`, `plan.md` and `overview.md`.

## What this phase found

**Only I13 made a false claim about the guard.** It said the guard and the
consent writer take W after a `cd` behind a redirection; it is corrected in
place and its renamed test anchor removed. I15 states the walk's order, which
still holds for the commit gate, and its guard case still passes through
`base_directories`, so it takes a re-read note. I9, I12, I14 and I2 drifted
with `walk_directories` or the gate's policy section and still hold; I14's
note says `base_directories` skips its second-reading step.

**The drift reached two other work items' rows.** 1790644505's E9, E10, E12
and E16 and one released row in `seal/releases/0.4.0.md` (`_expanded`'s
docstring) each took a dated re-read note; none of their claims changed.

**1790660768's changelog said the guard now judged W.** The sentence now says
the guard and the consent record keep the release base's reading.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| I13's clause that the guard and the consent writer take W | M2 in `seal/ledger/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order.md` |
| 1790660768's changelog clause that the guard judges W | this item's `changelog.md`, which states the accepted cost |
