# Round 1 report — a changelog fragment a fix range left behind is named (#797)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 4a8c0ee2 |
| Base | `release/v0.18.3` at a3aa139a |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 4a8c0ee2, in the session scratchpad, removed after the round |

## Summary

Spec compliance holds on a branch checkout. The arm is notice-only and homed
in `chain_check.py`, it asks one question per work item over the first-parent,
non-merge commits after round 1's first `Target SHA`, its behaviour path is
the negative rule the spec chose, it is silent in every state the spec lists
(and one more, with grounds), and the owner section, the three links and the
`RULES` row are in place and pinned. The narrow modules pass (executed).

One reader of the three is wrong, and it is the one the spec leaned on.

- **In CI the arm walks the base, not the branch.** `hygiene.yml` checks a
  pull request out as its head already merged into the base, and that merge's
  first parent is the base. A first-parent walk from it never reaches the work
  item's own commits. It reaches the base's commits since the fork instead,
  which are siblings' squashes. Executed: a lagging fix is named on the branch
  and not on the merge ref, and a sibling's squash is named on the merge ref
  for a lagging item and for an honest one alike, as *after the last round*.
  On this item's own branch, a probe fix is named on the branch checkout and
  nothing is named on the merge ref against `origin/release/v0.18.3`.
- **A behaviour file moved under `tests/` is not named.** `git log
  --name-only` reports a rename by its destination alone, so the deleted
  behaviour path never reaches `behaviour_path`. Executed.
- **The owner section and the fragment name two attributions where the
  notice writes three** (⬜, read).

## Findings

### 🔴 1 — in CI the walk follows the base, so the notice names siblings' squashes and never this item's commits

`skills/code-review/scripts/chain_check.py:4187` and `:4279`.

`commits_after` walks `git log --first-parent --no-merges <target>..HEAD`, and
`fragment_left_behind` computes *after the last round* as `rev-list
<end>..HEAD`. On a branch checkout HEAD is the work item's branch, and both are
right. In CI they are not. `.github/workflows/hygiene.yml:156` states that the
checkout has no `ref:`, so a pull request is checked out as its head already
merged into the base. That synthetic merge's first parent is the base tip and
its second is the pull request head.

From that HEAD the first-parent walk goes down the base. It lists the base's
commits that round 1's target cannot reach, which are the squashes that landed
on the release branch after this branch was cut. The work item's own commits
sit behind the second parent and are never listed. The ancestor guard does not
catch it, because the target is an ancestor of the merge through its second
parent.

What a person reads, by state (executed, probe B, C and the own-branch probe):

| Base since the fork | Item's fragment | Branch checkout (`close`, `round-record seal`) | CI |
|---|---|---|---|
| unmoved | left behind | names the item's fix | silent |
| a sibling landed | left behind | names the item's fix | names the sibling's squash, *after the last round*, and not the fix |
| a sibling landed | brought along | silent | names the sibling's squash, *after the last round* |

Why it matters: the spec chose `chain_check` over the two other homes because
CI runs it on every push (`spec.md` §*Scope*, box 1), and the changelog
fragment and the owner section both say the notice reaches a person *in CI*
(`docs/the-record-layout.md:102`, `changelog.md:13`). On a release branch that
moves by one squash per sibling, the CI notice is wrong in both directions. It
misses the item it was written for, and it tells an honest item's author that
another item's commit left their fragment behind. A reader who learns the CI
line is noise stops reading the branch-checkout line too. The tests never
build a merge ref (every case runs on `feature`), so nothing pins this.

The release is not harmed today only because no sibling has landed on
`release/v0.18.3` yet (`git log` shows a3aa139a at its tip), so this item's
own CI run is silent rather than wrong.

Fix: walk from the parent of a merge HEAD that descends from round 1's target
when the first parent does not, and use the same tip for *after the last
round*. A case builds the merge ref and is red at 4a8c0ee2 (probe B is that
case, executed).

### 🟡 2 — a behaviour file moved under `tests/` or `seal/` is not named

`skills/code-review/scripts/chain_check.py:4184`.

