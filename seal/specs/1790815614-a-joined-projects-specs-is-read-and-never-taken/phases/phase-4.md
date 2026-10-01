# 1790815614-a-joined-projects-specs-is-read-and-never-taken — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 7f13eb1c |
| Ran by | specseal:smith on claude-opus-5-5 — set by the orchestrator, which spawned it with that model and did not name it in the prompt |

## What this phase was asked

`unverified_check.py#overviews` prunes reference roots from a directory walk
and still reads an explicitly named file. One fixture — a team's
`specs/1788000001-team-thing/` with `spec.md`, a malformed `overview.md` and
`design.md`, beside a `seal/specs/<id>/` — handed to `settle --retire`,
`evidence-check`, `correction-check`, `chain_check.py` and `unverified-check`,
each asserted to leave it on disk, unread as a record, with its own verdict
unchanged. The case enumerates the shipped checks by name. D2 red against the
old walk; D3's pins red by widening the constant each rests on. Q4 measured.

## What this phase found

**The frame did not hold as drawn here, and the answer changes C1.** Thirty-
eight cases in `tests/test_unverified_rows_close.py` walk from the root of a
git repository whose fixture puts its work item under a top-level
`specs/<id>/` — the 0.3.x spelling, which `unverified_check.py` and
`survivor_check.py` still read as the plugin's records on purpose
(`a_gathered_fragment`'s two spellings, `settled_root`, `FOLD_MARKER`). Under
the default as phase 3 shipped it, every one of them would have had its work
item pruned as a reference root. The spec defines a reference root against
the plugin's root, and a repository with no `seal/` at either place has none
to be outside of: it has not opted in, and the one layout the plugin read
without a root is 0.3.x, whose `specs/` was its own. So
`hooks/config.py#reference_roots("")` answers `()`, no reference root, where
phase 3 had it answer the default. Both checks read that one answer; D1's
probes now carry a `seal/config.md` with no `Reference specs` row, and gained
a rootless arm that keeps the team document in the sweep. `overview.md`
records the divergence.

**The base must be read by the walk's rule.** `overviews_at`'s own comment
says why: an overview the walk leaves out and the base listing keeps is
reported deleted on every run. Both use `references_at`, and a prefix the
person named inside a reference root is honoured on both sides.

**A fallback, not an exit 2.** `unverified_check.py` loaded no sibling
before this phase, so a copy taken alone worked; a refusal would have been
its first break. With no `hooks/` beside it, it prunes nothing, which reads
more and never less. That is why it is not added to
`tests/test_a_script_copied_alone_exits_2.py`.

**Three units had nothing behind them and were removed before the
mutation run**: a `here is None` guard and a `rel is not None` guard (every
directory the walk meets is under `top`), and a cache with no observable
effect. The `top is None` guard survived its first mutation — `home_at(None)`
already answers `""` — so a case now pins its contract: outside a
repository nothing about reference roots is read. Its value on this
platform is that contract; on Windows it also keeps a cross-volume
`relpath` from being asked, which nothing here can execute.

**D3 is two layers.** The static layer names every `bin/` command with
what keeps it off a team's `specs/` and holds each pinned check's constant
under `seal/`; widening any of the four, or adding a command to `bin/`,
turns it red. The behavioural layer runs five checks over the repository
with and without a planted team directory and compares exit codes and output
with paths and SHAs written out. Read by hand, each check really reads
something there — `correction-check` needed the fixture's second commit to
arrive by a merge, or it stopped before reading.

**Q4.** `README.md`, `README.ko.md` and `skills/verify/SKILL.md` tell a
person to run `unverified-check .`, so the pruned walk is a documented one.
None of the three is false after the change. The module docstring's
`unverified-check specs/` is reworded to `seal/specs/`.

**One instruction broken in this phase.** A scratch JSON of mutation
patterns was rewritten once by `python - <<'PY'` instead of `Write`. It was
a file in the session's scratch directory, nothing in the tree changed, and
the gate did not stop; the spawn prompt forbids it all the same, and the
hand-back says so.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `reference_roots("")` answering the default for a repository with no root | `hooks/config.py#reference_roots`'s docstring and `templates/config.md` §*Reference specs*' value table; row C1 of `seal/ledger/1790815614-….md`, corrected in place |
