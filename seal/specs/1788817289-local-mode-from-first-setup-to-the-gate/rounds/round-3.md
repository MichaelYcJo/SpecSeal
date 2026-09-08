# 1788817289-local-mode-from-first-setup-to-the-gate — review round 3

| Field | Value |
|---|---|
| Target SHA | 3476579 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed — 2624 passed, 2 skipped locally; `ruff check .` and `ruff format --check .` both exit 0; `evidence-check` exits 1 on nine rows already deferred to the repository owner, which CI reads as a warning. CI's **Windows** leg then failed one case and it was a real defect: `git rev-parse --git-common-dir` answers with `/` on Windows too, so joining `seal` onto it printed `C:/Users/x/repo\.git\seal` — one path spelled two ways, in the gate's question and in chain-check's local-mode sentence. Normalised at the source in `optin.home_paths`, which closes it for all four places that print it |
| Fixes checked by | no fixes to check |
| Contract changes | `hooks/optin.py#home_at` `(root)` → `(root, common=None)`; `hooks/mode-gate.py#undeclared` `(root)` → `(root, common=None)`; `hooks/mode-gate.py#marker_dir` `(root, home)` → `(root, home, common=None)` — all defaulted |
| New units | none |
| Needs a fix | yes — 13 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of `1788817289-local-mode-from-first-setup-to-the-gate` (tickets #225, #151), at target `3476579`, base `origin/release/v0.9.1`. The verifying round over round 2's fixes, whose substance is `064330b`, `ad3ee1b` and `54cea1f`, and the last round this work item gets: rounds 1 and 2 both closed on fixes, so the record after this one ends the run whatever it finds.

The named targets. Finding 11's repair changed how the gate resolves a root, with git calls reported falling 4→2 and 2→1 and a second member of the class found in `chain_check.py#local_root`, so the counts were to be re-derived in every tree state and the verdict order `deny → ask → silent` checked as genuinely unchanged rather than reported unchanged. The fix pass could not write a regression case for finding 11 and routed it to the repository owner on the grounds that the repair sits inside a unit round 1 created, making the case depth 2; the round was to judge whether the repair is actually unpinned and, if so, name the smallest thing that would pin it — a fix nothing can fail on being what this repository's `verify` skill calls a counterfeit seal. Five more ledger rows drifted that no finding named, re-read and re-verified by the fix pass, to be opened claim by claim, since the rule permits a re-verify only where somebody actually read it. Round 2's own drift numbers had not reproduced (8/0/9/9 against 9/0/11/11) and the round was to say which is right. The rider stamp is deliberately in the OLD form at `2138c98`, because the two formats are mutually exclusive and this tree has one checker: the exclusivity claim, the ancestry, the AST identity of `other_worktrees` there, and whether the rider says in its own text that it is provisional. And whether the diff really adds no new unit, since `close` had refused a depth-2 unit and a hidden one would make the fix table wrong.

Rounds 1 and 2's subject matter — the prompt budget, the four original reds, the mutation sweep — was settled and not to be re-reviewed.

The report was to be a file, finding ids bare integers, one row per finding, no real user path, and `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | the rider stamp named a commit the squash discards | `skills/implement/scripts/seal.py#other_worktrees` | answered | executed: `2138c98` is an ancestor of HEAD and of `origin/release/v0.9.1`; `other_worktrees` AST-identical there; the new form turns two cases red in this tree; the rider names itself provisional |
| 10 | two ledger anchors drifted by round 1's rider | `seal/ledger.md` S26, `seal/ledger/1788789329-…md` R4 | answered | read: both re-anchored to `6f1dfdec`, both claims re-opened and still hold; executed: 39 / 22 / 13 fragment rows all OK |
| 11 | the mode gate asked git the same question three times | `hooks/mode-gate.py#marker_dir` | answered on the code, open on its pinning | executed: all six state counts reproduce, `deny → ask → silent` unchanged; the marker path is identical across the two versions. See 13 |
| 12 | the re-verification sentence did not say what it was | `seal/ledger.md`, `seal/ledger/1788817289-…md` | answered | read: each Notes cell now names the hash and the date that moved and which act it is |
| 13 | the `git`-process reduction is unpinned, and the depth-2 grounds for leaving it unpinned do not reach two of the three units | `hooks/optin.py#home_at`, `hooks/mode-gate.py#marker_dir` | deferred #244 | executed: reverting the three files leaves 316 cases green, exit 0. read: `round_record.py#depth_two` refuses only a unit added in the finding's own file; `round-1.md`'s `New units` names `marker_dir` and not `local_root`. The proposed case was seen red |
| 14 | the fix record names a symbol the tree does not carry, and `evidence-check` exits 2 on it | `seal/specs/1788817289-…/rounds/round-2-fixes.md:46` | answered | executed: `bin/evidence-check .` prints `1 refused` and exits 2; `.github/workflows/test.yml`'s `ledger` job fails on `>= 2` |
| 15 | the fix record miscounts the fragment rows it re-stamped | `seal/specs/1788817289-…/rounds/round-2-fixes.md:126-128` | answered | executed: the fragment names `home_at` zero times, and `--numstat` reports two changed rows, not four |
| 16 | a re-stamped ledger row carries a stale test count beside the word Executed | `seal/ledger.md` S2 | answered | executed: `tests/test_optin_home.py` collects 42; the cell says 31 |

## Paste-ready fixes

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
```markdown
| `Verified <date> at <sha>` | required | refused by `test_no_rider_stamp_names_a_commit` (NAME NOT IN TREE — the check on `fix/239-a-stamp-names-content-not-a-commit`) |
```
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
```markdown
**Executed**: `tests/test_optin_home.py`, 42 passed at `3476579` — both places in order, the shared root winning when both exist, a linked worktree's common directory found through git, a main worktree's without a process
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/mode-gate.py:223-226` | round 1's 1 — fixed |
| round-1 | `hooks/mode-gate.py:105-122` · `hooks/config.py:104-111` | round 1's 2 — fixed |
| round-1 | `hooks/mode-gate.py:125-142` | round 1's 3 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1384-1439` | round 1's 4 — fixed |
| round-1 | `hooks/mode-gate.py:210-226` | round 1's 5 — fixed |
| round-1 | `hooks/mode-gate.py:94` | round 1's 6 — fixed |
| round-1 | `templates/config.md` | round 1's 7 — fixed |
| round-1 | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/changelog.md` | round 1's 8 — fixed |
| round-2 | `hooks/mode-gate.py:304-327` | round 2's 1 — answered |
| round-2 | `hooks/mode-gate.py:152-177` | round 2's 2 — answered |
| round-2 | `hooks/mode-gate.py:209-225` | round 2's 3 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:1532-1589` | round 2's 4 — answered |
| round-2 | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/pr-notes.md` | round 2's 5 — answered |
| round-2 | `hooks/mode-gate.py:89-124` | round 2's 6 — answered |
| round-2 | `skills/implement/scripts/seal.py:1640` | round 2's 9 — fixed |
| round-2 | `seal/ledger.md:689` · `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md:73` | round 2's 10 — answered |
| round-2 | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/pr-notes.md` · `hooks/mode-gate.py:209-225` | round 2's 11 — fixed |
| round-2 | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/rounds/round-1-fixes.md` | round 2's 12 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| pinning `marker_dir`'s own two removed `git` calls | stays deferred — `marker_dir` is depth 1 by `round-1.md`, so a case for it is what `skills/code-review/SKILL.md` §*A fix pass may add a unit* calls depth 2 | the repository owner |
| the prose in `skills/code-review/SKILL.md` §*A fix pass may add a unit* and the enforcement in `round_record.py#depth_two` do not agree about a case under `tests/` | a follow-up work item, not this one | the repository owner |
| git's own `GIT_DIR` / `GIT_COMMON_DIR` environment variables (NAME NOT IN TREE) | unopened, named under *Not verified* above | the repository owner |
| the full suite, lint and typecheck | the broad gate | the orchestrator |
