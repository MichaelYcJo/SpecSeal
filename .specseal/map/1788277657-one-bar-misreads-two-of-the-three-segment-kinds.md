# 1788277657-one-bar-misreads-two-of-the-three-segment-kinds

Rows for the work item that wrote the per-segment bars and the resume rule
(issue #51, observations 1 and 2).

## One bar no longer judges all three segment kinds

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| The bars are written beside the meter they interpret, one per segment kind, and they refuse nothing — a reviewing segment at tools per turn ≥ 1.8, an implementing segment on `repeats = 0` and calls per deliverable, a verifying segment exempt | `docs/review-handoff-protocol.md#"### After the run — the per-segment bars"@e06930cf` | Read — the section is this work item's own text; `tests/test_the_handoff_before_round_one.py` executed green after the insertion, so the section it pins (the meter pointer, the progress channel) kept its content | 2026-09-02 | The small-round nuance is in the section: a 23-call round read 1.64 with few independent batches to rise on, so the bar reads rounds of ordinary size. The advisory (1.2, in `session_cost.py`) and the bar (1.8) are tied by the section's closing paragraph — the script cannot tell segment kinds apart, the orchestrator can |
| A fix pass is obtained by resuming the implementing session; the fresh spawn is the fallback for a session that no longer exists, and it costs the handoff before round 1 | `skills/code-review/SKILL.md#"## Orchestrator: a fix pass resumes the implementer"@e081e47f` | Read — the section is this work item's own text; `tests/test_docs_line_wrap.py` executed green on the file (it is wrap-covered), and the anchored regions on either side of the insertion kept their content (`evidence-check --strict` clean) | 2026-09-02 | Three measurements, no counterexample: 282 calls / 45 minutes as a fresh spawn (#33) against 30 / 3.9 (#29) and 26 / 5.2 (the #57 chain) as resumes |
