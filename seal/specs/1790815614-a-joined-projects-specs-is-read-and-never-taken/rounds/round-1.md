# 1790815614-a-joined-projects-specs-is-read-and-never-taken — review round 1

| Field | Value |
|---|---|
| Target SHA | 9e120b0a2228f43bff0897007b228da15fa55be2 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 700 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `c35317119feb0f1d7d6f2b8be2b8f5ce736dced7..838de55a76ee172cc9d5bc3c0bc8714aafd6404e`, 4 commits |
| Contract changes | unmarked → main, round-1-report.md, round-1.md |
| New units | tracked_marks (depth 1); test_a_routing_md_deeper_than_directly_under_is_not_a_mark (depth 1); test_a_mark_git_does_not_track_is_not_a_mark (depth 1) |
| Needs a fix | yes — 🟡 1, the hook's marks read from the disk, so an empty or ignored `rounds/` moves a team's directory |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 targets `9e120b0a` and the diff `cd24f516..9e120b0a`, the whole build. The change rewrites a session-start hook that writes to a person's tree and two checks CI runs, so the round was asked to attack the silent direction first:
1. Whether `root-migrate` can still move or re-point a team directory, or leave a real 0.3.x item behind.
2. Whether the bootstrap text is true to the hook.
3. The `Reference specs` row and resolver, including the build's divergence that a repository with no `seal/` root has no reference roots.
4. That `survivor-check` and `unverified-check` read no team `specs/` as a record and miss none of the plugin's own.
5. The agent and skill sentences, and the apostrophe finding: that no changed file flips the commit gate's reading.
6. The ledger's 58 re-stamped rows and the 0.15.1 C2 correction.
7. The class: every other place that reads a bare `specs/` as the old layout or moves by name.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the hook reads its marks from the disk while its units come from git, so an empty or ignored `rounds/` under a team's id-shaped directory makes it a work item and the hook stages its move | `hooks/root-migrate.py:255` | **fixed** `1e83a80e` | fixed at 1e83a80e; executed: both shapes moved and staged the team directory with a clean `git status`; box 2 and the changelog fragment say it never moves |
| ⬜ 2 | `routing.md` and `rounds/` are filenames, so a team's own `routing.md` under an id-shaped name still moves | `hooks/root-migrate.py:111` | answered | The approved design keeps the marks as file names (`spec.md` §Scope 1, `plan.md` §*Alternatives considered*, approved 2026-10-01). A content-checked mark is a design change for the repository owner. The failure it leaves is a team directory staged by `git mv`, which nothing commits before a person reads `git diff --cached`; read: the approved spec chose filenames; a content mark through `hooks/routing.py` would close it; the repository owner decides |
| ⬜ 3 | both READMEs promise silence to a repository whose `specs/` holds nothing of the plugin's, inside the section whose reader has `.specseal/` and hears a line | `README.md:385` | **fixed** `e30a5d7d` | fixed at e30a5d7d; read against `hooks/root-migrate.py#main`'s tail and the hook docstring's wording |
| ⬜ 4 | the seal README names the marks without the `<unix-seconds>-<slug>` shape the hook also requires | `templates/seal-README.md:51` | **fixed** `e30a5d7d` | fixed at e30a5d7d; read; `seal/README.md:51` carries the same text |
| ⬜ 5 | the no-root rationale says the checks still read the 0.3.x `specs/` as records, while `WORK_ITEM_DIR` no longer does | `hooks/config.py:543` | **fixed** `e30a5d7d` | fixed at e30a5d7d; read; the pool, the range and `unverified-check` still do, and no rootless repository runs the sweep |
| 🟢 | the no-root divergence opens no silent path | `hooks/config.py:551` | confirmed | read: `()` only adds to what both checks read, so an error there is loud; an unreadable `config.md` takes the default, as the template's rule for absent rows says |
| 🟢 | no changed file flips the commit gate's reading, and the smith rider is stamped true | `agents/smith.md:119` | confirmed | executed: 51 files under both gates at both revisions, 0 flips; the rider's 1, 1, True reproduces |
| 🟢 | the ledger re-stamp and the 0.15.1 C2 correction | `seal/releases/0.15.1.md` | confirmed | executed: `evidence-check .` 3224 ok, 0 drifted; read: 58 rows, each with a dated note |
| 🟢 | no real 0.3.x work item is left behind by the marks | `hooks/root-migrate.py:247` | confirmed | executed: every tag `v0.0.1`–`v0.3.0`, no unmarked work item; read: the 0.1–0.3 gate required `routing.md` |
| 🟢 | the new cases exercise the checks for real | `tests/test_a_reference_root_is_read_and_never_taken.py` | confirmed | executed: the hook's marks reverted to the name test and the walk's prune removed, five new cases red; reverted |

## Paste-ready fixes

