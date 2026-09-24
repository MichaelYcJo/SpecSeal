# 1790208643-the-spec-is-split-and-its-sentences-are-settled — review round 1

| Field | Value |
|---|---|
| Target SHA | ca9314dec758511f203696e0e85c63feb76826d5 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 567 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 and 🟡 2 (the halves rule's *exactly one side*, owner and guides), 🟡 3 and 🟡 4 (the edit arm's single outcome, owner and `CLAUDE.md`) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 was asked to review the whole branch at ca9314de against `release/v0.15.1` (06f10aaa): spec compliance first — for the split, whether every moved sentence arrived unchanged except the listed rewordings, by diffing the old document against the three new ones section by section — then quality, in a clone under the round's own directory, narrow runs only, with the smith's handoff as the account to audit: the split and its citations, tests and anchors; the #488 and #509 sentences in four documents and `CLAUDE.md`; #466's wider pin; #561's checklist readings, to be probed in zsh; #562's escapes and the cell-count case; and the merge that followed #558, #560 and #559.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the halves rule says the hash belongs to exactly one side; where both sides edited the unit it is neither's, and the re-read reads one edit | `docs/the-evidence-ledger.md:98` | open | `75b226a7` re-read nine anchors both sides edited after `4a077852`; F1 `9ceb2e34` → `c6fe69c1` |
| 🟡 2 | the guides carry the same *exactly one side* | `CONTRIBUTING.md:255`, `CLAUDE.md:168` | open | same sentence as 🟡 1 in each; `CLAUDE.md` is the orchestrator's edit |
| 🟡 3 | the edit arm names re-stamp as the one outcome of an edit, so a falsifying edit is re-stamped; `CONTRIBUTING.md` keys the choice to the claim | `docs/the-evidence-ledger.md:47` | open | phase 6 corrected G6, G7, G1, A5 in place, a third outcome the owner omits; `spec.md` §*Out* relies on the sentence covering it |
| 🟡 4 | `CLAUDE.md`'s edit arm has the same single outcome | `CLAUDE.md:138` | open | copy of 🟡 3's sentence |
| ⬜ 5 | *Nothing downstream can see that* now follows the paragraph saying the checker sees it | `docs/the-evidence-ledger.md:107` | open | the halves paragraph was inserted before the paragraph that pointed at the #424 one |
| ⬜ 6 | *this document's `blocks more` default* moved into a document with none | `docs/round-record-spec.md:529` | open | the only `blocks more` is at `docs/review-chain-spec.md:447` |
| ⬜ 7 | the pointer sends every row's refusal to the record document | `docs/commit-review-gate-spec.md:340` | open | floor, `Needs a fix`, reopening, `Written late` are the run document's |
| ⬜ 8 | the #316 paragraph describes SpecSeal's `bin/test` in a shipped skill as the reader's | `skills/verify/SKILL.md:80` | open | the class #474 item 2 corrected at `:367` and `:372` |
| ⬜ 9 | a docstring says the record document owns every row refusal and names the floor as the run document's | `tests/test_a_record_says_what_ran_it.py:439` | open | self-contradictory; over 100 columns |
| ⬜ 10 | *falsifies what an existing ledger row cites* | `skills/evidence-check/SKILL.md:316` | open | a row claims; it cites code |
| ⬜ 11 | three ledger claims name the run document for a section now in the record document | `seal/ledger.md:1086` | open | also `:1256`, `:2682`; a record, so a correction |
| ⬜ 12 | the `CLAUDE.md` exemption and the overview's pending-paste rows outlived `233d1a13` | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/survivors.md:16` | open | also `overview.md:12`, `:45`, `:49`; a record, so a correction |
| ⬜ 13 | the three doubled-notes rows' reading has no answerer | `seal/ledger.md` | open | `overview.md` §*Not done* names nobody; a record |
| ⬜ 14 | the plan's approval line carries a trailing clause, and `chain_check` reports it absent | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/plan.md:7` | open | executed: printed by the generator's check pass; reported, not refused; a record |
| 🟢 | the move adds no rewording beyond the recorded list | `docs/review-chain-spec.md`, `docs/commit-review-gate-spec.md`, `docs/round-record-spec.md` | confirmed | section diff against the base, executed |
| 🟢 | fold markers carried whole | the three documents | confirmed | multiset identical, 9 / 4 / 16, executed |
| 🟢 | absence checks read all three documents | `tests/conftest.py` | confirmed | two planted sentences turned two cases red, executed |
| 🟢 | #561's count is equal across the split and the fold in zsh | `docs/release-checklist.md` | confirmed | 1061 three times, strict 0 three times, executed |
| 🟢 | #562 changes escapes only | `seal/ledger.md` | confirmed | byte-identical modulo `\|`, executed |

