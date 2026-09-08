# Round 3 — the verifying round

Work item `1788817289-local-mode-from-first-setup-to-the-gate`, tickets #225
and #151. Branch `fix/225-151-local-mode-from-first-setup-to-the-gate`, target
`3476579`. The reviewed surface is `git diff 5e56470..3476579`, whose substance
is `064330b`, `ad3ee1b` and `54cea1f`. Rounds 1 and 2 and their verdicts are
inherited and were not re-walked.

## What was asked, and how it came out

Six things were handed over to be re-derived rather than read. All six
reproduce, and one of them opens a finding about the fix rather than about the
code it fixed.

| Asked | Answer |
|---|---|
| the four-state `git` count and the verdict order | reproduces exactly, all six states, verdicts unchanged |
| whether the repair is pinned by anything | **it is not** — reverting all three files leaves 316 cases green (finding 13) |
| the five ledger rows nobody's finding named | every claim re-read; all still hold |
| whose drift numbers are right, the report's or the fix pass's | the fix pass's — and the report's numbers were counting a different column |
| the rider stamp's exclusivity, ancestry and provisional wording | all three confirmed |
| that no new unit was added | confirmed |

Three further things opened, none of them in the code: two in the fix pass's
own record and one in a ledger row it re-stamped.

---

## The repair is real, and nothing in the tree fails when it is taken away

### The counts reproduce, and so does the verdict order

Executed. A shim `git` on `PATH` counting processes, one `ls`-shaped payload,
each of round 2's six tree states, with the gate module taken out of git at
`5e56470` and at `3476579` so the two versions ran against the same fixtures.

| The repository | Main tree | Linked worktree |
|---|---|---|
| no `seal/` | 1 → 1 | 2 → 2 |
| local root, no row | **2 → 1** | **4 → 2** |
| shared root, no row | 2 → 2 | **4 → 3** |

Name for name what `round-2-fixes.md` reports. The verdict order is
`deny → ask → silent` in all four states where the gate speaks, before and
after, and silence in the two where it does not.

One thing worth recording that the fix pass did not: in the first run the
linked worktree of the local-root fixture went silent under BOTH gate versions,
because the main tree had already spent that clone's two markers in the same
session. That is `marker_dir`'s per-clone keying working, and it also shows the
two versions write and find the SAME marker path — the marker the old gate
wrote was found by the new one and the other way round.

### But nothing can fail on it

Executed, and this is the decisive one. `hooks/mode-gate.py`, `hooks/optin.py`
and `skills/code-review/scripts/chain_check.py` were reverted to their
`5e56470` content in a clone at `3476579`, and the eight gate modules were run:
**316 passed, exit 0.** The whole `git`-process reduction can be removed
without a single case noticing.

The fix pass knew this and routed it to the repository owner. Its stated reason
does not hold, and finding 13 below is that reason.

---

## Finding 13 — 🟡 the reduction is unpinned, and the grounds for leaving it unpinned do not hold

**Location** — `hooks/optin.py#home_at`, `hooks/mode-gate.py#marker_dir`;
the grounds are at
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/rounds/round-2-fixes.md`
(*Not verified*, second row).

The record says a case pinning the reduction *"is at depth 2 and
`round_record.py close` refuses it"*. Two separate things are wrong with that.

**The enforcement does not refuse it.** `skills/code-review/scripts/round_record.py#depth_two`
refuses a unit added **in the same file as the finding's Location**:

```
for f in files:
    inside = [n for r, n in added if r == f]
```

`f` is `hooks/mode-gate.py`. A regression case lives under `tests/`, so `r != f`
and nothing is refused. `under_tests` is defined in that module and is not
applied to `added` at all. (Read, not executed — running `close` needs a whole
record to be staged, and the branch is the same either way.)

**And two of the three removed `git` calls sit in units that are depth 1
anyway.** `round-1.md`'s `New units` row names `marker_dir (depth 1)` and does
**not** name `local_root`, so:

