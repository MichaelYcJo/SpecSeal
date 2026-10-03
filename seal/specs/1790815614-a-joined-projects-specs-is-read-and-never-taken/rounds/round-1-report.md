# Round 1 report — 1790815614 (#688), warden

Target `9e120b0a2228f43bff0897007b228da15fa55be2` on
`fix/688-a-joined-projects-specs-is-read-and-never-taken`, base `cd24f516`
(`release/v0.17.0`), diff `cd24f516..9e120b0a`, 51 files. Worked in a
`git clone --no-local` at the target under the session scratchpad; nothing
was written in the worktree except this file.

First round: no earlier `round-*.md` exists, so the build's account
(`overview.md`, `phases/phase-1.md` to `phase-5.md`, the spawn prompt) is the
only other voice. Each claim below is labelled with what I did to it.

## Stage 1 — the spec and the plan's five boxes

| Box | Claimed | Found |
|---|---|---|
| 1 · bootstrap reads content | `skills/implement/orchestration.md` tells only a `.specseal/` or a marked `specs/` entry, and a bare `specs/` goes to the shared/local question | **read**: the 0.3.x paragraph names both marks and the `<unix-seconds>-<slug>` shape; the new bold paragraph sends a bare `specs/` on to the question before the mode's options. Matches `hooks/root-migrate.py#marked` |
| 2 · the hook moves only marked items | `old_items` keeps an id-shaped directory only with `routing.md` or `rounds/` directly under it | **executed**: true for every tracked shape. **Not true for an untracked `rounds/`** — finding 🟡 1 |
| 3 · `Reference specs` row and its reader | absent → every `specs` outside the root; `none`; listed prefixes; no root → none | **read and executed** (module run): `hooks/config.py#reference_roots` and `#under_reference_root` do exactly the four answers; the root's own paths are dropped from a row and never matched by the default |
| 4 · the checks | `survivor-check` pool and range, `unverified-check` walk and base | **executed**: mutating the walk's prune and the hook's marks back to the old code reddens five of the new cases (probe table); the D1 survivor cases assert both directions (`none` and rootless put the team document back) |
| 5 · adopt refused | `spec.md` §*What is refused* | **read**: the refusal and its reason are there, grounded in `settle`'s rule arm |

Every 0.3.x work item carried a mark — **executed**, wider than the build's
claim: I scanned every tag from `v0.0.1` to `v0.3.0` (1, 6, 7 and 13 work
items), not only `v0.3.0`, and found no work-item directory without
`routing.md` or `rounds/`. And **read**: `CLAUDE.md` and
`hooks/commit-review-gate.py` at `v0.1.0`, `v0.2.0` and `v0.3.0` all require
`specs/<work-item-id>/routing.md` before the first edit. A user repository
on 0.3.x could only lack it by bypassing the gate. The README and the hook's
line then name such a directory as left behind, so a person sees it.

## 🟡 1 — an empty or ignored `rounds/` makes a team's directory a work item, and the hook moves it

`hooks/root-migrate.py:247-257` (`marked`) and `:277` (`old_items`).

The hook takes its units from git, and its docstring calls that the *only
what git tracks* boundary. It takes the marks from the disk, though:
`os.path.isfile(here/routing.md)` or `os.path.isdir(here/rounds)`. Git tracks
no empty directory and no ignored file, so a `rounds/` that is one of those
leaves `git status --porcelain` empty and passes `dirty()`. The team's
directory then reads as marked, and `moves` stages a `git mv` of its tracked
`spec.md` and `plan.md` into `seal/specs/`.

**Executed** (a probe module in the clone, run once and deleted). The
fixture was a committed `specs/1788000001-team-thing/` holding `spec.md`
and `plan.md` beside the existing old-layout fixture:

- with an empty `rounds/` directory on disk, the team directory was moved
  and staged;
- with `rounds/` in a committed `.gitignore` and one ignored file under it,
  the team directory was moved and staged.

