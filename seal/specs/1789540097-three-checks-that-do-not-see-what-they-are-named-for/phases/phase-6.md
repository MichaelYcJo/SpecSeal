# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | cbf4dc73 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The closing pass. The documented widths in `tests/test_docs_line_wrap.py`'s
docstring re-derived with the module's own helpers; the drifted ledger row
phases 3 and 4 create re-read and its claim judged (`questions.md` Q2); and
this work item's ledger and changelog fragments written.

## What this phase found

**#422 reports one stale width and there are two, plus a restatement.**
Re-derived with `prose_lines` and `display_width`:

| File | Documented | Measured |
|---|---|---|
| `agents/scribe.md` | 160 | 160 |
| `agents/smith.md` | **148** | **109** |
| `skills/writing-style/SKILL.md` | 209 | 209 |
| `skills/implement/SKILL.md` | **99** | **90** |

Nobody reported the second. The first is also written a second time inside
`COVERED`'s own comment — *`smith.md` and `scribe.md` sit at 148 and 160* —
which is the instance a fix aimed at the coordinate would have left standing
(`agent-contract` §12). All four now equal what the helpers report, and the
docstring says they were re-derived and on what date, because a number
written by hand is what went stale.

**Four ledger rows drifted, not one, and the frame says none of them is in
the shared file.** `plan.md` §*The ledger* states *No row in `seal/ledger.md`
anchors a unit this work changes*. `bin/evidence-check .` reported otherwise
at exit 1:

| Row | Where | Drifted by |
|---|---|---|
| `test_docs_line_wrap.py#COVERED` | `seal/ledger.md:1752` | this phase's correction of the restated 148 |
| `test_one_word_one_meaning.py#test_no_instructing…` | `seal/ledger.md:2203` | phase 2's `SEAL_BARE` |
| the same anchor again | `seal/ledger/1789455558-….md:13` | phase 2 |
| `test_chain_hooks_hardening.py#test_the_questions…` | `seal/ledger/1789518345-….md` | phases 3 and 4 — the row Q2 is about |

Each was READ before anything was rewritten, which is the whole of what the
shared-file rule asks. The first claims which modules a review-skill split
breaks; the second and third claim the seal rule is held by one sweep that
skips a hit followed by a letter. A comment correcting a number and a literal
hoisted into a constant leave all three exactly as true as they were, so
nothing was corrected and only the hash moved. Both `seal/ledger.md` rows
carry **Re-verified 2026-09-16** in their Notes and the first's `Checked`
date moves from 2026-09-11, so a later merge that reverts either one is
visible — which is #424's whole subject, and #424 was filed today from this
release's own mistake.

**Q2 is answered `correct in place`, the default, and the row was half
true.** Its claim — *a check decides by what a sentence CLAIMS, not by the
phrase it uses* — was true of the refusal from the day it was written and
false of the finder until phase 4. The anchor never moved and the claim's
subject is the same unit, which is the criterion for correcting rather than
superseding. The claim now reads *a batching instruction in any of its
spellings*, the Verified cell carries what phase 4 measured, and the Notes
say the row was half true and which half.

**`bin/evidence-check .` exits 0 with zero drift**, 1321 rows ok across the
shared file and four fragments, and the records arm reads four work items
with 0 refused — so nothing in this work item's records names a unit the tree
lacks.

**No mutation, and the reason is that nothing in the tree reads a docstring.**
Planting a reader for these four numbers is new mechanism, and it points at
the covered-list question `seal/follow-up.md` already holds open for the
repository owner — which `spec.md` §*Out* rules out with grounds. What stands
in its place is that the numbers were re-derived from the module's own
helpers rather than read off a ticket, twice: once to find the drift and once
against the edited docstring.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The stale widths 148 and 99 in the docstring, and the restated 148 in `COVERED`'s comment | the re-derived numbers in the same places, with the date they were taken |
| The claim that the guard is about the phrase `in one batch` | corrected in place in `seal/ledger/1789518345-….md`, per Q2 |
