# 1791384155-a-round-record-cell-has-one-reader — handoff

## State at the machine move (2026-10-08 evening) — read this first

- No PR yet. The branch merged `release/v0.21.0` at ad447367 before the build, so it holds #860, #837, #869 and #867. Merge again before any seal; #836's branch clears the release branch's own 33 drifted rows.
- Phases 1–4 are closed, with Status commits d9c71475, 984e45c8, ae628547 and 4cdccc2b.
- **Phase 5 was stopped mid-edit by the machine move.** The smith was replacing the two per-record readers with the shared facts reader and the walks (`record_facts`, `floor_walks`, `cut_runs` in `chain_check.py`). Its uncommitted edits are committed as-is in the `wip:` commit on top: `chain_check.py`, `round_record.py`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` and the ledger fragment. **That commit is unverified and may be red.** Phase 6 (the rest of J5) and phase 7 (the closing) are not started.
- Next: a fresh smith opens `git show HEAD`, finishes phase 5 or reverts the wip and redoes it, then builds phases 6 and 7. After that comes the draft PR and round 1.
- **The owner's review applies here too** (`chore/834-…` → `seal/specs/1791382684-…/handoff.md` §*Review of the run*). One reader per round-record cell is consolidation, not prediction, so it keeps to the theme. Check each phase against "observe, force a format, or delete" before building on it.
- Write and close records with the installed 0.20.0 `round_record.py --root .`, not the tree's. Every smith prompt names the full-name fragment, the eight guard modules, `survivor-check` and `correction-check`.

Written 2026-10-08 by the orchestrating session, for a session on another
machine. The whole run's state, the owner's batch and the starting notes are
in `seal/specs/1791382684-every-reader-and-record-is-inventoried/handoff.md`
on branch `chore/834-every-reader-and-record-is-inventoried`; read it first.

| | |
|---|---|
| Issue(s) | #866 |
| State | framed by `framer` on Fable 5.1; `routing.md` answered `automation`; no smith spawned; `plan.md` not approved |
| Owner's questions | None for a person. |
| Build order | Shares `round_record.py`/`chain_check.py` with #837 and #860, and `broad_gate.py` with #869; build after #837 and #860. Its frame counts 172 released ledger rows on the units it edits. |

**Next act:** the owner's answers to every open row of the run, asked
together in one call; then fill `plan.md`'s `Approved <date> by <who>` line
and spawn smith on this branch. In a fresh worktree, run tests with
`bin/test <files>`; `uv run --frozen pytest` cannot start pytest there.
