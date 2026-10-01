# 1790815614-a-joined-projects-specs-is-read-and-never-taken — review round 3

| Field | Value |
|---|---|
| Target SHA | 1c320c327d124f903e336ed972d76be866c02162 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 700 |
| Broad gate | c8f7fd48 against e83db346; earlier run: d59a8d6b against a340221b; earlier run: 14a1e7d2 against a340221b |
| Fixes checked by | no fixes to check |
| Fix range | `1c320c327d124f903e336ed972d76be866c02162..043c9aa6fc17c40ddb7c0d7ce4ec5d04698f6b1c`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, a 0.3.x work item behind a relative link is named as no work item and stamped over; deferred, since this round commissions nothing |
| Loses a record or crashes | yes — 🟡 1 leaves a 0.3.x work item outside the root with the repository stamped, so no start ever moves it; its files and rows stay intact and readable through the link |

- [x] Pass

## What this round was asked

Round 3 is the verifying round after the run's one reopening, so it ends the run. It targets `1c320c32` and verifies round 2's fix range `52b433f7..affc5544`, three commits. It was asked to re-run round 2's two probes, the corrupt index after a stopped run and a file-by-file move stopped and settled. It was also asked to review the three new cases and the restored disk fallback, and to confirm or refute by execution the smith's own report that a linked work item is no longer moved.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a 0.3.x work item at a relative-link `specs/<id>` has no mark git lists, so the hook leaves it, names it *not a SpecSeal work item*, stamps, and never moves it | `hooks/root-migrate.py:290` | deferred #709 | executed: the target leaves the link, names it under the false reason, stamps, 5 ok 0 broken, the next start silent; `1e83a80e^` and the base move the link, which dangles, 4 ok 1 broken, stamped; the smith's account confirmed; `tracked_marks` is depth 1 per `round-1.md`'s `New units`; this round commissions nothing under the reopening bound |
| ⬜ 2 | a file-by-file resume leaves the item's emptied directory on disk, and the moved line names that item as *not a SpecSeal work item* | `hooks/root-migrate.py:421` | deferred #709 | executed: three settle shapes at the target leave an empty `specs/<item>/` and the false reason; the base leaves it too, under *not tracked*; only the reason is the branch's; nothing tracked and no row is affected |
| ⬜ 3 | `spec.md:203` quotes the reason without *that git tracks*, a carrier of round 2's ⬜ 3 the fix pass missed | `seal/specs/1790815614-a-joined-projects-specs-is-read-and-never-taken/spec.md:203` | answered | `spec.md` is the approved frame and is kept as approved; the hook, the test, the changelog and ledger B1 carry the new reason; read; a correction to the run's paperwork, outside `Needs a fix` |
| ⬜ 4 | the corrected 🟢 F row anchors only `hooks/root-migrate.py#move`, which decides nothing in its corrected claim | `seal/releases/0.4.0.md:292` | deferred #709 | #709 — The 🟢 F row is re-anchored by the change #709 makes to `tracked_marks`, which is where its claim is decided; read against `hooks/root-migrate.py#tracked_marks`, `#old_items` and `#main`; a correction to the run's paperwork, outside `Needs a fix` |
| 🟢 | round 2's first finding is closed — a git that cannot list the marks is refused as dirty and stamps nothing, and the next start moves the item | `hooks/root-migrate.py:319` | confirmed | executed: P2 at the target, `1e83a80e^` and the base alike; seen red with the fallback removed; class read across every reader of `tracked_marks` |
| 🟢 | round 2's second finding is closed — a stop at any file but the last mark resumes, whichever copy is kept | `hooks/root-migrate.py:416` | confirmed | executed: four stop shapes, each settled both ways, all resumed but the last-mark `git rm <src>`, which is #704; seen red with the sort removed |
| 🟢 | round 2's third finding is closed in the hook, the case, the changelog and B1 | `hooks/root-migrate.py:674` | confirmed | read; the remaining carrier is ⬜ 3 |
| 🟢 | round 2's fourth finding is closed — B5 says what the hook does | `seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md` | confirmed | read against `hooks/root-migrate.py#old_items` and `#main`; executed by P2 and P2b; `evidence-check .` clean |
| carried | round 2's fifth finding — a resume with nothing left to move re-points nothing | `hooks/root-migrate.py:598` | deferred #704 | already deferred in round 2; executed: a stop at `routing.md` settled with `git rm <src>` is silent with 1 ok 3 broken at all three versions |
| 🟢 | the disk fallback in `old_items` does not bring back round 1's first finding | `hooks/root-migrate.py:319` | confirmed | executed: P2b, a team directory with an empty `rounds/` beside a corrupt index, refused, then left and unstaged after the repair; both earlier versions moved it |
| 🟢 | the three new cases are seen red against the defect each exists for | `tests/test_the_root_migrates_itself.py:827` | confirmed | executed: 6 of 6 parameters failed with the fallback removed and the sort removed; reverted with `git checkout` |

