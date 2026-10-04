# one `--reverify` leaves the ledger clean and records only a real move (#774, #772, #775) — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

## Why this work exists

A pact change recorded a move from a hash to itself, one unfrozen `--reverify` left a citation it moved DRIFTED until a second run, and two statements of the pact-change trigger left out a refused row; now a move starts at the newest reading, one run leaves the ledger clean, and the trigger is stated whole.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the BROKEN list's old hash is chosen | Plan, technical context: `reverify_into` appends `m.group("hash")` at four sites, the fourth *the `for at, coord, detail, key, recorded in broken` loop* | The hash is chosen in `released_drift`'s family arm, which builds that list; the loop is unchanged | The loop's `key` is the member `released_drift` picked, and only a family's root keys `view.newest`. `released_drift` has `top` in hand. Its only other caller, `main`'s unfrozen arm, discards the list |
| The minor-anchor fallback | Plan, alternatives: *The newest row may spell the coordinate with a minor anchor, and then the match lookup misses. Mitigation: fall back to the member's match and record a divergence row* | No fallback is needed inside a family; `newest_hash` falls back to the member's own hash only for a row outside every family | `view.readings` is keyed by `coordinate_of`, which keeps the minor anchor, so the newest reading of a coordinate always carries it in the same spelling |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository lint and the typecheck at this branch's head | the sealer, after the review rounds settle |

## Not done

**The 0.18.1 hash churn (questions Q2) is confirmed and not fixed.** Phase 2's
probe, recorded in `phases/phase-2.md`, showed `--reverify --checked` under
the freeze, without `--into`, re-stamping and re-dating an outranked older
fragment `Re-read ·` row that `--strict` read OK, with nobody having re-read
it. The in-place walk is family-blind. Fixing it changes which rows the
in-place writer touches and dates, so it needs its own frame. The
orchestrator files it, with that probe as its coordinate.

**The dated note the *Without the row* paragraph promises.** An unfrozen
repository re-stamps a released row in place *with a dated note*, per
`docs/the-evidence-ledger.md`, and the in-place writer writes the date cell
alone. Building the note changes the in-place writer's output for every
unfrozen repository, so it is a finding for the orchestrator to file, as
`spec.md` §*Out* says.

## Fed back into the spec

none
