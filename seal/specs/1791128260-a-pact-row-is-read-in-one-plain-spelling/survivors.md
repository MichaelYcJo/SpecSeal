# Survivors — a pact row is read in one plain spelling

Round 1 of PR #793's fix pass made `templates/config.md` silent when copied
whole, and removed the closing memo's sentence that said making it silent
needed the code-span exemption. The framing records keep that reasoning as
it stood when framed, each with a dated correction written beside it in the
same place, so the places below share the removed sentence's wording on
purpose.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/plan.md` | It needs a code-span exemption, which is the very rule #784 rounds 2–4 kept re-opening, for a file no code reads as a config | the approved plan's Alternatives row as framed; the same cell now carries "*Corrected in round 1's fix pass of PR #793:*" saying the template is made silent by a rewrite that needs no exemption |
| `seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/spec.md` | It is not made silent, because that would need the code-span exemption that #784 rounds 2–4 kept re-opening. | spec §*Out* as framed; the same bullet now carries the dated correction, and the over-refusal table row carries the corrected premise |
| `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/plan.md` | `unglued` cuts at the first `<` or `>` and leaves an `&` on the word before it. | brought into this branch's range by its merge of `release/v0.18.2`: the removed wording is work item 1791119071's (#788), whose own `survivors.md` judges this place, a released plan describing `hooks/cmdline.py#unglued`, which no change here touches |
| `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/overview.md` | Without the freeze, one `--reverify` over every ledger that re-stamps a released row in place moves the line its fragment's `Re-read ·` rows cite | brought into this branch's range by its merge of `release/v0.18.2`: the removed wording is work item 1791119072's (#786), which reworded `docs/the-evidence-ledger.md`; the standing line is a released work item's closing memo, a record of what was true when it shipped, and no change here touches either |
