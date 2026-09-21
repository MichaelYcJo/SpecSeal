# 1789996775-the-gate-states-what-its-own-fixes-disproved — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | cfa718ce |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

#464's records half. The `seal_stamp.letter` row of work item 1789956662's
shipped `spec.md`, and the evidence label on the baseline half in its
`changelog.md`, `plan.md` §*Operational impact* and `overview.md`, each under
the A5 marker (A4, A5). Then the evidence write in one pass: `seal/ledger.md`
R4 corrected and R5 re-read (A7), and this work item's own fragment. Q1 is
built to its default and not answered.

## What this phase found

**A marker cannot sit immediately after a statement that is a table row.** A
`<!-- -->` line between two rows splits the table in every renderer, and the
`seal_stamp.letter` row has three rows below it. The marker sits after the
whole table and its first sentence says so and names the row. `spec.md`
§*The correction marker* fixes two properties deliberately — the uppercase
verb and naming the work item and the issue — and both are kept; what moved is
only where the comment can legally be put.

**Three of the four markers are about a statement that is not false**, and the
template's grounds slot reads *It is false because*. The three A4 statements
are true; what they lacked is the label saying how anybody knows. A marker
asserting the sentence was false would put a second false statement into the
same record, so each reads *It is not false, and that is the point* and then
gives the grounds with the coordinate, which is what the slot is for.

**`--reverify` re-stamped three rows against a drift report naming two
coordinates**, which is `seal/follow-up.md`'s open row reproducing exactly.
R4 cites `moved_line`; R5 of work item 1789956662 and G6 of work item
1789985781 both cite `panel`. All three were opened and judged before the
writer ran, and all three carry a note saying so. A7 names two rows; G6 is the
third and it is marked too, because a row re-stamped and unread is the silence
the follow-up row is about.

**R4 is the row the ticket was really about.** It recorded as **Executed** the
claim *it never says CI reads a ref CI does not read*, and that clause was
false when the row was written — `--base @{-1}` is a spelling where the line
did exactly that. `questions.md` §*What the tree answered* settles which side
moves: the design intent is the row's own wording, so A2 made the code true
and this phase marks the row `Corrected` for having been verified as true when
it was not. Narrowing the claim instead was `plan.md`'s rejected alternative
and stays rejected.

**This work item's own `spec.md` went BROKEN at the records arm the moment A2
and A3 landed.** Its §*Data & interfaces* table carried two coordinates with
a bare filename and the pre-change hashes, and `evidence-check` returned
*file not found — same name at skills/verify/scripts/broad_gate.py (content
differs)*, exit 2. Both are re-stamped with the path written in full and the
old hash named beside the new one. The frame is this work item's live
contract rather than a shipped record, so no A5 marker is owed. In full,
without the backticks the arm reads: the file is broad_gate.py, the units are
moved_line and panel, and the two hashes were f312f19b and e2c844e8.

**Then `overview.md` hit the same arm, and then this record did.** A record
that EXPLAINS a re-stamp has to quote the coordinate it is about, and the
records arm reads a backticked coordinate-shaped token as a live claim
wherever it stands — so the divergence row in `overview.md` and this
paragraph were each refused, on the same two tokens, after the `spec.md` row
they are about had already been repaired. Three refusals for one repair. The
repair that does not depend on the arm is to write the superseded hash bare
and name the unit in prose, which is what all three sites now do.
`seal/follow-up.md` already carries an open row for the comment-shaped
version of this, and this is the same arm meeting a table cell and a
paragraph.

**Q1 is built, not answered.** `CHANGELOG.md` §0.12.2 keeps the unlabelled
copy, the row stays ⬜, the divergence is a row of `overview.md`
§*Not verified* naming the repository owner, and `seal/follow-up.md` carries
the item so a later release branch can take it. `gather_changelog.py#ungathered`
decides by marker and never by content, so the corrected fragment is never
re-gathered and nothing in the tree can see the two copies diverge — which is
why the disclosure is in two places rather than one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `spec.md`'s *a longer ref is why the authoritative statement is a printed line rather than a panel cell* | the same row, saying the elision runs before the frame; and the marker below the table |
| the unlabelled baseline half in three records | the labelled sentence with its answerer, at each of the three sites, each under its own marker |
| R4's uncorrected **Executed** stamp over a claim that was false | a `Corrected` marker on the row, and the code change that makes the claim true |
