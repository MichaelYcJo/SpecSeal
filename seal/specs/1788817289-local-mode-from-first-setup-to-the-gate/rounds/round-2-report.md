# Round 2 — the verifying round

Target `5e56470`, base `origin/release/v0.9.1` (`2138c98`), branch
`fix/225-151-local-mode-from-first-setup-to-the-gate`. Ran by warden on
claude-opus-5, 2026-09-08. The surface is `git diff 9d2f440..5e56470`, whose
substance is `1a54687` and `a3bea92`; `ca59969`, `0f8e893`, `fb31a5e` and
`f21728a` carry the records and the one rider the fix pass planted. The merge
of `release/v0.9.1` at `5e56470` brings #111, #226 and #239's instance repair,
and none of that is this branch's work.

## What this round was asked

Round 1's eight findings are recorded as fixed. This round was to re-run the
fixes rather than read them, on six axes: re-derive the prompt budget by
running the gate in three repository states; say what an unattended session
experiences and whether the escape is reachable; judge the added `git` cost
and the deferral that leaves it; re-run the four reproduced reds; re-run the
one mutation that survived the first sweep; check that the single ledger
re-stamp is honest and that no blanket re-verify closed a deferral nobody
read; and check that the rider planted on `seal.py#other_worktrees` does not
name a commit of this branch.

Nothing in that list was narrowed and nothing was widened. The full suite,
the repository-wide lint and the typecheck were not run — `agent-contract` §2
keeps them out of a round, and the orchestrator answers for them.

## How the three new findings relate to each other

Round 1's eight are closed, and I confirmed all eight by running them. What
this round opens is not a return of any of them. It is the **tail of the fix
pass** — the two acts the pass took *after* the four code fixes, to record
what it had found.

```
round 1's four code fixes            → all four confirmed by execution
       ↓ the pass then recorded what it found
① it planted a rider on the one       → ⑨ the rider's stamp names a commit
   sibling reader it had enumerated       the squash destroys
                                      → ⑩ the same rider drifted two ledger
                                          rows and neither was re-read
② it stated the cost it chose not     → ⑪ the number it states is a main
   to remove                              work tree's; a linked worktree
                                          pays double
```

Findings 9 and 10 come from the same fifteen lines of comment. Finding 11 is
about the sentence beside them.

---

## ① The budget is now the number the code has — confirmed by running it

Round 1's 🔴 was that `pr-notes.md` claimed one deny per session while the
code produced one deny and then an `ask` on every command for the rest of the
session. `a3bea92` restated the budget as two prompts and published a table.
I re-derived that table without reading it: twenty ordinary Bash calls per
session, two sessions, three repository states.

| The repository | Session 1 | Session 2 |
|---|---|---|
| `seal/`, no `Mode` row | 1 deny, 1 ask, 18 silent | 1 deny, 1 ask, 18 silent |
| `seal/` with a `Mode` row | 20 silent | 20 silent |
| no `seal/` at all | 20 silent | 20 silent |

Executed. The numbers are the ones `pr-notes.md` §*A prompt budget* now
carries, cell for cell. The sequence in a fresh session is
`deny → ask → silent → silent → silent → silent`.

## ② The escape is reachable unattended, and the outage is gone

A run with nobody at the keyboard cannot answer either prompt. What it now
experiences in a repository with no `Mode` row is two stopped commands and
then an ordinary session:

| | Before `1a54687` | After |
|---|---|---|
| Call 1 | deny | deny |
| Call 2 | ask | ask |
| Calls 3–20 | ask, every one | silent |

Executed, and I ran the escape itself as the third call: `seal mode` reaches
the shell (`deny → ask → silent`). So the specific outage round 1 named — the
command that ends the asking is itself a Bash call, and every Bash call was
stopped — does not survive the fix.

What the fix does **not** do is get the row written. An unattended run never
answers, so `seal mode` is never chosen, and the next session pays the same
two prompts again. That is stated rather than hidden: the changelog fragment
says every repository that opted in before this release meets the gate until
somebody runs the command once. I am not opening a finding on it.

## ③ The four reds, re-run rather than read

All four reproduce as fixed. Executed, each against a repository built for it.

- **The ten-call session.** `deny, ask, silent…` — ① above.
- **The three unreadable `config.md` shapes.** A directory of that name,
  undecodable bytes, and `chmod 000` each return `silent` on three
  consecutive calls. A readable row returns `silent` too, and a missing row
  still returns `deny`.
