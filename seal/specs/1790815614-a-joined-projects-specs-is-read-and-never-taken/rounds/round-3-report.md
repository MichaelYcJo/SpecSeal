# 1790815614-a-joined-projects-specs-is-read-and-never-taken — round 3 report

Ran by specseal:warden on claude-opus-5-5. Target SHA
`1c320c327d124f903e336ed972d76be866c02162`. This is the verifying round
after the run's one reopening, so it ends the run whatever it finds. Its
target is round 2's fix range
`52b433f7e2043d939de6ab48994bf161b12389bd..affc55448579bbbb535564fa22d6d8d1f6a47f86`
(three commits). All work was done in a `git clone --no-local` at
`<scratchpad>/1790815614/round-3/clone`, checked out at the target.

## What this round found, in causal order

Round 2's two blocking-class findings are closed. Both were re-run as
round 2 ran them, against the target, against the hook before round 1's fix
pass (`1e83a80e^`) and against the base (`cd24f516`).

- **A corrupt index after a stopped run** is refused as uncommitted changes
  and stamps nothing. The next start, after the index is restored, moves the
  item and re-points 3 rows, 4 ok and 0 broken. Executed.
- **A file-by-file move stopped inside an item** now resumes for every stop
  except one at the item's last mark. Executed in four shapes, each settled
  both ways the hook's line offers. The one stop that still strands is the
  ground #704 already holds.

The smith's own report is confirmed by execution, and it is the one
finding this round opens that needs a fix (🟡 1):

1. **A work item behind a relative link is told it is no work item, and
   stamped over** (🟡 1). `specs/<id> → ../vault-item`, with a real
   `routing.md` and `rounds/round-1.md` behind the link, is committed as one
   blob. Git lists `specs/<id>` and nothing under it, so `tracked_marks`
   finds no mark. At the target the hook moved `.specseal/` alone, left the
   link where it was and named it as *no routing.md or rounds/ that git
   tracks — not a SpecSeal work item*. It then stamped the repository, and
   the next start was silent. The rows citing the item keep resolving
   through the link: 5 ok, 0 broken. At `1e83a80e^` and at the base the
   link was moved into `seal/specs/`, where it no longer resolves: 4 ok,
   1 broken, also stamped. The change is from loud to silent. Before, the
   checker reported the dangling link. Now, the one line a person reads
   says the item is not SpecSeal's, and no start ever moves it again. The
   cause is in `tracked_marks`, a unit round 1's fixes created (depth 1 in
   `round-1.md`'s `New units`). The repository already refuses a linked
   `.specseal/` and a linked `specs/` holding work items. The paste-ready
   fix gives a linked entry the same refusal, and it was executed: the
   module and both proposed cases passed (60), and both cases fail without
   it.

What reads wrong while the files land where they should:

2. **A file-by-file resume leaves the item's emptied directory behind, and
   the line names the item it just moved as left** (⬜ 2). `move` removes
   empty directories with a bottom-up `os.walk`. That walk lists `dirs`
   before it descends, so a parent whose `rounds/` was just removed still
   names it, is skipped, and stays on disk empty. `old_items` then lists the
   empty directory as left. The branch's `unmarked` gives it the reason *no
   routing.md or rounds/ that git tracks — not a SpecSeal work item*, in the
   same line that says *moved 1 work item*. Executed at the target for a stop
   at `spec.md` settled with `git rm <src>`, for a stop after one file settled
   either way, and for a stop at `routing.md` settled with `git rm <dst>`. The
   empty directory predates the branch: the base leaves it too, under *not
   tracked as a SpecSeal work item*. Only the reason is new. Git tracks
   nothing in the directory, so no row and no file is affected.
3. `spec.md:203` still quotes the reason without *that git tracks* (⬜ 3).
   Round 2's report named it among the carriers. The fix pass corrected the
   hook, the test's `LEFT_UNMARKED`, the changelog fragment and ledger row
   B1, but not this one. This is a correction to the run's paperwork.
