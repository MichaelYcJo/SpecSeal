# Round 1 report — 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest

| Field | Value |
|---|---|
| Target SHA | edd35c56f4730cbd7b7266b10ac287c5d138cd7f |
| Base | `origin/release/v0.20.0` (86cbd9a2) |
| Pull request | #850 (draft) |
| Round kind | finding round — the branch, spec compliance first |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

The branch does what `spec.md` asks in the main. The guard reads each git
segment as listed, a switch, a creation or unrecognised. It stops only where
the tree matters, denies under the press, and the four readings and their
cases are gone. The policy says what the code does, with one exception
below.

Three defects would ship, and each is a silence or an approval where §A row
1 denies. They are ordered by cause:

1. **The stop's `ask` runs a switch the ladder never judged (🔴 1).** The
   stop comes before the ladder on the grounds that "a stop there stops the
   whole line". That holds for a `deny`. Approving an `ask` runs every
   segment, and only a creation was hooked in front of it. So `git checkout
   f.txt && git -C W switch feature/x` asks about the dirty session tree,
   and one approval switches `W` while another session is ACTIVE there. The
   base denied this command (executed).
2. **A closed descriptor hides the deciding word (🔴 2).** `_plain_words`
   reads `2>&-`, `>&-` and `<&-` as taking the next word as their target.
   So `git worktree 2>&- add ../wt b` is listed and silent in a dirty or
   ACTIVE tree, and bash creates the worktree (executed). The base asked
   about it. Phase 3's enumeration walked every operator, but for `>&` and
   `<&` it walked one target only, `1`, which is why it missed this.
3. **`rebase` is listed, and `git rebase <upstream> <branch>` switches
   first (🔴 3).** git 2.50.1 left HEAD on `feature/x` after `git rebase
   main feature/x`, `git rebase --onto main main feature/x` and `git rebase
   --root feature/x` (executed). The build is silent on all three in an
   ACTIVE tree. The base was silent too, so this is not a regression. But it
   is the list's own claim, and the smith asked for exactly this check.

Two smaller defects:

- `_merged_findings` fails open (🟡 4). When the reader is missing or
  raises, the cut `&` group reads as no finding. The policy says a broken
  reader "costs a stop … and never a silence".
- Phase 3 closed the `-C` gap for a hidden git only (🟡 5). A string's `-C`
  is still judged in the tree the string was typed from, so `sh -c 'git -C
  W switch x'` is silent with `W` dirty. The base was silent too, and no
  sentence names it.

Two notes: a stale module comment (⬜ 6), and `git branch -m` against the
spec's literal definition (⬜ 7).

Seven pytest workflows of #850 were still pending when this report was
written (❓).

## Spec compliance

| Spec clause | What the code does | Label |
|---|---|---|
| In 1, three shapes from the frozen words | `_segment_finding` → `_git_finding` for a frozen git, `_hidden_in` otherwise; `shape_of` returns the shape | read; executed in the probe (16 spellings, build against base) |
| In 1, a body read through the same shapes, recursively | `_command_findings` → `_first_finding_in`, depth bound `BODY_DEPTH` | read |
| In 2, only where the tree matters, each shape in its own tree | the loop at `hooks/worktree-guard.py:2878`, `tree_matters`, `_finding_tree`, dedupe by directory | read; executed (the two-tree rows of 🟡 5) |
| In 2, a switch and an unrecognised shape on one line | the stop comes first. On the `ask` path the switch is never judged | **diverges, 🔴 1** |
| In 3, the two readers; the press read and not the record | `automation_pressed` wraps `worktree_consent.automation_answered` as the commit gate does; `deny if pressed or active` | read |
| In 4, the readings go | S11's case, and `uvx ruff check` is clean | executed (ruff); read (symbols) |
| In 5, the list holds what leaves the branch | 48 of 49 rows hold. `rebase` does not when it names a branch | **executed against git, 🔴 3** |
| In 6, policy, cases, records | §A, §*Which tree*, §*Creation consent*, §*Known limits* rewritten; `Enforced by:` lines name existing cases | read |
| S14, the numbers reach the PR body | the body's table matches `phases/phase-3.md` and `phases/phase-4.md` cell for cell; zero person-stops under the press is stated | read |

