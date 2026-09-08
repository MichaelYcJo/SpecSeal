# Round 2 — fix pass

Fix commits `ad3ee1b..54cea1f`, on
`fix/225-151-local-mode-from-first-setup-to-the-gate` at target `646cbcf`.

Every measurement the report handed over was re-derived here rather than
accepted, and the two reds were seen first: the squash onto `2138c98` for 9,
and the four-state `git` count for 11. One of the report's numbers did not
reproduce and is named below.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 9 | fixed | 064330b |
| 10 | answered | corrected at 54cea1f |
| 11 | fixed | ad3ee1b, and the document half corrected at 54cea1f |
| 12 | answered | corrected at 54cea1f |

10 and 12 are located under `seal/ledger.md`, `seal/ledger/` and
`seal/specs/`, which `docs/review-chain-spec.md` §*A finding located in a
record is a correction, not a round* closes `answered — corrected at <sha>`.
11 is located in a record **and** in `hooks/mode-gate.py`, and the code half
is a fix.

## What each one did

**9** — the rider stamp names `2138c98`, a commit on `release/v0.9.1`, where
`other_worktrees` is identical to this tree's once comment lines are stripped
(executed: an `ast` comparison of the two spans). `2138c98` is an ancestor of
HEAD and survives the squash, because the squash is onto it.

Red first, executed: a `--no-local` clone, `git merge --squash` of the branch
onto `2138c98`, then the one case. Exit 0 before the squash and exit 1 after
— *rider stamped a3bea92, which is not an ancestor of HEAD*. Both states exit
0 after the fix.

**The form is the old one, and it is provisional.** The round's own note says
`at <sha>` will be wrong again when
`fix/239-a-stamp-names-content-not-a-commit` lands, and that is true. It is
written this way because the two forms are mutually exclusive and only one
checker exists in this tree:

| The stamp | This tree's check | The #239 branch's check |
|---|---|---|
| `Verified <date> at <sha>` | required | refused by that branch's own rider check  <!-- NAME NOT IN TREE --> |
| `Verified <date> against <anchor>@<hash>` | refused — `a rider with no verification stamp` | required |

Both halves executed. The new form was written into the file and
`tests/test_a_rider_reaches_its_file.py` went red on two cases; the #239
branch's replacement was read at
`origin/fix/239-a-stamp-names-content-not-a-commit`.

Accepting the new form here would mean rewriting
`tests/test_a_rider_reaches_its_file.py` — mechanism, which a fix pass may
not add (`skills/code-review/SKILL.md` §*A fix pass adds the unit that pins
it*), and the one file that branch rewrites. So the rider carries the
hand-over at its own coordinate: whichever of the two branches merges into
`release/v0.9.1` second re-stamps it in the form its own check reads.

**10** — the anchor `skills/implement/scripts/seal.py#other_worktrees` moved
from `ddf91b71` to `6f1dfdec` in `seal/ledger.md`'s S26 row and in work item
1788789329's R4 row, with both `Checked` dates moved to 2026-09-08 and a
sentence in each Notes cell saying what was re-read.

**Re-verified, not removed, and the fragment's owner was not re-stamped
casually.** R4's claim is that `git()` has exactly one call site left in
`seal.py`, `other_worktrees`. The enumeration behind it was re-run —
`grep -n 'git(' skills/implement/scripts/seal.py` still leaves that one call
site, and a comment adds no call of any kind — so the claim is unchanged and
nothing it cites was taken away. `CLAUDE.md`'s removal rule is for a row
whose anchor a change REMOVES; this change removed nothing, so re-verifying
is the honest answer and deleting another work item's evidence for a claim
that still holds would not be.

**11** — the common git directory is resolved once in `main` and handed to
both readers. `optin.home_at` gains the `common` parameter `home_paths`
already had, `undeclared` and `marker_dir` pass it down, and `marker_dir`
returns it instead of asking `git_dir_of` for the same path a third time.

Measured with a logging `git` on `PATH`, one `ls` payload, before and after:

| The repository | Main tree | Linked worktree |
|---|---|---|
| no `seal/` | 1 → 1 | 2 → 2 |
| local root, no row | **2 → 1** | **4 → 2** |
| shared root, no row | 2 → 2 | **4 → 3** |

