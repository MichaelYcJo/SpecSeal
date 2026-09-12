# a release is sized by a count and cut by urgency — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

All four survivors of this range come from removing one ledger row — S3 of
`seal/ledger/1789100139-…md`, whose claim named the sizing rule's own wording.
Three of them are another work item's records, and the fourth is a phrase
collision.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-2.md` | `Its evidence sentence — *0.8.3 shipped three of eight, and carrying five forward was the call rather than the failure* — moved with it` | A closed work item's phase record, which says what that phase did at its own SHA. It is true as written: #351's phase 2 moved the rule and its evidence sentence into that paragraph. The evidence sentence itself still stands in the document unchanged — this range did not remove it — so nothing here is stale. Rewriting a shipped phase record would falsify the account of a build that happened |
| `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/phases/phase-2.md` | `**The sizing rule went to the `release:` paragraph rather than to a section of its own**` | The same record, and the same grounds. The placement it describes is also still true: this work item edited that paragraph in place rather than moving the rule out of it, for the reason `plan.md`'s alternatives table gives — a new section would have removed the unit the row was anchored to for no gain |
| `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md` | `That wording is what this work moved and not what the document says today` | #351's changelog fragment, gathered into `CHANGELOG.md`'s `0.11.1` section by the release that also ships this work item. Its claim is what #351 did — the rule moved into that document — and that is still true, so the bullet stays. **Round 1 measured the second half of the original exemption away and it is withdrawn**: `gather_changelog.py` concatenates fragments in work-item id order, so `1789100139` lands ABOVE this one and the released section would have stated the replaced sentence in the present tense before correcting it far below. The bullet is therefore MARKED rather than excused on its own — it now says the wording is what #351 moved and not what the document says today, and points at the entry below that replaces it. The quote above is that marking clause, so this exemption stops holding the moment the marking goes |
| `seal/ledger.md` | `**Re-anchored 2026-09-09, not re-verified**` | A phrase collision rather than a survivor. The two phrases the report shares are `re anchored 2026 09` and `s hash moved`, which are the vocabulary every re-anchoring note in this file uses; the row itself is about `## Phases` in a different document and says nothing about a release's size |