- **Two work trees, one local root.** Main tree `deny`, linked worktree
  `ask`, linked worktree `silent`, main tree `silent` — two prompts for the
  clone, not two per tree. Shared roots stay one question per tree: main tree
  `deny`, worktree `deny`.
- **The `--separate-git-dir` repository.** `git worktree list --porcelain`
  still prints the git directory as the worktree path, and `git -C` on it
  still answers *fatal: this operation must be run in a work tree*.
  `repo_of` now returns the caller's real tree. A bare clone with the caller
  outside returns `None`, which `where()` turns into the sentence naming both
  places it tried. An ordinary local-mode repository still resolves to itself.

## ④ The surviving mutation is killed, and the case pins the property

`common_dir_of` dropping the resolution against the directory it asked is
killed by `test_the_clone_is_identified_from_the_directory_it_was_asked_about`
— executed against a `--no-local` clone at the target, exit 1 for the case
alone and for the whole module. The case asserts the function's answer equals
the repository's real common directory with the process standing somewhere
else, so it pins the property rather than the mutant.

I also mutated the other half of the same expression, dropping the
`realpath`. It survives the whole module, and I could not construct a case
where it changes the answer: I built a `--separate-git-dir` repository whose
git directory was named through a symbolic link, and git resolved the link
itself, so both spellings agreed. **Reported as measured, not as a finding** —
I have no failure to show, and inventing one would be manufacturing.

## ⑤ The one ledger re-stamp is honest

`seal/ledger.md`'s S8 row moved its anchor hash from `541502a6` to
`b8ea59c3`, its `Checked` date from 2026-09-07 to 2026-09-08, and gained a
sentence saying what was re-read and why the claim still holds. The claim
pins `templates/config.md`'s table shape, and the table is untouched — the
diff of that file changes no `|` row, and the header plus the first real row
still read `| Item | Value |` and `| Commit and pull request language |
English |`.

No blanket re-verify happened. `ca59969` changes exactly one line of
`seal/ledger.md`, and the pre-existing drifted rows are all still drifted.

## ⑥ 🔴 The rider stamp names a commit this branch's own squash destroys

`skills/implement/scripts/seal.py:1640` ends the rider with `# Verified
2026-09-08 at a3bea92.` `a3bea92` is a commit of this feature branch. A
feature branch **squashes** into its release branch by repository rule, which
writes one new commit and keeps none of the originals.

This is #239's class, and #239's first instance turned `release/v0.9.1` red
three commits ago. `2138c98` repaired that one by re-stamping at a commit
that survives. This branch then planted a second instance of the same defect.

Executed. In a `--no-local` clone I squashed `5e56470` onto `2138c98` the way
the rule requires and ran the case:

```
before the squash: exit 0, a3bea92 is an ancestor of HEAD
after  the squash: exit 1, a3bea92 is NOT an ancestor of HEAD
  AssertionError: skills/implement/scripts/seal.py: rider stamped a3bea92,
  which is not an ancestor of HEAD. A stamp nobody else can resolve is not a
  stamp
```

**Why it matters and who pays.** The failure lands on the merge, not on the
branch that wrote it, so the person who has to repair it is never the person
who caused it — the sentence `1788824000-a-rider-stamp-names-a-commit-the-squash-discards`'s
changelog fragment already wrote about the last one.

`other_worktrees` is byte-identical at `2138c98` and at the target once
comments are stripped, so `2138c98` is an honest stamp for the same claim.

## ⑦ 🟡 The same rider drifted two ledger rows, and neither was re-read

The rider adds fifteen lines inside `seal.py#other_worktrees`, which changes
that unit's content hash. Two rows anchor it:

- `seal/ledger.md`'s S26 row, and
- `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md`'s R4
  row, which belongs to **another work item**.

Executed, in a `--no-local` clone at four tree states:

| Tree state | Drifted anchors |
|---|---|
| `9d2f440` — base of the fix pass | 8 |
| `2138c98` — the release branch | 0 |
| `ca59969` — after the rider | 9 |
| `5e56470` — the target | 9 |

The one name drifted at the target and at neither parent is
`skills/implement/scripts/seal.py#other_worktrees`.

**Why this is not the deferral the fix record describes.** `round-1-fixes.md`
§*Ledger* reasons carefully about not running a blanket re-verify, because
that would close the nine rows already deferred to the repository owner. That
reasoning is right and I am not reopening it. What it does not cover is drift
the same commit *created*. The pass re-read and re-stamped S8 when its own
prose drifted a row; it did not do the same for the row its own rider
drifted, and it left a second one in a fragment whose owner did not touch
`seal.py`.

