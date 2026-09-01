# 1788277657-one-bar-misreads-two-of-the-three-segment-kinds — review round 1

| Field | Value |
|---|---|
| Target SHA | b80c2a5 |
| PR | none yet |
| Broad gate | not yet — the one full run follows the chain |
| Fixes checked by | nobody — round 1's fixes are not yet written; the verifying round sets this |
| Contract changes | none — the fixes change document sentences and add test cases; no unit's signature, return arity, return type, or set of returnable values moved |
| New units | `tests/test_the_handoff_before_round_one.py::test_the_protocol_names_a_bar_per_segment_kind`; `tests/test_the_handoff_before_round_one.py::test_the_title_and_the_status_section_agree_on_the_draft`; `tests/test_the_handoff_before_round_one.py::test_the_advisory_and_the_tying_paragraph_name_one_value`; `tests/test_review_axes.py::test_the_fix_pass_resumes_the_implementer` |
| Needs a fix | yes — 🔴 1 (docs/review-handoff-protocol.md:415, Status line still 0.7); 🟡 2 and 🟡 3 can ride the same fix pass or be answered with the grounds quoted |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 0 | Stage 1: all three deliverables land with the issue's numbers verbatim; out-of-scope respected; assumptions A0–A4 sound (A2 verified against the file) | `docs/review-handoff-protocol.md:357`, `skills/code-review/SKILL.md:175`, `specs/1788224363-a-subagent-rediscovers-what-the-session-established/questions.md:11` | pass | every figure traced to its source (issue body, owner comments, agents/smith.md:170-171); Q1's shape mirrors the sibling convention; the map.md touch is the permitted maintenance class, not an append. Orchestrator re-read lines 1/415 of the protocol and map.md:97 and confirms the findings below |
| 🔴 1 | The Status section still declares draft 0.7 under a draft 0.8 title — the document names two current drafts, and Status is what a conformance reader opens | `docs/review-handoff-protocol.md:415` | open | line 1 reads 0.8; `git log -S` shows the 0.6→0.7 bump rewrote this same line, so the convention the bump follows includes it. One-line fix supplied |
| 🟡 2 | The grounds cell "Measured range 1.29–1.89" reads as the complete measured record while the cited issue holds readings outside it on both sides (2.0 baseline; 1.10–1.54 chain) | `docs/review-handoff-protocol.md:367` | open | the bar itself stands — the owner approved observation 1 after those comments; the finding is the sentence's scope. Closes by scoping the claim (fix supplied) or by answering with the grounds that the range quotes agents/smith.md:170-171 verbatim |
| 🟡 3 | The re-stamped ledger row kept Checked = 2026-09-01 while its hash was recomputed on 2026-09-02 — the record says nobody read the section the day it was re-hashed | `.specseal/map.md:97` | open | CLAUDE.md: the Checked column holds the date somebody read the code; overview says the region was re-read in full while writing into it. One-cell fix |
| 🟢 4 | Pins owed to the new rules (merged rule 8) — prescribed through tests-todo, not blocking | `skills/code-review/SKILL.md:364` | answered | the smith's argument that tests-todo is the channel is correct; the four rows are in tests-todo.md and the implementer plants them in the fix pass |

## Executed probes

| What was run | Result |
|---|---|
| pytest test_docs_line_wrap + test_one_word_one_meaning + test_no_real_identifiers + test_the_handoff_before_round_one | 28 passed (warden's own run, matching the smith's) |
| `evidence_check.py --strict .` | 69 ok · 0 drifted · 0 broken — proves the map.md re-hash was computed on the post-edit side |
| `git log -S` on the protocol's Status line | the 0.6→0.7 bump rewrote it — finding 1's convention |
| `gh api` on issue #51 body and comments | deliverables' numbers and finding 2's chronology |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain — all findings handed to the fixing session (smith, resumed).
