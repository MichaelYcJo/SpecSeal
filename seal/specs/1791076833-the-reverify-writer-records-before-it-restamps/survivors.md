# Survivors — the reverify writer records before it re-stamps

`survivor-check --range e141980a..HEAD`, run by the builder over the whole
branch before the hand-back, reported three places in one file. None of them
is a claim the range corrected. Two, judged in one row, pin a refusal the
walker still prints, now built from its parts, and one is the heading of the
cases that pin how the `Signatory` table's ends are refused, which the cases
under it still do.
PR #749's own `survivors.md` judged the same three places the same way.

Run again over the build range alone, `e44c75d0..HEAD`, it also reported two
records that quote the sentence `docs/the-pact.md` §*How a signatory names
the pact* lost: this item's own frame, which quotes it as the sentence the
work changes, and work item 1790993137's closing memo, which says what was
true when that item shipped.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_a_signatory_declares_its_pact.py` | which is not a one-cell | the pinned refusal `hooks/config.py#gfm_table` still prints for a table that stops at a row it cannot read, built from `shape` and `written` rather than spelled whole; the removed sentence is the base's literal, and both cases that pin it, one with the sentence split across two string literals, pass against the walker |
| `tests/test_a_signatory_declares_its_pact.py` | # --- every way GFM ends or breaks the `Signatory` table (round 2 of #647) --- | the heading of the cases that pin each end's sentence; the removed sentence is the base docstring's bold rule, which `gfm_table`'s docstring and the property case now carry, and the cases under the heading still cover each way |
| `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md` | this work is that record, so the sentence changes | this item's frame quoting the base sentence in its Grounding as the one this work changes; the frame records what was approved, and the quote is what it changes from |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/overview.md` | is read and printed and nothing acts on it | work item 1790993137's closing memo, true when it shipped in 0.18.0; `spec.md` §*Decision 1* leaves that item's shipped records untouched, and this item's records arm does not read a shipped item's records |
