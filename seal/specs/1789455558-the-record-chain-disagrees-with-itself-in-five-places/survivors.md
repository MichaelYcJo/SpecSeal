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
that text changes.

**Re-run over round 2's fix range** (`fc204d34..HEAD`): three survivors. Two are rows below — phase 4's record of the sentence it drafted, and a coincidental overlap in an unrelated hook. The third was `questions.md` Q6, still carrying the draft as though nothing had reviewed it, and that one was CORRECTED rather than excused: Q6's whole purpose is to say what the sentence is, and two rounds had changed it. -->

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
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-4.md` | `an unrecognised verdict counted as closed is the tolerant` | Phase 4's record quotes the sentence it DRAFTED, which is what that phase did. Two rounds have corrected the live sentence since; `questions.md` Q6 carries the version that ships. Group 1 |
| `hooks/worktree-guard.py` | `close or drop the quote and re-issue.` | Coincidental phrase overlap with a message in an unrelated hook about an unclosed quote in a commit body. Nothing to do with this change. Group 3 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/questions.md` | `a verdict counted as closed without being one of those words is the tolerant read` | Q6 quotes the sentence that SHIPS, and the new sentence deliberately keeps most of the old one — only the two corrected clauses changed, so the unchanged remainder reads as overlap. The row was corrected rather than excused first: the draft is gone and this is the live wording. Group 3 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-4.md` | `` `Pass` is checked, and this row's verdict reads `<word>`, which is outside `` | The block quote of the sentence phase 4 drafted. A phase record says what that phase did, and drafting this is what it did; `questions.md` Q6 carries the version that ships and names both corrections. Group 1 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/phases/phase-4.md` | `The vocabulary is **rendered from `CLOSED_WORDS`** rather than written out` | Still true of the shipped sentence — the list is rendered from the set today. The overlap is with Q6's own restatement of the same fact, not with anything removed. Group 3 |
| `seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/overview.md` | `the assertion #406 deleted, so its second half is now untrue` | The divergence row's account of why the ledger row was touched; the ⬜ 6 correction stands in the same cell. Group 3 |