## Paste-ready fixes

```
**Hunk by hunk has two halves, and only the notes are a union.** A row's
`Re-read <date>` and `Corrected <date>` notes are both sides', because each
records a reading somebody performed. The anchor's hash is not a union: it
belongs to the side that edited the anchored unit, and to neither side where
both did, because the merged unit is then content neither side hashed. A
resolution that keeps a hash the merge made stale names content that no
longer exists anywhere, and the marker check above cannot see it, because no
marker was dropped. So run `evidence-check` after the resolution: a drifted
anchor is the tool naming the row, and the row is re-read against every edit
the merged unit carries, one side's or both, before it is re-stamped.
```
```
**Hunk by hunk has two halves, and only the notes are a union.** A row's
`Re-read` and `Corrected` notes are both sides', because each records a
reading somebody performed; the anchor's hash belongs to the side that edited
the anchored unit, and to neither side where both did. `correction-check`
cannot see a union that kept a stale hash, because no marker was dropped, so
run `evidence-check` after the resolution: a drifted anchor is the tool naming
the row, which is re-read against every edit the merged unit carries.
`docs/the-evidence-ledger.md` §*A correction a merge dropped* owns the rule.
```
```
**Appended is the word, and a removal is not one — nor is an edit.** A
branch that removes or edits code an existing shared-file row cites must touch
the file the row is in to leave the ledger true. A removal takes the row out
there, and the new claim goes in the branch's own fragment. An edit drifts the
row, and the branch re-reads it against that edit: a claim that still holds is
re-stamped there with a dated note, and one the edit made false is corrected
there first, with a `Corrected <date>` note. Both are keeping an existing
claim true, which is not appending; adding a claim is what belongs in the
fragment, and always did.
```
```
the ledger true. A removal takes the row out there and writes the new claim
into the branch's own fragment; an edit drifts the row, which is re-read
against that edit and re-stamped there with a dated note, its claim first
corrected in place with a `Corrected <date>` note where the edit made it
false. Both are keeping an existing claim true, which is not appending.
```

## Executed probes

| What was run | Result |
|---|---|
| section diff of the base's run document against the three new documents, by heading, fences skipped | every old heading once, planned levels, body changes only the recorded rewordings, the 35-line tail and two re-wraps |
| citation resolver: every `§` citation naming one of the three documents in tracked `.md` and `.py`, against that file's headings | no miss in a shipped file; three ledger Claim cells name the old file (⬜ 11) |
| positional-reference read (`above`, `below`, `this document`) across the three documents | one dangling (⬜ 6) |
| live fold-marker multiset, base against the three files | identical, 29; 9 / 4 / 16 |
| `bin/test` over the 27 changed test modules | exit 0, `1331 passed, 1 skipped` |
| planted a forbidden sentence in each sibling document, ran the two absence cases, restored | both red, tree clean after |
| the checklist's step 2 and §3 readings in zsh on a scratch clone, gather then `--split` then `--version 1.2.3` | 1061 / 1061 / 1061, strict exit 0 / 0 / 0; old form `no matches found`, `0` |
| `git grep` table-line count at `eaba2dd1` and the target | 1047 and 1061 |
| `28439296`'s two ledger files against their parents with every escaped pipe read as a bare one | identical |
| `bin/survivor-check --range origin/<base>...HEAD`, with and without `--exempt survivors.md` | with: exit 0, one exempt used; without: exit 1, one place |
| `correction_check.py --range origin/<base>...HEAD` | exit 0 |
| `claude_block.py --check`; `uvx ruff check` and `format --check` over the edited `.py`; `rider_check.py` | exit 0 each |
| `evidence_check.py --strict .` in the clone, with this report copied in | exit 0 |
| `bin/test tests/test_no_real_identifiers.py` with this report staged intent-to-add in the clone | `5 passed` |
| `round_record.py new` over this report in the clone, record deleted after | exit 0; the tables parse; `Needs a fix` and the floor row copied; ⬜ 14 printed |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; not run by this round, which leaves it to the sealer |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| which date-and-notes pair is the row's, in the three doubled rows (⬜ 13) | not placed; a comment on #562 is the candidate | the orchestrator, who decides whether it goes to #562 or a new issue |
