# 1789034970-the-contract-is-settled-against-the-agents-that-exist — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `94a2451` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

## What this phase was asked

`plan.md`'s row 2. §7 widened so that the rule is about what a probe leaves
rather than about files. The `test_tmp_*` file rule stays — it is what the
reviewer who left a worktree did follow. The shapes are **not** enumerated:
that alternative was weighed in the question batch and refused, and the reason
goes into the section in one clause, because the next reader will reach for a
list. The story goes in as the sections around it carry theirs.

## What this phase found

**The primary source and the frame disagree by one word, and the source is
right.** `spec.md` and `plan.md` both say the worktree surfaced when
`git switch` refused a branch *it still held*. #120's comment of 2026-09-10
says *when `git switch` refused a branch **another worktree** already held*.
The section is written from the comment: the stray worktree is what made the
later `git switch` fail, but the branch it held was a different one, and *it
still held* invites a reader to look for the same branch twice. Read
2026-09-10 from `gh issue view 120`.

**The §7 heading was left alone deliberately, and the reason is a ledger
anchor.** `seal/ledger.md:738` (row L7) anchors on
``skills/agent-contract/SKILL.md#"## §7 A probe is named `test_tmp_*`, one
file, run once, deleted"``. A heading is the major level of a content anchor,
so rewording it does not drift the row — it BREAKS it, and this repository's
rule is that a row whose anchor a change removes is removed rather than
re-pointed. The widened rule loses nothing by living in the body: the heading
still states the file form, which is still the rule for the common case, and
row L7's own claim (*the probe rules and the git-from-Python rule are contract
§7 and §8*) stays true. The body change drifts the row's hash, which is a
re-read and `evidence-check --reverify` — phase 3's work, with the other
anchors this branch moves.

**What the widened sentence costs, stated rather than left to be found.** It
names no mechanism, so nothing in the tree can check that a probe cleaned up
after itself; #180's objection stands and was accepted in the question batch.
What is bought is that the sentence holds for a leaving nobody has met.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — §7's existing two paragraphs are both kept word for word; this phase only inserts | none |