4. The corrected 🟢 F row in `seal/releases/0.4.0.md:292` anchors only
   `hooks/root-migrate.py#move` (⬜ 4). Its corrected claim is decided by
   `tracked_marks`, `old_items` and `main`, and not by `move`. So a fix to
   finding 1 would leave the row reading OK while its claim turns false.
   This is also a correction to the run's paperwork.

## Round 2's verdicts, each answered

- **🟡 1, fixed at `fa38bbbc`: closed.** `tracked_marks` answers `None` where
  git cannot list (`hooks/root-migrate.py:281`, `:283`), and `old_items`
  then reads the marks from the disk (`:319`). So `units` stays non-empty,
  `main` passes its stamp branch, and `dirty()` refuses the run. Executed:
  P2 above, at all three versions, with the same result at each. The class
  was enumerated as every reader of `tracked_marks`. `old_items` is the one
  that decides the move. `main:668` reads it only for the printed reason,
  as `or set()`, after the move has run. `tracked_names`, `entries` and
  `dirty()` already answered `None` or refused. Seen red: with the
  fallback put back to `n in (marks or set())`, both parameters of
  `test_a_git_that_cannot_list_the_marks_stamps_nothing` fail.
- **🟡 2, fixed at `fa38bbbc`: closed except at the last mark.** `move`
  sorts the file list by `a_mark`, so marks move last
  (`hooks/root-migrate.py:416`). Executed at the target, each shape settled
  both ways:

  | Stop at | `git rm <dst>` | `git rm <src>` |
  |---|---|---|
  | `spec.md` | resumed, 4 ok 0 broken | resumed, 4 ok 0 broken |
  | `b.md`, after `a.md` moved | resumed, 5 ok 0 broken | resumed, 5 ok 0 broken |
  | `rounds/round-1.md`, the first mark | resumed, 4 ok 0 broken | resumed, 3 ok 1 broken |
  | `routing.md`, the last mark | resumed, 4 ok 0 broken | silent, 1 ok 3 broken |

  The `rounds/` row's 1 broken is correct: the person kept the newer file,
  which does not hold the heading that row cites. The last cell is #704's
  ground, as ledger row B6 says. Compared with the base, `spec.md` settled
  with `git rm <src>` moved from 3 broken to 0, so the fix also narrowed
  #704. Seen red: with the sort removed, both parameters of each new
  move case fail.
- **⬜ 3, fixed at `fa38bbbc`: closed in the hook, the case, the changelog
  and B1, and open in `spec.md:203`** (⬜ 3 above). Read.
- **⬜ 4, answered at `affc5544`: closed.** B5 now says the disk stands in
  only where git cannot list, and that `dirty()` then refuses because the
  units stay non-empty. Read against `hooks/root-migrate.py#old_items` and
  `#main`. Executed by P2 and P2b. `evidence-check .` is clean.
- **⬜ 5, deferred: still deferred, now at #704.** Executed as the last
  cell of the table above, silent with 3 broken at all three versions. Its
  home is open.

## New units, judged as code

- `test_a_git_that_cannot_list_the_marks_stamps_nothing`: sound. Both
  parameters are red against the fallback removed. In the *ls-files raises*
  parameter, `dirty()`'s own `tracked_names` raises too, and that is the arm
  that refuses. This is correct, because the two arms read the same command.
- `test_a_move_stopped_inside_an_item_resumes_whichever_file_is_kept`:
  red against the sort removed, both parameters. It does not assert that
  `specs/<item>/` is gone after the *newer one* settle, which is why ⬜ 2's
  leftover passes it. The proposed case covers that.
- `test_an_item_with_one_mark_stopped_inside_resumes`: red against the
  sort removed, both marks.
- The disk fallback in `old_items`, which round 2's 🟡 1 restored, does not
  bring back round 1's 🟡 1. P2b put a team directory with a tracked
  `notes.md` and an empty `rounds/` on disk next to a corrupt index. The
  target refused, stamped nothing, and after the repair left the team
  directory in place, named and unstaged. Both earlier versions moved it.
  One shape is read rather than executed: `tracked_marks` failing while
  `tracked_names` answers. They are the same `git ls-files -z -- specs`, so
  only a transient between two calls reaches it. Not reported as a finding.

## Class enumerated for 🟡 1

The class is any `specs/<id>` whose marks are on disk while git lists none
under it. Each member was read against `tracked_marks`:

- a relative link: executed, as above.
- an absolute link: the same branch in `tracked_marks`, and the proposed
  fix's `os.path.islink` covers it. Read.
- a submodule at `specs/<id>`: git lists one gitlink, so it is the same
  shape. The proposed fix does not cover it, and no 0.3.x layout is known to
  have used one. Read, and named here so the issue can carry it.

## Regression tests to plant

The destination is `tests/test_the_root_migrates_itself.py`. Both cases are
fenced under *Paste-ready fixes*, and both were executed: red at the target,
and green with the fixes applied in the clone together with the module's
58 cases.

## Facts for the evidence ledger

- Once 🟡 1 is fixed, the 0.4.0 🟢 F row's claim changes again. Its anchor
  should then name `hooks/root-migrate.py#main` and `#tracked_marks` beside
  the new case (⬜ 4).
- B6's last sentence is confirmed by execution: a stop at the last mark,
  settled with `git rm <src>`, is silent with 3 broken.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a 0.3.x work item at a relative-link `specs/<id>` has no mark git lists, so the hook leaves it, names it *not a SpecSeal work item*, stamps, and never moves it | `hooks/root-migrate.py:290` | deferred new issue | executed: the target leaves the link, names it under the false reason, stamps, 5 ok 0 broken, the next start silent; `1e83a80e^` and the base move the link, which dangles, 4 ok 1 broken, stamped; the smith's account confirmed; `tracked_marks` is depth 1 per `round-1.md`'s `New units`; this round commissions nothing under the reopening bound |
| ⬜ 2 | a file-by-file resume leaves the item's emptied directory on disk, and the moved line names that item as *not a SpecSeal work item* | `hooks/root-migrate.py:421` | deferred new issue | executed: three settle shapes at the target leave an empty `specs/<item>/` and the false reason; the base leaves it too, under *not tracked*; only the reason is the branch's; nothing tracked and no row is affected |
| ⬜ 3 | `spec.md:203` quotes the reason without *that git tracks*, a carrier of round 2's ⬜ 3 the fix pass missed | `seal/specs/1790815614-a-joined-projects-specs-is-read-and-never-taken/spec.md:203` | open | read; a correction to the run's paperwork, outside `Needs a fix` |
| ⬜ 4 | the corrected 🟢 F row anchors only `hooks/root-migrate.py#move`, which decides nothing in its corrected claim | `seal/releases/0.4.0.md:292` | open | read against `hooks/root-migrate.py#tracked_marks`, `#old_items` and `#main`; a correction to the run's paperwork, outside `Needs a fix` |
| 🟢 | round 2's first finding is closed — a git that cannot list the marks is refused as dirty and stamps nothing, and the next start moves the item | `hooks/root-migrate.py:319` | confirmed | executed: P2 at the target, `1e83a80e^` and the base alike; seen red with the fallback removed; class read across every reader of `tracked_marks` |
| 🟢 | round 2's second finding is closed — a stop at any file but the last mark resumes, whichever copy is kept | `hooks/root-migrate.py:416` | confirmed | executed: four stop shapes, each settled both ways, all resumed but the last-mark `git rm <src>`, which is #704; seen red with the sort removed |
| 🟢 | round 2's third finding is closed in the hook, the case, the changelog and B1 | `hooks/root-migrate.py:674` | confirmed | read; the remaining carrier is ⬜ 3 |
| 🟢 | round 2's fourth finding is closed — B5 says what the hook does | `seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md` | confirmed | read against `hooks/root-migrate.py#old_items` and `#main`; executed by P2 and P2b; `evidence-check .` clean |
| carried | round 2's fifth finding — a resume with nothing left to move re-points nothing | `hooks/root-migrate.py:598` | deferred #704 | already deferred in round 2; executed: a stop at `routing.md` settled with `git rm <src>` is silent with 1 ok 3 broken at all three versions |
| 🟢 | the disk fallback in `old_items` does not bring back round 1's first finding | `hooks/root-migrate.py:319` | confirmed | executed: P2b, a team directory with an empty `rounds/` beside a corrupt index, refused, then left and unstaged after the repair; both earlier versions moved it |
| 🟢 | the three new cases are seen red against the defect each exists for | `tests/test_the_root_migrates_itself.py:827` | confirmed | executed: 6 of 6 parameters failed with the fallback removed and the sort removed; reverted with `git checkout` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — a work item behind a relative link is named as no work item and stamped over; in `tracked_marks`, a unit round 1's fixes created | a new issue against `hooks/root-migrate.py#tracked_marks` and `#main`, with the paste-ready fix and case below and the submodule shape named | the repository owner, who files and schedules it; the finding is the branch's own unit, so the owner may instead take it on this branch |
| ⬜ 2 — a file-by-file resume leaves an empty item directory and names it under the branch's reason | the same new issue, or one of its own against `hooks/root-migrate.py#move` | the repository owner, who files it |
| ⬜ 5 of round 2 — a resume with nothing left to move re-points nothing | #704, already deferred in round 2 | the repository owner, who scheduled #704 |