**Why it matters.** Box 2 is "never moves", and the changelog fragment says
*A directory moves now only when it carries the plugin's own marks*. A
person reading `git diff --cached` sees the team's files renamed under
`seal/`, and the move line counts them as a work item. The marks have to
come from the same place the units do. Nothing is lost: the content is
staged as a rename, and `moved_items` re-points the rows that cite it
consistently. So this does not lose a record, but it is the act the ticket
forbids.

The symbolic-link refusal in `main` has to keep reading the disk, because
git lists nothing behind a linked `specs/`. A `git ls-files` through the
link fails, and the refusal would stop firing for a linked `specs/` that
holds real work items. That is the silent direction the refusal exists to
close, so the fix below leaves `marked` as it is for that one caller.

## ⬜ 2 — `routing.md` is a filename, and a team may have one

`hooks/root-migrate.py:111` (`MARKS`). The approved spec chose filenames.
A team's own `specs/<epoch>-api/routing.md` (a page about request routing)
moves today, and so does one with its own tracked `rounds/`. On a machine
whose marker file has never seen the repository (a fresh clone), this
happens even after the repository has a `seal/` root. A content mark would
close it: every 0.1–0.3 `routing.md` I opened is the `| Axis | Answer |`
table with a `Review` row, which `hooks/routing.py` already parses. This
needs no fix under the spec as approved. The repository owner can narrow it
with a follow-on.

## ⬜ 3 — the READMEs promise silence for a case that prints a line

`README.md:385-386` and its Korean twin (`README.ko.md`, the paragraph
ending *아무 말도 하지 않습니다*). The sentence says that a repository
whose `specs/` holds nothing of the plugin's hears nothing at all. It sits
in *Coming up from 0.3.x*, where the reader has `.specseal/`, and that
reader does hear a line: `.specseal/` moves, and the team directory is
named as left. The hook docstring says it correctly: *A repository holding
nothing else of the old layout hears nothing at all*. The behaviour is
right and only the sentence is too broad.

## ⬜ 4 — the seal README drops the shape half of the test

`templates/seal-README.md:51-56` and `seal/README.md:51-56`. This passage
says *a `specs/` entry carrying `routing.md` or `rounds/`* is moved. The
hook also requires the `<unix-seconds>-<slug>` name, so a team's
`specs/handbook/routing.md` stays where it is (pinned by
`tests/test_the_root_migrates_itself.py#test_a_mark_under_a_name_without_the_shape_is_not_a_work_item`).
The bootstrap and both READMEs carry the shape, and this file is the one
reader that does not.

## ⬜ 5 — the no-root rationale says more than the survivor sweep does

`hooks/config.py:543-549` (the `reference_roots` docstring) and the
`templates/config.md` §*Reference specs* row *no `seal/` root at either
place*. Both say that the checks still read the 0.3.x top-level `specs/` as
the plugin's records. `skills/code-review/scripts/survivor_check.py#WORK_ITEM_DIR`
now reads `seal/specs/` alone, so in a rootless repository a top-level
`specs/<x>/` that a range removes is measured as prose and is never a retired
work item. The pool and the range do still include it, and `unverified-check`
still reads it, so the claim is half true. This is a sentence, not a defect.
Nothing runs the sweep in a rootless 0.3.x repository, because the
session-start hook migrates it first.

## The build's divergence — no reference root without a `seal/` root

Judged and **confirmed**: it opens no silent path. A reference root only
ever takes paths out of what a check reads. With `()`, `survivor-check`
keeps every path in its pool and its range, and `unverified-check` prunes
nothing. Both read more, so any error they find is loud: a reported survivor
or a failed overview. The scratch opt-out has the same answer
(`hooks/optin.py#home_at` returns empty, and the result is `()`), and a
scratch repository runs no gates. The silent direction would be the default
`None` applying where it should not. That happens only for a root whose
`config.md` cannot be read, and the template's rule that a missing or
unreadable row takes its default covers that case. Local mode resolves the
root under the git directory and gets the default, which is right: nothing
of that root is in the tree.

## Stage 2 and the class (§12)

