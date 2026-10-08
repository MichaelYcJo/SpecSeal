# 1791384159-a-unit-the-extractor-cannot-bound-is-refused — handoff

## State at the machine move (2026-10-08 evening) — read this first

- Draft PR #889. Built in four phases at 8ca2b57a. The branch merged the release branch at fb86a834, so merge it again (now ad447367, or later) before any seal. The release branch's eight `agents/warden.md` drifted rows are cleared by #836's branch.
- Round 1 is recorded at 8b0d4d7a, not closed:
  - 🟡 1: the walk ignores the lexer's string and comment state, so #848's shape comes back after a regex or template;
  - 🟡 2: a comment at a YAML key's indent ends its items;
  - 🟡 3: two verdicts the changelog and the policy promise unchanged do change.
- **On hold by the owner's review** (`chore/834-…` → `seal/specs/1791382684-…/handoff.md` §*Review of the run*). A nine-family lexer is a new guessing reader, which is against 0.21.0's theme. The direction to weigh is to force a format: bound units only where a real parser exists, and require a quoted-line anchor elsewhere. Do not spawn the fix pass until the owner decides.
- Write and close records with the installed 0.20.0 `round_record.py --root .`, not the tree's.

Written 2026-10-08 by the orchestrating session, for a session on another
machine. The whole run's state, the owner's batch and the starting notes are
in `seal/specs/1791382684-every-reader-and-record-is-inventoried/handoff.md`
on branch `chore/834-every-reader-and-record-is-inventoried`; read it first.

| | |
|---|---|
| Issue(s) | #870, #848 |
| State | framed by `framer` on Fable 5.1; `routing.md` answered `automation`; no smith spawned; `plan.md` not approved |
| Owner's questions | None for a person. |
| Build order | Shares `evidence_check.py` with #836 and #867; build after #867. |

**Next act:** the owner's answers to every open row of the run, asked
together in one call; then fill `plan.md`'s `Approved <date> by <who>` line
and spawn smith on this branch. In a fresh worktree, run tests with
`bin/test <files>`; `uv run --frozen pytest` cannot start pytest there.
