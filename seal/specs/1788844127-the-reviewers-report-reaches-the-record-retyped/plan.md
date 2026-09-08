# Implementation Plan: the reviewer's report reaches the record retyped

<!-- seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/plan.md — HOW, in phases.
This is the Design Gate's artifact. The direction was settled by the
repository owner in the routing batch of 0.9.2 and handed to this work item in
its spawn prompt; this file records the design, its rejected alternatives, and
the constraint each one had to answer. -->

## Summary

Two halves of one repair, both from the ticket's primary suggestion.

1. The warden writes its report to
   `seal/specs/<work-item-id>/rounds/round-<n>-report.md` and returns that
   path.
2. `round_record.py new` defaults `--report` to that location, derived from
   `--item` and `--round`. The flag stays.

Then four documents that state who writes what under the work item learn the
distinction the change turns on: **the record is the orchestrator's, the
report is the reviewer's.** That sentence does not exist anywhere today,
which is why the second half of it reads as forbidden.

## Technical context

**What the change rests on.**

- `skills/code-review/scripts/round_record.py:2594-2597` — `--item`,
  `--round` and `--report` on the `new` subparser. `--report` is
  `required=True`; the other two are what the default is derived from.
- `skills/code-review/scripts/round_record.py:1611-1617` — `rounds =
  os.path.join(item, routing.ROUNDS_DIR)` and `round-{args.round}.md`. The
  record's own path is built from the same two arguments, one function away
  from where the report's would be.
- `skills/code-review/scripts/round_record.py:681-687` — `read_text` is the
  one reader, and its refusal already names the path.

**The three constraints the design had to answer, in the order they bite.**

| Constraint | Where | How the design answers it |
|---|---|---|
| *"A `git clone --no-local` … and only there … you never write in it"* | `agents/warden.md:29-34` | A named exception for this one file, written the way the parity mark's exception already is. This is the wall — sharper than §6, and the handoff pointed one section lower |
| §6 *"You write no durable record"* | `skills/agent-contract/SKILL.md` §6 | Untouched. §6 says an exception *"is one agent's, and it is named in that agent's definition — never here"*, so adding it to `agents/warden.md` is the mechanism §6 prescribes rather than a departure from it. The record stays the orchestrator's, written after verification, and the reviewer still commits nothing |
| *"reviewer workers never write here — parallel writers overwrite each other"* | `skills/code-review/SKILL.md:155-160` | The sentence is about `round-N.md` and the two todo files, and stays true of all three. The report is one file per round; where a round runs more than one reviewer, `--report` is still a flag and the orchestrator gives each a path |

**What breaks in 6 months.** A round is spawned, the warden writes
`round-3-report.md`, and the orchestrator never commits it — the record is
committed and the report it was written from is not, so `Fixes checked by`
still points at a round whose report nobody can open. The mitigation is that
the report sits beside the record in the same directory, so the commit that
adds one has the other in `git status` a line away; the residual is that
nothing enforces it. Making `round_record.py new` refuse an uncommitted
report was considered and left out: `new` runs before the record is committed
by design (`skills/code-review/SKILL.md` §*And commit the record before
commissioning the fixes*), so it would refuse every correct run.

**`close` was weighed as the gate in round 1's fix pass, and it fails the same
way.** It runs after the record's own commit, so the timing objection above
does not reach it and the reviewer was right to ask. What defeats it is
`--report`. That flag exists so a report can live somewhere other than the
conventional path — `report_path`'s own docstring names two callers who need
it — and `new` records nowhere which path it read, so `close` has nothing to
ask. A gate there refuses the runs the flag was added for. Executed at
`b76ce68`: with the gate inserted after `close`'s `target` check, 36 of the 41
cases in `tests/test_the_fixes_close_the_record.py` fail, because the suite's
own `generate` helper writes the report outside the repository and passes
`--report` on purpose.

A gate that reaches every run has to make `new` record the path it read, which
is a new field in the record, a template section and a checker that reads it —
mechanism, and a fix pass adds none. A narrower gate needs none of that:
guarded on the conventional path actually holding a file, the same refusal
passes all 41 cases at `b76ce68`, because a run that passed the flag leaves
that path empty. It buys less — it cannot see a report written elsewhere and
never committed — and that, rather than the cost, is why it is deferred rather
than built here. The residual is unchanged and stays in `overview.md`
§*Not done*, with the orchestrator named (round 1 🟡 3, round 2 ⬜ 8).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The ticket's smaller version** — the reviewer returns a path, `new` defaults `--report` to it, and no convention says the reviewer wrote it there | The default's whole value is that the file is at the derived path. With nothing establishing who puts it there, the default fires on a path the orchestrator has to fill by hand — which is the retyping, one step further from where it can be noticed. The two halves are one repair | **Rejected.** The ticket names it as the smaller version and the handoff names it as the rejected alternative |
| **The warden writes the report inside its clone**, at the same relative path, and returns the absolute path in the clone | Keeps `agents/warden.md`'s clone rule untouched, and costs two things. The default never fires — the orchestrator passes `--report <path in the clone>` — so half the repair is gone unless the orchestrator copies the file first, which is a step that can be forgotten. And nothing states when the clone is cleaned, so the returned path names a file whose lifetime nobody wrote down. That is the ticket's own failure shape: a report the next segment may not be able to open | **Rejected.** The clone lifetime is the decisive half — a path into an unstated lifetime is not better than chat text |
| **`new` derives the report from a `--rounds-dir` or a new flag** | A third spelling of a path two arguments already determine. Any drift between it and the record's own path is silent | Rejected |
| **The chosen design** — the warden writes into the repository under review, at the conventional path, one file, uncommitted; `new` defaults to it | Needs a named exception in `agents/warden.md`. That is a real cost and it is written where the rule it excepts is | **Chosen** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The report reaches the record as a file: the reviewer is told where to leave it, `round_record.py new` defaults `--report` to that path, the flag still wins, the absence is named, and the four documents tell the record from the report | `bin/test tests/test_the_reviewers_report_reaches_the_record.py -q`, each case seen red first | 7bcf36a |

**One phase, not two.** The generator's default and the reviewer's write were
planned as separate phases and are one vertical slice: a default that reads a
path nothing fills delivers nothing, and a file nothing reads delivers
nothing either. Splitting them would have put a red case in a commit or an
untested commit in the branch, which is the choice that says the split was
wrong.

## Operational impact

None for a deployer. One for the review chain: a round run by a warden that
predates this change returns chat text and no file, and `round_record.py new`
then refuses with the conventional path named — which is the correct answer
and reads as a new failure. `--report <path>` is the way through, unchanged
from today.
