# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 13a57d2 |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build the last phase: `docs/worktree-guard-spec.md`, the module docstring,
`pr-notes.md` carrying the four answers `CONTRIBUTING.md` requires so the
orchestrator can lift them into the pull request body, the changelog and ledger
fragments, and the closing memo. Fragments, never the shared files. A ledger row
is a content anchor — `path#major@hash`, never a line number and never a commit
SHA.

## What this phase found

**`docs/worktree-guard-spec.md` is the authority, so it gets the whole argument
and the hook docstring gets a pointer.** Its own opening says a hook change that
diverges from it changes one of them knowingly. The new §*Creation consent*
carries the token-versus-record table, the four decisions from `questions.md`,
and the two bounds — why the allow covers only a creation-only command, why the
Agent path is silent. §*Choice sites* gains one paragraph saying which record is
which, because the two now sit one directory apart under the same git directory
and the difference is what keeps them from being read as one.

**`hooks/dispatch.py#GROUPS` drifted a ledger row this branch did not write, and
that is the case `CONTRIBUTING.md` §House rules answers.** The claim still holds
and it was re-read, so `bin/evidence-check --reverify .` recomputed the hash
(`b3d45306 -> a5e67d2c`) rather than the row being removed or re-pointed. That
is an edit to `seal/ledger.md` on a branch that must not **append** to it, which
is the distinction the rule draws and the two documents used to disagree on.

**A fragment's rows have to carry hashes, and `--reverify` does not add
them.** It rewrites the hash a row already has; a row written without one is not
read at all, and the fragment reported `0 ok` with nothing wrong-looking on
screen. The stamps were computed with the checker's own `resolve_unit` and
`content_hash` rather than by hand, so the fragment agrees with the reader that
will judge it.

**The records arm caught a stale name in this work item's own `spec.md`.** An
acceptance row cited `test_consent_follows_the_clone_not_the_worktree`, and the
case that got written is `test_the_record_follows_the_clone_not_the_worktree` —
the scenario had moved from *the guard allows* to *the record lands under the
common directory* while the plan was being built, and the name moved with it.
Nothing but that check would have found it: the suite is green either way.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