| Where a call was removed | The unit | Depth of a case pinning it |
|---|---|---|
| `hooks/optin.py#home_at` | predates the run — in `seal/ledger.md` since 0.4.0 | **1** |
| `skills/code-review/scripts/chain_check.py#local_root` | added by the implementation, not by a fix | **1** |
| `hooks/mode-gate.py#marker_dir` | added by round 1's fixes | 2 by the prose in `skills/code-review/SKILL.md` §*A fix pass may add a unit* |

So the depth rule covers one of the three, and the fix pass's own
re-enumeration section names `local_root` as the class's second member — the
member it then declined to pin on grounds that do not reach it.

**Why it matters.** `skills/verify/SKILL.md` calls a fix nothing can fail on a
counterfeit seal, and this one is a performance property: it leaves no wrong
answer behind when it regresses, only three more processes on every Bash call,
which is exactly the kind of regression a reader never notices. The next
session that touches `home_at` and drops the `if common is None` guard turns
the linked-worktree cost back to four and every case stays green.

**The smallest thing that would pin it** is a sibling of the case that already
exists one level down, `tests/test_optin_home.py:272#test_home_paths_costs_no_second_git_call_when_common_is_passed`.
It is written out under *Paste-ready fixes* below, and it was seen red before
it was offered: green against `3476579`, and `AssertionError: home_at asked git
a second time` with the `if common is None` guard deleted. It must run from a
LINKED worktree — from a main tree `.git` is a directory, `git_common_dir`
never reaches `subprocess`, and the case passes against the old code too.

It pins one of the three calls. Pinning `local_root`'s is the same shape in
`tests/test_local_mode_reaches_the_review_chain.py` and is also depth 1;
`marker_dir`'s two remain the honest deferral.

---

## Finding 14 — ⬜ the fix pass's record turns the ledger check red

**Location** — `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/rounds/round-2-fixes.md:46`.

That line names `test_no_rider_stamp_names_a_commit` **(NAME NOT IN TREE** —
it is the check on `fix/239-a-stamp-names-content-not-a-commit`, and this tree
does not carry it**)**. The rule the round 2 prompt handed the fix pass, and the
one this round was handed, is to write `NAME NOT IN TREE` on such a line.

This is not only paperwork. Executed:

```
records — what unreleased work items state about the tree
  NOT-IN-TREE  …/rounds/round-2-fixes.md:46  `test_no_rider_stamp_names_a_commit` — …
  3 work items read · 42 unread · 475 names read · 0 stamps read · 1 refused · …
```

`bin/evidence-check .` exits **2**. `skills/evidence-check/scripts/evidence_check.py`
returns 2 on `refused`, and `.github/workflows/test.yml`'s `ledger` job fails on
any code `>= 2` while treating drift alone as a warning. So the pull request's
ledger job is red until that line is edited.

It is located under `seal/specs/`, so `docs/review-chain-spec.md` §*A finding
located in a record is a correction, not a round* makes it a correction rather
than a fix, and it is not counted in `Needs a fix`. It still has to be edited
before the pull request.

## Finding 15 — ⬜ and the same record miscounts what it re-stamped

**Location** — `.../rounds/round-2-fixes.md:126-128`.

> The `home_at` change of finding 11 drifted `hooks/optin.py#home_at` in five
> `seal/ledger.md` rows (S1, S2, S4, S16 and the `Mode`-row clause) and four
> rows in this work item's own fragment.

The first half is right — five rows, executed against the diff. The second half
is wrong twice. Executed:

- `seal/ledger/1788817289-local-mode-from-first-setup-to-the-gate.md` names
  `optin.py#home_at` **zero** times, so `home_at` drifted nothing there.
- `git diff 5e56470..3476579 --numstat` on that fragment reports `2 2` — **two**
  rows changed, not four.

