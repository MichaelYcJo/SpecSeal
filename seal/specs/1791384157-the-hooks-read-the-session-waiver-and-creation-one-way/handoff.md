# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — handoff

## State at the machine move (2026-10-08 evening) — read this first

- Draft PR #881, labelled `chain: reframed`. Rounds 1–3 stopped on a second fix of a fix in the brace rule, and the framer reframed it at 09446696. The redesign was built at df73a69c.
- Redesign rounds 4 and 5 are closed; round 5 closed at 11b6ed14. The brace test now reads a segment's raw text with quoted spans neutralised and errs toward stopping. Its over-stop is 42 of 33,287 recorded pairs, one of them git.
- **The next record is round 6, the verifying round that ends this run.**
- `questions.md` P1, the wide rule and its over-stop, is built on its default (yes). The owner has not answered it.
- **On hold by the owner's review** (`chore/834-…` → `seal/specs/1791382684-…/handoff.md` §*Review of the run*). The rule still imitates bash. The direction to weigh is to observe the act instead of predicting the command: git's `reference-transaction` hook sees HEAD move whatever spelled it, which is #692's conclusion. Do not spawn round 6 until the owner decides between finishing this chain and reframing it.
- Before any seal, merge the release branch in (it has moved since the branch last merged it).
- Write and close records with the installed 0.20.0 `round_record.py --root .`, not the tree's.

Written 2026-10-08 by the orchestrating session, for a session on another
machine. The whole run's state, the owner's batch and the starting notes are
in `seal/specs/1791382684-every-reader-and-record-is-inventoried/handoff.md`
on branch `chore/834-every-reader-and-record-is-inventoried`; read it first.

| | |
|---|---|
| Issue(s) | #868, #856 |
| State | framed by `framer` on Fable 5.1; `routing.md` answered `automation`; no smith spawned; `plan.md` not approved |
| Owner's questions | None in `questions.md`, but the frame answered #856 itself with (c) — a brace expansion stops the guard — where #856 had asked a person; confirm with the owner before phase 3. |
| Build order | Independent of the other chains. |

**Next act:** the owner's answers to every open row of the run, asked
together in one call; then fill `plan.md`'s `Approved <date> by <who>` line
and spawn smith on this branch. In a fresh worktree, run tests with
`bin/test <files>`; `uv run --frozen pytest` cannot start pytest there.
