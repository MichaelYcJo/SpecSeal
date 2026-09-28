# Survivors — the stamp reaches the person it is drawn for

Round 1's fix pass (`survivor-check --range a3b76a2f..23e75f53`) reported two
places. Both share wording with the orchestrator's old sentence about the
no-session line, which the range widened to every line naming a values
file. Each place is about the no-session line alone, which still says no
Claude Code session was found and still names `seal-stamp --from`, so
neither is a claim the range corrected.

| Path | Quote | Grounds |
|---|---|---|
| `agents/sealer.md` | Where it says no Claude Code session was found, quote it as it stands: that line is where a reader learns the stamp will not appear by itself. | the sealer's instruction for the no-session line, which is still true: that line still says no session was found, and it is still the only line saying no hook will draw the stamp. The sentence before it in the same paragraph now says every line naming a values file names the command |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | The line says no session was found and names `seal-stamp --from <path>`, so the stamp is not lost and nothing claims it will appear. | S14's case docstring, about the no-session line only, which still says both things; the case asserts them, and now asserts the path quoted too |
| `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/plan.md` | **S17 is not a phase.** It is read by the owner on the first real sealer run | the approved plan's record of how S17 would be read, which is what was planned and stays as written. S17 was in fact read before the merge, on 2026-09-28, with the branch's hook registered for the run's own session, and overview.md's S17 row carries that. The release preparation (#654) closed the overview row, which is the range survivor-check reports; the plan is a record of the gate, not a claim about the present |
