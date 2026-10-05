# 1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named — review round 1

| Field | Value |
|---|---|
| Target SHA | 4a8c0ee2d16d935829d75675048e1b6444703765 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #802 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `f96ea9a21c21e151c51c0f8adc761ae5c7973d1f..65ff34c67f29a3fa67958abb7d29b9c955961cba`, 4 commits |
| Contract changes | commits_after → round-1-report.md, round-1.md, fragment_left_behind |
| New units | walk_tip (depth 1); ci_merge_ref (depth 1); test_the_ci_merge_ref_names_the_items_commit_and_not_the_siblings (depth 1); test_a_merge_on_the_branch_keeps_the_branch_as_the_tip (depth 1); test_of_several_merged_heads_the_one_descending_from_round_one_is_the_tip (depth 1); test_an_honest_fragment_on_the_ci_merge_ref_is_not_named (depth 1); test_a_behaviour_file_moved_out_of_what_ships_is_named (depth 1) |
| Needs a fix | yes — 🔴 1 (in CI the walk follows the base, so the notice names siblings' squashes and never the item's own commits) and 🟡 2 (a behaviour file renamed under `tests/` or `seal/` is not named). |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Spec compliance first against `spec.md` (a notice only, homed in `chain_check`, one question per work item over first-parent non-merge commits after round 1's `Target SHA`, the negative behaviour-path rule, the silent states, the owner section, three links and `RULES` row), then quality: the overview's three divergences on their grounds; the history shapes the arm reads, by construction; the rule in another repository's layout; whether the notice fires on this item's own branch once records exist; the `agents/smith.md` RIDER re-stamp.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | in CI the first-parent walk follows the base (the checkout is the pull request merged into the base), so the notice names siblings' squashes and never the item's own commits | `skills/code-review/scripts/chain_check.py:4187` | **fixed** `71bf2d8a` | fixed at 71bf2d8a; executed: branch checkout names the fix; the merge ref names nothing with the base unmoved, and names the sibling's squash, for a lagging and an honest item, once one landed. `docs/the-record-layout.md:102` and the fragment say it reaches a person in CI |
| 🟡 2 | a behaviour file moved under `tests/` or `seal/` is not named: `--name-only` lists a rename's destination alone, and rename detection follows the reader's `diff.renames` | `skills/code-review/scripts/chain_check.py:4184` | **fixed** `71bf2d8a` | fixed at 71bf2d8a; executed: `R100 hooks/big.py tests/big.py`, no notice. Not among the docstring's stated blind spots |
| ⬜ 3 | the owner section and the fragment name two attributions; the notice also writes *outside every round's fix range* | `docs/the-record-layout.md:97` | **fixed** `65ff34c6` | fixed at 65ff34c6; read; `changelog.md:9` carries the same sentence |
| 🟢 | the silent state for a round 1 target HEAD does not descend from | `skills/code-review/scripts/chain_check.py:4255` | confirmed | a rebase leaves the old target resolving; the guard's case was corrected until its mutation went red; both prose carriers list it |
| 🟢 | the first SHA of a two-SHA `Target SHA` is the build's end | `skills/code-review/scripts/chain_check.py:4253` | confirmed | the second is a HEAD that moved mid-review (`templates/sdd-round.md`), so the first reads more commits, never fewer; pinned by a case |
| 🟢 | the `agents/smith.md` RIDER re-stamp | `agents/smith.md:122` | confirmed | executed: `rider_check.py` 20 ok; one, one and true at both the target and the base |
| 🟢 | owner section, three links and the `RULES` row | `tests/test_the_rules_have_one_owner.py:296` | confirmed | executed: the three narrow modules, 229 passed |

## Paste-ready fixes

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
```python
    tip = walk_tip(root, target)
    commits = commits_after(root, target, tip) or []
```
```python
    after = set((git(root, "rev-list", f"{end}..{tip}") or "").split()) if end else set()
```
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
```
changed. Each is attributed to the round whose `Fix range` holds it, to
*after the last round*, or to *outside every round's fix range* for a commit
between two rounds' ranges. It prints and never refuses, which is the
measurement
```
```
  one notice. Each is listed with its short SHA, up to three of its paths,
  and the round whose `Fix range` holds it, *after the last round*, or
  *outside every round's fix range*. The
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
