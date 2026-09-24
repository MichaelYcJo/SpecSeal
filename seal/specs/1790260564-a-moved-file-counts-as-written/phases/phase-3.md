# 1790260564-a-moved-file-counts-as-written — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 21248da1 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#554: a local-mode declaration owns the range on its own branch.
`whole_range` decides local mode lazily, only for a declaration that would
have matched: real path under the real path of `<git-common-dir>/seal/specs/`,
compared after `os.path.normcase`. Local mode reads the sibling `routing.md`
through `hooks/routing.py#parse`, loaded by path, and asks `git merge-base
--is-ancestor <b> refs/heads/<Branch>`. Shared mode is unchanged. The
`whole_range` docstring and the `OWNER_DIR` comment are updated,
`docs/review-chain-spec.md` sentence 2 corrected in place with no fold
marker, rows E4, G5 and U1 re-read. O1 seen red at the base, O2 red against
an ownership test reduced to `True`, O1 run in a linked worktree or saying
why not. The spawn added: after the build, run `survivor-check` over the
branch's own range and answer every report.

## What this phase found

- **The frame holds**, with one addition it did not name: the `not yours`
  line's reason. In local mode *this range touches nothing in it* is true of
  every range, so it would send the reader to a diff that can never hold the
  file. The line keeps its shape and now names the test that refused it
  (*this range's tip is not on the branch its routing.md names*), pinned in
  O2 and O4, with the shared-mode reason pinned in the depth case. `spec.md`
  §*Data & interfaces* said no report line changes shape; the divergence is
  in `overview.md`.
- **Three more carriers said the same false thing.** `agents/smith.md`
  §Phases and `skills/code-review/orchestration.md` both say a range row
  *never reaches a range that touches nothing in* its own work item, and so
  does the module docstring's second-anchor paragraph. In local mode each is
  now false, so each carries a parenthesis on local mode (§12). The edit to
  `agents/smith.md` moved the `"## Phases"` hash that section's RIDER is
  stamped against; its four numbers were re-measured at the edited file —
  the line alone one invocation, with everything above it one,
  `_hides_a_commit` True — and the rider re-stamped with
  `rider_check.py --reverify --only agents/smith.md`.
- **O1 runs in both worktree shapes.** `git rev-parse --git-common-dir`
  answers `.git`, relative, in a main worktree and an absolute path in a
  linked one, and the case is parametrised over both; the relative arm is
  what caught a mutation that dropped the join onto `root`. A third arm
  spells `--exempt` through a symlink to the repository, because the macOS
  temporary directory is already a real path here and the `realpath` on the
  file was otherwise unpinned (§13). It skips where a symlink cannot be made.
- **Mutations, one at a time, the file restored from a copy after each:**
  ownership reduced to `True`, O2 red; `local_item` answering None, O1 main
  and linked red; the common directory not joined onto `root`, O1 main red;
  `abspath` for `realpath`, O1 symlinked red; an unreadable `routing.md`
  answering True, O4 missing red; an unparsed one answering True, O4
  no-branch red; the reason fixed to the shared text, O2 and both O4 red;
  the missing-reader guard removed, O5 red. O4 and O5 were added because the
  first four mutations left those lines unpinned.
- **A missing `hooks/routing.py` refuses (exit 2)** rather than answering
  *not mine*, the way a missing `unverified_check.py` already does in
  `reader()`: a broken install is unusable input, not a judgment.
- **The sweep over this branch's range is clean.**
  `survivor-check --range f7ac2a24..HEAD` at `21248da1`: exit 0, 350 files,
  68 removed sentences, `no removed wording is still standing`. The same
  from the base, `c52e8350..HEAD`. No `survivors.md` row was needed.
- **The date turned during this phase**, so its ledger notes read
  2026-09-25 where phases 1 and 2 read 2026-09-24.
- **Gate items** (`CONTRIBUTING.md` §*What a change to a gate must carry*):
  - *Test seen red:* O1 (main and linked) at `502952ce`, phase 2's tip,
    whose `whole_range` is the base's: exit 1 with `not yours`. O2 by the
    ownership-to-`True` mutation; O4 and O5 by theirs.
  - *Failure direction:* allows more — an exemption now applies where it
    was refused. It is bounded by the branch-ancestor test (O2), and a
    declaration it cannot place prints under `not yours`. A wrong allow
    costs a survivor excused on a reused branch name (`plan.md`'s failure
    scenario); a wrong deny costs the red run it cost before this change.
  - *Prompt budget:* zero. The sweep prints and exits.
  - *Platform:* real paths and `normcase` for macOS's `/private` temporary
    symlink and Windows drive-letter case; `--git-common-dir` joined onto
    `root` because it can be relative. O1 runs in a linked worktree. Only
    macOS was run here; the three-OS matrix in `test.yml` is the rest.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/review-chain-spec.md`'s *In local mode the owner is never in the range's diff, which is MichaelYcJo/SpecSeal#554, open.* | the corrected sentence in the same statement; ledger row O1 in `seal/ledger/1790260564-a-moved-file-counts-as-written.md` |
