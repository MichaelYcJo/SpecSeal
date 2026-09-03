# 1788433011-every-spawn-prompt-is-retyped-from-memory — review round 2

<!-- Written after the fact by the review orchestrator, from the warden
report it received and verified independently at the time — see round-1.md
for why this file exists at all. A verifying round: it checks round 1's
three fixes rather than re-running round 1's broad sweep. -->

| Field | Value |
|---|---|
| Target SHA | 86dcb13, against base release/v0.6.0 |
| PR | none yet |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 4 (round 1's fix pass added an inaccurate `docs/flow.md` disclosure row) |

- [ ] Pass

Narrower by design than round 1, per its own contract's floor on repeated
sweeps: the reviewer re-ran `evidence_check.py --strict` on both ledgers
itself, diffed `seal/ledger.md` between the pre-fix and target SHAs to
confirm only the two rows round 1 named had moved, recounted the fragment's
rows and coordinates, and read the new `docs/flow.md` divergence row against
the three commits it names — including their actual diffs and their order
relative to the phase commits. It did not re-run the phase-test suite, the
section-derivation logic, or the contract-structure sweep round 1 already
covered.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 round 1's finding 1 | ledger reverify | `seal/ledger.md` | pass — no action | `evidence_check.py --strict` reports 413 ok · 0 drifted · 0 broken; `git diff 5f5d071 86dcb13 -- seal/ledger.md` touches exactly the two rows round 1 named, nothing else in the 400+ row file changed |
| 🟢 round 1's finding 2 | evidence-line count | `overview.md:14-18` | pass — no action | fragment holds 10 rows / 23 coordinates by direct count, matching the rewritten line; L6–L10 traced individually and confirmed as the stated replacements for the five rows removed from `seal/ledger.md` |
| 🟡 4 | The new `docs/flow.md` divergence row (added by round 1's fix, at 86dcb13) claimed all three named commits (`96aa3d2`, `e0d3d27`, `28a1400`) restructure milestones and that the restructuring is "a direct consequence of what phases 1–4 measured." Checked against each commit: `e0d3d27`'s diff to `docs/flow.md` only corrects a factual sentence in the 0.6.0 section (marketplace clone → version cache) and moves no issue between milestones. The causal claim is also temporally impossible for two of the three — `git log --oneline --reverse release/v0.6.0..86dcb13` places both `96aa3d2` (position 3) and `e0d3d27` (position 4) before phase 1's commit `37f8c11` (position 6); they cannot be a consequence of measurements that did not exist yet. Only `28a1400` follows phase 4, and its own commit message gives a different, independent reason (the contract's §2/§6 conflicting with the two agents 0.8.0 adds), never the phase-2 CI-lint miss or phase-split cost data the row cites | `seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/overview.md:64` | fixed at b49cfb9 | reviewer read all three commits' diffs and commit messages directly and ran the commit-ordering check itself; orchestrator reproduced both the ordering and the diff-content checks independently before accepting |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `evidence_check.py . --ledger seal/ledger.md --strict` | 413 ok · 0 drifted · 0 broken |
| reviewer: `evidence_check.py . --ledger seal/ledger/1788433011-every-spawn-prompt-is-retyped-from-memory.md --strict` | 23 ok · 0 drifted · 0 broken |
| reviewer: `git show 86dcb13 -- seal/ledger.md` | exactly two rows changed hash, nothing else |
| reviewer: `grep -c '^| L'` on the fragment, and a manual count of `path#anchor@hash` citations | 10 rows, 23 coordinates |
| reviewer: `git show e0d3d27 -- docs/flow.md` | one-sentence factual correction only, no milestone move |
| reviewer: `git log --oneline --reverse release/v0.6.0..86dcb13` | `96aa3d2` and `e0d3d27` before `37f8c11`; `28a1400` after phase 4's commits |
| orchestrator: `git show e0d3d27 -- docs/flow.md` | confirmed independently, same result |
| orchestrator: same `git log --oneline --reverse` ordering check | confirmed independently, same result |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/ledger.md` (the two drifted rows) | closed this round; kept here only as the record of what round 1's fix touched |
| round-1 | `seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/overview.md:14-18` | closed this round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | — | — |
