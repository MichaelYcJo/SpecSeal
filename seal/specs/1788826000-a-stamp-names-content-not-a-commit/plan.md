# 1788826000-a-stamp-names-content-not-a-commit — plan

## The approaches, and what each fails at

The direction is settled by the ticket and by `skills/evidence-check/SKILL.md`.
What was open is where the ledger's analogy stops holding, so the alternatives
below are three readings of that, not three directions.

### A — the rider anchors the unit it points at, rider blocks removed from the hash

`Verified <date> against <anchor>@<hash>`, anchor resolved in the rider's own
file by the ledger's own resolver, hash taken over the anchored region with
every `# RIDER:` block stripped out of it.

**Fails when** a change consists only of adding or removing a comment inside the
unit: nothing drifts. Also when an ordinary comment is butted directly against a
rider with no blank line, because the block is read as the run of comment lines
and absorbs it — the region loses lines it should have kept, so an edit to them
goes unreported.

Both failures are conservative: they lose an alarm, never invent one.

### B — the rider is hoisted above the unit, so no exclusion is needed

Make it a rule that a rider sits immediately above the unit it is about. The AST
span then excludes the comment and the hash needs no special reading.

**Fails immediately, on the corpus that exists.**
`skills/evidence-check/scripts/evidence_check.py`'s rider is about one
`except OSError` inside a 43-line function; `hooks/worktree-guard.py:1484`'s is
about one `if tool in ("Agent", "Task")` inside a 335-line `main`. Hoisting
either puts the comment somewhere other than at the line it is about, and
arriving at that line is the entire reason `seal/follow-up.md` moved riders out
of a list. It buys a simpler hash by breaking the convention the hash is for.

### C — drop the staleness signal entirely

Delete the stamp. `grep -rn "RIDER:"` still finds every rider, and the comment
still says what it says.

**Fails at the trade `seal/follow-up.md` wrote down.** That file's *what that
costs* paragraph is explicit: nothing forces a rider to be deleted, so a comment
can outlive the fix it asked for, and the stamp is the only thing letting a
reader tell a live rider from a spent one. Removing it does not answer the
ticket, it abandons the mitigation the ticket is trying to keep. The paragraph
also says the arrangement is overturnable if the stamps go stale faster than
they are read — and the measured failure is not staleness, it is a merge rule
erasing the referent, which is what A repairs.

**A is taken.** B loses the convention; C loses the safeguard. A loses one class
of silent alarm, in the direction of quiet.

## Phases

Vertical slices: each one ends with something that runs.

| # | What it delivers | Verified by | Status |
|---|---|---|---|
| 1 | The SDD ladder — `spec.md`, `plan.md`, `questions.md` | the documents exist and carry the two arguments | `c2c7864` |
| 2 | `.github/scripts/rider_check.py` — rider block detection, region hashing, anchor resolution, `--check` and `--reverify`. No corpus moved yet | run against the tree: every rider reports the old form, red | `03594e0` |
| 3 | The check in `tests/test_a_rider_reaches_its_file.py`, replacing the ancestry case. Seen red against the unmigrated corpus | the new case fails naming every unmigrated rider, before any stamp moves | `cbdd66e` planted red · `e2076cc` closed it, after mutation found two cases verifying nothing |
| 4 | The corpus migrated — all 19 stamps rewritten by `--reverify` | the new case passes; `grep` finds no `at <sha>` stamp | `4bf8dcb` |
| 5 | The corpus widened — the three unguarded riders brought under the check, the non-canonical one given a canonical stamp | the widened scan finds 20 riders and holds every one | delivered in `03594e0` and `4bf8dcb`; it is not a vertical slice and `phases/phase-5.md` says why |
| 6 | `templates/sdd-round.md` states the `Target SHA` exemption; `seal/follow-up.md` states the new stamp form | the template and the header say it; the test pins the sentence | `c381371` |
| 7 | Records — `overview.md`, `changelog.md`, `seal/ledger/<id>.md`, phase records | written and committed | this commit |

## What is deliberately not built

- **No CI job of its own.** The rider check runs inside the pytest job, which is
  where the old one ran. A second enforcement point is mechanism this change
  does not need.
- **No cross-file rider anchors.** A rider is in the file it is about, by the
  convention's own definition. A `path#anchor` form would invent a capability
  nothing in the corpus uses.
- **`evidence_check.py` is not modified.** It is imported. It ships to other
  repositories through `/specseal:evidence-ci`, and riders are this
  repository's own convention.
