# 1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 1b1a1ed2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 1: the notice-only arm in
`skills/code-review/scripts/chain_check.py` for S1–S8 and S10, homed beside
`pact_notices` and called once per `through the review chain` declaration
after the record walk; the section of `docs/the-record-layout.md` that owns
the rule and that the notice names, ending `Enforced by:` the arm and its
cases; and the module docstring's *What it reads* row. One question per work
item over first-parent, non-merge commits from round 1's `Target SHA` to
HEAD, a behaviour path being any path outside `seal/` and outside a `tests`
directory, silent in the states `spec.md` lists, and the exit status never
moved. Every new case seen red before the arm, or with its condition
reverted.

## What this phase found

**The frame holds.** Every coordinate `spec.md` and `plan.md` name was opened
before the first edit: `chain_check.py#pact_notices` is the notices-only
shape, `#fix_range`/`FIX_RANGE_RE`/`#target_shas`/`#resolves_to`/`#field`/
`#table_rows`/`#tracked_files` are reused as named, and
`round_record.py#run_check` runs `chain_check.main` in process with
`--worktree`, so the close and the seal reach the arm with no change there.

**Q3, answered by the work.** The notice is one line per work item, written
against the fragment's path. It names EVERY late commit as `` `<short>`
(<where>: <paths>) `` and lists at most three behaviour paths per commit
before counting the rest (`PATHS_NAMED`). `<where>` takes three values, one
more than `spec.md` named: `round N's fix range`, `after the last round`, and
`outside every round's fix range` for a commit between two ranges — a
commit after round 1's range and before round 2's record is neither of the
first two, and calling it either would be false. The sentence says the
release gathers the fragment *as it stands*, that *nothing is owed* where it
still says what ships, and names `docs/the-record-layout.md` §*A commit after
the build brings its changelog fragment along*. The module is
`tests/test_a_fragment_left_behind_is_named.py`.

**One silent state beyond `spec.md`'s list.** A round 1 `Target SHA` that
resolves and that HEAD does not descend from — a rebase leaves the old commit
answering `rev-parse` — makes `<target>..HEAD` read the build itself as late.
The arm is silent there too (`is_ancestor`), and the case for it keeps the
build in two commits so that the walk without the guard has something to name.

**An absent `round-1.md` needs no test of its own.** `target_shas` of a
record git does not carry is empty, so it lands on the unresolvable-target
state; the explicit membership test was removed after a mutation showed
nothing could tell it from that one.

**Which of two `Target SHA` values is the build's end.** The first:
`templates/sdd-round.md` lets the row name a second for a HEAD that moved
while the round ran, and that commit is after the build. A case pins it.

**`--worktree` still reads the fragment at HEAD.** The walk is over commits,
so a fragment edited and not yet committed is named until the commit that
brings it along — which is the commit the rule asks for. Written in the
arm's docstring rather than given a branch of its own.

**The `Enforced by:` line stands outside a fold statement.** The section
carries no `<!-- specs/… -->` marker, because it is not a fold, so
`fold-check` does not read the line; its targets were checked to resolve by
hand. `docs/the-record-layout.md` is not in `tests/test_docs_line_wrap.py`'s
covered set; the section is wrapped at 80 anyway.

**Red, per case** (contract §15). All eighteen first cases failed against
the tree before the arm existed (`AttributeError`: no `fragment_left_behind`,
no `FRAGMENT_RULE`). That proves the arm's absence and nothing about each
condition, so every guard, label and constant was also broken one at a time
with `mutation-check` against the case that covers it — 25 mutations. 24
were red at once. The ancestor guard SURVIVED: the off-branch case wrote the
fragment and the hook in one build commit, so the wrong walk had nothing to
name. The case now ends the build on a commit of its own, and the guard's
mutation is red (`1b1a1ed2`).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