The record also says the item's own fragment "is now clean", which is true
(39 ok, 0 drifted) and is not the file this lands in.

## ⑧ 🟡 The stated per-call cost is a main work tree's number

`pr-notes.md` §*A prompt budget* opens the cost paragraph with **"one `git`
process per Bash call, in every repository on the machine"** and continues
"in a repository that has a root and no row it is two, and it stays two on
the calls after the budget is spent."

Measured with a logging `git` on `PATH`, one `ls` payload:

| Where the session sits | Repository state | `git` processes | The commands |
|---|---|---|---|
| main work tree | no `seal/` | 1 | `--show-toplevel` |
| main work tree | local root, no row | 2 | `--show-toplevel`, `--git-common-dir` |
| **linked worktree** | no `seal/` | **2** | `--show-toplevel`, `--git-common-dir` |
| **linked worktree** | local root, no row | **4** | `--show-toplevel`, then `--git-common-dir` three times |

Wall clock in a linked worktree with no `seal/`, median of twelve: **59.0 ms
for the gate against the sibling's 27.2 ms**, where `pr-notes.md` records
36.4 ms against 26.7 ms. In a main work tree I measured 40.0 against 28.8,
which is the document's figure plus machine noise — so the document was
measured in a main tree and reads as if it were measured everywhere.

**Why the shape matters here.** This repository's own agents run in linked
worktrees; this round is running in one. The configuration the number
understates is the configuration the project uses.

**And two of those four calls are this branch's own.** The same question,
`rev-parse --git-common-dir`, is asked three times in one hook invocation:

1. `undeclared` → `optin.home_at` → `optin.git_common_dir`
2. `marker_dir` → `optin.home_paths(root)` with no `common` → `optin.git_common_dir`
3. `marker_dir` → `git_dir_of(root, "--git-common-dir")`

`optin.home_paths`'s own docstring says `common` "is passed by a caller that
has already resolved the common git directory, so nothing here costs a second
`git` call". The new caller does not pass it.

**On the deferral.** *Resolve the root once for all three gates* is the right
disposition for the `--show-toplevel` call, which is genuinely shared and
carries a rider on `optin.repo_root` counting it. It does not cover calls 2
and 3, which are inside one function this branch wrote. The paste-ready fix
below removes them with a default-valued parameter that leaves the other two
gates' call sites unchanged, so it is not the three-gate change the branch
declined.

Measured with that fix applied: local root in a main tree 2 → **1**, local
root in a linked worktree 4 → **2**, no `seal/` unchanged at 1 and 2, shared
root unchanged at 2. The `deny → ask → silent` sequence is unchanged and 191
cases across five modules pass.

## ⑨ ⬜ The fix record calls a re-verify a re-read

`round-1-fixes.md` §*Ledger* says the S8 row "was re-read rather than
re-stamped". The row's anchor hash and `Checked` date both changed, which is
what a re-verify is. The act was right and the note beside it is right; the
sentence describing it says the opposite of what the diff shows, and a later
reader comparing the two will not be able to tell which happened. A
correction to the run's paperwork, not to the tool.

---

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
| 9 | 🔴 The rider stamp names `a3bea92`, a commit of this feature branch, which the squash into `release/v0.9.1` discards — #239's class, one commit after #239's first instance was repaired | `skills/implement/scripts/seal.py:1640` | **open** | executed — squashed `5e56470` onto `2138c98` in a `--no-local` clone: `test_every_rider_stamp_names_a_commit_this_branch_can_reach` exits 0 before and 1 after, naming `a3bea92` |
| 10 | 🟡 The rider drifted `seal.py#other_worktrees` in `seal/ledger.md` and in another work item's ledger fragment, and neither row was re-read or re-stamped | `seal/ledger.md:689` · `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md:73` | **open** | executed — drifted anchors at `9d2f440` 8, at `2138c98` 0, at `ca59969` 9, at `5e56470` 9; the one name at the target and at neither parent is `seal.py#other_worktrees` |
| 11 | 🟡 The stated per-call `git` cost is a main work tree's number: a linked worktree pays 2 where the document says 1 and 4 where it says 2, and two of the four are the new code re-asking a question `optin.home_at` already answered | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/pr-notes.md` · `hooks/mode-gate.py:209-225` | **open** | executed — logging `git` on `PATH`, one `ls` payload: 1/2 from a main tree, 2/4 from a linked worktree; 59.0 ms against the sibling's 27.2 ms there, median of twelve |
| 12 | ⬜ `round-1-fixes.md` says the S8 row was "re-read rather than re-stamped"; its anchor hash and `Checked` date both changed, which is a re-verify | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/rounds/round-1-fixes.md` | **open** | executed — `541502a6` → `b8ea59c3`, 2026-09-07 → 2026-09-08 across `ca59969` |

## Paste-ready fixes

Finding 9 — `skills/implement/scripts/seal.py`, the last two lines of the
rider. `other_worktrees` is byte-identical at `2138c98` and at the target
once comments are stripped, so the release-branch commit carries the same
state the measurement was made against.

```python
    # this list the same way when this function is next opened.
    #
    # Stamped at a commit on the release branch rather than at the fix pass's
    # own, because a feature branch squashes and the commit that measured
    # this stops existing at that merge. #239 holds the class; this is the
    # second instance, and the first turned `release/v0.9.1` red.
    # Verified 2026-09-08 at 2138c98.