What actually drifted in this item's fragment is four ANCHORS across those two
rows: `chain_check.py#local_root`, `mode-gate.py#undeclared`,
`mode-gate.py#marker_dir` and `mode-gate.py#main`. The re-verifications
themselves are sound; the sentence describing them is not.

## Finding 16 — ⬜ a re-stamped row carries a test count that no longer matches

**Location** — `seal/ledger.md`, row S2.

Its `Checked` date moved to 2026-09-08 and its evidence cell still reads
**Executed**: `tests/test_optin_home.py`, 31 passed. Executed here: that module
now collects **42**. The claim the row pins — the reading order — holds, and
`CLAUDE.md` defines `Checked` as the date somebody read the CODE, so the date is
not itself a false execution claim. But the number beside the word *Executed*
is now three releases stale on a row that was just re-stamped, and the sibling
row S1 shows the form that avoids it by binding its count to a commit
(*38 passed at `8d05b00`*).

---

## The other four things that were asked, all clean

**The drift numbers — both counts were right, about different columns.**
Executed, `evidence_check.py` run at five checked-out states:

| State | Drifted rows | Distinct names |
|---|---|---|
| `9d2f440` | 9 | 9 |
| `2138c98` | 0 | 0 |
| `5e56470` | 11 | 10 |
| `646cbcf` | 11 | 10 |
| `3476579` | 9 | 9 |

The fix pass's table reproduces name for name, including *the nine at the end
are the nine at `9d2f440`* — `diff` of the two sorted name sets is empty. The
round 2 report's `8 / 0 / 9 / 9` matches neither column. Nothing turns on it:
the conclusion reproduces exactly, and `comm` of the name sets at `5e56470` and
`9d2f440` leaves one name, `skills/implement/scripts/seal.py#other_worktrees`.

**The rider stamp.** Four claims, three executed:

- `2138c98` is an ancestor of `3476579` **and** of `origin/release/v0.9.1`, so
  the squash keeps it (executed, `git merge-base --is-ancestor`).
- `other_worktrees` is identical at `2138c98` and `3476579` once comments go —
  the two `ast.unparse` dumps compare equal (executed).
- The two stamp forms are mutually exclusive. Writing
  `Verified 2026-09-08 against other_worktrees@00000000` into `seal.py` turns
  `tests/test_a_rider_reaches_its_file.py` red on exactly two cases,
  `test_every_rider_carries_the_date_and_sha_it_was_verified_at` and  <!-- NAME NOT IN TREE -->
  `test_every_rider_stamp_names_a_commit_this_branch_can_reach`, exit 1  <!-- NAME NOT IN TREE -->
  (executed). The other side is read, not executed: on
  `origin/fix/239-a-stamp-names-content-not-a-commit`,
  `test_no_rider_stamp_names_a_commit` **(NAME NOT IN TREE)** refuses the old
  spelling, and its `test_every_rider_carries_a_verification_stamp` (NAME NOT IN TREE)
  requires the new one.
- The rider says so in its own text — `PROVISIONAL FORM`, naming the branch
  that replaces it and who re-stamps it (read).

**No new units.** Executed. The diff's four `.py` files add no `def`, `class`
or module constant; the three `+def` lines are `undeclared`, `marker_dir` and
`home_at` gaining a defaulted parameter, and all three exist at `5e56470`.

**The nine re-verified ledger rows.** Read, each claim opened:

| Row | Claim | Still holds? |
|---|---|---|
| S1 | no config key, no marker, no environment variable | yes — a parameter carrying a path the caller resolved reads nothing new |
| S2 | the two places, in order, and nothing else | yes — `for found in home_paths(root, common)` is untouched |
| S4 | the opt-out is a FILE, read once, before either place | yes — still ahead of the loop in `home_at` |
| S16 | the pair costs no extra `git` call | yes, and widened; the widening is what finding 13 is about |
| `Mode` row | `home_at` stays the only reader of where the root IS | yes — `git_common_dir` answers where the git directory is, not where the root is |
| S26 | a clone with more than one worktree is named, not refused | yes — the change is comment-only, AST-identical |
| R4 (item 1788789329) | `git()` has one call site left in `seal.py` | yes — a comment adds no call |
| S5, S6 | `chain_check` names the root it searched | yes — `local_root`'s answer is unchanged, only its `git` cost moved |
| S7–S10 | the two-prompt budget, per session per repository | yes — re-measured above, `deny → ask → silent` in every state |

None of the nine is about a signature, so re-verifying rather than removing is
the right act: `CLAUDE.md`'s removal rule is for a row whose anchor a change
REMOVES, and this change removed nothing.

## The class of finding 11, re-enumerated independently

The class is *one hook invocation asking git the same question twice*. Read:
`grep` over `hooks/` and `skills/` for `home_at(`, `home_paths(` and
`git_common_dir(` finds two more modules with two `home_at` call sites each —
`hooks/evidence-advisor.py` (117, 146) and `hooks/ledger-migrate.py` (87, 166).
Neither is a member: both inner sites are guarded `home = home or optin.home_at(root)`
and both are reached with `home` already resolved by `main`. Every other caller
passes one argument, so the three widened signatures broke no call site —
which is what the record's `Contract changes` claims.

`chain_check.py#local_root` was the only other member, and it is fixed.

## Not verified — who answers what

| Item | Who answers |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator. `agent-contract` §2 keeps them out of a round; the broad gate has still not run. Eight gate modules were run here, which is the reviewed diff's surface and no wider |
| Windows and Linux behaviour of the changed resolvers | CI — everything here ran on macOS |
| whether `optin.git_common_dir`'s fast path and `git rev-parse --git-common-dir` can disagree under git's own `GIT_DIR` / `GIT_COMMON_DIR` environment variables (NAME NOT IN TREE — they are git's, not this repository's) | left unopened. `marker_dir` now takes the fast path's answer where it used to ask git, so the two readers agree with each other where they used to differ; the direction of the change is toward consistency, and no fixture was built for the env-var case |

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | the rider stamp named a commit the squash discards | `skills/implement/scripts/seal.py#other_worktrees` | answered | executed: `2138c98` is an ancestor of HEAD and of `origin/release/v0.9.1`; `other_worktrees` AST-identical there; the new form turns two cases red in this tree; the rider names itself provisional |
| 10 | two ledger anchors drifted by round 1's rider | `seal/ledger.md` S26, `seal/ledger/1788789329-…md` R4 | answered | read: both re-anchored to `6f1dfdec`, both claims re-opened and still hold; executed: 39 / 22 / 13 fragment rows all OK |
| 11 | the mode gate asked git the same question three times | `hooks/mode-gate.py#marker_dir` | answered on the code, open on its pinning | executed: all six state counts reproduce, `deny → ask → silent` unchanged; the marker path is identical across the two versions. See 13 |
| 12 | the re-verification sentence did not say what it was | `seal/ledger.md`, `seal/ledger/1788817289-…md` | answered | read: each Notes cell now names the hash and the date that moved and which act it is |
| 13 | the `git`-process reduction is unpinned, and the depth-2 grounds for leaving it unpinned do not reach two of the three units | `hooks/optin.py#home_at`, `hooks/mode-gate.py#marker_dir` | open (🟡) | executed: reverting the three files leaves 316 cases green, exit 0. read: `round_record.py#depth_two` refuses only a unit added in the finding's own file; `round-1.md`'s `New units` names `marker_dir` and not `local_root`. The proposed case was seen red |
| 14 | the fix record names a symbol the tree does not carry, and `evidence-check` exits 2 on it | `seal/specs/1788817289-…/rounds/round-2-fixes.md:46` | open (⬜ correction) | executed: `bin/evidence-check .` prints `1 refused` and exits 2; `.github/workflows/test.yml`'s `ledger` job fails on `>= 2` |
| 15 | the fix record miscounts the fragment rows it re-stamped | `seal/specs/1788817289-…/rounds/round-2-fixes.md:126-128` | open (⬜ correction) | executed: the fragment names `home_at` zero times, and `--numstat` reports two changed rows, not four |
| 16 | a re-stamped ledger row carries a stale test count beside the word Executed | `seal/ledger.md` S2 | open (⬜ correction) | executed: `tests/test_optin_home.py` collects 42; the cell says 31 |

