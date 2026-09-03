# 1788433011-every-spawn-prompt-is-retyped-from-memory — review round 1

<!-- Written after the fact by the review orchestrator, from the warden
report it received and verified independently at the time — see the
session log. `routing.md` declared this work item through the review
chain, and the review ran; only the committed record was missing until
this file. -->

| Field | Value |
|---|---|
| Target SHA | 5f5d071, against base release/v0.6.0 |
| PR | none yet |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none — every fix is a documentation edit |
| New units | none |
| Needs a fix | yes — 🟡 1 (a ledger row this branch drifted, misreported as pre-existing), 🟡 2 (`overview.md`'s evidence count stale after the branch's own last commit), 🟡 3 (`docs/flow.md`'s roadmap restructuring undisclosed) |

- [ ] Pass

The reviewer read issue #107 and both follow-on comments, all six work-item
documents, the contract, all three agent definitions, the protocol's diff,
and every new or changed test module, then cloned the branch and ran the
full set of test modules named in `plan.md`'s six phases plus `ruff check .`
and `ruff format --check .` and `evidence_check.py` with and without
`--strict`, both on this branch and on `release/v0.6.0` for comparison. It
also re-derived the WINDOW measurement and the Q4 paragraphs' longest-shared-
run figures independently rather than trusting the recorded numbers. None of
the class-enumeration sweep — the section-derivation logic, the three
definitions' byte-identical opening paragraphs, Q1's delivery mechanism, the
scribe's line-length exception, Q2's application-form boundary cases —
turned up a finding. All three findings are about this branch's own
bookkeeping, not about the contract or the agent definitions it ships.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Phase 5's Q4 edit inserted two paragraphs inside `skills/code-review/SKILL.md`'s `## Orchestrator: a fix pass resumes the implementer` section, changing its content hash. `seal/ledger.md` anchors an older, unrelated claim to that whole section, so the edit drifted the row. `evidence_check.py . --ledger seal/ledger.md --strict` on `release/v0.6.0` reports exactly one drifted row (`tests/test_no_document_names_the_old_roots.py#KEEP`); the same command on this branch reported two, and the fragment's own closing commit message described both as "pre-existing" | `skills/code-review/SKILL.md:206-241`, `seal/ledger.md` | fixed at 86dcb13 | reviewer measured the branch drift against a clean checkout of `release/v0.6.0`; orchestrator reproduced the same comparison independently before accepting the finding |
| 🟡 2 | `overview.md`'s evidence line read "five rows... Ten coordinates, all OK", describing the fragment as it stood after commit `5047442`. The branch's actual last commit, `5f5d071`, added five more rows (L6–L10) replacing five rows removed from `seal/ledger.md`, and `evidence_check.py` on the fragment reports 23 ok, not 10 | `seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/overview.md:14-18` | fixed at 86dcb13 | reviewer counted the fragment's actual rows and coordinates against the claim; orchestrator recounted independently before accepting |
| 🟡 3 | Three commits (`96aa3d2`, `e0d3d27`, `28a1400`) rewrite `docs/flow.md`'s milestone plan — moving issues between milestones and adding a new one carrying #30, #84, #120. None of `spec.md`'s Scope table, `plan.md`'s six phases, or `overview.md`'s divergence table names `docs/flow.md`, though `routing.md` covers the whole branch so the commit gate does not block it | `docs/flow.md` (via the three commits) | fixed at 86dcb13 — a divergence row added; corrected once more at round 2 (see round-2.md) | reviewer read `spec.md`'s Scope table and `plan.md`'s six phases and confirmed neither names the file; orchestrator confirmed via `grep` |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: every test module named in `plan.md`'s six phases | 356+ passed |
| reviewer: `ruff check .` / `ruff format --check .` | clean, matching `overview.md`'s claim |
| reviewer: `evidence_check.py` with and without `--strict`, this branch and `release/v0.6.0` | this branch: 2 drifted; `release/v0.6.0`: 1 drifted |
| reviewer: independent recomputation of the WINDOW and Q4 longest-shared-run figures | both reproduced exactly (10-word ceiling, 4-word Q4 paragraphs) |
| reviewer: README skill counts against `ls skills/*/SKILL.md` | 23 total, 5 preloaded — match |
| orchestrator: `evidence_check.py . --ledger seal/ledger.md --strict` on an isolated clone of `release/v0.6.0` | 432 ok · 1 drifted · 0 broken |
| orchestrator: same command on this branch's target SHA | 411 ok · 2 drifted · 0 broken |
| orchestrator: `grep -rn "flow.md"` across the work item's own documents | no match |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| — | none; this is the first round | — |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | — | — |
