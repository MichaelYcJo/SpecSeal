# 0.12.0 — where the cycle stands, for the session that picks it up

<!-- Written 2026-09-15 by the session that opened the cycle, at the moment it
ended. It is not part of the SDD file set and nothing reads it: it exists
because the next session starts with none of this session's context, and the
round records alone do not say which work items are still unopened.

Delete it at the release, with the branch it sits on. -->

The release branch is `release/v0.12.0`, cut from `main` at `a35a3ea1` and
pushed. Four work items were planned into it. Two exist, one is unopened, and
one cannot be opened yet.

| | Work item | Branch | Where it got to |
|---|---|---|---|
| 1 | the `Broad gate` row (#402, #401) | `fix/401-402-the-broad-gate-row-runs-unchecked-and-is-never-asked-for` | **done.** Pull request #412 open and ready, sealed at `3c1ef343` |
| 2 | the record chain (#404, #405, #406, #407, #408, #414) | `fix/404-405-406-407-408-414-the-record-chain-disagrees-with-itself-in-five-places` | **phases 1–6 of 7 committed**, pushed, no pull request yet |
| 3 | the ladder's rung is checked by nothing (#399) | — | **not opened** |
| 4 | #413, and two cells work item 1 left behind | — | **cannot be opened until #412 merges**, below |

## The one thing to read before touching anything

**The merge method is fixed per direction and is not a preference.**
`CLAUDE.md` and `docs/branch-and-release.md` carry the table. A feature branch
**squashes** into `release/v0.12.0`; the release branch reaches `main` as a
**3-way merge commit**. Squashing the second discards every commit the release
branch wrote, and the `Verified … at <sha>` stamps and every `Target SHA` in
every `round-N.md` point at those commits by SHA. Two rulesets make the wrong
button unavailable, so this is a thing to know rather than a thing to choose.

## Work item 2 — what phase 7 still needs

`plan.md`'s Phases table is the task list and there is no other. Status cells
1–6 carry their commits and 7 is empty, which is what "still to do" looks like
here.

- **Phase 7 — the work item's own records.** `changelog.md`,
  `seal/ledger/1789455558-….md`, and `overview.md` carrying the four corpus
  measurements. `seal/ledger/` is empty after the 0.11.5 fold, so this work
  item opens it again.

Q1 through Q6 in `questions.md` are all answered. Q3, Q4 and Q5 were measured
against the corpus during phases 1–3 and the numbers are in their rows; Q6 is a
sentence drafted in phase 4 for the round that reads it.

**The rule that costs attention:** `plan.md` §*How this branch avoids sawing
off the limb it sits on*. This branch repairs the machinery that writes and
reads its own round records. No phase may change `inherited_rows`, and phases
exercise the generator in throwaway clones through the existing `repo` fixture,
never against this work item's own `rounds/`.

After phase 7: open the draft pull request against `release/v0.12.0`, then the
review chain, then `sealer` once, then mark it ready.

## Work item 4 — why it cannot be opened yet, and what it carries

Both of its coordinates live in files that exist only on work item 1's branch.
Cut it from `release/v0.12.0` **after #412 has merged**, and it carries two
things:

- **#413** — `test_both_ampersand_cells_name_both_shells` asserts that both <!-- NAME NOT IN TREE: the case module lives on `fix/401-402-the-broad-gate-row-runs-unchecked-and-is-never-asked-for`, which this branch did not cut from; #413 travels with the fourth work item Q1 names. -->
  shell names appear in each `&` row and never which name does which, so either
  cell can be inverted with every case green. Measured: 18 passed under both
  swaps. Four lines, and the paste-ready assertions are in the issue.
- **Two cells in `seal/specs/1789445605-…/rounds/round-2.md`**, lines 39 and 40,
  which read `fixed at 6233b769 — . ` with a stray period. #414 removes the
  cause in work item 2; these two were already rendered. They misstate nothing,
  which is why they were not worth spending work item 1's seal on — one commit
  there would have bought the whole broad gate again.

## Decisions this session took, so they are not re-litigated

| | Decision | Why, in one line |
|---|---|---|
| Scope | all five of one round's deferred findings ship in 0.12.0, not three | #404, #405, #406, #407 and #408 are one round's deferred tail in one subsystem; the tracker had split them three ways |
| Version | 0.12.0, a minor | #399 adds a check that did not exist and #401 adds a bootstrap question — both visible to whoever runs the plugin |
| Work item 1, Q6 | a mid-line `&` stays legal with its cost stated, rather than being refused in code | it runs as the command it reads as and its exit code is that composition's, which is the position `;` already holds; refusing it needs `shlex`, whose misses and raises nobody budgeted |
| Work item 2, Q1 | work item 4 repairs the two stray-period cells | work item 1 is sealed, and a seal binds to a tree state |
| Work item 2, Q2 | the tracker fields were corrected, not the branch | #406, #408, #413 and #414 now read `release: 0.12.0`; #415 went to `backlog: gates & hooks` |
| Routing | every work item: `smith` builds, the review chain reviews, the pull request opens | answered by the owner in one batch before the first edit, for the whole cycle |

Three issues were opened by this session: **#413** and **#414** from work item
1's capped run, and **#415** for the pipe question its `questions.md` Q5 had
deferred to a person.

## Two things that cost this session time, stated so they cost less next time

**A broad gate run binds to a tree state, and an edit after it spends it.**
Work item 1 ran it three times. The first failed on one test file the gate
itself called `new`; the repair moved a document section's hash, so the second
failed on nine ledger rows anchored there; the third sealed. Nothing was wrong
with the procedure — but a document edit inside an anchored section is worth
re-reading the rows before running the gate rather than after.

**A verdict row with an empty `#` cell is refused by `round-record new`.** A
reviewer's report that writes confirmations and corrections without 🟢 or ⬜
has to be repaired by hand before the record will write. Say so in the spawn
prompt; this session did from round 2 onward and it did not recur.

## Phase 6 is committed

It was built, reverted when the session was told to stop at phase 5, then
rebuilt and committed at `1376409e` with its record at `a3e1475f`. Both
red-first mutations were re-run against the tree it shipped on rather than
reported from the earlier measurement.

The class is closed at five `re.sub` sites — four newly guarded and one that
already carried the guard, which is the house shape #407 says the author knew.
`phases/phase-6.md` holds the enumeration and both mutation messages.

One measurement in that record is about an **earlier** tree and says so: the
case passing green with a broken substitution and neither guard present was
measured at `703f25e5`, and re-running it here would mean deleting the very
assertions phase 6 exists to add.

**The revert cost more than it saved**, and it is worth carrying: a commit on a
branch that squashes into its release branch costs nothing, and an uncommitted
measurement is invisible to everyone. An agent told to stop should commit what
stands and say what it is.


## Phase 7 — two divergences are already waiting for `overview.md`

`overview.md` opens at the first divergence and it was not opened, because it
is phase 7's deliverable. Two rows are owed to it and both were found while
building phases 1–5:

- **`plan.md` §Operational impact overstates phase 2's break.** It says a table
  *edited or truncated since `new` wrote it* now exits 2. What shipped is
  narrower: a table that lost rows **and** names no row from round N at all. A
  table that lost some rows and kept one of round N's still passes — traded away
  on purpose by Q3's own rule, and the two corpus pairs that sit in that gap are
  named in `phases/phase-2.md`.
- **`spec.md` A7 cannot hold as written.** It asks for a 🟢 row quoting a 🔴
  *whose verdict is closed* to be silent and calls that red against the
  whole-row join. The join also requires the verdict to be open, so a closed
  verdict was already silent and no fixture of that shape can be red. What is
  red against the join is the same row reading `verified`. The built reading
  follows that, with a second case carrying the closed-verdict half as the
  silence it actually is.

The corpus measurements `overview.md` has to carry are already written in
`questions.md` Q3, Q4 and Q5 and in `phases/phase-2.md` and `phase-3.md`, with
their populations and dates. Copy them from there rather than re-deriving them.

**Phase 4 is a message split, not a predicate narrowing** — the set of refused
rows is unchanged, and two neighbouring cases say why it could not widen. Worth
knowing before reading the diff and concluding otherwise.
