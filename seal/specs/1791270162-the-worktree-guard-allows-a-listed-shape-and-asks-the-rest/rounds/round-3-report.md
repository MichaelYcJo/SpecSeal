# Round 3 report — 1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest

| Field | Value |
|---|---|
| Target SHA | 2c3a7f920204672160299f8ee2026655cdc70282 |
| Fix range under review | `3c9a1161..a3164380` (round 2's fixes, 7 commits) |
| Pull request | #850 (draft) |
| Round kind | verifying round after the reopening: round 2's closed verdicts, plus the units its `New units` row names. The reopening is spent, so this record ends the run |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Every finding round 2 closed is closed for the commands it named. One
defect remains in the code, and three notes remain in documents and in the
run's own paperwork. They are ordered by cause:

1. **The rebase class is still one spelling short (🟡 1).** Round 2's fix
   counts a lone `-` and every word after `--`. git has a second way to end
   its options, `--end-of-options`, and it takes any unambiguous prefix of a
   long option, so `--ro` is `--root`. `git rebase --ro feature/x` and `git
   rebase --end-of-options main -x` each left HEAD on the named branch under
   git 2.50.1, and the build is silent on both in an ACTIVE tree (executed).
   The base was silent too, so this is not a regression. No recorded run
   holds either spelling. The unit is one round 2's fixes changed, so this
   is the run's second fix of a fix.
2. **The policy's tree-placement limit names fewer spellings than reach it
   (⬜ 3).** A `cd` whose redirection the splitter cuts at its `&` (`cd W
   2>&1 && git switch x`), and a cut git inside an `if` body after `cd W`,
   are each judged in the session's own tree. Both are silent with `W`
   ACTIVE. The first is silent at the base too. The second is silent where
   the base asked, but the base asked with `W` clean as well, so that ask was
   tree-blind, which this work item removes by design. §*Known limits* names
   the fallback for a switch and lists `2>&1 cd w`, but neither of these.
3. **The one-tree reason names no tree (⬜ 2).** The new §A sentence says the
   reason names each tree that matters. With one tree it still reads "in
   this tree", also when that tree is not the one the session types from.
4. **`release` is red on round 2's own record (⬜ 4).** Row 42 of
   `rounds/round-2.md` quotes the earlier finding with its red glyph in its
   Grounds, beside the verdict `confirmed`. `chain_check.py` reads that
   glyph anywhere in a row as open, so the workflow fails. This is the run's paperwork, not the
   tool.

The two equivalent survivors are equivalent (executed). The seven cut rows
without a `cd` ask or deny at the build, are silent at `3c9a1161`, and the
base asked on five of them and was silent on the two `stash` rows (executed).

At 2c3a7f92, `lint`, `ledger`, both `arm-check-grammar` legs, Ubuntu and
all four Windows shards passed, and `release` failed (⬜ 4). macOS passed too, in 17m38s. The
git-binding case, round 2's ❓, took 7.41 s on Windows shard 4 at 2c3a7f92,
against a 90 s ceiling. At 274e29bb it was in no shard's 50 slowest.

## Round 2's verdicts, answered

| Round 2 | What the fix does | Answer |
|---|---|---|
| red 1, `git rebase - <branch>` listed | `_rebase_names_a_branch` keeps a lone `-` and every word after `--` | Closed for both. `git rebase - feature/x` denies in an ACTIVE tree at the build and was silent at `3c9a1161` and at the base (executed). The class is one spelling short, which is 🟡 1 below |
| red 2, a cut git placed by its last part | `_merged_findings` returns the group's first part and glued words; `main` places the group by them | Closed. The table below (executed) |
| yellow 3, a broken reader placed a cut by the later part | `_cut_unread` returns the part before the cut and its tokens | Closed. `test_a_broken_reader_judges_a_cut_in_the_tree_before_it` passes in both broken modes (executed) |
| yellow 4, the stop hid an IDLE or unreadable second tree | `stop_unrecognised` takes `trees` and describes each that matters, or the ACTIVE ones | Closed. English and Korean texts read right (executed, below). One note on the one-tree text, ⬜ 2 |
| white 5, the git-binding case checked no exit code | the helper asserts 0, or 1 for `check-ignore` | Closed. Read, and the case passes here under git 2.50.1 (executed) |
| white 6, `spec.md` gave the old signature | corrected | Closed. Read: `spec.md:322` gives `stop_unrecognised(findings, trees, pressed, before_ask=None, switch_on_line=False)`, which is the code's |

## The questions this round was asked

### Is the new return shape of `_merged_findings` safe, and is placing by the first part right?

Yes. Every caller unpacks three fields: `main`, `_first_finding_in`, and
`_read_by_the_guard` in `tests/test_guard_resolves_the_tree_it_judges.py`.
`_cut_unread` returns the same shape. The arm test that lists
`_merged_findings` reads its source only (read).

Placing by the first part is right because the group is one command, and
bash runs it where its first part runs. Executed with the session's tree
clean, against the build, `3c9a1161`'s guard and the base's (`86cbd9a2`,
whose readers are unchanged since):

| Row of `CUT_GROUPS` | `W` dirty: build / 3c9a1161 / base | `W` ACTIVE: build / 3c9a1161 / base |
|---|---|---|
| `2>&1 git -C W switch feature/x` | ask / silent / ask | deny / silent / ask |
| `2>&1 git -C W checkout feature/x` | ask / silent / ask | deny / silent / ask |
| `git -C W worktree &>/dev/null add ../wt b` | ask / silent / ask | deny / silent / ask |
| `git -C W worktree 2>&1 add ../wt b` | ask / silent / ask | deny / silent / ask |
| `git -C W worktree 2>&1 >&2 add ../wt b` | ask / silent / ask | deny / silent / ask |
| `git -C W stash &>/dev/null branch y` | ask / silent / silent | deny / silent / silent |
| `git -C W stash 2>&1 branch y` | ask / silent / silent | deny / silent / silent |
| `cd W && 2>&1 git switch feature/x` | ask / ask / ask | deny / deny / ask |
| `cd W && git worktree 2>&1 add ../wt b` | ask / ask / ask | deny / deny / ask |

So the case goes red at `3c9a1161` on all seven rows without a `cd`, and
the build stops on every row the base stopped on. The two `cd` rows were
already right at `3c9a1161`; they pin the directory a `cd` gives, as the
docstring says. The docstring's claim that the base asked on the `switch`
and `&>` rows holds, and the base also asked on the `checkout` and both
`2>&1 … add` rows.

### Is the per-tree reason right in English and Korean?

Yes. Executed with two trees ACTIVE, the deny names each tree with its
path, and `fmt_sessions`' lines sit under each, indented once more. With the
session's tree dirty and `W` IDLE, the Korean ask reads "아래 트리마다 브랜치
전환이 문제가 됩니다." and then one line per tree, the IDLE sessions under
`W`. `TREES_EN` and `TREES_KO` match what the code prints. With the
session's tree dirty and `W` ACTIVE, the deny describes `W` alone, as the
docstring says.

One note: a reason that describes one tree still says "this tree" and no
path, which is ⬜ 2.

### Do the rebase revision spellings close the class?

Not quite. That is 🟡 1.

### Do the two survivors change nothing a case can watch?

They change nothing, for the reasons the smith gave.

- **`index - 1` in `_cut_unread`.** `walk_directories` in
  `hooks/cmdline_base.py:2083` puts the running states first across an `&`,
  so the part after a cut has the part before it as its first directory.
  Executed over six commands, including `cd W || cd /nope; …` and an `if`
  body: the first directory of the two parts was equal at every cut. A
  reserved word could have told them apart, since it wraps a part's
  directories as unresolved. But once an `if` opens, every later part is
  wrapped too (executed), so both parts read the same there as well.
- **`>&` and `<&` left out of `_OPERATORS`.** `merged_view` glues a spaced
  `>& /dev/null` into one word, `>&/dev/null`, so no word ever ends in `>&`.
  Executed: `git -C W worktree >& /dev/null add ../wt b`, `2>& /dev/null
  add …`, `stash >& /dev/null branch y` and `worktree <& 0 add …` all reach
  the guard glued and deny with `W` ACTIVE.

## 🟡 1 — `git rebase --ro feature/x` switches HEAD, and the guard lists it

**Where.** `hooks/worktree-guard.py:2245`, in `_rebase_names_a_branch`.

**What is wrong.** Round 2's fix stops dropping words at `--`. git's
parse-options has a second word that ends the options, `--end-of-options`,
and after it `git rebase` reads every word as a revision, as after `--`.
And git takes any unambiguous prefix of a long option, so `--ro` and `--roo`
are `--root`. The function asks `"--root" in args`, so it sees neither.

**Why it matters.** Executed on git 2.50.1 in copies of the `repo` fixture,
HEAD on `main`:

| Command | git | Build, ACTIVE | 3c9a1161 | Base |
|---|---|---|---|---|
| `git rebase --ro feature/x` | HEAD on `feature/x` | silent | silent | silent |
| `git rebase --roo feature/x` | HEAD on `feature/x` | silent | not run | not run |
| `git rebase --end-of-options main -x` | HEAD on `-x` | silent | silent | silent |
| `git rebase --root feature/x` | HEAD on `feature/x` | deny | not run | not run |

A silent switch over an ACTIVE session is what the Premise exists to stop.
The weight is low: neither spelling is in the recorded runs (two `rebase`
forms in all, `overview.md` *Not verified*), the base was silent on both,
and the `-x` row needs a branch whose name starts with `-`. Ledger row F3
states the threshold as closing the class, so the row would ship one
spelling short.

**Which round owns it.** The unit is round 1's, and round 2's fixes
changed it, so `round_record.py new` should read this as the run's second
fix of a fix. Under `skills/code-review/orchestration.md` §*A fix of a fix
twice sends the work item back to its framer*, that sends the work item to
its framer rather than to another fix pass. The orchestrator applies that
rule, and the home is listed under Deferred.

**The fix.** End the options at either word, and read `--root` by prefix.
Applied in this round's clone: both rows above became `deny`, and the 21
rebase and git-binding cases passed (executed). The clone was reverted.

## ⬜ 2 — A one-tree reason calls the tree "this tree", whichever tree it is

`docs/worktree-guard-spec.md:97` says the stop's reason "names each tree
that matters and why". With the session's tree clean and `W` dirty, `git -C
W checkout feature/x` asks "in this tree a branch switch would matter: it
has 1 uncommitted tracked changes" (executed). The person reads "this
tree" as their own, whose tree is clean. The decision is right, the text
predates round 2, and the docstring keeps it on purpose so the existing pins
hold. The policy sentence overstates it. Either the sentence says one tree
is described as "this tree", or the one-tree reason names the tree where it
is not the session's own.

## ⬜ 3 — Two spellings reach the session-tree fallback, and the policy names neither

`docs/worktree-guard-spec.md:793`, the bullet on a switch whose tree the
guard cannot place. Executed with the session's tree clean:

| Command | `W` ACTIVE: build / 3c9a1161 / base | `W` clean: base |
|---|---|---|
| `cd W 2>&1 && git switch feature/x` | silent / silent / silent | not run |
| `cd W &>/dev/null && git switch feature/x` | silent / silent / silent | not run |
| `cd W && if true; then 2>&1 git switch feature/x; fi` | silent / silent / ask | ask |
| `cd W && if true; then git worktree 2>&1 add ../wt b; fi` | silent / silent / ask | ask |
| `cd W && if true; then git switch feature/x; fi` | silent / silent / silent | not run |

bash runs `cd W 2>&1` in the current shell, so the next segment runs in `W`
(executed). The frozen splitter cuts at the `&`, the walk carries the
directory before the `cd` first, and the guard judges the first directory.
An `if` body's directory is unresolved, and `judgeable` falls back to the
session's tree. The base asked on the cut `if` rows with `W` clean as well,
so that ask was tree-blind, the kind of stop this work item removes by
design. A plain switch in the same position is silent at the base.

So the behaviour is the owner's rule of 2026-10-03 for a tree the guard
cannot place, and only the bullet is short. It lists `2>&1 cd w` and not
`cd w 2>&1`, and it speaks of a switch, not of an unrecognised shape in a
construct body.

## ⬜ 4 — `release` fails on a red glyph quoted in a closed row of round 2's record

`seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/rounds/round-2.md:42`.
The row is the carried closure of round 1's third finding, and its Grounds
name round 2's first finding by its red glyph and number. `open_blocking`
in `skills/code-review/scripts/chain_check.py` reads that glyph anywhere in
a row, and `confirmed` is not a closing word, so the row reads open under a
ticked `Pass`. The `release` workflow at 2c3a7f92 fails on exactly this line.

Executed in the scratch clone: `chain_check.py` failed on `round-2.md:42` at
2c3a7f92. With that one cell reading `red 1` instead, committed in the
clone, the line-42 refusal was gone. The clone was reset.

Read, not executed: `open_blocking` reads the last record only, so
`round-3.md` replaces round 2's as the one it reads. This report carries no
red glyph anywhere, so the refusal should lift when `round-3.md` lands, with or
without the correction. The correction is a paperwork fix and is not
counted in `Needs a fix`.

## Regression tests to plant

| Finding | Destination | What it asserts |
|---|---|---|
| 🟡 1 | `tests/test_worktree_guard.py`, the parameters of `test_a_rebase_naming_a_branch_is_unrecognised` | `git rebase --ro feature/x` and `git rebase --end-of-options main -x` stop with the rebase sentence. Red at 2c3a7f92 (executed: silent in an ACTIVE tree) |
| 🟡 1 | `tests/test_worktree_guard.py`, the parameters of `test_a_rebase_of_the_current_branch_stays_listed` | `git rebase --rebase-merges main` stays listed, so the prefix reading does not take every `--r` word |
| 🟡 1 | `tests/test_worktree_guard.py`, `SWITCHING` | `rebase --ro feature/x`, so the git-binding case watches git read the prefix |

## Facts for the evidence ledger

- git 2.50.1 reads `--ro` and `--roo` as `--root` for `git rebase`, and
  `git rebase --ro feature/x` leaves HEAD on `feature/x` (executed in this
  round). Row F3's threshold changes with 🟡 1.
- `git rebase --end-of-options main -x` leaves HEAD on a branch named `-x`
  (git 2.50.1, executed).
- bash runs `cd W 2>&1 && pwd` and `cd W &>/dev/null && pwd` in `W`
  (executed). The frozen walk puts the directory before that `cd` first.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `_rebase_names_a_branch` ends the options only at `--` and reads `--root` by exact match, so `git rebase --ro feature/x` and `git rebase --end-of-options main -x`, which git runs as a switch, are listed and silent in an ACTIVE tree | `hooks/worktree-guard.py:2245` | open | executed: git 2.50.1 moved HEAD in both; the build, `3c9a1161` and the base silent in an ACTIVE tree; the trial fix denies both and the 21 rebase and git-binding cases pass; a fix of a fix in a unit round 2's fixes changed, home candidate the frame |
| ⬜ 2 | §A says the stop's reason names each tree that matters, and a one-tree reason names none: `git -C W checkout feature/x` with only `W` dirty asks about "this tree" | `docs/worktree-guard-spec.md:97` | open | executed; the text predates round 2 and the decision is right |
| ⬜ 3 | §Known limits' bullet on a tree the guard cannot place names neither `cd W 2>&1 && git switch x` nor a cut git in an `if` body after `cd W`, and both are silent with `W` ACTIVE | `docs/worktree-guard-spec.md:793` | open | executed against the build, `3c9a1161` and the base; the base's ask on the `if` rows was tree-blind (it asked with `W` clean); the behaviour is the owner's rule of 2026-10-03 |
| ⬜ 4 | a carried closure quotes the earlier finding's red glyph in its Grounds beside `confirmed`, so `release` fails at 2c3a7f92 | `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/rounds/round-2.md:42` | open | executed: `chain_check.py` fails on that line, and passes it with the cell corrected; a paperwork correction, not counted in `Needs a fix` |
| 🟢 | round 2's blocking finding 1 is closed for the lone `-` and every word after `--` | `hooks/worktree-guard.py:2245` | confirmed | executed: `git rebase - feature/x` denies in an ACTIVE tree, silent at `3c9a1161` and the base; the rebase cases pass; two further spellings are this round's finding 1 |
| 🟢 | round 2's blocking finding 2 is closed — a cut git is placed by its first part and its glued words | `hooks/worktree-guard.py:2996` | confirmed | executed: the seven rows of `CUT_GROUPS` without a `cd` ask with `W` dirty and deny with `W` ACTIVE, all silent at `3c9a1161`; the base asked on five and was silent on the two `stash` rows |
| 🟢 | round 2's finding 3 is closed — a broken reader places a cut by the part before it | `hooks/worktree-guard.py:2422` | confirmed | executed through the new case in both broken modes |
| 🟢 | round 2's finding 4 is closed — the reason names each tree that matters, or the ACTIVE ones | `hooks/worktree-guard.py:2765` | confirmed | executed: two ACTIVE trees each named in the deny; an IDLE `W` beside a dirty session tree named in Korean; `TREES_EN` and `TREES_KO` match the output |
| 🟢 | round 2's note 5 is closed — the git-binding case asserts each exit code | `tests/test_worktree_guard.py:1959` | confirmed | read; the case passes under git 2.50.1 (executed) |
| 🟢 | round 2's note 6 is closed — `spec.md` gives the current signature | `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/spec.md:322` | confirmed | read |
| 🟢 | the two equivalent survivors are equivalent: `index - 1` in `_cut_unread`, and `>&` left out of `_OPERATORS` | `hooks/worktree-guard.py:2422` | confirmed | executed: the walk gave both parts of every cut the same first directory over six commands, an `if` body included; four spaced `>&` and `<&` rows reach the guard glued and deny |
| 🟢 | round 2's question on the git-binding case's Windows cost is answered | `tests/test_worktree_guard.py:1959` | confirmed | read from CI's logs: 7.41 s on Windows shard 4 at 2c3a7f92 (job 112563064324), and in no Windows shard's 50 slowest at 274e29bb (run 37546586846), against a 90 s ceiling |
| 🟢 | every pytest workflow of #850 at 2c3a7f92 passed | `gh pr checks 850` | confirmed | read: Ubuntu, macOS and Windows shards 1 to 4 passed, with `lint`, `ledger` and both `arm-check-grammar` legs; `release` failed, which is finding 4 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py -q --durations=6` in this round's clone at 2c3a7f92 | 235 passed in 5.41 s; `test_no_listed_form_moves_head_under_git` 2.37 s, `test_a_cut_group_is_judged_in_the_tree_its_own_c_names` 1.30 s |
| a deleted probe loading the build's guard, `3c9a1161`'s and the base's (`git show` of each, kept outside `hooks/`; the readers they import are unchanged since `86cbd9a2`), with `sessions_in_tree` stubbed per tree | the `CUT_GROUPS` table; the ⬜ 3 table; the reason texts in both languages; the first directories of both parts of each cut; the spaced `>&` and `<&` rows |
| the same probe driving git 2.50.1 and bash in copies of the `repo` fixture | the 🟡 1 table; `cd W 2>&1 && pwd` and `cd W &>/dev/null && pwd` print `W` |
| 🟡 1's fix applied in the clone, the probe rerun, then `bin/test tests/test_worktree_guard.py -q -k "rebase or listed_form or carries_its_counts"` | both spellings deny; 21 passed. The clone was reverted |
| `chain_check.py --baseline origin/release/v0.20.0` in the clone, at 2c3a7f92 and again with row 42's cell corrected and committed there | line 42 refused, then not refused; the other refusals it printed are those of a ready pull request, which a draft only notices. The clone was reset to 2c3a7f92 |
| `gh pr checks 850`, read until the last leg ended, and the failed `release` job's log | `release` failed on `round-2.md:42`; `lint`, `ledger`, both `arm-check-grammar` legs, Ubuntu, macOS and Windows shards 1 to 4 passed. The scratch clone and the probe were deleted afterwards |
| the four Windows jobs' logs at 2c3a7f92 (`gh api …/actions/jobs/<id>/logs`) | 2686, 6731, 915 and 2227 passed; `test_no_listed_form_moves_head_under_git` 7.41 s on shard 4 |
| `gh run view 37546586846 --log`, the `tests` run at 274e29bb | every leg succeeded; the git-binding case was in no shard's 50 slowest |
| the full suite, the repository-wide lint, the typecheck (the broad gate) | not yet: the sealer's act, after the rounds settle. This record ends the run, so it comes due once the orchestrator has taken 🟡 1 to its home |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — `git rebase --ro <branch>` and `--end-of-options` are listed | candidate home: the frame, as the run's second fix of a fix (`skills/code-review/orchestration.md` §*A fix of a fix twice sends the work item back to its framer*); the orchestrator applies the count | the framer, re-spawned with the run's round records, or the orchestrator where it reads the count otherwise |
| P5 — whether an unrecognised shape in an ACTIVE tree is denied whatever the press | `questions.md` P5, already deferred in round 1 | the repository owner, at the pull request |

## Paste-ready fixes

### 🟡 1

```python
# hooks/worktree-guard.py, _rebase_names_a_branch, the body:
    words = _plain_words(args)
    end = next(
        (i for i, w in enumerate(words) if w in ("--", "--end-of-options")),
        len(words),
    )
    plain = [w for w in words[:end] if w == "-" or not w.startswith("-")]
    plain += words[end + 1 :]
    # git takes any unambiguous prefix of a long option, so `--ro` is
    # `--root` (git 2.50.1; round 3 of work item 1791270162).
    root = any(w.startswith("--r") and "--root".startswith(w) for w in words[:end])
    return len(plain) >= (1 if root else 2)
```

```python
# tests/test_worktree_guard.py, test_a_rebase_naming_a_branch_is_unrecognised:
# two more parameters.
        "git rebase --ro feature/x",
        "git rebase --end-of-options main -x",

# test_a_rebase_of_the_current_branch_stays_listed: one more.
        "git rebase --rebase-merges main",

# SWITCHING: one more form.
    "rebase --ro feature/x",
```

```markdown
docs/worktree-guard-spec.md §A, the rebase sentence's last clause becomes:

A lone `-` is a word, since git reads it as `@{-1}`, and so is every word
after a `--` or an `--end-of-options`: `git rebase - feature/x` switches
too. git takes a prefix of `--root` (`--ro`) as `--root`, and so does the
guard.
```

### ⬜ 2

```markdown
docs/worktree-guard-spec.md §A, the sentence at line 97 becomes:

The stop's reason names each tree that matters and why, its changes, its
IDLE sessions or its detection unusable, because approving the `ask` runs
the line in every one of them; a reason that describes one tree calls it
"this tree", and where one is ACTIVE, the reason describes the ACTIVE trees
alone.
```

### ⬜ 3

```markdown
docs/worktree-guard-spec.md §Known limits, the bullet at line 793, after
"`cd "$W"` with `W` unset, and `2>&1 cd w`":

, and `cd w 2>&1`, whose `&` the frozen splitter cuts so the walk keeps
the directory before the `cd` first. An unrecognised shape the walk cannot
place takes the same fallback: a cut git inside an `if` body after `cd w`
(`cd w && if …; then 2>&1 git switch x; fi`) is judged in the session's
own tree, where the guard before #826 asked in every tree.
```

### ⬜ 4

```markdown
seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/rounds/round-2.md:42,
the Grounds cell ends:

executed through the new cases; the lone `-` is red 1 of this round
```

Needs a fix: yes — 🟡 1: `git rebase --ro <branch>` and `git rebase --end-of-options <upstream> <branch>` switch HEAD and are listed, so each is silent in an ACTIVE tree

Loses a record or crashes: no

## Proof

Files opened in this round, in the round's clone at 2c3a7f92 unless named:

- `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/`:
  `rounds/round-2.md`, `rounds/round-2-report.md`, `overview.md`,
  `survivors.md`, and `git diff 3c9a1161..a3164380` of `spec.md`
- `seal/ledger/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest.md`:
  row F3 (by search)
- `hooks/worktree-guard.py`: 160–186, 596–640, 1296–1321, 1417–1440,
  2130–2530, 2700–3075, and `git diff 3c9a1161..a3164380` of it
- `hooks/cmdline_base.py`: 1950–2149
- `docs/worktree-guard-spec.md`: 665–700, 781–860, and `git diff
  3c9a1161..a3164380` of it
- `docs/review-chain-spec.md`: 76–130, 377–420, 494–560
- `skills/code-review/orchestration.md`: §*A fix of a fix twice sends the
  work item back to its framer*
- `skills/code-review/scripts/chain_check.py`: 399, 1706–1742, and its
  readers' `git show HEAD:` lines (by search)
- `tests/test_worktree_guard.py`: 1–40, 1095–1150, 2030–2045, and `git diff
  3c9a1161..a3164380` of it
- `tests/test_guard_resolves_the_tree_it_judges.py`: `git diff
  3c9a1161..a3164380`
- `tests/conftest.py`: 540–565, 820–850
- `bin/test`
- the base guard and `3c9a1161`'s, by `git show`, loaded and not read line
  by line
- `gh pr checks 850`, `gh pr view 850`, `gh run list` for the branch, the
  failed `release` job's log, and run 37546586846's log
- the reviewer's instructions: the agent contract, `code-review`, and the
  writing-style skill
