# 1789296200-the-record-before-the-fix-sequence-has-no-arm — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | <this commit> |
| Ran by | specseal:smith on claude-opus-5[1m] — the spawn prompt named no model; the segment's own harness line is the source |

## What this phase was asked

Take the measurement that sets phase 2's verdict, against a criterion written
before the number: over every `rounds/round-N.md` under `seal/specs/`, compare
the record's `Target SHA` against its adding commit's first parent, and count
how often they differ in runs nobody has called wrong. **0 or 1 differing
record → phase 2 refuses. 2 or more → phase 2 prints and continues.** Write the
number and the verdict into `overview.md`, naming the differing records
individually so a reader can open each. Do not renegotiate the criterion after
seeing the count.

## What this phase found

**The verdict: 40 differing records out of 152 measurable ones. Phase 2 prints
and continues; it refuses nothing.** The criterion's threshold is 2, and the
number is twenty times it.

Three things were learned taking it, and the first changed where the
measurement had to be taken at all.

### `main` cannot answer this question, and the plan assumed it could

`plan.md` phase 1 says *over every `rounds/round-N.md` under `seal/specs/`*,
which reads as the tree this branch is standing in. Run there, it answers
nothing: of the 328 records git carries at HEAD, **0** have a `Target SHA` that
equals their adding commit's first parent, and 221 have a `Target SHA` that is
not even an ancestor of their adding commit.

The cause is `CLAUDE.md`'s own merge table. A feature branch **squashes** into
its release branch, so on `main` every round record of a work item arrives in
one commit and the commit the reviewer read was discarded with the branch it
sat on. The parent of that squash commit is the release branch's previous
state, which was never HEAD at any `new`. Measuring it measures the release
process.

This is the same fact `chain_check.added_on_branch` is built around — it asks
`<base>..HEAD` rather than the whole history — and it means the question is
answerable **only inside a live branch**.

### Where the moment still exists

`refs/remotes/pull/N/head` — one ref per pull request ever opened — holds every
feature branch in its pre-squash form, and the local feature branches hold the
rest. Those are the trees `new` actually ran against. Over 102 such refs:

| | count |
|---|---|
| distinct (record, adding commit) pairs | 310 |
| excluded — the adding commit adds more than one record | 158 |
| excluded — unreadable | 0 |
| **counted** — one record, one commit | **152** |
| of those, `same` — HEAD was the `Target SHA` | 112 |
| of those, **`differ`** | **40** |

The exclusion is the second thing worth writing down. A commit that adds more
than one round record is not a `new` run: `new` writes one record and the
orchestrator commits it. The 158 excluded pairs are this repository's two bulk
moves — the `specs/` → `seal/specs/` migration of #90 above all, which adds 37
records in one commit whose first parent is a migration branch's previous
state. Counting them would have produced a far larger number for a reason that
has nothing to do with the workflow.

**The bias runs one way and is stated rather than hidden.** A record `new`
wrote but the orchestrator committed one commit later — behind an unrelated
commit — reads as `differ` here while HEAD at `new` was in fact the target. So
152/40 over-counts `differ` and never under-counts it. It does not matter at
this magnitude: the criterion's threshold is 2.

### The differing records are innocuous, which is the finding

Two recent ones were opened by hand rather than counted:

- `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/rounds/round-1.md`
  — `Target SHA` `5ce162e`, added by `a0f0e9a`, whose parent is `b46ff77`. The
  one commit between them is `b46ff77 docs: round 1's paragraph is recorded
  before the round runs`.
- `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/rounds/round-2.md`
  — `Target SHA` `ab069b1`, added by `99005ba`, whose parent is `ff22736`. The
  two commits between are `3b1eb6a docs: round 2's paragraph …` and `ff22736
  docs: the handoff for the session that takes 0.11.1 from here`.

Neither is a fix pass that ran early. Both are the round's own paperwork
landing between the review and the record — which is exactly the failure
scenario `plan.md` predicted for the refusal shape: *every round's `new` refuses
because something innocuous committed during the review, the orchestrator learns
the flag, and a genuinely late record arrives carrying a reason nobody read.*
The measurement says that scenario is not a risk, it is the common case, at 26%
of correct runs.

**So the difference between HEAD and the target is evidence and not a verdict.**
`new` is the only place it can be said while anybody can still act, so it is
still said — but the orchestrator reads what lies between and judges, because
`new` cannot tell a fix commit from a round paragraph and the numbers say it
would be wrong about one run in four.

### What this changes downstream

- **Phase 2 prints; it does not refuse.** `plan.md`'s fallback row — *Print a
  line, refuse nothing* — is what gets built, and `spec.md` A2's word *refuses*
  is overturned by the clause directly under that table: *A2's verdict — refuse,
  or print and continue — is set by phase 1's measurement, not by this table.*
- **Phase 3's flag stops being an escape from a refusal.** With nothing to
  escape, it is the way the reason reaches the record, which is what phase 4
  reads. Q2 authorised phases 3 and 4 on their own merits — a record that says
  why it was written late passes the pull request — and that answer does not
  depend on `new` refusing anything.
- **The empty-reason refusal of A4 stands.** It is not a gate on the run; it is
  a gate on the flag, and a flag carrying nothing writes a cell nobody can read.
- **Phase 2's message must name the commits between**, because the orchestrator
  is now the party that decides. A count alone would not let anybody tell
  `b46ff77 docs: round 1's paragraph` from a fix commit.

The measurement script is not committed: it is a probe under
`agent-contract` §7, and its inputs — `refs/remotes/pull/*` — exist only in a
clone that has fetched them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
