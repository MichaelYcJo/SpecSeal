# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | a2ea14ec |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

As planned, the switch at git: the three switch rows as refusals at
`prepared` or as a `post-checkout` undo per M1 (S10); `[shared-tree-ok]` and
`-c specseal.answer=shared-tree-ok`; the dirty-tree row as a refusal naming
`-c specseal.answer=carry-changes`; P4's fallback wired below the floor
through `hooks/cmdline_base.py` as it stands (S11); the guard's Bash walk
deleted above the floor.

As answered by the owner on 2026-10-01 (`questions.md` P4, option 1): **the
switch arm keeps the frozen 0.16.0 reading on every git, permanently and
byte-pinned, with no rule added.**

## What this phase found

- **Option 1 leaves nothing of the planned switch work to build.** The plan
  had a switch arm at git. With none, the arm stays exactly where 0.16.0 had
  it, so none of the following was done, each for the same reason:
  - no `-c specseal.answer=shared-tree-ok` and no `carry-changes`;
  - no floor wiring, because M1 named no floor;
  - the guard's Bash walk is not deleted.
  `[shared-tree-ok]` stays the switch arm's own bare word, read from the
  command by the guard's `has_token` as before, and `hooks/answers.py`
  deliberately does not carry it.
- **What the phase does deliver is the pin.**
  `tests/test_the_frozen_reading_never_grows.py` holds three things:
  - the bytes of `hooks/cmdline_base.py` below its rider equal
    `86256492:hooks/cmdline.py` less its shebang line, compared by sha256
    unconditionally and against `git show 86256492` wherever the commit is
    reachable (CI checks out with `fetch-depth: 0`);
  - only `hooks/worktree-guard.py` and `hooks/worktree_consent.py` import
    it;
  - a switch in a clone where git decides commits and creations is still
    the guard's (S10).
  Each was seen red under a mutant: one more line below the rider, a third
  importer, and the guard standing aside for a switch.
- **The rider said the file would be deleted by #692, which became false.**
  It now says where the file stays and why: the switch arm on every git,
  and the creation arm and consent writer in a foreign clone (P5). It also
  points at the pin. The stamp was re-dated against the same unit hash,
  `walk_directories@672f1550`, which this phase did not move.
- **`tests/test_what_the_reader_understands.py#test_the_guard_reads_the_same_answer`
  was kept as it was**, not retargeted to bytes as the plan said. It
  asserts what the frozen reader answers, which is still true and still
  wanted. The byte pin is the new module beside it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the rider's "deleting this module … is part of #692" | the rider's new paragraph, and `questions.md` P4's answer |
