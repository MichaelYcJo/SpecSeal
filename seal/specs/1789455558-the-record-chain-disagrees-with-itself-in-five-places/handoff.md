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
| 2 | the record chain (#404, #405, #406, #407, #408, #414) | `fix/404-405-406-407-408-414-the-record-chain-disagrees-with-itself-in-five-places` | **built, all seven phases**, pushed. No pull request, no review round, no broad gate |
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

## Work item 2 — the build is closed, and one thing blocks the seal

All seven Status cells in `plan.md` carry their commits. What has not happened
is everything after the build: no pull request, no review round, no broad gate.

**The next step is not the pull request. It is a decision.**
`bin/evidence-check --strict .` exits **2** on this branch, with seven anchors
DRIFTED, and the broad gate runs the ledger arm — so the gate will come back
NOT SEALED until this is resolved. Work item 1 met the same wall on two rows
and the run cost three broad-gate spends.

The seven are units this branch changed that `seal/ledger.md` already cites:
`close`, `seal`, `fix_table`, `reach_forward` and three test units. **The drift
is the mechanism firing correctly, not a defect.** Every one of the thirteen
rows citing them was re-read on 2026-09-15: twelve hold, and one did not — that
one is removed, below. There are two ways out and the build chose neither:

- **`bin/evidence-check --reverify .`** — one command, and what the branch did
  for work item 1. It refreshes the hashes and does **not** touch the `Checked`
  column, so the re-read it records is invisible; and it puts a multi-row edit
  to `seal/ledger.md` on a branch while others are in flight, which is the
  collision the fragment convention exists to prevent.
- **Leave it to the release**, which is what the build chose and wrote into
  `overview.md` §*Not verified* with the owner named. CI's own invocation is
  non-strict, where this is exit 1 and a printed warning. **The broad gate is
  not**, so the sealer cannot seal this branch as it stands.

Whoever takes this decides before spawning `sealer`, not after — a gate run is
spent by any edit that follows it.

**`seal/ledger.md` was touched, once, and on purpose.** The instruction the
build was given said it would not need to be, and that premise turned out
false: one row's claim ended *…and the case that pins it asserts the whole
output holds no bare `the seal`*, and that assertion is what #406 deleted. The
row is removed, nothing else in the file changed, and the fragment's fifth row
carries the superseding claim. `CLAUDE.md` §*a change writes fragments* states
this exception in as many words.

Q1 through Q6 in `questions.md` are all answered. Q3, Q4 and Q5 carry the
corpus measurements with their populations and dates; Q6 is a sentence drafted
in phase 4 for the round that reads it. `overview.md` carries four divergence
rows and `seal/ledger/` is reopened with six rows over 23 coordinates.

**One trap the build hit three times:** a record that names a unit the tree
lacks makes the evidence checker's records arm refuse it — and a refused record
takes the **non-strict** run to exit 2, which is the form CI runs. Naming
`test_both_ampersand_cells_name_both_shells` <!-- NAME NOT IN TREE: the fourth instance, written by the session that was documenting the other three. The case lives on `fix/401-402-…`, which this branch did not cut from. --> here, then in `overview.md`, then
in `phases/phase-7.md`, refused all three; each line carries `NAME NOT IN TREE`
now. That case module lives on work item 1's branch, which this one was not cut
from.

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