- **The commit gate's reading** — **executed**. Over all 51 changed files,
  under the gate at `cd24f516` and at the target, I compared each file's
  text at the base and at the tip: `commit_invocations` on the whole file,
  `_hides_a_commit` on the whole file, and both on the text up to and
  including the first waiver line. There was no flip. The `agents/smith.md`
  rider's own numbers reproduce inside a heredoc body under both gates and
  both revisions: one invocation for the line alone, one with everything
  above it, and `_hides_a_commit` True. The re-stamp `Verified 2026-10-01
  against "## Phases"@7d7bc750` is stamped true.
- **The ledger** — **executed**. `evidence-check .` unscoped exits 0 with
  3224 ok and nothing drifted, broken, malformed or over the cell limit.
  **Read**: 58 changed rows across the 14 release files, and every one
  carries a dated *Re-read 2026-10-01* or *Corrected 2026-10-01* note naming
  the phase. The 0.15.1 C2 correction narrows the claim to say that the
  pre-0.4.0 spelling sits under a reference root by default. That matches
  `survivor_check.py#a_reference_root` in `corpus` and `corrected`.
- **A resumed half-run** — **executed**. A first run stopped at a taken
  destination after moving the first item. I settled it by hand and
  committed, and the second run re-pointed the rows citing the first item.
  `moved_items` reads `seal/specs/` on disk, which is what makes the resume
  work. The cost is theoretical only: a team directory that shares an exact
  id with a `seal/specs/` entry would be re-pointed. Not raised.
- **The class** — **read**. I grepped every shipped script under `hooks/`,
  `skills/*/scripts/` and `.github/scripts/` for a `specs` reader. The
  remaining readers are pinned under the root (`settle.py#SPECS`,
  `hooks/routing.py#WORK_ITEMS`, the evidence and correction constants,
  `gather_changelog.py`'s `seal/specs/*/changelog.md` glob). The others
  match `specs` only to exclude a record (`records_a_past_state`,
  `a_gathered_fragment`), or are the out-of-scope items `spec.md` names
  (`DOC_ROOTS`, the settle citation scan, the evidence tree corpus, the
  hook's `dirty()`). No other place reads a bare `specs/` as the 0.3.x
  layout. `test_every_shipped_command_is_classified` holds the `bin/` list.
- **The agent and skill sentences** — **read**. The framer, smith, warden,
  settle and implement passages agree with each other and with
  `templates/config.md` §*Reference specs*. Each points at that section
  instead of restating the grammar. The warden's sentence makes an edit
  into a reference root a stage-1 finding, and none was found here: the
  diff touches no `specs/` outside `seal/`.
- **This repository's own records** — **executed**: `git ls-files` lists no
  directory named `specs` outside `seal/`, so the default takes nothing of
  the plugin's own tree out of either check.

## Regression tests to plant

- `tests/test_the_root_migrates_itself.py`: the parametrised case in the
  fix for 🟡 1. It was seen red at the target by the same probe shape (both
  arms moved the team directory).

## Facts for the evidence ledger

- B1 in `seal/ledger/1790815614-a-joined-projects-specs-is-read-and-never-taken.md`
  should cite the new case and the git-read marks once 🟡 1 is fixed. Its
  claim *is not moved* currently holds only for a tracked layout.
- Every work-item directory under `specs/` at the tags `v0.0.1`, `v0.1.0`,
  `v0.2.0` and `v0.3.0` (1, 6, 7, 13) carries `routing.md` — executed by
  `git ls-tree` at each tag.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the hook reads its marks from the disk while its units come from git, so an empty or ignored `rounds/` under a team's id-shaped directory makes it a work item and the hook stages its move | `hooks/root-migrate.py:255` | open | executed: both shapes moved and staged the team directory with a clean `git status`; box 2 and the changelog fragment say it never moves |
| ⬜ 2 | `routing.md` and `rounds/` are filenames, so a team's own `routing.md` under an id-shaped name still moves | `hooks/root-migrate.py:111` | open | read: the approved spec chose filenames; a content mark through `hooks/routing.py` would close it; the repository owner decides |
| ⬜ 3 | both READMEs promise silence to a repository whose `specs/` holds nothing of the plugin's, inside the section whose reader has `.specseal/` and hears a line | `README.md:385` | open | read against `hooks/root-migrate.py#main`'s tail and the hook docstring's wording |
| ⬜ 4 | the seal README names the marks without the `<unix-seconds>-<slug>` shape the hook also requires | `templates/seal-README.md:51` | open | read; `seal/README.md:51` carries the same text |
| ⬜ 5 | the no-root rationale says the checks still read the 0.3.x `specs/` as records, while `WORK_ITEM_DIR` no longer does | `hooks/config.py:543` | open | read; the pool, the range and `unverified-check` still do, and no rootless repository runs the sweep |
| 🟢 | the no-root divergence opens no silent path | `hooks/config.py:551` | confirmed | read: `()` only adds to what both checks read, so an error there is loud; an unreadable `config.md` takes the default, as the template's rule for absent rows says |
| 🟢 | no changed file flips the commit gate's reading, and the smith rider is stamped true | `agents/smith.md:119` | confirmed | executed: 51 files under both gates at both revisions, 0 flips; the rider's 1, 1, True reproduces |
| 🟢 | the ledger re-stamp and the 0.15.1 C2 correction | `seal/releases/0.15.1.md` | confirmed | executed: `evidence-check .` 3224 ok, 0 drifted; read: 58 rows, each with a dated note |
| 🟢 | no real 0.3.x work item is left behind by the marks | `hooks/root-migrate.py:247` | confirmed | executed: every tag `v0.0.1`–`v0.3.0`, no unmarked work item; read: the 0.1–0.3 gate required `routing.md` |
| 🟢 | the new cases exercise the checks for real | `tests/test_a_reference_root_is_read_and_never_taken.py` | confirmed | executed: the hook's marks reverted to the name test and the walk's prune removed, five new cases red; reverted |

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

### Probe for 🟡 1

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 — the marks come from git, as the units do

`hooks/root-migrate.py`, beside `marked` (which stays for the symlink
refusal in `main`):

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

and in `main`'s tail:

```python
    _, left = old_items(root)
    marks = tracked_marks(root) or set()
    shaped = [n for n in left if unmarked(root, n, marks)]
```

The test, in `tests/test_the_root_migrates_itself.py` after
`test_a_mark_under_a_name_without_the_shape_is_not_a_work_item`:

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

Needs a fix: yes — 🟡 1, the hook's marks read from the disk, so an empty or ignored `rounds/` moves a team's directory

Loses a record or crashes: no

Broad gate: not yet. One 🟡 is open, so the sealer's spawn has not come due.

## Proof block

Opened in the clone at `9e120b0a`: `hooks/root-migrate.py`, `hooks/config.py`
(the reference-root section and its imports), `hooks/optin.py#home_at`,
`hooks/commit-review-gate.py` (signatures of `commit_invocations` and
`_hides_a_commit`), `skills/code-review/scripts/survivor_check.py` (the
exclusion predicates, `WORK_ITEM_DIR`, `corrected`, `references`,
`a_reference_root`, `local_specs`), `skills/verify/scripts/unverified_check.py`
(`overviews`, `references_at`, `reference_rule`, `overviews_at`,
`repo_root`, `repo_relative`, `main`), `skills/verify/scripts/broad_gate.py`
(constants), `templates/hygiene.yml` (how the checks are fetched),
`templates/config.md` §*Reference specs*, the work item's `spec.md`,
`overview.md`, `phases/phase-5.md`, `changelog.md`, its ledger fragment,
`agents/smith.md` (the rider), `README.md` §*Coming up from 0.3.x*, the diff
of every prose file the branch changed, and the diffs of
`tests/test_a_reference_root_is_read_and_never_taken.py`,
`tests/test_the_root_migrates_itself.py`, `tests/test_unverified_rows_close.py`,
`tests/test_first_setup_asks_once.py`, `tests/test_settle_reads_before_it_removes.py`,
`tests/test_no_document_names_the_old_roots.py` and
`tests/test_a_corrected_sentence_survives_elsewhere.py`. At the tags: the
`routing.md` of one `v0.3.0` work item, and `CLAUDE.md` and the gate's
routing lines at `v0.1.0`, `v0.2.0` and `v0.3.0`.