With rename detection, which `git log` applies by default, `--name-only`
prints a rename as its destination alone. A commit that runs `git mv
hooks/big.py tests/big.py` lists `tests/big.py` only, `behaviour_path` rejects
it, and the commit is not named, although it removed a file from what ships
(executed, probe D: `R100 hooks/big.py tests/big.py`, no notice). The same
holds for a move into `seal/`. The docstring's *WHAT IT CANNOT SEE* names the
merge and the outside-`tests` cases and not this one.

There is a second cost. Whether a rename is detected follows the reader's own
`diff.renames` setting, so a local run and CI can list different paths for the
same commit. `--no-renames` lists both sides of a rename on every machine. A
renamed fragment is still seen as touched, because the added side is the
fragment's path.

Would the release ship a defect? Yes: an arm whose declared blind spots are
written down ships with one more that is not.

### ⬜ 3 — the owner section and the fragment name two attributions; the notice writes three

`docs/the-record-layout.md:97-98`, and the same sentence in `changelog.md:9`.

Both say each commit is attributed to the round whose `Fix range` holds it,
*or to after the last round*. The arm also writes *outside every round's fix
range* for a commit between two rounds' ranges (the overview's second
divergence, pinned by the two-round case). The behaviour is right and the
divergence is grounded. The owner section is the document the notice sends
its reader to, so a reader holding the third label finds no sentence for it.
The location of the second coordinate is under `seal/specs/`, so that half is
a correction to the run's paperwork.

## Answers to what the round was asked

**Spec compliance, item by item** (read, with the module run executed):

| Spec clause | Verdict | Where |
|---|---|---|
| a notice only, never a refusal, exit status unchanged | holds | the arm returns `([], notices)`; every case compares the exit code with the arm patched out; executed in all probes (exit equal with and without the notices) |
| homed in `chain_check`, once per chain item after the record walk | holds | `chain_check.py` `main`, after the per-record loop; `straight to the PR` continues before it |
| one question per work item, first-parent non-merge commits from round 1's `Target SHA` to HEAD | holds on a branch checkout; wrong in CI | 🔴 1 |
| behaviour path = outside `seal/` and outside a `tests` directory | holds, with a rename gap | `behaviour_path`, the predicate the same as `under_tests` in `round_record.py`; 🟡 2 |
| the silent cases | hold | `fragment_left_behind`'s guards and the five S7 cases |
| owner section, three links, `RULES` row | hold | `docs/the-record-layout.md` §*A commit after the build brings its changelog fragment along*; `agents/smith.md`, `skills/implement/SKILL.md` §5, `skills/code-review/orchestration.md`; rule 15 in `RULES`; executed in the module run |

**The three divergences in `overview.md`.**

- *A silent state where round 1's target resolves and is not an ancestor of
  HEAD.* Grounded. After a rebase the old commit still answers `rev-parse`,
  and `<target>..HEAD` would read the build itself as late. The guard's own
  case was corrected so its mutation goes red (`phases/phase-1.md`), and both
  the owner section and the fragment list the state. 🟢.
- *The label `outside every round's fix range`.* Grounded: a commit after
  round 1's range and before round 2's record is in neither. The code is
  right; the two prose carriers omit it (⬜ 3).
- *The first SHA of a two-SHA `Target SHA` as the build's end.* Grounded.
  `templates/sdd-round.md` gives the second as a HEAD that moved mid-review,
  which is after the build, so taking the first reads more commits, never
  fewer. Pinned by the moved-HEAD case. 🟢.

**The history shapes, by construction.** The walk names a commit exactly when
three things hold: it is a non-merge commit on HEAD's first-parent chain after
round 1's target, its listed paths include a behaviour path, and it comes after
the last commit in that walk whose listed paths include the fragment.

| Shape | Prints exactly when a behaviour commit stands after the fragment's last change? | Exit status |
|---|---|---|
| release branch merged in, siblings' squashes behind it | yes on a branch: the merge is skipped and the siblings stay behind its second parent (S6 cases) | unchanged |
| merge of the release branch, own commits after it | yes on a branch (S6 second case) | unchanged |
| CI's merge ref of the pull request into the base | **no** — 🔴 1 | unchanged |
| rebase | silent, by the ancestor guard (a stated divergence, 🟢) | unchanged |
| fix range rewrote the fragment, then a later commit | yes: the line is the fragment's last change (S2 last-change case) | unchanged |
| fragment deleted | silent: `tracked_files` at HEAD has no `changelog.md` (read) | unchanged |
| fragment renamed in | seen as touched, the destination is the fragment's path (read) | unchanged |
| behaviour file renamed into `tests/` or `seal/` | **no** — 🟡 2 | unchanged |
| no rounds | silent: `target_shas` of an absent record is empty (case) | unchanged |
| `straight to the PR` | never reaches the arm (case) | unchanged |
| local mode | silent: nothing under the root is committed, so `tracked_files` has no fragment (read) | unchanged |
| behaviour change inside a merge's conflict resolution | not named, and written down as such | unchanged |

