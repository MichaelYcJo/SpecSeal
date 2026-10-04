# a waiver inside a here-document body is data — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Decided from the tree, so nobody reopens them

Issue #773 left these open, and the repository answered each one. The grounds
are in `spec.md` and in `plan.md` §*Alternatives considered*.

- **Which reader decides what a body is.** The two the gate already has:
  `hooks/one_heredoc.py#reduce` where it matches, else
  `hooks/cmdline.py#drop_heredoc_bodies`. No new tokenizer (alternatives A, C
  and E in `plan.md`).
- **Whether a body a shell runs keeps its waiver.** It does not
  (`spec.md` case 4, alternative C). Telling a shell-fed body from a data body
  needs a reader that pairs each body with its consumer, which the tree does
  not have. The cost is one stop, and the stop names its way on.
- **Whether `hooks/tokens.py#given` is in scope.** It is (§12). Where git's
  hooks judge the commit, it is the only consent read.
- **Whether the new read may honour a token the base did not.** It may not.
  The read is ANDed with the base read, by construction (alternative F).
- **Whether the policy sentence "the scan for a waiver token still sees the
  command as written" forbids the change.** It does not. The only reason the
  tree gives for it covers comments, and comments stay read. The owner put
  #773 in milestone 54 with this fix stated, and this work amends the sentence
  in the same commit as the fix.
- **#773's second checkbox.** #769 already did it: at `94d7b2e0`, `main`'s
  comment states which way each raw-text read runs. This work rewrites that
  comment again only because it names #773 as open.

## The residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does the worktree guard's consent read, `hooks/worktree-guard.py#has_token` (`[worktree-ok]`, `[shared-tree-ok]`), join this item? It reads here-document bodies the same way, and a `[shared-tree-ok]` token in a body would turn that guard off. The tree cannot answer this, because it is a question of what this release's work items cover: the gate is a different one, the file belongs to sibling item D, and the owner chose the items of milestone 54 | a person (the repository owner) | (a) Join: the same shared function, one more read, and the two branches meet in `hooks/worktree-guard.py`. (b) A new issue: this item stays on the commit gate, and the guard's read is filed with this frame's §*The class* as its evidence | (b). The orchestrator files the issue, and `overview.md`'s *Not done* names it | ⬜ |
| Q2 | Does an existing case rely on a waiver token inside a body being honoured? Eight modules hold both a heredoc and a waiver token (`plan.md` phase 1 lists them). Reading cannot tell which of their cases put the token inside a body | a measurement: phase 1 runs those eight modules after the fix | A case whose token sits inside a body moves to the new verdict, with `spec.md`'s case number in its docstring. A case whose token sits outside every body and that turns red is a regression and goes back to the fix | No such case expected. Phase 1 records what the run showed | ⬜ |
| Q3 | Does `drop_heredoc_bodies` keep every documented waiver spelling? That covers the no-op in front, the trailing comment, and the apostrophe cases beside the token in `tests/test_the_waiver_can_be_typed.py`. Reading `_heredoc_split` says comments are copied through, but only a run settles it | a measurement: S3 and that module, run after the fix | Kept: nothing to do. Lost: the AND does not help here, because it can only refuse, so the function has to change before phase 1 closes | Kept | ⬜ |
| Q4 | The shared function's name, and whether the commit gate imports it from `hooks/tokens.py` or `has_marker` reaches it through `tokens` | the work | Either option builds the same thing | `hooks/tokens.py`, named by the builder | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

Q1 blocks nothing. Its default leaves this item's code the same under either
answer.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
