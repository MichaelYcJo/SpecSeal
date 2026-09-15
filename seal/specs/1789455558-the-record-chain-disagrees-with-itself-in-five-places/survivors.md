# survivors — 1789455558-the-record-chain-disagrees-with-itself-in-five-places

<!-- `survivor-check --range f41927ff..HEAD` at the close of round 1's fix pass
reported ten places still carrying wording the range removed. **None is a live
defect, and they fall into three groups**, each with the same reason.

1. **Records of a past state.** `handoff.md` (four rows) is the orchestrating
   session's account of what it did and when; `phases/phase-4.md` states what
   phase 4 was ASKED, which is a fact about the spawn rather than about the
   code; `plan.md` §*Alternatives considered* quotes the reasoning that rejected
   an alternative, which is still why it was rejected. A record that asserts a
   past state does not stop being true when the present changes, and rewriting
   one is the bookkeeping the ledger's content anchors exist to remove.

2. **Already marked corrected in place.** The two `phases/phase-5.md` rows sit
   in the paragraph that now carries an explicit `CORRECTED by round 1's 🟡 2`
   comment naming what replaced it. The wording stands on purpose, with its
   overturning beside it.

3. **Still true where it stands.** `chain_check.py#open_blocking`'s docstring
   sentence is about the SELECTION, which this fix pass did not change — what
   changed is the message `open_row_reason` builds from it. `overview.md`'s
   divergence row states the history of the removed ledger row and already
   carries the ⬜ 6 correction in the same cell.

Each row quotes the standing text, so the exemption stops holding the moment
that text changes. -->

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/handoff.md` | `Re-verifying is re-reading, and the re-reading happened first` | The orchestrating session's account of its own act, true when written and still true. Group 1 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/handoff.md` | `which refreshed 15 rows, after which` | A record of a run that happened. Group 1 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/handoff.md` | `the broad gate runs the ledger arm` | A record of why the drift was cleared. Still true of the gate. Group 1 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/handoff.md` | `was touched, once, and on purpose` | The orchestrating session's account. Round 1's ⬜ 6 changed how wide the touch should have been, not that it happened. Group 1 |
| `skills/code-review/scripts/chain_check.py` | `an unrecognised verdict counting as closed is the tolerant read` | `open_blocking`'s docstring, about the SELECTION — unchanged by this fix pass, which changed only the message built from it. Group 3 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/plan.md` | `stops being refused at all` | The alternatives table's grounds for rejecting *read the severity from the `#` cell and stop there*. Still the reason it was rejected. Group 1 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-4.md` | `naming the verdict word, naming the vocabulary` | What phase 4 was ASKED, quoted from its spawn. A fact about the spawn, not about the code. Group 1 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-5.md` | `The deletion loses no coverage` | Overturned, and left standing under an explicit `CORRECTED by round 1's 🟡 2` comment that names what replaced it. Group 2 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-5.md` | `So the sweep already reads this sentence.` | Same paragraph, same correction comment. Group 2 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/overview.md` | `the assertion #406 deleted, so its second half is now untrue` | The divergence row's account of why the ledger row was touched; the ⬜ 6 correction stands in the same cell. Group 3 |
