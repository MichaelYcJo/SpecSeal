# an exited session reads as live for five minutes — questions for the planner

<!-- seal/specs/1788846800-an-exited-session-reads-as-live-for-five-minutes/questions.md
The routing batch was answered before the first edit and is in routing.md.
These are the decisions the ticket itself left open, plus one raised by the
milestone move. Each carries a recommendation, and the work continued under
it rather than stopping. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Where should an unreadable liveness answer land? | **(a) toward active** — an unprobeable owner keeps its transcript counted; reproduces today's behaviour, costs a wrong deny at worst. **(b) toward idle** — opens the fail-open direction `proc_cwd`'s docstring argues against, where the guard reports a single stream and allows a switch that yanks someone else's branch | **(a), implemented.** The chosen design narrows the question: the exclusion is evidence *of death*, not a liveness test, so `lease_owner_alive` returning `None` leaves the session counted. Same rule `fresh_leases` already states for itself | ⬜ |
| Q2 | Should `transcript_idle_minutes` become per-tree instead of per-project? | **(a) leave per-project** — keeps the real signal that another worktree of the project is being worked in. **(b) narrow to per-tree** — a separate behaviour change with its own failure direction | **(a), left alone.** The over-reporting is per-session and the repair lands per-session, which is finer than either option, so this fix does not need it. Narrowing is owed its own ticket | ⬜ |
| Q3 | `docs/flow.md`'s `## 0.9.3` opens *"Three work items on one method rather than one file"*, and that sentence is a claim about enumeration-by-construction, not a count. #256 and #257 are not that method. Should the count and the claim be separated, and how? | **(a)** bump the count and leave the sentence — makes the method claim cover two tickets it is false for. **(b)** separate them: keep the sentence for the three it describes and add the new rows under their own sentence. **(c)** owner rewrites the section | **(b), written plainly.** The method sentence keeps its three; the two new rows arrive under a sentence of their own that does not claim the method. Flagged because it edits the shape of a document the owner writes | ⬜ |

Answerer for all three: **the orchestrator**.

Q1 and Q2 are the ticket's own *Decisions left open*. Q3 arose from the
milestone move to 0.9.3 mid-work.