## 🔴 1 — The stop's `ask` lets one approval switch a tree another session is ACTIVE in

**Where.** `hooks/worktree-guard.py:2699` (`stop_unrecognised`'s
decision) and the call at `hooks/worktree-guard.py:2889`.

**What is wrong.** The stop runs before the ladder, on the grounds in
`spec.md` In 2 and in the policy that "a stop there stops the whole line".
A `deny` does stop the whole line. An `ask` does not: approving it runs
every segment. The code knows this for a creation and passes `before_ask`
for one. It does nothing for a switch, so the switch's own tree is never
judged.

**Why it matters.** Executed, without the press, with the session tree
dirty and `W` ACTIVE:

| Command | Build | Base |
|---|---|---|
| `git -C W switch feature/x` | deny | deny |
| `git checkout f.txt && git -C W switch feature/x` | **ask** | deny |
| `git update-ref refs/x HEAD && git -C W switch feature/x` | **ask** | deny |
| `git checkout f.txt && cd W && git switch feature/x` | **ask** | deny |
| the same with `W` IDLE (the `choose` row) | **ask** | deny |

The ask names the session tree's changes and lists `git checkout f.txt`.
It says nothing about `W` or the session in it. One approval switches `W`,
which is what §A row 1 and the P5 reasoning in `overview.md` exist to
prevent: "an `ask` would let one approval take the branch out from under
that session".

**The fix.** When a switch is on the line, the stop is a `deny`. That
costs no person a prompt, by P5's own argument: the model splits the line,
and the switch meets its rows on the retry. S9 changes from `ask` to
`deny`, and the policy sentence about the `ask` path gains the switch.

## 🔴 2 — A closed descriptor in front of `add` or `branch` hides it, and the worktree is created silently

**Where.** `hooks/worktree-guard.py:2161`.

**What is wrong.** `skip = word[-1] in "<>&|!-"` treats every word ending
in `-` as an operator whose target is the next word. That is right for
`<<-` (the target is the delimiter). It is wrong for `>&-`, `<&-` and
`N>&M-`. Those close or move a descriptor and take no target. So
`_plain_words(["2>&-", "add", "../wt", "b"])` drops `add`, and
`_hidden_mover` sees `../wt` as the first word bash hands git.

**Why it matters.** Executed:

| Command | Tree | Build | Base |
|---|---|---|---|
| `git worktree 2>&- add ../wt b` | dirty | **silent** | ask |
| `git worktree >&- add ../wt b` | dirty | **silent** | ask |
| `git worktree <&- add ../wt b` | dirty | **silent** | ask |
| `git worktree 2>&- add ../wt feature/x` | ACTIVE | **silent** | ask |
| `git stash 2>&- branch x` | ACTIVE | **silent** | silent |

bash runs `git worktree 2>&- add ../wt-close feature/x` and `git worktree
>&- add -b viaclose ../wt-out2`, and both worktrees exist afterwards. `git
stash 2>&- branch stashed` leaves HEAD on `stashed` (git 2.50.1, executed).

**Why the enumeration missed it.** `_redirections` in
`tests/test_guard_resolves_the_tree_it_judges.py` gives `>&` and `<&` one
target, `1`, so the closing forms `-` and `1-` were never placed. Phase 3's
208-shape case enumerated the operators of the class and only one of
their target kinds. The fix covers the reader and adds those target kinds
to the generator.

## 🔴 3 — `rebase` is listed, and `git rebase <upstream> <branch>` switches to `<branch>` first

**Where.** `hooks/worktree-guard.py:2086` (the `rebase` row of
`LEAVES_THE_TREE`) and `_git_finding`.

**What is wrong.** git-rebase(1) says that where `<branch>` is given,
"git rebase will perform an automatic `git switch <branch>` before doing
anything else", and HEAD stays there. Executed in a scratch repository on
git 2.50.1, with HEAD on `main` before each:

| Command | HEAD after |
|---|---|
| `git rebase main feature/x` | `feature/x` |
| `git rebase --onto main main feature/x` | `feature/x` |
| `git rebase --root feature/x` | `feature/x` |

