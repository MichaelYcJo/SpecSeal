# tests to plant — written by the review orchestrator, acted on by the implementer

| Pin | Destination |
|---|---|
| the protocol names ≥ 1.8 for reviewing, `repeats = 0` + calls per deliverable ("never tools per turn") for implementing, exempt for verifying, and the lens-not-refusal sentence | `tests/test_the_handoff_before_round_one.py` |
| the document's title draft number equals the Status section's opening draft number — catches 🔴 1's class mechanically, forever | `tests/test_the_handoff_before_round_one.py` |
| `skills/code-review/SKILL.md` carries the resume rule: resume the implementing session; fresh spawn only when it no longer exists | `tests/test_review_axes.py` or a sibling — implementer judges |
| the cross-instrument tie: `session_cost.py`'s advisory threshold (1.2) equals the value the protocol's tying paragraph names — the plan's own 6-month failure scenario | new case in `tests/test_the_handoff_before_round_one.py`, reading both files |
