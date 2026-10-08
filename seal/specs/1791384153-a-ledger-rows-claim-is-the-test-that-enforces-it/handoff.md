# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — handoff

## State at the machine move (2026-10-08 evening) — read this first

- Draft PR #887. Built in five phases. The branch merged `release/v0.21.0` at ad447367 and cleared the release branch's 33 drifted rows (`overview.md` §*The release branch's integration drift, cleared here*). **Land this before #870 and #866.**
- Round 1 is closed at d5642a07: four fixed, one answered. Round 2 is recorded at da1a0cd3:
  - 🟡 1: a keyword-conditional or strict `xfail` reads as unconditional;
  - 🟡 2: a mark under an `if`, or a `pytestmark +=`, is not read.

  Its `Fix of a fix` reads `first`. One reopening remains, so the next fix pass is the run's last.
- **On hold by the owner's review** (`chore/834-…` → `seal/specs/1791382684-…/handoff.md` §*Review of the run*). The collection half, which reads a test file to predict whether pytest would collect it and whether it could fail, keeps finding new spellings. The direction to weigh is to observe #869's pytest recorder record instead. The test-row half does not predict and can stand apart. Do not spawn the fix pass until the owner decides.
- Write and close records with the installed 0.20.0 `round_record.py --root .`, not the tree's.

Written 2026-10-08 by the orchestrating session, for a session on another
machine. The whole run's state, the owner's batch and the starting notes are
in `seal/specs/1791382684-every-reader-and-record-is-inventoried/handoff.md`
on branch `chore/834-every-reader-and-record-is-inventoried`; read it first.

| | |
|---|---|
| Issue(s) | #836 |
| State | framed by `framer` on Fable 5.1; `routing.md` answered `automation`; no smith spawned; `plan.md` not approved |
| Owner's questions | Q1 for the owner (a bulk pass over released rows?), default (a). |
| Build order | Shares `evidence_check.py` with #867 and #870; build after #867. |

**Next act:** the owner's answers to every open row of the run, asked
together in one call; then fill `plan.md`'s `Approved <date> by <who>` line
and spawn smith on this branch. In a fresh worktree, run tests with
`bin/test <files>`; `uv run --frozen pytest` cannot start pytest there.