## Paste-ready fixes

```python
    linked = [
        n
        for n in old_items(root)[1]
        if os.path.islink(under(root, f"{OLD_ITEMS}/{n}")) and marked(root, n)
    ]
    if linked:
        # One entry instead of the whole root: git lists the link as one blob
        # and no mark behind it, so `tracked_marks` cannot see the work item
        # and the line would name it as no work item at all.
        say(
            f"specseal: {', '.join(f'{OLD_ITEMS}/{n}' for n in linked)} — a "
            "symbolic link holding a work item, which git tracks as the link and "
            'not as its files — not moving it. Move by hand (README, "Coming up '
            'from 0.3.x") and remove the link.'
        )
        return
```
```python
LINKED = "1788000002-linked-item"


def test_a_linked_work_item_is_refused_not_named_as_no_work_item(hook, repo):
    """Round 3 of #688. Git lists a linked `specs/<id>` as one blob and no
    mark behind it, so the item was named as no work item and stamped over."""
    write(repo, "vault-item/routing.md", ROUTING)
    write(repo, "vault-item/rounds/round-1.md", ROUND)
    os.symlink("../vault-item", repo / "specs" / LINKED)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "a work item behind a relative link")
    out = message(start(hook, repo))
    assert f"specs/{LINKED} — a symbolic link holding a work item" in out, out
    assert "not a SpecSeal work item" not in out, out
    assert not stamped(hook, repo)
    assert os.path.islink(repo / "specs" / LINKED)
    assert (repo / ".specseal" / "map.md").is_file()
    assert not (repo / "seal").exists()
```
```python
    # `dirs` is listed before the walk descends, so a parent whose
    # subdirectories were just removed still names them: try every
    # directory bottom-up and let `rmdir` refuse the ones not empty.
    for here, _dirs, _files in os.walk(under(root, src), topdown=False):
        try:
            os.rmdir(here)
        except OSError:
            pass
```
```python
def test_a_resumed_item_leaves_no_directory_behind(hook, repo):
    """Round 3 of #688. The walk listed `rounds/` before removing it, so the
    item's directory stayed empty and the line named the moved item as left."""
    write(repo, f"specs/{ITEM}/spec.md", "# the old spec\n")
    write(repo, f"seal/specs/{ITEM}/spec.md", "# the newer spec\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "both spec.md")
    message(start(hook, repo))
    git(repo, "rm", "-q", f"specs/{ITEM}/spec.md")
    out = message(start(hook, repo))
    assert "moved 1 work item into seal/" in out, out
    assert f"specs/{ITEM}" not in out, out
    assert not (repo / "specs" / ITEM).exists()
```
```markdown
`; left specs/1788000001-team-thing where it is (no routing.md or rounds/
that git tracks — not a SpecSeal work item)`, beside the existing `(not
tracked as a SpecSeal work item)` for a non-item name.
```
```text
| 🟢 F · ... | `hooks/root-migrate.py#move@04ff113f`, `hooks/root-migrate.py#tracked_marks@<hash>`, `hooks/root-migrate.py#main@<hash>` | ... |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_root_migrates_itself.py -q` in the clone at the target | exit 0, 58 passed |
| a throwaway probe module, P2: `.specseal/` moved and committed, the item still under `specs/`, `.git/index` overwritten, one start, the index restored, one start; against the target, `1e83a80e^` and the base | all three: the first start refused as uncommitted changes and did not stamp; the second moved 1 work item and re-pointed 3 rows, 4 ok 0 broken |
| the same module, P2b: P2 plus a team directory with a tracked `notes.md` and an empty `rounds/` on disk | target: refused, then the item moved and the team directory left, named, nothing of it staged; `1e83a80e^` and the base: refused, then moved 2 work items, the team's `notes.md` staged into `seal/specs/` |
| the same module, P3: four stop shapes (`spec.md`, `b.md` after `a.md`, `rounds/round-1.md`, `routing.md`), each settled by `git rm <dst>` and by `git rm <src>`, then one start and `evidence-check` | target: the table under *Round 2's verdicts*; the base: `spec.md` and `routing.md` settled by `git rm <src>` both silent with 1 ok 3 broken |
| the same module, P3 at the target, listing `specs/<item>/` after the resume | an empty `specs/<item>/` in three settles, named in the line under *no routing.md or rounds/ that git tracks* |
| the same module, P4: `specs/1788000002-linked-item → ../vault-item` holding `routing.md` and `rounds/round-1.md`, a row citing the file through the link, one start, commit, one start | target: `.specseal/` moved alone, the link left and named *not a SpecSeal work item*, 5 ok 0 broken, stamped, the second start silent; `1e83a80e^` and the base: the link moved to `seal/specs/` and unresolvable, 4 ok 1 broken, stamped, the second start silent |
| mutation: `old_items` on `n in (marks or set())` and `move` without the sort, the three new cases | 6 failed, 52 deselected; reverted with `git checkout` |
| both proposed fixes applied in the clone, the module plus the two proposed cases | exit 0, 60 passed; with the fixes stashed, the two proposed cases: 2 failed; reverted with `git checkout` |
| `bin/evidence-check .`, unscoped, in the clone at the target | exit 0; total 3258 ok, 0 drifted, 0 broken, 0 malformed, 0 overflow |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet — nobody ran it in this round; it is the sealer's, after the rounds settle |