## Executed probes

| What was run | Result |
|---|---|
| shim `git` on `PATH`, one Bash payload, six tree states, gate at `5e56470` and at `3476579` | 1→1, 2→2, **2→1**, **4→2**, 2→2, **4→3**; `deny → ask → silent` unchanged in all four speaking states |
| same probe with one session id shared across a clone's two work trees | linked tree silent under both gate versions — the marker path is identical before and after |
| revert `hooks/mode-gate.py`, `hooks/optin.py`, `chain_check.py` to `5e56470`, run 8 gate modules | `316 passed`, exit 0 — nothing pins the fix |
| `bin/test` on the 7 gate modules at `3476579` | `231 passed` |
| `git merge-base --is-ancestor 2138c98 3476579` / `… origin/release/v0.9.1` | both yes |
| `ast.unparse` compare of `other_worktrees` at `2138c98` and `3476579` | identical |
| write `Verified 2026-09-08 against other_worktrees@00000000` into `seal.py`, run `tests/test_a_rider_reaches_its_file.py` | `2 failed, 6 passed`, exit 1 — the two forms are mutually exclusive |
| `evidence_check.py .` at `9d2f440`, `2138c98`, `5e56470`, `646cbcf`, `3476579` | rows 9 / 0 / 11 / 11 / 9; names 9 / 0 / 10 / 10 / 9; name sets at `9d2f440` and `3476579` identical |
| `bin/evidence-check .` at `3476579`, exit code read directly | `1 refused`, exit **2** |
| `comm` of drifted name sets, `5e56470` minus `9d2f440` | one name: `skills/implement/scripts/seal.py#other_worktrees` |
| the proposed case appended to `tests/test_optin_home.py`, run at `3476579` | `1 passed` |
| the same case with `if common is None:` deleted from `home_at` | `1 failed` — `AssertionError: home_at asked git a second time` |
| `git diff 5e56470..3476579` grepped for added `def` / `class` / module constant | three `+def` lines, all existing units gaining a defaulted parameter; no new unit |

Probes were `test_tmp_*`, run in a `git clone --no-local` at `3476579`, and are
deleted. The working tree was not written to.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| pinning `marker_dir`'s own two removed `git` calls | stays deferred — `marker_dir` is depth 1 by `round-1.md`, so a case for it is what `skills/code-review/SKILL.md` §*A fix pass may add a unit* calls depth 2 | the repository owner |
| the prose in `skills/code-review/SKILL.md` §*A fix pass may add a unit* and the enforcement in `round_record.py#depth_two` do not agree about a case under `tests/` | a follow-up work item, not this one | the repository owner |
| git's own `GIT_DIR` / `GIT_COMMON_DIR` environment variables (NAME NOT IN TREE) | unopened, named under *Not verified* above | the repository owner |
| the full suite, lint and typecheck | the broad gate | the orchestrator |

## Paste-ready fixes

Finding 13 — append to `tests/test_optin_home.py`, beside
`test_home_paths_costs_no_second_git_call_when_common_is_passed`. It uses the
module's existing `local_home` and `linked_worktree` helpers, and the linked
worktree is load-bearing: from a main tree `.git` is a directory,
`git_common_dir` never reaches `subprocess`, and the case would pass against
the old code too.