```

Finding 10 — `seal/ledger.md:689`, the S26 row. Change the one anchor hash
and the `Checked` date, and add the sentence to the Notes cell. Hand-edited
rather than swept, because `--reverify` rewrites every row and would close
the nine deferrals nobody has read.

```
`skills/implement/scripts/seal.py#other_worktrees@9cc8fc3d`
```

```
2026-09-08
```

```
**Re-read 2026-09-08 in work item 1788817289's round 1 fix pass**, which planted a `# RIDER:` inside this function while enumerating a class; the comment is the whole of what changed, the loop and its answer are untouched, so what this row pins did not move.
```

Finding 10 — the same three edits to
`seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md:73`, the
R4 row, whose anchor is the same unit at the same old hash `ddf91b71`.

```
`skills/implement/scripts/seal.py#other_worktrees@9cc8fc3d`
```

Finding 11 — `hooks/optin.py`, so a caller that has already resolved the
common git directory can say so. The default leaves
`hooks/commit-review-gate.py` and every other caller's call site unchanged,
which is why this is not the three-gate change the branch declined.

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

Finding 11 — and the sentence in `pr-notes.md` that has to change with it.
Re-measure after the fix rather than pasting my numbers, since the fix moves
them.

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

Finding 12 — `round-1-fixes.md` §*Ledger*, first sentence of the second
paragraph.

```
One row in `seal/ledger.md` drifted because this pass rewrote the prose above
`templates/config.md`'s table. It was re-read and then re-verified — the row
pins the table's shape, the table is untouched, and the hash was rewritten
by hand so the nine other drifted rows kept their deferral. A blanket
`--reverify` would have closed that deferral without anyone reading a line.
```

## Regression cases to plant

| Case | Destination file |
|---|---|
| The gate's `git` process count from a linked worktree, so the reduction in finding 11 cannot silently regress: build a clone with a linked worktree and a local root, put a logging `git` on `PATH`, and assert the count for the four states in the table above | `tests/test_the_mode_question_is_asked_once.py` |
| A rider stamp must name a commit that is an ancestor of the RELEASE branch, not only of HEAD — the existing case passes on the feature branch and fails after the squash, which is the wrong time to learn it | `tests/test_a_rider_reaches_its_file.py` |

Each has to be seen red before it is planted: the first with the fix reverted,
the second against `5e56470` as it stands, where it should fail on
`a3bea92`.

## Facts for the evidence ledger

| Claim | Coordinates | Grounds |
|---|---|---|
| The gate spends two prompts per session per repository and is silent after them, in all three repository states | `hooks/mode-gate.py#main`, `tests/test_the_mode_question_is_asked_once.py#test_the_third_command_of_a_session_is_silent` | **Executed** 2026-09-08: 20 calls × 2 sessions × 3 states — 1 deny, 1 ask, 18 silent where a root has no row; 20 silent otherwise |
| A `--separate-git-dir` repository resolves to the caller's own work tree, and a root that is not a work tree is refused rather than named | `skills/code-review/scripts/round_record.py#repo_of`, `skills/code-review/scripts/round_record.py#shares_the_clone` | **Executed** 2026-09-08: separated repository → the caller's tree; bare clone with the caller outside → `None` |

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
| round 1 | `hooks/mode-gate.py#main`, the two-marker decision | the budget lives in six lines; every re-derivation starts here |
| round 1 | `skills/code-review/scripts/round_record.py#repo_of` | the root oracle, and the only place a printed worktree path is turned into a decision |
| round 1 | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/pr-notes.md` §*A prompt budget* | `CONTRIBUTING.md` requires it and a passing suite cannot report on it — round 1 found the budget wrong there, this round found the cost wrong there |
| round 1 | `tests/test_the_mode_question_is_asked_once.py` and `tests/test_local_mode_reaches_the_review_chain.py` | where every case for this work item lives; nothing had to be searched for |
| the branch | `skills/implement/scripts/seal.py#other_worktrees` | named by the fix pass as the second reader of the same list, and the origin of findings 9 and 10 |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether `--worktree` should read routing declarations from the working tree | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/questions.md` Q3 and `seal/follow-up.md` | the repository owner — already deferred by this branch, not re-filed here |
| `tests/test_the_pull_request_language_is_the_repositorys.py#items` reimplements `config_rows` | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/overview.md` §*Not verified* | the repository owner — already deferred by this branch, not re-filed here |
| the eight pre-existing drifted rows in `seal/ledger.md` | `seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/overview.md` §*Not done* | the repository owner — already deferred by this branch. Finding 10 is not one of them |
| resolving `rev-parse --show-toplevel` once for all three gates | the `# RIDER:` on `hooks/optin.py#repo_root` | the repository owner — the right disposition, and finding 11 is the part of the cost that sits outside it |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator — `agent-contract` §2 keeps them out of a round. The broad gate has still not run: `round-1.md` records it as `not yet`, and it comes due after findings 9, 10 and 11 are fixed |
| Windows and Linux behaviour of the gate and of `repo_of` | CI — everything here was executed on macOS |
| whether the two-prompt budget is the right budget, as opposed to the honest one | the repository owner — this round verified that the number stated is the number the code has, not that two is the number to want |

Needs a fix: yes — 9, 10 and 11
Loses a record or crashes: no
Contract changes: `hooks/mode-gate.py#already_asked` — `(cwd, git_dir, session)` became `(git_dir, session, choice_dir=CHOICE_DIR)`, callers `main` and `tests/test_the_mode_question_is_asked_once.py`; `hooks/mode-gate.py#git_dir_of` — `(root)` became `(root, which="--absolute-git-dir")`, callers `marker_dir` and `tests/test_the_mode_question_is_asked_once.py#test_the_marker_directory_is_absolute_for_either_question`; `skills/code-review/scripts/round_record.py#repo_of` — the return type widened to include `None`, caller `where`, which turns it into a `Refused`
New units: RETRY_DIR (depth 1); unreadable (depth 1); marker_dir (depth 1); common_dir_of (depth 1); shares_the_clone (depth 1); test_a_separated_git_directory_does_not_displace_the_callers_tree (depth 1); test_the_clone_is_identified_from_the_directory_it_was_asked_about (depth 1); test_a_root_that_is_not_a_work_tree_is_refused (depth 1); test_the_third_command_of_a_session_is_silent (depth 1); test_the_two_prompts_are_counted_apart (depth 1); test_a_config_nobody_can_open_is_silence_not_a_deny (depth 1); test_one_local_root_is_one_question_for_the_whole_clone (depth 1); test_a_shared_root_is_still_a_question_per_work_tree (depth 1); test_the_marker_directory_is_absolute_for_either_question (depth 1)

## Proof block

Read: `hooks/mode-gate.py`, `hooks/optin.py`, `hooks/config.py` (`config_path`,
`config_rows`), `skills/code-review/scripts/round_record.py` (`git`, `repo_of`,
`common_dir_of`, `shares_the_clone`, `worktrees_of`, `where`, `run_check`),
`skills/implement/scripts/seal.py` (`other_worktrees` and its rider),
`templates/config.md`, `seal/config.md`, `seal/ledger.md` (the S8 and S26 rows),
`seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md`,
`seal/follow-up.md`,
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/pr-notes.md`,
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/changelog.md`,
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/routing.md`,
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/rounds/round-1.md`,
`seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/rounds/round-1-fixes.md`,
`tests/test_a_rider_reaches_its_file.py`,
`tests/test_the_mode_question_is_asked_once.py`,
`tests/test_local_mode_reaches_the_review_chain.py`, `CONTRIBUTING.md`,
`/Users/x/.claude/skills/writing-style/SKILL.md`.

Diffs read in full: `1a54687`, `a3bea92`, `ca59969`, `0f8e893`, `2138c98`, and
`git diff 9d2f440..5e56470` for `seal/ledger.md`, `seal/follow-up.md`,
`templates/config.md` and `README.md`.
