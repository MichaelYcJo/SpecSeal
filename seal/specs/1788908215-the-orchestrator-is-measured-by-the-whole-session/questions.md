# Questions: the orchestrator segment is measured by the whole session

The routing batch was answered before the first edit: `smith` implements, the
review chain reviews, the pull request opens, and the boundary is the spawn
cycle. What follows are the assumptions taken under that answer. **None of
them changes what is built**, which is why each is an assumption here rather
than a question that stopped the work.

| # | Assumption | Why it does not wait |
|---|---|---|
| 1 | The mode is spelled `--spawns`, and `--json` gains a `spawns` key beside the existing ones | A flag name is not a decision about behaviour. Renaming it costs one line and no reading |
| 2 | Posting the first reading to #51 is part of this work rather than a separate act | `skills/verify/SKILL.md` §*Where a log is open* already prescribes posting a segment's numbers as part of the segment, and #145's *Done when* names the band #51 is missing |
| 3 | The interpreter-floor guard on `session_cost.py` stays out, with `seal/follow-up.md`'s row untouched | That row's open question is where the five-script class belongs, not how to fix it. Answering it inside this work item would settle a tracker question by editing one of its members |

## Undecidable from a transcript, and therefore not asked

Between taking report *N-1* and spawning *N*, the orchestrator verifies one
report and frames the next prompt. Nothing in the transcript marks the
boundary between those two acts, so a person could not answer it either
without labelling acts by hand — which is what the per-act split would be.
The whole window is charged to the cycle that follows it, `plan.md` says so,
and the row is read as a band rather than as an attribution.
