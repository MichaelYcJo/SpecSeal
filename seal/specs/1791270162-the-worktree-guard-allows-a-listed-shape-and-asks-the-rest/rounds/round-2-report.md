# Round 2 report — 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest

| Field | Value |
|---|---|
| Target SHA | 274e29bb4101086a6f66cb945238e3c1b63b2131 |
| Fix range under review | `4de95fa7..5ba5e51a` (round 1's fixes, 4 commits) |
| Pull request | #850 (draft) |
| Round kind | verifying round: round 1's closed verdicts, plus the units its `New units` row names |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Every finding round 1 closed is closed for the commands it named. Three
defects remain, and two of them would ship a silent switch where the tree
matters. They are ordered by cause:

1. **`git rebase - <branch>` is still listed (🔴 1).** The new
   `_rebase_names_a_branch` drops every word that starts with `-`, and git
   reads a lone `-` as the previous branch. So `git rebase - feature/x`
   counts one plain word, is listed, and is silent in an ACTIVE tree. Under
   git 2.50.1 it left HEAD on `feature/x` (executed). The base was silent
   too, but this is the class round 1's 🔴 3 closed, one member short.
2. **A git cut by an `&` is judged in the tree of its last part (🔴 2).**
   `main` places a merged finding by the tokens of the group's last part,
   which carry no `-C`. So `2>&1 git -C W switch feature/x` and `git -C W
   worktree &>/dev/null add ../wt b` are silent with `W` ACTIVE, where the
   base asked (executed). Phase 3 closed the hidden git's `-C` for
   `2>/dev/null` and did not reach the `&` cut. This one is a regression.
3. **The broken-reader path inherits the same placement (🟡 3).**
   `_cut_unread` reports the cut at the later part, so with the reader
   missing `git -C W worktree 2>&1 add ../wt b` is silent with `W` dirty.

One more defect is in what the person reads:

- **The stop describes the first tree that matters unless a later one is
  ACTIVE (🟡 4).** With the session's tree dirty and `W` IDLE or
  unreadable, the `ask` says only "1 uncommitted tracked changes". The IDLE
  session in `W` is never shown, and approving runs the checkout there. The
  new case pins that text.

Two notes: the git-binding case does not check that each form ran (⬜ 5),
and `spec.md` still gives `stop_unrecognised` its old signature (⬜ 6).

At the end of the round, Ubuntu and one Windows shard of #850 had passed.
macOS and three Windows shards were still pending, and no job log could be
read before the run ended, so the git-binding case's cost on Windows is
unmeasured (❓).

## Round 1's verdicts, answered

| Round 1 | What the fix does | Answer |
|---|---|---|
| 🔴 1, a switch beside the stop's ask | `switch_on_line` makes the stop a `deny`, and every tree on the line is read before it | Closed. `test_no_approval_runs_a_line_past_an_active_tree` passes, and the probe's ACTIVE-second-tree row denies (executed) |
| 🔴 2, a closed descriptor hides `add` | `_OPERATORS` decides whether a word takes the next one | Closed. Eight forms under bash, every one of which created a worktree or switched, ask in a dirty tree and deny in an ACTIVE one (executed). The `-C` placement in 🔴 2 below is a separate cause |
| 🔴 3, `rebase` naming a branch | `_rebase_names_a_branch` | Closed for the three forms round 1 named (executed through the new cases). The lone `-` is still listed (🔴 1 below) |
| 🟡 4, a broken reader on an `&` cut | `_cut_unread` | Closed for the four rows round 1 measured. A `-C` on the cut group is judged in the wrong tree (🟡 3 below) |
| 🟡 5, a string's `-C` | named in §*Known limits* and §A | Closed. Read: both sentences are in `docs/worktree-guard-spec.md`, and a case pins each |
| ⬜ 6, the module comment | rewritten | Closed. Read: it now names `_finding_tree` |
| ⬜ 7, `branch -m` | a clause beside the `branch` row; ledger row F6 | Closed. Read |

## The questions this round was asked

**Is the cost of reading every tree bounded?** Yes. Each directory is read
once (`placed`), and each tree's sessions and changes once (`seen`). So the
reads grow with the number of distinct trees the line's unrecognised
shapes name, which the command's length bounds. Reads after an ACTIVE tree
change nothing. The smith removed the early exit at `d594eb81` because a
mutation dropping it survived, which trades a few spawns on a rare line for
a case nobody can watch. That is a fair trade.

**Is the reason text right when several trees differ?** No, except where
one is ACTIVE. See 🟡 4.

**Does `_OPERATORS` follow bash's redirection grammar?** Yes, for every form
run. The smith had not run `<<<-` and `<>-` under bash, so this round did.
Bash reads `<<<-` as a here-string of `-` and `<>-` as a file named `-`, so
`add` reaches git in both, and the guard keeps `add` as a word in both.
The spaced `>& -`, `<& -` and `2>& 1-` reach the guard cut at the `&`, and
the merged reading asks about them too.

| Command, run by bash | git | Guard, dirty | Guard, ACTIVE |
|---|---|---|---|
| `git worktree <<<- add ../wtA -b bA` | worktree created | ask | deny |
| `git worktree <>- add ../wtB -b bB` | worktree created | ask | deny |
| `git worktree >- add ../wtC -b bC` | worktree created | ask | deny |
| `git worktree 2>&- add ../wtD -b bD` | worktree created | ask | deny |
| `git worktree >& - add ../wtE -b bE` | worktree created | ask | deny |
| `git worktree <& - add ../wtF -b bF` | worktree created | ask | deny |
| `git worktree 2>& 1- add ../wtG -b bG` | worktree created | ask | deny |
| `git stash <>- branch sx` | HEAD on `sx` | ask | deny |

`<<-` stays in the set, and that is right: its next word is the
here-document's delimiter, so bash never hands it to git.

**Do `_rebase_names_a_branch`'s thresholds hold with options before the
upstream?** For every option form, yes, and each mistake lands on a stop.
`--onto main x`, `-x make main`, `-s ours main` and `--root --onto main`
all stop although none of them switches, because an option's value counts
as a word. The one silence is the lone `-` (🔴 1).

**What does the git-binding case cost on Windows?** Unmeasured. It copies
the repository 56 times and starts about 62 git processes. On macOS under
xdist it took 2.80 s (executed). The Windows shards had not finished (❓).

## 🔴 1 — `git rebase - feature/x` switches HEAD and the guard lists it

**Where.** `hooks/worktree-guard.py:2235`, in `_rebase_names_a_branch`.

**What is wrong.** The function filters out every word starting with `-` to
drop options. git-rebase reads a lone `-` as `@{-1}`, the previous branch,
so `git rebase - feature/x` names an upstream and a branch. The filter
counts one plain word and returns False.

**Why it matters.** Executed on git 2.50.1, with HEAD on `main` and
`@{-1}` naming another branch: `git rebase - feature/x` printed
"Successfully rebased and updated refs/heads/feature/x" and left HEAD on
`feature/x`. The guard reads the command as listed and is silent in an
ACTIVE tree, which is the silent switch over a working session that the
Premise exists to stop. `git rebase -i - feature/x` is listed the same way.
The base was silent too, so this is not a regression, but ledger row F3
states the threshold as closing the class.

**The fix.** Count `-` as a word. The paste-ready fix below was applied in
the round's clone and its cases ran: `git rebase - feature/x` became a
`deny` in an ACTIVE tree, and the three guard modules passed apart from the
case 🟡 4 changes.

## 🔴 2 — A git cut by an `&` is judged in the tree its last part names

**Where.** `hooks/worktree-guard.py:2941`, in `main`, where each result of
`_merged_findings` is placed.

**What is wrong.** `_merged_findings` reads the cut group whole and returns
only the index of its last part. `main` then takes that part's tokens to
find the tree. For `2>&1 git -C W switch feature/x` the last part is `1 git
-C W switch feature/x`, which neither reading reads as git, so
`_finding_tree` falls back to the typed-from directory. For `git -C W
worktree &>/dev/null add ../wt b` the `-C` sits in the first part, and the
last part `>/dev/null add ../wt b` names no tree at all.

**Why it matters.** Executed, with the session's tree clean and `W` as
named:

| Command | `W` | Build | Base (86cbd9a2) |
|---|---|---|---|
| `2>&1 git -C W switch feature/x` | dirty | **silent** | ask |
| `git -C W worktree &>/dev/null add ../wt b` | dirty | **silent** | ask |
| `2>&1 git -C W switch feature/x` | ACTIVE | **silent** | ask |
| `git -C W worktree &>/dev/null add ../wt b` | ACTIVE | **silent** | ask |
| `git -C W stash &>/dev/null branch y` | ACTIVE | **silent** | silent |
| `2>/dev/null git -C W switch feature/x` | ACTIVE | deny | ask |

The last row is phase 3's fix working where no `&` is involved. The rows
above it are the same class, a hidden git's own `-C`, one spelling over.
Round 1's 🟢 that each shape is judged in its own tree rested on the
`2>/dev/null` spelling only.

**The fix.** Return the group's merged words and its first part with each
finding, and place the finding by those. Applied in the clone: all six rows
became `ask` with `W` dirty and `deny` with `W` ACTIVE (executed).

## 🟡 3 — With the reader broken, a cut group's `-C` is never read

**Where.** `hooks/worktree-guard.py:2393`, in `_cut_unread`.

**What is wrong.** The new unit reports each cut at the later part's index,
so `main` places it by the later part's tokens. With `hooks/cmdline.py`
missing, `git -C W worktree 2>&1 add ../wt b` is silent with `W` dirty and
the session's tree clean (executed). The `-C` is in the part before the
cut, where the frozen reading can read it.

**Why it matters.** The policy sentence round 1's fix added says a broken
reader "costs a stop where the tree matters and never a silence". It holds
only where the cut group runs in the typed-from tree.

**The fix.** Hand back the part before the cut, which is where the frozen
reading finds a `-C`. Applied in the clone, the row above became `ask`
(executed). One spelling stays silent: in `2>&1 git -C W switch x` the
`-C` sits after the cut, and only the broken reader could read it there.
The fix names that as a limit.

## 🟡 4 — The stop's reason hides an IDLE or unreadable second tree

**Where.** `hooks/worktree-guard.py:2981`, in `main`, where the state the
stop describes is chosen.

**What is wrong.** The loop keeps the first tree that matters and replaces
it only with an ACTIVE one. With the session's tree dirty and `W` IDLE,
the stop is an `ask` whose reason says only "it has 1 uncommitted tracked
changes, which a switch would carry onto the other branch" (executed). The
same holds with `W` unreadable.

**Why it matters.** §A row 2 answers an IDLE tree by showing the person the
sessions in it, so they can judge whether one is theirs. Here the person is
asked about a different tree's changes, and approving runs `git -C W
checkout feature/x` over the IDLE session without that session ever being
shown. `test_no_approval_runs_a_line_past_an_active_tree` asserts
"uncommitted tracked changes" for the IDLE case, so the case pins the text
this finding says is wrong.

**The fix.** Rank the states by §A's rows (ACTIVE, then IDLE, then
unusable, then changes) and describe the one that says the most. Applied in
the clone: the IDLE case's reason named the IDLE sessions and the
unreadable case named the detection failure (executed). The new case's
IDLE assertion goes red under the fix, as it should, and changes with it.

## ⬜ 5 — The git-binding case does not check that each form ran

`tests/test_worktree_guard.py`, `test_no_listed_form_moves_head_under_git`.
The docstring says the comparison "cannot pass by measuring nothing", and
that holds for `SWITCHING`, which must move HEAD. A `FORMS` entry that git
refuses also leaves HEAD where it was and passes. Under git 2.50.1 every
form ran. `check-ignore f.txt` exits 1, which means "not ignored" (executed).
A git that refused a form on another runner, an older `merge-tree` for
instance, would pass that row unmeasured. Asserting each return code is 0,
or 1 for `check-ignore`, would close it.

## ⬜ 6 — `spec.md` still gives `stop_unrecognised` four parameters

`seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/spec.md:312`
reads `stop_unrecognised(findings, state, pressed, before_ask=None)`. Round
1's fix added `switch_on_line`. This is a correction to the run's
paperwork, not to the tool.

## Regression tests to plant

| Finding | Destination | What it asserts |
|---|---|---|
| 🔴 1 | `tests/test_worktree_guard.py`, the parameters of `test_a_rebase_naming_a_branch_is_unrecognised` | `git rebase - feature/x` and `git rebase -i - feature/x` stop with the rebase sentence. Red at 274e29bb (executed: listed) |
| 🔴 2 | `tests/test_worktree_guard.py` | the session's tree clean and `W` ACTIVE: `2>&1 git -C W switch feature/x`, `git -C W worktree &>/dev/null add ../wt b` and `git -C W stash &>/dev/null branch y` are each `deny`. Red at 274e29bb (executed: silent) |
| 🟡 3 | `tests/test_worktree_guard.py`, beside `test_a_broken_reader_leaves_no_cut_group_silent` | the reader missing, the session's tree clean and `W` dirty: `git -C W worktree 2>&1 add ../wt b` is `ask`. Red at 274e29bb (executed: silent) |
| 🟡 4 | `tests/test_worktree_guard.py`, `test_no_approval_runs_a_line_past_an_active_tree` | the IDLE half asserts the IDLE sentence, and an unreadable `W` asserts the detection sentence. Red at 274e29bb (executed: the changes sentence) |

## Facts for the evidence ledger

- `git rebase - <branch>` reads `-` as `@{-1}` and leaves HEAD on
  `<branch>` (git 2.50.1, executed in this round). Ledger row F3's
  statement of the threshold changes with 🔴 1.
- bash runs `git worktree <<<- add …`, `<>- add …`, `>- add …`, `>& - add
  …`, `<& - add …` and `2>& 1- add …` as a creation, and `git stash <>-
  branch sx` as a switch (executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `_rebase_names_a_branch` drops a lone `-`, so `git rebase - feature/x`, which git runs as a switch to `feature/x`, is listed and silent in an ACTIVE tree | `hooks/worktree-guard.py:2235` | open | executed: HEAD moved under git 2.50.1; the build silent in an ACTIVE tree; the base silent too |
| 🔴 2 | a git cut by an `&` is placed by its last part's tokens, so `2>&1 git -C W switch feature/x` and `git -C W worktree &>/dev/null add ../wt b` are silent with `W` ACTIVE | `hooks/worktree-guard.py:2941` | open | executed against the build and the base: silent where the base asked; a regression |
| 🟡 3 | `_cut_unread` places a cut by the later part, so with the reader missing `git -C W worktree 2>&1 add ../wt b` is silent with `W` dirty | `hooks/worktree-guard.py:2393` | open | executed: silent; the trial fix asks |
| 🟡 4 | the stop describes the first tree that matters unless a later one is ACTIVE, so an IDLE or unreadable second tree is never shown in the `ask` | `hooks/worktree-guard.py:2981` | open | executed: the IDLE and unreadable rows name only the session tree's changes; the new case pins that text |
| ⬜ 5 | the git-binding case passes a `FORMS` row git refused, since it checks no return code | `tests/test_worktree_guard.py:1772` | open | executed: every form ran under git 2.50.1; a refusal elsewhere would pass unmeasured |
| ⬜ 6 | `spec.md` Data & interfaces gives `stop_unrecognised` its pre-round-1 signature | `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/spec.md:312` | open | read; a paperwork correction, not counted in `Needs a fix` |
| 🟢 | round 1's blocking finding 1 is closed — a switch beside the stop, or an ACTIVE second tree, makes the stop a deny | `hooks/worktree-guard.py:2775` | confirmed | executed: the new case passes, and the probe's ACTIVE-second-tree row denies |
| 🟢 | round 1's blocking finding 2 is closed — a closed, moved or `-`-named target takes no next word | `hooks/worktree-guard.py:2155` | confirmed | executed: eight forms under bash, each a creation or a switch, ask in a dirty tree and deny in an ACTIVE one |
| 🟢 | round 1's blocking finding 3 is closed for the three forms it named | `hooks/worktree-guard.py:2226` | confirmed | executed through the new cases; the lone `-` is 🔴 1 of this round |
| 🟢 | round 1's finding 4 is closed for the four rows it measured | `hooks/worktree-guard.py:2383` | confirmed | executed through the new case; the `-C` placement is 🟡 3 of this round |
| 🟢 | round 1's finding 5 is closed — a string's `-C` is named in §*Known limits* and §A | `docs/worktree-guard-spec.md` | confirmed | read; pinned by `test_the_guard_policy_says_nothing_is_read_past_the_base` |
| 🟢 | round 1's notes 6 and 7 are closed — the module comment and the `branch` clause | `hooks/worktree-guard.py:157` | confirmed | read; ledger row F6 carries the `branch -m` fact |
| 🟢 | reading every tree before the stop costs one read per distinct tree on the line, and nothing more | `hooks/worktree-guard.py:2971` | confirmed | read; `placed` and `seen` bound it, and the early exit's removal at `d594eb81` costs only reads that change nothing |
| 🟢 | `_OPERATORS` follows bash for `<<<-`, `<>-`, `>-` and the spaced `>& -`, `<& -`, `2>& 1-` | `hooks/worktree-guard.py:2155` | confirmed | executed under bash; `<<-` correctly keeps its delimiter |
| ❓ | the git-binding case's cost on the Windows shards | `tests/test_worktree_guard.py:1772` | ❓ out of verified scope | 2.80 s on macOS under xdist (executed); 56 copies and about 62 git processes; the Windows shards were pending; the orchestrator reads the durations when they finish |
| ❓ | five of #850's pytest workflows at 274e29bb: macOS and Windows shards 1, 3 and 4 | `gh pr checks 850` | ❓ out of verified scope | pending at the end of the round; `lint`, `ledger`, both `arm-check-grammar` legs, `release`, Ubuntu and Windows shard 2 passed; the orchestrator reads them again before the next round |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py -q --durations=8` in the round's clone at 274e29bb | 222 passed; `test_no_listed_form_moves_head_under_git` 2.80 s, `test_no_approval_runs_a_line_past_an_active_tree` 1.16 s |
| a deleted `test_tmp_*` probe driving bash and git 2.50.1 in copies of the `repo` fixture | the bash table above; `git rebase - feature/x` moved HEAD; every `FORMS` row ran, `check-ignore` with exit 1 |
| the same probe loading 274e29bb's guard and the base's (`git show 86cbd9a2:hooks/worktree-guard.py`, kept outside `hooks/`; the four readers it imports are unchanged since the base), with `sessions_in_tree` stubbed per tree | the build and base columns of 🔴 2; the reason texts of 🟡 4; the shapes of the option forms |
| the paste-ready fixes below applied in the clone, the probe rerun, then `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py tests/test_the_guard_asks_once_per_session.py -q` | every probe row as each fix's section says; 299 passed, 1 failed: `test_no_approval_runs_a_line_past_an_active_tree`'s IDLE assertion, the text 🟡 4 changes. The clone was reverted and the probe deleted afterwards |
| `gh pr checks 850`, three times | first read: `lint` passed, the rest pending. Second read: `lint`, `ledger`, `arm-check-grammar (3.13)`, `arm-check-grammar (3.14)` and `release` passed, the seven pytest legs pending. Third read: `pytest (ubuntu-latest, 3.12, 15)` and the Windows shard `--group 2` passed too; macOS and Windows shards 1, 3 and 4 pending. No job log can be read until the run ends, so no Windows duration was seen. The previous head's `tests` run (edd35c56) concluded success |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. It is not due while 🔴 1, 🔴 2, 🟡 3 and 🟡 4 are open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| P5 — whether an unrecognised shape in an ACTIVE tree is denied whatever the press | `questions.md` P5, already deferred in round 1 | the repository owner, at the pull request |

## Paste-ready fixes

### 🔴 1

```python
# hooks/worktree-guard.py, _rebase_names_a_branch: git reads a lone `-` as
# `@{-1}`, so it is a word that can name the upstream (`git rebase -
# feature/x` switches to feature/x; git 2.50.1, round 2 of 1791270162).
    plain = [w for w in _plain_words(args) if w == "-" or not w.startswith("-")]
    return len(plain) >= (1 if "--root" in args else 2)
```

```python
# tests/test_worktree_guard.py, test_a_rebase_naming_a_branch_is_unrecognised:
# two more parameters.
        "git rebase - feature/x",
        "git rebase -i - feature/x",
```

```markdown
seal/ledger/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest.md,
row F3, the claim's first clause becomes:

a `rebase` with two words that are not options, a lone `-` counted as a
word, or `--root` and one, is unrecognised
```

### 🔴 2

```python
# hooks/worktree-guard.py, _merged_findings: each finding carries the group's
# own words and its first part, so main judges the group in the tree its
# `-C` names rather than the tree of its last part.
                if finding is not None:
                    out.append((parts[-1], finding, toks, parts[0]))
                continue
            if _wide_git(toks):
                out.append(
                    (parts[-1], Finding("hidden", _spoken(toks)), toks, parts[0])
                )

# hooks/worktree-guard.py, _first_finding_in:
    for _index, finding, _toks, _first in _merged_findings(items):
        return finding

# hooks/worktree-guard.py, main:
    for index, finding, toks, first in _merged_findings(items):
        wheres = walked[first][1]
        unrecognised.append((index, finding, toks, wheres[0] if wheres else cwd))
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py, _read_by_the_guard:
    found += [merged[1] for merged in wg._merged_findings(items)]
```

```python
# tests/test_worktree_guard.py
def test_a_cut_group_is_judged_in_the_tree_its_own_c_names(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of work item 1791270162, red 2. A git an `&` cut was judged
    in the tree of the group's last part, which carries no `-C`: silent at
    274e29bb with W ACTIVE, where the base asked."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    monkeypatch.setattr(
        wg,
        "sessions_in_tree",
        lambda top, own="": (ACTIVE, [], True) if top.endswith("W") else ([], [], True),
    )
    for command in (
        f"2>&1 git -C {w} switch feature/x",
        f"git -C {w} worktree &>/dev/null add ../wt b",
        f"git -C {w} stash &>/dev/null branch y",
    ):
        assert verdict(monkeypatch, capsys, repo, command)[0] == "deny", command
```

### 🟡 3

```python
# hooks/worktree-guard.py, _cut_unread: hand back the part before the cut,
# where the frozen reading finds a `-C` (`git -C W worktree 2>&1 add …`).
            if _holds_git(text):
                before = items[index - 1][1]
                out.append((index, Finding("unread", text), before, index - 1))
```

```python
# tests/test_worktree_guard.py
def test_a_broken_reader_judges_a_cut_in_the_tree_its_c_names(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of work item 1791270162, yellow 3. Silent at 274e29bb."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    (w / "f.txt").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(wg, "wide", None)
    command = f"git -C {w} worktree 2>&1 add ../wt b"
    assert verdict(monkeypatch, capsys, repo, command)[0] == "ask", command
```

```markdown
docs/worktree-guard-spec.md §Known limits, after the string bullet:

- Where `hooks/cmdline.py` did not load, a git an `&` cut is judged in the
  tree the part before the cut names: `git -C W worktree 2>&1 add …` is
  judged in `W`, and `2>&1 git -C W switch x`, whose `-C` comes after the
  cut, in the tree it was typed from.
```

### 🟡 4

```python
# hooks/worktree-guard.py, beside stop_unrecognised:
def _weight(state):
    """How much STATE, `(active, idle, reliable, entries)`, says, by §A's
    rows: an ACTIVE session over an IDLE one, over detection unusable, over
    tracked changes. The stop describes the tree that says the most."""
    active, idle, reliable, _entries = state
    return 3 if active else 2 if idle else 1 if not reliable else 0


# hooks/worktree-guard.py, main, the tree loop:
            here_state = (active, idle, reliable, entries)
            if matters and (state is None or _weight(here_state) > _weight(state)):
                state = here_state
```

```python
# tests/test_worktree_guard.py, test_no_approval_runs_a_line_past_an_active_tree,
# the IDLE half of the second loop becomes:
            else:
                assert decision == "ask", (command, decision, reason)
                assert "none of them can be shown to be working" in reason, reason
```

```markdown
docs/worktree-guard-spec.md §A, after "Every tree on the line is read
before the stop is taken, …":

The stop's reason describes the tree that says the most: an ACTIVE session,
then an IDLE one, then detection unusable, then tracked changes.
```

Needs a fix: yes — 🔴 1, 🔴 2, 🟡 3 and 🟡 4: `git rebase - <branch>` switches while listed, a git cut by an `&` is judged in the tree of its last part and so is silent over an ACTIVE `-C` tree, the broken-reader path places a cut the same way, and the stop hides an IDLE or unreadable second tree behind the first tree's changes

Loses a record or crashes: no

## Proof

Files opened in this round, in the round's clone at 274e29bb unless named:

- `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/`:
  `rounds/round-1.md`, `rounds/round-1-report.md`, `overview.md`, `spec.md`
- `seal/ledger/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest.md`:
  rows S1, S3, S10, F3, F6 (by search)
- `hooks/worktree-guard.py`: 2136–2515, 2700–3030, 1296–1325, 1417–1440,
  and `git diff 4de95fa7..5ba5e51a` of it
- `hooks/cmdline.py`: 48–60
- `docs/worktree-guard-spec.md`: `git diff 4de95fa7..5ba5e51a` of it
- `tests/test_worktree_guard.py`: 1–140 and `git diff 4de95fa7..5ba5e51a`
- `tests/test_guard_resolves_the_tree_it_judges.py`:
  `git diff 4de95fa7..5ba5e51a`
- `tests/conftest.py`: 543–565, 820–860
- `bin/test`
- the base guard, `git show 86cbd9a2:hooks/worktree-guard.py`, loaded and
  not read line by line
- `git show d594eb81`
- `gh pr checks 850`, `gh pr view 850`, `gh run list` for the branch
- the reviewer's instructions: the agent contract, `code-review`, and the
  writing-style skill