```python
# P4, run once against three versions of the hook, deleted
write(repo, "vault-item/routing.md", ROUTING)
write(repo, "vault-item/rounds/round-1.md", ROUND)
os.symlink("../vault-item", repo / "specs" / "1788000002-linked-item")
# plus a ledger fragment under .specseal/map/ citing specs/1788000002-linked-item/rounds/round-1.md
git(repo, "add", "-A"); git(repo, "commit", "-qm", "a linked item")
first = message(start(hook, repo))
# target: "... left specs/1788000002-linked-item where it is (no routing.md or
#          rounds/ that git tracks — not a SpecSeal work item)) ..."; stamped; 5 ok 0 broken
```
```python
# P3, the empty directory, run once at the target, deleted
write(repo, f"specs/{ITEM}/spec.md", "# old spec\n")
write(repo, f"seal/specs/{ITEM}/spec.md", "# the newer one\n")
git(repo, "add", "-A"); git(repo, "commit", "-qm", "fixture")
message(start(hook, repo))                     # stopped at specs/<item>/spec.md
git(repo, "rm", "-q", f"specs/{ITEM}/spec.md"); git(repo, "commit", "-qm", "settled")
second = message(start(hook, repo))
# "moved 1 work item ... left specs/<item> where it is (no routing.md or rounds/
#  that git tracks — not a SpecSeal work item)"; specs/<item>/ exists and is empty
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/root-migrate.py:255` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/root-migrate.py:111` | round 1's ⬜ 2 — answered |
| round-1 | `README.md:385` | round 1's ⬜ 3 — fixed |
| round-1 | `templates/seal-README.md:51` | round 1's ⬜ 4 — fixed |
| round-1 | `hooks/config.py:543` | round 1's ⬜ 5 — fixed |
| round-1 | `hooks/config.py:551` | round 1's 🟢 — confirmed |
| round-1 | `agents/smith.md:119` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.15.1.md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/root-migrate.py:247` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_reference_root_is_read_and_never_taken.py` | round 1's 🟢 — confirmed |
| round-2 | `hooks/root-migrate.py:278` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/root-migrate.py:398` | round 2's 🟡 2 — fixed |
| round-2 | `hooks/root-migrate.py:654` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md` | round 2's ⬜ 4 — answered |
| round-2 | `hooks/root-migrate.py:569` | round 2's ⬜ 5 — deferred |
| round-2 | `hooks/root-migrate.py:313` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790815614-a-joined-projects-specs-is-read-and-never-taken/plan.md:123` | round 2's 🟢 — confirmed |
| round-2 | `hooks/config.py:548` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_root_migrates_itself.py:813` | round 2's 🟢 — confirmed |
| round-2 | `hooks/root-migrate.py:591` | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.12.0.md:109` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — a work item behind a relative link is named as no work item and stamped over; in `tracked_marks`, a unit round 1's fixes created | a new issue against `hooks/root-migrate.py#tracked_marks` and `#main`, with the paste-ready fix and case below and the submodule shape named | the repository owner, who files and schedules it; the finding is the branch's own unit, so the owner may instead take it on this branch |
| ⬜ 2 — a file-by-file resume leaves an empty item directory and names it under the branch's reason | the same new issue, or one of its own against `hooks/root-migrate.py#move` | the repository owner, who files it |
| ⬜ 5 of round 2 — a resume with nothing left to move re-points nothing | #704, already deferred in round 2 | the repository owner, who scheduled #704 |
