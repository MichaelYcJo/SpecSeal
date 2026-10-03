# 1790815614-a-joined-projects-specs-is-read-and-never-taken — round 2 report

Ran by specseal:warden on claude-opus-5-5. Target SHA
`6fb43173b4b43a1fde705eb6e97deb93fc9bdaf7`. This is the verifying round, and
its target is round 1's fix range
`c35317119feb0f1d7d6f2b8be2b8f5ce736dced7..838de55a76ee172cc9d5bc3c0bc8714aafd6404e`
(four commits), plus the merge `c3531711` before it. All work was done in a
`git clone --no-local` at `<scratchpad>/1790815614/round-2/clone`.

## What this round found, in causal order

Round 1's 🟡 1 is closed for the shapes it named. An empty `rounds/`, an
ignored `rounds/` and an ignored `routing.md` under a team's id-shaped
directory move nothing and stage nothing. That holds in the planted cases and
in a repository holding only a team's `specs/`, where the hook also stays
silent. A real tracked work item still moves, and the symbolic-link refusal
still holds. All of this was executed.

The fix pass broke two things, and both lead to the same outcome: the hook
stamps the repository and goes silent while a 0.3.x work item, or part of
one, is still under `specs/`.

1. **The fallback the smith removed can be observed** (🟡 1). The account
   says `dirty()` refuses first. That is false for the one decision taken
   before `dirty()`: when `moves()` returns nothing, `main` stamps the
   repository wherever `seal/` exists (`hooks/root-migrate.py:580`). Since
   `d52ded2`, `tracked_marks` answers `set()` when git cannot list. So a
   `git ls-files` that fails while `rev-parse` still works lists no items.
   With `.specseal/` already moved, `units` is then empty and the hook
   stamps instead of refusing. Executed with a real corrupt index after a
   stopped run: the target stamped silently, and the next start, with the
   index repaired, stayed silent and left the item under `specs/`. The
   versions at `1e83a80`, at `9e120b0a` and at the base all refused it as
   dirty, stamped nothing, and moved the item on the next start.
2. **A move that stops inside an item, after the item's marks have moved,
   never resumes** (🟡 2). A destination that already exists is moved file
   by file, in `git ls-files` order. `rounds/…` and `routing.md` sort before
   `spec.md` and `survivors.md`, so a stop at a taken `spec.md` has already
   moved both marks. The hook's own line then offers *git rm `<dst>` to let
   the move bring the old one over*. Once a person does that, the next start
   finds no mark and so no unit, stamps, and goes silent. `spec.md` is
   stranded at the old path, and the three rows citing files that already
   moved stay BROKEN. Executed: the target and `1e83a80` strand it. `9e120b0a`
   moves it only because the empty `rounds/` directory that `git mv` leaves
   on disk counted as a mark there. This round 1 fix is exactly what stopped
   that from counting. The base moves it by name. So the build introduced
   this for an item carrying only `routing.md`, and the fix pass widened it
   to every item. Its location is `move()`, depth 0.

What reads badly but changes no behaviour:

3. The printed reason says *no routing.md or rounds/* even next to an ignored
   `routing.md` the person can see (⬜ 3).
4. Ledger row B5 says the disk stands in where git cannot list and that
   `dirty()` refuses that run. At the target the disk stands in nowhere, and
   the stamp branch comes before `dirty()`. This is a correction to the run's
   paperwork (⬜ 4).
5. One case predates the branch. If the resume finds nothing left to move,
   the rows of a stopped run are never re-pointed. Settling a taken file with
   *git rm `<src>`* leaves 3 rows BROKEN at every version, including the base
   (⬜ 5, deferred). `evidence-check` reports this loudly. With 🟡 2's fix,
   the marks stay behind, so that settle resumes and re-points, as executed
   below. Only a stop at the last mark itself still reaches it.

## Round 1's verdicts, each answered

- **🟡 1, fixed at `1e83a80e`.** Closed for its shapes. Executed: the planted
  `test_a_mark_git_does_not_track_is_not_a_mark` passes, and a probe of the
  three shapes in a repository holding only a team's `specs/` was silent,
  moved nothing, staged nothing and left `seal/` absent. Seen red: with
  `old_items` reverted to `marked(root, n)`, all three shapes fail. Its fix
  pass caused 🟡 1 and widened 🟡 2 above, which are new findings and not a
  reopening of this one.
- **⬜ 2, answered.** The grounds still hold. `plan.md`'s alternatives table
  lists *Marks = `routing.md` or `rounds/` (chosen)* and rejects the content
  names, and `plan.md:7` records the approval. Read.
- **⬜ 3, fixed at `e30a5d7d`.** Closed. Both READMEs now say silence comes to
  a repository holding neither the old root nor a marked entry. That matches
  `main`: `.specseal/` always yields units, and a team-only `specs/` yields
  none and returns silently. Read, and executed by the team-only probe, which
  printed nothing.
- **⬜ 4, fixed at `e30a5d7d`.** Closed. `templates/seal-README.md:51` and
  `seal/README.md:51` both name the `<unix-seconds>-<slug>` shape. Read.
- **⬜ 5, fixed at `e30a5d7d`.** Closed. `survivor_check.py` lines 220–222 say
  `WORK_ITEM_DIR` reads `seal/specs/` alone, and lines 857–887 still read any
  `specs/` for the pool. The docstring at `hooks/config.py:548` says exactly
  that. Read.

## New units, judged as code

- `tracked_marks`: the fallback (🟡 1). Everything else matches the docstring.
  With `-z`, no path is quoted. A gitlink at `specs/<id>/rounds` is one entry
  with three parts, so it is not a mark, which is the safe direction.
- `test_a_routing_md_deeper_than_directly_under_is_not_a_mark`: seen red.
  With `len(parts) == 3 and parts[2] == routing` mutated to
  `parts[-1] == routing`, it fails with *2 work items* and the other three
  pass. That is the mutation it exists for. Disk marks never treated
  `docs/routing.md` as a mark either, so only this condition can turn it red.
- `test_a_mark_git_does_not_track_is_not_a_mark`: seen red, as above.

## The merge `c3531711`

There are three conflicted hunks, and each was read against both parents
and the merge base `cd24f516` by a throwaway script.

- `seal/releases/0.12.0.md` lines 26–32 form one hunk of interleaved rows.
  Each row was edited by one side only, and the merge took that side for
  every row: 26, 28 and 31 from #638, and 30 and 32 from #688.
- `seal/releases/0.12.0.md:109` was edited by both sides. The notes are a
  union: all 15 of each side's notes, plus the merge's own *Re-read again
  2026-10-01*. `templates/config.md#"## Broad gate"` carries #638's
  `b9eebc39`. #688 kept the base hash there, so #688 had not edited that
  unit. The Bootstrap section carries #688's `f2f05383`, and #638 kept its
  base hash. Each hash comes from the side that edited its unit.
- `seal/releases/0.5.0.md:107` was edited by both sides. The notes are a
  union: 19 of ours and 18 of theirs, plus the merge note.
  `templates/config.md#"# Repository config"` is the whole document, and
  both sides edited it, so the hash is neither side's: `76849f53`,
  re-stamped and still valid at the target. The merge note says so.

`correction-check` dropped nothing over either range, and `evidence-check .`
is clean.

## Regression tests to plant

The destination is `tests/test_the_root_migrates_itself.py`, and both
fenced cases are under *Paste-ready fixes*.

- For 🟡 1: a stopped run's state with a corrupt index. It is refused as
  dirty and stamps nothing, and the next start moves the item. The same
  shape was executed red at the target and green with the fix.
- For 🟡 2: a taken `spec.md` settled each way the line offers, then resumed.
  The same shape was executed red at the target for both settles and green
  with the fix. The exact message assertion in the fenced case was read, not
  run.

## Facts for the evidence ledger

- B5 in `seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md`
  needs its claim corrected in place, whichever way 🟡 1 is fixed (⬜ 4).
- Once 🟡 2 is fixed, a new row should state that a file-by-file move takes
  the marks last, so a stopped item stays marked. Anchor it on
  `hooks/root-migrate.py#move` and the new case.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the fix pass made `tracked_marks` answer no mark where git cannot list, and the stamp branch, which `main` reaches before `dirty()`, reads that as nothing old left: a stopped run's item is stamped over and never moves | `hooks/root-migrate.py:278` | open | executed: real corrupt index after a stopped run; the target stamped silently and the repaired next start stayed silent with the item under `specs/`; `1e83a80`, `9e120b0a` and the base refused as dirty and moved it next start; the account's *`dirty()` refuses first* is false for `hooks/root-migrate.py:580` |
| 🟡 2 | a file-by-file move stopped after an item's marks moved is never resumed: settled as the hook's line says, the next start finds no mark, stamps, strands the file at the old path and leaves the moved files' rows BROKEN | `hooks/root-migrate.py:398` | open | executed: taken `spec.md`, `git rm <dst>`; the target and `1e83a80` strand it with 3 broken, `9e120b0a` (empty `rounds/` on disk) and the base move it with 0 broken; depth 0, since the build introduced it for a `routing.md`-only item and the fix pass widened it |
| ⬜ 3 | the printed reason says *no routing.md or rounds/* beside an ignored `routing.md` the person can see | `hooks/root-migrate.py:654` | open | read; the behaviour is right and the sentence is not; the reason is quoted in `spec.md:203`, the changelog fragment, ledger row B1 and the test's `LEFT_UNMARKED`, so it is fix or justify |
| ⬜ 4 | ledger row B5 says the disk stands in where git cannot list and `dirty()` refuses that run; at the target neither is true | `seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md` | open | read against `hooks/root-migrate.py#old_items` and `#main`; a correction to the run's paperwork, outside `Needs a fix` |
| ⬜ 5 | a resume with nothing left to move never re-points the rows of a stopped run, so settling a taken file with `git rm <src>` leaves them BROKEN | `hooks/root-migrate.py:569` | deferred new issue | executed: 3 broken at the target, `1e83a80`, `9e120b0a` and the base alike; present in 0.16.0, loud through `evidence-check`; 🟡 2's fix narrows it to a stop at the last mark |
| 🟢 | round 1's finding 1 is closed for its shapes — an empty or ignored `rounds/` and an ignored `routing.md` move nothing and stage nothing | `hooks/root-migrate.py:313` | confirmed | executed: planted cases green; a team-only repository silent with nothing staged in all three shapes; seen red with `old_items` back on disk marks |
| 🟢 | round 1's finding 2 stays answered — the marks are file names by the approved design | `seal/specs/1790815614-a-joined-projects-specs-is-read-and-never-taken/plan.md:123` | confirmed | read: the alternatives table chooses the names, and `plan.md:7` records the approval |
| 🟢 | round 1's finding 3 is closed — both READMEs promise silence only where neither the old root nor a marked entry exists | `README.md:385` | confirmed | read against `hooks/root-migrate.py#main`; executed by the team-only probe, which printed nothing |
| 🟢 | round 1's finding 4 is closed — the root README names the id shape | `templates/seal-README.md:51` | confirmed | read; `seal/README.md:51` is the same text |
| 🟢 | round 1's finding 5 is closed — the no-root rationale names what still reads the 0.3.x `specs/` | `hooks/config.py:548` | confirmed | read against `skills/code-review/scripts/survivor_check.py` lines 220–222 and 857–887 |
| 🟢 | the two new cases are seen red against the mutation each exists for | `tests/test_the_root_migrates_itself.py:813` | confirmed | executed: 3 of the ignored/empty shapes red on disk marks; the depth case red alone on `parts[-1] == routing`; reverted |
| 🟢 | a real tracked work item still moves, and the symbolic-link refusal still holds | `hooks/root-migrate.py:591` | confirmed | executed: the module's 52 cases at the target, including the either-mark, linked-`specs/` and unmarked-link cases |
| 🟢 | the merge's three resolved hunks keep both sides' notes, and each hash belongs to the side that edited its unit | `seal/releases/0.12.0.md:109` | confirmed | executed: row-by-row comparison against base, both parents and merge; `seal/releases/0.5.0.md:107` re-stamped because both sides edited the whole document; `correction-check` and `evidence-check` clean |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_root_migrates_itself.py -q` in the clone at the target | exit 0, 52 passed |
| throwaway probe module, P1: a repository holding only a team's `specs/` with an empty `rounds/`, an ignored `rounds/`, an ignored `routing.md` | 3 passed: nothing printed, nothing staged, no `seal/`, the team's files in place |
| the same module, P2: `.specseal/` moved and committed, the item still under `specs/`, then `.git/index` overwritten (`rev-parse` exit 0, `ls-files` non-zero), one start, the index restored, one start; run against the target, `1e83a80`, `9e120b0a` and the base | target: first start silent and stamped, second silent, item left under `specs/` (red); the other three: first refused as uncommitted changes and not stamped, second moved 1 work item and re-pointed 3 rows |
| the same module, P3: `specs/<item>/spec.md` and `seal/specs/<item>/spec.md` both committed, one start, settled by `git rm` of the destination, one start, `evidence-check` | target and `1e83a80`: stopped at `spec.md`, then silent, `spec.md` left at the old path, 1 ok 3 broken (red); `9e120b0a` and base: moved, 4 ok 0 broken |
| P3 settled by `git rm` of the source instead | all four versions: second start silent, 1 ok 3 broken |
| mutation: `old_items` on `marked(root, n)` and `tracked_marks` on `parts[-1] == routing`, the two new cases | 4 failed; then the depth mutation alone: the depth case failed, 3 passed; reverted with `git checkout` |
| both proposed fixes applied, the module plus P2 and both P3 settles at the target | 54 passed; 1 failed, the old-names case, which read the probe's own copies of the earlier hooks placed under `hooks/`; reverted, copies deleted |
| `bin/evidence-check .`, unscoped, in the clone | exit 0; total 3254 ok, 0 drifted, 0 broken, 0 malformed, 0 overflow |
| `bin/correction-check --range origin/release/v0.17.0...HEAD` | exit 0; 1 merge examined, no correction marker dropped; in the clone that ref is `cd24f516` |
| `bin/correction-check --range a340221b...HEAD`, against the real release tip | exit 0; 1 merge examined, no correction marker dropped |
| throwaway script: every row of `seal/releases/0.12.0.md` and `0.5.0.md` changed by either parent of `c3531711`, against the base, both parents and the merge | two rows both sides edited, each a union of notes with the hash rule kept; every other row taken from the one side that edited it |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet — nobody ran it in this round; it is the sealer's, after the rounds settle |

```python
# P2, run once against four versions of the hook, deleted
(repo / "seal").mkdir()
for src, dst in ((".specseal/map.md", "seal/ledger.md"), (".specseal/map", "seal/ledger"),
                 (".specseal/README.md", "seal/README.md"), (".specseal/follow-up.md", "seal/follow-up.md")):
    git(repo, "mv", src, dst)
git(repo, "commit", "-qm", "the home moved, the item not yet")
index = repo / ".git" / "index"; good = index.read_bytes()
index.write_bytes(b"DIRC garbage")          # rev-parse answers, ls-files cannot
first = message(start(hook, repo)); was_stamped = stamped(hook, repo)
index.write_bytes(good)
second = message(start(hook, repo))
# target: first == '' and was_stamped is True; second == ''; the item is still under specs/
```

```python
# P3, run once against four versions of the hook, deleted
write(repo, f"specs/{ITEM}/spec.md", "# the old spec\n")
write(repo, f"seal/specs/{ITEM}/spec.md", "# the newer spec\n")
git(repo, "add", "-A"); git(repo, "commit", "-qm", "both spec.md")
first = message(start(hook, repo))          # moved 4 of 5 ... stopped at specs/<item>/spec.md
git(repo, "rm", "-q", f"seal/specs/{ITEM}/spec.md")   # the line's own second option
second = message(start(hook, repo))
# target: second == ''; specs/<item>/spec.md still there; check(repo) -> 1 ok · 3 broken
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 5 — a resume with nothing left to move never re-points the rows of a stopped run; present in 0.16.0 | a new issue against `hooks/root-migrate.py#main`, the branch that stamps when `units` is empty | the repository owner, who files and schedules it |

## Paste-ready fixes

```python
# 🟡 1 — hooks/root-migrate.py: put back the None that d52ded2 removed, and
# the disk that stands in for it. The stamp branch in main() reads moves()
# before dirty(), so "no answer" must not read as "no work item".
def tracked_marks(root):
    """The id-shaped names under `specs/` whose mark git TRACKS directly
    under them — `specs/<name>/routing.md`, or a file under
    `specs/<name>/rounds/` — or None when git cannot say. `old_items` then
    reads the marks from the disk, so the run still has units and `dirty()`
    refuses it; an empty answer would read as nothing old left, and `main`
    would stamp over a work item that has not moved (round 2 of #688).

    The move's units come from git (`tracked_names`), and so do its marks.
    Git tracks no empty directory and no ignored file, so a mark that is
    either leaves `git status` clean, and read from the disk it made a
    team's directory a work item (round 1 of #688, 🟡 1)."""
    try:
        r = git(root, "ls-files", "-z", "--", OLD_ITEMS)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    ...


def old_items(root):
    ...
    marks = tracked_marks(root)
    items = [
        n
        for n in entries(root, OLD_ITEMS)
        if (n in marks if marks is not None else marked(root, n))
    ]
    ...

# in main(), the tail:
    _, left = old_items(root)
    marks = tracked_marks(root) or set()
    shaped = [n for n in left if unmarked(root, n, marks)]
```

```python
# 🟡 1 — tests/test_the_root_migrates_itself.py
def test_a_git_that_cannot_list_the_marks_stamps_nothing(hook, repo):
    """Round 2 of #688, 🟡 1. With `.specseal/` already moved, the items are
    the only units, and a `git ls-files` that cannot answer listed none: the
    hook read that as nothing old left and stamped, so the move never ran
    once git answered again. A corrupt index is the real shape: `rev-parse`
    answers and `ls-files` does not."""
    (repo / "seal").mkdir()
    for src, dst in (
        (".specseal/map.md", "seal/ledger.md"),
        (".specseal/map", "seal/ledger"),
        (".specseal/README.md", "seal/README.md"),
        (".specseal/follow-up.md", "seal/follow-up.md"),
    ):
        git(repo, "mv", src, dst)
    git(repo, "commit", "-qm", "the home moved, the item not yet")
    index = repo / ".git" / "index"
    good = index.read_bytes()
    index.write_bytes(b"DIRC garbage")
    out = message(start(hook, repo))
    assert "uncommitted changes" in out, out
    assert not stamped(hook, repo)
    index.write_bytes(good)
    out = message(start(hook, repo))
    assert "moved 1 work item into seal/" in out, out
    assert (repo / "seal" / "specs" / ITEM / "routing.md").is_file()
    assert stamped(hook, repo)
```

```python
# 🟡 2 — hooks/root-migrate.py, move(): the marks move last
    r = git(root, "ls-files", "-z", "--", src)
    if r.returncode != 0:
        raise MoveError(src, (r.stderr or "").strip() or "git ls-files failed")
    # The marks move last. A run stopped at any other file leaves the item
    # marked as git tracks it, so the next start still finds a work item and
    # resumes it; moved first, they left a `spec.md` the line told the person
    # to keep with no mark beside it, and the next start stamped over it
    # (round 2 of #688). The stopped file itself always stays at `src`.
    routing, rounds = MARKS

    def a_mark(rel):
        tail = rel[len(src) + 1 :]
        return tail == routing or tail.startswith(rounds + "/")

    for rel in sorted((p for p in r.stdout.split("\0") if p), key=a_mark):
        target = dst + rel[len(src) :]
        if os.path.exists(under(root, target)):
            raise taken(rel, target)
        git_mv(root, rel, target)
```

```python
# 🟡 2 — tests/test_the_root_migrates_itself.py
@pytest.mark.parametrize("keep", ["the old one", "the newer one"])
def test_a_move_stopped_inside_an_item_resumes_whichever_file_is_kept(
    hook, repo, keep
):
    """Round 2 of #688, 🟡 2. A destination that exists is moved file by
    file, and `routing.md` and `rounds/` sort before `spec.md`: a stop at a
    taken `spec.md` had moved both marks, so once the person settled it as
    the line says, the next start found no work item, stamped, and left the
    file at the old path and three rows BROKEN."""
    write(repo, f"specs/{ITEM}/spec.md", "# the old spec\n")
    write(repo, f"seal/specs/{ITEM}/spec.md", "# the newer spec\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "both spec.md")
    out = message(start(hook, repo))
    assert f"stopped at specs/{ITEM}/spec.md" in out and "already exists" in out, out
    gone = f"seal/specs/{ITEM}/spec.md" if keep == "the old one" else f"specs/{ITEM}/spec.md"
    git(repo, "rm", "-q", gone)
    out = message(start(hook, repo))
    assert "moved 1 work item into seal/" in out, out
    assert not (repo / "specs" / ITEM / "spec.md").exists()
    assert (repo / "seal" / "specs" / ITEM / "spec.md").is_file()
    assert (repo / "seal" / "specs" / ITEM / "routing.md").is_file()
    totals = check(repo)
    assert "0 broken" in totals, totals
```

```python
# ⬜ 3 — hooks/root-migrate.py, main(): say which kind of mark is missing.
# LEFT_UNMARKED, spec.md:203, the changelog fragment and ledger row B1 quote
# the old reason and move with it, or the smith answers with grounds.
        (shaped, "no routing.md or rounds/ that git tracks — not a SpecSeal work item"),
```

```markdown
⬜ 4 — seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md, row B5,
claim corrected in place (if 🟡 1's fix lands as above):

… the disk is read for the symbolic-link refusal, and stands in for git only
where git cannot list — a run `dirty()` then refuses, because the items read
from the disk keep `units` non-empty and the stamp branch is not reached …
**Corrected 2026-10-01 in round 2 (⬜ 4):** at `6fb43173` the disk stood in
nowhere and the stamp branch came before `dirty()`.
```

Needs a fix: yes — 🟡 1 (no answer from git reads as no work item, and the
hook stamps over a stopped run) and 🟡 2 (a move stopped after an item's
marks moved is never resumed)

Loses a record or crashes: yes — 🟡 1 and 🟡 2 each leave a 0.3.x work item,
or part of one, outside the root with the repository stamped, so the hook
never moves it and its rows that already moved stay BROKEN

## Proof block

Files opened in this round, all at the target in the clone unless noted:

- `seal/specs/1790815614-a-joined-projects-specs-is-read-and-never-taken/rounds/round-1.md`
- `hooks/root-migrate.py`, lines 100–669, and the same file at `cd24f516`, `1e83a80` and `9e120b0a` (extracted, run, deleted)
- `hooks/optin.py`, `repo_root` and `git_common_dir`
- `hooks/config.py`, the fix range's hunk at `reference_roots`
- `tests/test_the_root_migrates_itself.py`, lines 1–165, 287–376, 506–524, 642–870
- `tests/conftest.py`, `load_hook_module`
- `bin/test`
- the fix range's diffs of `README.md`, `README.ko.md`, `seal/README.md`, `templates/seal-README.md`, `skills/implement/orchestration.md`, `docs/one-root-by-lifetime.md`, `seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md`, `seal/releases/*.md`
- `seal/releases/0.12.0.md` and `seal/releases/0.5.0.md` at `cd24f516`, `5edc7710`, `a340221b` and `c3531711`
- `skills/code-review/scripts/survivor_check.py` and `skills/verify/scripts/unverified_check.py`, by search
- `seal/specs/1790815614-a-joined-projects-specs-is-read-and-never-taken/plan.md` and `spec.md`, by search
- `seal/config.md` in the worktree (no `Record language` row, so English)