The `deny → ask → silent` verdicts are unchanged in all six states, and 279
cases across the seven gate modules pass. `pr-notes.md` now states all three
states in both shapes, with the wall clock re-measured after the fix: 32.8 ms
in a main work tree and 44.8 ms in a linked one, against the sibling's 21.9
and 22.2, median of twelve.

**12** — the sentence says re-verified, names the hash and date that moved,
and says which act each is.

## Re-enumeration

**The class of 11 is *one hook invocation asking git the same question
twice*.** `skills/code-review/scripts/chain_check.py#local_root` is the
second member — this branch wrote it, and it has the same `home_at` then
`home_paths` pair. Fixed in the same commit. The remaining duplication is
`rev-parse --show-toplevel` resolved once per gate, which is the deferral the
rider on `hooks/optin.py#repo_root` already carries and a change to three
gates at once.

**The class of 9 and 10 is *planting a rider*, and its second defect is what
the round found.** So the whole fix range was walked again for drifted
anchors rather than only the two rows the finding named:

| Tree state | Drifted anchors | Distinct names |
|---|---|---|
| `9d2f440` — base of round 1's fixes | 9 | 9 |
| `2138c98` — `release/v0.9.1` | 0 | 0 |
| `5e56470` — round 2's target | 11 | 10 |
| `646cbcf` — round 2's record | 11 | 10 |
| this pass's code, with the ledger as it stood | 16 | 15 |
| this pass, after | **9** | **9** |

The nine at the end are name for name the nine at `9d2f440` — the rows
already deferred to the repository owner, still deferred, with no blanket
`--reverify` run.

**Five of the rows this pass re-stamped were nobody's finding.** The
`home_at` change of finding 11 drifted `hooks/optin.py#home_at` in five
`seal/ledger.md` rows (S1, S2, S4, S16 and the `Mode`-row clause) and two
rows in this work item's own fragment, neither of which names `home_at`. Each claim was re-read: none of them
is about the signature, all five still hold, and S16 — *the pair costs no
extra `git` call* — is widened by the change rather than threatened by it.

**The report's drift counts do not reproduce exactly.** It states 8 / 0 / 9 /
9; the same four states measured here give 9 / 0 / 11 / 11 rows. The
conclusion is unaffected and reproduces exactly: the one name drifted at the
target and at neither parent is `seal.py#other_worktrees`, in two files.

**Every stamp and date written by this pass** was checked against what was
read: one rider stamp, `2138c98`, verified as an ancestor of HEAD and as
holding an identical `other_worktrees`; every `Checked` date 2026-09-08, the
day the rows were re-read.

**No unit was added.** `git diff 646cbcf..HEAD` adds no `def`, `class` or
module constant — the three `def` lines it touches are signatures gaining a
defaulted parameter. Finding 11's Location resolves to `marker_dir`, a unit
round 1's fixes created, so a case added to pin its fix would be at depth 2
and refused; see *Not verified* below for where that case went.

**The changelog fragment states no `git` cost**, so nothing in it is
falsified by this pass and it is unchanged.

## Contract changes

Three signatures widened, all with defaults, so no existing call site had to
move: `hooks/optin.py#home_at` `(root)` → `(root, common=None)`;
`hooks/mode-gate.py#undeclared` `(root)` → `(root, common=None)`;
`hooks/mode-gate.py#marker_dir` `(root, home)` → `(root, home, common=None)`.
Two callers were changed to pass the new argument, `hooks/mode-gate.py#main`
and `skills/code-review/scripts/chain_check.py#local_root`.

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — `agent-contract` §2 keeps them out of a fix pass. The broad gate has still not run |
| a regression case for the gate's `git` process count from a linked worktree, so finding 11's reduction cannot silently regress | the repository owner. Finding 11 sits inside `marker_dir`, a unit round 1's fixes created, so a case pinning its fix is at depth 2 and `round_record.py close` refuses it — the exit is a deferral or an issue, not a case in this pass |
| a rider stamp in the form `fix/239-a-stamp-names-content-not-a-commit` requires | the repository owner, at whichever of the two branches merges into `release/v0.9.1` second. The two forms are mutually exclusive, both measured above, and the rider carries the note at its own coordinate |
| Windows and Linux behaviour of the changed resolvers | CI — everything here was executed on macOS |
