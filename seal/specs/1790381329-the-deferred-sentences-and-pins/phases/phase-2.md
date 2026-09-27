# 1790381329-the-deferred-sentences-and-pins — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | e4c76096 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#611. The round's paste-ready sentence in `skills/settle/SKILL.md` §1, naming
*kept: the closure has not reached <base>* beside *kept until the closure
reaches <base>*. The second wording asserted beside the first in
`test_the_documents_say_the_closure_has_to_reach_the_base`; the round's
summary-line assertion in
`test_the_report_does_not_promise_what_the_retirement_refuses`. Enumerate
both heading wordings and the summary line first, English and Korean,
tree-wide.

## What this phase found

- **The frame holds: the skill is the only document naming a heading.**
  Searched at the build tip over `docs/ skills/ agents/ templates/ hooks/
  .github/ README.md README.ko.md CONTRIBUTING.md`, outside `settle.py`:
  *kept until the closure*, *closure has not reached*, *closure reaches*,
  *kept because the closure*, *closure has not*; in Korean *도달하지 않*,
  *닫힘이 … 도달*, *종결 … 도달*, *클로저*; and by meaning, every line naming
  `settle` together with *kept*, *keeps*, *heading*, *남겨*, *남깁*, *제목*.
  Hits and judgments: `skills/settle/SKILL.md:118`, the twin, fixed;
  `README.ko.md:337`, *아무에게도 도달하지 않습니다*, about an unreleased change
  reaching nobody, not a twin; `docs/the-evidence-ledger.md` §retirement and
  `docs/one-root-by-lifetime{,.ko}.md`'s settle rows say a directory is kept
  and name no heading, not twins; both README cheat-sheet rows name no
  heading.
- **The paste-ready text applied unchanged**, and the paragraph re-wraps
  within `tests/test_docs_line_wrap.py`'s bounds (green).
- **Seen red (§15).** The documents case against the unedited skill: red at
  the new assertion. The summary-line assertion is green on the code as it
  stands, because it pins wording that already shipped; it was red with the
  pre-bc63b91d wording (`kept until the closure reaches`) restored in
  `settle.py#main`, then the file was restored from the bytes kept before
  the mutation.
- **Two 0.15.4 rows drifted and were re-read**, M2 and M3 in
  `seal/releases/0.15.4.md`, each with a dated `Re-read` note and its
  `Checked` date moved; no claim became false. No new ledger row: both rows
  already carry the claims, and the note records the new pins.
- **Verified by (executed, 2026-09-26):** `tests/test_settle_reads_before_it_removes.py`
  and `tests/test_docs_line_wrap.py`, 160 passed. `evidence-check .` after
  the re-stamp: 0 drifted, 0 broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
