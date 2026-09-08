# 1788817289-local-mode-from-first-setup-to-the-gate — review round 2

| Field | Value |
|---|---|
| Target SHA | 5e56470 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed under round 3 |
| Fixes checked by | round-3 |
| Contract changes | undeclared → marker_dir, main, round-1-report.md, round-1.md, round-2-report.md, round-2.md, pytest; marker_dir → main, round-1-fixes.md, round-1-report.md, round-1.md, round-2-report.md, round-2.md; home_at → declaration_hint, failing_rows, main, ledgers, undeclared, optin.py, git_common_dir, home, declarations, ledger.md, plan.md, questions.md, round-1.md, spec.md, phase-1.md, round-1-report.md, round-2-report.md, round-2.md, local_root, seal_home, resolve, pytest |
| New units | none |
| Needs a fix | yes — 9, 10 and 11 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of `1788817289-local-mode-from-first-setup-to-the-gate` (tickets #225, #151), at target `5e56470`, base `origin/release/v0.9.1`. The verifying round over round 1's fixes, whose substance is `1a54687` and `a3bea92`.

Round 1's verdicts were inherited. It had opened eight findings, one of them 🔴: `hooks/mode-gate.py` denied once and then fell to `ask` on every subsequent Bash call — one deny and nine asks in ten calls, where the sibling gates give nine silences — and the escape, `seal mode`, is itself a Bash call, so an unattended run could not reach it.

The prompt budget was the first target, because it is the claim and it had changed: the fix pass re-measured it by running the gate and reported two per repository per session, one deny then one ask, not the one the original notes claimed. The round was to re-derive it in all three states and say what the numbers are, since `CONTRIBUTING.md` calls the budget the one thing a passing suite cannot report on. Then: whether the escape now works unattended, or whether the fix moves the outage one call along. The added cost the fix pass measured and did not remove — a `git rev-parse` on every Bash call in every repository, including those with no `seal/` at all — and whether the deferral of "three gates should resolve the root once" is the right disposition. The four reds re-run rather than read. The nine mutations, especially `common_dir_of`, which survived the first sweep and was not equivalent. Whether `seal/ledger.md`'s deliberately narrow touch is honest and no batch `--reverify` closed a deferral nobody read. And whether the planted `# RIDER:` names a commit of this branch, #239 being the ticket for exactly that.

The bound was stated: round 1 met the floor, a round that opens nothing needing a fix does not consume the cap, and neither manufacturing nor softening a finding was acceptable. The report was to be a file, finding ids bare integers, one row per finding, no real user path, and `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The `ask` never stopped: one deny then a prompt on every command, and the escape is itself a Bash call | `hooks/mode-gate.py:304-327` | **answered** | executed — 20 calls × 2 sessions × 3 states gives 1 deny, 1 ask, 18 silent where a root has no row and 20 silent otherwise; `seal mode` run as call 3 reaches the shell |
| 2 | 🟡 A `config.md` that exists and cannot be read was treated as one that declared nothing | `hooks/mode-gate.py:152-177` | **answered** | executed — a directory of that name, undecodable bytes and `chmod 000` each return `silent` on three consecutive calls; a missing row still returns `deny` |
| 3 | 🟡 The marker was keyed per work tree while a local root is one folder for the whole clone | `hooks/mode-gate.py:209-225` | **answered** | executed — one clone, one local root: main `deny`, worktree `ask`, worktree `silent`. Shared roots still `deny` per tree |
| 4 | 🟡 `repo_of` returned a directory that is not a work tree for `--separate-git-dir` and for a bare clone | `skills/code-review/scripts/round_record.py:1532-1589` | **answered** | executed — separated repository resolves to the caller's tree; bare clone with the caller outside returns `None`; ordinary local-mode repository unchanged |
| 5 | ⬜ Every Bash call in every repository pays an extra `git rev-parse` | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/pr-notes.md` | **answered, and reopened as 11** | executed — the cost is stated now, and the number stated is a main work tree's; see 11 |
| 6 | ⬜ `already_asked`'s `cwd` argument was discarded because `git_dir_of` returns an absolute path | `hooks/mode-gate.py:89-124` | **answered** | read, then executed — the parameter is gone, and `git_dir_of` returns an absolute existing directory for both `--absolute-git-dir` and `--git-common-dir` from a main tree and from a linked one |
| 7 | ⬜ `templates/config.md` still opened with *an absent row is not an error* | `templates/config.md` | **answered** | read — the opening now carves `Mode` out twice over, and no table row changed |
| 8 | ⬜ The changelog fragment did not say who meets the gate on upgrade | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/changelog.md` | **answered** | read — the fragment names every repository that opted in before this release and the one command that ends it |
| 9 | 🔴 The rider stamp names `a3bea92`, a commit of this feature branch, which the squash into `release/v0.9.1` discards — #239's class, one commit after #239's first instance was repaired | `skills/implement/scripts/seal.py:1640` | **fixed** `064330b` | fixed at 064330b; executed — squashed `5e56470` onto `2138c98` in a `--no-local` clone: `test_every_rider_stamp_names_a_commit_this_branch_can_reach` exits 0 before and 1 after, naming `a3bea92` |
| 10 | 🟡 The rider drifted `seal.py#other_worktrees` in `seal/ledger.md` and in another work item's ledger fragment, and neither row was re-read or re-stamped | `seal/ledger.md:689` · `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md:73` | answered | corrected at 54cea1f |
| 11 | 🟡 The stated per-call `git` cost is a main work tree's number: a linked worktree pays 2 where the document says 1 and 4 where it says 2, and two of the four are the new code re-asking a question `optin.home_at` already answered | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/pr-notes.md` · `hooks/mode-gate.py:209-225` | **fixed** `ad3ee1b` | fixed at ad3ee1b — and the document half corrected at 54cea1f; executed — logging `git` on `PATH`, one `ls` payload: 1/2 from a main tree, 2/4 from a linked worktree; 59.0 ms against the sibling's 27.2 ms there, median of twelve |
| 12 | ⬜ `round-1-fixes.md` says the S8 row was "re-read rather than re-stamped"; its anchor hash and `Checked` date both changed, which is a re-verify | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/rounds/round-1-fixes.md` | answered | corrected at 54cea1f |

## Paste-ready fixes

```python
    # this list the same way when this function is next opened.
    #
    # Stamped at a commit on the release branch rather than at the fix pass's
    # own, because a feature branch squashes and the commit that measured
    # this stops existing at that merge. #239 holds the class; this is the
    # second instance, and the first turned `release/v0.9.1` red.
    # Verified 2026-09-08 at 2138c98.
```
```
`skills/implement/scripts/seal.py#other_worktrees@9cc8fc3d`
```
```
2026-09-08
```
```
**Re-read 2026-09-08 in work item 1788817289's round 1 fix pass**, which planted a `# RIDER:` inside this function while enumerating a class; the comment is the whole of what changed, the loop and its answer are untouched, so what this row pins did not move.
```
```
`skills/implement/scripts/seal.py#other_worktrees@9cc8fc3d`
```
```python
def home_at(root, common=None):
    """The `seal/` of the repository at `root`, or "" — for a caller that has
    already resolved the root and should not pay for a second `git` call.

    The two places are read in order, `<root>/seal/` then
    `<git-common-dir>/seal/`, and whichever exists first is the answer;
    nothing else is read. The opt-out is read once, here, so it cannot be
    honoured by one arm of a gate and missed by the other — the migration
    config sits inside the root the marker takes back, and a repository
    nobody reviews has nothing to compare against an original either.

    `common` is passed by a caller that needs the common directory for
    something else too, so one hook invocation asks git for it once rather
    than once per unit that wants it. `hooks/mode-gate.py` is that caller:
    it resolves the root, the opt-in and the marker directory in one pass,
    and measured from a linked worktree the same `rev-parse --git-common-dir`
    was running three times.
    """
    if not root:
        return ""
    if common is None:
        common = git_common_dir(root)
```
```python
def marker_dir(root, home, common=None):
    """The git directory this root's answer is recorded in.

    Per work tree for a SHARED root, which one tree owns: each work tree has
    its own `<repo>/seal/`, so each is a separate unanswered root and each
    deserves its own question.

    Per CLONE for a LOCAL one. There is one root under the common git
    directory serving every work tree, `undeclared()` reads that same folder
    from all of them, and `README.md`'s gate row says once per session per
    repository -- so keying it to the tree asks twice about one folder,
    measured 2026-09-08: one session, one clone, one local root, two denies.

    `common` is the caller's already-resolved common git directory. Without
    it this asked git for the same path twice more in one invocation -- once
    through `home_paths` and once through `git_dir_of` -- which from a linked
    worktree, where `.git` is a file and no fast path applies, was four `git`
    processes on every Bash call against a main tree's two.
    """
    shared, _local = optin.home_paths(root, common)
    if shared and os.path.realpath(home) == os.path.realpath(shared):
        return git_dir_of(root)
    return os.path.normpath(common) if common else git_dir_of(root, "--git-common-dir")
```
```python
def undeclared(root, common=None):
```
```python
    home = optin.home_at(root, common)
    if not home:
        return ""
```
```python
    common = optin.git_common_dir(root)
    home = undeclared(root, common)
    if not home:
        return
```
```python
    git_dir = marker_dir(root, home, common)
```
```
**And a cost that is not a prompt: one `git` process per Bash call from a
main work tree, two from a linked one.** Measured 2026-09-08 with a logging
`git` on `PATH`, one `ls` payload. From a main work tree this gate makes one
`git rev-parse --show-toplevel` in a repository with no `seal/` at all, where
`commit-review-gate.py` makes none — it returns before resolving anything for
a command that is not a commit. A linked worktree pays a second process for
the common git directory, because `.git` is a file there and `optin.py`'s
fast path does not apply, and that is the shape this repository's own
sessions run in. Where a root has no row the count rises by one for the
marker directory, and it stays there on the calls after the budget is spent,
because the root is resolved before there is anything to say.
```
```
One row in `seal/ledger.md` drifted because this pass rewrote the prose above
`templates/config.md`'s table. It was re-read and then re-verified — the row
pins the table's shape, the table is untouched, and the hash was rewritten
by hand so the nine other drifted rows kept their deferral. A blanket
`--reverify` would have closed that deferral without anyone reading a line.
```

## Executed probes

| What was run | Result |
|---|---|
| `hooks/mode-gate.py` fed 20 ordinary Bash payloads per session, two sessions, in three repository states | 1 deny + 1 ask + 18 silent where a root has no row; 20 silent with a row and with no `seal/` |
| the same gate, six calls in one fresh session, root with no row | `deny → ask → silent → silent → silent → silent` |
| the same gate, `ls`, `ls`, then a `seal mode` payload in one session | `deny → ask → silent` — the escape reaches the shell without either prompt being answered |
| `hooks/mode-gate.py` against three unreadable `config.md` shapes, three calls each | directory, undecodable bytes and `chmod 000` all `silent`, nine calls out of nine |
| `hooks/mode-gate.py` in a clone with one local root and a linked worktree | main `deny`, worktree `ask`, worktree `silent`, main `silent` |
| the same, with a shared root in each work tree | main `deny`, worktree `deny` |
| `worktrees_of`, `shares_the_clone` and `repo_of` in a `--separate-git-dir` repository, a bare clone and an ordinary local-mode repository | the caller's tree; `None`; the repository itself. `git -C <sepgit> rev-parse --show-toplevel` still answers *fatal: this operation must be run in a work tree* |
| logging `git` on `PATH`, one `ls` payload, mode gate and commit gate, main tree and linked worktree | mode gate 1/2/2/4 for (no `seal/`, main), (no `seal/`, linked), (root no row, main), (root no row, linked); commit gate 0 in every one |
| wall clock, median of twelve, one `ls`, no `seal/` | linked worktree 59.0 ms against the sibling's 27.2 ms; main tree 40.0 against 28.8 |
| `common_dir_of` with the join dropped, against a `--no-local` clone at `5e56470` | KILLED — exit 1 for the named case alone and for the whole module |
| `common_dir_of` with the `realpath` dropped, same clone | SURVIVED, and a `--separate-git-dir` repository whose git directory was named through a symbolic link gave identical answers both ways, so no failure is constructible from here |
| `skills/evidence-check/scripts/evidence_check.py .` at `9d2f440`, `2138c98`, `ca59969` and `5e56470` in a `--no-local` clone | 8, 0, 9, 9 drifted anchors; the one new name is `skills/implement/scripts/seal.py#other_worktrees` |
| `--reverify` in a throwaway clone, to read the hash the two rows should carry | `ddf91b71` → `9cc8fc3d` in both `seal/ledger.md` and the `1788789329` fragment |
| `git merge --squash 5e56470` onto `2138c98` in a `--no-local` clone, then `tests/test_a_rider_reaches_its_file.py::test_every_rider_stamp_names_a_commit_this_branch_can_reach` | exit 0 before the squash, exit 1 after — *rider stamped a3bea92, which is not an ancestor of HEAD* |
| `bin/test tests/test_the_mode_question_is_asked_once.py tests/test_local_mode_reaches_the_review_chain.py tests/test_first_setup_asks_once.py tests/test_gate_judges_the_repo_it_commits_to.py -q` | 174 passed |
| `bin/test tests/test_a_rider_reaches_its_file.py -q` at the target | 8 passed — the case is green on the feature branch, which is the whole problem in finding 9 |
| finding 11's fix applied in a throwaway clone, then the five gate modules | 191 passed; call counts 2 → 1 (local root, main tree) and 4 → 2 (local root, linked worktree), `deny → ask → silent` unchanged |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether `--worktree` should read routing declarations from the working tree | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/questions.md` Q3 and `seal/follow-up.md` | the repository owner — already deferred by this branch, not re-filed here |
| `tests/test_the_pull_request_language_is_the_repositorys.py#items` reimplements `config_rows` | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/overview.md` §*Not verified* | the repository owner — already deferred by this branch, not re-filed here |
| the eight pre-existing drifted rows in `seal/ledger.md` | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/overview.md` §*Not done* | the repository owner — already deferred by this branch. Finding 10 is not one of them |
| resolving `rev-parse --show-toplevel` once for all three gates | the `# RIDER:` on `hooks/optin.py#repo_root` | the repository owner — the right disposition, and finding 11 is the part of the cost that sits outside it |
