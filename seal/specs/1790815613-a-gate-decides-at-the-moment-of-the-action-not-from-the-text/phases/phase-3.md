# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 4388e73d |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

Build the commit gate at the commit, against real git. The judgment moves
from `hooks/commit-review-gate.py#judge` into `hooks/gate.py`. `pre-commit`
decides in the worktree git commits into. It reads the session from the
environment and then the lease (W3), and gives P2's answer when there is
neither. It reads the press through `automation_answered`, the declaration
through `routing.declared`, both arms, and `-c specseal.waive=` (M11). The
refusal texts are W1 and W2, with the old spelling named where P3 keeps it.
`reference-transaction` is the `--no-verify` backstop, mark-based on the
criterion phase 1 measured (the owner's answer of 2026-10-01). The
implementer notice moves to `post-commit`. The plan also said to remove
`commit-review-gate.py` from `GROUPS["pre-bash"]` in this same phase. S1–S6,
S9.

## What this phase found

- **P5: the PreToolUse gate stays, and stands aside wherever git
  decides.** P1(a) keeps 0.16.0's behaviour for a foreign clone, and for the
  commit arm that behaviour is `commit-review-gate.py` reading through
  `cmdline.py`. So the plan's removal from `pre-bash` was not done.
  `questions.md` P5 holds the trade, the default and the alternative.
  - **The rule as built:** a target whose clone carries this plugin's stubs
    (`githooks.decides`) is left to git. A target the reader could not
    place is left to git when the session's own clone is git-decided. The
    two never both judge one clone.
  - **What it costs:** a commit through an unreadable construct into a clone
    that carries no stubs, made from a git-decided session, is judged by
    nobody. That is a known limit, and phase 6 writes it into
    `docs/commit-review-gate-spec.md`.
- **One judgment, two renderings.** `gate.arms_missing` says which arms
  stand, and both the git hooks and the fallback ask it. The fallback keeps
  0.16.0's texts and its `deny`-then-`ask` budget, while the hooks have
  their own texts. Its whole test suite (41 modules, 2,568 cases) stayed
  green on the change, in fixture clones that carry no stubs.
- **W1, W2.** A refusal opens with `SpecSeal stopped this commit; nothing
  was committed.`, gives each arm's state, then either the automation text
  or the AskUserQuestion instruction with options that run (git-native
  first, P3's old spelling second). It closes with `Re-issuing this commit
  unchanged meets this same refusal.` The second attempt meets the same
  text (W2). There is no once-per-session budget, because there is no `ask`
  left for it to fall to.
  - **Changed from 0.16.0's automation text:** its two text-specific ways on
    are gone — "write the path out" and "edit through `Edit`", which
    steered around a reader the hook does not have.
- **The mark.** `pre-commit` leaves `<git-dir>/specseal-judged/<sha1>`,
  keyed by the old HEAD, the tree it computes with `git write-tree` over
  `GIT_INDEX_FILE`, and `GIT_AUTHOR_DATE`. `reference-transaction` takes it.
  A mark left by a commit that aborted after `pre-commit` is pruned after a
  day. An update with no mark is judged again with the same arms, and the
  paths come from `git diff old new` (`diff-tree --root` for a root commit).
- **A detached HEAD moves no branch,** so the backstop reads the `HEAD` line
  when `HEAD` is detached. On 2.34–2.43 a branch commit sends both lines, so
  each `(old, new)` pair is judged once.
- **M6's two `env -i` rows were probe artifacts, now shown.**
  `test_s9_an_emptied_environment_is_still_judged_through_the_lease` runs
  `env -i git commit` under a process named `claude` holding a lease, and the
  commit is refused. S2 replays the commit corpora the way the harness runs
  a call: the variable exported, a lease in every clone, and the command in
  a shell below a `claude` process. 140 commands commit into an undeclared
  repository without the hooks, and none of them lands with the hooks. 62
  commit nowhere undeclared and are skipped.
- **Three things only trying showed.**
  - macOS kills a copied system binary on launch (exit 137), so the fake
    `claude` is a symlink to bash, which `ps` reports by the symlink's path.
  - A fork of a shell named `claude` is named `claude` too, so the corpus
    runs in a separate shell below it.
  - The edit hook's formatter removes an import that is unused at the
    moment it is added, which left the fallback raising `NameError` on
    every target. `dispatch.py` turns a raising gate into silence, and
    `test_a_foreign_clone_keeps_the_text_reading` is what caught it. Every
    import is now added with its use.
- **`GIT_DIR` is not exported to these hooks** (M4), so every reading goes
  through `git rev-parse` in the hook's working directory.
- **Mutation testing: 45 mutants, 44 red.** The one survivor is
  `commitgate._context`'s opt-in check. It is equivalent: `arms_missing`
  finds nothing in a clone that does not opt in, so the early exit only
  saves the lease walk.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/commit-review-gate.py`'s inline arm conditions | `hooks/gate.py#arms_missing`, which the gate now calls |
| `hooks/implementer-notice.py#main`'s body | `notify`, called by `post-commit` and by `main` for a clone git does not decide |
