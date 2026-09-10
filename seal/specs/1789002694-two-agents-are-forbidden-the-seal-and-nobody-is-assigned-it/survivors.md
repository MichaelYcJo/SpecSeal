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