**The behaviour-path rule in another repository's layout.** Right for a check
that only prints. A negative rule fails toward *named although nothing was
owed*, which is one notice line; a positive list fails toward silence, and the
issue's own list had already missed `bin/` and `agents/`. A repository whose
tests live in `test/`, `spec/` or `__tests__/` gets notices for test-only
commits, the same class the owner section already names. `seal/` is read from
`optin.HOME`, so the root's name has one source. 🟢.

**Does the notice fire on this item's own branch once records exist?** On a
branch checkout, yes. Executed in the clone: a `round-1.md` at 4a8c0ee2 and a
later commit to `chain_check.py` named that commit as *after the last round*.
In CI, no: the same tree, merged into `origin/release/v0.18.3` the way the
checkout does it, printed nothing (🔴 1). The `round-record` on PATH is the
installed 0.18.2, which has no arm, so this cycle's `close` and `round-record
seal` print nothing either unless the tree's `round_record.py` is run. Until
🔴 1 is fixed, no reader of this release cycle would show the notice for this
item.

**The `agents/smith.md` RIDER re-stamp.** Holds (executed). `rider_check.py`
at the target: 20 ok, 0 drifted, 0 broken. The three measurements re-taken
against `hooks/commit-review-gate.py` at both the target and the base: the
waiver line alone in a heredoc body gives one invocation from
`commit_invocations`, the line with everything above it gives one, and
`_hides_a_commit` is true for the file. These are the numbers the stamp and
the ledger notes record (one, one, true).

**The smith's other claims.** The 25 mutations and the per-case red runs are
the smith's account, and I did not re-run them. What I did check: the cases
exist as described, the S7 guards each have a case that reaches them, and the
probe cases B and D above are red at the target, which no existing case is.

## Regression tests to plant

- `tests/test_a_fragment_left_behind_is_named.py`: a case that builds CI's
  merge ref and asserts the item's fix is named and the sibling's squash is
  not (🔴 1). Red at 4a8c0ee2: probe B printed the sibling and not the fix.
- `tests/test_a_fragment_left_behind_is_named.py`: a case that moves
  `hooks/x.py` under `tests/` and asserts the commit is named with
  `hooks/x.py` (🟡 2). Red at 4a8c0ee2: probe D printed nothing.

## Facts for the evidence ledger

- The arm's first ledger row (S1, S5, S8, S10) says it names *every
  first-parent, non-merge commit after round 1's first `Target SHA`*. That is
  true of a branch checkout. In a `pull_request` run the first parent is the
  base, so the row needs either the fix of 🔴 1 or the qualification.
- The S2–S6 row says *a merge of the base is skipped and the sibling's commits
  stay off the first-parent walk*. Also true only on a branch checkout; on the
  merge ref the sibling's commits ARE the first-parent walk.

## Carried, not re-established

- That `round_record.py` `run_check` runs `chain_check.main` in process with
  `--worktree` (read once at `run_check`, not re-run).
- The measurement tables in `spec.md` (42 work items, 24 would print) — the
  framer's, not re-taken; they decide notice against refusal and nothing here
  turns on their exact values.
- The 21 `Re-read ·` ledger rows — not re-read row by row; `bin/evidence-check
  --strict .` exit 0 is the orchestrator's run, not mine.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | in CI the first-parent walk follows the base (the checkout is the pull request merged into the base), so the notice names siblings' squashes and never the item's own commits | `skills/code-review/scripts/chain_check.py:4187` | open | executed: branch checkout names the fix; the merge ref names nothing with the base unmoved, and names the sibling's squash, for a lagging and an honest item, once one landed. `docs/the-record-layout.md:102` and the fragment say it reaches a person in CI |
| 🟡 2 | a behaviour file moved under `tests/` or `seal/` is not named: `--name-only` lists a rename's destination alone, and rename detection follows the reader's `diff.renames` | `skills/code-review/scripts/chain_check.py:4184` | open | executed: `R100 hooks/big.py tests/big.py`, no notice. Not among the docstring's stated blind spots |
| ⬜ 3 | the owner section and the fragment name two attributions; the notice also writes *outside every round's fix range* | `docs/the-record-layout.md:97` | open | read; `changelog.md:9` carries the same sentence |
| 🟢 | the silent state for a round 1 target HEAD does not descend from | `skills/code-review/scripts/chain_check.py:4255` | confirmed | a rebase leaves the old target resolving; the guard's case was corrected until its mutation went red; both prose carriers list it |
| 🟢 | the first SHA of a two-SHA `Target SHA` is the build's end | `skills/code-review/scripts/chain_check.py:4253` | confirmed | the second is a HEAD that moved mid-review (`templates/sdd-round.md`), so the first reads more commits, never fewer; pinned by a case |
| 🟢 | the `agents/smith.md` RIDER re-stamp | `agents/smith.md:122` | confirmed | executed: `rider_check.py` 20 ok; one, one and true at both the target and the base |
| 🟢 | owner section, three links and the `RULES` row | `tests/test_the_rules_have_one_owner.py:296` | confirmed | executed: the three narrow modules, 229 passed |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q tests/test_a_fragment_left_behind_is_named.py tests/test_the_rules_have_one_owner.py tests/test_chain_check_at_the_pull_request.py` at 4a8c0ee2 | 229 passed |
| `python3 .github/scripts/rider_check.py --root .` at 4a8c0ee2 | exit 0; 20 ok, 0 drifted, 0 broken |
| `bin/fold-check` at 4a8c0ee2 | exit 0; 170 statements in 18 documents |
| probe A — scratch repository, a lagging fix, base unmoved; checked on `feature`, then on a `--no-ff` merge of the head into a detached `base` (CI's merge ref) | branch: the fix named in round 1's fix range; merge ref: nothing |
| probe B — as A, plus a sibling commit to `hooks/sibling.py` on `base` | branch: the fix named; merge ref: the sibling named, *after the last round*, the fix not named |
| probe C — fragment brought along in the fix commit, a sibling on `base` | branch: nothing; merge ref: the sibling named |
| probe D — a behaviour file moved under `tests/` after the fragment's last change | `R100`, nothing named |
| probe E — the RIDER's three numbers at 4a8c0ee2 and a3aa139a, via `commit_invocations` and `_hides_a_commit` | 1, 1, true at both |
| own-branch probe — in the clone, a `round-1.md` at 4a8c0ee2 and a later commit to `chain_check.py`; then the same HEAD merged into `origin/release/v0.18.3` | branch: the commit named *after the last round*; merge ref: nothing |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle (contract §2) |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🔴 1

In `skills/code-review/scripts/chain_check.py`, add above `commits_after`:

```python
def walk_tip(root, target):
    """The commit the walk ends at: HEAD, or the pull request's own head
    where HEAD is the merge a `pull_request` checkout makes of it.

    `actions/checkout` with no `ref:` checks a pull request out as its head
    already merged into the base, and that merge's FIRST parent is the base.
    A first-parent walk from it reads the base's commits since the fork -- a
    sibling's squash -- and never the work item's own. So where HEAD is a
    merge whose first parent does not descend from round 1's target, the
    parent that does is the branch, and the walk starts there.
    """
    line = git(root, "rev-list", "--parents", "-n", "1", "HEAD") or ""
    parents = line.split()[1:]
    if len(parents) > 1 and not is_ancestor(root, target, parents[0]):
        for parent in parents[1:]:
            if is_ancestor(root, target, parent):
                return parent
    return "HEAD"
```

Give `commits_after` the tip:

```python
def commits_after(root, target, tip="HEAD"):
    """[(full, short, paths)], oldest first: the first-parent, non-merge
    commits in `<target>..<tip>` and the paths each changed, or None."""
    out = git(
        root,
        "log",
        "--first-parent",
        "--no-merges",
        "--no-renames",
        "--name-only",
        "-z",
        "--format=%x01%H %h",
        f"{target}..{tip}",
    )
```

And in `fragment_left_behind`:

```python
    tip = walk_tip(root, target)
    commits = commits_after(root, target, tip) or []
```

```python
    after = set((git(root, "rev-list", f"{end}..{tip}") or "").split()) if end else set()
```

The case, in `tests/test_a_fragment_left_behind_is_named.py` under S6:

```python
def ci_merge_ref(repo):
    """What `actions/checkout` gives a pull request: its head merged into the
    base, with the base as the merge's FIRST parent."""
    head = git(repo, "rev-parse", "feature").stdout.strip()
    git(repo, "switch", "-q", "--detach", "base")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "merge",
        "-q",
        "--no-ff",
        "-m",
        "Merge head into base",
        head,
    )


def test_the_ci_merge_ref_names_the_items_commit_and_not_the_siblings(
    repo, monkeypatch, capsys
):
    """CI reads the pull request merged into the base. The first-parent walk
    from that merge is the base's, so without the tip it names the sibling's
    squash and never the item's own fix."""
    target = built(repo)
    start = open_round(repo, 1, target)
    fix = change(repo, "hooks/x.py", message="fix")
    close_round(repo, 1, target, start, fix)
    git(repo, "switch", "-q", "base")
    sibling = change(repo, "hooks/sibling.py", message="a sibling's squash")
    git(repo, "switch", "-q", "feature")
    ci_merge_ref(repo)

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, f"the merge ref hid the item's own fix:\n{out}"
    assert fix[:7] in line and "round 1's fix range" in line, line
    assert sibling[:7] not in line, line
```

### 🟡 2

`--no-renames` in `commits_after`, as in the 🔴 1 block above. The case:

```python
def test_a_behaviour_file_moved_under_tests_is_named(repo, monkeypatch, capsys):
    """A rename is listed by its destination alone unless renames are off,
    so a hook moved under `tests/` left what ships and was never named."""
    target = built(repo)
    open_round(repo, 1, target)
    (repo / "tests").mkdir(exist_ok=True)
    git(repo, "mv", "hooks/x.py", "tests/x.py")
    moved = commit(repo, "move the hook under tests")

    _code, out = judged(repo, monkeypatch, capsys)
    line = notice(out)
    assert line is not None, out
    assert moved[:7] in line and "hooks/x.py" in line, line
```

### ⬜ 3

`docs/the-record-layout.md`, the sentence at lines 97-98:

```
changed. Each is attributed to the round whose `Fix range` holds it, to
*after the last round*, or to *outside every round's fix range* for a commit
between two rounds' ranges. It prints and never refuses, which is the
measurement
```

And `changelog.md`, the sentence at lines 8-9:

```
  one notice. Each is listed with its short SHA, up to three of its paths,
  and the round whose `Fix range` holds it, *after the last round*, or
  *outside every round's fix range*. The
```

Needs a fix: yes — 🔴 1 (in CI the walk follows the base, so the notice names
siblings' squashes and never the item's own commits) and 🟡 2 (a behaviour file
renamed under `tests/` or `seal/` is not named).

Loses a record or crashes: no

## Proof block

Opened: `seal/specs/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named/`
`spec.md`, `overview.md`, `routing.md`, `phases/phase-1.md`, `phase-2.md`,
`phase-3.md`, `changelog.md`;
`seal/ledger/1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named.md`;
the diff a3aa139a..4a8c0ee2 of `skills/code-review/scripts/chain_check.py`,
`agents/smith.md`, `docs/the-record-layout.md`, `skills/implement/SKILL.md`,
`skills/code-review/orchestration.md`, `tests/test_the_rules_have_one_owner.py`;
`chain_check.py` `main`, `git`, `tracked_files`, `worktree_files`,
`read_record`, `round_records`, `is_ancestor`, `resolves_to`, `target_shas`,
`pull_request_state`, `FIX_RANGE_RE`; `tests/test_a_fragment_left_behind_is_named.py`
(whole); `.github/workflows/hygiene.yml` (checkout and the chain-check step);
`round_record.py` `under_tests` and `run_check`; `hooks/commit-review-gate.py`
`_hides_a_commit` and `commit_invocations`; the head of
`.github/scripts/rider_check.py`; `templates/sdd-round.md` (the `Fix range`
row); `agents/smith.md` lines 60-125.
Not opened: `plan.md`, `questions.md`, the three hygiene modules the
orchestrator ran.