```python
def tracked_marks(root):
    """The id-shaped names under `specs/` whose mark git TRACKS directly
    under them: `specs/<name>/routing.md`, or a file under
    `specs/<name>/rounds/` -- or None when git cannot say, which `dirty()`
    already refuses, so the fallback below never decides a move.

    The move's units come from git (`tracked_names`), and so do its marks.
    Git tracks no empty directory and no ignored file, so a `rounds/` that
    is either leaves `git status` clean and would otherwise make a team's
    directory a work item (round 1 of #688). `marked` keeps the disk for the
    symbolic-link refusal alone, because git lists nothing behind a link."""
    try:
        r = git(root, "ls-files", "-z", "--", OLD_ITEMS)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    routing, rounds = MARKS
    names = set()
    for path in r.stdout.split("\0"):
        parts = path.split("/")
        if len(parts) < 3 or parts[0] != OLD_ITEMS or not ITEM_RE.match(parts[1]):
            continue
        if (len(parts) == 3 and parts[2] == routing) or (
            len(parts) > 3 and parts[2] == rounds
        ):
            names.add(parts[1])
    return names


def unmarked(root, name, marks):
    """True when `specs/<name>` has a work item's shape and none of the
    marks git tracks: the case the printed line gives its own reason for."""
    return (
        ITEM_RE.match(name) is not None
        and os.path.isdir(under(root, f"{OLD_ITEMS}/{name}"))
        and name not in marks
    )


def old_items(root):
    """(SpecSeal work items under `specs/`, everything else on disk there).

    The first list is what moves and comes from git, each one carrying a
    mark git tracks; the second is what the printed line names as left
    behind and comes from the directory, because what stays on disk is what
    a person will see there.
    """
    marks = tracked_marks(root)
    items = [
        n
        for n in entries(root, OLD_ITEMS)
        if (n in marks if marks is not None else marked(root, n))
    ]
    try:
        names = sorted(os.listdir(under(root, OLD_ITEMS)))
    except OSError:
        names = []
    return items, [n for n in names if n not in items]
```
```python
    _, left = old_items(root)
    marks = tracked_marks(root) or set()
    shaped = [n for n in left if unmarked(root, n, marks)]
```
```python
@pytest.mark.parametrize("ignored", [False, True])
def test_a_rounds_directory_git_does_not_track_is_not_a_mark(hook, repo, ignored):
    """Round 1 of #688. Git tracks no empty directory and no ignored file,
    so a `rounds/` that is either leaves `git status` clean. The marks come
    from git, as the units do, and the team's directory stays."""
    if ignored:
        write(repo, ".gitignore", "rounds/\n")
    plant_team_directory(repo)
    if ignored:
        write(repo, f"specs/{TEAM}/rounds/scratch.md", "# local only\n")
    else:
        os.makedirs(repo / "specs" / TEAM / "rounds")
    assert git(repo, "status", "--porcelain").stdout == ""
    out = message(start(hook, repo))
    assert "moved .specseal/ and 1 work item into seal/" in out, out
    assert LEFT_UNMARKED in out, out
    assert not (repo / "seal" / "specs" / TEAM).exists()
    staged = git(repo, "diff", "--cached", "--name-only").stdout
    assert TEAM not in staged, staged
```

## Executed probes

| What was run | Result |
|---|---|
| the narrow modules for the reference root, the root move, first setup, settle, the survivor sweep and the rider (`bin/test`, six modules) | exit 0, 441 passed |
| the narrow modules for the unverified record, the config front door, the mode row, both editions, the old-root names, one word one meaning, line wrap, and edits through the Edit tool (`bin/test`, eight modules) | exit 0, 362 passed |
| a throwaway probe module in the clone: a team directory with an empty `rounds/`, and one with an ignored `rounds/` | both moved and staged the team directory (red against the target); deleted after the run |
| the same probe module: a run stopped at a taken destination, settled by hand, then resumed | the rows citing the first item were re-pointed; passed |
| a throwaway probe script over all 51 changed files: `commit_invocations` and `_hides_a_commit` under the gate at `cd24f516` and at the target, each file at both revisions, whole and up to the first waiver line | 0 flips; the smith rider's heredoc reading is 1, 1, True under both gates |
| `evidence-check .`, unscoped, in the clone | exit 0; total 3224 ok, 0 drifted, 0 broken, 0 malformed, 0 overflow |
| mutation: `old_items` back to the name test, and the walk's reference-root prune removed; the new cases run | 5 failed (the three B cases, D2's walk, D3's planted case); both files reverted, clone clean |
| `git ls-tree` of every work-item directory under `specs/` at `v0.0.1`, `v0.1.0`, `v0.2.0` and `v0.3.0` | 0 without `routing.md` or `rounds/` |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet — not run by anyone in this round; the sealer's, after the rounds settle |

```python
# a probe module beside tests/test_the_root_migrates_itself.py, run once, deleted
def test_tmp_an_empty_untracked_rounds_dir(hook, repo):
    plant(repo)                                   # tracked spec.md and plan.md
    os.makedirs(repo / "specs" / TEAM / "rounds")
    assert git(repo, "status", "--porcelain").stdout == ""
    out = message(start(hook, repo))
    assert not (repo / "seal" / "specs" / TEAM).exists()   # FAILED: moved

def test_tmp_an_ignored_rounds_dir(hook, repo):
    write(repo, ".gitignore", "rounds/\n")
    plant(repo)
    write(repo, f"specs/{TEAM}/rounds/scratch.md", "# local only\n")
    assert git(repo, "status", "--porcelain").stdout == ""
    out = message(start(hook, repo))
    assert not (repo / "seal" / "specs" / TEAM).exists()   # FAILED: moved
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