```python
def test_home_at_costs_no_second_git_call_when_common_is_passed(
    optin, repo, tmp_path
):
    """S16, one level up, from the tree where it is worth a process.

    `hooks/mode-gate.py#main` resolves the common git directory once and hands
    it to both readers. What that bought -- four `git` processes to two on
    every Bash call from a linked worktree with a local root -- rests on
    `home_at` honouring the parameter rather than resolving it again, and a
    linked worktree is where `.git` is a FILE and the fast path does not
    apply.
    """
    local_home(repo)
    other = linked_worktree(repo, tmp_path)
    common = optin.git_common_dir(str(other))

    def refuse(*a, **k):
        raise AssertionError("home_at asked git a second time")

    optin.subprocess.run, saved = refuse, optin.subprocess.run
    try:
        assert optin.home_at(str(other), common) == os.path.join(common, "seal")
    finally:
        optin.subprocess.run = saved
```

Finding 14 — `round-2-fixes.md:46`, the whole line:

```markdown
| `Verified <date> at <sha>` | required | refused by `test_no_rider_stamp_names_a_commit` (NAME NOT IN TREE — the check on `fix/239-a-stamp-names-content-not-a-commit`) |
```

Finding 15 — `round-2-fixes.md`, the sentence at 126-128:

```markdown
**Five of the rows this pass re-stamped were nobody's finding.** The
`home_at` change of finding 11 drifted `hooks/optin.py#home_at` in five
`seal/ledger.md` rows (S1, S2, S4, S16 and the `Mode`-row clause), and the
same fix drifted four anchors — `chain_check.py#local_root`,
`mode-gate.py#undeclared`, `mode-gate.py#marker_dir` and `mode-gate.py#main` —
across two rows of this work item's own fragment. Each claim was re-read: none
of them is about a signature, all of them still hold, and S16 — *the pair
costs no extra `git` call* — is widened by the change rather than threatened
by it.
```

Finding 16 — `seal/ledger.md` row S2, the evidence cell only:

```markdown
**Executed**: `tests/test_optin_home.py`, 42 passed at `3476579` — both places in order, the shared root winning when both exist, a linked worktree's common directory found through git, a main worktree's without a process
```

---

Needs a fix: yes — 13
Loses a record or crashes: no
Contract changes: `hooks/optin.py#home_at` `(root)` → `(root, common=None)`; `hooks/mode-gate.py#undeclared` `(root)` → `(root, common=None)`; `hooks/mode-gate.py#marker_dir` `(root, home)` → `(root, home, common=None)`. All defaulted; every other caller of the three passes one argument, verified by grep over `hooks/`, `skills/` and `tests/`
New units: none

## Proof

Opened in the worktree at `3476579` and in a `git clone --no-local` of it:
`hooks/mode-gate.py`, `hooks/optin.py`, `hooks/config.py`,
`hooks/evidence-advisor.py`, `hooks/ledger-migrate.py`, `hooks/routing.py`,
`skills/code-review/scripts/chain_check.py`,
`skills/code-review/scripts/round_record.py`, `skills/code-review/SKILL.md`,
`skills/implement/scripts/seal.py`,
`skills/evidence-check/scripts/evidence_check.py`,
`tests/test_a_rider_reaches_its_file.py`,
`tests/test_a_fix_pass_may_add_a_unit.py`, `tests/test_optin_home.py`,
`templates/sdd-round.md`, `docs/review-chain-spec.md`, `CONTRIBUTING.md`,
`CLAUDE.md`, `.github/workflows/test.yml`, `seal/ledger.md`,
`seal/ledger/1788817289-local-mode-from-first-setup-to-the-gate.md`,
`seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md`,
`seal/config.md`, and this work item's `rounds/round-1.md`, `round-2.md`,
`round-2-asked.md`, `round-2-fixes.md`. Read at
`origin/fix/239-a-stamp-names-content-not-a-commit`:
`tests/test_a_rider_reaches_its_file.py`.
