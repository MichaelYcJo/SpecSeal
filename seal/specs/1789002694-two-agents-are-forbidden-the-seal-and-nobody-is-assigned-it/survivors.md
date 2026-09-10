# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — survivor exemptions

## Phase 3

`survivor-check --range 52f6bd3..HEAD` reports three places. Two were real
survivors of the same correction and are fixed in the range —
`skills/code-review/scripts/chain_check.py`'s two failure messages told a
reader to take the broad run by hand and to write the cell with
`round_record.py close --broad-gate`, which is what this phase moved to a
sealer spawn. They are corrected and pinned, so they are not exempted here.

The third is not a stale copy of a corrected claim. It states a different
fact, in a sentence the correction did not touch.

| Path | Quote | Grounds |
|---|---|---|
| `README.md:71` | At the gate, the run is read against the base commit: a failure that predates the work is named as a follow-up rather than chased, and nothing edits between that seal and the PR. | **Still true, and about a different subject.** What the range removed is `agents/smith.md`'s instruction to the implementer — *when the broad gate returns a failure, first ask whether it fails on the base commit as well* — which named an act the smith no longer performs, because `broad-gate` now re-runs the failing files at the base itself and hands back `new` or `failing on base too`. The check matched two phrases the two sentences share, *"a failure that predates the"* and *"the work is"*, scoring 1.60. The README sentence names no actor: it says the comparison happens at the gate and what a base failure is treated as, and both are exactly what the gate does now. Correcting it would remove a true statement about the design in order to erase a coincidence of wording |

**What would make this exemption stop holding.** The quote is the anchor. If
that sentence comes to name WHO takes the comparison — the smith, the
orchestrator, or a session reading the report — it is asserting the act this
range moved to the sealer, and it becomes a genuine survivor.

## Phase 4

`survivor-check --range 6f09a3f..HEAD` reports four places, and the corrected
sentence behind three of them is one this phase wrote: `seal/ledger.md`'s G2
row said *`close --broad-gate` is the only thing that changes the value*,
which #30 made false by adding `seal`.

**Two of the four were corrected rather than exempted**, and they are the two
that are alive: `skills/code-review/scripts/chain_check.py`'s gate docstring
and the inline comment a hundred lines below it both enumerated the writers of
the `Broad gate` cell and both stopped at one. Phase 3 left them, reading the
sentence as reasoning that survives `seal` joining `close`; the word in it is
*only*, and the conclusion it carries — *so a cell this arm cannot parse there
is a cell somebody chose* — rests on the enumeration being complete. An
enumeration one short is the defect, which is the same class phase 3 corrected
in the docstring of the case that pins that arm.

The three below are records of what was true when they were written. None of
them describes the tree as it stands, and correcting one would rewrite what a
past release shipped or what a past phase decided.

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | above the cutoff `round_record.py new` writes the row on every record and `close --broad-gate` is the only thing that changes the value, so such a cell is a choice | **True of the release it describes.** `seal` did not exist in 0.9.5 — #30 adds it in 0.10.0 — so the entry is an accurate account of what that release shipped. A changelog entry is dated by the section it sits in, and editing a shipped section to match a later release makes it a description of the present rather than a record of a release |
| `seal/specs/1788912166-red-for-following-the-documents-green-for-ignoring-one/changelog.md` | above the cutoff `round_record.py new` writes the row on every record and `close --broad-gate` is the only thing that changes the value, so such a cell is a choice | **The same sentence, in the fragment that produced it.** `gather_changelog.py` copies a fragment into the released section and leaves the fragment behind, so this is the source of the row above and shipped with it in 0.9.5. Correcting it would put the fragment and the section it was gathered into out of step, which is the one thing a reader comparing them checks |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-3.md` | Renaming it removes an anchor rather than drifting one, and a removed anchor is BROKEN where a changed body is DRIFTED — so the rename belongs to the phase that touches the ledger, beside the row it forces | **This work item's own record of the handover, and it is what phase 4 carried out.** The corrected text is the docstring of the case phase 3 chose not to rename; phase 4 renamed it and the docstring now says why the old name stood. The record says why phase 3 deferred the rename, which is a statement about a decision rather than about the tree, and it stays true whatever the case is called. The line carries `NAME NOT IN TREE` for the same reason |

**What would make these three stop holding.** Each quote is its own anchor. If
a CHANGELOG section is ever rewritten to describe the tree as it stands rather
than the release it shipped, the first two stop being history and become
present-tense claims; and if `phases/phase-3.md` comes to assert what the case
is called TODAY rather than what phase 3 read and deferred, the third does.
