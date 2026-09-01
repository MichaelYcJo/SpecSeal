# tests to plant — written by the review orchestrator, acted on by the implementer

| Pin | Destination | Planted as |
|---|---|---|
| the protocol names ≥ 1.8 for reviewing, `repeats = 0` + calls per deliverable ("never tools per turn") for implementing, exempt for verifying, and the lens-not-refusal sentence | `tests/test_the_handoff_before_round_one.py` | `test_the_protocol_names_a_bar_per_segment_kind` |
| the document's title draft number equals the Status section's opening draft number — catches 🔴 1's class mechanically, forever | `tests/test_the_handoff_before_round_one.py` | `test_the_title_and_the_status_section_agree_on_the_draft` — planted before 🔴 1's fix and seen red against the 0.7 Status line |
| `skills/code-review/SKILL.md` carries the resume rule: resume the implementing session; fresh spawn only when it no longer exists | `tests/test_review_axes.py` or a sibling — implementer judges | `tests/test_review_axes.py::test_the_fix_pass_resumes_the_implementer` — that file is where the code-review skill's sentences are pinned |
| the cross-instrument tie: `session_cost.py`'s advisory threshold (1.2) equals the value the protocol's tying paragraph names — the plan's own 6-month failure scenario | new case in `tests/test_the_handoff_before_round_one.py`, reading both files | `test_the_advisory_and_the_tying_paragraph_name_one_value` — reads the threshold out of the script with a pattern, so a moved constant with an unmoved sentence turns it red |

drained — all four rows planted (the Planted as column names each function); round 2 judged them as code and mutation-probed all four.
