# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 10

| Field | Value |
|---|---|
| Phase | 10 |
| Commit | bee729a8 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The fragments and the closures, again: ledger rows for S17–S24 in the
fragment; `overview.md`'s divergence rows for what phases 7–9 found, its
`Not verified` table (M5's zsh half where phase 7 could not run it; Windows
as before) and what was fed back; `changelog.md` carrying phase 7's figure;
`plan.md`'s Status column for 7–10. Verified by `bin/evidence-check .
--strict`, `bin/correction-check` and the text-hygiene modules; before the
hand-back, the eight guard modules and `bin/survivor-check` with the work
item's exemptions.

## What this phase found

**M5 needs no `unverified` row.** Phase 7 ran the zsh half, and both shells
printed `{a,b}`, so the `Not verified` table keeps its three rows: the hook
half of M1, the Windows branches, and the full suite.

**The changelog already carries the figure.** Phase 9 rewrote the brace
bullet with phase 7's figure and a pointer to the method, so this phase
added nothing to it (round 4 corrected the figure to 34 of 32,715, one of
them git, in both places).

**The survivors file held.** `bin/survivor-check --range
origin/release/v0.21.0...HEAD --exempt …/survivors.md` exits 0 with the
same eleven places excused: the reframe removed sentences only from §A and
from cases and units this work item wrote, and no copy of them stands
elsewhere.

**What each check said, executed:** `bin/evidence-check . --strict` exit 0,
nothing drifted, broken or naming a unit the tree lacks;
`bin/correction-check --range 5623d728..HEAD` exit 0; `bin/unverified-check
.` reads this overview's three open rows.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