## Paste-ready fixes

### 🟡 1 — refuse a linked work item as the linked roots are refused

In `hooks/root-migrate.py#main`, after the linked-`specs/` refusal and before
`dirty()`:

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

The case, in `tests/test_the_root_migrates_itself.py`:

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

The 0.4.0 🟢 F row and both READMEs' by-hand section would then describe a
refusal, which is a sentence a person reads (§14 of the contract).

### ⬜ 2 — remove every emptied directory, the parent included

In `hooks/root-migrate.py#move`, replacing the final walk:

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

The case:

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

### ⬜ 3 — the spec's quoted line

```markdown
`; left specs/1788000001-team-thing where it is (no routing.md or rounds/
that git tracks — not a SpecSeal work item)`, beside the existing `(not
tracked as a SpecSeal work item)` for a non-item name.
```

### ⬜ 4 — the 0.4.0 🟢 F row's anchor

Add `hooks/root-migrate.py#tracked_marks` and `hooks/root-migrate.py#main` to
the row's coordinate cell beside `#move`, stamped at their current hashes with
`evidence-check --reverify`. Or, if 🟡 1 is fixed first, replace the row's
claim with the refusal and anchor it on the new case.

```text
| 🟢 F · ... | `hooks/root-migrate.py#move@04ff113f`, `hooks/root-migrate.py#tracked_marks@<hash>`, `hooks/root-migrate.py#main@<hash>` | ... |
```

Needs a fix: yes — 🟡 1, a 0.3.x work item behind a relative link is named as
no work item and stamped over; deferred, since this round commissions nothing

Loses a record or crashes: yes — 🟡 1 leaves a 0.3.x work item outside the
root with the repository stamped, so no start ever moves it; its files and
rows stay intact and readable through the link

## Proof block

Files opened in this round, all in the clone at the target unless noted:
`hooks/root-migrate.py` (lines 150–690), `tests/test_the_root_migrates_itself.py`
(lines 1–175 and the fix range's diff), `tests/conftest.py#load_hook_module`,
`docs/review-chain-spec.md` (the cap, the reopening and the ladder sections),
`seal/releases/0.4.0.md:268` and `:292`,
`seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md`
(the fix range's diff), the work item's `spec.md:198-208`,
`rounds/round-1.md` (`New units`), `rounds/round-2.md` and
`rounds/round-2-report.md` in the worktree, the fix range's diff of
`seal/releases/0.4.0.md` and the changelog fragment, and #704's title and
state. The probe module, the two extracted earlier hooks and their outputs
were deleted, and the clone with them.
