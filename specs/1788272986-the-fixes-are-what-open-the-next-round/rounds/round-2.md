# 1788272986-the-fixes-are-what-open-the-next-round — review round 2

<!-- Began as the verifying round for round 1's fixes; it opened one finding,
so it consumes the cap as a finding round. -->

| Field | Value |
|---|---|
| Target SHA | dc2a752 (fix diff e5e0c48..dc2a752) and 638b4cf, HEAD at review time |
| PR | none yet |
| Broad gate | not yet — the one full-suite run follows the last round |
| Fixes checked by | nobody — round 2's fix is not yet written; the next verifying round sets this |
| Contract changes | none — the fix rewrites one hash cell in the work item's ledger fragment; no unit's contract moves |
| New units | none |
| Needs a fix | yes — 🔴 1 (the re-anchored `## Comparison axes` ledger row is drifted at HEAD and CI's evidence check exits 1 on it; one `--reverify` run closes it). Every round-1 verdict is otherwise closed, and both fix-surface rows are truthful |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1-1 | round-1 🟡 1 separator-only cell | `skills/code-review/scripts/chain_check.py:1397` | closed | guard sits after the `says_none` continue, before the `label != CONTRACT` skip, so it reaches both rows; `EMPHASIS.sub` first catches a bare-backtick cell; strip set `SEPARATORS + ";"` consistent with `SEPARATORS`; regression test discriminates — round 1's identical fixture ran exit 0 against the unguarded code |
| 🟢 1-2 | round-1 🟡 2 fail-open coverage | `.specseal/map/1788272986-the-fixes-are-what-open-the-next-round.md` | closed | fact merged, anchored at `chain_check.py#git` |
| 🟢 1-3 | round-1 🟡 3 ASCII arrow limit | `skills/code-review/scripts/chain_check.py:1335`, `docs/review-chain-spec.md:615` | closed as recorded limit | both sentences exist, `RECORDED_LIMIT` needle binds both, current behavior pinned executed, no parser crept in |
| 🟢 1-4 | round-1 🟡 4 security exemption ground | `skills/code-review/SKILL.md:71` | closed | good-faith sentence present, pin contiguous on one line, 49 passed across the three targeted files |
| 🔴 1 | `dc2a752` re-anchored the Comparison-axes ledger row to a hash computed on the wrong side of its own edit — DRIFTED at HEAD, and CI's `evidence_check.py .` (no `--strict`, test.yml:87) exits 1 on it | `.specseal/map/1788272986-the-fixes-are-what-open-the-next-round.md` row `skills/code-review/SKILL.md#"## Comparison axes"@3da5dc89` | open | executed: `evidence_check.py --strict .` → 66 ok · 1 drifted, "content changed at 44-123 — re-verify". The section's content is correct; the hash is what is stale. Fix: `--reverify` the fragment |

## Executed probes

| What was run | Result |
|---|---|
| test_the_fixes_name_their_surface + test_review_axes + test_docs_line_wrap | 49 passed |
| `ruff check` on the two changed .py files | clean |
| `evidence_check.py --strict .` | 66 ok · 1 drifted → 🔴 1 |
| `chain_check.py --baseline origin/release/v0.3.0` | exit 1 — unchecked `Pass` + `nobody` notice, the true mid-run state; round-1's fix-surface rows parse clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/chain_check.py#fix_surface` | the guard and the recorded limit live here; any later fix touching the function re-opens both |
| round-1 | `tests/test_the_fixes_name_their_surface.py` | round 1's New units surface — three tests and a constant, judged as code this round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain — 🔴 1 is fixed in this work item, not deferred.
