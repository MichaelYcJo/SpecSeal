# every published reading carries three wrong rows — questions for the planner

<!-- The routing batch was answered before the first edit and is in
routing.md. These are the decisions the tickets themselves left open, plus one
this work raised. Each carries a recommendation, and the work continued under
it rather than stopping. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Are the readings already published re-derived, or marked? | **(a) mark them** — say in the log that every reading before 0.9.4 carries all three, and leave the numbers. **(b) re-derive** — re-run the meter over the transcripts that produced them and post corrected figures. **(c) neither**, and let #145 and #149 take their own readings | **(a), and the marking is posted to #285.** The transcripts still exist so (b) stays available, but what a corrected reading changes about #51's bands is the question #145 and #149 are scheduled to ask, and answering it here would answer it off one work item's convenience rather than off a design | ⬜ |
| Q2 | Should a repository be able to NAME its own runner, in `seal/config.md`? | **(a) no**, the widened pattern plus the printed line is the whole answer. **(b) yes**, a `Test command` row read through `hooks/config.py`. **(c) yes, and more than one row**, so `lint/type` and `build` are nameable too | **(a), built.** (b) is the most faithful shape and the one this work rejected on cost: it cannot help a repository on the day it installs, and it puts a hook's parser inside a script whose argument is a transcript that need not belong to the repository the command runs in. If the printed line turns out to be ignored rather than acted on, (b) is where to go | ⬜ |
| Q3 | `bin/evidence-check` — 256 calls, and the single slowest command in the segment #200 was found on — belongs to no family. Should it have one? | **(a) leave it in `other`**, now that the report names it. **(b) a `project` family** for anything under `bin/` or `scripts/`. **(c) a `check` family** alongside `lint/type` | **(a), left.** (b) is the ticket's own third shape and its own objection to it stands: it does not say what the command does, and a name that describes nothing is not better than `other` — it is `other` with a smaller cell. What changed is that the reader is now told | ⬜ |
| Q4 | `load`'s per-turn `output` was removed rather than repaired. Should a consumer bring it back? | **(a) leave it removed.** **(b) restore it, taking the maximum across the message's rows** | **(a).** Nothing read it, and what sat there was the first partial count — #202's defect in the reader that has no reader. The shape a consumer should take is written where the element was | ⬜ |

Answerer for all four: **the repository owner**.

Q1 is #200's own closing paragraph. Q2 and Q3 are the shapes #200 left
undecided. Q4 is this work's own, raised by #202's *Not verified* row.
