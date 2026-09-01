---
name: evidence-ci
description: Wire the ledger drift check into this repo's CI — vendor the checker and write the workflow, so drift fails a build instead of waiting to be run by hand.
disable-model-invocation: true
---

# /specseal:evidence-ci — put the drift check in CI

The ledger only earns its keep when something checks it without being asked.
Run by hand, the check gets run right after you already remembered the
coordinates — which is the moment you least need it.

This vendors `evidence_check.py` into the repo and writes the workflow. Both
files are committed, so CI does not depend on the plugin being installed on
any machine.

## Why vendored rather than fetched

Fetch-at-run would tie every CI run to a network round trip and to whatever
version the source happens to serve that day. A vendored copy makes the run
deterministic and offline-safe, and puts the checker in the diff where a
reviewer can see it change. The cost is that updates are a deliberate re-run
of this command, not something that arrives silently.

## Procedure

1. **Locate the checker.** It ships at
   `<plugin root>/skills/evidence-check/scripts/evidence_check.py`. Resolve
   the plugin root from this skill file's own path rather than asking the
   user — the point of this command is that no one should need to know where
   the plugin lives.

2. **Check what already exists.** If `tools/evidence_check.py` or
   `.github/workflows/evidence-check.yml` is present, diff against what you
   would write and show it. Overwrite only on the user's say-so; an edited
   workflow may carry deliberate changes (a different path filter, a schedule,
   a dropped `--strict`).

3. **Vendor the checker** to `tools/evidence_check.py`, creating `tools/` if
   needed. Keep the filename — the workflow's path filter names it, so that a
   change to the checker itself re-runs the check.

4. **Write the workflow** to `.github/workflows/evidence-check.yml` from
   `templates/evidence-check.yml`. Two things deserve a question rather than a
   default:
   - **`--strict` or not.** It picks the exit code, not whether the build
     breaks. A coordinate whose content changed exits 1 without
     the flag and 2 with it, and the step fails on either, so a repo
     mid-migration gets no softer mode by dropping it. Strict is still the
     honest default — drift means nobody has re-verified, and 2 is the code a
     broken coordinate already uses. Making drift warn without blocking takes
     both halves: drop `--strict` so drift exits 1, and let the step accept
     that one code.

     ```yaml
     run: python3 tools/evidence_check.py . || [ $? -eq 1 ]  # 2 (broken) still fails
     ```
   - **Path filters.** The template watches `docs/**`, `src/**`, and the
     checker. Replace `src/**` with this repo's actual source roots; a filter
     that never matches is a check that never runs.

5. **Say what happens next, honestly.** If the repo has no `.specseal/map.md` yet,
   the check passes trivially — `no evidence ledgers found` — until the smith
   records a first coordinate. That is not a failure, but it does mean the
   green check proves nothing yet.

6. **Do not commit for the user.** Show the two files and let them review.
   Adding a required check to someone's CI is their call to make in a diff.

## Updating later

Re-run this command. It diffs the vendored copy against the plugin's current
version and reports what changed, so an update is a reviewable diff rather
than a silent swap.