The build is silent on `git rebase main feature/x` in an ACTIVE tree
(executed). The other 48 rows hold on reading. `stash` holds by exception
(`stash branch` is excepted, executed above), and `branch` holds where the
branch is renamed rather than switched (⬜ 7).

**Why it matters.** This is the silent switch over a working session that
the Premise exists to stop. The base was silent on it too, so the branch
did not cause it. But the branch adds a list that claims positive knowledge,
and `overview.md` §*Not verified* put this row's judgment to this round. The
list's comment says the judgment "was read off what each does, not run
against git", and nothing in the suite binds it to git. The S10 case binds
the counts. The option-table binding it replaced bound git itself.

**The fix.** A `rebase` that can name a branch is unrecognised: two words
that are not options, or `--root` with one. No option table is read, so an
option's value counts as a word, and the cost lands in the safe direction
(`git rebase --onto main x` stops too). The corpus holds 2 `rebase` pairs.
The plain spelling is `git switch <branch>` followed by `git rebase
<upstream>`.

## 🟡 4 — A broken or missing reader leaves an `&`-cut group silent

**Where.** `hooks/worktree-guard.py:2321` and `hooks/worktree-guard.py:2341`.

**What is wrong.** `_merged_findings` returns `[]` when `wide` is None and
when `merged_view` raises. The policy sentence in §*Which tree* says that
where `hooks/cmdline.py` "fails to load, or a reader in it raises", a
hidden git "costs a stop where the tree matters and never a silence".

**Why it matters.** Executed, in a dirty tree:

| Command | Reader | Build |
|---|---|---|
| `2>&1 git switch feature/x` | `merged_view` raising | silent |
| `git worktree &>/dev/null add ../wt b` | `merged_view` raising | silent |
| `git worktree &>/dev/null add ../wt b` | `wide` None | silent |
| `2>&1 git switch feature/x` | `wide` None | ask (`_hidden_in`'s bare-word test reaches it) |

`test_a_broken_wider_reader_costs_a_stop_never_a_silence` exercises the
segment and body paths, not this one. The retired
`test_a_broken_wider_reader_costs_only_the_question` had no cut group to · NAME NOT IN TREE
cover either, so no property was dropped. The new claim is wider than what
pins it.

## 🟡 5 — A string's `-C` is judged in the tree the string was typed from

**Where.** `hooks/worktree-guard.py:2397` (`_finding_tree`) and `_hidden_in`.

**What is wrong.** Phase 3 found that a git only the wider reader reads
"carried a `-C` nothing applied", and it closed that for the `hidden` kind.
`_finding_tree` composes the wider `-C` only where `wide.parse_git` reads
the segment itself as git. A `string` finding (`sh -c`, `bash -c`, `eval`)
is not such a segment, so its inner `-C` is never read. Executed, with `W`
dirty and the session tree clean:

| Command | Build | Base |
|---|---|---|
| `2>/dev/null git -C W switch feature/x` | ask | ask |
| `sh -c 'git -C W switch feature/x'` | silent | silent |
| `echo $(git -C W checkout feature/x)` | silent | silent |
| `cd W && sh -c 'git checkout feature/x'` | ask | silent |

**Why it matters.** It is not a regression. The body row is covered by the
§*Known limits* bullet on bodies, which `spec.md` In 1 grounds. The string
row has no sentence anywhere. `spec.md` In 2 judges a string in "the tree
its segment names", which is the typed-from tree, so the code follows the
spec. But the policy's "A git only the commit gate's wider reading reads
is judged in the tree its own `-C` names" reads as covering a string too,
and it does not. The fix below names the limit. Reading the string's own
`-C` is the alternative, if the owner wants the class closed.

## ⬜ 6 — The module comment still says the wider reader never picks the tree

`hooks/worktree-guard.py:157`: "It never takes the first slot and never
picks the tree (#689)". `_finding_tree` now composes that reader's `-C` into
the tree a hidden git is judged in, and §*Which tree* says "One answer names
a tree". The sentence should say the same.

## ⬜ 7 — `git branch -m` leaves HEAD on a different branch name

`spec.md` Grounding defines leaving the tree as "HEAD names the same branch
… when the command ends". `git branch -m renamed` while on `main` leaves
HEAD on `renamed` (executed). The other session's next edits still land on
the same line of history, so the Premise holds and `branch` stays listed.
One clause beside the `branch` row would stop the next reader from
re-deriving this.

## What the smith left for this round

- **`_finding_tree` and #689.** It is consistent and bounded. #689 took the
  wider reading back because two readings competed for one slot, the
  *first* switch and its tree, and the order decided which tree. Here no
  slot is shared. Each finding is judged in its own tree, and the wider
  `-C` only applies to a segment the frozen reading reads no git in. It is
  composed onto the directory the frozen walk placed that segment in, and it
  spawns nothing beyond the `repo_paths` the loop already pays once per
  directory. The equivalent mutant recorded in phase 3 holds on reading. The
  comment at line 157 is stale (⬜ 6), and the class stops short of strings
  (🟡 5).
- **`LEAVES_THE_TREE` against git.** See 🔴 3. `stash branch` was run and
  switches, and it is excepted. `worktree` other than `add` was read, not
  run.
- **The three silences phase 3 closed.**
  - The redirection hiding `add`/`branch`: closed for every operator with
    a file target, not for a closing descriptor (🔴 2).
  - One lookup per tree, every tree: closed. The loop reads each
    directory, and the two-tree rows of 🟡 5 meet each shape in its own
    tree.
  - The hidden git's `-C`: closed for the `hidden` kind, not for a string
    (🟡 5).
- **The 48 retired or rewritten cases.** I read the phase-3 table and
  opened the generator, S9, S10 and the two-tree helpers. Each retirement
  goes with a removed subject. Two properties the new design owes have no
  case that binds them in full: the list's judgment against git (🔴 3,
  where the option-table binding was retired,
  `test_the_option_table_binds_the_installed_git`), and the broken-reader · NAME NOT IN TREE
  property on the cut path (🟡 4). Each fix plants its case.
- **#841's fragment and records (974dc542).** Both removed rows, S5 and
  `Re-read · D1`, rested only on cases this branch retired. Both sat in an
  unreleased fragment, and the fragment's existence is the not-shipped
  boundary in `docs/the-evidence-ledger.md`. That document's rule is that a
  row whose anchor a change removes "is `REMOVED`, not re-pointed — its
  claim went with the code". Only a released row is never removed. D1 keeps
  one correcting row, in this item's fragment, so no family holds two. I
  checked the 28 marker lines one by one against `git grep`. Each names at
  least one retired helper of the sampler, a `path#name` the named file
  lacks, or a retired case left only in `.test_durations`. None is on a
  line where every name still exists.
- **P5.** For the stop's own tree the code matches the rewritten §A: `deny`
  in an ACTIVE tree whatever the press. §A row 1 speaks of a branch-form
  `checkout`, and the new paragraph widens it to every unrecognised shape.
  The code follows the paragraph. The one place the code falls short of row
  1 is the switch's tree on the same line (🔴 1). Which answer P5 takes is
  the owner's.
- **The body limit (`overview.md` §*Not verified*).** It stands. `spec.md`
  In 1 grounds it, §*Known limits* names it, and the base was silent on
  `cd W && echo $(git checkout feature/x)` too (executed). Its reason,
  "belong to no one segment", is looser than the case: a body nested in one
  segment could take that segment's tree from its opener's offset. That
  would be an extension, not a repair.
- **#850's workflows.** Read at the end of the round: `lint`, `ledger`,
  `arm-check-grammar (3.13)`, `arm-check-grammar (3.14)` and `release`
  pass. `pytest (macos-latest, 3.12, 35)`, `pytest (ubuntu-latest, 3.12,
  15)` and the four Windows shards were pending.

## Regression tests to plant

| Finding | Destination | What it asserts |
|---|---|---|
| 🔴 1 | `tests/test_worktree_guard.py` | a dirty session tree and an ACTIVE `W`. `git checkout f.txt && git -C W switch feature/x` without the press is `deny`. S9's expectation moves from `ask` to `deny`. Red at HEAD (executed: `ask`) |
| 🔴 2 | `tests/test_guard_resolves_the_tree_it_judges.py` | `_redirections` also yields `>&`/`<&` with the targets `-` and `1-`. `test_no_redirection_makes_a_moving_verb_listed_wherever_it_stands` then fails at HEAD on `git worktree 2>&- add ../wt b` (executed: silent) |
| 🔴 3 | `tests/test_worktree_guard.py` | `git rebase main feature/x`, `git rebase --onto main main feature/x` and `git rebase --root feature/x` stop in a dirty tree. `git rebase main`, `git rebase -i HEAD~3` and `git rebase --continue` stay silent. Plus one case that runs `git rebase main feature/x` in the `repo` fixture and asserts HEAD moved, so the judgment is bound to git |
| 🟡 4 | `tests/test_worktree_guard.py` | with `wide` None, and with `merged_view` raising, `git worktree &>/dev/null add ../wt b` and `2>&1 git switch feature/x` stop in a dirty tree |

## Facts for the evidence ledger

- `git rebase <upstream> <branch>`, `git rebase --onto <a> <b> <branch>` and
  `git rebase --root <branch>` leave HEAD on `<branch>` (git 2.50.1,
  executed in this round).
- bash runs `git worktree 2>&- add …` and `git worktree >&- add …` as a
  creation, and `git stash 2>&- branch x` as a switch to `x` (executed).
- `git branch -m <new>` on the current branch leaves HEAD naming `<new>`
  (executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | the stop's `ask` runs a switch on the same line that the ladder never judged, so one approval switches a tree another session is ACTIVE in | `hooks/worktree-guard.py:2699` | open | executed: four commands `ask` at HEAD where the base denied; `spec.md` In 2's "a stop there stops the whole line" holds only for a `deny` |
| 🔴 2 | `_plain_words` reads `>&-`, `<&-` and `2>&-` as taking the next word, so `git worktree 2>&- add …` and `git stash 2>&- branch x` are listed | `hooks/worktree-guard.py:2161` | open | executed: silent in dirty and ACTIVE trees where the base asked; bash creates the worktree |
| 🔴 3 | `rebase` is listed, and `git rebase <upstream> <branch>` switches HEAD to `<branch>` | `hooks/worktree-guard.py:2086` | open | executed against git 2.50.1: three forms move HEAD; the build is silent in an ACTIVE tree |
| 🟡 4 | `_merged_findings` returns no finding when the reader is missing or raises, against the policy's "never a silence" | `hooks/worktree-guard.py:2321` | open | executed: three silent rows in a dirty tree |
| 🟡 5 | a string's `-C` is judged in the typed-from tree, and no sentence names it | `hooks/worktree-guard.py:2397` | open | executed: `sh -c 'git -C W switch feature/x'` silent with `W` dirty; not a regression |
| ⬜ 6 | the module comment says the wider reader never picks the tree | `hooks/worktree-guard.py:157` | open | read: `_finding_tree` composes its `-C` |
| ⬜ 7 | `git branch -m` leaves HEAD on a different name, against `spec.md`'s literal definition | `hooks/worktree-guard.py:2056` | open | executed; the Premise holds, so a comment only |
| 🟢 | `_finding_tree` reads past the frozen walk only for a segment it reads no git in, one `-C` per finding, judged in that finding's own tree | `hooks/worktree-guard.py:2397` | confirmed | read; no slot is shared, so #689's ordering failure cannot arise |
| 🟢 | each unrecognised shape is judged in its own tree, each directory looked up once | `hooks/worktree-guard.py:2878` | confirmed | read; executed in the two-tree rows of 🟡 5 |
| 🟢 | #841's S5 and `Re-read · D1` were removed under the ledger's REMOVED rule, and every marker sits on a line naming a name the tree no longer has | `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` | confirmed | read: the rule in `docs/the-evidence-ledger.md`; each of the 28 lines checked against `git grep` |
| 🟢 | in the stop's own tree the code denies under an ACTIVE session whatever the press, as the rewritten §A says | `hooks/worktree-guard.py:2699` | confirmed | read; P5's choice stays the owner's |
| 🟢 | the body limit stands: `spec.md` In 1 grounds it, §*Known limits* names it, and the base was silent too | `docs/worktree-guard-spec.md` | confirmed | executed: `cd W && echo $(git checkout feature/x)` silent at HEAD and at the base |
| ❓ | #850's seven pytest workflows (macOS, Ubuntu, four Windows shards) | `gh pr checks 850` | ❓ out of verified scope | pending at the end of the round; the orchestrator reads them again before the next round |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_the_guard_asks_once_per_session.py tests/test_guard_resolves_the_tree_it_judges.py tests/test_the_frozen_reading_never_grows.py -q` in the clone at edd35c56 | 287 passed, 1 failed. The failure was this round's own leaving: the base guard copied into `hooks/` for the probe made a third reader of the frozen module. Re-run of `tests/test_the_frozen_reading_never_grows.py` after deleting it: 3 passed |
| `uvx ruff check` on the guard and the three touched test modules | all checks passed |
| a deleted `test_tmp_*` probe loading the build and the base's `hooks/worktree-guard.py` (`git show base:…`, beside the unchanged `cmdline_base.py`, `cmdline.py`, `worktree_consent.py` and `tokens.py`), with `sessions_in_tree` stubbed per tree | the build and base verdicts quoted in 🔴 1, 🔴 2, 🔴 3, 🟡 4, 🟡 5 and the body row; 16 precommand and alias spellings agree with the base or stop where it was silent |
| a deleted `test_tmp_*` script driving git 2.50.1 and bash from Python in a scratch repository | the rebase, fd-close, `stash branch` and `branch -m` rows in the findings and the ledger facts |
| `gh pr checks 850`, twice | first read: `lint` passed, everything else pending; second read: `lint`, `ledger`, `arm-check-grammar (3.13)`, `arm-check-grammar (3.14)` and `release` passed, the seven pytest legs pending |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. Nothing is open for it until the findings above are answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| P5 — whether an unrecognised shape in an ACTIVE tree is denied whatever the press | `questions.md` P5, already open | the repository owner, at the pull request |

## Paste-ready fixes

### 🔴 1

```python
# hooks/worktree-guard.py, stop_unrecognised: a switch elsewhere on the line
# makes the stop a deny, because approving an ask would run it past §A.
def stop_unrecognised(findings, state, pressed, before_ask=None, switch_on_line=False):
    ...
    decision = "deny" if pressed or active or switch_on_line else "ask"
    if decision == "ask" and before_ask is not None:
        before_ask()
    ending = (
        tr(
            "Re-issue the command in a plain spelling.",
            "평범한 표기로 다시 실행하세요.",
        )
        + (
            tr(
                " Run the `git switch` as a command of its own, so the "
                "branch-switch rules judge its tree.",
                " `git switch` 는 따로 실행해 브랜치 전환 규칙이 그 트리를 판단하게 하세요.",
            )
            if switch_on_line
            else ""
        )
        if decision == "deny"
        else tr(
            "Approve to run it as written, or decline and re-issue it in a plain "
            "spelling.",
            "그대로 실행하려면 승인하고, 아니면 거부한 뒤 평범한 표기로 다시 "
            "실행하세요.",
        )
    )

# hooks/worktree-guard.py, main, the call in the stop loop:
                stop_unrecognised(
                    [found[1] for found in unrecognised],
                    (active, idle, reliable, entries),
                    automation_pressed(repo_paths(cwd)[0], session_id, transcript_path),
                    before_ask=...,  # unchanged
                    switch_on_line=switch_at is not None,
                )
```

```python
# tests/test_worktree_guard.py, S9's first half becomes:
    assert decision == "deny" and STOP in reason, reason


def test_a_switch_beside_a_stop_is_not_approved_past_an_active_tree(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1, red 1. Approving the stop's ask runs every segment, so a
    switch on the line in a tree another session is ACTIVE in made the
    ACTIVE deny of §A row 1 one approval away. Asked at edd35c56."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    in_state(monkeypatch, repo, "dirty")
    monkeypatch.setattr(
        wg,
        "sessions_in_tree",
        lambda top, own="": (ACTIVE, [], True) if top.endswith("W") else ([], [], True),
    )
    for command in (
        f"git checkout f.txt && git -C {w} switch feature/x",
        f"git checkout f.txt && cd {w} && git switch feature/x",
    ):
        assert verdict(monkeypatch, capsys, repo, command)[0] == "deny", command
```

```markdown
docs/worktree-guard-spec.md §A, the two-readers paragraph, after "…because
approving runs every segment.":

A switch on the same line makes the stop a `deny` whoever is at the
keyboard, for the same reason: approving would run the switch past the rows
above, in a tree the stop's reason does not describe.
```

### 🔴 2

```python
# hooks/worktree-guard.py, _plain_words: `>&-`, `<&-` and `N>&M-` close or
# move a descriptor and take no target; `<<-` still takes its delimiter.
            skip = word[-1] in "<>&|!-" and not re.search(r"[<>]&[0-9]*-$", word)
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py, _redirections: give the
# duplicating operators their closing and moving targets too.
    for op in (o.replace("\\", "") for o in re.split(r"(?<!\\)\|", operators)):
        target = {"<<<": "word", "<<": "EOF", "<<-": "EOF"}.get(op, "/dev/null")
        targets = [target]
        if op.endswith("&"):
            targets = ["1", "-", "1-"]
        fds = [""] if op.startswith("&") else ["", "2", "{fd}"]
        pairs += [(fd + op, t) for fd in fds for t in targets]
    return pairs
# test_the_redirections_are_read_from_the_reader counts operators, not
# pairs, so it holds unchanged. Run the module after: the LISTED direction
# meets the new targets too.
```

### 🔴 3

```python
# hooks/worktree-guard.py, beside _hidden_mover:
def _rebase_names_a_branch(args) -> bool:
    """Whether a `rebase`'s words can name the branch it switches to first.

    `git rebase <upstream> <branch>` and `git rebase --root <branch>` run
    `git switch <branch>` before anything else, and HEAD stays there
    (git-rebase(1); executed on git 2.50.1, round 1 of work item 1791270162).
    Read without an option table, so an option's value counts as a word and
    the cost is a stop: `git rebase --onto main x` stops too."""
    plain = [w for w in _plain_words(args) if not w.startswith("-")]
    return len(plain) >= (1 if "--root" in args else 2)


# hooks/worktree-guard.py, _git_finding, before `if sub in LEAVES_THE_TREE:`
    if sub == "rebase" and _rebase_names_a_branch(args):
        return "unrecognised", Finding("rebase", words)


# hooks/worktree-guard.py, _described, beside the `checkout` kind:
    if kind == "rebase":
        return (
            tr(
                "a `git rebase` naming a branch, which git switches to before it "
                "rebases",
                "브랜치를 지정한 `git rebase` 로, git 은 리베이스하기 전에 그 "
                "브랜치로 전환합니다",
            ),
            tr(
                "Write `git switch <branch>` first, then `git rebase <upstream>`.",
                "먼저 `git switch <branch>` 를 실행한 뒤 `git rebase <upstream>` 을 "
                "쓰세요.",
            ),
        )


# hooks/worktree-guard.py, LEAVES_THE_TREE:
        "rebase",  # 2/2, one word at most (`_rebase_names_a_branch`); HEAD detached while it runs: a named limit
```

```python
# tests/test_worktree_guard.py
@pytest.mark.parametrize(
    "command",
    [
        "git rebase main feature/x",
        "git rebase --onto main main feature/x",
        "git rebase --root feature/x",
    ],
)
def test_a_rebase_naming_a_branch_is_unrecognised(monkeypatch, capsys, repo, command):
    """Round 1, red 3. git switches to the named branch before it rebases."""
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "ask" and "git switch <branch>` first" in reason, reason


@pytest.mark.parametrize(
    "command", ["git rebase main", "git rebase -i HEAD~3", "git rebase --continue"]
)
def test_a_rebase_of_the_current_branch_stays_listed(command):
    assert wg.shape_of(command.split()) == "listed"


def test_git_switches_before_a_rebase_naming_a_branch(repo):
    """Binds the row above to git: if this stops holding, the list may say less."""
    import subprocess

    run = lambda *a: subprocess.run(
        ["git", "-C", str(repo), *a], capture_output=True, text=True
    )
    start = run("symbolic-ref", "--short", "HEAD").stdout.strip()
    run("rebase", start, "feature/x")
    assert run("symbolic-ref", "--short", "HEAD").stdout.strip() == "feature/x"
```

```markdown
docs/worktree-guard-spec.md §A, the `listed` bullet, after "…each beside its
count,":

except a `rebase` with two words that are not options, or `--root` and one,
which names the branch git switches to before it rebases and is
unrecognised;
```

### 🟡 4

```python
# hooks/worktree-guard.py, beside _merged_findings:
def _cut_unread(items):
    """Where the reader that rejoins an `&` cut is missing or raises, a cut
    in a command holding the bare word `git` is the finding: a broken reader
    costs a stop, never a silence (§*Which tree*)."""
    cut = [i for i, (sep, _tokens) in enumerate(items) if sep == "&"]
    if cut and any(_holds_git(" ".join(t)) for _sep, t in items):
        text = " ".join(" ".join(t) for _sep, t in items)
        return [(cut[-1], Finding("unread", text))]
    return []


# hooks/worktree-guard.py, _merged_findings: both early returns
    if wide is None:
        return _cut_unread(items)
    ...
    except (Exception, SystemExit):
        return _cut_unread(items)
```

```python
# tests/test_worktree_guard.py
@pytest.mark.parametrize(
    "command", ["git worktree &>/dev/null add ../wt b", "2>&1 git switch feature/x"]
)
@pytest.mark.parametrize("broken", ["missing", "raising"])
def test_a_broken_reader_leaves_no_cut_group_silent(
    monkeypatch, capsys, repo, command, broken
):
    """Round 1, yellow 4."""
    in_state(monkeypatch, repo, "dirty")
    if broken == "missing":
        monkeypatch.setattr(wg, "wide", None)
    else:

        def boom(*_a, **_k):
            raise RuntimeError("broken reader")

        monkeypatch.setattr(wg.wide, "merged_view", boom)
    assert verdict(monkeypatch, capsys, repo, command)[0] == "ask", command
```

### 🟡 5

```markdown
docs/worktree-guard-spec.md §Known limits, after the body bullet:

- A string handed to a shell (`sh -c`, `bash -c`, `eval`) is judged in the
  tree its segment names, the one it was typed from: its own `-C` and `cd`
  are not read. `sh -c 'git -C W switch x'` with `W` dirty and the session's
  tree clean says nothing, as it did before #826. Only a git the wider
  reading reads as a segment of its own has its `-C` composed.
```

```markdown
docs/worktree-guard-spec.md §A, the paragraph "Each unrecognised shape is
judged…", the sentence "A git only the commit gate's wider reading reads is
judged in the tree its own `-C` names." becomes:

A git the commit gate's wider reading reads as a segment of its own (behind
a redirection or a zsh precommand word) is judged in the tree its own `-C`
names; a string handed to a shell is not read for one.
```

Needs a fix: yes — 🔴 1, 🔴 2, 🔴 3, 🟡 4 and 🟡 5: a switch beside the stop's ask is approved past an ACTIVE tree, a closed descriptor hides `worktree add` and `stash branch`, `git rebase <upstream> <branch>` switches silently, a broken reader leaves an `&`-cut group silent, and a string's `-C` is neither read nor named

Loses a record or crashes: no


## Proof

Files opened in this round, at edd35c56 in the clone unless named:

- `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/`:
  `routing.md`, `spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `survivors.md`, `handoff.md`, `changelog.md`, `phases/phase-2.md`,
  `phases/phase-3.md`, `phases/phase-4.md`
- `hooks/worktree-guard.py`: 150–186, 1395–1460, 590–650, 2030–3228
- `docs/worktree-guard-spec.md`: 1–35 and the branch's diff against the base
- `docs/the-evidence-ledger.md`: 30–58, 76–130, 168–215
- `tests/test_worktree_guard.py`: 1–30, 95–130, 1100–1200, 1360–1400
- `tests/test_guard_resolves_the_tree_it_judges.py`: 1–62, 716–745,
  1030–1175
- `tests/conftest.py`: 543–568, 812–848
- `bin/test`
- `git show 974dc542` (the #841 ledger fragment and records)
- `gh pr view 850`, `gh pr checks 850`
- the reviewer's instructions: `skills/agent-contract`, `code-review`, and
  the writing-style skill
