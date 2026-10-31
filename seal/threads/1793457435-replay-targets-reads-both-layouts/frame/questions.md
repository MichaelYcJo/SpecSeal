# Questions for the planner: 1793457435-replay-targets-reads-both-layouts

The tree answered these judgments that the ticket left open. Do not reopen them:

- Whether the scaffolds should write the thread layout: `frame/plan.md` A3 and A4.
- Whether `evals/README.md`'s rule on a changed scaffold applies: `frame/design.md` *Grounding*, the `evals/README.md` row.
- Whether records written in `seal` blocks since #1198 are in scope: `frame/design.md` *Grounding*, the `checks_at` row.
- Which exit code the empty read takes: `frame/plan.md` A5.
- How a block record's values are read: `frame/plan.md` A6.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What does the proofer read, and where does it write its record, when the current release runs a committed 0.22.x case? Its `seal/README.md` does not open with `hooks/lib/optin.py#MARKER`. The issue's comment asks for one such run. A framer cannot make it: the run starts `claude plugin eval`, which spawns the proofer, and contract rule 6 withholds spawning from every agent. | a measurement | Run `python3 evals/scripts/noninferiority.py run --agent proofer --rev <HEAD> --case replay-1791382684-r2 --runs 1 --out <scratch>/side.json`, then read the run's `report_text` and its graders. (a) The side reads the case's records and writes at the prompt's path: the committed cases stay valid, and Q2 has no urgency. (b) The side looks for its records under `$(git rev-parse --git-common-dir)/seal/`, or misses its earlier rounds: the committed cases measure a tree no user runs, and Q2 has grounds. | The build does not wait on it, because neither answer changes the reader. The orchestrator makes the run after the phases close. It records the result as a row of `frame/plan.md` *Judgments of the run* and carries it into the issue Q2 opens. | open |
| Q2 | Should the proofer suite's eight committed cases, cut from 0.22.x records, be replaced by cases cut from thread-layout records? After this work, `--count` can pick those. | a person | (a) Replace them: the suite measures trees the current plugin reads as its root. No recorded side is lost, since 0.27.0 already made the next comparison run both sides fresh. But the cases measured change, and the owner chooses those. (b) Keep them: the suite stays comparable to its own cases, and each of them rebuilds a tree the current plugin does not read as its root. | (b) for this work: no committed case changes (`frame/design.md` Scenario 5). The orchestrator opens an issue carrying Q1's result. | open |
